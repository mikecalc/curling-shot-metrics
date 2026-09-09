"""Win-probability table from line scores (design Section 9.4).

Built by backward induction over an end-outcome distribution estimated from the
Game Results line scores of every book. The outcome distribution is conditioned on
(score_diff, ends_remaining) where data allow, shrunk towards the pooled
distribution with a pseudo-count prior.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .value import OUTCOMES, IDX, N_OUT, ValueMapping, clip_outcome

MAX_DIFF = 6


def ends_from_line_scores(line_scores: pd.DataFrame) -> pd.DataFrame:
    """One row per played end: game_key, end, ends_total, hammer_side ('a'/'b'), score_a, score_b,
    diff_before_hammer (hammer team minus other, before the end), outcome_hammer.
    """
    rows = []
    for gk, grp in line_scores.groupby("game_key"):
        if len(grp) != 2:
            continue
        a, b = grp.iloc[0], grp.iloc[1]
        n_ends = int(a["n_ends"])
        ends_a, ends_b = list(a["ends"]) + list(a["extra"]), list(b["ends"]) + list(b["extra"])
        if a["lsfe"] == b["lsfe"]:
            continue
        hammer = "a" if a["lsfe"] else "b"
        tot_a = tot_b = 0
        for e, (sa, sb) in enumerate(zip(ends_a, ends_b), start=1):
            if sa == "X" or sb == "X" or sa == "" or sb == "":
                break
            try:
                sa, sb = int(sa), int(sb)
            except ValueError:
                break
            h_score = sa if hammer == "a" else sb
            n_score = sb if hammer == "a" else sa
            diff = (tot_a - tot_b) if hammer == "a" else (tot_b - tot_a)
            rows.append({"game_key": gk, "end": e, "n_ends": n_ends, "ends_remaining": n_ends - e + 1,
                         "hammer_side": hammer, "diff_hammer": diff, "outcome_hammer": h_score - n_score,
                         "is_extra": e > n_ends, "team_hammer": a["team"] if hammer == "a" else b["team"],
                         "discipline": a.get("discipline")})
            tot_a += sa; tot_b += sb
            if h_score > 0:
                hammer = "b" if hammer == "a" else "a"
            # blank or steal: hammer team keeps hammer
    return pd.DataFrame(rows)


@dataclass
class WinProbTable:
    """WP[d, n, h]: probability the team with score difference d (own minus opponent), n ends
    remaining (including the current one), and hammer flag h (1 = has hammer) wins."""
    wp: np.ndarray                      # shape (2*MAX_DIFF+1, n_max+1, 2)
    pooled: np.ndarray                  # pooled hammer outcome distribution
    cond: dict = field(default_factory=dict)   # (d, n) -> smoothed outcome distribution
    n_max: int = 10
    prior_weight: float = 30.0

    def P(self, d: int, n: int, h: int) -> float:
        d = max(-MAX_DIFF, min(MAX_DIFF, d))
        n = min(n, self.n_max)
        return float(self.wp[d + MAX_DIFF, n, h])

    def outcome_dist(self, d: int, n: int) -> np.ndarray:
        return self.cond.get((max(-MAX_DIFF, min(MAX_DIFF, d)), min(n, self.n_max)), self.pooled)

    def v_vector(self, d: int, n: int) -> np.ndarray:
        """v(outcome) for the hammer team in situation (d, n): win probability after the end."""
        v = np.zeros(N_OUT)
        for i, o in enumerate(OUTCOMES):
            keeps = o <= 0
            v[i] = self._after(d + int(o), n - 1, 1 if keeps else 0)
        return v

    def _after(self, d: int, n: int, h: int) -> float:
        if n <= 0:
            if d > 0:
                return 1.0
            if d < 0:
                return 0.0
            return self.extra_end_wp(h)
        return self.P(d, n, h)

    def extra_end_wp(self, h: int) -> float:
        p = self.pooled
        p_score = float(p[OUTCOMES > 0].sum())
        p_blank = float(p[IDX[0]])
        wp_h = p_score / max(1e-9, 1.0 - p_blank)
        return wp_h if h == 1 else 1.0 - wp_h

    def regime(self, d: int, n: int) -> str:
        """Named strategic regime implied by the shape of v (hammer team's view)."""
        v = self.v_vector(d, n)
        vb, v1, v2, vm1 = v[IDX[0]], v[IDX[1]], v[IDX[2]], v[IDX[-1]]
        if n == 1:
            if d == 0:
                return "must score (tied, last end)"
            if d > 0:
                return "protect lead"
            return f"need {-d + 1}+ to win"
        if v2 - v1 < 0.02 and v1 - vb > 0.05:
            return "score one is enough"
        if vb >= v1:
            return "two or blank"
        return "take what is there"


class WinProbability(ValueMapping):
    """Value mapping in win-probability units for one game situation (hammer team's view)."""
    name = "win_probability"

    def __init__(self, table: WinProbTable, diff_hammer: int, ends_remaining: int):
        super().__init__()
        self.v = table.v_vector(diff_hammer, ends_remaining)


def build_table(end_rows: pd.DataFrame, n_max: int = 10, prior_weight: float = 30.0) -> WinProbTable:
    """Backward induction with a (diff, ends_remaining)-conditional outcome distribution."""
    oc = end_rows["outcome_hammer"].map(clip_outcome).to_numpy()
    pooled = np.array([(oc == o).mean() for o in OUTCOMES])
    cond = {}
    key = list(zip(end_rows["diff_hammer"].clip(-MAX_DIFF, MAX_DIFF), end_rows["ends_remaining"].clip(upper=n_max)))
    df = pd.DataFrame({"k": key, "o": oc})
    for k, grp in df.groupby("k"):
        counts = np.array([(grp["o"] == o).sum() for o in OUTCOMES], dtype=float)
        cond[k] = (counts + prior_weight * pooled) / (counts.sum() + prior_weight)
    wp = np.zeros((2 * MAX_DIFF + 1, n_max + 1, 2))
    t = WinProbTable(wp=wp, pooled=pooled, cond=cond, n_max=n_max, prior_weight=prior_weight)
    # n = 0 handled by _after; fill n = 1..n_max
    for n in range(1, n_max + 1):
        for d in range(-MAX_DIFF, MAX_DIFF + 1):
            dist = t.outcome_dist(d, n)
            # with hammer
            val = 0.0
            for i, o in enumerate(OUTCOMES):
                val += dist[i] * t._after(d + int(o), n - 1, 1 if o <= 0 else 0)
            wp[d + MAX_DIFF, n, 1] = val
        for d in range(-MAX_DIFF, MAX_DIFF + 1):
            # without hammer: the opponent has hammer with difference -d
            dist = t.outcome_dist(-d, n)
            val = 0.0
            for i, o in enumerate(OUTCOMES):
                # opponent outcome o: our diff becomes d - o; we get hammer iff they score
                val += dist[i] * t._after(d - int(o), n - 1, 0 if o <= 0 else 1)
            wp[d + MAX_DIFF, n, 0] = val
    return t
