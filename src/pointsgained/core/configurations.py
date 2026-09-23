"""Configurations: the position as a skip reads it.

A skip does not see sixteen independent stones; they see "the deuce is loose", "the steal is on",
"a split house", "two guards up". Each label here is a deterministic test on a canonical position
(hammer team = own, owner 1), multi-label, so a position can be a split house with a centre guard up.
The question behind most of them is what the position leaves the opponent: can they find the shot
that wrecks it? Vocabulary and thresholds from Mike (2026-09-23); the split thresholds are checked
against how often the field's hits actually removed both stones of a pair (reports/front_end.md).

Besides the labels, continuous measures (`MEASURES`): the double on each team's two best stones
in the house (separation, and stagger as the angle of the line between them from level; 0 = side by
side at the same depth, the flat and nearly impossible double), and the runback on the shot rock:
any stone in front of it, either team's, can be driven into it. Straight runbacks (the stone in
front nearly on the line) are the ones skips like, the thrown stone staying as a new guard; angled
ones are harder. What is at stake is `swing_if_shot_removed`, the count change (hammer team's view)
if the shot rock goes: a lonely steal stone in front of the hammer team's two, three and four is a
swing of three to five.
"""
from __future__ import annotations

import numpy as np

from .geometry import RING_12_RADIUS, RING_4_RADIUS, STONE_DIAMETER, STONE_RADIUS
from .positions import Position

CENTER_LANE = 24.0           # |x| <= 24 in is the centre lane (as in the baseline features)
SPLIT_MIN_SEPARATION = 36.0  # a split: every pair of the hammer team's house stones at least 3 ft apart
FLAT_MIN_SEPARATION = 48.0   # a flat split: 4 ft or more apart ...
FLAT_MAX_ANGLE = 15.0        # ... and within 15 degrees of level: the field doubles it off about 2% of the time
DEUCE_LOOSE_MAX_ROCKS = 8    # from stone 9 on: the hammer team's first four stones have been thrown
BUSY_HOUSE = 4               # stones in the house for a busy house
RUNBACK_MAX_DIST = 180.0     # a stone up to 15 ft in front of the shot rock can be run back into it
RUNBACK_STRAIGHT = 10.0      # degrees off the line of delivery: a straight runback
RUNBACK_MAX_ANGLE = 35.0     # beyond this the angle runback is not a practical shot

LABELS = [
    "empty",                # no stones in play
    "guards_only",          # stones in play, none in the house
    "own_centre_guard",     # hammer team has a guard in the centre lane
    "opp_centre_guard",     # non-hammer team has a guard in the centre lane
    "own_corner_guard",     # hammer team has a guard outside the centre lane
    "opp_corner_guard",     # non-hammer team has a guard outside the centre lane
    "open_house",           # no guards at all
    "own_shot",             # hammer team lies shot
    "opp_shot",             # non-hammer team lies shot
    "own_two_plus",         # hammer team lies two or more
    "opp_two_plus",         # non-hammer team lies two or more
    "split_house",          # hammer team has two or more in the house, every pair 3 ft+ apart, and the opponent none
    "split_flat",           # a split whose pairs are 4 ft+ apart and within 15 degrees of level: the double is nearly off
    "split_staggered",      # a split that is not flat: staggered in depth (the walked split), the double is on
    "own_shot_covered",     # hammer team's shot rock has a stone in front of it
    "deuce_loose",          # from stone 9: a flat split, or a covered hammer stone that will count second with the centre open
    "steal_setup",          # non-hammer team has two or more centre guards
    "steal_on",             # non-hammer team lies shot and it is covered
    "opp_exposed",          # non-hammer team has a stone in the house with nothing in front of it
    "open_shot_own",        # hammer team lies shot and there are no guards: only a freeze gets the opponent shot and hidden
    "open_shot_opp",        # non-hammer team lies shot and there are no guards
    "shot_runback_straight",  # a stone in front of the shot rock, within 10 degrees of its line: a straight runback
    "shot_runback_angled",    # the best runback on the shot rock is at 10-35 degrees
    "lonely_steal",         # non-hammer team lies one, and the hammer team counts two or more without it
    "lonely_steal_exposed", # a lonely steal stone with a runback on it: guarding it risks the big end
    "busy_house",           # four or more stones in the house
    "near_tie",             # the count is not knowable from the sheet (boundary gap under 2 in)
]
PAIR_FEATURES = ["own_pair_sep", "own_pair_angle", "opp_pair_sep", "opp_pair_angle"]
RUNBACK_FEATURES = ["shot_runback_angle", "shot_runback_dist", "swing_if_shot_removed"]
MEASURES = PAIR_FEATURES + RUNBACK_FEATURES
NO_RUNBACK_ANGLE = 90.0
NO_RUNBACK_DIST = 300.0


