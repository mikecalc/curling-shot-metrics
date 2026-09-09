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


def run_batch(inventory_csv: str, raw_dir: str, out_dir: str, reports_dir: str,
              limit: int | None = None, force: bool = False) -> pd.DataFrame:
    inv = pd.read_csv(inventory_csv)
    os.makedirs(out_dir, exist_ok=True); os.makedirs(reports_dir, exist_ok=True)
    n = 0
    for i, r in inv.iterrows():
        if not r["in_scope"] or r["status"] not in ("downloaded", "surveyed", "extracted", "validated", "error"):
            continue
        if r["status"] in ("validated", "excluded") and not force:
            continue
        year = int(r["year"]) if pd.notna(r["year"]) else 0
        pdf = os.path.join(raw_dir, str(year), r["file_name"])
        if not os.path.exists(pdf):
            continue
        if limit is not None and n >= limit:
            break
        n += 1
        book_id = os.path.splitext(r["file_name"])[0]
        t0 = time.time()
        try:
            sv = survey_book(pdf)
            inv.at[i, "has_shot_by_shot"] = sv["has_shot_by_shot"]
            inv.at[i, "style_family"] = sv["style_family"]
            if not sv["has_shot_by_shot"]:
                inv.at[i, "status"] = "excluded"; inv.at[i, "notes"] = "no shot-by-shot pages"
                inv.to_csv(inventory_csv, index=False)
                continue
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
            ok = (v.get("counter_census_ok_rate") or 0) >= 0.99 and (v.get("score_reconstruction_ok_rate") or 0) >= 0.9 \
                and v.get("hammer_alternation_violations", 1) == 0 and v.get("n_games", 0) > 0
            inv.at[i, "status"] = "validated" if ok else "extracted"
            inv.at[i, "notes"] = (f"games={v['n_games']} shots={v['n_shots']} census={v.get('counter_census_ok_rate', 0):.3f} "
                                  f"score={v.get('score_reconstruction_ok_rate') or 0:.3f} hammer_viol={v.get('hammer_alternation_violations')}")
        except Exception as e:
            inv.at[i, "status"] = "error"; inv.at[i, "notes"] = f"{type(e).__name__}: {str(e)[:100]}"
            log.exception("failed %s", book_id)
        inv.to_csv(inventory_csv, index=False)
    return inv
