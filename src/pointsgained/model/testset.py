"""The face-validity test set (design Sections 6 and 13).

Six last-rock shots from the 2026 Olympic men's tournament: the five hit-family calls the V0
model rated worst by win probability (four of them made and won the end) and Brad Jacobs'
ninth-end clearing in the gold-medal game (the worst-rated call of all, made for three). The
type-only call component prices them as poor menus because the field rarely plays them from
those positions; the intent and skill inputs are meant to tell whether the shot was on.
"""
from __future__ import annotations

import pandas as pd

OWG = "OWG2026_ResultsBook"
TEST_SHOTS = [
    # (game_key, end, shot, note)
    (f"{OWG}|2026-02-21|19:05|Gold_Medal_Game|CAN-GBR", 9, 16, "Jacobs, down one with hammer, runback clearing for three"),
    (f"{OWG}|2026-02-15|19:05|Round_Robin_Session_7_Sheet_B|NOR-USA", 10, 16, "Casper, tied last end, promotion take-out for two"),
    (f"{OWG}|2026-02-13|9:05|Round_Robin_Session_3_Sheet_B|GBR-ITA", 10, 16, "Retornaz, tied last end, promotion take-out for two"),
    (f"{OWG}|2026-02-11|19:05|Round_Robin_Session_1_Sheet_C|CZE-USA", 10, 16, "Casper, tied last end, promotion take-out for one"),
    (f"{OWG}|2026-02-17|9:05|Round_Robin_Session_9_Sheet_D|CZE-GER", 9, 16, "Muskatewitz, down one with hammer, raise for two"),
    (f"{OWG}|2026-02-19|19:35|Semi_final_Sheet_B|GBR-SUI", 6, 16, "Schwarz-van Berkel, up one with hammer, clearing missed, steal"),
]

COLS = ["player", "shot_type", "grade_pct", "diff_hammer", "ends_remaining", "end_score_hammer",
        "pg_call", "pg_throw", "pg_call_own", "pg_throw_own", "pg_call_wp", "pg_throw_wp", "pg_call_own_wp", "pg_throw_own_wp"]


def testset_table(pg: pd.DataFrame, extra_cols: list[str] | None = None) -> pd.DataFrame:
    """The six shots' rows from a Points Gained table, in the pinned order, with a note column."""
    key = pd.DataFrame(TEST_SHOTS, columns=["game_key", "end", "shot", "note"])
    cols = [c for c in COLS + (extra_cols or []) if c in pg]
    df = key.merge(pg[["game_key", "end", "shot"] + cols], on=["game_key", "end", "shot"], how="left")
    return df[["note"] + cols]


def write_testset_report(pg: pd.DataFrame, path: str, title: str = "Face-validity test set", extra_cols=None) -> pd.DataFrame:
    t = testset_table(pg, extra_cols)
    with open(path, "w") as f:
        f.write(f"# {title}\n\nSix last-rock shots from the 2026 Olympic men's tournament (design Section 6). "
                "`pg_call` and `pg_throw` are in hammer-adjusted points from the thrower's view, with the call valued at the "
                "tier's reference skill; `_own` values the call at the thrower's own skill (design 3.5); `_wp` is win probability. "
                "`diff_hammer` is the hammer team's lead before the end.\n\n")
        f.write(t.round(3).to_markdown(index=False) + "\n")
    return t
