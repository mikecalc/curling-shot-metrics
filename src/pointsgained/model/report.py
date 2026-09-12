"""Game report: one game shot by shot from the Points Gained table (design Section 10).

The per-shot table is the substrate every leaderboard is built from; this report shows it for one
game so the aggregates can be traced back to the shots that produced them. Values V are in
hammer-adjusted points from the hammer team's view (the canonical frame); the `call`, `throw` and
`total` columns are from the thrower's view, so a good shot is positive for whoever threw it.
Win-probability columns are in percentage points.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

SHOT_COLS = ["shot", "team", "player", "type", "turn", "grade", "V before", "V call", "V after",
             "call", "throw", "total", "throw wp", "total wp"]


def game_file_name(game_key: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", game_key) + ".md"


def _outcome_label(hammer: str, other: str, score: int) -> str:
    if score > 0:
        return f"{hammer} {score}"
    if score < 0:
        return f"{other} steals {-score}"
    return "blank"


def _team_view(values: np.ndarray, hammer_team: np.ndarray, team: str) -> np.ndarray:
    """A hammer-view win probability seen from `team`."""
    return np.where(hammer_team == team, values, 1.0 - values)


def game_report(pg_game: pd.DataFrame, title: str, subtitle: str = "", team_order: tuple[str, str] | None = None) -> str:
    """Markdown report for one game. `pg_game` is that game's rows of the Points Gained table."""
    df = pg_game.sort_values(["end", "shot"]).reset_index(drop=True)
    teams = list(team_order) if team_order else sorted(df["team"].unique())
    if len(teams) != 2:
        raise ValueError(f"expected two teams, found {teams}")
    a, b = teams
    out = [f"# {title}\n"]
    if subtitle:
        out.append(subtitle + "\n")
    out.append(
        "Every value is a difference of model outputs on the diagrammed positions (design Sections 2 and 10). "
        "`V before`, `V call` and `V after` are the hammer team's expected hammer-adjusted points before the shot, "
        "after the call (the field's usual result for this shot type from this position) and after the delivered stone. "
        "`call`, `throw` and `total` are from the thrower's view: `call` = V call - V before, `throw` = V after - V call, "
        "`total` = call + throw, signed so a gain for the thrower's team is positive. The `wp` columns are the same "
        "differences in win probability, in percentage points. Within an end the hammer team's totals minus the "
        "other team's totals sum exactly to the end's result minus `V before` on the first stone.\n")

    # ---- ends ------------------------------------------------------------------------------
    rows = []
    max_resid = 0.0
    # H, the value of holding hammer, recovered from the first end's terminal value: a score of k is
    # worth k - H (hammer passes), a steal of k is worth -k + H and a blank +H (design 9.2)
    g0 = df[df["end"] == df["end"].min()]
    s0, t0 = int(g0["end_score_hammer"].iloc[0]), float(g0["V_post"].iloc[-1])
    H = s0 - t0 if s0 > 0 else t0 - s0
    for end, g in df.groupby("end", sort=True):
        h = str(g["hammer_team"].iloc[0])
        o = b if h == a else a
        score = int(g["end_score_hammer"].iloc[0])
        v0 = float(g["V_pre"].iloc[0])
        v_result = score - H if score > 0 else score + H
        wp0 = float(g["V_pre_wp"].iloc[0])
        wp1 = float(g["V_post_wp"].iloc[-1])
        resid = float(g["pg_canonical"].sum() - (v_result - v0))
        max_resid = max(max_resid, abs(resid))
        sums = {t: g[g["team"] == t] for t in (a, b)}
        rows.append({
            "end": int(end), "hammer": h, "result": _outcome_label(h, o, score), "E[pts] start": round(v0, 2),
            "result (adj)": round(v_result, 2),
            f"{a} call": round(float(sums[a]["pg_call"].sum()), 2), f"{a} throw": round(float(sums[a]["pg_throw"].sum()), 2),
            f"{b} call": round(float(sums[b]["pg_call"].sum()), 2), f"{b} throw": round(float(sums[b]["pg_throw"].sum()), 2),
            f"WP {a} start": round(100 * (wp0 if h == a else 1 - wp0), 1),
            f"WP {a} end": round(100 * (wp1 if h == a else 1 - wp1), 1),
        })
    ends = pd.DataFrame(rows)
    out.append("## Ends\n")
    out.append("`E[pts] start` is the hammer team's expected hammer-adjusted points at the start of the end and "
               f"`result (adj)` the end's result in the same currency (H = {H:.2f}: a score of k is worth k - H because the "
               "hammer passes, a steal of k is -k + H, a blank +H). The call and throw columns are each team's summed values "
               f"over the end (thrower's view); the win-probability columns are {a}'s, before the first stone and after the last.\n")
    out.append(ends.to_markdown(index=False) + "\n")
    out.append(f"Conservation: max |sum of shot values - (result (adj) - E[pts] start)| over ends = {max_resid:.1e}.\n")

    # ---- players ---------------------------------------------------------------------------
    df = df.assign(_pos=((df["shot"] + 1) // 2 + 1) // 2)
    pl = df.groupby(["team", "player"]).agg(
        shots=("pg", "size"), call=("pg_call", "sum"), throw=("pg_throw", "sum"), total=("pg", "sum"),
        **{"throw wp": ("pg_throw_wp", lambda x: 100 * x.sum()), "total wp": ("pg_wp", lambda x: 100 * x.sum())},
        grade=("grade_pct", "mean"), position=("_pos", lambda s: int(s.mode().iloc[0])),
    ).reset_index()
    worst = df.loc[df.groupby(["team", "player"])["pg_throw"].idxmin(), ["team", "player", "end", "shot", "pg_throw"]]
    best = df.loc[df.groupby(["team", "player"])["pg_throw"].idxmax(), ["team", "player", "end", "shot", "pg_throw"]]
    worst["worst throw"] = worst.apply(lambda r: f"{r['pg_throw']:+.2f} (end {int(r['end'])}, stone {int(r['shot'])})", axis=1)
    best["best throw"] = best.apply(lambda r: f"{r['pg_throw']:+.2f} (end {int(r['end'])}, stone {int(r['shot'])})", axis=1)
    pl = pl.merge(worst[["team", "player", "worst throw"]], on=["team", "player"]).merge(best[["team", "player", "best throw"]], on=["team", "player"])
    pl["team"] = pd.Categorical(pl["team"], teams)
    pl = pl.sort_values(["team", "position"], ascending=[True, False]).drop(columns="position")
    out.append("## Players\n")
    out.append("Sums over the game, thrower's view. `throw` is execution: the value of the delivered stone against the field's "
               "usual result for the call. `total` adds the call component. The official grade is the book's percentage.\n")
    out.append(pl.round(2).to_markdown(index=False) + "\n")

    # ---- swings ----------------------------------------------------------------------------
    sw = df.assign(**{"total wp": 100 * df["pg_wp"], "throw wp": 100 * df["pg_throw_wp"]})
    sw = sw.reindex(sw["total wp"].abs().sort_values(ascending=False).index).head(10)
    sw = sw.rename(columns={"shot_type": "type", "grade_pct": "grade", "pg_call": "call", "pg_throw": "throw", "pg": "total"})
    out.append("## Largest swings\n")
    out.append("The ten shots that moved win probability most, either way.\n")
    out.append(sw[["end", "shot", "team", "player", "type", "turn", "grade", "call", "throw", "total", "throw wp", "total wp"]]
               .round(2).to_markdown(index=False) + "\n")

    # ---- shots -----------------------------------------------------------------------------
    out.append("## Shots\n")
    for end, g in df.groupby("end", sort=True):
        h = str(g["hammer_team"].iloc[0])
        o = b if h == a else a
        score = int(g["end_score_hammer"].iloc[0])
        d = int(g["diff_hammer"].iloc[0])
        lead = "tied" if d == 0 else (f"up {d}" if d > 0 else f"down {-d}")
        out.append(f"### End {int(end)}: {h} hammer, {lead}, {int(g['ends_remaining'].iloc[0])} ends left; result {_outcome_label(h, o, score)}\n")
        t = pd.DataFrame({
            "shot": g["shot"].astype(int), "team": g["team"], "player": g["player"], "type": g["shot_type"], "turn": g["turn"],
            "grade": g["grade_pct"], "V before": g["V_pre"], "V call": g["V_call"], "V after": g["V_post"],
            "call": g["pg_call"], "throw": g["pg_throw"], "total": g["pg"],
            "throw wp": 100 * g["pg_throw_wp"], "total wp": 100 * g["pg_wp"],
        })
        out.append(t.round(2).to_markdown(index=False) + "\n")
    return "\n".join(out)
