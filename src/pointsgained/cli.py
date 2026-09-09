"""Command line interface: pointsgained ingest | validate | audit."""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time

import pandas as pd


def cmd_ingest(args):
    from .ingest.book import extract_book
    from .ingest.validate import validate_book
    os.makedirs(args.out, exist_ok=True)
    os.makedirs(args.reports, exist_ok=True)
    for pdf in args.pdfs:
        t0 = time.time()
        book_id = os.path.splitext(os.path.basename(pdf))[0]
        logging.info("extracting %s", book_id)
        t = extract_book(pdf, book_id, max_pages=args.max_pages, progress=True)
        outdir = os.path.join(args.out, book_id)
        os.makedirs(outdir, exist_ok=True)
        for name, df in t.tables().items():
            df.to_parquet(os.path.join(outdir, f"{name}.parquet"), index=False)
        with open(os.path.join(outdir, "warnings.txt"), "w") as f:
            f.write("\n".join(t.warnings))
        v = validate_book(t)
        v["seconds"] = round(time.time() - t0, 1)
        v["n_warnings"] = len(t.warnings)
        with open(os.path.join(args.reports, f"validation_{book_id}.json"), "w") as f:
            json.dump(v, f, indent=2, default=str)
        summary = {k: v[k] for k in v if k != "score_mismatches"}
        print(json.dumps(summary, indent=2, default=str))


def cmd_validate(args):
    from .ingest.validate import validate_book
    for book_dir in args.books:
        tabs = {n: pd.read_parquet(os.path.join(book_dir, f"{n}.parquet"))
                for n in ("pages", "games", "ends", "shots", "stones", "line_scores", "players")}
        v = validate_book(tabs)
        v["book"] = os.path.basename(book_dir)
        print(json.dumps({k: v[k] for k in v if k != "score_mismatches"}, indent=2, default=str))


