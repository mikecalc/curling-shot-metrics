"""Points Gained per shot (design Sections 2.2-2.5) with the conservation identity.

Both currencies (hammer-adjusted points and win probability) are computed in one pass: V is a
matrix product of the outcome distributions with a per-row v-vector.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .config_features import CONFIG_COLUMNS, config_row
from .dataset import Dataset, situation_table
from .features import position_features, FEATURE_NAMES
from .train import FittedModels
from .value import ValueMapping, N_OUT, clip_outcome
from .winprob import WinProbTable


def point_mass(points_hammer: int) -> np.ndarray:
    d = np.zeros(N_OUT); d[clip_outcome(points_hammer) + 3] = 1.0
    return d


def _point_masses(scores: np.ndarray) -> np.ndarray:
    out = np.zeros((len(scores), N_OUT))
    out[np.arange(len(scores)), np.clip(scores, -3, 3).astype(int) + 3] = 1.0
    return out


def wp_vectors(table: WinProbTable, diff_hammer: np.ndarray, ends_remaining: np.ndarray) -> np.ndarray:
    """(n, 7) matrix of v-vectors, one per row, from the win-probability table."""
    cache = {}
    out = np.zeros((len(diff_hammer), N_OUT))
    for i, (d, n) in enumerate(zip(diff_hammer, ends_remaining)):
        key = (int(d), int(n))
        v = cache.get(key)
        if v is None:
            v = cache[key] = table.v_vector(*key)
        out[i] = v
    return out


def compute_points_gained(ds: Dataset, models: FittedModels, vm: ValueMapping,
                          wp_table: WinProbTable | None = None, skill_reference: np.ndarray | None = None, post_features: pd.DataFrame | None = None) -> pd.DataFrame:
    """One row per real shot with D(S), D(S|C), D(S'), and pg / pg_call / pg_throw (thrower's view)
    in hammer-adjusted points, plus the same in win probability (`_wp` columns) when a table is given.

    With `skill_reference` (one value per row of ds.rows) and a g that takes `skill_thrower`, the
    default call distribution is evaluated at the reference skill (level-comparable) and the
    thrower's own skill gives the `_own` columns: the call's value for the person throwing it."""
    unm_idx = np.flatnonzero((ds.rows["mirror"] == 0).to_numpy())
    rows = ds.rows.iloc[unm_idx].reset_index(drop=True)
    X = ds.X[unm_idx]
    X_f, X_g = models.design(rows, X)
    groups = rows[models.group_key].to_numpy() if models.group_key in rows else None
    D_pre = models.predict_f(X_f, groups)      # out-of-fold: never valued by a model that saw this book
    D_call = models.predict_g(X_g, groups)
    D_call_own = None
    if skill_reference is not None and ({"skill_thrower", "expected_grade"} & set(models.g_cols)):
        D_call_own = D_call
        ref_rows = rows.assign(skill_thrower=np.asarray(skill_reference)[unm_idx])
        _, X_g_ref = models.design(ref_rows, X)
        D_call = models.predict_g(X_g_ref, groups)
    is_last = rows["is_last_shot"].to_numpy(bool)
    end_score = rows["end_score_hammer"].to_numpy(int)
    # post position = next shot's pre position (same end); last shot = the realised outcome
    full_to_unm = np.full(len(ds.rows), -1, dtype=int)
    full_to_unm[unm_idx] = np.arange(len(unm_idx))
    post_row = rows["post_row"].to_numpy(int)
    post_u = np.where(post_row >= 0, full_to_unm[np.maximum(post_row, 0)], -1)
    D_post = D_pre.copy()
    has_next = (post_u >= 0) & ~is_last
    D_post[has_next] = D_pre[post_u[has_next]]
    fallback = np.flatnonzero(~has_next & ~is_last)
    if len(fallback):
        feats, cfg, keep = [], [], []
        has_post = rows["has_post"].to_numpy(bool)
        for i in fallback:
            if not has_post[i]:
                continue                    # no diagram: the post position is carried forward as the pre
            r = rows.iloc[i]
            p = ds.position(r["game_key"], int(r["end"]), int(r["shot"]))
            feats.append(position_features(p)); cfg.append(config_row(p)); keep.append(i)
        if keep:
            # the row carries the pre-shot configuration columns; the rebuilt post position needs its own
            sub = rows.iloc[keep].reset_index(drop=True)
            cols = [c for c in CONFIG_COLUMNS if c in sub]
            if cols:
                sub[cols] = pd.DataFrame(cfg)[cols].to_numpy(dtype=float)
            if post_features is not None:
                # stone and potential columns of the rebuilt post position (keyed by this shot's post position)
                pcols = [c for c in post_features.columns if c in sub]
                if pcols:
                    key = pd.MultiIndex.from_arrays([sub["game_key"], sub["end"], sub["shot"]])
                    sub[pcols] = post_features[pcols].reindex(key).fillna(0.0).to_numpy(dtype=float)
            Xp_f, _ = models.design(sub, np.vstack(feats))
            D_post[keep] = models.predict_f(Xp_f, groups[keep] if groups is not None else None)
    D_post[is_last] = _point_masses(end_score[is_last])
    sign = np.where(rows["thrower_has_hammer"].to_numpy(bool), 1.0, -1.0)
    out = rows[["game_key", "end", "shot", "book", "discipline", "date", "team", "player", "shot_type", "turn",
                "grade_pct", "thrower_has_hammer", "hammer_team", "diff_hammer", "ends_remaining"]].copy()
    currencies = [("", np.broadcast_to(vm.v, D_pre.shape))]
    if wp_table is not None:
        currencies.append(("_wp", wp_vectors(wp_table, rows["diff_hammer"].to_numpy(), rows["ends_remaining"].to_numpy())))
    for suffix, Vm in currencies:
        V_pre, V_call, V_post = (D_pre * Vm).sum(1), (D_call * Vm).sum(1), (D_post * Vm).sum(1)
        out["V_pre" + suffix] = V_pre; out["V_call" + suffix] = V_call; out["V_post" + suffix] = V_post
        out["pg_canonical" + suffix] = V_post - V_pre
        out["pg" + suffix] = sign * (V_post - V_pre)
        out["pg_call" + suffix] = sign * (V_call - V_pre)
        out["pg_throw" + suffix] = sign * (V_post - V_call)
        if D_call_own is not None:
            V_own = (D_call_own * Vm).sum(1)
            out["pg_call_own" + suffix] = sign * (V_own - V_pre)
            out["pg_throw_own" + suffix] = sign * (V_post - V_own)
    out["D_pre"] = list(np.round(D_pre, 4)); out["D_call"] = list(np.round(D_call, 4)); out["D_post"] = list(np.round(D_post, 4))
    if D_call_own is not None:
        out["D_call_own"] = list(np.round(D_call_own, 4))
    out["end_score_hammer"] = end_score
    out["is_last_shot"] = is_last
    out["post_missing"] = ~rows["has_post"].to_numpy(bool) & ~is_last
    return out


def situation_lookup(tabs: dict) -> dict:
    """(game_key, end) -> (diff_hammer, ends_remaining). Kept for callers that index by end."""
    t = situation_table(tabs)
    return {(g, int(e)): (int(d), int(n)) for g, e, d, n in zip(t["game_key"], t["end"], t["diff_hammer"], t["ends_remaining"])}


def conservation_check(pg: pd.DataFrame, vm: ValueMapping, suffix: str = "") -> pd.DataFrame:
    """Per end: sum of canonical PG versus actual - V(D(S0)). Exact by construction."""
    df = pg.sort_values(["game_key", "end", "shot"])
    g = df.groupby(["game_key", "end"], sort=False)
    out = g.agg(sum_pg=("pg_canonical" + suffix, "sum"), first_pre=("V_pre" + suffix, "first"),
                last_post=("V_post" + suffix, "last"), score=("end_score_hammer", "first")).reset_index()
    out["final_minus_start"] = out["last_post"] - out["first_pre"]
    out["residual"] = out["sum_pg"] - out["final_minus_start"]
    out["actual_value"] = [vm.value_of_outcome(int(s)) for s in out["score"]]
    out["terminal_is_actual"] = (out["last_post"] - out["actual_value"]).abs() < 1e-9
    return out.drop(columns=["first_pre", "last_post", "score"])
