"""Command line interface: pointsgained ingest | validate | audit | model | features | experiment | events | frontend | stones | traits | inventory | download | batch."""
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


def attach_position_sets(rows, sets, parquet_root, grade_books=None, grade_groups=None):
    """The position sets of the rows' pre-shot positions: rock traits, slots, the draw to beat, doubles and
    runbacks, the tap, and trait grades and the tap's trait rescore (fitted on `grade_books`, or cross-fitted
    over `grade_groups`)."""
    if "traits" in sets:
        from .model.trait_features import attach_traits, load_tables as load_trait_tables
        rows = attach_traits(rows, load_trait_tables(parquet_root)[1])
    if "slots" in sets:
        from .model.slot_features import attach_slots
        rows = attach_slots(rows, parquet_root)
    for rel in ("draw", "combo", "tap"):
        if rel in sets:
            from .model.draw_features import attach_draw, load_table as load_rel_table
            rows = attach_draw(rows, load_rel_table(parquet_root, name=rel), name=rel)
    if "tapedge" in sets:
        from .model.draw_features import attach_tap_edge, load_table as load_rel_table
        rows = attach_tap_edge(rows, load_rel_table(parquet_root, name="tap"), load_rel_table(parquet_root, name="draw"))
    if "grades" in sets or "tapgrade" in sets:
        from .model.trait_study import attach_grades
        rows = attach_grades(rows, parquet_root, fit_books=grade_books, groups=grade_groups, tap="tapgrade" in sets)
    return rows


def _with_level(ds, sets, parquet_root, event_strength_csv="data/event_strength.csv", grade_books=None, grade_groups=None):
    """Attach the level column (the event's rating), the intent columns and the position sets requested."""
    if "level" in sets:
        es = pd.read_csv(event_strength_csv).set_index("book")["rating"] if os.path.exists(event_strength_csv) else pd.Series(dtype=float)
        ds.rows = ds.rows.assign(event_rating=es.reindex(ds.rows["book"].to_numpy()).fillna(float(es.median()) if len(es) else 85.0).to_numpy(dtype=float))
    if "intent" in sets:
        from .model.intent import attach_intent
        ds.rows = attach_intent(ds.rows, pd.read_parquet(os.path.join(parquet_root, "intent.parquet")))
    ds.rows = attach_position_sets(ds.rows, sets, parquet_root, grade_books, grade_groups)
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
    from .model.experiment import run_experiment, split_rows
    sets = _feature_sets(args.features)
    ds = load_or_build(args.parquet, rebuild=args.rebuild)
    # trait grades are fitted on the split's training books only, so the held-out rows are graded honestly
    grade_books = set(ds.rows["book"].to_numpy()[split_rows(ds.rows, args.split, args.cutoff_year, args.fold)[0]])
    ds = _with_level(ds, sets, args.parquet, grade_books=grade_books)
    name = args.name or f"{args.split}_{'+'.join(sets)}"
    rep = run_experiment(ds, name, sets, split=args.split, cutoff_year=args.cutoff_year, fold=args.fold,
                         seed=args.seed, reports=args.reports, inventory_csv=args.inventory, target=args.target,
                         save_predictions=os.path.join(args.parquet, "experiments") if args.save_predictions else None)
    print(json.dumps({k: rep[k] for k in ("name", "split", "sets", "n_train", "n_test", "trivial_logloss", "f_logloss", "g_logloss", "seconds")}, indent=2))
    print("by rocks remaining:", {r: (v["f"], v["trivial"]) for r, v in rep["logloss_by_rocks_remaining"].items()})
    print("front-end gates:", {k: round(v, 3) for k, v in rep["frontend_gates"].items()})
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
    ds = load_or_build(args.parquet, mirror=not args.no_mirror, rebuild=args.rebuild)
    # trait grades cross-fitted on the same book folds as the models: a held-out book is graded by weights
    # fitted without it
    from sklearn.model_selection import GroupKFold
    books = ds.rows["book"].to_numpy()
    grade_groups = {}
    for k, (_, te) in enumerate(GroupKFold(n_splits=5).split(books, groups=books)):
        grade_groups.update({b: k for b in set(books[te])})
    ds = _with_level(ds, sets, args.parquet, grade_groups=grade_groups)
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

    models = fit_models(ds.rows, ds.X, ds.y, seed=args.seed, sets=sets, target=args.target)
    rep["target"] = args.target
    rep["cv"] = models.cv_report
    logging.info("models fitted in %.0fs; f logloss %.4f vs trivial %.4f", time.time() - t0,
                 models.cv_report["f_logloss"], models.cv_report["trivial_logloss"])

    vm = HammerAdjustedPoints(vs_all.H)
    pg = compute_points_gained(ds, models, vm, wp_table=wpt,
                               attach_position=lambda sub: attach_position_sets(sub, sets, args.parquet, grade_groups=grade_groups))
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

    from .model.model_report import build_tables, write_model_report
    lb, strata = build_tables(pg, args.reports, args.min_shots, args.inventory)
    rep["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(args.reports, "model_report.json"), "w") as f:
        json.dump(rep, f, indent=2, default=str)
    write_model_report(os.path.join(args.reports, "model_report.md"), rep, lb, strata, args.min_shots)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("cv",)}, indent=2, default=str))
    print(json.dumps({k: v for k, v in rep["cv"].items() if k not in ("calibration_f", "logloss_by_rocks_remaining", "logloss_by_abs_diff", "logloss_by_tier", "f_cols", "g_cols")}, indent=2))
    print(f"wrote {args.reports}/model_report.md in {time.time() - t0:.0f}s")


