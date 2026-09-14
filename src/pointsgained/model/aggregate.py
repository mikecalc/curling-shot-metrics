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


def attach_strata(pg: pd.DataFrame, situations: dict | None = None, inventory_csv: str | None = None) -> pd.DataFrame:
    """Add tier, event family, hammer label and game-state bucket (thrower's view) to the PG table.
    The situation comes from the table's own diff_hammer / ends_remaining columns, or from `situations`."""
    pg = pg.copy()
    if "diff_hammer" in pg and situations is None:
        diff_h = pg["diff_hammer"].to_numpy(dtype=float)
        ends_left = pg["ends_remaining"].to_numpy(dtype=float)
    else:
        situations = situations or {}
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
    # players are keyed by normalised name within a discipline: the same person appears under
    # different team codes (SCO at Worlds, GBR at the Olympics) and with case variants
    pg = pg.assign(player_key=pg["player"].fillna("").str.upper().str.replace(r"\s+", " ", regex=True).str.strip())
    pg = pg[pg["player_key"] != ""]
    players = _agg(pg, ["discipline", "player_key"], min_shots=min_shots_player)
    teams_of = pg.groupby(["discipline", "player_key"])["team"].agg(lambda s: "/".join(sorted(set(s)))).rename("teams").reset_index()
    # field-relative execution: subtract the field mean throw value for the same shot type and hammer state
    base = pg.groupby(["shot_type", "hammer"], observed=True)["pg_throw"].transform("mean")
    rel = pg.assign(pg_throw_rel=pg["pg_throw"] - base).groupby(["discipline", "player_key"]).agg(
        pg_throw_rel=("pg_throw_rel", "mean"), grade=("grade_pct", "mean")).reset_index()
    t["players"] = (players.merge(teams_of, on=["discipline", "player_key"]).merge(rel, on=["discipline", "player_key"])
                    .rename(columns={"player_key": "player"}).sort_values("pg_throw_rel", ascending=False))
    t["players_hammer"] = _agg(pg, ["discipline", "player_key", "hammer"], min_shots=max(20, min_shots_player // 2)).rename(columns={"player_key": "player"})
    return t


# ---- Per-event player leaderboards ----------------------------------------------------------

POSITION_NAMES = {1: "LEAD", 2: "SECOND", 3: "THIRD", 4: "FOURTH"}


def normalise_player(name) -> str:
    if not isinstance(name, str):
        return ""
    return " ".join(name.upper().split())


def by_player_event(pg: pd.DataFrame, books: list[str] | None = None, min_shots: int = 30) -> pd.DataFrame:
    """One row per (event book, discipline, player): position from throwing order (mode over the
    player's shots), execution relative to the whole field and to that event's field, both currencies.
    The execution block splits the distribution rather than averaging it: reliability (share of shots at
    or above the field), the average make and the average miss, the big-make and big-miss counts and the
    worst five; the mean is kept as the net."""
    df = pg.copy()
    if books:
        df = df[df["book"].isin(books)]
    df["player"] = df["player"].map(normalise_player)
    df = df[df["player"] != ""]
    df["hammer"] = np.where(df["thrower_has_hammer"], "hammer", "no hammer")
    df["team_shot"] = (df["shot"] + 1) // 2                     # 1..8 within the team's order
    df["pos_code"] = ((df["team_shot"] + 1) // 2).clip(1, 4)     # 1-2 lead, 3-4 second, 5-6 third, 7-8 fourth
    # field baselines for execution: whole corpus, and this event's field
    base_all = pg.assign(hammer=np.where(pg["thrower_has_hammer"], "hammer", "no hammer")) \
                 .groupby(["shot_type", "hammer"], observed=True)["pg_throw"].mean()
    df["pg_throw_rel"] = df["pg_throw"] - pd.MultiIndex.from_arrays([df["shot_type"], df["hammer"]]).map(base_all).to_numpy(dtype=float)
    base_ev = df.groupby(["book", "discipline", "shot_type", "hammer"], observed=True)["pg_throw"].transform("mean")
    df["pg_throw_rel_event"] = df["pg_throw"] - base_ev
    base_ev_wp = df.groupby(["book", "discipline", "shot_type", "hammer"], observed=True)["pg_throw_wp"].transform("mean")
    df["pg_throw_rel_event_wp"] = df["pg_throw_wp"] - base_ev_wp
    # same shot number and hammer state at this event: removes the leverage that fourths carry
    base_slot = df.groupby(["book", "discipline", "shot", "hammer"], observed=True)["pg_throw"].transform("mean")
    df["pg_throw_rel_slot"] = df["pg_throw"] - base_slot
    keys = ["book", "discipline", "player"]
    agg = df.groupby(keys).agg(
        team=("team", lambda s: "/".join(sorted(set(s)))),
        position=("pos_code", lambda s: POSITION_NAMES[int(s.mode().iloc[0])]),
        shots=("pg", "size"), games=("game_key", "nunique"),
        pg=("pg", "mean"), pg_call=("pg_call", "mean"), pg_throw=("pg_throw", "mean"),
        pg_throw_rel=("pg_throw_rel", "mean"), pg_throw_rel_event=("pg_throw_rel_event", "mean"),
        pg_throw_rel_event_median=("pg_throw_rel_event", "median"),
        sd=("pg_throw_rel_event", "std"),
        floor10=("pg_throw_rel_event", lambda x: float(x.quantile(0.10))),          # a bad day: 10th percentile
        reliability=("pg_throw_rel_event", lambda x: float((x >= 0).mean())),      # share of shots at or above the field's expectation
        avg_make=("pg_throw_rel_event", lambda x: float(x[x >= 0].mean()) if (x >= 0).any() else 0.0),   # how good when above
        avg_miss=("pg_throw_rel_event", lambda x: float(x[x < 0].mean()) if (x < 0).any() else 0.0),     # how bad when below
        big_misses=("pg_throw_rel_event", lambda x: int((x < -0.5).sum())),
        big_makes=("pg_throw_rel_event", lambda x: int((x > 0.5).sum())),
        worst5=("pg_throw_rel_event", lambda x: x.nsmallest(5).sum()),
        pg_throw_rel_slot=("pg_throw_rel_slot", "mean"),
        pg_total=("pg", "sum"), pg_throw_total=("pg_throw", "sum"),
        pg_wp=("pg_wp", "mean"), pg_call_wp=("pg_call_wp", "mean"), pg_throw_wp=("pg_throw_wp", "mean"),
        # the same tail in win probability: execution relative to the event's field, in percentage points
        pg_throw_rel_event_wp=("pg_throw_rel_event_wp", "mean"),
        floor10_wp=("pg_throw_rel_event_wp", lambda x: float(x.quantile(0.10))),
        big_misses_wp=("pg_throw_rel_event_wp", lambda x: int((x < -0.05).sum())),      # shots that cost 5+ points of win probability
        big_makes_wp=("pg_throw_rel_event_wp", lambda x: int((x > 0.05).sum())),        # shots that gained 5+ points
        worst5_wp=("pg_throw_rel_event_wp", lambda x: x.nsmallest(5).sum()),
        best5_wp=("pg_throw_rel_event_wp", lambda x: x.nlargest(5).sum()),
        grade=("grade_pct", "mean"),
    ).reset_index()
    agg = agg[agg["shots"] >= min_shots].rename(columns={"book": "event"})
    # sorted by reliability (how often above the field), then by how bad the misses were
    return agg.sort_values(["event", "discipline", "reliability", "avg_miss"], ascending=[True, True, False, False])


def by_team_event(pg: pd.DataFrame, books: list[str] | None = None) -> pd.DataFrame:
    """One row per (event book, discipline, team): the team-level view in win probability. Record from the
    end scores, and the team's stones' summed effect on its chance of winning (PG in win probability,
    calls and throws together, thrower's view) per game, in percentage points. No execution columns:
    a team's standing is what it did to its chance of winning, not how its stones compared with the field."""
    df = pg if not books else pg[pg["book"].isin(books)]
    # final score of each game from the end results (hammer team's view per end)
    ends = df[df["shot"] == 1].drop_duplicates(["game_key", "end"])[["book", "discipline", "game_key", "hammer_team", "end_score_hammer"]]
    teams = df.groupby("game_key")["team"].agg(lambda s: sorted(set(s)))
    rec: dict[tuple, list] = {}
    for gk, g in ends.groupby("game_key", sort=False):
        ts = teams[gk]
        if len(ts) != 2:
            continue
        score = {t: 0 for t in ts}
        for h, r in zip(g["hammer_team"], g["end_score_hammer"]):
            o = ts[1] if h == ts[0] else ts[0]
            score[h if r > 0 else o] += abs(int(r))
        if score[ts[0]] == score[ts[1]]:
            continue
        w, l = (ts[0], ts[1]) if score[ts[0]] > score[ts[1]] else (ts[1], ts[0])
        b, d = g["book"].iloc[0], g["discipline"].iloc[0]
        rec.setdefault((b, d, w), [0, 0])[0] += 1
        rec.setdefault((b, d, l), [0, 0])[1] += 1
    keys = ["book", "discipline", "team"]
    agg = df.groupby(keys).agg(games=("game_key", "nunique"), shots=("pg", "size"),
                               wp_gain=("pg_wp", "sum"), wp_exec=("pg_throw_wp", "sum")).reset_index()
    agg["wins"] = [rec.get(k, [0, 0])[0] for k in zip(agg["book"], agg["discipline"], agg["team"])]
    agg["losses"] = [rec.get(k, [0, 0])[1] for k in zip(agg["book"], agg["discipline"], agg["team"])]
    agg["wp_gain"] = 100 * agg["wp_gain"] / agg["games"]
    agg["wp_exec"] = 100 * agg["wp_exec"] / agg["games"]
    return agg.rename(columns={"book": "event"}).sort_values(["event", "discipline", "wp_gain"], ascending=[True, True, False])

