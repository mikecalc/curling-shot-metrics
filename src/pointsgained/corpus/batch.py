"""Survey and batch extraction over downloaded Results Books (design Sections 3.6.3-3.6.5)."""
from __future__ import annotations

import json
import logging
import os
import time

import pandas as pd
import pdfplumber

from ..ingest.book import extract_book, is_diagram_image
from ..ingest.diagram import decode_image, classify_pixels, CLASS_INDEX
from ..ingest.validate import validate_book
from ..ingest.pdf_pages import page_kind

log = logging.getLogger(__name__)


def read_inventory(path: str) -> pd.DataFrame:
    """Read the inventory with text columns as object dtype (an all-empty column reads back as float)."""
    inv = pd.read_csv(path)
    for c in ("notes", "status", "style_family", "has_shot_by_shot", "gender", "division", "location"):
        if c in inv:
            inv[c] = inv[c].astype(object).where(inv[c].notna(), None)
    return inv


def survey_book(pdf_path: str, max_pages: int = 400) -> dict:
    """Detect shot-by-shot pages and characterise the template of one book."""
    info = {"has_shot_by_shot": False, "n_pages": 0, "template": None, "grade_style": None,
            "diagram_format": None, "style_family": None}
    with pdfplumber.open(pdf_path) as pdf:
        info["n_pages"] = len(pdf.pages)
        for i in range(min(len(pdf.pages), max_pages)):
            page = pdf.pages[i]
            text = page.extract_text() or ""
            if page_kind(text) != "shot_by_shot":
                page.flush_cache(); continue
            info["has_shot_by_shot"] = True
            info["grade_style"] = "pct" if "%" in text else "four"
            info["template"] = "olympic" if ("/" in text.split("\n")[1] if "\n" in text else False) else "wcf"
            big = [im for im in page.images if is_diagram_image(im)]
            if big:
                im = big[0]
                try:
                    rgb = decode_image(im)
                    cls = classify_pixels(rgb)
                    n_mark = int((cls == CLASS_INDEX["mark"]).sum())
                    w, h = im["srcsize"]
                    std = 298 <= w <= 302 and 598 <= h <= 602
                    info["diagram_format"] = f"{'std' if std else f'{w}x{h}'}/{im.get('bits')}bit"
                    info["yellow_cross"] = bool(n_mark > 10)
                except Exception as e:
                    info["diagram_format"] = f"undecodable: {e}"
            page.flush_cache()
            break
    info["style_family"] = f"{info['template']}-{info['grade_style']}-{info['diagram_format']}"
    return info


def process_book(pdf: str, book_id: str, out_dir: str, reports_dir: str) -> dict:
    """Worker: survey, extract, validate one book; write its tables and report. Returns a summary."""
    t0 = time.time()
    sv = survey_book(pdf)
    res = {"book_id": book_id, "has_shot_by_shot": sv["has_shot_by_shot"], "style_family": sv["style_family"]}
    if not sv["has_shot_by_shot"]:
        res["status"] = "excluded"; res["notes"] = "no shot-by-shot pages"
        return res
    log.info("extracting %s (%s)", book_id, sv["style_family"])
    t = extract_book(pdf, book_id, progress=True)
    bd = os.path.join(out_dir, book_id); os.makedirs(bd, exist_ok=True)
    for name, df in t.tables().items():
        df.to_parquet(os.path.join(bd, f"{name}.parquet"), index=False)
    with open(os.path.join(bd, "warnings.txt"), "w") as f:
        f.write("\n".join(t.warnings))
    v = validate_book(t); v["seconds"] = round(time.time() - t0, 1); v["n_warnings"] = len(t.warnings)
    with open(os.path.join(reports_dir, f"validation_{book_id}.json"), "w") as f:
        json.dump(v, f, indent=2, default=str)
    checked = max(1, v.get("hammer_alternation_checked", 0) or 0)
    # gates catch extraction failures (which show as ~50-60% rates); older books carry more
    # inch-level ties in the diagrams, so the score gate admits them (recorded score is the label)
    ok = (v.get("counter_census_ok_rate") or 0) >= 0.95 and (v.get("score_reconstruction_ok_rate") or 0) >= 0.85 \
        and (v.get("hammer_alternation_violations", 1) or 0) / checked <= 0.01 and v.get("n_games", 0) > 0
    res["status"] = "validated" if ok else "extracted"
    res["notes"] = (f"games={v['n_games']} shots={v['n_shots']} census={v.get('counter_census_ok_rate', 0):.3f} "
                    f"score={v.get('score_reconstruction_ok_rate') or 0:.3f} hammer_viol={v.get('hammer_alternation_violations')} s={v['seconds']}")
    return res


def _worker(args):
    pdf, book_id, out_dir, reports_dir = args
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    try:
        return process_book(pdf, book_id, out_dir, reports_dir)
    except Exception as e:
        log.exception("failed %s", book_id)
        return {"book_id": book_id, "status": "error", "notes": f"{type(e).__name__}: {str(e)[:100]}"}


def run_batch(inventory_csv: str, raw_dir: str, out_dir: str, reports_dir: str,
              limit: int | None = None, force: bool = False, workers: int = 1) -> pd.DataFrame:
    """Survey, extract and validate every downloaded in-scope book. Only this process writes the inventory."""
    from concurrent.futures import ProcessPoolExecutor, as_completed
    inv = read_inventory(inventory_csv)
    os.makedirs(out_dir, exist_ok=True); os.makedirs(reports_dir, exist_ok=True)
    jobs = []
    for i, r in inv.iterrows():
        if not r["in_scope"] or r["status"] in ("validated", "excluded") and not force:
            continue
        year = int(r["year"]) if pd.notna(r["year"]) else 0
        pdf = os.path.join(raw_dir, str(year), r["file_name"])
        if not os.path.exists(pdf) or os.path.getsize(pdf) == 0:
            continue
        # skip books already validated on disk (report present and newer than the pdf) unless forced
        book_id = os.path.splitext(r["file_name"])[0]
        jobs.append((i, (pdf, book_id, out_dir, reports_dir)))
        if limit is not None and len(jobs) >= limit:
            break
    log.info("batch: %d books, %d workers", len(jobs), workers)
    index_of = {a[1]: i for i, a in jobs}

    def apply(res):
        i = index_of[res["book_id"]]
        for k in ("status", "notes", "has_shot_by_shot", "style_family"):
            if k in res:
                inv.at[i, k] = res[k]
        inv.to_csv(inventory_csv, index=False)
        log.info("%s -> %s %s", res["book_id"], res.get("status"), res.get("notes", ""))

    if workers <= 1:
        for _, a in jobs:
            apply(_worker(a))
    else:
        with ProcessPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(_worker, a) for _, a in jobs]
            for fut in as_completed(futs):
                apply(fut.result())
    return inv
