"""Leaderboards (design Section 10)."""
from __future__ import annotations

import pandas as pd


def by_player(pg: pd.DataFrame, min_shots: int = 40) -> pd.DataFrame:
    g = pg.groupby(["player", "team", "discipline"])
    df = g.agg(shots=("pg", "size"), pg_throw_total=("pg_throw", "sum"), pg_throw_per_shot=("pg_throw", "mean"),
               pg_total=("pg", "sum"), grade=("grade_pct", "mean")).reset_index()
    return df[df["shots"] >= min_shots].sort_values("pg_throw_per_shot", ascending=False)


def by_team(pg: pd.DataFrame) -> pd.DataFrame:
    g = pg.groupby(["team", "discipline"])
    return g.agg(shots=("pg", "size"), pg_call_per_shot=("pg_call", "mean"), pg_throw_per_shot=("pg_throw", "mean"),
                 pg_per_shot=("pg", "mean")).reset_index().sort_values("pg_per_shot", ascending=False)


def by_shot_type(pg: pd.DataFrame) -> pd.DataFrame:
    g = pg.groupby("shot_type")
    return g.agg(shots=("pg", "size"), pg_call=("pg_call", "mean"), pg_throw=("pg_throw", "mean"),
                 pg=("pg", "mean"), grade=("grade_pct", "mean")).reset_index().sort_values("shots", ascending=False)


def by_shot_number(pg: pd.DataFrame) -> pd.DataFrame:
    g = pg.groupby("shot")
    return g.agg(shots=("pg", "size"), pg_abs=("pg", lambda s: s.abs().mean()), pg_throw_sd=("pg_throw", "std")).reset_index()
