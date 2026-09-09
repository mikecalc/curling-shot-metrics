from pointsgained.core.count import count_position


def test_empty_house_blank():
    assert count_position([]) == (None, 0)
    assert count_position([("red", 0.0, 100.0)]) == (None, 0)   # guard only


def test_single_shot_rock():
    assert count_position([("red", 0.0, 0.0), ("yellow", 30.0, 0.0)]) == ("red", 1)


def test_two_before_opponent():
    stones = [("yellow", 5.0, 0.0), ("yellow", 0.0, 20.0), ("red", 40.0, 0.0), ("yellow", 60.0, 0.0)]
    assert count_position(stones) == ("yellow", 2)


def test_biting_twelve_foot_counts():
    # centre 76 inches from the pin: bites the 12-foot (72 + 5.7)
    assert count_position([("red", 76.0, 0.0)]) == ("red", 1)
    assert count_position([("red", 78.0, 0.0)]) == (None, 0)
