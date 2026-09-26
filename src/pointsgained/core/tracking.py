"""Stone tracking: follow each stone through the diagrams of an end.

A results-book diagram shows the position after each shot, with the delivered stone marked and hollow
rings where moved stones were before the shot. Stones have no identity on the page; this module gives
them one, shot by shot:

- **unmoved**: a stone of the same team within `UNMOVED_TOL` of a stone in the previous diagram keeps
  that stone's identity (the diagrams place an unmoved stone at the same pixel);
- **thrown**: the delivered stone, when the diagram marks it, is new;
- **moved**: the remaining stones are matched to the previous diagram's unmatched stones of the same
  team by least total distance, preferring stones whose old position carries a prior-position ring;
- anything left over in the new diagram is **new** (origin unknown), and anything left over in the old
  one was **removed**. When the diagram marks no delivered stone and exactly one new stone is the
  thrower's colour (non-hammer on odd stones, hammer on even), that stone is **thrown** too: many
  templates and the first diagram of an end carry no mark. `marked` in the records says which.

The result is a stone's life through the end: where it was after every shot, and whether it counted
when the end was over. `count_ids` gives the counting stones of a final position.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import linear_sum_assignment

from .geometry import RING_12_RADIUS, STONE_RADIUS

UNMOVED_TOL = 1.0        # inches: an unmoved stone is redrawn at the same place
PRIOR_TOL = 3.0          # inches: a prior-position ring marks a stone that moved from there
PRIOR_BONUS = 60.0       # inches of distance forgiven when a previous stone's old place carries a ring


@dataclass
class Frame:
    """One diagram: stones after a shot (x, y in inches; owner 1 = hammer team; delivered flag) and the
    prior-position rings drawn on it."""
    shot: int
    x: np.ndarray
    y: np.ndarray
    owner: np.ndarray
    delivered: np.ndarray
    prior_x: np.ndarray
    prior_y: np.ndarray


def _greedy_unmoved(px, py, po, cx, cy, co) -> list[tuple[int, int]]:
    """One-to-one pairs (prev, cur) of same-team stones within UNMOVED_TOL, closest first."""
    if len(px) == 0 or len(cx) == 0:
        return []
    d = np.hypot(px[:, None] - cx[None, :], py[:, None] - cy[None, :])
    d[po[:, None] != co[None, :]] = np.inf
    pairs, used_p, used_c = [], set(), set()
    for flat in np.argsort(d, axis=None):
        i, j = divmod(int(flat), d.shape[1])
        if d[i, j] > UNMOVED_TOL:
            break
        if i in used_p or j in used_c:
            continue
        pairs.append((i, j)); used_p.add(i); used_c.add(j)
    return pairs


def match(prev: Frame, cur: Frame) -> tuple[dict[int, int], dict[int, str]]:
    """Map each stone of `cur` to a stone of `prev` (cur index -> prev index) and give each cur stone a
    status: 'unmoved', 'moved', 'thrown' or 'new'."""
    link, status = {}, {}
    for i, j in _greedy_unmoved(prev.x, prev.y, prev.owner, cur.x, cur.y, cur.owner):
        link[j] = i
        status[j] = "unmoved"
    free_c = [j for j in range(len(cur.x)) if j not in link]
    thrown = [j for j in free_c if cur.delivered[j]]
    for j in thrown[:1]:
        status[j] = "thrown"
    free_c = [j for j in free_c if j not in status]
    free_p = [i for i in range(len(prev.x)) if i not in link.values()]
    if free_c and free_p:
        has_ring = np.zeros(len(free_p), dtype=bool)
        if len(cur.prior_x):
            fx, fy = prev.x[free_p], prev.y[free_p]
            dr = np.hypot(fx[:, None] - cur.prior_x[None, :], fy[:, None] - cur.prior_y[None, :])
            has_ring = (dr <= PRIOR_TOL).any(axis=1)
        d = np.hypot(prev.x[free_p][:, None] - cur.x[free_c][None, :], prev.y[free_p][:, None] - cur.y[free_c][None, :])
        d = d - PRIOR_BONUS * has_ring[:, None]
        d[prev.owner[free_p][:, None] != cur.owner[free_c][None, :]] = 1e6
        rows, cols = linear_sum_assignment(d)
        for r, c in zip(rows, cols):
            if d[r, c] < 1e5:
                link[free_c[c]] = free_p[r]
                status[free_c[c]] = "moved"
    for j in range(len(cur.x)):
        status.setdefault(j, "new")
    return link, _infer_thrown(cur, status)


def _infer_thrown(cur: Frame, status: dict[int, str]) -> dict[int, str]:
    """With no delivered stone found, the one new stone of the thrower's colour is the thrown stone."""
    if "thrown" in status.values():
        return status
    thrower = 1 if cur.shot % 2 == 0 else 0
    cand = [j for j, s in status.items() if s == "new" and cur.owner[j] == thrower]
    if len(cand) == 1:
        status[cand[0]] = "thrown"
    return status


def count_ids(x: np.ndarray, y: np.ndarray, owner: np.ndarray) -> tuple[np.ndarray, int]:
    """(indices of the counting stones, index of the shot rock or -1) of a final position."""
    d = np.hypot(x, y)
    ih = np.flatnonzero(d <= RING_12_RADIUS + STONE_RADIUS)
    if not len(ih):
        return np.zeros(0, dtype=int), -1
    ih = ih[np.argsort(d[ih])]
    first = owner[ih[0]]
    counting = []
    for i in ih:
        if owner[i] != first:
            break
        counting.append(i)
    return np.array(counting, dtype=int), int(ih[0])


def track_end(frames: list[Frame]) -> list[dict]:
    """One record per stone per diagram: shot, stone id, owner, x, y, status, the shot it appeared, and
    whether it counted and was shot rock in the end's final diagram (None when the end has no frames)."""
    records, ids, next_id = [], np.zeros(0, dtype=int), 0
    born: dict[int, int] = {}
    prev = None
    for fr in frames:
        n = len(fr.x)
        cur_ids = np.full(n, -1, dtype=int)
        status = _infer_thrown(fr, {j: "new" for j in range(n)})
        if prev is not None and n:
            link, status = match(prev, fr)
            for j, i in link.items():
                cur_ids[j] = ids[i]
        for j in range(n):
            if cur_ids[j] < 0:
                cur_ids[j] = next_id
                born[next_id] = fr.shot
                next_id += 1
        for j in range(n):
            records.append(dict(shot=fr.shot, sid=int(cur_ids[j]), owner=int(fr.owner[j]), x=float(fr.x[j]),
                                y=float(fr.y[j]), status=status[j], marked=bool(fr.delivered[j]),
                                born=born[int(cur_ids[j])]))
        ids, prev = cur_ids, fr
    if prev is None:
        return records
    counting, shot_rock = count_ids(prev.x, prev.y, prev.owner)
    count_sids = set(int(ids[i]) for i in counting)
    shot_sid = int(ids[shot_rock]) if shot_rock >= 0 else -1
    for r in records:
        r["counts_end"] = r["sid"] in count_sids
        r["shot_rock_end"] = r["sid"] == shot_sid
        r["alive_end"] = r["sid"] in set(int(i) for i in ids)
    return records
