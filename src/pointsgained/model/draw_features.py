"""The draw to beat (core/draw.py) for every position, cached next to the feature cache.

`draw_features.parquet` has one row per post-shot position in the canonical stones table, with the draw
computed for each team as the next thrower (`<feature>_h` for the hammer team, `<feature>_n` for the
other). A training row takes its pre-shot position (the post position of `pre_source_shot`; the empty
sheet when 0 or when the position has no stones) seen by the team throwing the shot. Feature set `draw`
(model/train.py) puts them in f and g.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd

from ..core.draw import DRAW_FEATURES, draw_to_beat

KEYS = ["game_key", "end", "shot"]
SIDES = (("h", 1), ("n", 0))
CACHE_VERSION = 1


def compute_table(stones: pd.DataFrame) -> pd.DataFrame:
    x, y, o = stones["x"].to_numpy(float), stones["y"].to_numpy(float), stones["owner"].to_numpy(int)
    idx = stones.groupby(KEYS, sort=False).indices
    vals = np.zeros((len(idx), 2 * len(DRAW_FEATURES)))
    keys = []
    for j, (k, i) in enumerate(idx.items()):
        for s, (_, who) in enumerate(SIDES):
            f = draw_to_beat(x[i], y[i], o[i], who)
            vals[j, s * len(DRAW_FEATURES):(s + 1) * len(DRAW_FEATURES)] = [f[c] for c in DRAW_FEATURES]
        keys.append(k)
    out = pd.DataFrame(keys, columns=KEYS)
    out[[f"{c}_{t}" for t, _ in SIDES for c in DRAW_FEATURES]] = vals
    return out


def load_table(parquet_root: str, rebuild: bool = False) -> pd.DataFrame:
    path = os.path.join(parquet_root, "draw_features.parquet")
    meta_path = os.path.join(parquet_root, "draw_features.json")
    stones_path = os.path.join(parquet_root, "stones_canonical.parquet")
    sig = {"version": CACHE_VERSION, "features": DRAW_FEATURES, "stones_mtime": os.path.getmtime(stones_path)}
    if not rebuild and os.path.exists(path) and os.path.exists(meta_path):
        with open(meta_path) as f:
            if json.load(f) == sig:
                return pd.read_parquet(path)
    table = compute_table(pd.read_parquet(stones_path))
    table.to_parquet(path, index=False)
    with open(meta_path, "w") as f:
        json.dump(sig, f)
    return table


def attach_draw(rows: pd.DataFrame, table: pd.DataFrame) -> pd.DataFrame:
    """The `draw` design columns: the draw to beat in each row's pre-shot position, for the team throwing."""
    t = table.set_index(KEYS)
    idx = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["pre_source_shot"]])
    ham = rows["thrower_has_hammer"].fillna(False).to_numpy(dtype=bool)
    empty = {c: draw_to_beat(np.zeros(0), np.zeros(0), np.zeros(0, dtype=int), 1)[c] for c in DRAW_FEATURES}
    add = {}
    for c in DRAW_FEATURES:
        h = t[f"{c}_h"].reindex(idx).to_numpy()
        n = t[f"{c}_n"].reindex(idx).to_numpy()
        v = np.where(ham, h, n)
        add[c] = np.where(np.isnan(v), empty[c], v)
    return rows.assign(**add)
