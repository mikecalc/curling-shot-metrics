"""One experiment: a named feature set on one split, fitted once, scored on the held-out rows.

Splits:
  time   train on events dated through `cutoff_year`, test on later events (design 12.7)
  book   one GroupKFold fold by book (the same held-out books every time, for comparability)

Targets (model/targets.py): final, local:k or phase.

Every experiment is scored against the final end outcome on the held-out rows, and also by the
front-end gates: Points Gained on the held-out rows from the fitted f and g, and whether early
execution see-saws between consecutive stones and between opposing leads (model/frontend.py).

Results go to reports/experiments/<name>.json and a line is appended to reports/experiments/log.md
and reports/experiments/frontend_gates.md.
"""
from __future__ import annotations

import json
import logging
import os
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

from .aggregate import _records, normalise_player
from .dataset import Dataset
from .frontend import next_stone, opponent_same_game, split_half, _spearman
from .train import design_matrices, make_model, monotone_cst, _cat_index, column, evaluate, _full_proba, TRIVIAL_FEATURES, FEATURE_SETS
from .targets import training_rows
from .value import HammerAdjustedPoints, ValueSet

log = logging.getLogger(__name__)


def split_rows(rows: pd.DataFrame, split: str, cutoff_year: int = 2024, fold: int = 0):
    """(train index, test index) over rows. Mirrored rows follow their shot."""
    if split == "time":
        year = pd.to_datetime(rows["date"]).dt.year.to_numpy()
        return np.flatnonzero(year <= cutoff_year), np.flatnonzero(year > cutoff_year)
    if split == "book":
        groups = rows["book"].to_numpy()
        splits = list(GroupKFold(n_splits=5).split(rows, groups=groups))
        return splits[fold]
    raise ValueError(f"unknown split {split!r}")


def attach_tier(rows: pd.DataFrame, inventory_csv: str | None) -> pd.DataFrame:
    if not inventory_csv or not os.path.exists(inventory_csv) or "tier" in rows:
        return rows
    inv = pd.read_csv(inventory_csv)
    inv["book"] = inv["file_name"].str.replace(r"\.pdf$", "", regex=True)
    m = inv.drop_duplicates("book").set_index("book")["tier"]
    return rows.assign(tier=rows["book"].map(m))


