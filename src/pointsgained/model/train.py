"""Fit the baseline f and g models (gradient-boosted trees) and report validation (Section 7.5)."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import log_loss
from sklearn.model_selection import GroupKFold

from .features import FEATURE_NAMES
from .value import N_OUT

TRIVIAL_FEATURES = ["rocks_remaining", "next_thrower_has_hammer", "count"]


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
    # Strongly regularised: with ~3k ends per book, anything richer overfits and loses to the
    # trivial model on held-out books (checked on WWCC 2025 and WJCC 2025).
    return HistGradientBoostingClassifier(max_iter=80, learning_rate=0.05, max_leaf_nodes=8,
                                          min_samples_leaf=300, l2_regularization=10.0,
                                          early_stopping=False,
                                          categorical_features=categorical, random_state=seed)


@dataclass
class FittedModels:
    f: HistGradientBoostingClassifier
    g: HistGradientBoostingClassifier
    trivial: HistGradientBoostingClassifier
    f_cols: list[str]
    g_cols: list[str]
    cv_report: dict = field(default_factory=dict)
    folds: list = field(default_factory=list)     # (set of held-out group keys, f model, g model)
    group_key: str = "book"

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


def design_matrices(rows: pd.DataFrame, X: np.ndarray):
    """f uses position features + discipline; g adds the shot type and turn."""
    disc = (rows["discipline"] == "W").astype(float).to_numpy()[:, None]
    fgz = X[:, FEATURE_NAMES.index("fgz_rocks")][:, None]
    X_f = np.hstack([X, disc])
    f_cols = FEATURE_NAMES + ["is_women"]
    turn = rows["turn"].map({"cw": 1.0, "ccw": -1.0, "in": 0.5, "out": -0.5}).fillna(0.0).to_numpy()[:, None]
    stc = rows["shot_type_code"].to_numpy()[:, None].astype(float)
    X_g = np.hstack([X_f, stc, turn])
    g_cols = f_cols + ["shot_type_code", "turn"]
    return X_f, f_cols, X_g, g_cols


def fit_models(rows: pd.DataFrame, X: np.ndarray, y: np.ndarray, seed: int = 0) -> FittedModels:
    X_f, f_cols, X_g, g_cols = design_matrices(rows, X)
    cat_g = [g_cols.index("shot_type_code")]
    tri_idx = [FEATURE_NAMES.index(c) for c in TRIVIAL_FEATURES]
    groups = rows["book"].to_numpy()
    n_groups = len(set(groups))
    report = {"n_rows": int(len(rows)), "n_groups": int(n_groups), "group_key": "book"}
    if n_groups < 3:
        groups = rows["game_key"].to_numpy(); n_groups = len(set(groups)); report["group_key"] = "game_key"
    n_splits = min(5, n_groups)
    folds = GroupKFold(n_splits=n_splits)
    P_f = np.zeros((len(y), N_OUT)); P_g = np.zeros_like(P_f); P_t = np.zeros_like(P_f)
    unm = (rows["mirror"] == 0).to_numpy()
    fold_models = []
    for tr, te in folds.split(X_f, y, groups):
        mf = make_model(seed).fit(X_f[tr], y[tr]); P_f[te] = _full_proba(mf, X_f[te])
        mg = make_model(seed, cat_g).fit(X_g[tr], y[tr]); P_g[te] = _full_proba(mg, X_g[te])
        mt = make_model(seed).fit(X[tr][:, tri_idx], y[tr]); P_t[te] = _full_proba(mt, X[te][:, tri_idx])
        fold_models.append((set(groups[te]), mf, mg))
    eps = 1e-6
    for name, P in (("trivial", P_t), ("f", P_f), ("g", P_g)):
        Pn = np.clip(P[unm], eps, 1); Pn /= Pn.sum(axis=1, keepdims=True)
        report[f"{name}_logloss"] = float(log_loss(y[unm], Pn, labels=list(range(N_OUT))))
        report[f"{name}_brier"] = _brier(Pn, y[unm])
    # calibration of f by class: mean predicted vs observed in deciles of predicted prob
    calib = {}
    for k in range(N_OUT):
        pk = P_f[unm][:, k]; yk = (y[unm] == k).astype(float)
        if yk.sum() < 20:
            continue
        bins = np.quantile(pk, np.linspace(0, 1, 6))
        idx = np.clip(np.searchsorted(bins, pk, side="right") - 1, 0, 4)
        calib[int(k - 3)] = [(round(float(pk[idx == b].mean()), 3), round(float(yk[idx == b].mean()), 3), int((idx == b).sum()))
                             for b in range(5) if (idx == b).any()]
    report["calibration_f"] = calib
    # by rocks_remaining: how log-loss improves as the end progresses
    rr = X[unm][:, FEATURE_NAMES.index("rocks_remaining")]
    by_rr = {}
    for r in sorted(set(rr.astype(int))):
        m = rr == r
        Pn = np.clip(P_f[unm][m], eps, 1); Pn /= Pn.sum(axis=1, keepdims=True)
        Pt = np.clip(P_t[unm][m], eps, 1); Pt /= Pt.sum(axis=1, keepdims=True)
        by_rr[int(r)] = {"n": int(m.sum()),
                         "f": round(float(log_loss(y[unm][m], Pn, labels=list(range(N_OUT)))), 4),
                         "trivial": round(float(log_loss(y[unm][m], Pt, labels=list(range(N_OUT)))), 4)}
    report["logloss_by_rocks_remaining"] = by_rr
    f = make_model(seed).fit(X_f, y)
    g = make_model(seed, cat_g).fit(X_g, y)
    t = make_model(seed).fit(X[:, tri_idx], y)
    return FittedModels(f, g, t, f_cols, g_cols, report, fold_models, report["group_key"])
