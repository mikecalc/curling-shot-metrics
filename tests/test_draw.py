import numpy as np
from pointsgained.core.draw import draw_to_beat, path_offset


def D(stones, thrower=1):
    """stones: list of (x, y, owner) with owner 1 = hammer team."""
    a = np.array(stones, dtype=float).reshape(-1, 3)
    return draw_to_beat(a[:, 0], a[:, 1], a[:, 2].astype(int), thrower)


def test_path_is_widest_far_up():
    U = np.array(372.0)
    assert path_offset(np.array(0.0), U) == 0
    assert path_offset(np.array(60.0), U) < path_offset(np.array(200.0), U) <= 48


def test_empty_house_is_open_both_sides():
    f = D([])
    assert f["draw_open_sides"] == 2 and f["draw_against"] == 0 and f["draw_gain"] == 1 and f["draw_open_worst"] == 1


def test_straight_centre_guard_does_not_block():
    # other team lies one in the 8-foot, a centre guard straight in front of the button
    f = D([(0, 40, 0), (0, 130, 0)])
    assert f["draw_against"] == 1 and f["draw_open_sides"] == 2


def test_wing_guard_closes_one_side():
    # guards out on the right, where a draw curling in from that side passes: the left stays open
    f = D([(0, 40, 0), (42, 130, 0), (44, 160, 0), (40, 100, 0)])
    assert f["draw_open_sides"] == 1 and f["draw_open_best"] > 0.8 and f["draw_open_worst"] < 0.3


def test_both_sides_closed():
    f = D([(0, 40, 0)] + [(s * 42, yy, 0) for s in (-1, 1) for yy in (100, 130, 160, 190)])
    assert f["draw_open_sides"] == 0 and f["draw_backed"] == 0


def test_backing_behind_the_tee():
    # other team lies three, its best stone behind the tee: a draw onto it outcounts it and is backed
    f = D([(0, -20, 0), (30, -50, 0), (-40, 30, 0)])
    assert f["draw_against"] == 3 and f["draw_backed"] == 1 and f["draw_open_sides"] == 2


def test_stone_on_the_button_leaves_no_room():
    f = D([(0, 1, 0)])
    assert f["draw_open_sides"] == 0 and f["draw_open_best"] == 0


def test_gain_counts_own_stones_inside():
    f = D([(0, 50, 0), (10, 10, 1), (-20, -15, 1)])
    assert f["draw_against"] == 0 and f["draw_gain"] == 3


def test_mirror_symmetric():
    s = [(0, 40, 0), (42, 130, 0), (44, 160, 0), (-15, -30, 1)]
    a, b = D(s), D([(-x, y, o) for x, y, o in s])
    assert a == b
