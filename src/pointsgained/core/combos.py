"""Doubles and runbacks for the next thrower: geometric configurations that unlock more than playing
against one stone (Mike Calcagno, 2026-09-29). A double that is not there does not get called, and the
skip plays something else; a runback gets called for its upside and is weighed against its downside.
Either way the position is what makes them available, and the aftermath of a miss is valued by
re-reading the house, so only availability and stakes are described here.

- **Double**: two of the other team's stones, the first hittable (nothing in front of it within half a
  stone of its line) and the second behind it, the pair not flat: the line between them at least
  DOUBLE_MIN_ANGLE from level, and within DOUBLE_MAX_SEP. The field doubles a flat split four feet
  or more apart about 2% of the time (core/configurations.py), a staggered one far more often.
  `dbl_jam` is the share of the back stone's exit cone that runs into a stone behind it (core/traits.py):
  "the double jams" is a common reason not to play one.
- **Runback**: a stone of either team in front of the other team's best stone, hittable, within
  RUNBACK_MAX_ANGLE of the line behind it and RUNBACK_MAX_DIST in front: driving it back removes the
  stone to beat. Straight runbacks (under RUNBACK_STRAIGHT) are the ones skips like.

Stakes are count swings from the thrower's side: what the thrower would lie with the stones removed,
against what it lies now. Straight-line geometry (hits carry little curl). Canonical frame; mirror-symmetric.
"""
from __future__ import annotations

import numpy as np

from .configurations import FLAT_MAX_ANGLE, RUNBACK_MAX_ANGLE, RUNBACK_MAX_DIST, RUNBACK_STRAIGHT
from .geometry import RING_12_RADIUS, STONE_DIAMETER, STONE_RADIUS
from .traits import jam_share

DOUBLE_MIN_ANGLE = FLAT_MAX_ANGLE      # flatter than this the double is (nearly) off
DOUBLE_MAX_SEP = 96.0                  # eight feet
NO_ANGLE, NO_DIST = 90.0, 300.0

COMBO_FEATURES = ["dbl_on", "dbl_house", "dbl_sep", "dbl_angle", "dbl_swing", "dbl_jam",
                  "rb_on", "rb_straight", "rb_angle", "rb_dist", "rb_front_own", "rb_swing"]


def signed_count(x: np.ndarray, y: np.ndarray, owner: np.ndarray, thrower: int) -> int:
    """What the thrower lies (+) or the other team lies (-) in this position."""
    d = np.hypot(x, y)
    ih = np.flatnonzero(d <= RING_12_RADIUS + STONE_RADIUS)
    if not len(ih):
        return 0
    o = owner[ih[np.argsort(d[ih])]]
    n = int(np.argmax(o != o[0])) if (o != o[0]).any() else len(o)
    return n if o[0] == thrower else -n


def hittable(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """No stone in front within half a stone of its line (open or partly open, as the traits have it)."""
    dx = np.abs(x[:, None] - x[None, :])
    in_front = (y[None, :] - y[:, None]) > STONE_RADIUS
    return ~(in_front & (dx <= STONE_RADIUS)).any(axis=1)


def combos(x: np.ndarray, y: np.ndarray, owner: np.ndarray, thrower: int) -> dict[str, float]:
    """Double and runback availability and stakes for `thrower` (1 hammer, 0 non-hammer)."""
    x, y, owner = np.asarray(x, float), np.asarray(y, float), np.asarray(owner, int)
    out = {"dbl_on": 0.0, "dbl_house": 0.0, "dbl_sep": NO_DIST, "dbl_angle": 0.0, "dbl_swing": 0.0, "dbl_jam": 0.0,
           "rb_on": 0.0, "rb_straight": 0.0, "rb_angle": NO_ANGLE, "rb_dist": NO_DIST, "rb_front_own": 0.0, "rb_swing": 0.0}
    if len(x) < 2:
        return out
    d = np.hypot(x, y)
    house = d <= RING_12_RADIUS + STONE_RADIUS
    hit = hittable(x, y)
    now = signed_count(x, y, owner, thrower)
    opp = np.flatnonzero(owner != thrower)

    # doubles: first stone a (hittable), second b behind it, not flat, not too far
    best = None
    for a in opp:
        if not hit[a]:
            continue
        for b in opp:
            if b == a or y[b] >= y[a]:
                continue
            sep = float(np.hypot(x[a] - x[b], y[a] - y[b]))
            ang = float(np.degrees(np.arctan2(y[a] - y[b], abs(x[a] - x[b]))))   # 0 level, 90 straight behind
            if sep > DOUBLE_MAX_SEP or ang < DOUBLE_MIN_ANGLE:
                continue
            both = bool(house[a] and house[b])
            keep = np.ones(len(x), dtype=bool)
            keep[[a, b]] = False
            swing = signed_count(x[keep], y[keep], owner[keep], thrower) - now
            key = (both, swing, -sep)
            if best is None or key > best[0]:
                best = (key, sep, ang, both, swing, b)
    if best is not None:
        _, sep, ang, both, swing, b = best
        out.update(dbl_on=1.0, dbl_house=float(both), dbl_sep=sep, dbl_angle=ang, dbl_swing=float(swing),
                   dbl_jam=float(jam_share(x, y)[0][b]))

    # runbacks on the other team's best stone in the house
    opp_house = opp[house[opp]]
    if len(opp_house):
        t = opp_house[np.argmin(d[opp_house])]
        dy, dx = y - y[t], np.abs(x - x[t])
        cand = np.flatnonzero((dy > STONE_DIAMETER) & (dy <= RUNBACK_MAX_DIST) & hit)
        if len(cand):
            ang = np.degrees(np.arctan2(dx[cand], dy[cand]))
            k = int(np.argmin(ang))
            if ang[k] <= RUNBACK_MAX_ANGLE:
                f = cand[k]
                keep = np.ones(len(x), dtype=bool)
                keep[t] = False
                out.update(rb_on=1.0, rb_straight=float(ang[k] < RUNBACK_STRAIGHT), rb_angle=float(ang[k]),
                           rb_dist=float(dy[f]), rb_front_own=float(owner[f] == thrower),
                           rb_swing=float(signed_count(x[keep], y[keep], owner[keep], thrower) - now))
    return out
