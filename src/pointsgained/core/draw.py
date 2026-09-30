"""The draw to beat: can the next thrower draw inside the other team's best stone, and how easily?

"Draw against n": the other team lies n, and a draw that finishes closer to the pin than its best stone
turns that into a count for the thrower. Whether it is on is a relation between a few stones, not a
property of any one of them (Mike Calcagno, 2026-09-29):

- **Paths.** The final draw curls in on an in-turn or an out-turn, from one side or the other. Any stone
  along that curved path blocks it: stones on the wing on the side it curls in from, and stones tighter
  to the 4-foot lane the nearer it gets to the house. A straight-line centre guard does not block it.
  Often one side is closed and the other open.
- **Backing.** The draw is close to a sure thing (high 90s) with backing: the stone to beat is behind the
  tee, so a draw onto it outcounts it, or another stone will stop the draw from going too far.

The path is the curve of a stone that decelerates uniformly while curling with a constant sideways
acceleration: with u the distance still to travel and U the length of the curl, the stone is
D (2r - r^2) to the side of where it finishes, r = sqrt(u / U), so the final approach comes in at an
angle and the path is widest far up the sheet. D (CURL_IN) and U (CURL_LENGTH beyond the hog line) are
round numbers for a draw, not fitted. A stone blocks a path when its centre is within a stone's
diameter of the path where the path passes it. Canonical frame (inches, pin at 0, y towards the hog
line); every test is mirror-symmetric.
"""
from __future__ import annotations

import numpy as np

from .geometry import HOG_LINE_Y, RING_12_RADIUS, RING_4_RADIUS, STONE_DIAMETER, STONE_RADIUS

CURL_IN = 48.0                 # sideways travel of a draw over its curl (about four feet)
CURL_BEYOND_HOG = 120.0        # the curl starts about ten feet before the hog line
TARGET_RADII = (0.0, 6.0, 12.0, 18.0, 24.0)
TARGET_ANGLES = np.radians(np.arange(0, 360, 45))
BEAT_MARGIN = 1.0              # a draw must finish at least an inch inside the stone to beat
BACKING_DEPTH = 2 * STONE_DIAMETER   # a stone this close behind the target stops a heavy draw
NO_STONE_DIST = RING_12_RADIUS + STONE_RADIUS + 6.0   # "distance" of the stone to beat when there is none

OPEN_SIDE_SHARE = 0.5          # a side is open when at least half the finishing points can be reached from it

DRAW_FEATURES = ["draw_beat_dist", "draw_against", "draw_gain", "draw_open_sides", "draw_open_best", "draw_open_worst",
                 "draw_backed"]


def path_offset(u: np.ndarray, U: np.ndarray, curl: float = CURL_IN) -> np.ndarray:
    """How far to the side of its finishing point a draw is with u inches still to travel."""
    r = np.sqrt(np.clip(u / U, 0.0, 1.0))
    return curl * (2 * r - r * r)


def targets(x: np.ndarray, y: np.ndarray, limit: float) -> np.ndarray:
    """Candidate finishing points within `limit` of the pin (at most the 4-foot): a small grid plus a freeze
    onto the front of every stone in the house, keeping the points no stone already occupies."""
    pts = [(0.0, 0.0)] + [(r * np.cos(a), r * np.sin(a)) for r in TARGET_RADII[1:] for a in TARGET_ANGLES]
    pts += [(sx, sy + STONE_DIAMETER + 0.2) for sx, sy in zip(x, y) if np.hypot(sx, sy) <= RING_12_RADIUS + STONE_RADIUS]
    P = np.array(pts, dtype=float)
    P = P[np.hypot(P[:, 0], P[:, 1]) <= min(limit, RING_4_RADIUS + STONE_RADIUS)]
    if len(x) and len(P):
        d = np.hypot(P[:, None, 0] - x[None, :], P[:, None, 1] - y[None, :])
        P = P[(d >= STONE_DIAMETER).all(axis=1)]
    return P


def open_sides(P: np.ndarray, x: np.ndarray, y: np.ndarray, curl: float = CURL_IN) -> np.ndarray:
    """(targets, 2) booleans: the path from the left (-x) and from the right (+x) to each target is clear
    (`curl`: the sideways travel of the stone over its curl; a tap curls a little less than a draw)."""
    out = np.ones((len(P), 2), dtype=bool)
    if not len(x) or not len(P):
        return out
    u = y[None, :] - P[:, None, 1]                               # distance up the sheet from target to stone
    ahead = u > STONE_RADIUS
    U = (HOG_LINE_Y - P[:, 1] + CURL_BEYOND_HOG)[:, None]
    off = path_offset(u, U, curl)
    for k, side in enumerate((-1.0, 1.0)):
        px = P[:, None, 0] + side * off                          # where the path is at each stone's depth
        out[:, k] = ~(ahead & (np.abs(x[None, :] - px) < STONE_DIAMETER)).any(axis=1)
    return out


def backed(P: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Targets with a stone just behind them, in line: a heavy draw stops there."""
    if not len(x) or not len(P):
        return np.zeros(len(P), dtype=bool)
    dy = P[:, None, 1] - y[None, :]
    return ((dy > STONE_RADIUS) & (dy <= BACKING_DEPTH) & (np.abs(P[:, None, 0] - x[None, :]) <= STONE_DIAMETER)).any(axis=1)


def draw_to_beat(x: np.ndarray, y: np.ndarray, owner: np.ndarray, thrower: int) -> dict[str, float]:
    """The draw to beat for `thrower` (1 hammer, 0 non-hammer):
    draw_beat_dist   distance from the pin of the other team's best stone in the house (the one to beat)
    draw_against     how many the other team lies now (the n of "draw against n"; 0 if the thrower is shot)
    draw_gain        what a made draw leaves the thrower lying (its stones inside the stone to beat, plus one)
    draw_open_sides  0, 1 or 2: sides from which at least half the finishing points inside the stone to beat
                     (and in the 4-foot) can be reached
    draw_open_best   the share of finishing points reachable from the more open side
    draw_open_worst  the same from the more closed side
    draw_backed      1 if a reachable finishing point has backing"""
    x, y, owner = np.asarray(x, float), np.asarray(y, float), np.asarray(owner, int)
    d = np.hypot(x, y)
    house = d <= RING_12_RADIUS + STONE_RADIUS
    opp = house & (owner != thrower)
    own = house & (owner == thrower)
    beat = float(d[opp].min()) if opp.any() else NO_STONE_DIST
    against = 0
    if house.any():
        order = np.argsort(d[house])
        o = owner[house][order]
        if o[0] != thrower:
            against = int(np.argmax(o == thrower)) if (o == thrower).any() else len(o)
    gain = int((own & (d < beat)).sum()) + 1
    P = targets(x, y, beat - BEAT_MARGIN)
    if not len(P):
        return {"draw_beat_dist": beat, "draw_against": float(against), "draw_gain": float(gain),
                "draw_open_sides": 0.0, "draw_open_best": 0.0, "draw_open_worst": 0.0, "draw_backed": 0.0}
    sides = open_sides(P, x, y)
    share = sides.mean(axis=0)
    return {"draw_beat_dist": beat, "draw_against": float(against), "draw_gain": float(gain),
            "draw_open_sides": float((share >= OPEN_SIDE_SHARE).sum()),
            "draw_open_best": float(share.max()), "draw_open_worst": float(share.min()),
            "draw_backed": float((sides.any(axis=1) & backed(P, x, y)).any())}