def _covered(x: float, y: float, xs: np.ndarray, ys: np.ndarray) -> bool:
    """A stone in front (larger y) within one stone diameter laterally: the straight-line cover test."""
    front = ys > y + STONE_RADIUS
    return bool(np.any(front & (np.abs(xs - x) <= STONE_DIAMETER)))


def _pair(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """(separation, angle from level in degrees) of two stones."""
    dx, dy = abs(x[0] - x[1]), abs(y[0] - y[1])
    return float(np.hypot(dx, dy)), float(np.degrees(np.arctan2(dy, dx)))


def pair_measures(p: Position) -> dict[str, float]:
    """Separation and stagger of each team's two stones closest to the pin in the house (0 if fewer than two)."""
    out = dict.fromkeys(PAIR_FEATURES, 0.0)
    if p.n < 2:
        return out
    d = np.hypot(p.x, p.y)
    in_house = d <= RING_12_RADIUS + STONE_RADIUS
    for who, mask in (("own", p.owner == 1), ("opp", p.owner != 1)):
        idx = np.flatnonzero(in_house & mask)
        if len(idx) >= 2:
            top = idx[np.argsort(d[idx])[:2]]
            out[f"{who}_pair_sep"], out[f"{who}_pair_angle"] = _pair(p.x[top], p.y[top])
    return out


def _count(own: np.ndarray, d: np.ndarray, in_house: np.ndarray) -> int:
    """Signed count (hammer team's view) of the stones in the house."""
    ih = [i for i in np.argsort(d) if in_house[i]]
    if not ih:
        return 0
    first = bool(own[ih[0]])
    n = 0
    for i in ih:
        if bool(own[i]) != first:
            break
        n += 1
    return n if first else -n


def runback(p: Position) -> dict[str, float]:
    """The best runback on the shot rock (smallest angle off the line of delivery, among stones of either team
    in front of it within RUNBACK_MAX_DIST), and the count swing if the shot rock were removed."""
    out = {"shot_runback_angle": NO_RUNBACK_ANGLE, "shot_runback_dist": NO_RUNBACK_DIST, "swing_if_shot_removed": 0.0}
    if p.n == 0:
        return out
    x, y, own = p.x, p.y, p.owner == 1
    d = np.hypot(x, y)
    in_house = d <= RING_12_RADIUS + STONE_RADIUS
    if not in_house.any():
        return out
    s = min(np.flatnonzero(in_house), key=lambda i: d[i])
    dy, dx = y - y[s], np.abs(x - x[s])
    cand = (dy > STONE_DIAMETER) & (dy <= RUNBACK_MAX_DIST)
    if cand.any():
        ang = np.degrees(np.arctan2(dx[cand], dy[cand]))
        b = int(np.argmin(ang))
        if ang[b] <= RUNBACK_MAX_ANGLE:
            out["shot_runback_angle"], out["shot_runback_dist"] = float(ang[b]), float(dy[cand][b])
    keep = np.ones(p.n, dtype=bool)
    keep[s] = False
    out["swing_if_shot_removed"] = float(_count(own[keep], d[keep], in_house[keep]) - _count(own, d, in_house))
    return out


def measures(p: Position) -> dict[str, float]:
    return {**pair_measures(p), **runback(p)}


def configuration(p: Position) -> dict[str, bool]:
    """The configuration labels of one canonical position."""
    lab = dict.fromkeys(LABELS, False)
    if p.n == 0:
        lab["empty"] = lab["open_house"] = True
        return lab
    x, y, own = p.x, p.y, p.owner == 1
    d = np.hypot(x, y)
    in_house = d <= RING_12_RADIUS + STONE_RADIUS
    guard = (~in_house) & (y > 0)
    centre = np.abs(x) <= CENTER_LANE
    lab["guards_only"] = not in_house.any()
    lab["own_centre_guard"] = bool(np.any(guard & centre & own))
    lab["opp_centre_guard"] = bool(np.any(guard & centre & ~own))
    lab["own_corner_guard"] = bool(np.any(guard & ~centre & own))
    lab["opp_corner_guard"] = bool(np.any(guard & ~centre & ~own))
    lab["open_house"] = not guard.any()
    lab["busy_house"] = int(in_house.sum()) >= BUSY_HOUSE
    lab["steal_setup"] = int(np.sum(guard & centre & ~own)) >= 2
    lab["opp_exposed"] = any(not _covered(x[i], y[i], x, y) for i in np.flatnonzero(in_house & ~own))
    if not in_house.any():
        return lab

    ih = [i for i in np.argsort(d) if in_house[i]]
    first = ih[0]
    shooter_own = bool(own[first])
    cnt = 0
    for i in ih:
        if bool(own[i]) != shooter_own:
            break
        cnt += 1
    covered = _covered(x[first], y[first], x, y)
    lab["own_shot"] = shooter_own
    lab["opp_shot"] = not shooter_own
    lab["own_two_plus"] = shooter_own and cnt >= 2
    lab["opp_two_plus"] = (not shooter_own) and cnt >= 2
    lab["own_shot_covered"] = shooter_own and covered
    lab["steal_on"] = (not shooter_own) and covered
    lab["open_shot_own"] = shooter_own and lab["open_house"]
    lab["open_shot_opp"] = (not shooter_own) and lab["open_house"]
    opp_ih = [i for i in ih if bool(own[i]) != shooter_own]
    if opp_ih:
        lab["near_tie"] = bool(d[opp_ih[0]] - d[ih[cnt - 1]] < 2.0)

    rb = runback(p)
    lab["shot_runback_straight"] = rb["shot_runback_angle"] < RUNBACK_STRAIGHT
    lab["shot_runback_angled"] = RUNBACK_STRAIGHT <= rb["shot_runback_angle"] <= RUNBACK_MAX_ANGLE
    lab["lonely_steal"] = (not shooter_own) and cnt == 1 and rb["swing_if_shot_removed"] >= 3   # -1 -> +2 or more
    lab["lonely_steal_exposed"] = lab["lonely_steal"] and rb["shot_runback_angle"] <= RUNBACK_MAX_ANGLE

    own_ih = np.flatnonzero(in_house & own)
    opp_in = np.flatnonzero(in_house & ~own)
    if len(own_ih) >= 2 and len(opp_in) == 0:
        pairs = [_pair(x[[a, b]], y[[a, b]]) for k, a in enumerate(own_ih) for b in own_ih[k + 1:]]
        if min(s for s, _ in pairs) >= SPLIT_MIN_SEPARATION:
            lab["split_house"] = True
            lab["split_flat"] = all(s >= FLAT_MIN_SEPARATION and a < FLAT_MAX_ANGLE for s, a in pairs)
            lab["split_staggered"] = not lab["split_flat"]

    if p.rocks_remaining <= DEUCE_LOOSE_MAX_ROCKS:
        # a hammer stone behind cover that will count second: no opponent stone closer to the pin,
        # with the centre open for the first point (no centre guard, no opponent stone in the 4-foot)
        opp_nearest = d[opp_in].min() if len(opp_in) else np.inf
        centre_open = not np.any(guard & centre) and not np.any(in_house & ~own & (d <= RING_4_RADIUS + STONE_RADIUS))
        covered_counter = any(d[i] < opp_nearest and _covered(x[i], y[i], x, y) for i in own_ih)
        lab["deuce_loose"] = lab["split_flat"] or (covered_counter and centre_open)
    return lab


def label_matrix(positions) -> np.ndarray:
    """Boolean matrix (n_positions, len(LABELS)) for an iterable of Positions."""
    return np.array([[configuration(p)[k] for k in LABELS] for p in positions], dtype=bool).reshape(-1, len(LABELS))
