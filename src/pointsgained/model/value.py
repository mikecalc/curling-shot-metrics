"""Value mappings V over end-outcome distributions (design Section 9).

Outcomes are end scores from the hammer team's perspective, clipped to [-3, +3].
A distribution is a length-7 vector over OUTCOMES. Every mapping exposes
v(outcome) so that V(D) = sum_k D[k] * v[k]; Points Gained are differences of V.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

OUTCOMES = np.array([-3, -2, -1, 0, 1, 2, 3])
N_OUT = len(OUTCOMES)
IDX = {o: i for i, o in enumerate(OUTCOMES)}


def clip_outcome(points: int) -> int:
    return int(max(-3, min(3, points)))


def hammer_net(dist: np.ndarray) -> float:
    """N: expected net score of the hammer team in one end."""
    return float(np.dot(dist, OUTCOMES))


def markov_hammer_value(dist: np.ndarray) -> float:
    """H: infinite-horizon value of holding hammer under a stationary end-outcome distribution.

    H = N + (P(blank) + P(steal) - P(score)) * H  =>  H = N / (1 - P(blank) - P(steal) + P(score)).
    """
    n = hammer_net(dist)
    p_blank = float(dist[IDX[0]])
    p_steal = float(dist[OUTCOMES < 0].sum())
    p_score = float(dist[OUTCOMES > 0].sum())
    denom = 1.0 - p_blank - p_steal + p_score
    return n / denom if denom > 1e-9 else n


class ValueMapping:
    """v(outcome) in the hammer team's perspective. Subclasses set self.v (length 7)."""
    name = "base"

    def __init__(self):
        self.v = np.zeros(N_OUT)

    def V(self, dist: np.ndarray) -> float:
        return float(np.dot(np.asarray(dist, dtype=float), self.v))

    def value_of_outcome(self, points_hammer: int) -> float:
        return float(self.v[IDX[clip_outcome(points_hammer)]])


class HammerAdjustedPoints(ValueMapping):
    """Section 9.2: v = points + h * hammer_after, where hammer_after = +1 if the hammer team
    keeps hammer (blank or steal) and -1 if it scores. h is N (one-end lookahead) or H (Markov)."""
    name = "hammer_adjusted_points"

    def __init__(self, hammer_value: float):
        super().__init__()
        self.h = hammer_value
        for i, o in enumerate(OUTCOMES):
            keep = 1.0 if o <= 0 else -1.0
            self.v[i] = o + self.h * keep


class ExpectedPoints(ValueMapping):
    """Naive: blank = 0. Kept only as a reference."""
    name = "expected_points"

    def __init__(self):
        super().__init__()
        self.v = OUTCOMES.astype(float)


@dataclass
class ValueSet:
    """Value mappings estimated for one stratum (tier, gender, era)."""
    dist: np.ndarray
    N: float
    H: float

    @classmethod
    def from_outcomes(cls, outcomes_hammer) -> "ValueSet":
        arr = np.asarray([clip_outcome(o) for o in outcomes_hammer])
        dist = np.array([(arr == o).mean() for o in OUTCOMES])
        return cls(dist=dist, N=hammer_net(dist), H=markov_hammer_value(dist))

    def mapping(self, kind: str = "H") -> ValueMapping:
        return HammerAdjustedPoints(self.H if kind == "H" else self.N)
