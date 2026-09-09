import numpy as np
from pointsgained.core.positions import Position
from pointsgained.model.features import position_features, FEATURE_NAMES


def F(p):
    return dict(zip(FEATURE_NAMES, position_features(p)))


def test_empty():
    f = F(Position.empty())
    assert f["count"] == 0 and f["stones_in_play"] == 0 and f["shot_rock_ring"] == 4


def test_count_and_guards():
    # hammer team shot rock on the button, opp in the 8-foot, own centre guard
    p = Position(np.array([0.0, 40.0, 2.0]), np.array([0.0, 0.0, 120.0]), np.array([1, 0, 1]), 5)
    f = F(p)
    assert f["count"] == 1 and f["shot_rock_ring"] == 0 and f["margin"] == 40.0
    assert f["own_guard_center"] == 1 and f["opp_in_house"] == 1
    assert f["shot_rock_covered"] == 1.0 and f["button_covered"] == 1.0


def test_steal_count_negative():
    p = Position(np.array([0.0, 5.0, 60.0]), np.array([0.0, 10.0, 0.0]), np.array([0, 0, 1]), 2)
    assert F(p)["count"] == -2


def test_near_tie_at_boundary():
    # hammer counts two; the second counting stone and the first opponent stone are 1 inch apart
    p = Position(np.array([0.0, 30.0, 31.0]), np.array([0.0, 0.0, 0.0]), np.array([1, 1, 0]), 4)
    f = F(p)
    assert f["count"] == 2 and abs(f["boundary_gap"] - 1.0) < 1e-9 and f["near_tie"] == 1.0
    q = Position(np.array([0.0, 30.0, 40.0]), np.array([0.0, 0.0, 0.0]), np.array([1, 1, 0]), 4)
    assert F(q)["near_tie"] == 0.0 and abs(F(q)["boundary_gap"] - 10.0) < 1e-9
