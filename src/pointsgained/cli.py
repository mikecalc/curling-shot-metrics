"""Command line interface: pointsgained ingest | validate | audit | model | features | experiment | events | inventory | download | batch."""
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


def cmd_features(args):
    """Build (or refresh) the feature cache: one row per shot and mirror with strata, situation, label and features."""
    from .model.cache import load_or_build
    ds = load_or_build(args.parquet, mirror=not args.no_mirror, rebuild=args.rebuild)
    print(f"{len(ds.rows)} rows, {len(ds.stones)} stones -> {args.parquet}/features.parquet")


def _feature_sets(spec: str) -> tuple[str, ...]:
    return tuple(s.strip() for s in spec.split(",") if s.strip())


def _with_level(ds, sets, parquet_root, aliases_csv, event_strength_csv="data/event_strength.csv"):
    """Attach the level columns (event rating; or the per-player skill sets) and the intent columns when requested."""
    if "level" in sets:
        es = pd.read_csv(event_strength_csv).set_index("book")["rating"] if os.path.exists(event_strength_csv) else pd.Series(dtype=float)
        ds.rows = ds.rows.assign(event_rating=es.reindex(ds.rows["book"].to_numpy()).fillna(float(es.median()) if len(es) else 85.0).to_numpy(dtype=float))
    if "level_player" in sets or "level_id" in sets:
        from .model.difficulty import load_level
        ds.rows = load_level(parquet_root, ds.rows, aliases_csv)
    if "intent" in sets:
        from .model.intent import attach_intent
        ds.rows = attach_intent(ds.rows, pd.read_parquet(os.path.join(parquet_root, "intent.parquet")))
    return ds


def cmd_intent(args):
    """Realised intent per shot from the delivered stone and prior rings (design Section 6) -> intent.parquet."""
    from .model.dataset import load_books
    from .model.cache import load_or_build
    from .model.intent import realised_intent, apply_target_model
    t0 = time.time()
    tabs = load_books(args.parquet)
    it = realised_intent(tabs)
    ds = load_or_build(args.parquet)
    it = apply_target_model(it, ds.rows, ds.X, seed=args.seed)
    it.to_parquet(os.path.join(args.parquet, "intent.parquet"), index=False)
    # Phase 2 seed: delivered-stone error relative to the modal target (design Section 11)
    from .model.intent import execution_error_summary
    skill = None
    if os.path.exists(os.path.join(args.parquet, "skill.parquet")):
        from .model.difficulty import load_level
        skill = load_level(args.parquet, ds.rows, args.aliases)["skill_thrower"].to_numpy()
    err = execution_error_summary(it, ds.rows, skill)
    os.makedirs(args.reports, exist_ok=True)
    with open(os.path.join(args.reports, "execution_error.md"), "w") as f:
        f.write("# Delivered-stone error relative to the modal target (draw family)\n\n"
                "Seed for the Phase 2 execution error model. Lateral error is |x_rest - x_target|, depth error is "
                "y_rest - y_target (positive towards the hog line), inches; the target is the modal cell centre, so "
                "part of the spread is the cell's coarseness. Rows by grade, thrower skill tercile and rocks-remaining band.\n\n")
        f.write(err.to_markdown(index=False) + "\n")
    books = tabs["games"].drop_duplicates("game_key").set_index("game_key")["book"]
    it["year"] = it["game_key"].map(books).str.extract(r"(20\d\d)")[0]
    cov = it.groupby(["year", "family"])["target_known"].mean().unstack("family").round(3)
    print(cov.to_string())
    print(f"{len(it)} shots, target known {it['target_known'].mean():.3f} -> {args.parquet}/intent.parquet in {time.time() - t0:.0f}s")


def cmd_experiment(args):
    """Fit f, g and the trivial model once on one split and score the held-out rows."""
    from .model.cache import load_or_build
    from .model.experiment import run_experiment
    sets = _feature_sets(args.features)
    ds = _with_level(load_or_build(args.parquet, rebuild=args.rebuild), sets, args.parquet, args.aliases)
    name = args.name or f"{args.split}_{'+'.join(sets)}"
    rep = run_experiment(ds, name, sets, split=args.split, cutoff_year=args.cutoff_year, fold=args.fold,
                         seed=args.seed, reports=args.reports, inventory_csv=args.inventory)
    print(json.dumps({k: rep[k] for k in ("name", "split", "sets", "n_train", "n_test", "trivial_logloss", "f_logloss", "g_logloss", "seconds")}, indent=2))
    print("by rocks remaining:", {r: (v["f"], v["trivial"]) for r, v in rep["logloss_by_rocks_remaining"].items()})
    if "logloss_by_abs_diff" in rep:
        print("by |diff|:", {d: (v["f"], v["trivial"]) for d, v in rep["logloss_by_abs_diff"].items()})


