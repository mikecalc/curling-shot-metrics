import numpy as np
from pointsgained.core.configurations import LABELS, configuration, label_matrix
from pointsgained.core.positions import Position


def P(stones, rocks_remaining=8):
    """stones: list of (x, y, owner) with owner 1 = hammer team."""
    a = np.array(stones, dtype=float).reshape(-1, 3)
    return Position(a[:, 0], a[:, 1], a[:, 2].astype(int), rocks_remaining)


def on(p):
    return {k for k, v in configuration(p).items() if v}


def test_empty_sheet():
    assert on(Position.empty()) == {"empty", "open_house"}


def test_guards_only_centre_and_corner():
    labs = on(P([(0, 120, 0), (-50, 110, 1)], 14))
    assert labs == {"guards_only", "opp_centre_guard", "own_corner_guard"}


def test_split_house():
    # two hammer stones in the house either side of the pin, 80 in apart, no opponent in the house
    labs = on(P([(-40, 10, 1), (40, 5, 1)]))
    assert {"split_house", "own_shot", "own_two_plus", "open_house"} <= labs
    # an opponent stone in the house breaks the split
    assert "split_house" not in on(P([(-40, 10, 1), (40, 5, 1), (60, -30, 0)]))
    # two hammer stones close together are not split
    assert "split_house" not in on(P([(0, 0, 1), (12, 3, 1)]))


def test_steal_on():
    # non-hammer shot rock on the button behind a guard
    labs = on(P([(0, 0, 0), (2, 110, 0), (40, 0, 1)], 6))
    assert {"steal_on", "opp_shot", "opp_centre_guard"} <= labs
    assert "own_shot" not in labs
    # the same shot rock without the guard is not covered
    assert "steal_on" not in on(P([(0, 0, 0), (40, 0, 1)], 6))


def test_own_shot_covered_and_busy_house():
    labs = on(P([(0, 0, 1), (1, 100, 0), (30, 0, 0), (-30, 5, 1), (0, -40, 0)]))
    assert {"own_shot_covered", "opp_centre_guard", "busy_house"} <= labs
    assert "own_two_plus" not in labs   # the second stone is the opponent's


def test_near_tie():
    labs = on(P([(0, 0, 1), (30, 0, 1), (31, 0, 0)]))
    assert {"near_tie", "own_two_plus"} <= labs


def test_label_matrix_shape():
    m = label_matrix([Position.empty(), P([(0, 0, 1)])])
    assert m.shape == (2, len(LABELS)) and m[0, LABELS.index("empty")] and m[1, LABELS.index("own_shot")]


def test_split_flat_and_staggered():
    # side by side at the same depth, 80 in apart: flat
    assert {"split_house", "split_flat"} <= on(P([(-40, 10, 1), (40, 5, 1)]))
    # 60 in apart but staggered 40 in in depth (about 34 degrees): the double is on
    labs = on(P([(-30, 30, 1), (30, -10, 1)]))
    assert {"split_house", "split_staggered"} <= labs and "split_flat" not in labs
    # 40 in apart and level: a split, but not far enough apart to be flat
    labs = on(P([(-20, 0, 1), (20, 0, 1)]))
    assert "split_staggered" in labs and "split_flat" not in labs


def test_deuce_loose():
    # from stone 9: a flat split
    assert "deuce_loose" in on(P([(-40, 10, 1), (40, 5, 1)], 8))
    assert "deuce_loose" not in on(P([(-40, 10, 1), (40, 5, 1)], 10))
    # a covered hammer stone on the wing with the centre open; not shot rock is fine as long as it counts second
    wing = [(55, 20, 1), (57, 110, 0), (-66, -20, 0)]
    assert "deuce_loose" in on(P(wing, 7))
    # an opponent stone in the 4-foot closes the centre
    assert "deuce_loose" not in on(P(wing + [(0, 5, 0)], 7))
    # a centre guard closes the centre
    assert "deuce_loose" not in on(P(wing + [(0, 120, 0)], 7))


def test_steal_setup_and_exposed():
    labs = on(P([(0, 120, 0), (10, 150, 0)], 12))
    assert "steal_setup" in labs and "opp_exposed" not in labs
    labs = on(P([(0, 120, 0), (40, 0, 0)], 12))           # a non-hammer stone in the house off the guard's line
    assert "opp_exposed" in labs and "steal_setup" not in labs


def test_open_shot():
    assert {"open_shot_own", "own_shot"} <= on(P([(0, 0, 1), (30, 0, 0)]))
    assert "open_shot_opp" in on(P([(0, 0, 0)]))
    assert "open_shot_opp" not in on(P([(0, 0, 0), (0, 120, 1)]))


def test_pair_measures():
    from pointsgained.core.configurations import pair_measures
    m = pair_measures(P([(-30, 30, 1), (30, -10, 1), (0, 200, 1), (0, 0, 0)]))
    assert abs(m["own_pair_sep"] - np.hypot(60, 40)) < 1e-9
    assert abs(m["own_pair_angle"] - np.degrees(np.arctan2(40, 60))) < 1e-9
    assert m["opp_pair_sep"] == 0.0


def test_runback_straight_angled_and_stake():
    from pointsgained.core.configurations import runback
    # non-hammer lying one on the button, hammer 2 and 3 behind it; a guard straight in front 8 ft up
    base = [(0, 0, 0), (20, -10, 1), (-30, 5, 1)]
    straight = base + [(3, 96, 0)]
    r = runback(P(straight, 6))
    assert r["shot_runback_angle"] < 10 and abs(r["shot_runback_dist"] - 96) < 1e-9
    assert r["swing_if_shot_removed"] == 3.0                  # -1 -> +2
    labs = on(P(straight, 6))
    assert {"shot_runback_straight", "lonely_steal", "lonely_steal_exposed"} <= labs
    # the same guard 30 in to the side: an angle runback (about 17 degrees)
    labs = on(P(base + [(30, 96, 0)], 6))
    assert "shot_runback_angled" in labs and "shot_runback_straight" not in labs and "lonely_steal_exposed" in labs
    # guard far to the side: no runback, the lonely steal is not exposed
    labs = on(P(base + [(90, 96, 0)], 6))
    assert "lonely_steal" in labs and "lonely_steal_exposed" not in labs
    # hammer counts only one behind: the stake is a swing of two, not a lonely steal
    assert "lonely_steal" not in on(P([(0, 0, 0), (20, -10, 1), (3, 96, 0)], 6))


def test_tucked_stone_can_be_run_back():
    # hammer tucks behind a non-hammer stone but not far enough: the non-hammer stone is straight in front
    labs = on(P([(2, -3, 1), (0, 20, 0)], 8))
    assert "own_shot" in labs and "shot_runback_straight" in labs
