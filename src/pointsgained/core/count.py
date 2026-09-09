"""The count function: exact scoring of a position (design Section 5.3)."""
from __future__ import annotations

from typing import Iterable

from .geometry import RING_12_RADIUS, STONE_RADIUS, distance_to_pin


def count_position(stones: Iterable[tuple[str, float, float]],
                   stone_radius: float = STONE_RADIUS) -> tuple[str | None, int]:
    """Score a position.

    stones: iterable of (color, x_in, y_in).
    Returns (scoring_color, points). Empty house -> (None, 0).
    """
    in_house = [(distance_to_pin(x, y), c) for c, x, y in stones
                if distance_to_pin(x, y) <= RING_12_RADIUS + stone_radius]
    if not in_house:
        return None, 0
    in_house.sort()
    winner = in_house[0][1]
    points = 0
    for _, c in in_house:
        if c != winner:
            break
        points += 1
    return winner, points