def cmd_model_report(args):
    """Rewrite the model report from the saved run summary and the Points Gained table, without refitting."""
    from .model.model_report import build_tables, write_model_report
    with open(os.path.join(args.reports, "model_report.json")) as f:
        rep = json.load(f)
    pg = pd.read_parquet(os.path.join(args.parquet, "points_gained.parquet"))
    lb, strata = build_tables(pg, args.reports, args.min_shots, args.inventory)
    write_model_report(os.path.join(args.reports, "model_report.md"), rep, lb, strata, args.min_shots)
    print(f"wrote {args.reports}/model_report.md")


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
    from .model.ledger import style_table
    led_path = os.path.join(args.parquet, "rock_ledger.parquet")
    led = pd.read_parquet(led_path) if os.path.exists(led_path) else None
    if led is not None:
        pg = pg.merge(led, on=["game_key", "end", "shot"], how="left")
    books = args.books or None
    if args.match:
        books = sorted(b for b in pg["book"].unique() if any(m in b for m in args.match))
    lb = agg.by_player_event(pg, books, min_shots=args.min_shots)
    te = agg.by_team_event(pg, books)
    out_dir = os.path.join(args.reports, "events")
    os.makedirs(out_dir, exist_ok=True)
    lb.to_csv(os.path.join(args.reports, "leaderboard_events.csv"), index=False)
    inv = pd.read_csv(args.inventory) if os.path.exists(args.inventory) else None
    names = {}
    if inv is not None:
        inv["book"] = inv["file_name"].str.replace(r"\.pdf$", "", regex=True)
        names = inv.drop_duplicates("book").set_index("book")[["event_name", "year", "location", "tier"]].to_dict("index")
    cols = ["player", "team", "shots", "games", "reliability", "avg_make", "avg_miss", "big_makes", "big_misses", "worst5",
            "pg_throw_rel_event", "big_makes_wp", "big_misses_wp", "best5_wp", "worst5_wp", "pg_call", "grade"]
    short = {"pg_throw_rel_event": "net", "pg_call": "call"}
    legend = ("Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, "
              "in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the "
              "share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when "
              "below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is "
              "the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for "
              "reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage "
              "points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then "
              "by average miss. The team table above them is a different kind of table: a team's standing is its record and what its "
              "stones did to its chance of winning, so it carries no execution columns.\n\n")
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
                tt = te[(te["event"] == ev) & (te["discipline"] == d)].copy()
                tt["record"] = tt["wins"].astype(str) + "-" + tt["losses"].astype(str)
                tt = tt[["team", "games", "record", "wp_gain"]].rename(columns={"wp_gain": "WP gained / game"})
                f.write("### Teams\n\nThe team-level view, in win probability: the record, and the summed effect of the team's own "
                        "stones on its chance of winning, per game, in percentage points (calls and throws together).\n\n"
                        + tt.round(1).to_markdown(index=False) + "\n\n")
                if led is not None:
                    st = style_table(pg[(pg["book"] == ev) & (pg["discipline"] == d)])
                    f.write("### Build or address\n\nHow each team played the stones, in rock grades (descriptive, not a "
                            "ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how "
                            "much it took from the other team's, per stone, relative to this field at the same stage of the end; "
                            "`builds_share` the share of its stones that built more than they addressed; `temperature` the mean "
                            "peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, "
                            "low: conservative ones).\n\n" + st.round(3).to_markdown(index=False) + "\n\n")
                for pos in ("FOURTH", "THIRD", "SECOND", "LEAD"):
                    gp = gd[gd["position"] == pos].sort_values(["reliability", "avg_miss"], ascending=False)
                    if not len(gp):
                        continue
                    f.write(f"### {pos.title()}s\n\n" + gp[cols].rename(columns=short).round(3).to_markdown(index=False) + "\n\n")
        n_games = int(pg.loc[pg["book"] == ev, "game_key"].nunique())
        index.append((year, ev, title, fn, int(grp["player"].nunique()), sorted(grp["discipline"].unique()), n_games))
    with open(os.path.join(out_dir, "README.md"), "w") as f:
        f.write("# Per-event player leaderboards\n\nOne file per event; players grouped by position and sorted by reliability (the share of shots at or above that event's field for the same call), then by the average miss.\n\n")
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


