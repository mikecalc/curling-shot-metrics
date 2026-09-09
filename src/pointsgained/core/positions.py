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
      post (Position), pre (Position), end_score_hammer (final score of the end, hammer perspective)
    """
    st = stones[stones["kind"] == "stone"]
    colour_of = {}
    for _, g in games.iterrows():
        colour_of[(g["game_key"], g["team_a"])] = g["color_a"]
        colour_of[(g["game_key"], g["team_b"])] = g["color_b"]
    end_info = ends.drop_duplicates(["game_key", "end"]).set_index(["game_key", "end"])
    grouped = {k: v for k, v in st.groupby(["game_key", "end", "shot"])}
    rows = []
    for (gk, e), grp in shots.sort_values(["game_key", "end", "shot"]).groupby(["game_key", "end"]):
        try:
            er = end_info.loc[(gk, e)]
        except KeyError:
            continue
        hammer = er["hammer"]
        if hammer is None or pd.isna(hammer):
            continue
        hammer_colour = colour_of.get((gk, hammer))
        if hammer_colour is None:
            continue
        date = games.loc[games["game_key"] == gk, "date"].iloc[0]
        fgz = fgz_rocks_for(date)
        prev = Position.empty(fgz)
        n_shots = len(grp)
        last_shot_no = int(grp["shot"].max())
        # final score of the end from the recorded header (hammer perspective), fallback to reconstruction
        sa, sb = er.get("score_end_a"), er.get("score_end_b")
        conceded = bool(er.get("conceded", False)) if "conceded" in er else False
        if conceded:
            end_score = None
            sa = sb = None
        if pd.notna(sa) and pd.notna(sb):
            hs = sa if er["team_a"] == hammer else sb
            ns = sb if er["team_a"] == hammer else sa
            end_score = int(hs - ns)
        else:
            end_score = None
        for _, srow in grp.iterrows():
            k = int(srow["shot"])
            g2 = grouped.get((gk, e, k))
            if g2 is None or not srow.get("has_diagram", True):
                post = None
            else:
                owner = (g2["color"].values == hammer_colour).astype(int)
                post = Position(g2["x_in"].to_numpy(float), g2["y_in"].to_numpy(float), owner, 16 - k, fgz)
            rows.append({
                "game_key": gk, "end": e, "shot": k, "hammer_team": hammer,
                "thrower_has_hammer": srow["team"] == hammer,
                "rocks_remaining_before": 16 - (k - 1), "rocks_remaining_after": 16 - k,
                "fgz_rocks": fgz, "pre": prev, "post": post, "end_score_hammer": end_score,
                "is_last_shot": k == last_shot_no,
            })
            if post is not None:
                prev = post
        if end_score is None and not conceded and rows and rows[-1]["post"] is not None:
            # reconstruct from the final position
            final = rows[-1]["post"].score_hammer()
            for r in rows[-n_shots:]:
                r["end_score_hammer"] = final
    return pd.DataFrame(rows)
