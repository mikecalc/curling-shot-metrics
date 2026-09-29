"""Rock traits for every stone of every position, cached next to the feature cache (core/traits.py).

Two tables from the canonical stones table (post-shot positions, keyed game_key, end, shot):
- `rock_traits.parquet`: one row per stone per position, with owner, x, y, the trait booleans and `type`,
  the stone's trait vector as a bitmask;
- `trait_counts.parquet`: one row per position, each team's number of stones with each trait
  (`h_<trait>` for the hammer team, `n_<trait>` for the other).
A shot's pre-shot position is the post position of its `pre_source_shot` (0 = the empty sheet, all zeros).
Feature set `traits` (model/train.py) puts the pre-shot counts in f and g.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd

from ..core.traits import TRAITS, trait_type, traits_xy

KEYS = ["game_key", "end", "shot"]
TRAIT_COLUMNS = [f"h_{t}" for t in TRAITS] + [f"n_{t}" for t in TRAITS]


def compute_tables(stones: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(per-stone traits, per-position counts) for the canonical stones table."""
    stones = stones.sort_values(KEYS, kind="stable").reset_index(drop=True)
    x, y, o = stones["x"].to_numpy(float), stones["y"].to_numpy(float), stones["owner"].to_numpy(int)
    m = np.zeros((len(stones), len(TRAITS)), dtype=bool)
    for i in stones.groupby(KEYS, sort=False).indices.values():
        m[i] = traits_xy(x[i], y[i], o[i])
    long = stones[KEYS + ["owner", "x", "y"]].copy()
    long[TRAITS] = m
    long["type"] = trait_type(m)
    ham = (o == 1)[:, None]
    per = pd.DataFrame(np.hstack([m & ham, m & ~ham]).astype(np.int16), columns=TRAIT_COLUMNS)
    per[KEYS] = stones[KEYS]
    wide = per.groupby(KEYS, sort=False)[TRAIT_COLUMNS].sum().reset_index()
    return long, wide


def load_tables(parquet_root: str, rebuild: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    """The cached tables, rebuilt when the stones table or the trait list changed."""
    long_path = os.path.join(parquet_root, "rock_traits.parquet")
    wide_path = os.path.join(parquet_root, "trait_counts.parquet")
    meta_path = os.path.join(parquet_root, "rock_traits.json")
    stones_path = os.path.join(parquet_root, "stones_canonical.parquet")
    sig = {"traits": TRAITS, "stones_mtime": os.path.getmtime(stones_path)}
    if not rebuild and all(os.path.exists(p) for p in (long_path, wide_path, meta_path)):
        with open(meta_path) as f:
            if json.load(f) == sig:
                return pd.read_parquet(long_path), pd.read_parquet(wide_path)
    long, wide = compute_tables(pd.read_parquet(stones_path))
    long.to_parquet(long_path, index=False)
    wide.to_parquet(wide_path, index=False)
    with open(meta_path, "w") as f:
        json.dump(sig, f)
    return long, wide


def counts_at(rows: pd.DataFrame, wide: pd.DataFrame, shot_col: str = "pre_source_shot") -> pd.DataFrame:
    """Trait counts of the position after `shot_col` for each row (zeros for the empty sheet or a position
    with no stones), aligned with `rows`."""
    t = wide.set_index(KEYS)[TRAIT_COLUMNS]
    idx = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows[shot_col]])
    return t.reindex(idx).fillna(0).astype(float).reset_index(drop=True)


def attach_traits(rows: pd.DataFrame, wide: pd.DataFrame) -> pd.DataFrame:
    """The `traits` design columns for the training rows (pre-shot position of each row)."""
    c = counts_at(rows, wide)
    return rows.assign(**{k: c[k].to_numpy() for k in TRAIT_COLUMNS})
