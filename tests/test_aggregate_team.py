import pandas as pd

from pointsgained.model.aggregate import by_team_event


def _pg():
    """Two games, each one end of two stones. Game 1: A has hammer and scores 2. Game 2: B has hammer, A steals 1."""
    rows = []
    for gk, hammer, score in (("g1", "A", 2), ("g2", "B", -1)):
        for shot, team in ((1, "B" if hammer == "A" else "A"), (2, hammer)):
            rows.append(dict(book="BK", discipline="M", game_key=gk, end=1, shot=shot, team=team, hammer_team=hammer,
                             end_score_hammer=score, pg=0.1, pg_wp=0.2 if team == "A" else -0.1, pg_throw_wp=0.05))
    return pd.DataFrame(rows)


def test_record_and_wp_gain_per_game():
    t = by_team_event(_pg()).set_index("team")
    assert (t.loc["A", "wins"], t.loc["A", "losses"]) == (2, 0)
    assert (t.loc["B", "wins"], t.loc["B", "losses"]) == (0, 2)
    assert t.loc["A", "games"] == 2
    assert abs(t.loc["A", "wp_gain"] - 20.0) < 1e-9      # 0.2 per stone, one stone per game, in percentage points
    assert abs(t.loc["B", "wp_gain"] + 10.0) < 1e-9
    assert list(t.index) == ["A", "B"]                     # sorted by WP gained
