"""Rock slots: the rocks that matter, each with its own trait vector (feature set `slots`).

Trait counts (model/trait_features.py) say how many of a team's rocks are open, and separately how many
are shot rock; they cannot say whether *the shot rock* is open. Slots keep the rock whole: the shot rock,
second shot and third shot (either team's), and each team's guard nearest the pin, every one with its
owner and its traits as they are in this position. Late in an end these are most of the rocks in play
(the endgame is close to a lookup on them); the rest stay in the counts.

Per slot: `owner` (1 hammer, 0 non-hammer, -1 no such rock), the ring and tee traits, wing,
controls_4ft, guarding, frozen to own / to the other colour (relative to the slot's owner), and
`exposure` (0 open, 1 partly open, 2 behind cover). Built from `rock_traits.parquet`; a row takes its
pre-shot position (the post position of `pre_source_shot`; no rocks for the empty sheet).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .trait_features import KEYS, load_tables

SLOTS = ["s1", "s2", "s3", "gh", "gn"]           # shot, second, third; hammer's and non-hammer's nearest guard
SLOT_TRAITS = ["four_foot", "eight_foot", "behind_tee", "wing", "controls_4ft", "guarding", "frozen_own", "frozen_opp"]
SLOT_FIELDS = ["owner"] + SLOT_TRAITS + ["exposure"]
SLOT_COLUMNS = [f"{s}_{f}" for s in SLOTS for f in SLOT_FIELDS]


def _fields(d: pd.DataFrame) -> pd.DataFrame:
    out = d[KEYS].copy()
    out["owner"] = d["owner"].astype(float)
    for t in SLOT_TRAITS:
        out[t] = d[t].astype(float)
    out["exposure"] = np.where(d["behind_cover"], 2.0, np.where(d["partly_open"], 1.0, 0.0))
    return out


def compute_table(long: pd.DataFrame) -> pd.DataFrame:
    """One row per position with any rock: the slot columns."""
    parts = []
    for slot, flag in (("s1", "shot_rock"), ("s2", "second_shot"), ("s3", "third_shot")):
        parts.append((slot, _fields(long[long[flag]])))
    front = long[long["front"]].assign(d=lambda t: np.hypot(t["x"], t["y"]))
    for slot, who in (("gh", 1), ("gn", 0)):
        g = front[front["owner"] == who].sort_values("d", kind="stable").drop_duplicates(KEYS)
        parts.append((slot, _fields(g)))
    table = long[KEYS].drop_duplicates().reset_index(drop=True)
    for slot, f in parts:
        table = table.merge(f.rename(columns={c: f"{slot}_{c}" for c in SLOT_FIELDS}), on=KEYS, how="left")
    return fill_absent(table)


def fill_absent(t: pd.DataFrame) -> pd.DataFrame:
    for s in SLOTS:
        t[f"{s}_owner"] = t[f"{s}_owner"].fillna(-1.0)
    return t.fillna({c: 0.0 for c in SLOT_COLUMNS})


def attach_slots(rows: pd.DataFrame, parquet_root: str) -> pd.DataFrame:
    """The `slots` design columns for the training rows (pre-shot position of each row)."""
    long, _ = load_tables(parquet_root)
    t = compute_table(long).set_index(KEYS)[SLOT_COLUMNS]
    idx = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["pre_source_shot"]])
    v = fill_absent(t.reindex(idx).reset_index(drop=True))
    return rows.assign(**{c: v[c].to_numpy(float) for c in SLOT_COLUMNS})
