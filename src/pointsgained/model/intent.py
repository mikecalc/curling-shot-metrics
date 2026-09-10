"""Intent from the delivered stone (design Sections 6 and 11).

Per shot, the realised target in the canonical (hammer) frame:
  draw family (Draw, Guard, Front, Freeze, Through): where the delivered stone came to rest;
  hit family (Take-out, Hit and Roll, Double, Clearing, Raise, Promotion, Wick): the first struck
  stone, taken as the prior-position ring furthest up the sheet (the shooter arrives from the hog
  line), with its owner, ring, whether it was the shot rock or a guard in the pre-position, and
  whether the shooter stayed in play.

Leakage rule. A draw's rest is the intent only when the shot was made (grade >= MADE_GRADE); a
missed draw's rest is the miss, and at the last rock it is the outcome. Using it, or a flag that
says whether it was used, would put execution into the call. So the columns g sees are:
  draws:  the modal target from a **target model** P(target cell | position, call) fitted on made
          draws (out of fold by book) and applied to every draw whatever its grade;
  hits:   the struck stone from the rings at any grade (which stone was hit is intent, not
          outcome), and the target model's modal struck-stone class when there are no rings.
`target_known` and `shooter_stays` are kept in the table for diagnostics and the Phase 2 error
model but are not design columns. Columns are mirrored with the position (x -> -x).
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
MADE_GRADE = 75.0
INTENT_COLS = ["target_x", "target_y", "target_owner", "target_ring", "target_is_shot_rock", "target_is_guard"]
DIAG_COLS = ["shooter_stays", "target_known", "family", "realised_x", "realised_y"]
# draw target cells: lateral (left / centre / right, centre is |x| <= 24 in) x depth band
DRAW_DEPTH_EDGES = [-1e9, -78.0, -24.0, 24.0, 78.0, 140.0, 1e9]     # through, back, button band, top, near guard, far guard
DRAW_DEPTH_CENTRES = [-100.0, -50.0, 0.0, 50.0, 110.0, 170.0]
DRAW_LATERAL_CENTRES = [-40.0, 0.0, 40.0]


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
    shots = tabs["shots"].drop_duplicates(["game_key", "end", "shot"])[["game_key", "end", "shot", "shot_type", "team", "color", "grade_pct"]]
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
    made = (df["grade_pct"].fillna(0).to_numpy(dtype=float) >= MADE_GRADE)
    known = np.where(is_hit, df["px"].notna() & (df["n_priors"] > 0), is_draw & df["dx"].notna() & made)
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
    # diagnostics (never design columns): where the delivered stone actually rested (draws) or the struck stone (hits)
    out["realised_x"] = np.where(is_hit, df["px"], df["dx"]).astype(float)
    out["realised_y"] = np.where(is_hit, df["py"], df["dy"]).astype(float)
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


def draw_cell(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    lat = np.where(x < -24.0, 0, np.where(x > 24.0, 2, 1))
    depth = np.searchsorted(np.asarray(DRAW_DEPTH_EDGES[1:-1]), y, side="right")
    return lat * len(DRAW_DEPTH_CENTRES) + depth


def hit_class(owner: np.ndarray, ring: np.ndarray, is_guard: np.ndarray) -> np.ndarray:
    """Struck-stone descriptor class: owner (own / opp) x ring (0-4) x guard flag."""
    return ((owner > 0).astype(int) * 5 + ring.astype(int)) * 2 + is_guard.astype(int)


def _target_features(rows: pd.DataFrame, X: np.ndarray) -> np.ndarray:
    from .train import column
    cols = ["shot_type_code", "turn_code", "diff_hammer_clip", "ends_remaining_clip"]
    return np.column_stack([X] + [column(rows, X, c) for c in cols])


def apply_target_model(intent: pd.DataFrame, rows: pd.DataFrame, X: np.ndarray, seed: int = 0, n_splits: int = 5) -> pd.DataFrame:
    """Fill the design columns: draws from the modal target cell for every draw; hits without rings
    from the modal struck-stone class. Out of fold by book. `rows`/`X` are the unmirrored cache rows."""
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.model_selection import GroupKFold
    t0 = time.time()
    key = ["game_key", "end", "shot"]
    r = rows[rows["mirror"] == 0].reset_index(drop=True)
    Xu = X[(rows["mirror"] == 0).to_numpy()]
    it = intent.set_index(key).reindex(pd.MultiIndex.from_frame(r[key])).reset_index()
    F = _target_features(r, Xu)
    groups = r["book"].to_numpy()
    out = it.copy()

    def oof_predict(train_mask, apply_mask, labels):
        pred = np.full(len(r), -1)
        if train_mask.sum() < 500:                       # too few to fit: the field's majority class for every row
            if train_mask.any():
                vals, counts = np.unique(labels[train_mask], return_counts=True)
                pred[apply_mask] = vals[np.argmax(counts)]
            return pred
        tr_idx = np.flatnonzero(train_mask)
        ap_idx = np.flatnonzero(apply_mask)
        n_groups = len(set(groups[tr_idx]))
        splits = GroupKFold(n_splits=min(n_splits, n_groups)).split(F[tr_idx], labels[tr_idx], groups[tr_idx]) if n_groups >= 2 else [(np.arange(len(tr_idx)), np.arange(0))]
        held_books = set()
        for tr, te in splits:
            books_te = set(groups[tr_idx][te])
            m = HistGradientBoostingClassifier(max_iter=100, learning_rate=0.1, max_leaf_nodes=15, min_samples_leaf=100,
                                               categorical_features=[F.shape[1] - 4], random_state=seed).fit(F[tr_idx][tr], labels[tr_idx][tr])
            target = ap_idx[np.isin(groups[ap_idx], list(books_te))]
            if len(target):
                pred[target] = m.classes_[np.argmax(m.predict_proba(F[target]), axis=1)]
            held_books |= books_te
        rest = ap_idx[~np.isin(groups[ap_idx], list(held_books))]      # books with no training rows: full model
        if len(rest):
            m = HistGradientBoostingClassifier(max_iter=100, learning_rate=0.1, max_leaf_nodes=15, min_samples_leaf=100,
                                               categorical_features=[F.shape[1] - 4], random_state=seed).fit(F[tr_idx], labels[tr_idx])
            pred[rest] = m.classes_[np.argmax(m.predict_proba(F[rest]), axis=1)]
        return pred

    # draws: modal cell for every draw, trained on made draws with a marker
    is_draw = (it["family"] == "draw").to_numpy()
    known = it["target_known"].to_numpy(dtype=float) == 1.0
    cells = draw_cell(it["realised_x"].to_numpy(dtype=float), it["realised_y"].to_numpy(dtype=float))
    pred = oof_predict(is_draw & known, is_draw, cells)
    ok = is_draw & (pred >= 0)
    lat, depth = pred[ok] // len(DRAW_DEPTH_CENTRES), pred[ok] % len(DRAW_DEPTH_CENTRES)
    out.loc[ok, "target_x"] = np.asarray(DRAW_LATERAL_CENTRES)[lat]
    out.loc[ok, "target_y"] = np.asarray(DRAW_DEPTH_CENTRES)[depth]
    ty = out.loc[ok, "target_y"].to_numpy(); tx = out.loc[ok, "target_x"].to_numpy()
    out.loc[ok, "target_ring"] = [RING_CODE[ring_of(x, y)] for x, y in zip(tx, ty)]
    out.loc[ok, ["target_owner", "target_is_shot_rock", "target_is_guard"]] = 0.0
    out.loc[ok, "target_is_guard"] = (ty > RING_12_RADIUS + STONE_RADIUS).astype(float)
    # hits without rings: modal struck-stone class, trained on hits with rings
    is_hit = (it["family"] == "hit").to_numpy()
    hc = hit_class(it["target_owner"].to_numpy(dtype=float), it["target_ring"].to_numpy(dtype=float), it["target_is_guard"].to_numpy(dtype=float))
    pred = oof_predict(is_hit & known, is_hit & ~known, hc)
    ok = is_hit & ~known & (pred >= 0)
    if ok.any():
        cls_mean = it[is_hit & known].assign(_c=hc[is_hit & known]).groupby("_c")[["target_x", "target_y", "target_is_shot_rock"]].mean()
        c = pred[ok]
        out.loc[ok, "target_owner"] = np.where((c // 2) // 5 == 1, 1.0, -1.0)
        out.loc[ok, "target_ring"] = ((c // 2) % 5).astype(float)
        out.loc[ok, "target_is_guard"] = (c % 2).astype(float)
        m = cls_mean.reindex(c)
        out.loc[ok, "target_x"] = 0.0
        out.loc[ok, "target_y"] = m["target_y"].fillna(0.0).to_numpy()
        out.loc[ok, "target_is_shot_rock"] = m["target_is_shot_rock"].fillna(0.0).to_numpy()
    log.info("target model: draws %d (modal for all), hits filled %d, in %.0fs", int(is_draw.sum()), int(ok.sum()), time.time() - t0)
    return out


def execution_error_summary(intent: pd.DataFrame, rows: pd.DataFrame, skill: np.ndarray | None = None) -> pd.DataFrame:
    """Seed for the Phase 2 error model (design Section 11): for draws with a marker, the delivered
    stone's rest relative to the modal target, by grade, skill tercile and rocks-remaining band.
    Lateral error is |x_rest - x_target| and depth error y_rest - y_target (positive = heavy... towards
    the hog line), in inches. Hits report how often the struck stone matched the modal class."""
    key = ["game_key", "end", "shot"]
    r = rows[rows["mirror"] == 0][key + ["grade_pct"]].copy()
    if skill is not None:
        r["skill_bucket"] = pd.qcut(pd.Series(skill[(rows["mirror"] == 0).to_numpy()]), 3, labels=["low", "mid", "high"]).astype(str).to_numpy()
    else:
        r["skill_bucket"] = "all"
    df = intent.merge(r, on=key, how="inner")
    df["band"] = pd.cut(df["shot"], [0, 4, 8, 12, 16], labels=["1-4", "5-8", "9-12", "13-16"]).astype(str)
    d = df[(df["family"] == "draw") & df["realised_y"].notna() & (df["realised_x"] != 0.0)].copy()
    d["lateral"] = (d["realised_x"] - d["target_x"]).abs()
    d["depth"] = d["realised_y"] - d["target_y"]
    out = d.groupby(["grade_pct", "skill_bucket", "band"], observed=True).agg(
        n=("lateral", "size"), lateral_med=("lateral", "median"), depth_med=("depth", "median"),
        depth_iqr=("depth", lambda s: float(s.quantile(0.75) - s.quantile(0.25)))).reset_index()
    return out.round(1)
