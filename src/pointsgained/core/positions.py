"""Position assembly: pre/post positions per shot in the canonical hammer-team frame.

Design Sections 2.4 and 4. Every physical position is expressed once, from the
perspective of the team holding hammer in the end: stones are labelled
'hammer' / 'non_hammer'. A thrower's value is the canonical value times +1 if the
thrower holds hammer, -1 otherwise.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .count import count_position


@dataclass
class Position:
    """Stones as arrays in inches (pin at 0,0; y towards the hog line), owner 1 = hammer team, 0 = non-hammer."""
    x: np.ndarray
    y: np.ndarray
    owner: np.ndarray            # 1 hammer, 0 non-hammer
    rocks_remaining: int         # stones not yet thrown (0-16); the next thrower is non-hammer iff rocks_remaining is even
    fgz_rocks: int = 5

    @property
    def n(self) -> int:
        return len(self.x)

    @property
    def next_thrower_has_hammer(self) -> bool:
        # 16 remaining: non-hammer throws first. Parity alternates.
        return self.rocks_remaining % 2 == 1

    def mirrored(self) -> "Position":
        return Position(-self.x, self.y.copy(), self.owner.copy(), self.rocks_remaining, self.fgz_rocks)

    def score_hammer(self) -> int:
        """Points from the hammer team's perspective (negative = steal)."""
        colour, pts = count_position(zip(np.where(self.owner == 1, "H", "N"), self.x, self.y))
        if colour is None:
            return 0
        return pts if colour == "H" else -pts

    @staticmethod
    def empty(fgz_rocks: int = 5) -> "Position":
        z = np.zeros(0)
        return Position(z, z.copy(), z.astype(int), 16, fgz_rocks)


def fgz_rocks_for(date) -> int:
    """Four-rock free guard zone before the 2018-19 season, five-rock after."""
    if date is None:
        return 5
    return 5 if (date.year > 2018 or (date.year == 2018 and date.month >= 7)) else 4


def build_positions(shots: pd.DataFrame, stones: pd.DataFrame, ends: pd.DataFrame,
                    games: pd.DataFrame) -> pd.DataFrame:
    """One row per shot with the post-shot position (and the pre-shot position from the previous shot).

    Returns a DataFrame keyed by (game_key, end, shot) with columns:
      hammer_team, thrower_has_hammer, rocks_remaining, fgz_rocks,
      post (Position), pre (Position), end_score_hammer (final score of the end, hammer perspective),
      pre_source_shot (the shot whose post position is this shot's pre position; 0 = empty sheet).
    """
    st = stones[stones["kind"] == "stone"]
    colour_of = {}
    for g in games.itertuples(index=False):
        colour_of[(g.game_key, g.team_a)] = g.color_a
        colour_of[(g.game_key, g.team_b)] = g.color_b
    date_of = dict(zip(games["game_key"], games["date"]))
    end_cols = ["hammer", "team_a", "score_end_a", "score_end_b", "conceded"]
    ends_u = ends.drop_duplicates(["game_key", "end"])
    if "conceded" not in ends_u:
        ends_u = ends_u.assign(conceded=False)
    end_info = {(r.game_key, r.end): r for r in ends_u[["game_key", "end"] + end_cols].itertuples(index=False)}
    grouped = {k: (v["color"].to_numpy(), v["x_in"].to_numpy(float), v["y_in"].to_numpy(float))
               for k, v in st.groupby(["game_key", "end", "shot"])}
    has_diagram_col = "has_diagram" in shots
    rows = []
    for (gk, e), grp in shots.sort_values(["game_key", "end", "shot"]).groupby(["game_key", "end"]):
        er = end_info.get((gk, e))
        if er is None:
            continue
        hammer = er.hammer
        if hammer is None or pd.isna(hammer):
            continue
        hammer_colour = colour_of.get((gk, hammer))
        if hammer_colour is None:
            continue
        fgz = fgz_rocks_for(date_of.get(gk))
        prev = Position.empty(fgz)
        prev_shot = 0
        n_shots = len(grp)
        last_shot_no = int(grp["shot"].max())
        # final score of the end from the recorded header (hammer perspective), fallback to reconstruction
        sa, sb = er.score_end_a, er.score_end_b
        conceded = bool(er.conceded) if not pd.isna(er.conceded) else False
        if conceded:
            end_score = None
            sa = sb = None
        if pd.notna(sa) and pd.notna(sb):
            hs = sa if er.team_a == hammer else sb
            ns = sb if er.team_a == hammer else sa
            end_score = int(hs - ns)
        else:
            end_score = None
        shot_nos = grp["shot"].to_numpy()
        teams = grp["team"].to_numpy()
        has_diag = grp["has_diagram"].to_numpy() if has_diagram_col else np.ones(n_shots, dtype=bool)
        for k, team, hd in zip(shot_nos, teams, has_diag):
            k = int(k)
            g2 = grouped.get((gk, e, k))
            if g2 is None or not hd:
                post = None
            else:
                colour, xs, ys = g2
                owner = (colour == hammer_colour).astype(int)
                post = Position(xs, ys, owner, 16 - k, fgz)
            rows.append({
                "game_key": gk, "end": e, "shot": k, "hammer_team": hammer,
                "thrower_has_hammer": team == hammer,
                "rocks_remaining_before": 16 - (k - 1), "rocks_remaining_after": 16 - k,
                "fgz_rocks": fgz, "pre": prev, "post": post, "end_score_hammer": end_score,
                "is_last_shot": k == last_shot_no, "pre_source_shot": prev_shot,
            })
            if post is not None:
                prev = post
                prev_shot = k
        if end_score is None and not conceded and rows and rows[-1]["post"] is not None:
            # reconstruct from the final position
            final = rows[-1]["post"].score_hammer()
            for r in rows[-n_shots:]:
                r["end_score_hammer"] = final
    return pd.DataFrame(rows)
