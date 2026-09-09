"""Validation gates for an extracted book (design Section 3.6.5)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..core.count import count_position
from ..core.geometry import STONE_RADIUS_PX


def validate_book(t) -> dict:
    """Return a dict of gate metrics for a BookTables (or dict of DataFrames)."""
    tabs = t.tables() if hasattr(t, "tables") else t
    shots, stones, ends, games = tabs["shots"], tabs["stones"], tabs["ends"], tabs["games"]
    out = {"book": getattr(t, "book_id", None), "n_games": len(games), "n_ends": len(ends), "n_shots": len(shots),
           "n_stones": int((stones["kind"] == "stone").sum()) if len(stones) else 0}
    if shots.empty:
        return out

    # 1. shot count per end: 16 unless it is the last end of the game
    last_end = ends.groupby("game_key")["end"].transform("max")
    full = ends[ends["end"] < last_end]
    out["ends_not_16_shots"] = int((full["n_shots"] != 16).sum())
    out["ends_missing_diagrams"] = int((ends["n_diagrams"] < ends["n_shots"]).sum())
    out["ends_colour_unresolved"] = int(ends["colour_source"].eq("none").sum())

    # 2. counters: remaining + on sheet + removed == 8 per colour
    s = shots[shots["has_diagram"]].copy()
    for c in ("red", "yellow"):
        s[f"census_{c}"] = s[f"cnt_{c}_remaining"] + s[f"n_{c}"] + s[f"cnt_{c}_removed"]
    out["counter_census_ok_rate"] = float(((s["census_red"] == 8) & (s["census_yellow"] == 8)).mean())
    # remaining counters should decrease by one for the throwing colour
    out["counter_remaining_sum_ok_rate"] = float(
        ((s["cnt_red_remaining"] + s["cnt_yellow_remaining"]) == (16 - s["shot"])).mean())

    # 3. delivered stone colour agrees with thrower colour
    d = s[s["delivered_color"].notna() & s["color"].notna()]
    out["delivered_detected_rate"] = float(s["delivered_color"].notna().mean())
    out["delivered_colour_ok_rate"] = float((d["delivered_color"] == d["color"]).mean()) if len(d) else None

    # 4. score reconstruction on the final position of each end
    st = stones[stones["kind"] == "stone"]
    last_shot = shots.groupby(["game_key", "end"])["shot"].max().rename("last_shot").reset_index()
    fin = st.merge(last_shot, on=["game_key", "end"])
    fin = fin[fin["shot"] == fin["last_shot"]]
    recon = []
    for (gk, e), grp in fin.groupby(["game_key", "end"]):
        col, pts = count_position(zip(grp["color"], grp["x_in"], grp["y_in"]))
        recon.append({"game_key": gk, "end": e, "recon_color": col, "recon_points": pts})
    # ends with no stones at the end are blanks (no rows in fin)
    recon = pd.DataFrame(recon)
    ev = ends.merge(recon, on=["game_key", "end"], how="left")
    ev["recon_points"] = ev["recon_points"].fillna(0).astype(int)
    colour_of = {}
    for _, g in games.iterrows():
        colour_of[(g["game_key"], g["team_a"])] = g["color_a"]
        colour_of[(g["game_key"], g["team_b"])] = g["color_b"]
    def rec_score(row, side):
        c = colour_of.get((row["game_key"], row[f"team_{side}"]))
        return row["recon_points"] if (c is not None and c == row["recon_color"]) else 0
    ev["recon_a"] = ev.apply(lambda r: rec_score(r, "a"), axis=1)
    ev["recon_b"] = ev.apply(lambda r: rec_score(r, "b"), axis=1)
    has = ev["score_end_a"].notna() & ev["score_end_b"].notna()
    if "conceded" in ev:
        has &= ~ev["conceded"].fillna(False).astype(bool)
    ok = has & (ev["recon_a"] == ev["score_end_a"]) & (ev["recon_b"] == ev["score_end_b"])
    out["score_recorded_rate"] = float(has.mean())
    out["score_reconstruction_ok_rate"] = float(ok[has].mean()) if has.any() else None
    out["score_mismatches"] = ev.loc[has & ~ok, ["game_key", "end", "score_end_a", "score_end_b", "recon_a", "recon_b", "page"]].to_dict("records")[:50]

    # 5. hammer alternation: hammer(n+1) = non-scoring team of end n (or unchanged after a blank)
    ev = ev.sort_values(["game_key", "end"])
    viol = 0; checked = 0
    for gk, grp in ev.groupby("game_key"):
        prev = None
        for _, r in grp.iterrows():
            if prev is not None and r["end"] == prev["end"] + 1 and prev["hammer"] and r["hammer"]:
                sa, sb = prev["score_end_a"], prev["score_end_b"]
                if pd.notna(sa) and pd.notna(sb):
                    checked += 1
                    if sa > 0:
                        exp = prev["team_b"]
                    elif sb > 0:
                        exp = prev["team_a"]
                    else:
                        exp = prev["hammer"]
                    if r["hammer"] != exp:
                        viol += 1
            prev = r
    out["hammer_alternation_checked"] = checked
    out["hammer_alternation_violations"] = viol

    # 6. position sanity: no two stones closer than one stone diameter (in px)
    close = 0; pairs = 0
    for _, grp in st.groupby(["game_key", "end", "shot"]):
        if len(grp) < 2:
            continue
        pts = grp[["col", "row"]].to_numpy()
        dmat = np.hypot(pts[:, None, 0] - pts[None, :, 0], pts[:, None, 1] - pts[None, :, 1])
        iu = np.triu_indices(len(pts), 1)
        pairs += len(iu[0])
        close += int((dmat[iu] < 2 * STONE_RADIUS_PX - 2).sum())
    out["stone_pairs_checked"] = pairs
    out["stone_pairs_too_close"] = close
    out["stones_split_from_merged"] = int((st["split_from"] > 1).sum())

    # 7. shot types
    out["unknown_shot_types"] = sorted(set(shots["shot_type"].dropna()) - _known_types())
    out["shots_missing_type"] = int(shots["shot_type"].isna().sum())
    out["shots_missing_grade"] = int(shots["grade_pct"].isna().sum())
    return out


def _known_types():
    from .panel_text import KNOWN_TYPES
    return KNOWN_TYPES
