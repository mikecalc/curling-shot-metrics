"""The split expectation model: the setup and the endgame, bridged at the end of the free guard zone.

During the free guard zone the rules stop a team from simply playing for points, so the setup is valued
on its own terms. Two pairs of models, both predicting the end's outcome distribution:

- **endgame** (f_L, g_L): positions from the end of the free guard zone on (the pre-shot positions of
  stones fgz+1 to 16), on the full geometry, trained on the end's result;
- **setup** (f_E, g_E): positions during the free guard zone (stones 1 to fgz), on a lean description
  built around rock potential, never trained on the end's result. Its target is the endgame model's
  out-of-fold distribution at the **handover** H, the position after the last free-guard-zone stone:
  the setup is worth what it hands to the endgame.

Every position is valued by exactly one model, so the per-end conservation identity telescopes across
the split: the stone that ends the setup is credited f_L(H) minus g_E(S, C).

A **blend** (`blend=(a, b)`) replaces the hard handover with a gradual one: a position before stone a is
valued by the setup models, one from stone b on by the endgame models, and in between by a mixture of
the two distributions whose setup share falls linearly with the stone number. The endgame models are then
fitted on every position (final results), and the setup models on every position before stone b, taught
by the endgame model at the handover during the free guard zone and at the position itself after it, so
the two agree where they overlap. Each position still has one value, so credit still telescopes.
"""
from __future__ import annotations

import time
import logging
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

from .targets import expand_soft
from .train import _cat_index, _full_proba, design_matrices, make_model
from .value import N_OUT

log = logging.getLogger(__name__)


def blend_weight(rows: pd.DataFrame, blend: tuple[int, int] | None) -> np.ndarray:
    """The setup models' share of a row's valuation: 1 before stone a, 0 from stone b, linear in between;
    without a blend, 1 for setup rows and 0 otherwise."""
    if blend is None:
        return setup_mask(rows).astype(float)
    a, b = blend
    return np.clip((b - rows["shot"].to_numpy()) / max(b - a, 1), 0.0, 1.0)


def setup_mask(rows: pd.DataFrame) -> np.ndarray:
    """True for rows whose pre-shot position is during the free guard zone (stones 1 to fgz)."""
    fgz = rows["fgz_rocks"].to_numpy() if "fgz_rocks" in rows else np.full(len(rows), 5)
    return rows["shot"].to_numpy() <= fgz


def handover_rows(rows: pd.DataFrame) -> np.ndarray:
    """For every row, the index of the row holding its end's handover position (the pre-shot position of
    stone fgz+1, same mirror), or -1 when that row is missing."""
    fgz = rows["fgz_rocks"].to_numpy().astype(int) if "fgz_rocks" in rows else np.full(len(rows), 5)
    key = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["shot"], rows["mirror"]])
    lookup = pd.Series(np.arange(len(rows)), index=key)
    want = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], fgz + 1, rows["mirror"]])
    return lookup.reindex(want).fillna(-1).to_numpy().astype(int)


def teacher_targets(rows: pd.DataFrame, X_fL: np.ndarray, y: np.ndarray, tr: np.ndarray, setup: np.ndarray,
                    seed: int = 0, n_splits: int = 5) -> np.ndarray:
    """Soft targets (n_rows, 7) for the setup rows in `tr`: the endgame model's out-of-fold distribution at
    the row's handover position (f_L fitted on the endgame rows of the other book groups), or the end's
    result where the handover row is missing or outside the training rows."""
    T = np.zeros((len(y), N_OUT))
    T[np.arange(len(y)), y] = 1.0
    late_tr = tr[~setup[tr]]
    P = np.full((len(y), N_OUT), np.nan)
    groups = rows["book"].to_numpy()[late_tr]
    for a, b in GroupKFold(n_splits=min(n_splits, len(set(groups)))).split(late_tr, groups=groups):
        m = make_model(seed).fit(X_fL[late_tr[a]], y[late_tr[a]])
        P[late_tr[b]] = _full_proba(m, X_fL[late_tr[b]])
    early_tr = tr[setup[tr]]
    h = handover_rows(rows)[early_tr]
    ok = h >= 0
    ok[ok] = ~np.isnan(P[h[ok], 0])
    T[early_tr[ok]] = P[h[ok]]
    # rows past the handover that the setup models also learn (the blend's transition): the endgame
    # model's own value of that position
    trans = tr[~setup[tr]]
    ok2 = ~np.isnan(P[trans, 0])
    T[trans[ok2]] = P[trans[ok2]]
    return T


@dataclass
class SplitModels:
    f_E: object
    g_E: object
    f_L: object
    g_L: object
    sets_early: tuple
    sets_late: tuple
    report: dict = field(default_factory=dict)
    blend: tuple | None = None

    def predict(self, rows: pd.DataFrame, X: np.ndarray, idx: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """(D(S), D(S | C)) for rows `idx`: the setup models' and the endgame models' distributions mixed by
        the row's blend weight (0 or 1 for a hard handover)."""
        sub, Xs = rows.iloc[idx], X[idx]
        w = blend_weight(sub, self.blend)
        Pf, Pg = np.zeros((len(idx), N_OUT)), np.zeros((len(idx), N_OUT))
        for mask, share, sets, f, g in ((w > 0, w, self.sets_early, self.f_E, self.g_E),
                                        (w < 1, 1.0 - w, self.sets_late, self.f_L, self.g_L)):
            if mask.any():
                X_f, _, X_g, _ = design_matrices(sub[mask], Xs[mask], sets)
                Pf[mask] += share[mask, None] * _full_proba(f, X_f)
                Pg[mask] += share[mask, None] * _full_proba(g, X_g)
        return Pf, Pg


def fit_split(rows: pd.DataFrame, X: np.ndarray, y: np.ndarray, tr: np.ndarray, sets_early: tuple, sets_late: tuple,
              seed: int = 0, blend: tuple[int, int] | None = None) -> SplitModels:
    """Fit the endgame pair on the endgame training rows (every training row with a blend; final results),
    then the setup pair on the rows it values, with the endgame model's values as targets."""
    t0 = time.time()
    setup = setup_mask(rows)
    X_fL, _, X_gL, g_colsL = design_matrices(rows, X, sets_late)
    late_tr = tr if blend is not None else tr[~setup[tr]]
    early_tr = tr[blend_weight(rows, blend)[tr] > 0] if blend is not None else tr[setup[tr]]
    f_L = make_model(seed).fit(X_fL[late_tr], y[late_tr])
    g_L = make_model(seed, _cat_index(g_colsL)).fit(X_gL[late_tr], y[late_tr])
    log.info("split: endgame models fitted in %.0fs", time.time() - t0)
    T = teacher_targets(rows, X_fL, y, tr, setup, seed)
    idx, cls, w = expand_soft(early_tr, T)
    X_fE, _, X_gE, g_colsE = design_matrices(rows, X, sets_early)
    f_E = make_model(seed).fit(X_fE[idx], cls, sample_weight=w)
    g_E = make_model(seed, _cat_index(g_colsE)).fit(X_gE[idx], cls, sample_weight=w)
    log.info("split: setup models fitted in %.0fs (%d weighted rows from %d)", time.time() - t0, len(idx), len(early_tr))
    return SplitModels(f_E, g_E, f_L, g_L, tuple(sets_early), tuple(sets_late),
                       {"seconds": round(time.time() - t0, 1), "setup_rows": int(len(early_tr)), "endgame_rows": int(len(late_tr))},
                       blend)
