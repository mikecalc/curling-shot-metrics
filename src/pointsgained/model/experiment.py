"""One experiment: a named feature set on one split, fitted once, scored on the held-out rows.

Splits:
  time   train on events dated through `cutoff_year`, test on later events (design 12.7)
  book   one GroupKFold fold by book (the same held-out books every time, for comparability)

Targets:
  final      every row is labelled with the end's final score (the Phase 1 models)
  local:k    early rows (9 or more rocks remaining) are trained on the value of the position k stones
             later instead: a soft label, the out-of-fold f distribution there (the end's result if the end
             finishes first). Positions are valued more locally, and the noise of everything after them
             is averaged by the model rather than carried in the label.

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

from .aggregate import normalise_player
from .dataset import Dataset
from .features import FEATURE_NAMES
from .frontend import next_stone, opponent_same_game, split_half, _spearman
from .train import design_matrices, make_model, _cat_index, column, evaluate, _full_proba, TRIVIAL_FEATURES, FEATURE_SETS
from .value import N_OUT, HammerAdjustedPoints, ValueSet

LOCAL_MIN_ROCKS = 9          # rows with this many rocks remaining or more take the local target
SOFT_MIN_MASS = 0.005        # soft-label classes below this probability are dropped

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


def local_targets(rows: pd.DataFrame, X_f: np.ndarray, y: np.ndarray, tr: np.ndarray, k: int, seed: int = 0) -> np.ndarray:
    """Soft targets (n_rows, 7) for the training rows: one-hot on the end's result, except rows with
    LOCAL_MIN_ROCKS or more rocks remaining, which take the out-of-fold f distribution of the position k
    stones later (stage 1: f on final labels, GroupKFold by book within the training rows). If the end
    finishes within k stones the target is its result; if the chain breaks on a missing diagram, the
    last position reached is used."""
    T = np.zeros((len(y), N_OUT))
    T[np.arange(len(y)), y] = 1.0
    P1 = np.zeros_like(T)
    groups = rows["book"].to_numpy()[tr]
    for a, b in GroupKFold(n_splits=5).split(tr, groups=groups):
        m = make_model(seed).fit(X_f[tr[a]], y[tr[a]])
        P1[tr[b]] = _full_proba(m, X_f[tr[b]])
    post = rows["post_row"].to_numpy()
    last = rows["is_last_shot"].to_numpy(dtype=bool)
    rr = rows["rocks_remaining"].to_numpy()
    early = tr[rr[tr] >= LOCAL_MIN_ROCKS]
    j = early.copy()
    terminal = np.zeros(len(early), dtype=bool)
    moved = np.zeros(len(early), dtype=bool)
    for _ in range(k):
        active = ~terminal
        terminal |= active & last[j]                 # the end finished at j: its result is the target
        nxt = post[j]
        step = ~terminal & (nxt >= 0)
        j = np.where(step, nxt, j)
        moved |= step
    use = moved & ~terminal
    T[early[use]] = P1[j[use]]
    return T


def expand_soft(idx: np.ndarray, T: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(row index, class, weight) for fitting a classifier on soft targets: one weighted copy of a row per
    class with probability at least SOFT_MIN_MASS (one-hot rows stay single)."""
    sub = T[idx]
    r, c = np.nonzero(sub >= SOFT_MIN_MASS)
    return idx[r], c, sub[r, c]


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
    return out


def run_experiment(ds: Dataset, name: str, sets: tuple[str, ...], split: str = "time", cutoff_year: int = 2024,
                   fold: int = 0, seed: int = 0, reports: str = "reports", inventory_csv: str | None = None,
                   target: str = "final") -> dict:
    t0 = time.time()
    rows = attach_tier(ds.rows, inventory_csv)
    tr, te = split_rows(rows, split, cutoff_year, fold)
    X_f, f_cols, X_g, g_cols = design_matrices(rows, ds.X, sets)
    tri_cols = TRIVIAL_FEATURES + (FEATURE_SETS["situation"] if "situation" in sets else [])
    X_t = np.column_stack([column(rows, ds.X, c) for c in tri_cols])
    y = ds.y
    fit_idx, fit_y, fit_w = tr, y[tr], None
    if target.startswith("local:"):
        k = int(target.split(":")[1])
        t1 = time.time()
        T = local_targets(rows, X_f, y, tr, k, seed)
        fit_idx, fit_y, fit_w = expand_soft(tr, T)
        log.info("%s: local targets (k=%d) in %.0fs, %d weighted rows from %d", name, k, time.time() - t1, len(fit_idx), len(tr))
    elif target != "final":
        raise ValueError(f"unknown target {target!r}")
    P = {}
    for mname, Xm, cat in (("trivial", X_t, None), ("f", X_f, None), ("g", X_g, _cat_index(g_cols))):
        t1 = time.time()
        if mname == "trivial":
            m = make_model(seed, cat).fit(Xm[tr], y[tr])       # the reference stays on final labels
        else:
            m = make_model(seed, cat).fit(Xm[fit_idx], fit_y, sample_weight=fit_w)
        P[mname] = _full_proba(m, Xm[te])
        log.info("%s: %s fitted in %.0fs", name, mname, time.time() - t1)
    unm = (rows["mirror"].to_numpy() == 0)[te]
    rep = {"name": name, "sets": list(sets), "target": target, "split": split, "cutoff_year": cutoff_year if split == "time" else None,
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
                "lead_repeatability", "second_repeatability", "lead_sd"]


def _append_gates(path: str, rep: dict):
    g = rep["frontend_gates"]
    by_rr = rep["logloss_by_rocks_remaining"]
    def band(lo, hi, key):
        n = sum(v["n"] for r, v in by_rr.items() if lo <= int(r) <= hi)
        return sum(v["n"] * v[key] for r, v in by_rr.items() if lo <= int(r) <= hi) / n if n else float("nan")
    cols = ["name", "target", "f", "g", "f 12+", "f 5-11", "f 1-4"] + GATE_COLUMNS
    line = "| " + " | ".join([rep["name"], rep.get("target", "final"), f"{rep['f_logloss']:.4f}", f"{rep['g_logloss']:.4f}",
                              f"{band(12, 16, 'f'):.4f}", f"{band(5, 11, 'f'):.4f}", f"{band(1, 4, 'f'):.4f}"]
                             + [f"{g[c]:.3f}" for c in GATE_COLUMNS]) + " |\n"
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# Front-end gates\n\nHeld-out log-loss against the final end outcome (f overall and by band of rocks "
                    "remaining, g overall), then the front-end measures on the held-out events from Points Gained computed "
                    "with the experiment's f and g: `seesaw_*` the correlation of a stone's execution with the next stone's "
                    "(toward 0 is better), `*_opponent` the correlation of the two teams' mean execution at a position in the "
                    "same game (grades for reference), `lead_second_team` the team-event correlation, agreement with grades "
                    "(a check only) and split-half repeatability.\n\n"
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
