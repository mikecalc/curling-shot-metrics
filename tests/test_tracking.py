import numpy as np

from pointsgained.core.tracking import Frame, count_ids, match, track_end


def F(shot, stones, delivered=None, priors=()):
    """stones: list of (x, y, owner)."""
    a = np.array(stones, dtype=float).reshape(-1, 3)
    d = np.zeros(len(a), dtype=bool)
    if delivered is not None:
        d[delivered] = True
    p = np.array(priors, dtype=float).reshape(-1, 2)
    return Frame(shot, a[:, 0], a[:, 1], a[:, 2].astype(int), d, p[:, 0], p[:, 1])


def by_sid(recs, shot):
    return {r["sid"]: r for r in recs if r["shot"] == shot}


def test_unmoved_keeps_identity_and_thrown_is_new():
    f1 = F(1, [(0, 10, 0)], delivered=0)
    f2 = F(2, [(0, 10, 0), (20, 100, 1)], delivered=1)
    link, status = match(f1, f2)
    assert link == {0: 0} and status == {0: "unmoved", 1: "thrown"}


def test_moved_stone_is_linked_through_its_prior_ring():
    # a hammer stone at (0, 10) is hit back to (2, -30) by an opponent stone that stays at (0, 12);
    # a ring marks (0, 10), where the hammer stone was
    f1 = F(3, [(0, 10, 1), (50, 120, 0)])
    f2 = F(4, [(50, 120, 0), (2, -30, 1), (0, 12, 0)], delivered=2, priors=[(0, 10)])
    link, status = match(f1, f2)
    assert status[0] == "unmoved" and link[0] == 1
    assert status[1] == "moved" and link[1] == 0
    assert status[2] == "thrown"


def test_removed_stone_disappears_and_the_life_records_counting():
    frames = [
        F(1, [(0, 60, 0)], delivered=0),                              # non-hammer guard
        F(2, [(0, 60, 0), (30, -10, 1)], delivered=1),                 # hammer stone behind the tee
        F(3, [(0, 60, 0), (1, 5, 0)], delivered=1),                    # hammer stone removed; non-hammer on the button
        F(4, [(0, 60, 0), (1, 5, 0), (40, 0, 1)], delivered=2),
    ]
    recs = track_end(frames)
    guard = [r for r in recs if r["shot"] == 1][0]["sid"]
    button = [r for r in recs if r["shot"] == 3 and r["y"] == 5][0]["sid"]
    last = by_sid(recs, 4)
    assert guard in last and last[guard]["status"] == "unmoved" and last[guard]["born"] == 1
    assert all(r["counts_end"] for r in recs if r["sid"] == button)       # it counts at the end
    assert all(r["shot_rock_end"] for r in recs if r["sid"] == button)
    assert not any(r["counts_end"] for r in recs if r["sid"] == guard)    # the guard is out of the house
    removed = [r for r in recs if r["shot"] == 2 and r["owner"] == 1][0]["sid"]
    assert not any(r["alive_end"] for r in recs if r["sid"] == removed)


def test_count_ids():
    idx, shot = count_ids(np.array([0.0, 20.0, 40.0, 100.0]), np.array([0.0, 0.0, 0.0, 0.0]), np.array([1, 1, 0, 1]))
    assert list(idx) == [0, 1] and shot == 0
    idx, shot = count_ids(np.array([200.0]), np.array([0.0]), np.array([1]))
    assert len(idx) == 0 and shot == -1


def test_unmarked_thrown_stone_is_inferred_from_the_throwers_colour():
    f1 = F(1, [(0, 10, 0)])                                   # first diagram, no mark: the non-hammer stone
    f2 = F(2, [(0, 10, 0), (20, 100, 1)])                     # no mark: the one new hammer stone
    recs = track_end([f1, f2])
    assert [r["status"] for r in recs if r["shot"] == 1] == ["thrown"]
    s2 = {r["owner"]: r for r in recs if r["shot"] == 2}
    assert s2[1]["status"] == "thrown" and not s2[1]["marked"] and s2[0]["status"] == "unmoved"


def test_two_unmarked_new_stones_of_the_throwers_colour_stay_new():
    # a missing diagram between: two new hammer stones, neither can be named the thrown one
    f1 = F(1, [(0, 10, 0)], delivered=0)
    f3 = F(4, [(0, 10, 0), (20, 100, 1), (-20, 90, 1)])
    _, status = match(f1, f3)
    assert status[1] == "new" and status[2] == "new"
