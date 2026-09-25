"""Game report: one game shot by shot from the Points Gained table (design Section 10).

The per-shot table is the substrate every leaderboard is built from; this report shows it for one
game so the aggregates can be traced back to the stones that produced them. Two currencies, by
the rule that team-level tables are in win probability and individual tables lead with execution:
the end table is score and win probability only; the players table is execution in hammer-adjusted
points (`PGAA`, points gained above average, the leaderboard measure) with the effect on win
probability beside it; the shots table is situation, shot, execution, effect.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

SHOT_COLS = ["shot", "team", "player", "type", "turn", "grade", "WP before", "PGAA", "call", "WP after", "WP gain"]


def game_file_name(game_key: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", game_key) + ".md"


def _outcome_label(hammer: str, other: str, score: int) -> str:
    if score > 0:
        return f"{hammer} {score}"
    if score < 0:
        return f"{other} steals {-score}"
    return "blank"


def _r(x, nd: int):
    """Round and clear negative zeros, so a tiny loss prints as 0 rather than -0. Numeric columns only."""
    if isinstance(x, pd.DataFrame):
        x = x.copy()
        for c in x.select_dtypes("number").columns:
            x[c] = x[c].round(nd) + 0.0
        return x
    return x.round(nd) + 0.0


def _fmt_stone(r: pd.Series) -> str:
    return f"{r['PGAA']:+.2f} (end {int(r['end'])}, stone {int(r['shot'])})"


def game_report(pg_game: pd.DataFrame, title: str, subtitle: str = "", team_order: tuple[str, str] | None = None) -> str:
    """Markdown report for one game. `pg_game` is that game's rows of the Points Gained table."""
    df = pg_game.sort_values(["end", "shot"]).reset_index(drop=True)
    teams = list(team_order) if team_order else sorted(df["team"].unique())
    if len(teams) != 2:
        raise ValueError(f"expected two teams, found {teams}")
    a, b = teams
    # win probability from the throwing team's view, in percentage points; execution in hammer-adjusted points
    has = (df["team"] == df["hammer_team"]).to_numpy()
    df["WP before"] = 100 * np.where(has, df["V_pre_wp"], 1 - df["V_pre_wp"])
    df["WP after"] = 100 * np.where(has, df["V_post_wp"], 1 - df["V_post_wp"])
    df["WP gain"] = 100 * df["pg_wp"]
    df["PGAA"] = df["pg_throw"]
    df["call"] = df["pg_call"]

    out = [f"# {title}\n"]
    if subtitle:
        out.append(subtitle + "\n")
    out.append(
        "Two currencies, used by the level of the table. Team-level: the end table is the score and each team's chance of "
        "winning the game, in percent, and nothing else. Individual: a player is judged on what they were asked to throw, "
        "so the players and shots tables lead with execution, `PGAA` (points gained above average), the value of the "
        "delivered stone against the field's usual result for that shot type from that position, in hammer-adjusted "
        "points, the currency of the leaderboards. `call` is what the call itself was worth against the field's usual "
        "call from the position, in the same units. The effect on the game sits beside it: `WP before` and `WP after` are "
        "the throwing team's chance of winning, `WP gain` the change, in percentage points. Every value is a difference "
        "of model outputs on the diagrammed positions (design Sections 2, 9 and 10).\n")

    # ---- ends ------------------------------------------------------------------------------
    rows = []
    max_resid = 0.0
    score = {a: 0, b: 0}
    for end, g in df.groupby("end", sort=True):
        h = str(g["hammer_team"].iloc[0])
        o = b if h == a else a
        res = int(g["end_score_hammer"].iloc[0])
        score[h if res > 0 else o] += abs(res)
        wp0 = float(g["WP before"].iloc[0])
        wp1 = float(g["WP after"].iloc[-1])
        if str(g["team"].iloc[0]) != a:
            wp0 = 100 - wp0
        if str(g["team"].iloc[-1]) != a:
            wp1 = 100 - wp1
        # conservation in win probability: one team's gains minus the other's is the end's swing
        gain = g.groupby("team")["WP gain"].sum()
        max_resid = max(max_resid, abs(float(gain.get(a, 0.0) - gain.get(b, 0.0) - (wp1 - wp0))))
        rows.append({
            "end": int(end), "hammer": h, "result": _outcome_label(h, o, res), f"score {a}-{b}": f"{score[a]}-{score[b]}",
            f"WP {a} before": wp0, f"WP {a} after": wp1, f"swing {a}": wp1 - wp0,
        })
    ends = _r(pd.DataFrame(rows), 1)
    out.append("## Ends\n")
    out.append(f"{a}'s chance of winning before the first stone of the end and after the last, and the swing.\n")
    out.append(ends.to_markdown(index=False) + "\n")
    if max_resid > 1e-6:
        out.append(f"Warning: the stones' WP gains do not close the ends (largest residual {max_resid:.2e} points).\n")

    # ---- players ---------------------------------------------------------------------------
    df = df.assign(_pos=((df["shot"] + 1) // 2 + 1) // 2)
    pl = df.groupby(["team", "player"]).agg(
        shots=("PGAA", "size"), grade=("grade_pct", "mean"), PGAA=("PGAA", "sum"),
        **{"WP gain": ("WP gain", "sum")}, position=("_pos", lambda s: int(s.mode().iloc[0])),
    ).reset_index()
    worst = df.loc[df.groupby(["team", "player"])["PGAA"].idxmin(), ["team", "player", "end", "shot", "PGAA"]]
    best = df.loc[df.groupby(["team", "player"])["PGAA"].idxmax(), ["team", "player", "end", "shot", "PGAA"]]
    worst["worst stone"] = worst.apply(_fmt_stone, axis=1)
    best["best stone"] = best.apply(_fmt_stone, axis=1)
    pl = pl.merge(worst[["team", "player", "worst stone"]], on=["team", "player"]).merge(best[["team", "player", "best stone"]], on=["team", "player"])
    pl["team"] = pd.Categorical(pl["team"], teams)
    pl = pl.sort_values(["team", "position"], ascending=[True, False]).drop(columns="position")
    pl["grade"] = _r(pl["grade"], 1)
    pl["PGAA"] = _r(pl["PGAA"], 2)
    pl["WP gain"] = _r(pl["WP gain"], 1)
    pl = pl[["team", "player", "shots", "grade", "PGAA", "worst stone", "best stone", "WP gain"]]
    out.append("## Players\n")
    out.append("Execution over the game: `PGAA` is the sum of what each stone did against the field's usual result for the "
               "call, in hammer-adjusted points, with the worst and best stones by the same measure. The official grade is "
               "the book's percentage. `WP gain` is the sum of the player's stones' effect on the team's chance of winning, "
               "for reference; it includes the calls and weighs the late ends more.\n")
    out.append(pl.to_markdown(index=False) + "\n")

    # ---- swings ----------------------------------------------------------------------------
    sw = df.reindex(df["WP gain"].abs().sort_values(ascending=False).index).head(10)
    sw = sw.rename(columns={"shot_type": "type", "grade_pct": "grade"})
    out.append("## Largest swings\n")
    out.append("The ten stones that moved the chance of winning most, either way.\n")
    sw = sw[["end", "shot", "team", "player", "type", "turn", "grade", "WP before", "WP after", "WP gain", "PGAA"]].copy()
    for c in ("WP before", "WP after", "WP gain"):
        sw[c] = _r(sw[c], 1)
    sw["PGAA"] = _r(sw["PGAA"], 2)
    out.append(sw.to_markdown(index=False) + "\n")

    # ---- shots -----------------------------------------------------------------------------
    out.append("## Shots\n")
    out.append("Per stone: the situation (the end header and `WP before`), the shot (type, turn and the book's grade), "
               "its execution (`PGAA` and `call`, hammer-adjusted points) and its effect (`WP after`, `WP gain`).\n")
    ledger = "pot_h" in df
    if ledger:
        out.append(f"Then the position's **rock potential** after the stone, for each team (`pot {a}`, `pot {b}`): its stones' "
                   "chance of counting or covering a counter when the end is over, from where stones like them sit at that "
                   "stage of the end, with a stone in front of or just behind a counter credited to whichever team the "
                   "counter belongs to. `build` is how much the stone added to its own team's potential, `address` how much "
                   "it took from the other team's. Potential describes the position; it is not a value and does not add up "
                   "to the result. Under each end header: each team's potential after the free guard zone, after stone 12 "
                   "and before the last stone, and the end's peak temperature (both teams' potential together: high in an "
                   "aggressive end, low in a conservative one).\n")
    for end, g in df.groupby("end", sort=True):
        h = str(g["hammer_team"].iloc[0])
        o = b if h == a else a
        res = int(g["end_score_hammer"].iloc[0])
        d = int(g["diff_hammer"].iloc[0])
        lead = "tied" if d == 0 else (f"up {d}" if d > 0 else f"down {-d}")
        n_left = int(g["ends_remaining"].iloc[0])
        out.append(f"### End {int(end)}: {h} hammer, {lead}, {n_left} end{'s' if n_left != 1 else ''} left; result {_outcome_label(h, o, res)}\n")
        cols = list(SHOT_COLS)
        g = g.copy()
        if ledger:
            pa = np.where(g["hammer_team"] == a, g["pot_h"], g["pot_n"])
            pb = np.where(g["hammer_team"] == b, g["pot_h"], g["pot_n"])
            g[f"pot {a}"], g[f"pot {b}"] = pa, pb
            cols += [f"pot {a}", f"pot {b}", "build", "address"]
            fgz = 5 if pd.to_datetime(g["date"].iloc[0]) >= pd.Timestamp("2018-07-01") else 4
            def at(k):
                r = g[g["shot"] == k]
                return f"{a} {r[f'pot {a}'].iloc[0]:.2f}, {b} {r[f'pot {b}'].iloc[0]:.2f}" if len(r) and r[f"pot {a}"].notna().iloc[0] else "n/a"
            last = int(g["shot"].max())
            peak = (g[f"pot {a}"] + g[f"pot {b}"]).max()
            out.append(f"Potential after the free guard zone: {at(fgz)}; after stone 12: {at(12)}; before the last stone: "
                       f"{at(last - 1)}. Peak temperature {peak:.2f}.\n")
        t = g.rename(columns={"shot_type": "type", "grade_pct": "grade"})[cols].copy()
        t["shot"] = t["shot"].astype(int)
        for c in ("WP before", "WP after", "WP gain"):
            t[c] = _r(t[c], 1)
        for c in ("PGAA", "call"):
            t[c] = _r(t[c], 2)
        if ledger:
            for c in (f"pot {a}", f"pot {b}", "build", "address"):
                t[c] = _r(t[c], 2)
        out.append(t.to_markdown(index=False) + "\n")
    return "\n".join(out)
