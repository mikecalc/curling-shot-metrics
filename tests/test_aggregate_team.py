import numpy as np
import pandas as pd

from pointsgained.model.aggregate import by_team_event, game_ledger


def _pg():
    """Two one-end games of two stones each (the last end of the game). Game 1: A has hammer and scores 2.
    Game 2: B has hammer, A steals 1. WP (hammer team's view) runs 0.6 -> 0.5 -> result."""
    rows = []
    for gk, hammer, score in (("g1", "A", 2), ("g2", "B", -1)):
        other = "B" if hammer == "A" else "A"
        final = 1.0 if score > 0 else 0.0
        for shot, team, pre, post in ((1, other, 0.6, 0.5), (2, hammer, 0.5, final)):
            sign = 1.0 if team == hammer else -1.0
            rows.append(dict(book="BK", discipline="M", game_key=gk, end=1, shot=shot, team=team, hammer_team=hammer,
                             end_score_hammer=score, ends_remaining=1, V_pre_wp=pre, V_post_wp=post,
                             pg=0.1, pg_wp=sign * (post - pre), pg_throw_wp=0.05))
    return pd.DataFrame(rows)


def test_game_ledger_adds_up_to_the_result():
    led = game_ledger(_pg())
    assert np.allclose(led["net"], led["dsc"] + led["own"] + led["allowed"] + led["other"])
    a = led[led["team"] == "A"].set_index("game_key")
    assert np.allclose(a["net"], 50.0)                                  # A won both
    assert np.isclose(a.loc["g1", "dsc"], 10.0) and np.isclose(a.loc["g2", "dsc"], -10.0)   # 0.6 with hammer, 0.4 without
    assert np.isclose(a.loc["g1", "control"], 60.0)                     # one scheduled end: its start


def test_own_is_relative_to_the_field_by_stone_pair():
    led = game_ledger(_pg()).set_index(["game_key", "team"])
    # pair 1 (stones 1-2): field mean of pg_wp over the four stones; own = stone minus that mean
    pg = _pg()
    m = pg["pg_wp"].mean()
    own_a_g1 = 100 * (pg[(pg.game_key == "g1") & (pg.team == "A")]["pg_wp"].sum() - m)
    assert np.isclose(led.loc[("g1", "A"), "own"], own_a_g1)
    assert np.isclose(led.loc[("g1", "A"), "allowed"], -led.loc[("g1", "B"), "own"])


def test_record_sorted_by_net():
    t = by_team_event(_pg()).set_index("team")
    assert (t.loc["A", "wins"], t.loc["A", "losses"]) == (2, 0)
    assert (t.loc["B", "wins"], t.loc["B", "losses"]) == (0, 2)
    assert t.loc["A", "games"] == 2 and np.isclose(t.loc["A", "net"], 50.0)
    assert list(t.index) == ["A", "B"]


def test_x_ended_end_scores_nothing():
    pg = _pg()
    x = pg[pg.game_key == "g1"].assign(end=2, end_score_hammer=np.nan)     # an X end after A's 2
    led = game_ledger(pd.concat([pg, x])).set_index(["game_key", "team"])
    assert np.isclose(led.loc[("g1", "A"), "net"], 50.0)


def test_by_team_record_and_win_rate():
    from pointsgained.model.aggregate import by_team
    t = by_team(_pg(), min_games=1).set_index("team")
    assert t.loc["A", "win_rate"] == 1.0 and t.loc["B", "win_rate"] == 0.0


def test_execution_block_splits_the_distribution():
    from pointsgained.model.aggregate import execution_block
    b = execution_block(pd.Series([0.6, 0.2, 0.0, -0.1, -0.7]))
    assert b["reliability"] == 0.6
    assert abs(b["avg_make"] - (0.8 / 3)) < 1e-12 and abs(b["avg_miss"] + 0.4) < 1e-12
    assert (b["big_makes"], b["big_misses"]) == (1, 1)
    assert abs(b["net"] - 0.0) < 1e-12
