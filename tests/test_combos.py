import numpy as np
from pointsgained.core.combos import combos, signed_count


def C(stones, thrower=1):
    """stones: list of (x, y, owner) with owner 1 = hammer team."""
    a = np.array(stones, dtype=float).reshape(-1, 3)
    return combos(a[:, 0], a[:, 1], a[:, 2].astype(int), thrower)


def test_empty_and_single():
    assert C([])["dbl_on"] == 0 and C([(0, 0, 0)])["rb_on"] == 0


def test_staggered_pair_is_a_double():
    f = C([(-20, 20, 0), (25, -15, 0)])
    assert f["dbl_on"] == 1 and f["dbl_house"] == 1 and f["dbl_swing"] == 2 and f["dbl_angle"] > 15


def test_flat_pair_far_apart_is_not():
    assert C([(-40, 5, 0), (40, 0, 0)])["dbl_on"] == 0


def test_covered_first_stone_blocks_the_double():
    # the front stone of the pair has a guard straight in front of it; the back stone is not reachable first
    assert C([(-20, 20, 0), (25, -15, 0), (-20, 120, 1)])["dbl_on"] == 0


def test_own_stones_are_not_doubled():
    assert C([(-20, 20, 1), (25, -15, 1)])["dbl_on"] == 0


def test_straight_runback_on_the_other_teams_shot_rock():
    # the other team lies two; a hammer guard straight in front of its shot rock
    f = C([(0, 5, 0), (30, -20, 0), (2, 90, 1)])
    assert f["rb_on"] == 1 and f["rb_straight"] == 1 and f["rb_front_own"] == 1 and f["rb_swing"] == 1


def test_no_runback_off_the_line():
    assert C([(0, 5, 0), (80, 90, 1)])["rb_on"] == 0


def test_signed_count_from_the_thrower():
    x, y, o = np.array([0.0, 10.0, 40.0]), np.array([0.0, 10.0, 0.0]), np.array([0, 0, 1])
    assert signed_count(x, y, o, 1) == -2 and signed_count(x, y, o, 0) == 2


def test_mirror_symmetric():
    s = [(-20, 20, 0), (25, -15, 0), (5, 100, 1), (30, 40, 1)]
    assert C(s) == C([(-x, y, o) for x, y, o in s])
