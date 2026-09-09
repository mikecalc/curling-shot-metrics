import numpy as np
from pointsgained.core.positions import Position, fgz_rocks_for
from datetime import date


def test_empty_position_parity():
    p = Position.empty()
    assert p.rocks_remaining == 16 and not p.next_thrower_has_hammer   # non-hammer throws first
    p.rocks_remaining = 1
    assert p.next_thrower_has_hammer                                  # hammer throws last


def test_score_hammer_sign():
    p = Position(np.array([0.0, 30.0]), np.array([0.0, 0.0]), np.array([1, 0]), 0)
    assert p.score_hammer() == 1
    p2 = Position(np.array([0.0, 30.0]), np.array([0.0, 0.0]), np.array([0, 1]), 0)
    assert p2.score_hammer() == -1


def test_mirror():
    p = Position(np.array([10.0]), np.array([5.0]), np.array([1]), 3)
    m = p.mirrored()
    assert m.x[0] == -10.0 and m.y[0] == 5.0


def test_fgz_era():
    assert fgz_rocks_for(date(2018, 3, 1)) == 4
    assert fgz_rocks_for(date(2018, 11, 1)) == 5
    assert fgz_rocks_for(date(2026, 4, 1)) == 5
