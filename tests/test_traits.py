import numpy as np
from pointsgained.core.positions import Position
from pointsgained.core.traits import TRAITS, stone_traits, trait_type, type_name


def P(stones, rocks_remaining=8):
    """stones: list of (x, y, owner) with owner 1 = hammer team."""
    a = np.array(stones, dtype=float).reshape(-1, 3)
    return Position(a[:, 0], a[:, 1], a[:, 2].astype(int), rocks_remaining)


def on(p, i):
    return {k for k, v in zip(TRAITS, stone_traits(p)[i]) if v}


def test_empty_sheet():
    assert stone_traits(Position.empty()).shape == (0, len(TRAITS))


def test_single_centre_guard():
    # Mike's example: in the front and controlling the 4-foot, nothing else (and open)
    assert on(P([(0, 120, 0)], 15), 0) == {"front", "controls_4ft", "open"}


def test_rings_nested_and_tee():
    t = on(P([(0, 10, 1)]), 0)
    assert {"four_foot", "eight_foot", "twelve_foot", "above_tee", "shot_rock", "open"} == t
    t = on(P([(0, -40, 1)]), 0)
    assert {"eight_foot", "twelve_foot", "behind_tee", "shot_rock", "open"} == t


def test_wing_house_stone_vs_corner_guard():
    assert "wing" in on(P([(50, 20, 1)]), 0)
    t = on(P([(50, 120, 1)]), 0)
    assert "wing" not in t and "front" in t and "controls_4ft" not in t


def test_high_centre_house_stone_controls_4ft():
    t = on(P([(5, 45, 0)]), 0)
    assert {"controls_4ft", "eight_foot", "above_tee", "shot_rock"} <= t


def test_draw_behind_guard():
    p = P([(0, 110, 0), (3, 5, 1)])
    assert {"front", "guarding", "controls_4ft", "open"} == on(p, 0)
    assert {"four_foot", "behind_cover", "shot_rock"} <= on(p, 1)


def test_partly_open():
    p = P([(0, 110, 0), (9, 5, 1)])      # the guard overlaps the stone's line by less than half a stone
    assert "partly_open" in on(p, 1)


def test_freeze_front_stone_is_frozen():
    # yellow in the 4-foot, red frozen onto the front of it
    p = P([(0, 0, 1), (1, 11.6, 0)])
    front, back = on(p, 1), on(p, 0)
    assert {"frozen_opp", "guarding"} <= front and "frozen_own" not in front
    assert "behind_cover" in back and not ({"frozen_own", "frozen_opp"} & back)
    p = P([(0, 0, 1), (1, 11.6, 1)])
    assert "frozen_own" in on(p, 1)


def test_shot_ranking_is_colour_blind():
    p = P([(0, 30, 1), (0, 2, 0), (40, 0, 1), (70, 60, 0)])
    assert "shot_rock" in on(p, 1) and "second_shot" in on(p, 0) and "third_shot" in on(p, 2)
    assert not ({"shot_rock", "second_shot", "third_shot"} & on(p, 3))


def test_exposure_is_exclusive_and_mirror_invariant():
    p = P([(0, 110, 0), (9, 5, 1), (-40, -20, 0), (20, 60, 1), (-3, 30, 0)])
    m = stone_traits(p)
    ex = m[:, [TRAITS.index(k) for k in ("open", "partly_open", "behind_cover")]]
    assert (ex.sum(axis=1) == 1).all()
    assert (stone_traits(p.mirrored()) == m).all()


def test_type_bitmask():
    m = stone_traits(P([(0, 120, 0)], 15))
    assert type_name(int(trait_type(m)[0])) == "front+controls_4ft+open"


def test_slots_keep_each_rock_whole():
    import pandas as pd
    from pointsgained.core.traits import TRAITS, traits_xy
    from pointsgained.model.slot_features import compute_table
    # non-hammer shot rock behind a hammer guard; hammer second shot open on the wing
    x, y, o = np.array([0.0, 2.0, 40.0]), np.array([110.0, 5.0, 10.0]), np.array([1, 0, 1])
    m = traits_xy(x, y, o)
    long = pd.DataFrame({"game_key": "g", "end": 1, "shot": 3, "owner": o, "x": x, "y": y})
    long[TRAITS] = m
    t = compute_table(long).iloc[0]
    assert t["s1_owner"] == 0 and t["s1_exposure"] == 2 and t["s1_four_foot"] == 1
    assert t["s2_owner"] == 1 and t["s2_wing"] == 1 and t["s2_exposure"] == 0
    assert t["s3_owner"] == -1
    assert t["gh_owner"] == 1 and t["gh_guarding"] == 1 and t["gn_owner"] == -1
