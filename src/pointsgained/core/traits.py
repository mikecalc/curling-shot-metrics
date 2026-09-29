"""Rock traits: what a single stone is, as a set of objective yes/no properties.

A configuration (core/configurations.py) describes the whole position. A trait describes one stone: it is
in the four-foot, it is behind the tee, it is frozen to an opponent's stone, it is open or behind cover.
Every stone carries a trait vector; the traits overlap by design (a four-foot stone is also in the eight
and the twelve), and the corpus says which of them, held by the hammer or the non-hammer team at a given
stage of the end, go with which end results (model/trait_study.py). No tracking: a stone's traits are read
off the position it is in. Vocabulary by Mike Calcagno (2026-09-29): a single centre guard at the start of
an end is "in the front" and "controlling the 4-foot" and nothing else (and open).

Canonical frame (core/positions.py): inches, pin at (0, 0), y > 0 towards the hog line, owner 1 = hammer.
Every test uses |x| only, so traits are unchanged by mirroring.
"""
from __future__ import annotations

import numpy as np

from .geometry import RING_12_RADIUS, RING_4_RADIUS, RING_8_RADIUS, STONE_DIAMETER, STONE_RADIUS
from .positions import Position

CENTER_LANE = 24.0        # |x| <= 24 in: the width of the 4-foot (as in the features and configurations)
FROZEN_TOLERANCE = 2.0    # centre distance up to a stone's diameter plus 2 in: touching, within the diagram's resolution

TRAITS = [
    "four_foot",      # in or touching the 4-foot
    "eight_foot",     # in or touching the 8-foot (includes the 4-foot)
    "twelve_foot",    # in or touching the 12-foot: in the house
    "above_tee",      # in the house, in front of the tee line
    "behind_tee",     # in the house, behind the tee line
    "wing",           # in the house, outside the 4-foot lane (|x| > 24 in)
    "front",          # in front of the house: the guard zone
    "controls_4ft",   # in the 4-foot lane and in front of the 4-foot: a centre guard or a high centre stone
    "guarding",       # in front of a stone in the house (either team's), within a stone's width of its line
    "shot_rock",      # shot rock (closest to the pin in the house, either team)
    "second_shot",    # second shot
    "third_shot",     # third shot
    "frozen_own",     # touching a stone of its own team behind it: the front stone of a freeze
    "frozen_opp",     # touching an opponent's stone behind it
    "open",           # no stone in front of it within a stone's width of its line
    "partly_open",    # the nearest stone in front of it overlaps its line by less than half a stone
    "behind_cover",   # a stone in front of it overlaps its line by half a stone or more
]
T = {k: i for i, k in enumerate(TRAITS)}


def stone_traits(p: Position) -> np.ndarray:
    """Boolean matrix (n stones, len(TRAITS)) for one canonical position."""
    return traits_xy(p.x, p.y, p.owner)


def traits_xy(x: np.ndarray, y: np.ndarray, owner: np.ndarray) -> np.ndarray:
    n = len(x)
    out = np.zeros((n, len(TRAITS)), dtype=bool)
    if n == 0:
        return out
    x, y = np.asarray(x, float), np.asarray(y, float)
    d = np.hypot(x, y)
    house = d <= RING_12_RADIUS + STONE_RADIUS
    out[:, T["four_foot"]] = d <= RING_4_RADIUS + STONE_RADIUS
    out[:, T["eight_foot"]] = d <= RING_8_RADIUS + STONE_RADIUS
    out[:, T["twelve_foot"]] = house
    out[:, T["above_tee"]] = house & (y > 0)
    out[:, T["behind_tee"]] = house & (y < 0)
    out[:, T["wing"]] = house & (np.abs(x) > CENTER_LANE)
    out[:, T["front"]] = ~house & (y > 0)
    out[:, T["controls_4ft"]] = (np.abs(x) <= CENTER_LANE) & (y > RING_4_RADIUS + STONE_RADIUS)

    ih = np.flatnonzero(house)
    ih = ih[np.argsort(d[ih], kind="stable")]
    for k, name in enumerate(("shot_rock", "second_shot", "third_shot")):
        if len(ih) > k:
            out[ih[k], T[name]] = True

    # pairwise: [s, t] is stone s relative to stone t
    dx = np.abs(x[:, None] - x[None, :])
    dy = y[:, None] - y[None, :]
    not_self = ~np.eye(n, dtype=bool)
    in_front = (dy > STONE_RADIUS) & not_self                # s is in front of t (clear of it along the line)
    out[:, T["guarding"]] = (in_front & (dx <= STONE_DIAMETER) & house[None, :]).any(axis=1)

    # frozen: s touches t and t is behind it (more behind than beside). The front stone is the frozen one.
    touching = (np.hypot(dx, dy) <= STONE_DIAMETER + FROZEN_TOLERANCE) & (dy > STONE_RADIUS / 2) & not_self
    same = owner[:, None] == owner[None, :]
    out[:, T["frozen_own"]] = (touching & same).any(axis=1)
    out[:, T["frozen_opp"]] = (touching & ~same).any(axis=1)

    # exposure: the smallest lateral offset of any stone in front of s (t in front of s is in_front[t, s])
    offs = np.where(in_front.T, dx, np.inf).min(axis=1)
    out[:, T["behind_cover"]] = offs <= STONE_RADIUS
    out[:, T["partly_open"]] = (offs > STONE_RADIUS) & (offs <= STONE_DIAMETER)
    out[:, T["open"]] = offs > STONE_DIAMETER
    return out


def trait_type(m: np.ndarray) -> np.ndarray:
    """Each stone's trait vector as one integer bitmask (bit i = TRAITS[i])."""
    return (m.astype(np.int64) << np.arange(m.shape[1], dtype=np.int64)).sum(axis=1)


def type_name(mask: int) -> str:
    """The traits of a bitmask, joined with '+', leaving out the nested rings and the exposure when implied."""
    on = [k for i, k in enumerate(TRAITS) if (int(mask) >> i) & 1]
    if "four_foot" in on:
        on = [k for k in on if k not in ("eight_foot", "twelve_foot")]
    elif "eight_foot" in on:
        on = [k for k in on if k != "twelve_foot"]
    return "+".join(on) if on else "(none)"