def frontend_gates(rows: pd.DataFrame, Pf: np.ndarray, Pg: np.ndarray, y: np.ndarray, H: float) -> dict:
    """Points Gained (execution, hammer-adjusted points) on held-out unmirrored rows from the fitted f and g,
    and the front-end measures: the see-saw between consecutive stones (1-4) and between opposing leads,
    agreement with grades (a check only) and repeatability for leads and seconds."""
    v = HammerAdjustedPoints(H).v
    V_f, V_g = Pf @ v, Pg @ v
    pos_of = pd.Series(np.arange(len(rows)), index=rows.index)
    post = rows["post_row"].to_numpy()
    j = pos_of.reindex(post).to_numpy()
    V_post = np.where(rows["is_last_shot"].to_numpy(dtype=bool), v[y], np.where(np.isnan(j), np.nan, V_f[np.nan_to_num(j).astype(int)]))
    sign = np.where(rows["thrower_has_hammer"].to_numpy(dtype=bool), 1.0, -1.0)
    d = rows[["game_key", "end", "shot", "book", "discipline", "shot_type", "thrower_has_hammer", "team", "player", "grade_pct"]].copy()
    d["pg_throw"] = sign * (V_post - V_g)
    d = d[d["pg_throw"].notna()]
    d["rel"] = d["pg_throw"] - d.groupby(["book", "discipline", "shot_type", "thrower_has_hammer"])["pg_throw"].transform("mean")
    d["player_key"] = d["player"].map(normalise_player)
    d["pos_code"] = ((((d["shot"] + 1) // 2) + 1) // 2).clip(1, 4)
    ns = next_stone(d).set_index("shot")["next_stone"]
    out = {"seesaw_1_4": float(ns.loc[1:4].mean()), "seesaw_5_8": float(ns.loc[5:8].mean()),
           **{f"seesaw_{s}": float(ns.get(s, np.nan)) for s in (1, 2, 3, 4)}}
    for code, name in ((1, "lead"), (2, "second"), (4, "fourth")):
        p = d[d["pos_code"] == code]
        opp = opponent_same_game(p)
        sh = split_half(p, "rel", min_half=40)
        pl = p[p["player_key"] != ""].groupby(["player_key", "book"]).agg(rel=("rel", "mean"), grade=("grade_pct", "mean"), n=("rel", "size"))
        pl = pl[pl["n"] >= 80]
        out.update({f"{name}_opponent": opp["rel"], f"{name}_opponent_grade": opp["grade_pct"],
                    f"{name}_grade_shot": _spearman(p["pg_throw"], p["grade_pct"]),
                    f"{name}_grade_player": _spearman(pl["rel"], pl["grade"]),
                    f"{name}_repeatability": _spearman(sh["a"], sh["b"]) if len(sh) > 2 else float("nan"),
                    f"{name}_sd": float(p["pg_throw"].std())})
    te = d.groupby(["book", "team", "pos_code"])["rel"].mean().unstack()
    out["lead_second_team"] = _spearman(te[1], te[2]) if {1, 2} <= set(te.columns) else float("nan")
    out.update(setup_battle(rows, V_f))
    out.update(spread_checks(rows, V_f, v[y]))
    return out


def spread_checks(rows: pd.DataFrame, V_f: np.ndarray, realised: np.ndarray) -> dict:
    """Does the model carry the real spread between positions? The calibration slope of the end's realised
    value on the model's value, by stage of the end (1 is right; under 1 the model is too flat), and the
    lead's first rock: the model's value gap between a lone non-hammer stone behind the tee in the 8-12
    ft and one in front of the tee in the 4-foot, against the realised gap."""
    rr = rows["rocks_remaining"].to_numpy()
    out = {}
    for lo, hi, name in ((12, 16, "slope_12plus"), (8, 11, "slope_8_11"), (4, 7, "slope_4_7"), (1, 3, "slope_1_3")):
        m = (rr >= lo) & (rr <= hi)
        x, yv = V_f[m], realised[m]
        out[name] = float(np.cov(x, yv)[0, 1] / np.var(x, ddof=1)) if m.sum() > 10 and np.var(x) > 0 else float("nan")
    if "net_pot" in rows:
        # the model's error along net rock potential: flat when expectation uses potential fully
        resid = realised - V_f
        for lo, hi, name in ((12, 16, "pot_resid_12plus"), (8, 11, "pot_resid_8_11"), (4, 7, "pot_resid_4_7"), (1, 3, "pot_resid_1_3")):
            m = (rr >= lo) & (rr <= hi)
            out[name] = _spearman(pd.Series(resid[m]), pd.Series(rows["net_pot"].to_numpy()[m])) if m.sum() > 10 else float("nan")
    one = ((rows["shot"] == 2) & (rows["opp_in_house"] == 1) & (rows["own_in_house"] == 0) & (rows["stones_in_play"] == 1)).to_numpy()
    back = one & (rows["opp_behind_tee"] == 1).to_numpy() & (rows["opp_min_dist"] > 29.7).to_numpy()
    front = one & (rows["opp_behind_tee"] == 0).to_numpy() & (rows["opp_min_dist"] <= 29.7).to_numpy()
    if back.sum() > 5 and front.sum() > 5:
        out["first_rock_gap_model"] = float(V_f[back].mean() - V_f[front].mean())
        out["first_rock_gap_real"] = float(realised[back].mean() - realised[front].mean())
    return out


def setup_battle(rows: pd.DataFrame, V_f: np.ndarray, min_half: int = 30) -> dict:
    """The battle for the type of end: per end, the change in the model's value from the empty sheet to the
    position after the free guard zone (hammer-adjusted points), from each team's view; per team and event,
    its split-half repeatability and its correlation with the win rate."""
    r = rows.reset_index(drop=True)
    fgz = r["fgz_rocks"].to_numpy() if "fgz_rocks" in r else np.full(len(r), 5)
    v0 = pd.Series(V_f[r["shot"].to_numpy() == 1], index=pd.MultiIndex.from_frame(r.loc[r["shot"] == 1, ["game_key", "end"]]))
    at = r["shot"].to_numpy() == fgz + 1                      # the row whose pre-position is the end of the setup
    vb = pd.Series(V_f[at], index=pd.MultiIndex.from_frame(r.loc[at, ["game_key", "end"]]))
    swing = (vb - v0.reindex(vb.index)).dropna()
    ends = r[r["shot"] == 1].set_index(["game_key", "end"])[["book", "hammer_team", "diff_hammer", "ends_remaining"]].reindex(swing.index)
    # the part of the swing explained by the score and ends left alone: good teams lead more often, so an
    # unadjusted setup battle partly measures leading; the gate also reports the swing within the situation
    sit = ends["diff_hammer"].clip(-3, 3).astype(str) + "|" + ends["ends_remaining"].clip(1, 8).astype(str)
    within = swing - swing.groupby(sit.to_numpy()).transform("mean")
    teams = r.groupby("game_key")["team"].agg(lambda x: sorted(set(x)))
    other = [t[1] if h == t[0] else t[0] for h, t in zip(ends["hammer_team"], teams.reindex(ends.index.get_level_values(0)))
             if len(t) == 2] if len(ends) else []
    keep = [len(t) == 2 for t in teams.reindex(ends.index.get_level_values(0))]
    ends, swing, within = ends[keep], swing[keep], within[keep]
    gk = ends.index.get_level_values(0)
    view = pd.concat([pd.DataFrame({"book": ends["book"].to_numpy(), "team": ends["hammer_team"].to_numpy(), "game_key": gk,
                                    "s": swing.to_numpy(), "w": within.to_numpy()}),
                      pd.DataFrame({"book": ends["book"].to_numpy(), "team": other, "game_key": gk,
                                    "s": -swing.to_numpy(), "w": -within.to_numpy()})])
    view["half"] = view.groupby(["book", "team"])["game_key"].rank(method="dense").astype(int) % 2
    h = view.groupby(["book", "team", "half"])["s"].agg(["mean", "size"]).unstack()
    h = h[(h[("size", 0)] >= min_half) & (h[("size", 1)] >= min_half)]
    rec = _records(r, ["book", "team"])
    wr = pd.Series({k: v[0] / (v[0] + v[1]) for k, v in rec.items() if sum(v) >= 5}, dtype=float)
    te = view.groupby(["book", "team"])[["s", "w"]].mean()
    j = pd.concat([te, wr.rename("wr")], axis=1).dropna() if len(wr) else pd.DataFrame(columns=["s", "w", "wr"])
    hw = view.groupby(["book", "team", "half"])["w"].agg(["mean", "size"]).unstack()
    hw = hw[(hw[("size", 0)] >= min_half) & (hw[("size", 1)] >= min_half)]
    return {"setup_repeatability": _spearman(h[("mean", 0)], h[("mean", 1)]) if len(h) > 2 else float("nan"),
            "setup_winrate": _spearman(j["s"], j["wr"]) if len(j) > 2 else float("nan"),
            "setup_repeatability_within": _spearman(hw[("mean", 0)], hw[("mean", 1)]) if len(hw) > 2 else float("nan"),
            "setup_winrate_within": _spearman(j["w"], j["wr"]) if len(j) > 2 else float("nan"),
            "setup_sd": float(swing.std())}


def run_experiment(ds: Dataset, name: str, sets: tuple[str, ...], split: str = "time", cutoff_year: int = 2024,
                   fold: int = 0, seed: int = 0, reports: str = "reports", inventory_csv: str | None = None,
                   target: str = "final", monotone: bool = False, split_model: str | None = None,
                   early_sets: tuple = (), blend: tuple[int, int] | None = None) -> dict:
    t0 = time.time()
    rows = attach_tier(ds.rows, inventory_csv)
    tr, te = split_rows(rows, split, cutoff_year, fold)
    X_f, f_cols, X_g, g_cols = design_matrices(rows, ds.X, sets)
    tri_cols = TRIVIAL_FEATURES + (FEATURE_SETS["situation"] if "situation" in sets else [])
    X_t = np.column_stack([column(rows, ds.X, c) for c in tri_cols])
    y = ds.y
    P = {}
    if split_model:
        from .split import fit_split
        sm = fit_split(rows, ds.X, y, tr, tuple(early_sets), tuple(sets), seed, blend=blend)
        P["f"], P["g"] = sm.predict(rows, ds.X, te)
        m = make_model(seed).fit(X_t[tr], y[tr])
        P["trivial"] = _full_proba(m, X_t[te])
        P = {k: P[k] for k in ("trivial", "f", "g")}
        target = f"split:{split_model}" + (f":blend{blend[0]}-{blend[1]}" if blend else "")
    else:
        t1 = time.time()
        fit_idx, fit_y, fit_w = training_rows(target, rows, X_f, y, tr, seed)
        log.info("%s: %s targets in %.0fs, %d weighted rows from %d", name, target, time.time() - t1, len(fit_idx), len(tr))
    mono = {"f": monotone_cst(f_cols) if monotone else None, "g": monotone_cst(g_cols) if monotone else None}
    for mname, Xm, cat in (() if split_model else (("trivial", X_t, None), ("f", X_f, None), ("g", X_g, _cat_index(g_cols)))):
        t1 = time.time()
        if mname == "trivial":
            m = make_model(seed, cat).fit(Xm[tr], y[tr])       # the reference stays on final labels
        else:
            m = make_model(seed, cat, mono[mname]).fit(Xm[fit_idx], fit_y, sample_weight=fit_w)
        P[mname] = _full_proba(m, Xm[te])
        log.info("%s: %s fitted in %.0fs", name, mname, time.time() - t1)
    unm = (rows["mirror"].to_numpy() == 0)[te]
    rep = {"name": name, "sets": list(sets), "early_sets": list(early_sets), "target": target, "monotone": monotone, "split": split, "cutoff_year": cutoff_year if split == "time" else None,
           "fold": fold if split == "book" else None, "n_train": int(len(tr)), "n_test": int(len(te)),
           "test_books": sorted(set(rows["book"].to_numpy()[te])), "f_cols": f_cols, "g_cols": g_cols,
           "seconds": round(time.time() - t0, 1)}
    rep.update(evaluate({k: v[unm] for k, v in P.items()}, y[te][unm], rows.iloc[te[unm]], ds.X[te][unm]))
    first = rows.iloc[tr][(rows["mirror"].to_numpy()[tr] == 0) & (rows["shot"].to_numpy()[tr] == 1)]
    H = ValueSet.from_outcomes(first["label"]).H
    rep["frontend_gates"] = frontend_gates(rows.iloc[te[unm]], P["f"][unm], P["g"][unm], y[te][unm], H)
    rep["seconds"] = round(time.time() - t0, 1)
    out_dir = os.path.join(reports, "experiments")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, f"{name}.json"), "w") as f:
        json.dump(rep, f, indent=1, default=str)
    _append_log(os.path.join(out_dir, "log.md"), rep)
    _append_gates(os.path.join(out_dir, "frontend_gates.md"), rep)
    return rep


GATE_COLUMNS = ["seesaw_1_4", "seesaw_5_8", "lead_opponent", "lead_opponent_grade", "second_opponent", "lead_second_team",
                "lead_grade_player", "second_grade_player", "fourth_grade_player", "lead_grade_shot", "second_grade_shot",
                "lead_repeatability", "second_repeatability", "lead_sd", "setup_repeatability", "setup_winrate",
                "setup_repeatability_within", "setup_winrate_within",
                "slope_12plus", "slope_8_11", "slope_4_7", "slope_1_3", "first_rock_gap_model", "first_rock_gap_real",
                "pot_resid_12plus", "pot_resid_8_11", "pot_resid_4_7", "pot_resid_1_3"]


def _append_gates(path: str, rep: dict):
    g = rep["frontend_gates"]
    by_rr = rep["logloss_by_rocks_remaining"]
    def band(lo, hi, key):
        n = sum(v["n"] for r, v in by_rr.items() if lo <= int(r) <= hi)
        return sum(v["n"] * v[key] for r, v in by_rr.items() if lo <= int(r) <= hi) / n if n else float("nan")
    cols = ["name", "target", "mono", "f", "g", "f 12+", "f 5-11", "f 1-4"] + GATE_COLUMNS
    line = "| " + " | ".join([rep["name"], rep.get("target", "final"), "yes" if rep.get("monotone") else "", f"{rep['f_logloss']:.4f}", f"{rep['g_logloss']:.4f}",
                              f"{band(12, 16, 'f'):.4f}", f"{band(5, 11, 'f'):.4f}", f"{band(1, 4, 'f'):.4f}"]
                             + [f"{g.get(c, float('nan')):.3f}" for c in GATE_COLUMNS]) + " |\n"
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# Front-end gates\n\nHeld-out log-loss against the final end outcome (f overall and by band of rocks "
                    "remaining, g overall), then the front-end measures on the held-out events from Points Gained computed "
                    "with the experiment's f and g: `seesaw_*` the correlation of a stone's execution with the next stone's "
                    "(toward 0 is better), `*_opponent` the correlation of the two teams' mean execution at a position in the "
                    "same game (grades for reference), `lead_second_team` the team-event correlation, agreement with grades "
                    "(a check only), split-half repeatability, and the setup battle (the change in value over the free "
                    "guard zone per end, each team's view): its repeatability and correlation with win rate.\n\n"
                    "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n")
        f.write(line)


