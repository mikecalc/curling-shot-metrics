"""Leaderboards (design Section 10)."""
from __future__ import annotations

import os

import numpy as np
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


# ---- Stratified reporting -------------------------------------------------------------------

STATE_BINS = [-99, -3, -1, 0, 2, 99]
STATE_LABELS = ["down 3+", "down 1-2", "tied", "up 1-2", "up 3+"]


def attach_strata(pg: pd.DataFrame, situations: dict, inventory_csv: str | None = None) -> pd.DataFrame:
    """Add tier, event family, hammer label and game-state bucket (thrower's view) to the PG table."""
    pg = pg.copy()
    diff_h = np.array([situations.get((g, e), (np.nan, np.nan))[0] for g, e in zip(pg["game_key"], pg["end"])], dtype=float)
    ends_left = np.array([situations.get((g, e), (np.nan, np.nan))[1] for g, e in zip(pg["game_key"], pg["end"])], dtype=float)
    pg["diff_thrower"] = np.where(pg["thrower_has_hammer"], diff_h, -diff_h)
    pg["ends_remaining"] = ends_left
    pg["game_state"] = pd.cut(pg["diff_thrower"], STATE_BINS, labels=STATE_LABELS)
    pg["hammer"] = np.where(pg["thrower_has_hammer"], "hammer", "no hammer")
    pg["tier"] = None
    pg["event_family"] = None
    if inventory_csv and os.path.exists(inventory_csv):
        inv = pd.read_csv(inventory_csv)
        inv["book"] = inv["file_name"].str.replace(r"\.pdf$", "", regex=True)
        m = inv.drop_duplicates("book").set_index("book")
        pg["tier"] = pg["book"].map(m["tier"])
        pg["event_family"] = pg["book"].map(m["event_family"])
    return pg


VALUE_COLS = ["pg", "pg_call", "pg_throw", "pg_wp", "pg_call_wp", "pg_throw_wp"]


def _agg(pg: pd.DataFrame, keys: list[str], min_shots: int = 1) -> pd.DataFrame:
    cols = [c for c in VALUE_COLS if c in pg]
    out = pg.groupby(keys, observed=True, dropna=False).agg(shots=("pg", "size"), **{c: (c, "mean") for c in cols}).reset_index()
    return out[out["shots"] >= min_shots]


def strata_tables(pg: pd.DataFrame, min_shots_player: int = 40) -> dict[str, pd.DataFrame]:
    """The stratified tables: by discipline/tier, hammer, game state, shot type x hammer, players x hammer."""
    t = {}
    t["discipline_tier"] = _agg(pg, ["discipline", "tier"])
    t["discipline_hammer"] = _agg(pg, ["discipline", "hammer"])
    t["game_state_hammer"] = _agg(pg, ["hammer", "game_state"])
    t["shot_type_hammer"] = _agg(pg, ["shot_type", "hammer"], min_shots=30)
    t["shot_number"] = _agg(pg, ["shot"])
    t["teams"] = _agg(pg, ["discipline", "team"], min_shots=200).sort_values("pg", ascending=False)
    t["teams_hammer"] = _agg(pg, ["discipline", "team", "hammer"], min_shots=100)
    players = _agg(pg, ["discipline", "team", "player"], min_shots=min_shots_player)
    # field-relative execution: subtract the field mean throw value for the same shot type and hammer state
    base = pg.groupby(["shot_type", "hammer"], observed=True)["pg_throw"].transform("mean")
    rel = pg.assign(pg_throw_rel=pg["pg_throw"] - base).groupby(["discipline", "team", "player"]).agg(
        pg_throw_rel=("pg_throw_rel", "mean"), grade=("grade_pct", "mean")).reset_index()
    t["players"] = players.merge(rel, on=["discipline", "team", "player"]).sort_values("pg_throw_rel", ascending=False)
    t["players_hammer"] = _agg(pg, ["discipline", "team", "player", "hammer"], min_shots=max(20, min_shots_player // 2))
    return t
