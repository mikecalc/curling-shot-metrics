"""Points Gained per shot (design Sections 2.2-2.5) with the conservation identity."""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..core.positions import Position
from .dataset import Dataset
from .features import position_features, FEATURE_NAMES
from .train import FittedModels, design_matrices
from .value import ValueMapping, N_OUT, clip_outcome


def point_mass(points_hammer: int) -> np.ndarray:
    d = np.zeros(N_OUT); d[clip_outcome(points_hammer) + 3] = 1.0
    return d


def compute_points_gained(ds: Dataset, models: FittedModels, vm: ValueMapping,
                          vm_by_situation=None) -> pd.DataFrame:
    """One row per real shot with D(S), D(S|C), D(S'), and pg / pg_call / pg_throw (thrower's view).

    vm_by_situation: optional callable (game_key, end) -> ValueMapping (e.g. win probability),
    used instead of vm when given.
    """
    unm = (ds.rows["mirror"] == 0).to_numpy()
    rows = ds.rows[unm].reset_index(drop=True)
    X = ds.X[unm]
    X_f, _, X_g, _ = design_matrices(rows, X)
    groups = rows[models.group_key].to_numpy() if models.group_key in rows else None
    D_pre = models.predict_f(X_f, groups)      # out-of-fold: never valued by a model that saw this book
    D_call = models.predict_g(X_g, groups)
    pos = ds.positions.set_index(["game_key", "end", "shot"])
    keys = list(zip(rows["game_key"], rows["end"], rows["shot"]))
    posr = pos.loc[keys]
    is_last = posr["is_last_shot"].to_numpy(bool)
    end_score = posr["end_score_hammer"].to_numpy()
    posts = posr["post"].tolist()
    is_women = (rows["discipline"] == "W").astype(float).to_numpy()
    # batch the post-position features
    need = [i for i, p in enumerate(posts) if not is_last[i] and p is not None and p.rocks_remaining > 0]
    D_post = D_pre.copy()
    if need:
        Xp = np.vstack([np.hstack([position_features(posts[i]), [is_women[i]]]) for i in need])
        D_post[need] = models.predict_f(Xp, groups[need] if groups is not None else None)
    for i in range(len(rows)):
        if is_last[i] or (posts[i] is not None and posts[i].rocks_remaining == 0):
            D_post[i] = point_mass(int(end_score[i]))
    out = []
    keep = ("game_key", "end", "shot", "book", "discipline", "date", "team", "player",
            "shot_type", "turn", "grade_pct", "thrower_has_hammer", "hammer_team")
    for i, r in enumerate(rows.itertuples(index=False)):
        m = vm_by_situation(r.game_key, r.end) if vm_by_situation else vm
        V_pre, V_call, V_post = m.V(D_pre[i]), m.V(D_call[i]), m.V(D_post[i])
        sign = 1.0 if r.thrower_has_hammer else -1.0
        rec = {k: getattr(r, k) for k in keep}
        rec.update({"V_pre": V_pre, "V_call": V_call, "V_post": V_post,
                    "pg_canonical": V_post - V_pre,
                    "pg": sign * (V_post - V_pre), "pg_call": sign * (V_call - V_pre), "pg_throw": sign * (V_post - V_call),
                    "D_pre": D_pre[i].round(4).tolist(), "D_call": D_call[i].round(4).tolist(), "D_post": np.round(D_post[i], 4).tolist(),
                    "end_score_hammer": int(end_score[i]), "is_last_shot": bool(is_last[i]),
                    "post_missing": posts[i] is None and not is_last[i]})
        out.append(rec)
    return pd.DataFrame(out)


def situation_lookup(tabs: dict) -> dict:
    """(game_key, end) -> (diff_hammer, ends_remaining) from the ends table and line scores."""
    ends, ls = tabs["ends"], tabs.get("line_scores")
    n_ends = {}
    if ls is not None and len(ls):
        n_ends = ls.groupby("game_key")["n_ends"].first().to_dict()
    out = {}
    for r in ends.itertuples(index=False):
        if r.hammer is None or pd.isna(r.score_before_a) or pd.isna(r.score_before_b):
            continue
        diff = int(r.score_before_a - r.score_before_b) if r.hammer == r.team_a else int(r.score_before_b - r.score_before_a)
        total = int(n_ends.get(r.game_key, 10))
        out[(r.game_key, r.end)] = (diff, max(1, total - int(r.end) + 1))
    return out


def conservation_check(pg: pd.DataFrame, vm: ValueMapping) -> pd.DataFrame:
    """Per end: sum of canonical PG versus actual - V(D(S0)). Exact by construction."""
    recs = []
    for (gk, e), grp in pg.groupby(["game_key", "end"]):
        grp = grp.sort_values("shot")
        lhs = float(grp["pg_canonical"].sum())
        rhs = float(grp["V_post"].iloc[-1] - grp["V_pre"].iloc[0])
        actual = vm.value_of_outcome(int(grp["end_score_hammer"].iloc[0]))
        recs.append({"game_key": gk, "end": e, "sum_pg": lhs, "final_minus_start": rhs,
                     "residual": lhs - rhs, "actual_value": actual, "terminal_is_actual": abs(grp["V_post"].iloc[-1] - actual) < 1e-9})
    return pd.DataFrame(recs)
