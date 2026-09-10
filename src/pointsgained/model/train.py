"""Fit the baseline f and g models (gradient-boosted trees) and report validation (Section 7.5).

Feature sets (design Sections 5.4, 7.2, 13) are named so that experiments can toggle them:
  base       the 28 position features plus discipline (f and g)
  situation  score difference and ends remaining, hammer perspective (f and g)
  call       shot type and turn (g only, always on)
  level      thrower skill and event effect (g only)
  intent     target of the called shot from the delivered stone (g only)
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import log_loss
from sklearn.model_selection import GroupKFold

from .features import FEATURE_NAMES
from .value import N_OUT

log = logging.getLogger(__name__)

TRIVIAL_FEATURES = ["rocks_remaining", "next_thrower_has_hammer", "count"]
TURN_CODE = {"cw": 1.0, "ccw": -1.0, "in": 0.5, "out": -0.5}

FEATURE_SETS = {
    "base": FEATURE_NAMES + ["is_women"],
    "situation": ["diff_hammer_clip", "ends_remaining_clip", "is_extra_end"],
    "call": ["shot_type_code", "turn_code"],
    "level": ["expected_grade"],                         # the difficulty model's expected grade at the thrower's skill
    "level_id": ["skill_thrower", "event_effect"],       # raw per-player / per-book effects (identity proxies; see experiments)
    "intent": ["target_x", "target_y", "target_owner", "target_ring", "target_is_shot_rock", "target_is_guard",
               "shooter_stays", "target_known"],
}
F_SETS = ("base", "situation")                  # sets that enter f (and g)
G_ONLY_SETS = ("call", "level", "level_id", "intent")       # sets that enter g only
CATEGORICAL = {"shot_type_code"}


def column(rows: pd.DataFrame, X: np.ndarray, name: str) -> np.ndarray:
    """One design column, from the baseline features or derived from the row table."""
    if name in FEATURE_NAMES:
        return X[:, FEATURE_NAMES.index(name)]
    if name == "is_women":
        return (rows["discipline"] == "W").to_numpy(dtype=float)
    if name == "diff_hammer_clip":
        return rows["diff_hammer"].clip(-6, 6).to_numpy(dtype=float)
    if name == "ends_remaining_clip":
        return rows["ends_remaining"].clip(1, 10).to_numpy(dtype=float)
    if name == "is_extra_end":
        return rows["is_extra_end"].to_numpy(dtype=float)
    if name == "turn_code":
        return rows["turn"].map(TURN_CODE).fillna(0.0).to_numpy(dtype=float)
    if name == "shot_type_code":
        return rows["shot_type_code"].to_numpy(dtype=float)
    if name == "expected_grade":
        # the difficulty model's expected grade for this shot at the thrower's skill (design 3.5)
        z = rows["grade_logit_base"].to_numpy(dtype=float) + rows["skill_thrower"].to_numpy(dtype=float)
        return 1.0 / (1.0 + np.exp(-z))
    if name in rows:
        return pd.to_numeric(rows[name], errors="coerce").fillna(0.0).to_numpy(dtype=float)
    raise KeyError(f"no builder for design column {name!r}")


def design_columns(sets: tuple[str, ...]) -> tuple[list[str], list[str]]:
    """(f columns, g columns) for the named feature sets. 'base' and 'call' are always present."""
    sets = tuple(dict.fromkeys(("base",) + tuple(sets) + ("call",)))
    f_cols = [c for s in F_SETS if s in sets for c in FEATURE_SETS[s]]
    g_cols = f_cols + [c for s in G_ONLY_SETS if s in sets for c in FEATURE_SETS[s]]
    return f_cols, g_cols


def design_matrices(rows: pd.DataFrame, X: np.ndarray, sets: tuple[str, ...] = ("base",)):
    """f uses position features + discipline (+ situation); g adds the call (+ level, intent)."""
    f_cols, g_cols = design_columns(sets)
    X_f = np.column_stack([column(rows, X, c) for c in f_cols]) if len(rows) else np.zeros((0, len(f_cols)))
    extra = [column(rows, X, c) for c in g_cols[len(f_cols):]]
    X_g = np.column_stack([X_f] + extra) if extra else X_f
    return X_f, f_cols, X_g, g_cols


def _full_proba(model, X) -> np.ndarray:
    """Probabilities over all 7 classes even if some were absent in training."""
    p = model.predict_proba(X)
    out = np.zeros((len(X), N_OUT))
    out[:, model.classes_.astype(int)] = p
    return out


def _brier(P, y):
    Y = np.zeros_like(P); Y[np.arange(len(y)), y] = 1
    return float(np.mean(np.sum((P - Y) ** 2, axis=1)))


def make_model(seed: int = 0, categorical=None):
    # Regularised. On four books anything richer than 8 leaves / 80 rounds overfit; on the full
    # archive (1.2M rows) 15 leaves / 200 rounds is the plateau: 31 leaves / 300 rounds scores the
    # same at 25x the cost and 63 leaves is worse (15 held-out books, 2026-09-09).
    return HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, max_leaf_nodes=15,
                                          min_samples_leaf=300, l2_regularization=10.0,
                                          early_stopping=False,
                                          categorical_features=categorical, random_state=seed)


def _cat_index(cols: list[str]):
    idx = [i for i, c in enumerate(cols) if c in CATEGORICAL]
    return idx or None


@dataclass
class FittedModels:
    f: HistGradientBoostingClassifier
    g: HistGradientBoostingClassifier
    trivial: HistGradientBoostingClassifier
    f_cols: list[str]
    g_cols: list[str]
    sets: tuple[str, ...] = ("base",)
    cv_report: dict = field(default_factory=dict)
    folds: list = field(default_factory=list)     # (set of held-out group keys, f model, g model)
    group_key: str = "book"

    def design(self, rows: pd.DataFrame, X: np.ndarray):
        X_f, _, X_g, _ = design_matrices(rows, X, self.sets)
        return X_f, X_g

    def predict_f(self, X_f: np.ndarray, groups=None) -> np.ndarray:
        return self._predict("f", X_f, groups)

    def predict_g(self, X_g: np.ndarray, groups=None) -> np.ndarray:
        return self._predict("g", X_g, groups)

    def _predict(self, kind: str, X: np.ndarray, groups) -> np.ndarray:
        """Out-of-fold prediction when `groups` is given (rows whose group was held out use that
        fold's model); the full-data model otherwise."""
        full = _full_proba(self.f if kind == "f" else self.g, X)
        if groups is None or not self.folds:
            return full
        groups = np.asarray(groups)
        out = full.copy()
        for held, mf, mg in self.folds:
            m = np.isin(groups, list(held))
            if m.any():
                out[m] = _full_proba(mf if kind == "f" else mg, X[m])
        return out


def _scores(P: np.ndarray, y: np.ndarray, eps: float = 1e-6) -> tuple[float, float]:
    Pn = np.clip(P, eps, 1); Pn /= Pn.sum(axis=1, keepdims=True)
    return float(log_loss(y, Pn, labels=list(range(N_OUT)))), _brier(Pn, y)


def evaluate(P: dict[str, np.ndarray], y: np.ndarray, rows: pd.DataFrame, X: np.ndarray) -> dict:
    """Log-loss and Brier per model, overall, by rocks remaining, by |score diff| and by tier when present."""
    rep = {}
    for name, Pm in P.items():
        ll, br = _scores(Pm, y)
        rep[f"{name}_logloss"], rep[f"{name}_brier"] = ll, br
    rr = X[:, FEATURE_NAMES.index("rocks_remaining")].astype(int)
    by_rr = {}
    for r in sorted(set(rr)):
        m = rr == r
        by_rr[int(r)] = {"n": int(m.sum()), **{name: round(_scores(Pm[m], y[m])[0], 4) for name, Pm in P.items()}}
    rep["logloss_by_rocks_remaining"] = by_rr
    if "diff_hammer" in rows:
        ad = rows["diff_hammer"].abs().clip(upper=4).to_numpy()
        by_d = {}
        for d in sorted(set(ad)):
            m = ad == d
            by_d[int(d)] = {"n": int(m.sum()), **{name: round(_scores(Pm[m], y[m])[0], 4) for name, Pm in P.items()}}
        rep["logloss_by_abs_diff"] = by_d
    if "tier" in rows and rows["tier"].notna().any():
        by_t = {}
        for t, m in rows.groupby("tier").indices.items():
            by_t[str(t)] = {"n": int(len(m)), **{name: round(_scores(Pm[m], y[m])[0], 4) for name, Pm in P.items()}}
        rep["logloss_by_tier"] = by_t
    # calibration of f by class: mean predicted vs observed in quintiles of predicted prob
    if "f" in P:
        calib = {}
        for k in range(N_OUT):
            pk = P["f"][:, k]; yk = (y == k).astype(float)
            if yk.sum() < 20:
                continue
            bins = np.quantile(pk, np.linspace(0, 1, 6))
            idx = np.clip(np.searchsorted(bins, pk, side="right") - 1, 0, 4)
            calib[int(k - 3)] = [(round(float(pk[idx == b].mean()), 3), round(float(yk[idx == b].mean()), 3), int((idx == b).sum()))
                                 for b in range(5) if (idx == b).any()]
        rep["calibration_f"] = calib
    return rep


def fit_models(rows: pd.DataFrame, X: np.ndarray, y: np.ndarray, seed: int = 0,
               sets: tuple[str, ...] = ("base",), n_splits: int = 5) -> FittedModels:
    t0 = time.time()
    X_f, f_cols, X_g, g_cols = design_matrices(rows, X, sets)
    cat_g = _cat_index(g_cols)
    tri_cols = TRIVIAL_FEATURES + (FEATURE_SETS["situation"] if "situation" in sets else [])
    X_t = np.column_stack([column(rows, X, c) for c in tri_cols])
    groups = rows["book"].to_numpy()
    n_groups = len(set(groups))
    report = {"n_rows": int(len(rows)), "n_groups": int(n_groups), "group_key": "book", "sets": list(sets),
              "f_cols": f_cols, "g_cols": g_cols}
    if n_groups < 3:
        groups = rows["game_key"].to_numpy(); n_groups = len(set(groups)); report["group_key"] = "game_key"
    n_splits = min(n_splits, n_groups)
    folds = GroupKFold(n_splits=n_splits)
    P_f = np.zeros((len(y), N_OUT)); P_g = np.zeros_like(P_f); P_t = np.zeros_like(P_f)
    unm = (rows["mirror"] == 0).to_numpy()
    fold_models = []
    for k, (tr, te) in enumerate(folds.split(X_f, y, groups)):
        t1 = time.time()
        mf = make_model(seed).fit(X_f[tr], y[tr]); P_f[te] = _full_proba(mf, X_f[te])
        mg = make_model(seed, cat_g).fit(X_g[tr], y[tr]); P_g[te] = _full_proba(mg, X_g[te])
        mt = make_model(seed).fit(X_t[tr], y[tr]); P_t[te] = _full_proba(mt, X_t[te])
        fold_models.append((set(groups[te]), mf, mg))
        log.info("fold %d/%d fitted in %.0fs", k + 1, n_splits, time.time() - t1)
    report.update(evaluate({"trivial": P_t[unm], "f": P_f[unm], "g": P_g[unm]}, y[unm], rows[unm], X[unm]))
    t1 = time.time()
    f = make_model(seed).fit(X_f, y)
    g = make_model(seed, cat_g).fit(X_g, y)
    t = make_model(seed).fit(X_t, y)
    log.info("full-data models fitted in %.0fs (total %.0fs)", time.time() - t1, time.time() - t0)
    report["fit_seconds"] = round(time.time() - t0, 1)
    return FittedModels(f, g, t, f_cols, g_cols, tuple(sets), report, fold_models, report["group_key"])
