import numpy as np
from pointsgained.core.taps import TAP_COUNT_COLUMNS, taps


def T(stones, thrower=1, **kw):
    """stones: list of (x, y, owner) with owner 1 = hammer team."""
    a = np.array(stones, dtype=float).reshape(-1, 3)
    return taps(a[:, 0], a[:, 1], a[:, 2].astype(int), thrower, **kw)


def test_empty_house_has_no_tap():
    assert T([])["tap_on"] == 0 and T([(0, 120, 1)])["tap_on"] == 0


def test_raise_own_stone_to_the_button():
    # Mike's case: our stone at the top of the 4-foot, raised towards the button; the shooter stays for two
    f = T([(0, 30, 1)])
    assert f["tap_on"] == 1 and f["tap_own"] == 1 and f["tap_swing"] == 1


def test_come_around_our_stone_to_tap_theirs():
    # ours at the top of the 8-foot, theirs at the top of the button: curling past ours to tap theirs back
    f = T([(0, 40, 1), (0, 10, 0)])
    assert f["tap_on"] == 1 and f["tap_own"] == 0 and f["tap_swing"] >= 2 and f["tap_covered"] == 1


def test_tap_theirs_back_and_sit_backed():
    # Mike's case: their stone at the top of the 4-foot, tapped back just far enough; the shooter outcounts it
    # and has a stone behind it
    f = T([(0, 20, 0)])
    assert f["tap_on"] == 1 and f["tap_own"] == 0 and f["tap_swing"] == 2 and f["tap_backed"] >= 1
    assert f["tap_move"] == 48.0 and f["tap_angle"] == 0.0


def test_tap_comes_around_cover():
    # taps are draws: their stone behind a centre guard is tapped by curling around the guard
    f = T([(0, 20, 0), (0, 120, 1)])
    assert f["tap_on"] == 1 and f["tap_own"] == 0 and f["tap_covered"] == 1
    assert T([(0, 20, 0)])["tap_covered"] == 0


def test_only_stones_around_the_4_foot_are_tapped():
    # finesse taps: the 4-foot plus about two stones, in front of the tee (or up to a foot behind), not the wings
    assert T([(20, 0, 0)])["tap_on"] == 1 and T([(30, 30, 0)])["tap_on"] == 1
    assert T([(50, 0, 0)])["tap_on"] == 0          # wing
    assert T([(0, -10, 0)])["tap_on"] == 1         # on the button, just behind the tee
    assert T([(0, -20, 0)])["tap_on"] == 0         # behind the tee
    assert T([(0, 60, 0)])["tap_on"] == 0          # top of the 12-foot


def test_no_contact_point_no_tap():
    # a stone frozen onto the front of it: no contact point is free, and the front stone cannot move
    assert T([(0, 20, 0), (0, 31.4, 0)])["tap_on"] == 0


def test_path_stops_at_the_freeze():
    # they lie two in a frozen stack, which cannot be tapped; ours above them is tapped down and stops frozen
    f = T([(0, 40, 1), (0, 16.4, 0), (0, 5, 0)])
    assert f["tap_on"] == 1 and f["tap_own"] == 1 and f["tap_swing"] == 0 and f["tap_move"] < 16


def test_tap_counts_are_the_position_after():
    f = T([(0, 20, 0)], with_counts=True)
    assert f["tp_h_twelve_foot"] == 1 and f["tp_n_twelve_foot"] == 1 and len([k for k in f if k.startswith("tp_")]) == len(TAP_COUNT_COLUMNS)


def test_tap_is_mirror_symmetric():
    s = [(-10, 25, 0), (30, -30, 1), (-40, 10, 1), (5, 110, 0)]
    for thrower in (0, 1):
        a = T(s, thrower)
        b = T([(-x, y, o) for x, y, o in s], thrower)
        assert all(np.isclose(a[k], b[k]) for k in a)
