import numpy as np
import pandas as pd

from pointsgained.model.report import game_report, game_file_name

H = 0.6


def _game():
    """Two ends of four stones: A scores one with hammer in end 1, B blanks in end 2. Values telescope
    (each stone's V before is the previous stone's V after) and the terminal value is the hammer-adjusted result."""
    rows = []
    ends = [  # (hammer, score, V path: V_pre of stone 1 then V_call/V_post per stone)
        ("A", 1, 0.5, [(0.55, 0.6), (0.5, 0.7), (0.8, 0.9), (0.95, 1 - H)]),
        ("B", 0, 0.5, [(0.45, 0.4), (0.5, 0.6), (0.55, 0.5), (0.7, H)]),
    ]
    for end, (hammer, score, v0, path) in enumerate(ends, start=1):
        v_pre = v0
        for shot, (v_call, v_post) in enumerate(path, start=1):
            team = "A" if (shot % 2 == 1) == (hammer == "A") else "B"
            sign = 1.0 if team == hammer else -1.0
            # win probability (hammer view) telescopes the same way: V + 0.1, call halfway
            w_pre, w_post = v_pre + 0.1, v_post + 0.1
            w_call = (w_pre + w_post) / 2
            rows.append(dict(game_key="k", end=end, shot=shot, team=team, player=f"P{team}{(shot + 1) // 2}",
                             shot_type="Draw", turn="cw", grade_pct=100.0, hammer_team=hammer, diff_hammer=0,
                             ends_remaining=3 - end, V_pre=v_pre, V_call=v_call, V_post=v_post,
                             pg_canonical=v_post - v_pre, pg=sign * (v_post - v_pre),
                             pg_call=sign * (v_call - v_pre), pg_throw=sign * (v_post - v_call),
                             V_pre_wp=w_pre, V_call_wp=w_call, V_post_wp=w_post, pg_wp=sign * (w_post - w_pre),
                             pg_call_wp=sign * (w_call - w_pre), pg_throw_wp=sign * (w_post - w_call),
                             end_score_hammer=score))
            v_pre = v_post
    return pd.DataFrame(rows)


def test_game_report_sections_and_conservation():
    text = game_report(_game(), "Title", "sub", team_order=("A", "B"))
    for section in ("# Title", "## Ends", "## Players", "## Largest swings", "## Shots", "### End 1", "### End 2"):
        assert section in text
    assert "A 1" in text and "blank" in text                 # end results
    assert "Warning" not in text                              # the PG columns close every end
    for col in ("WP before", "WP after", "WP gain", "PGAA", "call"):
        assert f" {col} " in text
    assert "WP call" not in text and "PG pts" not in text


def test_game_report_end_table_in_win_probability():
    df = _game()
    text = game_report(df, "T", team_order=("A", "B"))
    section = text.split("## Ends")[1].split("## Players")[0]
    ends = [l for l in section.splitlines() if l.startswith("|     1 ") or l.startswith("|     2 ")]
    assert len(ends) == 2
    # end 1: A has hammer; WP A before = 100 * (0.5 + 0.1) = 60, after = 100 * (1 - H + 0.1) = 50, swing -10
    cells = [c.strip() for c in ends[0].split("|")[1:-1]]
    assert cells[:4] == ["1", "A", "A 1", "1-0"]
    assert [float(c) for c in cells[4:7]] == [60.0, round(100 * (1 - H + 0.1), 1), -10.0]
    assert len(cells) == 7                                     # nothing but score and win probability
    # A's WP gains minus B's equal the swing (checked inside the report; no warning printed)
    e1 = df[df["end"] == 1]
    lhs = 100 * (e1.loc[e1["team"] == "A", "pg_wp"].sum() - e1.loc[e1["team"] == "B", "pg_wp"].sum())
    assert abs(lhs + 10.0) < 1e-9


def test_players_table_leads_with_execution():
    text = game_report(_game(), "T", team_order=("A", "B"))
    header = [l for l in text.split("## Players")[1].splitlines() if l.startswith("| team")][0]
    cols = [c.strip() for c in header.split("|")[1:-1]]
    assert cols == ["team", "player", "shots", "grade", "PGAA", "worst stone", "best stone", "WP gain"]


def test_game_report_team_sums_close_the_end():
    df = _game()
    text = game_report(df, "T", team_order=("A", "B"))
    # end 1: A's totals minus B's totals equal the adjusted result minus the start expectation
    e1 = df[df["end"] == 1]
    lhs = e1.loc[e1["team"] == "A", "pg"].sum() - e1.loc[e1["team"] == "B", "pg"].sum()
    assert abs(lhs - ((1 - H) - 0.5)) < 1e-12
    assert "PA2" in text and "PB2" in text
    header = [l for l in text.split("### End 1")[1].splitlines() if l.startswith("|   shot")][0]
    cols = [c.strip() for c in header.split("|")[1:-1]]
    assert cols == ["shot", "team", "player", "type", "turn", "grade", "WP before", "PGAA", "call", "WP after", "WP gain"]


def test_file_name_is_safe():
    assert game_file_name("OWG2026_ResultsBook|2026-02-21|19:05|Gold_Medal_Game|CAN-GBR") == \
        "OWG2026_ResultsBook_2026-02-21_19_05_Gold_Medal_Game_CAN-GBR.md"
