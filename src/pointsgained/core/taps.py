"""The tap for the next thrower: move a stone in the house a little and stay (Mike Calcagno, 2026-09-30).

Towards the end of an end a skip considers the tap almost every time. Either the thrower's own stone is
tapped into a better place (a stone controlling the 4-foot raised two feet towards the button, beating
geometry that limits a draw), or the other team's stone is tapped back just far enough that the shooter,
or another of the thrower's stones, outcounts it (a stone at the top of the 4-foot tapped back six feet:
the shooter now sits in front of it, backed by it). A naked tap, raising a centre guard to the button, is
much harder than drawing around it and is rarely played; in the corpus the field makes Raise calls on a
house stone 68-80% of the time and on a stone six to twelve feet in front of the pin 6-36%. So only stones
around the 4-foot are tapped (below), and only taps that leave the tapped stone in play (hit and stick is
not a tap).

Taps are draws (Mike Calcagno, 2026-09-30): finesse shots, expected to curl, a little straighter than a
freeze; the shooter does not have to reach the nose of the stone, only to hit enough of it to move it the
desired amount on the desired angle. So a stone behind cover can be tapped by coming around the guard.
Skips play finesse taps on stones controlling the 4-foot, very rarely on the wings (Mike, 2026-09-30; in the
corpus 89% of Raise calls around the tee line strike a stone within 24 in of the centre line): the 4-foot
plus about two stones, in front of the tee, a cone aimed at the 4-foot; and stones on the button up to a
foot behind the tee (the field taps the other team's there and makes it 78% of the time). Enumeration: every
stone in that zone (centre no more than TAP_BEHIND_TEE behind the tee, within TAP_ZONE of the pin, and within
the 4-foot lane widened by the largest push angle as it goes up the sheet), pushed away from the hog line along TAP_ANGLES off straight back. The
shooter must reach the contact point for that angle (a stone's width from the tapped stone, on the far
side of the push) along a curled in-turn or out-turn path from either side (core/draw.py, with TAP_CURL),
and the contact point must be free. The tapped stone travels TAP_MOVES inches, stopping frozen to the
first stone in its path; the shooter rests where the tapped stone was, just in front of its new place. Each outcome is rescored the way positions are:
the count swing first; among taps that gain a count, the shortest (the tap is played just far enough);
among those that do not, the change in the thrower's shot margin (the other team's best distance less
the thrower's). Straight-line geometry; canonical frame; mirror-symmetric (the angles are symmetric).
"""
from __future__ import annotations

import numpy as np

from .combos import hittable, signed_count
from .draw import CURL_IN, open_sides
from .geometry import RING_4_RADIUS, RING_12_RADIUS, STONE_DIAMETER, STONE_RADIUS
from .traits import CENTER_LANE, TRAITS, jam_share, traits_xy

HOUSE = RING_12_RADIUS + STONE_RADIUS
TAP_ANGLES = np.array([-20.0, -10.0, 0.0, 10.0, 20.0])    # degrees off straight back
TAP_MOVES = np.array([6.0, 12.0, 24.0, 36.0, 48.0, 72.0])  # inches the tapped stone travels
TAP_MIN_MOVE = 3.0          # a stone frozen to the one behind it cannot be tapped along that line
TAP_MIN_GAIN = 6.0          # a tap that changes no count is on when it gains six inches of shot margin
NO_STONE_DIST = HOUSE + 6.0  # as in core/draw.py: the "distance" of a team with no stone in the house
TAP_CURL = 0.8 * CURL_IN     # a tap curls, a little less than a draw
TAP_ZONE = RING_4_RADIUS + 2 * STONE_DIAMETER   # the 4-foot plus about two stones
TAP_BEHIND_TEE = 12.0        # stones on the button up to a foot behind the tee line

TAP_FEATURES = ["tap_on", "tap_own", "tap_swing", "tap_gain", "tap_move", "tap_from", "tap_angle", "tap_backed",
                "tap_covered", "tap_options"]
# trait counts of the position after the best tap (for the trait rescore, model/trait_study.py)
TAP_COUNT_COLUMNS = [f"tp_{t}_{k}" for t in ("h", "n") for k in TRAITS]