def cmd_game(args):
    """One game shot by shot: ends, players, largest swings and every shot's values, under reports/games/."""
    from .model.report import game_report, game_file_name
    pg = pd.read_parquet(os.path.join(args.parquet, "points_gained.parquet"))
    led_path = os.path.join(args.parquet, "rock_ledger.parquet")
    if os.path.exists(led_path):
        # the rock ledger (`pointsgained traits` writes it): each team's rock grade per stone
        pg = pg.merge(pd.read_parquet(led_path), on=["game_key", "end", "shot"], how="left")
    keys = sorted(k for k in pg["game_key"].unique() if all(m in k for m in args.match))
    if not keys:
        raise SystemExit(f"no game key contains all of {args.match}")
    inv = pd.read_csv(args.inventory) if os.path.exists(args.inventory) else None
    names = {}
    if inv is not None:
        inv["book"] = inv["file_name"].str.replace(r"\.pdf$", "", regex=True)
        names = inv.drop_duplicates("book").set_index("book")["event_name"].to_dict()
    out_dir = os.path.join(args.reports, "games")
    os.makedirs(out_dir, exist_ok=True)
    for key in keys:
        book, local_key = key.split("|", 1)
        games = pd.read_parquet(os.path.join(args.parquet, book, "games.parquet"))
        meta = games[games["game_key"] == local_key].iloc[0]
        ls = pd.read_parquet(os.path.join(args.parquet, book, "line_scores.parquet"))
        ls = ls[ls["game_key"] == local_key].set_index("team")
        a, b = str(meta["team_a"]), str(meta["team_b"])
        disc = {"M": "men", "W": "women"}.get(str(meta["discipline"]), str(meta["discipline"]))
        title = f"{names.get(book, book)}: {meta['session']}, {meta['team_a_name']} v {meta['team_b_name']} ({disc})"
        final = f"Final score {a} {int(ls.loc[a, 'total'])}, {b} {int(ls.loc[b, 'total'])}" if {a, b} <= set(ls.index) else ""
        subtitle = f"{meta['date']} {meta['start_time']}; {a} {meta['color_a']}, {b} {meta['color_b']}. {final}. Game key `{key}`."
        text = game_report(pg[pg["game_key"] == key], title, subtitle, team_order=(a, b))
        fn = os.path.join(out_dir, game_file_name(key))
        with open(fn, "w") as f:
            f.write(text)
        print(f"wrote {fn}")


def cmd_frontend(args):
    """The front-end diagnostic: what early-end execution values measure, configuration calibration, scenario probes."""
    from .model.frontend import load_frame, write_report
    os.makedirs(args.reports, exist_ok=True)
    t0 = time.time()
    df = load_frame(args.parquet)
    path = write_report(df, args.reports)
    print(f"wrote {path} in {time.time() - t0:.0f}s")


def cmd_stones(args):
    """The stone study: every stone followed through the end, what stones end up doing, late risers, and
    how flat the model's values are by stage of the end (reports/stones.md)."""
    from .model.stone_value import load_lives, write_report
    os.makedirs(args.reports, exist_ok=True)
    t0 = time.time()
    load_lives(args.parquet, rebuild=args.rebuild)
    print(f"wrote {write_report(args.parquet, args.reports)} in {time.time() - t0:.0f}s")


def cmd_traits(args):
    """The rock-trait study: what positions whose stones carry each trait have been worth, by team and
    stage, stone types, and additive stone grades (reports/traits.md); and the rock ledger for every
    stone (rock_ledger.parquet: each team's grade before and after, build and address)."""
    from .model.trait_features import load_tables
    from .model.trait_study import write_report
    from .model.ledger import rock_ledger
    t0 = time.time()
    load_tables(args.parquet, rebuild=args.rebuild)
    rock_ledger(args.parquet)
    print(f"wrote {write_report(args.parquet, args.reports, args.inventory, args.tier1)} in {time.time() - t0:.0f}s")


def cmd_misprice(args):
    """Where experiments' models over- or under-price positions, from their saved held-out predictions."""
    from .model.misprice import write_report
    print(f"wrote {write_report(args.parquet, args.reports, args.names, args.which)}")


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


def cmd_testset(args):
    """The six-shot face-validity table from the current Points Gained table."""
    from .model.testset import write_testset_report
    pg = pd.read_parquet(os.path.join(args.parquet, "points_gained.parquet"))
    os.makedirs(args.reports, exist_ok=True)
    t = write_testset_report(pg, os.path.join(args.reports, "testset.md"))
    print(t.round(3).to_string(index=False))