def _append_log(path: str, rep: dict):
    header = ("| name | split | sets | n_test | trivial | f | g | f: 1-4 left | f: 12+ left | s |\n"
              "|---|---|---|---|---|---|---|---|---|---|\n")
    by_rr = rep["logloss_by_rocks_remaining"]
    def band(lo, hi, key):
        n = sum(v["n"] for r, v in by_rr.items() if lo <= int(r) <= hi)
        return sum(v["n"] * v[key] for r, v in by_rr.items() if lo <= int(r) <= hi) / n if n else float("nan")
    line = (f"| {rep['name']} | {rep['split']}{'' if rep['split'] != 'time' else ' ≤' + str(rep['cutoff_year'])} | "
            f"{'+'.join(rep['sets'])} | {rep['n_test']} | {rep['trivial_logloss']:.4f} | {rep['f_logloss']:.4f} | "
            f"{rep['g_logloss']:.4f} | {band(1, 4, 'f'):.4f} | {band(12, 16, 'f'):.4f} | {rep['seconds']:.0f} |\n")
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# Experiment log\n\nHeld-out log-loss (unmirrored rows). Bands are n-weighted means over rocks remaining. "
                    "The trivial model (rocks remaining, hammer, count) also takes the situation columns when the set includes `situation`.\n\n" + header)
        f.write(line)