def cmd_audit(args):
    """Contact sheet: random panels with detected stones overlaid."""
    import random
    import pdfplumber
    from PIL import Image, ImageDraw
    from .ingest import diagram as D
    from .ingest.panel_text import panel_index_from_image
    from .ingest.book import is_diagram_image
    random.seed(args.seed)
    tiles = []
    for pdf_path in args.pdfs:
        with pdfplumber.open(pdf_path) as pdf:
            n = len(pdf.pages)
            cand = list(range(n))
            random.shuffle(cand)
            got = 0
            for pi in cand:
                page = pdf.pages[pi]
                text = page.extract_text() or ""
                if "Shot by Shot" not in text:
                    page.flush_cache(); continue
                big = [im for im in page.images if is_diagram_image(im)]
                if not big:
                    page.flush_cache(); continue
                im = random.choice(big)
                idx = panel_index_from_image(im["x0"], im["top"])
                rgb = D.decode_image(im)
                dg = D.read_diagram(rgb)
                if dg.flipped:
                    rgb = rgb[::-1, ::-1]
                img = Image.fromarray(rgb).convert("RGB")
                dr = ImageDraw.Draw(img)
                for s in dg.stones:
                    r = 11
                    dr.ellipse([s.col - r, s.row - r, s.col + r, s.row + r], outline=(0, 160, 0) if not s.delivered else (255, 0, 255), width=2)
                for p in dg.priors:
                    dr.rectangle([p.col - 6, p.row - 6, p.col + 6, p.row + 6], outline=(0, 0, 0), width=1)
                c = dg.counters
                label = f"{os.path.basename(pdf_path)[:8]} p{pi+1} #{idx}{' F' if dg.flipped else ''} R{c['red_remaining']}/{c['red_removed']} Y{c['yellow_remaining']}/{c['yellow_removed']}"
                dr.text((4, 602 if img.height > 601 else 585), label, fill=(0, 0, 0))
                tiles.append(img.resize((200, 400)))
                got += 1
                page.flush_cache()
                if got >= args.per_book:
                    break
    cols = 8
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 200, rows * 400), "white")
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * 200, (i // cols) * 400))
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    sheet.save(args.out)
    print(f"wrote {args.out} with {len(tiles)} panels")


def cmd_model(args):
    """Phase 1 pipeline: positions -> value set -> WP table -> f/g -> Points Gained -> leaderboards."""
    import numpy as np
    from .model.dataset import load_books, build_dataset
    from .model.value import ValueSet, HammerAdjustedPoints, OUTCOMES
    from .model.winprob import ends_from_line_scores, build_table, WinProbability
    from .model.train import fit_models
    from .model.pg import compute_points_gained, conservation_check
    from .model import aggregate as agg
    os.makedirs(args.reports, exist_ok=True)
    t0 = time.time()
    tabs = load_books(args.parquet)
    logging.info("loaded %d games, %d ends, %d shots", len(tabs["games"]), len(tabs["ends"]), len(tabs["shots"]))
    ds = build_dataset(tabs, mirror=not args.no_mirror)
    logging.info("dataset: %d rows (%d unmirrored) in %.0fs", len(ds.rows), int((ds.rows["mirror"] == 0).sum()), time.time() - t0)
    rep = {"n_games": int(len(tabs["games"])), "n_ends": int(len(tabs["ends"])), "n_shots": int(len(tabs["shots"])),
           "n_rows": int(len(ds.rows))}

    # value set per discipline from the end outcomes seen in shot-by-shot ends
    first = ds.rows[(ds.rows["mirror"] == 0) & (ds.rows["shot"] == 1)]
    vs_all = ValueSet.from_outcomes(first["label"])
    rep["hammer_outcome_dist"] = dict(zip([int(o) for o in OUTCOMES], vs_all.dist.round(4).tolist()))
    rep["N_all"], rep["H_all"] = round(vs_all.N, 4), round(vs_all.H, 4)
    for d, grp in first.groupby("discipline"):
        vs = ValueSet.from_outcomes(grp["label"])
        rep[f"N_{d}"], rep[f"H_{d}"], rep[f"ends_{d}"] = round(vs.N, 4), round(vs.H, 4), int(len(grp))

    # win-probability table from line scores
    er = ends_from_line_scores(tabs["line_scores"])
    rep["line_score_ends"] = int(len(er))
    wpt = build_table(er) if len(er) else None
    if wpt is not None:
        rep["wp_tied_start_with_hammer"] = round(wpt.P(0, 10, 1), 4)
        rep["wp_examples"] = {f"d={d},n={n},h={h}": round(wpt.P(d, n, h), 3)
                              for d, n, h in [(0, 10, 1), (0, 5, 1), (1, 5, 0), (-1, 5, 1), (2, 3, 0), (0, 1, 1), (0, 1, 0), (-2, 2, 1)]}
        rep["regimes"] = {f"d={d},n={n}": wpt.regime(d, n) for d, n in [(0, 10), (0, 1), (-1, 1), (1, 2), (-2, 3), (3, 4)]}

    models = fit_models(ds.rows, ds.X, ds.y, seed=args.seed)
    rep["cv"] = models.cv_report
    logging.info("models fitted in %.0fs; f logloss %.4f vs trivial %.4f", time.time() - t0,
                 models.cv_report["f_logloss"], models.cv_report["trivial_logloss"])

    vm = HammerAdjustedPoints(vs_all.H)
    pg = compute_points_gained(ds, models, vm)
    cons = conservation_check(pg, vm)
    rep["conservation_max_abs_residual"] = float(cons["residual"].abs().max())
    rep["conservation_terminal_ok_rate"] = float(cons["terminal_is_actual"].mean())
    # calibration check: V(f(S0)) should be near H (empty sheet, hammer perspective)
    s0 = pg[pg["shot"] == 1]
    rep["V_S0_mean"] = round(float(s0["V_pre"].mean()), 4)
    rep["H_used"] = round(vs_all.H, 4)
    if wpt is not None:
        from .model.pg import situation_lookup
        sit = situation_lookup(tabs)
        cache = {}
        def vm_wp(gk, e):
            d, n = sit.get((gk, e), (0, 10))
            key = (d, n)
            if key not in cache:
                cache[key] = WinProbability(wpt, d, n)
            return cache[key]
        pg_wp = compute_points_gained(ds, models, vm, vm_by_situation=vm_wp)
        for c in ("pg", "pg_call", "pg_throw", "V_pre"):
            pg[f"{c}_wp"] = pg_wp[c].values
        rep["wp_pg_abs_mean"] = round(float(pg["pg_wp"].abs().mean()), 4)
    pg.to_parquet(os.path.join(args.parquet, "points_gained.parquet"), index=False)
    cons.to_parquet(os.path.join(args.parquet, "conservation.parquet"), index=False)

    lb = {"players": agg.by_player(pg, min_shots=args.min_shots), "teams": agg.by_team(pg),
          "shot_types": agg.by_shot_type(pg), "shot_numbers": agg.by_shot_number(pg)}
    for k, df in lb.items():
        df.to_csv(os.path.join(args.reports, f"leaderboard_{k}.csv"), index=False)
    with open(os.path.join(args.reports, "model_report.json"), "w") as f:
        json.dump(rep, f, indent=2, default=str)
    with open(os.path.join(args.reports, "model_report.md"), "w") as f:
        f.write("# Points Gained: Phase 1 model report\n\n")
        f.write(f"Games {rep['n_games']}, ends {rep['n_ends']}, shots {rep['n_shots']}, training rows {rep['n_rows']}.\n\n")
        f.write(f"Hammer outcome distribution (hammer perspective, clipped): {rep['hammer_outcome_dist']}\n\n")
        f.write(f"N (hammer net) = {rep['N_all']}, H (Markov hammer value) = {rep['H_all']}\n\n")
        for d in ("M", "W"):
            if f"N_{d}" in rep:
                f.write(f"- {d}: N = {rep[f'N_{d}']}, H = {rep[f'H_{d}']} over {rep[f'ends_{d}']} ends\n")
        f.write("\n## Cross-validated outcome models (held out by book)\n\n")
        cv = rep["cv"]
        f.write("| model | log-loss | Brier |\n|---|---|---|\n")
        for m in ("trivial", "f", "g"):
            f.write(f"| {m} | {cv[m + '_logloss']:.4f} | {cv[m + '_brier']:.4f} |\n")
        f.write("\nLog-loss by rocks remaining (f vs trivial):\n\n| rocks remaining | n | f | trivial |\n|---|---|---|---|\n")
        for r, v in sorted(cv["logloss_by_rocks_remaining"].items()):
            f.write(f"| {r} | {v['n']} | {v['f']} | {v['trivial']} |\n")
        f.write(f"\n## Conservation\n\nMax |sum PG - (final - start)| over ends: {rep['conservation_max_abs_residual']:.2e}; ")
        f.write(f"terminal distribution equals the actual score in {100 * rep['conservation_terminal_ok_rate']:.1f}% of ends.\n\n")
        f.write(f"Mean V(f(S0)) = {rep['V_S0_mean']} versus H = {rep['H_used']} (calibration check).\n\n")
        if wpt is not None:
            f.write("## Win probability (from line scores)\n\n")
            for k, v in rep["wp_examples"].items():
                f.write(f"- {k}: {v}\n")
            f.write("\nRegimes: " + "; ".join(f"{k}: {v}" for k, v in rep["regimes"].items()) + "\n\n")
        f.write("## Leaderboards\n\n### Shot types\n\n" + lb["shot_types"].round(3).to_markdown(index=False) + "\n\n")
        f.write("### Players (PG: Throw per shot, min %d shots)\n\n" % args.min_shots + lb["players"].head(25).round(3).to_markdown(index=False) + "\n\n")
        f.write("### Teams\n\n" + lb["teams"].round(3).to_markdown(index=False) + "\n")
    print(json.dumps({k: v for k, v in rep.items() if k not in ("cv",)}, indent=2, default=str))
    print(json.dumps({k: v for k, v in rep["cv"].items() if k not in ("calibration_f", "logloss_by_rocks_remaining")}, indent=2))
    print(f"wrote {args.reports}/model_report.md in {time.time() - t0:.0f}s")


def cmd_inventory(args):
    from .corpus.inventory import build_inventory
    html = open(args.html).read() if args.html else None
    df = build_inventory(args.out, html=html, check=args.check)
    print(f"{len(df)} links, {(df['doc_type'] == 'ResultsBook').sum()} results books, {int(df['in_scope'].sum())} in scope -> {args.out}")
    print(df[df["in_scope"]].groupby(["event_family", "tier"]).size().to_string())


def cmd_download(args):
    from .corpus.download import download_books
    inv = download_books(args.inventory, args.raw, delay=args.delay, limit=args.limit, tiers=args.tiers)
    print(inv["status"].value_counts().to_string())


def cmd_batch(args):
    from .corpus.batch import run_batch
    inv = run_batch(args.inventory, args.raw, args.out, args.reports, limit=args.limit, force=args.force)
    print(inv[inv["in_scope"] == True]["status"].value_counts().to_string())


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    p = argparse.ArgumentParser(prog="pointsgained")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ingest", help="extract Results Book PDFs to Parquet")
    a.add_argument("pdfs", nargs="+")
    a.add_argument("--out", default="data/parquet")
    a.add_argument("--reports", default="reports")
    a.add_argument("--max-pages", type=int, default=None)
    a.set_defaults(func=cmd_ingest)
    b = sub.add_parser("validate", help="re-run validation gates on extracted books")
    b.add_argument("books", nargs="+")
    b.set_defaults(func=cmd_validate)
    c = sub.add_parser("audit", help="contact sheet of random panels with detections overlaid")
    c.add_argument("pdfs", nargs="+")
    c.add_argument("--per-book", type=int, default=8)
    c.add_argument("--seed", type=int, default=0)
    c.add_argument("--out", default="reports/audit.png")
    c.set_defaults(func=cmd_audit)
    d = sub.add_parser("model", help="fit Phase 1 models and compute Points Gained")
    d.add_argument("--parquet", default="data/parquet")
    d.add_argument("--reports", default="reports")
    d.add_argument("--seed", type=int, default=0)
    d.add_argument("--min-shots", type=int, default=40)
    d.add_argument("--no-mirror", action="store_true")
    d.set_defaults(func=cmd_model)
    e = sub.add_parser("inventory", help="build the inventory of the curlit results directory")
    e.add_argument("--out", default="data/inventory.csv")
    e.add_argument("--html", default=None, help="parse a saved copy of the results page instead of fetching")
    e.add_argument("--check", action="store_true", help="HEAD-check every in-scope URL")
    e.set_defaults(func=cmd_inventory)
    f = sub.add_parser("download", help="download in-scope results books listed in the inventory")
    f.add_argument("--inventory", default="data/inventory.csv")
    f.add_argument("--raw", default="data/raw")
    f.add_argument("--delay", type=float, default=3.0)
    f.add_argument("--limit", type=int, default=None)
    f.add_argument("--tiers", type=int, nargs="*", default=None)
    f.set_defaults(func=cmd_download)
    g = sub.add_parser("batch", help="survey, extract and validate every downloaded in-scope book")
    g.add_argument("--inventory", default="data/inventory.csv")
    g.add_argument("--raw", default="data/raw")
    g.add_argument("--out", default="data/parquet")
    g.add_argument("--reports", default="reports")
    g.add_argument("--limit", type=int, default=None)
    g.add_argument("--force", action="store_true")
    g.set_defaults(func=cmd_batch)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