def _counts(x: np.ndarray, y: np.ndarray, owner: np.ndarray) -> list[float]:
    m = traits_xy(x, y, owner)
    ham = (owner == 1)[:, None]
    return list((m & ham).sum(axis=0).astype(float)) + list((m & ~ham).sum(axis=0).astype(float))


def _batch_count(d: np.ndarray, o: np.ndarray, thrower: int) -> tuple[np.ndarray, np.ndarray]:
    """Signed count and shot margin for a batch of positions (rows), distances d (inf where no stone)."""
    order = np.argsort(d, axis=1, kind="stable")
    ds, os_ = np.take_along_axis(d, order, 1), np.take_along_axis(o, order, 1)
    inh = ds <= HOUSE
    lead = np.cumprod((os_ == os_[:, :1]) & inh, axis=1).sum(axis=1)
    count = np.where(inh[:, 0], np.where(os_[:, 0] == thrower, lead, -lead), 0)
    house = d <= HOUSE
    own = np.where(house & (o == thrower), d, np.inf).min(axis=1)
    opp = np.where(house & (o != thrower), d, np.inf).min(axis=1)
    margin = np.minimum(opp, NO_STONE_DIST) - np.minimum(own, NO_STONE_DIST)
    return count, margin


def taps(x: np.ndarray, y: np.ndarray, owner: np.ndarray, thrower: int, with_counts: bool = False) -> dict[str, float]:
    """The best tap for `thrower` (1 hammer, 0 non-hammer):
    tap_on       the tap improves the count, or gains at least TAP_MIN_GAIN of shot margin
    tap_own      1 if the tapped stone is the thrower's own, 0 if the other team's
    tap_swing    the count swing (what the thrower lies after, less what it lies now)
    tap_gain     the change in the thrower's shot margin, inches
    tap_move     how far the tapped stone travels, inches
    tap_from     the tapped stone's distance from the pin before the tap
    tap_angle    degrees off straight back
    tap_backed   the jam class of the thrower's shot stone after the tap (0 clear, 1 partly backed, 2 backed)
    tap_covered  1 if the tapped stone is not open in a straight line: the tap comes around cover
    tap_options  the number of stones with a tap that is on
    With `with_counts`, also the trait counts of the position after the best tap (TAP_COUNT_COLUMNS; the
    current position's when there is no tap to play)."""
    x, y, owner = np.asarray(x, float), np.asarray(y, float), np.asarray(owner, int)
    out = {k: 0.0 for k in TAP_FEATURES}
    n = len(x)
    d0 = np.hypot(x, y)
    cone = CENTER_LANE + np.clip(y, 0, None) * np.tan(np.radians(TAP_ANGLES.max()))
    cand = np.flatnonzero((y >= -TAP_BEHIND_TEE) & (d0 <= TAP_ZONE) & (np.abs(x) <= cone))
    best_xyo = (x, y, owner)
    if len(cand):
        now = signed_count(x, y, owner, thrower)
        _, m0 = _batch_count(np.where(d0 <= HOUSE, d0, np.inf)[None, :], owner[None, :], thrower)
        th = np.radians(TAP_ANGLES)
        ux, uy = np.sin(th), -np.cos(th)                                          # (A,) direction of travel
        # the contact point for each push: the shooter's centre a stone's width up the line of the push; it must be
        # free and reachable on a curled path from one side or the other (the tapped stone itself is behind it)
        qx = (x[cand, None] - ux[None, :] * STONE_DIAMETER).ravel()
        qy = (y[cand, None] - uy[None, :] * STONE_DIAMETER).ravel()
        Q = np.column_stack([qx, qy])
        free = (np.hypot(qx[:, None] - x[None, :], qy[:, None] - y[None, :]) >= STONE_DIAMETER - 0.5).all(axis=1)
        reach = (open_sides(Q, x, y, TAP_CURL).any(axis=1) & free).reshape(len(cand), len(TAP_ANGLES))
        straight = hittable(x, y)
        # first stone in each candidate's path along each direction: where the tapped stone stops frozen to it
        rx, ry = x[None, :] - x[cand, None], y[None, :] - y[cand, None]           # (C, n)
        s = rx[:, None, :] * ux[None, :, None] + ry[:, None, :] * uy[None, :, None]           # (C, A, n) along the path
        lat = np.abs(rx[:, None, :] * uy[None, :, None] - ry[:, None, :] * ux[None, :, None])  # distance off the path
        stop = np.where((s > 0) & (lat < STONE_DIAMETER), s - np.sqrt(np.clip(STONE_DIAMETER ** 2 - lat ** 2, 0, None)), np.inf)
        self_mask = np.zeros((len(cand), 1, n), dtype=bool)
        self_mask[np.arange(len(cand)), 0, cand] = True
        stop = np.where(self_mask, np.inf, stop).min(axis=2)                       # (C, A)
        # endpoints: every move short of the stop, and the freeze onto the stopper (once)
        e = np.minimum(TAP_MOVES[None, None, :], stop[:, :, None])                 # (C, A, K)
        first_over = np.cumsum(TAP_MOVES[None, None, :] >= stop[:, :, None], axis=2) == 1
        ok = ((TAP_MOVES[None, None, :] < stop[:, :, None]) | first_over) & (e >= TAP_MIN_MOVE) & reach[:, :, None]
        ci, ai, ki = np.nonzero(ok)
        c, ev = cand[ci], e[ci, ai, ki]
        nx, ny = x[c] + ux[ai] * ev, y[c] + uy[ai] * ev                             # the tapped stone's new place
        back = np.maximum(STONE_DIAMETER - ev, 0.0)
        sx, sy = x[c] - ux[ai] * back, y[c] - uy[ai] * back                         # the shooter, just in front
        keep = np.hypot(nx, ny) <= HOUSE                                             # taps only: it stays in play
        c, ai, ev, nx, ny, sx, sy = c[keep], ai[keep], ev[keep], nx[keep], ny[keep], sx[keep], sy[keep]
        if len(c):
            B = len(c)
            X = np.hstack([np.repeat(x[None, :], B, 0), sx[:, None]])
            Y = np.hstack([np.repeat(y[None, :], B, 0), sy[:, None]])
            X[np.arange(B), c], Y[np.arange(B), c] = nx, ny
            O = np.hstack([np.repeat(owner[None, :], B, 0), np.full((B, 1), thrower)])
            D = np.hypot(X, Y)
            count, margin = _batch_count(np.where(D <= HOUSE, D, np.inf), O, thrower)
            swing, gain = count - now, margin - m0[0]
            on = (swing > 0) | (gain >= TAP_MIN_GAIN)
            # a tap that turns the count: the shortest that does it ("just far enough"); otherwise the most margin
            b = int(np.argmax(swing * 1000.0 + np.where(swing > 0, -ev, gain) - 0.01 * np.abs(TAP_ANGLES[ai])))   # then the straighter
            bx, by, bo = X[b], Y[b], O[b]
            db = np.hypot(bx, by)
            own = np.flatnonzero((db <= HOUSE) & (bo == thrower))
            jam = 0.0
            if len(own):
                share, _ = jam_share(bx, by)
                sh = share[own[np.argmin(db[own])]]
                jam = 2.0 if sh >= 0.5 else (1.0 if sh > 0 else 0.0)
            out.update(tap_on=float(on[b]), tap_own=float(owner[c[b]] == thrower), tap_swing=float(swing[b]),
                       tap_gain=float(gain[b]), tap_move=float(ev[b]), tap_from=float(d0[c[b]]),
                       tap_angle=float(abs(TAP_ANGLES[ai[b]])), tap_backed=jam, tap_covered=float(not straight[c[b]]),
                       tap_options=float(len(set(c[on]))))
            best_xyo = (bx, by, bo)
    if with_counts:
        bx, by, bo = best_xyo
        out.update(zip(TAP_COUNT_COLUMNS, _counts(bx, by, bo) if len(bx) else [0.0] * len(TAP_COUNT_COLUMNS)))
    return out
