"""Configuration labels and pair measures for every position, cached next to the feature cache.

One row per post-shot position in the canonical stones table (keyed game_key, end, shot); a shot's
pre-shot position is the post position of its `pre_source_shot` (0 = the empty sheet). The labels
and pair measures are unchanged by mirroring, so the same values serve the mirrored training rows.
Feature set `config` (model/train.py) puts them in f and g as `cfg_<label>` and the measure columns.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd

from ..core.configurations import LABELS, MEASURES, configuration, measures
from ..core.positions import Position

KEYS = ["game_key", "end", "shot"]
CONFIG_COLUMNS = [f"cfg_{k}" for k in LABELS] + MEASURES


def compute_table(stones: pd.DataFrame) -> pd.DataFrame:
    """Labels and pair measures of every post-shot position in the canonical stones table."""
    idx = stones.groupby(KEYS, sort=False).indices
    x, y, o = stones["x"].to_numpy(float), stones["y"].to_numpy(float), stones["owner"].to_numpy(int)
    lab = np.zeros((len(idx), len(LABELS)), dtype=bool)
    pair = np.zeros((len(idx), len(MEASURES)))
    keys = []
    for j, (k, i) in enumerate(idx.items()):
        p = Position(x[i], y[i], o[i], 16 - int(k[2]))
        c, m = configuration(p), measures(p)
        lab[j] = [c[n] for n in LABELS]
        pair[j] = [m[n] for n in MEASURES]
        keys.append(k)
    out = pd.DataFrame(keys, columns=KEYS)
    out[LABELS] = lab
    out[MEASURES] = pair
    return out


def load_table(parquet_root: str, rebuild: bool = False) -> pd.DataFrame:
    """The cached table, rebuilt when the stones table or the label list changed."""
    path = os.path.join(parquet_root, "configurations.parquet")
    meta_path = os.path.join(parquet_root, "configurations.json")
    stones_path = os.path.join(parquet_root, "stones_canonical.parquet")
    sig = {"labels": LABELS, "pairs": MEASURES, "stones_mtime": os.path.getmtime(stones_path)}
    if not rebuild and os.path.exists(path) and os.path.exists(meta_path):
        with open(meta_path) as f:
            if json.load(f) == sig:
                return pd.read_parquet(path)
    table = compute_table(pd.read_parquet(stones_path))
    table.to_parquet(path, index=False)
    with open(meta_path, "w") as f:
        json.dump(sig, f)
    return table


def empty_row() -> dict:
    c, m = configuration(Position.empty()), measures(Position.empty())
    return {**c, **m}


def pre_and_post(rows: pd.DataFrame, table: pd.DataFrame, has_post: pd.Series | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(pre, post) frames aligned with `rows`, columns LABELS + MEASURES. The pre-shot position is the
    post position of `pre_source_shot` (0: the empty sheet). A post position absent from the table is the
    empty sheet when the shot has a diagram (`has_post`), unknown (labels False) otherwise."""
    cols = LABELS + MEASURES
    empty = empty_row()
    t = table.set_index(KEYS)[cols]
    pre_idx = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["pre_source_shot"]])
    pre = t.reindex(pre_idx).reset_index(drop=True)
    post_idx = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["shot"]])
    post = t.reindex(post_idx).reset_index(drop=True)
    known = np.ones(len(rows), dtype=bool) if has_post is None else has_post.fillna(False).to_numpy(dtype=bool)
    for c in cols:
        fill = float(empty[c])
        pre[c] = pre[c].astype(float).fillna(fill)
        post[c] = post[c].astype(float).where(post[c].notna(), np.where(known, fill, 0.0))
    for c in LABELS:
        pre[c], post[c] = pre[c].astype(bool), post[c].astype(bool)
    return pre, post


def config_row(p: Position) -> dict[str, float]:
    """The `config` design columns of one position."""
    c, m = configuration(p), measures(p)
    return {**{f"cfg_{k}": float(c[k]) for k in LABELS}, **{k: float(m[k]) for k in MEASURES}}


def attach_config(rows: pd.DataFrame, table: pd.DataFrame) -> pd.DataFrame:
    """The `config` design columns for the training rows (pre-shot position of each row)."""
    pre, _ = pre_and_post(rows, table)
    add = {f"cfg_{k}": pre[k].to_numpy(dtype=float) for k in LABELS}
    add.update({k: pre[k].to_numpy(dtype=float) for k in MEASURES})
    return rows.assign(**add)