def cmd_model(args):
    """Phase 1 pipeline: feature cache -> value set -> WP table -> f/g -> Points Gained -> leaderboards."""
    from .model.cache import load_or_build
    from .model.dataset import load_books
    from .model.value import ValueSet, HammerAdjustedPoints, OUTCOMES
    from .model.winprob import ends_from_line_scores, build_table
    from .model.train import fit_models
    from .model.pg import compute_points_gained, conservation_check
    from .model import aggregate as agg
    os.makedirs(args.reports, exist_ok=True)
    t0 = time.time()
    sets = _feature_sets(args.features)
    ds = _with_level(load_or_build(args.parquet, mirror=not args.no_mirror, rebuild=args.rebuild), sets, args.parquet, args.aliases)
    rep = {"n_games": int(ds.rows["game_key"].nunique()), "n_ends": int(ds.rows.groupby(["game_key", "end"]).ngroups),
           "n_shots": int((ds.rows["mirror"] == 0).sum()), "n_rows": int(len(ds.rows)), "feature_sets": list(sets)}
    logging.info("dataset: %d rows (%d shots) in %.0fs", rep["n_rows"], rep["n_shots"], time.time() - t0)

    # value set per discipline from the end outcomes seen in shot-by-shot ends
    first = ds.rows[(ds.rows["mirror"] == 0) & (ds.rows["shot"] == 1)]
    vs_all = ValueSet.from_outcomes(first["label"])
    rep["hammer_outcome_dist"] = dict(zip([int(o) for o in OUTCOMES], vs_all.dist.round(4).tolist()))
    rep["N_all"], rep["H_all"] = round(vs_all.N, 4), round(vs_all.H, 4)
    for d, grp in first.groupby("discipline"):
        vs = ValueSet.from_outcomes(grp["label"])
        rep[f"N_{d}"], rep[f"H_{d}"], rep[f"ends_{d}"] = round(vs.N, 4), round(vs.H, 4), int(len(grp))

    # win-probability table from line scores (every book, including those without shot-by-shot pages)
    tabs = load_books(args.parquet)
    er = ends_from_line_scores(tabs["line_scores"])
    rep["line_score_ends"] = int(len(er))
    wpt = build_table(er) if len(er) else None
    if wpt is not None:
        rep["wp_tied_start_with_hammer"] = round(wpt.P(0, 10, 1), 4)
        rep["wp_examples"] = {f"d={d},n={n},h={h}": round(wpt.P(d, n, h), 3)
                              for d, n, h in [(0, 10, 1), (0, 5, 1), (1, 5, 0), (-1, 5, 1), (2, 3, 0), (0, 1, 1), (0, 1, 0), (-2, 2, 1)]}
        rep["regimes"] = {f"d={d},n={n}": wpt.regime(d, n) for d, n in [(0, 10), (0, 1), (-1, 1), (1, 2), (-2, 3), (3, 4)]}

    models = fit_models(ds.rows, ds.X, ds.y, seed=args.seed, sets=sets)
    rep["cv"] = models.cv_report
    logging.info("models fitted in %.0fs; f logloss %.4f vs trivial %.4f", time.time() - t0,
                 models.cv_report["f_logloss"], models.cv_report["trivial_logloss"])

    vm = HammerAdjustedPoints(vs_all.H)
    skill_ref = None
    if "level_player" in sets:
        from .model.difficulty import reference_skill
        from .model.experiment import attach_tier
        tiers = attach_tier(ds.rows, args.inventory).get("tier")
        skill_ref = reference_skill(ds.rows, ds.rows["skill_thrower"].to_numpy(), tiers)
    pg = compute_points_gained(ds, models, vm, wp_table=wpt, skill_reference=skill_ref)
    cons = conservation_check(pg, vm)
    rep["conservation_max_abs_residual"] = float(cons["residual"].abs().max())
    rep["conservation_terminal_ok_rate"] = float(cons["terminal_is_actual"].mean())
    # calibration check: V(f(S0)) should be near H (empty sheet, hammer perspective)
    s0 = pg[pg["shot"] == 1]
    rep["V_S0_mean"] = round(float(s0["V_pre"].mean()), 4)
    rep["H_used"] = round(vs_all.H, 4)
    if wpt is not None:
        rep["wp_pg_abs_mean"] = round(float(pg["pg_wp"].abs().mean()), 4)
    logging.info("points gained computed in %.0fs", time.time() - t0)
    pg.to_parquet(os.path.join(args.parquet, "points_gained.parquet"), index=False)
    cons.to_parquet(os.path.join(args.parquet, "conservation.parquet"), index=False)

    lb = {"players": agg.by_player(pg, min_shots=args.min_shots), "teams": agg.by_team(pg),
          "shot_types": agg.by_shot_type(pg), "shot_numbers": agg.by_shot_number(pg)}
    for k, df in lb.items():
        df.to_csv(os.path.join(args.reports, f"leaderboard_{k}.csv"), index=False)
    # stratified tables (discipline, tier, hammer, game state), both currencies
    pgs = agg.attach_strata(pg, inventory_csv=args.inventory)
    strata = agg.strata_tables(pgs, min_shots_player=args.min_shots)
    for k, df in strata.items():
        df.to_csv(os.path.join(args.reports, f"strata_{k}.csv"), index=False)
    rep["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(args.reports, "model_report.json"), "w") as f:
        json.dump(rep, f, indent=2, default=str)
    with open(os.path.join(args.reports, "model_report.md"), "w") as f:
        f.write("# Points Gained: Phase 1 model report\n\n")
        f.write(f"Games {rep['n_games']}, ends {rep['n_ends']}, shots {rep['n_shots']}, training rows {rep['n_rows']}. "
                f"Feature sets: {', '.join(sets)}. Run time {rep['seconds']:.0f}s.\n\n")
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
        if "logloss_by_abs_diff" in cv:
            f.write("\nLog-loss by |score difference| (f vs trivial):\n\n| abs diff | n | f | trivial |\n|---|---|---|---|\n")
            for r, v in sorted(cv["logloss_by_abs_diff"].items()):
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
        f.write("\n## Stratified (pg in hammer-adjusted points; _wp columns in win probability)\n\n")
        for k, title in [("discipline_tier", "By discipline and tier"), ("discipline_hammer", "By discipline and hammer"),
                         ("game_state_hammer", "By game state (thrower's view) and hammer"),
                         ("shot_type_hammer", "By shot type and hammer")]:
            f.write(f"### {title}\n\n" + strata[k].round(4).to_markdown(index=False) + "\n\n")
        f.write("### Players: execution relative to the field for the same shot type and hammer state (min %d shots)\n\n" % args.min_shots)
        f.write(strata["players"].head(30).round(4).to_markdown(index=False) + "\n\n")
        f.write("### Teams by hammer\n\n" + strata["teams_hammer"].round(4).to_markdown(index=False) + "\n")
    print(json.dumps({k: v for k, v in rep.items() if k not in ("cv",)}, indent=2, default=str))
    print(json.dumps({k: v for k, v in rep["cv"].items() if k not in ("calibration_f", "logloss_by_rocks_remaining", "logloss_by_abs_diff", "logloss_by_tier", "f_cols", "g_cols")}, indent=2))
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
    inv = run_batch(args.inventory, args.raw, args.out, args.reports, limit=args.limit, force=args.force, workers=args.workers, match=args.match)
    print(inv[inv["in_scope"] == True]["status"].value_counts().to_string())


def cmd_events(args):
    """Per-event player leaderboards: one file per event under reports/events/, an index by year, one combined CSV."""
    from .model import aggregate as agg
    pg = pd.read_parquet(os.path.join(args.parquet, "points_gained.parquet"))
    books = args.books or None
    if args.match:
        books = sorted(b for b in pg["book"].unique() if any(m in b for m in args.match))
    lb = agg.by_player_event(pg, books, min_shots=args.min_shots)
    out_dir = os.path.join(args.reports, "events")
    os.makedirs(out_dir, exist_ok=True)
    lb.to_csv(os.path.join(args.reports, "leaderboard_events.csv"), index=False)
    inv = pd.read_csv(args.inventory) if os.path.exists(args.inventory) else None
    names = {}
    if inv is not None:
        inv["book"] = inv["file_name"].str.replace(r"\.pdf$", "", regex=True)
        names = inv.drop_duplicates("book").set_index("book")[["event_name", "year", "location", "tier"]].to_dict("index")
    cols = ["player", "team", "shots", "games", "pg_throw_rel_event_median", "pg_throw_rel_event", "floor10", "reliability",
            "big_misses", "big_makes", "worst5", "pg_throw_rel_event_wp", "floor10_wp", "big_misses_wp", "worst5_wp", "pg_call", "grade"]
    short = {"pg_throw_rel_event_median": "median", "pg_throw_rel_event": "mean", "pg_throw_rel_event_wp": "mean_wp", "pg_call": "call"}
    legend = ("Execution (PG: Throw) relative to this event's field for the same shot type and hammer state, hammer-adjusted points per shot. "
              "`median` is the player's typical shot; `mean` also carries the tail. `floor10` is the 10th percentile (a bad day); `reliability` the share "
              "of shots at or above the field's expectation; `big_misses` / `big_makes` count shots beyond half a point either way; `worst5` sums the five "
              "costliest shots. The `_wp` columns are the same in win probability (`big_misses_wp`: shots costing five or more points of win probability). "
              "`call` is the call component (secondary). Players are grouped by throwing position and sorted by median.\n\n")
    index = []
    for ev, grp in lb.groupby("event", sort=True):
        meta = names.get(ev, {})
        title = meta.get("event_name") or ev
        year = int(meta["year"]) if meta.get("year") == meta.get("year") and meta.get("year") is not None else int(ev[-4:]) if ev[-4:].isdigit() else 0
        fn = f"{ev}.md"
        with open(os.path.join(out_dir, fn), "w") as f:
            f.write(f"# {title} ({ev})\n\n")
            if meta:
                f.write(f"{meta.get('location', '')}, {meta.get('year', '')}; tier {meta.get('tier', '')}.\n\n")
            f.write(legend)
            for d, gd in grp.groupby("discipline", sort=True):
                f.write(f"## {'Men' if d == 'M' else 'Women'}\n\n")
                team = gd.groupby("team").agg(players=("player", "size"), shots=("shots", "sum"),
                                              mean=("pg_throw_rel_event", lambda x: float((x * gd.loc[x.index, "shots"]).sum() / gd.loc[x.index, "shots"].sum())),
                                              mean_wp=("pg_throw_rel_event_wp", lambda x: float((x * gd.loc[x.index, "shots"]).sum() / gd.loc[x.index, "shots"].sum())),
                                              call=("pg_call", "mean")).reset_index().sort_values("mean", ascending=False)
                f.write("### Teams (shot-weighted execution relative to the field)\n\n" + team.round(3).to_markdown(index=False) + "\n\n")
                for pos in ("FOURTH", "THIRD", "SECOND", "LEAD"):
                    gp = gd[gd["position"] == pos].sort_values("pg_throw_rel_event_median", ascending=False)
                    if not len(gp):
                        continue
                    f.write(f"### {pos.title()}s\n\n" + gp[cols].rename(columns=short).round(3).to_markdown(index=False) + "\n\n")
        n_games = int(pg.loc[pg["book"] == ev, "game_key"].nunique())
        index.append((year, ev, title, fn, int(grp["player"].nunique()), sorted(grp["discipline"].unique()), n_games))
    with open(os.path.join(out_dir, "README.md"), "w") as f:
        f.write("# Per-event player leaderboards\n\nOne file per event; players grouped by position and sorted by median execution relative to that event's field.\n\n")
        for year in sorted(set(i[0] for i in index), reverse=True):
            f.write(f"## {year}\n\n")
            for y, ev, title, fn, n, discs, ng in sorted(index, key=lambda i: i[1]):
                if y == year:
                    note = " (shot-by-shot for a few games only)" if ng < 10 else ""
                    f.write(f"- [{title}]({fn}) — {ev}, {'/'.join(discs)}, {ng} games, {n} players{note}\n")
            f.write("\n")
    # keep the combined markdown for grep, but the per-event files are the reading copy
    with open(os.path.join(args.reports, "leaderboard_events.md"), "w") as f:
        f.write("# Per-event player leaderboards (combined)\n\nSee reports/events/README.md for one file per event.\n\n" + legend)
        for (ev, d), grp in lb.groupby(["event", "discipline"], sort=True):
            f.write(f"## {ev} ({'Men' if d == 'M' else 'Women'})\n\n" + grp[cols].rename(columns=short).round(3).to_markdown(index=False) + "\n\n")
    print(f"{len(lb)} player-event rows over {lb['event'].nunique()} events -> {out_dir}/README.md and one file per event")


def cmd_difficulty(args):
    """Fit the shot-difficulty model: skill scalar per player and event effect per book (design 3.5, 8)."""
    import numpy as np
    from .model.cache import load_or_build
    from .model.dataset import load_books
    from .model.strength import field_strength_by_book, strength_table, junior_books_from_inventory
    from .model.difficulty import fit_difficulty, normalise_player, apply_aliases
    t0 = time.time()
    ds = load_or_build(args.parquet)
    tabs = load_books(args.parquet)
    jb = junior_books_from_inventory(args.inventory) if os.path.exists(args.inventory) else set()
    st = strength_table(tabs, jb)
    st.to_parquet(os.path.join(args.parquet, "team_strength.parquet"), index=False)
    fsb = field_strength_by_book(ds.rows, tabs, jb)
    fsb.to_parquet(os.path.join(args.parquet, "event_field_strength.parquet"), index=False)
    fkey = fsb.set_index(["book", "discipline"])["field_strength"]
    field_strength = fkey.reindex(pd.MultiIndex.from_arrays([ds.rows["book"], ds.rows["discipline"]])).to_numpy(dtype=float)
    logging.info("field strength for %d book-disciplines in %.0fs (%d nation-seasons)", len(fsb), time.time() - t0, len(st))
    es = pd.read_csv(args.event_strength).set_index("book")["rating"] if os.path.exists(args.event_strength) else pd.Series(dtype=float)
    event_strength = es.reindex(ds.rows["book"].to_numpy()).to_numpy(dtype=float)
    aliases = pd.read_csv(args.aliases) if os.path.exists(args.aliases) else None
    pk = apply_aliases(ds.rows["player"].map(normalise_player), ds.rows["discipline"], aliases)
    team_key = ds.rows["team"].astype(str) + np.where(ds.rows["book"].isin(jb), "-J", "")
    res = fit_difficulty(ds.rows, ds.X, event_strength, field_strength, pk, team_key=team_key, seed=args.seed)
    res["players"].to_parquet(os.path.join(args.parquet, "skill.parquet"), index=False)
    res["events"].to_parquet(os.path.join(args.parquet, "event_effects.parquet"), index=False)
    res["shots"].to_parquet(os.path.join(args.parquet, "shot_difficulty.parquet"), index=False)
    os.makedirs(args.reports, exist_ok=True)
    p, e = res["players"], res["events"]
    with open(os.path.join(args.reports, "difficulty_report.md"), "w") as f:
        f.write("# Shot-difficulty model: skill and event effects\n\n")
        f.write(f"Coefficients (logit scale): {', '.join(f'{k} {v:.3f}' for k, v in res['coef'].items())}. Fit {res['seconds']}s.\n\n")
        f.write("Skill is the thrower's expected advantage on the grade over the fields the player has played in, in logit units: "
                "team effect plus a shrunk player deviation. Level of play enters through the event: the hand-rated event strength "
                "(`data/event_strength.csv`) and the field strength derived from game results (mean Bradley-Terry strength of the "
                "teams in the book, fitted leaving the book out). The event effect is what remains of the book after both: ice, "
                "conditions and the grader.\n\n")
        fs = fsb.merge(pd.read_csv(args.event_strength)[["book", "rating"]], on="book", how="left") if os.path.exists(args.event_strength) else fsb
        f.write("## Field strength by event (derived) next to the event rating (hand)\n\n")
        f.write(fs.sort_values(["discipline", "field_strength"], ascending=[True, False]).round(3).to_markdown(index=False) + "\n\n")
        for d in ("M", "W"):
            q = p[(p["discipline"] == d) & (p["shots"] >= 200)].sort_values("skill", ascending=False)
            f.write(f"## {'Men' if d == 'M' else 'Women'}: top and bottom 15 by skill (min 200 shots)\n\n")
            f.write(pd.concat([q.head(15), q.tail(15)])[["player", "team", "shots", "grade", "skill", "player_dev", "team_effect", "event_level"]].round(3).to_markdown(index=False) + "\n\n")
        f.write("## Event effects\n\n" + e.sort_values("event_effect").round(3).to_markdown(index=False) + "\n")
    print(json.dumps({k: round(float(v), 4) for k, v in res["coef"].items()}))
    print(p.groupby("discipline")["skill"].describe().round(3).to_string())
    print(e.sort_values("event_effect")[["book", "event_effect"]].head(5).round(3).to_string(index=False))
    print(e.sort_values("event_effect")[["book", "event_effect"]].tail(5).round(3).to_string(index=False))
    print(f"wrote {args.reports}/difficulty_report.md in {time.time() - t0:.0f}s")


def cmd_raster(args):
    """Raw-geometry f (and g) on one split: time-split log-loss against the trees, the subtlety probe
    and the monotonicity checks (design Sections 5.2, 7.5). Writes reports/raster_<name>.json."""
    import numpy as np
    from .model.cache import load_or_build
    from .model.experiment import split_rows, attach_tier
    from .model.train import design_matrices, make_model, _cat_index, _full_proba, evaluate, FittedModels, design_columns
    from .model.raster import pre_position_arrays, scalar_matrix, fit_raster, target_xy_from_rows, arrays_subset
    from .model import probe as PR
    from .model.value import HammerAdjustedPoints
    t0 = time.time()
    sets = _feature_sets(args.features)
    ds = _with_level(load_or_build(args.parquet), sets, args.parquet, args.aliases)
    rows_all = attach_tier(ds.rows, args.inventory)
    unm = (rows_all["mirror"] == 0).to_numpy()
    keep_cols = [c for c in rows_all.columns if c not in ("player", "team", "hammer_team")]   # memory: drop strings not needed here
    rows = rows_all[unm][keep_cols].reset_index(drop=True); X = ds.X[unm]; y = ds.y[unm]
    del rows_all
    tr, te = split_rows(rows, args.split, args.cutoff_year, args.fold)
    if args.max_train and len(tr) > args.max_train:
        tr = np.random.default_rng(args.seed).choice(tr, args.max_train, replace=False)
    val = np.random.default_rng(args.seed + 1).choice(te, min(len(te), 40000), replace=False)   # early-stopping subset
    logging.info("raster: %d train, %d test rows; building stone arrays", len(tr), len(te))
    arrays = pre_position_arrays(ds)
    rep = {"name": args.name, "split": args.split, "sets": list(sets), "n_train": int(len(tr)), "n_test": int(len(te)), "device": None}
    from .model.raster import device_name
    rep["device"] = device_name()
    P = {}
    # trees on the same split for a like-for-like comparison
    X_f, f_cols, X_g, g_cols = design_matrices(rows, X, sets)
    mf = make_model(args.seed).fit(X_f[tr], y[tr]); P["f_tree"] = _full_proba(mf, X_f[te])
    mg = make_model(args.seed, _cat_index(g_cols)).fit(X_g[tr], y[tr]); P["g_tree"] = _full_proba(mg, X_g[te])
    logging.info("trees fitted in %.0fs", time.time() - t0)
    del X_f, X_g
    ds.rows = ds.rows[(ds.rows["mirror"] == 0).to_numpy()].reset_index(drop=True)   # the probe reads unmirrored rows only
    import gc; gc.collect()
    fits = {}
    for kind in (["f", "g"] if not args.f_only else ["f"]):
        S, cols = scalar_matrix(rows, X, kind, hybrid=args.hybrid)
        txy = target_xy_from_rows(rows) if (kind == "g" and "intent" in sets) else None
        fit = fit_raster(kind, arrays, S, y, txy, tr, val, epochs=args.epochs, batch=args.batch, lr=args.lr, seed=args.seed)
        fits[kind] = (fit, S, txy)
        P[f"{kind}_raster"] = fit.predict(arrays_subset(arrays, te), S[te], None if txy is None else txy[te])
        rep[f"{kind}_history"] = fit.history
        logging.info("raster %s done in %.0fs", kind, time.time() - t0)
    ev = evaluate(P, y[te], rows.iloc[te], X[te])
    rep.update({k: v for k, v in ev.items() if k != "calibration_f"})
    # probe on made doubles with a known struck stone, and monotonicity
    vm = HammerAdjustedPoints(0.58); v = PR.v_points(vm)
    if "g" in fits and os.path.exists(os.path.join(args.parquet, "intent.parquet")):
        it = pd.read_parquet(os.path.join(args.parquet, "intent.parquet"))
        probes = PR.probe_positions(ds, it, n=args.n_probe, seed=args.seed)
        if len(probes):
            models = FittedModels(mf, mg, mf, f_cols, g_cols, tuple(sets), {}, [], "book")
            tc = PR.tree_curve(models, ds, probes, v)
            fit, S, txy = fits["g"]
            pr = probes["row"].to_numpy()
            rc = PR.raster_curve(fit, ds, probes, v, S[pr], None if txy is None else txy[pr])
            rep["probe"] = {"n": int(len(probes)), "offsets": PR.OFFSETS.tolist(), "tree": PR.curve_summary(tc), "raster": PR.curve_summary(rc),
                            "tree_mean_curve": np.round(tc.mean(0), 4).tolist(), "raster_mean_curve": np.round(rc.mean(0), 4).tolist()}
            np.save(os.path.join(args.reports, f"probe_{args.name}.npy"), np.stack([tc, rc]))
    if "f" in fits:
        fit, S, _ = fits["f"]
        from .model.raster import StoneArrays, MAX_STONES
        def raster_value(positions):
            n = len(positions)
            x = np.zeros((n, MAX_STONES), np.float32); yy = np.zeros_like(x); o = np.zeros_like(x); valid = np.zeros((n, MAX_STONES), bool)
            feats = []
            for i, p in enumerate(positions):
                m = min(p.n, MAX_STONES)
                x[i, :m], yy[i, :m], o[i, :m], valid[i, :m] = p.x[:m], p.y[:m], p.owner[:m], True
                feats.append(np.hstack([position_features_row(p), ]))
            Xp = np.vstack(feats)
            sub = pd.DataFrame({"discipline": "M", "diff_hammer": 0, "ends_remaining": 5, "is_extra_end": False, "turn": "cw", "shot_type_code": 0}, index=range(n))
            Sp, _ = scalar_matrix(sub, Xp, "f", hybrid=args.hybrid)
            return fit.predict(StoneArrays(x, yy, o, valid), Sp, None) @ v
        def tree_value(positions):
            from .model.train import column as _col
            Xp = np.vstack([position_features_row(p) for p in positions])
            sub = pd.DataFrame({"discipline": "M", "diff_hammer": 0, "ends_remaining": 5, "is_extra_end": False, "turn": "cw", "shot_type_code": 0}, index=range(len(positions)))
            Xf = np.column_stack([_col(sub, Xp, c) for c in f_cols])       # f columns only: no level or intent needed
            return _full_proba(mf, Xf) @ v
        from .model.features import position_features as position_features_row
        rep["monotonicity"] = {"raster": PR.monotonicity_report(raster_value), "tree": PR.monotonicity_report(tree_value)}
    rep["seconds"] = round(time.time() - t0, 1)
    os.makedirs(args.reports, exist_ok=True)
    with open(os.path.join(args.reports, f"raster_{args.name}.json"), "w") as f:
        json.dump(rep, f, indent=1, default=str)
    print(json.dumps({k: rep[k] for k in rep if k.endswith("_logloss") or k in ("n_train", "n_test", "device", "seconds", "probe", "monotonicity")}, indent=1, default=str))


def cmd_testset(args):
    """The six-shot face-validity table from the current Points Gained table."""
    from .model.testset import write_testset_report
    pg = pd.read_parquet(os.path.join(args.parquet, "points_gained.parquet"))
    os.makedirs(args.reports, exist_ok=True)
    t = write_testset_report(pg, os.path.join(args.reports, "testset.md"))
    print(t.round(3).to_string(index=False))


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
    d.add_argument("--inventory", default="data/inventory.csv", help="for tier and event family strata")
    d.add_argument("--features", default="base", help="comma list of feature sets: base,situation,level,intent")
    d.add_argument("--rebuild", action="store_true", help="rebuild the feature cache")
    d.add_argument("--aliases", default="data/player_aliases.csv")
    d.set_defaults(func=cmd_model)
    i = sub.add_parser("features", help="build or refresh the feature cache under the parquet root")
    i.add_argument("--parquet", default="data/parquet")
    i.add_argument("--no-mirror", action="store_true")
    i.add_argument("--rebuild", action="store_true")
    i.set_defaults(func=cmd_features)
    j = sub.add_parser("experiment", help="fit once on one split and score the held-out rows")
    j.add_argument("--parquet", default="data/parquet")
    j.add_argument("--reports", default="reports")
    j.add_argument("--inventory", default="data/inventory.csv")
    j.add_argument("--features", default="base", help="comma list of feature sets")
    j.add_argument("--split", choices=["time", "book"], default="time")
    j.add_argument("--cutoff-year", type=int, default=2024, help="time split: last training year")
    j.add_argument("--fold", type=int, default=0, help="book split: which of the five folds")
    j.add_argument("--name", default=None)
    j.add_argument("--seed", type=int, default=0)
    j.add_argument("--rebuild", action="store_true")
    j.add_argument("--aliases", default="data/player_aliases.csv")
    j.set_defaults(func=cmd_experiment)
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
    g.add_argument("--workers", type=int, default=1)
    g.add_argument("--match", nargs="*", default=None, help="only books whose file name contains one of these substrings")
    g.set_defaults(func=cmd_batch)
    h = sub.add_parser("events", help="per-event player leaderboards")
    h.add_argument("--parquet", default="data/parquet")
    h.add_argument("--reports", default="reports")
    h.add_argument("--books", nargs="*", default=None, help="book ids (file stems)")
    h.add_argument("--match", nargs="*", default=None, help="substrings of book ids to include")
    h.add_argument("--min-shots", type=int, default=30)
    h.add_argument("--inventory", default="data/inventory.csv")
    h.set_defaults(func=cmd_events)
    n = sub.add_parser("intent", help="realised intent per shot from the delivered stone and prior rings")
    n.add_argument("--parquet", default="data/parquet")
    n.add_argument("--seed", type=int, default=0)
    n.add_argument("--reports", default="reports")
    n.add_argument("--aliases", default="data/player_aliases.csv")
    n.set_defaults(func=cmd_intent)
    m = sub.add_parser("difficulty", help="fit the shot-difficulty model: skill per player, effect per event")
    m.add_argument("--parquet", default="data/parquet")
    m.add_argument("--reports", default="reports")
    m.add_argument("--inventory", default="data/inventory.csv")
    m.add_argument("--event-strength", default="data/event_strength.csv")
    m.add_argument("--aliases", default="data/player_aliases.csv")
    m.add_argument("--seed", type=int, default=0)
    m.add_argument("--no-leave-out", action="store_true", help="team strength from all books including the row's own")
    m.set_defaults(func=cmd_difficulty)
    o = sub.add_parser("raster", help="raw-geometry f/g on one split with the subtlety probe and monotonicity gates")
    o.add_argument("--parquet", default="data/parquet")
    o.add_argument("--reports", default="reports")
    o.add_argument("--inventory", default="data/inventory.csv")
    o.add_argument("--aliases", default="data/player_aliases.csv")
    o.add_argument("--features", default="base,situation,level,intent")
    o.add_argument("--split", choices=["time", "book"], default="time")
    o.add_argument("--cutoff-year", type=int, default=2024)
    o.add_argument("--fold", type=int, default=0)
    o.add_argument("--name", default="raster")
    o.add_argument("--epochs", type=int, default=6)
    o.add_argument("--batch", type=int, default=256)
    o.add_argument("--lr", type=float, default=1e-3)
    o.add_argument("--max-train", type=int, default=None, help="subsample the training rows")
    o.add_argument("--n-probe", type=int, default=300)
    o.add_argument("--f-only", action="store_true")
    o.add_argument("--hybrid", action="store_true", help="also feed the 28 hand-built features to the dense layer")
    o.add_argument("--seed", type=int, default=0)
    o.set_defaults(func=cmd_raster)
    k = sub.add_parser("testset", help="face-validity table for the six pinned 2026 Olympic shots")
    k.add_argument("--parquet", default="data/parquet")
    k.add_argument("--reports", default="reports")
    k.set_defaults(func=cmd_testset)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
