"""One experiment: a named feature set on one split, fitted once, scored on the held-out rows.

Splits:
  time   train on events dated through `cutoff_year`, test on later events (design 12.7)
  book   one GroupKFold fold by book (the same held-out books every time, for comparability)

Results go to reports/experiments/<name>.json and a line is appended to reports/experiments/log.md.
"""
from __future__ import annotations

import json
import logging
import os
import time

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

from .dataset import Dataset
from .features import FEATURE_NAMES
from .train import design_matrices, make_model, _cat_index, column, evaluate, _full_proba, TRIVIAL_FEATURES, FEATURE_SETS

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


def run_experiment(ds: Dataset, name: str, sets: tuple[str, ...], split: str = "time", cutoff_year: int = 2024,
                   fold: int = 0, seed: int = 0, reports: str = "reports", inventory_csv: str | None = None) -> dict:
    t0 = time.time()
    rows = attach_tier(ds.rows, inventory_csv)
    tr, te = split_rows(rows, split, cutoff_year, fold)
    X_f, f_cols, X_g, g_cols = design_matrices(rows, ds.X, sets)
    tri_cols = TRIVIAL_FEATURES + (FEATURE_SETS["situation"] if "situation" in sets else [])
    X_t = np.column_stack([column(rows, ds.X, c) for c in tri_cols])
    y = ds.y
    P = {}
    for mname, Xm, cat in (("trivial", X_t, None), ("f", X_f, None), ("g", X_g, _cat_index(g_cols))):
        t1 = time.time()
        m = make_model(seed, cat).fit(Xm[tr], y[tr])
        P[mname] = _full_proba(m, Xm[te])
        log.info("%s: %s fitted in %.0fs", name, mname, time.time() - t1)
    unm = (rows["mirror"].to_numpy() == 0)[te]
    rep = {"name": name, "sets": list(sets), "split": split, "cutoff_year": cutoff_year if split == "time" else None,
           "fold": fold if split == "book" else None, "n_train": int(len(tr)), "n_test": int(len(te)),
           "test_books": sorted(set(rows["book"].to_numpy()[te])), "f_cols": f_cols, "g_cols": g_cols,
           "seconds": round(time.time() - t0, 1)}
    rep.update(evaluate({k: v[unm] for k, v in P.items()}, y[te][unm], rows.iloc[te[unm]], ds.X[te][unm]))
    out_dir = os.path.join(reports, "experiments")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, f"{name}.json"), "w") as f:
        json.dump(rep, f, indent=1, default=str)
    _append_log(os.path.join(out_dir, "log.md"), rep)
    return rep


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
            f.write("# Experiment log\n\nHeld-out log-loss (unmirrored rows). Bands are n-weighted means over rocks remaining.\n\n" + header)
        f.write(line)