def main(argv=None):
    from .model.train import ADOPTED
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
    d.add_argument("--features", default=",".join(ADOPTED), help="comma list of feature sets (model/train.py)")
    d.add_argument("--rebuild", action="store_true", help="rebuild the feature cache")
    d.add_argument("--target", default="local:2", help="final or local:k (model/targets.py)")
    d.set_defaults(func=cmd_model)
    i = sub.add_parser("features", help="build or refresh the feature cache under the parquet root")
    i.add_argument("--parquet", default="data/parquet")
    i.add_argument("--no-mirror", action="store_true")
    i.add_argument("--rebuild", action="store_true")
    i.set_defaults(func=cmd_features)
    j = sub.add_parser("experiment", help="fit once on one split and score the held-out rows")
    j.add_argument("--target", default="local:2", help="final (the end's score) or local:k (early rows take the value k stones later)")
    j.add_argument("--parquet", default="data/parquet")
    j.add_argument("--reports", default="reports")
    j.add_argument("--inventory", default="data/inventory.csv")
    j.add_argument("--features", default=",".join(ADOPTED), help="comma list of feature sets (model/train.py)")
    j.add_argument("--split", choices=["time", "book"], default="time")
    j.add_argument("--cutoff-year", type=int, default=2024, help="time split: last training year")
    j.add_argument("--fold", type=int, default=0, help="book split: which of the five folds")
    j.add_argument("--name", default=None)
    j.add_argument("--seed", type=int, default=0)
    j.add_argument("--rebuild", action="store_true")
    j.add_argument("--save-predictions", action="store_true", help="write the held-out predictions to <parquet>/experiments/<name>.parquet")
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
    mr = sub.add_parser("model-report", help="rewrite the model report from the saved run summary without refitting")
    mr.add_argument("--parquet", default="data/parquet")
    mr.add_argument("--reports", default="reports")
    mr.add_argument("--min-shots", type=int, default=40)
    mr.add_argument("--inventory", default="data/inventory.csv")
    mr.set_defaults(func=cmd_model_report)
    h = sub.add_parser("events", help="per-event player leaderboards")
    h.add_argument("--parquet", default="data/parquet")
    h.add_argument("--reports", default="reports")
    h.add_argument("--books", nargs="*", default=None, help="book ids (file stems)")
    h.add_argument("--match", nargs="*", default=None, help="substrings of book ids to include")
    h.add_argument("--min-shots", type=int, default=30)
    h.add_argument("--inventory", default="data/inventory.csv")
    h.set_defaults(func=cmd_events)
    q = sub.add_parser("game", help="one game shot by shot: ends, players, largest swings, every shot's values")
    q.add_argument("--parquet", default="data/parquet")
    q.add_argument("--reports", default="reports")
    q.add_argument("--match", nargs="+", required=True, help="substrings that the game key must all contain, e.g. OWG2026 Gold_Medal")
    q.add_argument("--inventory", default="data/inventory.csv")
    q.set_defaults(func=cmd_game)
    fe = sub.add_parser("frontend", help="front-end diagnostic: early-end execution, configurations, scenario probes")
    fe.add_argument("--parquet", default="data/parquet")
    fe.add_argument("--reports", default="reports")
    fe.set_defaults(func=cmd_frontend)
    sn = sub.add_parser("stones", help="the stone study: stones tracked through the end, their roles, late risers")
    sn.add_argument("--parquet", default="data/parquet")
    sn.add_argument("--reports", default="reports")
    sn.add_argument("--rebuild", action="store_true", help="re-track the stones")
    sn.set_defaults(func=cmd_stones)
    tr = sub.add_parser("traits", help="the rock-trait study: stones by trait, outcome distributions, additive grades")
    tr.add_argument("--parquet", default="data/parquet")
    tr.add_argument("--reports", default="reports")
    tr.add_argument("--inventory", default="data/inventory.csv")
    tr.add_argument("--tier1", action="store_true", help="Worlds and Olympics only")
    tr.add_argument("--rebuild", action="store_true", help="recompute the trait tables")
    tr.set_defaults(func=cmd_traits)
    mp = sub.add_parser("misprice", help="where models over- or under-price positions (needs experiment --save-predictions)")
    mp.add_argument("names", nargs="+", help="experiment names; the first is the reference")
    mp.add_argument("--which", choices=["f", "g"], default="f")
    mp.add_argument("--parquet", default="data/parquet")
    mp.add_argument("--reports", default="reports")
    mp.set_defaults(func=cmd_misprice)
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
    k = sub.add_parser("testset", help="face-validity table for the six pinned 2026 Olympic shots")
    k.add_argument("--parquet", default="data/parquet")
    k.add_argument("--reports", default="reports")
    k.set_defaults(func=cmd_testset)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
