"""Relations for the next thrower, cached next to the feature cache: the draw to beat (core/draw.py,
feature set `draw`), doubles and runbacks (core/combos.py, feature set `combo`) and the tap (core/taps.py,
feature set `tap`; its table also keeps the trait counts of the position after the best tap, for the
trait rescore `tapgrade` in model/trait_study.py).

`<name>_features.parquet` has one row per post-shot position in the canonical stones table, with the
relation computed for each team as the next thrower (`<feature>_h` for the hammer team, `<feature>_n`
for the other). A training row takes its pre-shot position (the post position of `pre_source_shot`; the
empty sheet when 0 or when the position has no stones) seen by the team throwing the shot.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd

from ..core.combos import COMBO_FEATURES, combos
from ..core.draw import DRAW_FEATURES, draw_to_beat
from ..core.taps import TAP_COUNT_COLUMNS, TAP_FEATURES, taps

KEYS = ["game_key", "end", "shot"]
SIDES = (("h", 1), ("n", 0))
CACHE_VERSION = {"draw": 2, "combo": 2, "tap": 5}    # combo 2: dbl_jam; tap 3: curled reach; 4-5: the zone around the 4-foot
RELATIONS = {"draw": (DRAW_FEATURES, draw_to_beat), "combo": (COMBO_FEATURES, combos),
             "tap": (TAP_FEATURES, lambda x, y, o, t: taps(x, y, o, t, with_counts=True))}
EXTRAS = {"tap": TAP_COUNT_COLUMNS}      # cached with the relation, not design columns


def _stored(name: str) -> list[str]:
    return RELATIONS[name][0] + EXTRAS.get(name, [])


def compute_table(stones: pd.DataFrame, name: str = "draw") -> pd.DataFrame:
    features, fn = _stored(name), RELATIONS[name][1]
    x, y, o = stones["x"].to_numpy(float), stones["y"].to_numpy(float), stones["owner"].to_numpy(int)
    idx = stones.groupby(KEYS, sort=False).indices
    vals = np.zeros((len(idx), 2 * len(features)))
    keys = []
    for j, (k, i) in enumerate(idx.items()):
        for s, (_, who) in enumerate(SIDES):
            f = fn(x[i], y[i], o[i], who)
            vals[j, s * len(features):(s + 1) * len(features)] = [f[c] for c in features]
        keys.append(k)
    out = pd.DataFrame(keys, columns=KEYS)
    out[[f"{c}_{t}" for t, _ in SIDES for c in features]] = vals
    return out


def load_table(parquet_root: str, rebuild: bool = False, name: str = "draw") -> pd.DataFrame:
    features = _stored(name)
    path = os.path.join(parquet_root, f"{name}_features.parquet")
    meta_path = os.path.join(parquet_root, f"{name}_features.json")
    stones_path = os.path.join(parquet_root, "stones_canonical.parquet")
    sig = {"version": CACHE_VERSION[name], "features": features, "stones_mtime": os.path.getmtime(stones_path)}
    if not rebuild and os.path.exists(path) and os.path.exists(meta_path):
        with open(meta_path) as f:
            if json.load(f) == sig:
                return pd.read_parquet(path)
    table = compute_table(pd.read_parquet(stones_path), name)
    table.to_parquet(path, index=False)
    with open(meta_path, "w") as f:
        json.dump(sig, f)
    return table


def attach_draw(rows: pd.DataFrame, table: pd.DataFrame, name: str = "draw") -> pd.DataFrame:
    """The `draw` (or `combo`, `tap`) design columns: the relation in each row's pre-shot position, for the team throwing."""
    features, fn = RELATIONS[name]
    t = table.set_index(KEYS)
    idx = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["pre_source_shot"]])
    ham = rows["thrower_has_hammer"].fillna(False).to_numpy(dtype=bool)
    empty = {c: fn(np.zeros(0), np.zeros(0), np.zeros(0, dtype=int), 1)[c] for c in features}
    add = {}
    for c in features:
        h = t[f"{c}_h"].reindex(idx).to_numpy()
        n = t[f"{c}_n"].reindex(idx).to_numpy()
        v = np.where(ham, h, n)
        add[c] = np.where(np.isnan(v), empty[c], v)
    return rows.assign(**add)


def tap_counts_at(rows: pd.DataFrame, table: pd.DataFrame) -> pd.DataFrame:
    """Trait counts (TRAIT_COLUMNS naming) of the position after the thrower's best tap from each row's pre-shot
    position; NaN rows where the table has no such position (the empty sheet)."""
    from ..core.traits import TRAITS
    t = table.set_index(KEYS)
    idx = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["pre_source_shot"]])
    ham = rows["thrower_has_hammer"].fillna(False).to_numpy(dtype=bool)
    out = {}
    for team in ("h", "n"):
        for k in TRAITS:
            h = t[f"tp_{team}_{k}_h"].reindex(idx).to_numpy()
            n = t[f"tp_{team}_{k}_n"].reindex(idx).to_numpy()
            out[f"{team}_{k}"] = np.where(ham, h, n)
    return pd.DataFrame(out, index=rows.index)


def attach_tap_edge(rows: pd.DataFrame, tap_table: pd.DataFrame, draw_table: pd.DataFrame) -> pd.DataFrame:
    """Feature set `tapedge`, the minimal tap overlay: how many more the thrower lies after its best straight
    tap than after a made draw (the draw leaves the count as it is when no path is open); 0 when the tap does
    not beat the draw or has to come around cover. The counting study (30 September 2026) found the model
    under-prices exactly these positions by about 0.1 points; come-around taps and the rest are priced by the
    rocks."""
    t = attach_draw(attach_draw(rows[KEYS + ["pre_source_shot", "thrower_has_hammer"]], tap_table, "tap"), draw_table, "draw")
    sign = np.where(rows["thrower_has_hammer"].fillna(False).to_numpy(dtype=bool), 1.0, -1.0)
    now = rows["count"].to_numpy(dtype=float) * sign
    draw = np.where(t["draw_open_sides"].to_numpy() >= 1, t["draw_gain"].to_numpy(), now).clip(-3, 3)
    tap = np.where(t["tap_on"].to_numpy() == 1, now + t["tap_swing"].to_numpy(), now).clip(-3, 3)
    edge = np.where(t["tap_covered"].to_numpy() == 0, np.maximum(tap - draw, 0.0), 0.0)
    return rows.assign(tap_edge=edge)
