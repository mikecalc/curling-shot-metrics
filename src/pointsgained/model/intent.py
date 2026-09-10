"""Intent from the delivered stone (design Sections 6 and 11).

Per shot, the realised target in the canonical (hammer) frame:
  draw family (Draw, Guard, Front, Freeze, Through): where the delivered stone came to rest;
  hit family (Take-out, Hit and Roll, Double, Clearing, Raise, Promotion, Wick): the first struck
  stone, taken as the prior-position ring furthest up the sheet (the shooter arrives from the hog
  line), with its owner, ring, whether it was the shot rock or a guard in the pre-position, and
  whether the shooter stayed in play.

When the marker or the rings are missing the target is unknown (`target_known` = 0) and the
columns are zero; the target model fills those with the modal target for (type, position).
Columns are mirrored with the position (x -> -x) for mirrored rows.
"""
from __future__ import annotations

import logging
import time

import numpy as np
import pandas as pd

from ..core.geometry import RING_12_RADIUS, STONE_RADIUS, ring_of

log = logging.getLogger(__name__)

DRAW_TYPES = {"Draw", "Guard", "Front", "Freeze", "Through"}
HIT_TYPES = {"Take-out", "Hit and Roll", "Double Take-out", "Clearing", "Raise", "Promotion Take-out", "Wick / Soft Peeling"}
RING_CODE = {"button": 0, "4ft": 1, "8ft": 2, "12ft": 3, "out": 4}
INTENT_COLS = ["target_x", "target_y", "target_owner", "target_ring", "target_is_shot_rock", "target_is_guard",
               "shooter_stays", "target_known"]


def _hammer_colour(tabs: dict) -> pd.DataFrame:
    games = tabs["games"].drop_duplicates("game_key")[["game_key", "team_a", "team_b", "color_a", "color_b"]]
    ends = tabs["ends"].drop_duplicates(["game_key", "end"])[["game_key", "end", "hammer"]]
    e = ends.merge(games, on="game_key", how="inner")
    e = e[e["hammer"].notna()]
    e["hammer_colour"] = np.where(e["hammer"] == e["team_a"], e["color_a"], e["color_b"])
    return e[["game_key", "end", "hammer_colour"]]


def canonical_stones_full(tabs: dict) -> pd.DataFrame:
    """Every stone and prior ring with owner (1 = hammer team) and the delivered flag."""
    st = tabs["stones"][["game_key", "end", "shot", "kind", "color", "x_in", "y_in", "delivered"]]
    st = st.merge(_hammer_colour(tabs), on=["game_key", "end"], how="inner")
    st["owner"] = (st["color"] == st["hammer_colour"]).astype(int)
    return st.drop(columns=["hammer_colour"])


def realised_intent(tabs: dict) -> pd.DataFrame:
    """One row per shot with INTENT_COLS in the canonical frame (unmirrored)."""
    t0 = time.time()
    st = canonical_stones_full(tabs)
    shots = tabs["shots"].drop_duplicates(["game_key", "end", "shot"])[["game_key", "end", "shot", "shot_type", "team", "color"]]
    shots = shots.merge(_hammer_colour(tabs), on=["game_key", "end"], how="inner")
    shots["thrower_owner"] = (shots["color"] == shots["hammer_colour"]).astype(int)
    stones = st[st["kind"] == "stone"]
    priors = st[st["kind"] == "prior"]
    # delivered stone rest per shot
    dl = stones[stones["delivered"] == True].groupby(["game_key", "end", "shot"]).first()[["x_in", "y_in"]].rename(columns={"x_in": "dx", "y_in": "dy"})
    # first struck stone: the prior ring furthest up the sheet (largest y)
    pr = priors.sort_values("y_in", ascending=False).groupby(["game_key", "end", "shot"]).first()[["x_in", "y_in", "owner"]].rename(columns={"x_in": "px", "y_in": "py", "owner": "powner"})
    n_pr = priors.groupby(["game_key", "end", "shot"]).size().rename("n_priors")
    df = shots.set_index(["game_key", "end", "shot"]).join(dl).join(pr).join(n_pr).reset_index()
    df["n_priors"] = df["n_priors"].fillna(0).astype(int)
    # pre-position of each shot: the stones after the previous shot with a diagram in the same end
    pre_stones = stones[["game_key", "end", "shot", "x_in", "y_in", "owner"]].copy()
    pre_stones["shot"] = pre_stones["shot"] + 1                      # post of shot k is pre of shot k+1
    # (a missing diagram at k means pre(k+1) = pre(k); handled by carrying forward below)
    is_hit = df["shot_type"].isin(HIT_TYPES).to_numpy()
    is_draw = df["shot_type"].isin(DRAW_TYPES).to_numpy()
    out = pd.DataFrame({"game_key": df["game_key"], "end": df["end"], "shot": df["shot"]})
    tx = np.where(is_hit, df["px"], df["dx"]).astype(float)
    ty = np.where(is_hit, df["py"], df["dy"]).astype(float)
    known = np.where(is_hit, df["px"].notna() & (df["n_priors"] > 0), is_draw & df["dx"].notna())
    tx, ty = np.where(known, tx, 0.0), np.where(known, ty, 0.0)
    owner = np.where(is_hit & known, np.where(df["powner"] == 1, 1.0, -1.0), 0.0)
    ring = np.array([RING_CODE[ring_of(x, y)] if k else RING_CODE["out"] for x, y, k in zip(tx, ty, known)], dtype=float)
    d = np.hypot(tx, ty)
    is_guard = (known & is_hit & (d > RING_12_RADIUS + STONE_RADIUS) & (ty > 0)).astype(float)
    shooter_stays = (df["dx"].notna()).astype(float)
    # shot rock in the pre-position: nearest pre stone to the struck position is the pre position's closest stone to the pin
    pre_min = pre_stones.assign(d=np.hypot(pre_stones["x_in"], pre_stones["y_in"])).groupby(["game_key", "end", "shot"])["d"].min()
    pm = pre_min.reindex(pd.MultiIndex.from_arrays([df["game_key"], df["end"], df["shot"]])).to_numpy()
    is_shot_rock = (known & is_hit & (np.abs(d - np.nan_to_num(pm, nan=1e9)) < 2.0 * STONE_RADIUS)).astype(float)
    out["target_x"], out["target_y"] = tx, ty
    out["target_owner"], out["target_ring"] = owner, ring
    out["target_is_shot_rock"], out["target_is_guard"] = is_shot_rock, is_guard
    out["shooter_stays"], out["target_known"] = shooter_stays, known.astype(float)
    out["family"] = np.where(is_hit, "hit", np.where(is_draw, "draw", "other"))
    log.info("intent: %d shots, target known %.3f (hits %.3f, draws %.3f) in %.0fs", len(out), known.mean(),
             known[is_hit].mean() if is_hit.any() else 0, known[is_draw].mean() if is_draw.any() else 0, time.time() - t0)
    return out


def attach_intent(rows: pd.DataFrame, intent: pd.DataFrame) -> pd.DataFrame:
    """Join the intent columns onto a row table; mirrored rows get x negated."""
    key = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["shot"]])
    it = intent.set_index(["game_key", "end", "shot"])[INTENT_COLS].reindex(key)
    rows = rows.copy()
    for c in INTENT_COLS:
        rows[c] = it[c].fillna(0.0).to_numpy(dtype=float)
    rows.loc[rows["mirror"] == 1, "target_x"] *= -1.0
    return rows
