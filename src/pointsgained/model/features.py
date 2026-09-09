"""Baseline hand-built position features (design Section 5.4), canonical hammer frame.

'own' means the hammer team, 'opp' the non-hammer team.
"""
from __future__ import annotations

import numpy as np

from ..core.geometry import RING_12_RADIUS, STONE_RADIUS, STONE_DIAMETER, ring_of
from ..core.positions import Position

CENTER_LANE = 24.0
FEATURE_NAMES = [
    "rocks_remaining", "next_thrower_has_hammer", "fgz_rocks", "stones_in_play",
    "count", "shot_rock_ring", "margin", "second_owner", "third_owner",
    "own_in_house", "opp_in_house", "own_behind_tee", "opp_behind_tee",
    "own_guard_left", "own_guard_center", "own_guard_right",
    "opp_guard_left", "opp_guard_center", "opp_guard_right",
    "center_guard_depth", "shot_rock_covered", "button_covered", "own_min_dist", "opp_min_dist",
    "boundary_gap", "near_tie",
]
NEAR_TIE_INCHES = 2.0   # below the diagram's resolving power: a perceptual tie on the sheet
RING_CODE = {"button": 0, "4ft": 1, "8ft": 2, "12ft": 3, "out": 4}


def _covered(x: float, y: float, gx: np.ndarray, gy: np.ndarray, allowance: float = STONE_DIAMETER) -> bool:
    """Crude straight-line cover test: some stone in front (larger y) within a lateral allowance."""
    if len(gx) == 0:
        return False
    front = gy > y + STONE_RADIUS
    return bool(np.any(front & (np.abs(gx - x) <= allowance)))


def position_features(p: Position) -> np.ndarray:
    x, y, own = p.x, p.y, p.owner == 1
    d = np.hypot(x, y)
    in_house = d <= RING_12_RADIUS + STONE_RADIUS
    f = {k: 0.0 for k in FEATURE_NAMES}
    f["rocks_remaining"] = p.rocks_remaining
    f["next_thrower_has_hammer"] = float(p.next_thrower_has_hammer)
    f["fgz_rocks"] = p.fgz_rocks
    f["stones_in_play"] = p.n
    order = np.argsort(d)
    ih = [i for i in order if in_house[i]]
    if ih:
        first = ih[0]
        sign = 1 if own[first] else -1
        cnt = 0
        for i in ih:
            if own[i] != own[first]:
                break
            cnt += 1
        f["count"] = float(max(-3, min(3, sign * cnt)))
        f["shot_rock_ring"] = RING_CODE[ring_of(x[first], y[first])]
        opp_ih = [i for i in ih if own[i] != own[first]]
        f["margin"] = float(sign * ((d[opp_ih[0]] - d[first]) if opp_ih else (RING_12_RADIUS + STONE_RADIUS - d[first])))
        f["second_owner"] = (1.0 if own[ih[1]] else -1.0) if len(ih) > 1 else 0.0
        f["third_owner"] = (1.0 if own[ih[2]] else -1.0) if len(ih) > 2 else 0.0
        f["shot_rock_covered"] = float(_covered(x[first], y[first], x, y))
        # gap at the ownership boundary: distance between the last counting stone and the first
        # opposing stone. Under NEAR_TIE_INCHES the count is not knowable from the sheet.
        if opp_ih:
            last_counting = ih[cnt - 1]
            f["boundary_gap"] = float(d[opp_ih[0]] - d[last_counting])
            f["near_tie"] = float(f["boundary_gap"] < NEAR_TIE_INCHES)
        else:
            f["boundary_gap"] = float(RING_12_RADIUS + STONE_RADIUS - d[ih[-1]])
    else:
        f["shot_rock_ring"] = RING_CODE["out"]
        f["margin"] = 0.0
        f["boundary_gap"] = 0.0
    f["own_in_house"] = float(np.sum(in_house & own))
    f["opp_in_house"] = float(np.sum(in_house & ~own))
    f["own_behind_tee"] = float(np.sum(in_house & own & (y < 0)))
    f["opp_behind_tee"] = float(np.sum(in_house & ~own & (y < 0)))
    guard = (~in_house) & (y > 0)
    for who, mask in (("own", own), ("opp", ~own)):
        g = guard & mask
        f[f"{who}_guard_left"] = float(np.sum(g & (x < -CENTER_LANE)))
        f[f"{who}_guard_center"] = float(np.sum(g & (np.abs(x) <= CENTER_LANE)))
        f[f"{who}_guard_right"] = float(np.sum(g & (x > CENTER_LANE)))
    cg = guard & (np.abs(x) <= CENTER_LANE)
    f["center_guard_depth"] = float(np.min(y[cg])) if np.any(cg) else 0.0
    f["button_covered"] = float(_covered(0.0, 0.0, x, y))
    f["own_min_dist"] = float(np.min(d[own])) if np.any(own) else 200.0
    f["opp_min_dist"] = float(np.min(d[~own])) if np.any(~own) else 200.0
    return np.array([f[k] for k in FEATURE_NAMES], dtype=float)
