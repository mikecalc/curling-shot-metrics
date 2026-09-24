"""Training targets for f and g (design Section 7).

  final      every row is labelled with the end's final score (the Phase 1 models)
  local:k    early rows (9 or more rocks remaining) are trained on the value of the position k stones
             later instead: a soft label, the out-of-fold f distribution there (the end's result if the end
             finishes first). Positions are valued more locally, and the noise of everything after them
             is averaged by the model rather than carried in the label.
  phase      the end's structure: the setup (the free guard zone, stones 1-5, or 1-4 before 2018) is
             trained on the value of the position at the end of the setup; the middle game (to stone 8)
             on the value two stones later; the rest on the end's result. Tried and not adopted: it made
             the setup battle less repeatable than local:2 (reports/experiments/frontend_gates.md).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

from .train import _full_proba, make_model
from .value import N_OUT

LOCAL_MIN_ROCKS = 9          # rows with this many rocks remaining or more take the local target
SOFT_MIN_MASS = 0.005        # soft-label classes below this probability are dropped


def phase_steps(rows: pd.DataFrame, middle_k: int = 2) -> np.ndarray:
    """Steps ahead for the phase target: to the end of the setup (the position after stone `fgz_rocks`) for
    setup stones, `middle_k` for the rest of the early rows (9 or more rocks remaining), 0 otherwise."""
    shot = rows["shot"].to_numpy()
    fgz = rows["fgz_rocks"].to_numpy() if "fgz_rocks" in rows else np.full(len(rows), 5)
    early = rows["rocks_remaining"].to_numpy() >= LOCAL_MIN_ROCKS
    return np.where(shot <= fgz, fgz + 1 - shot, np.where(early, middle_k, 0)).astype(int)


def local_targets(rows: pd.DataFrame, X_f: np.ndarray, y: np.ndarray, tr: np.ndarray, k, seed: int = 0) -> np.ndarray:
    """Soft targets (n_rows, 7) for the training rows: one-hot on the end's result, except rows with
    LOCAL_MIN_ROCKS or more rocks remaining, which take the out-of-fold f distribution of the position k
    stones later (k an int or one per row; stage 1: f on final labels, GroupKFold by book within the
    training rows). If the end finishes within k stones the target is its result; if the chain breaks on
    a missing diagram, the last position reached is used."""
    T = np.zeros((len(y), N_OUT))
    T[np.arange(len(y)), y] = 1.0
    P1 = np.zeros_like(T)
    groups = rows["book"].to_numpy()[tr]
    for a, b in GroupKFold(n_splits=5).split(tr, groups=groups):
        m = make_model(seed).fit(X_f[tr[a]], y[tr[a]])
        P1[tr[b]] = _full_proba(m, X_f[tr[b]])
    post = rows["post_row"].to_numpy()
    last = rows["is_last_shot"].to_numpy(dtype=bool)
    rr = rows["rocks_remaining"].to_numpy()
    steps = np.full(len(rows), k) if np.isscalar(k) else np.asarray(k)
    early = tr[(rr[tr] >= LOCAL_MIN_ROCKS) & (steps[tr] > 0)]
    need = steps[early]
    j = early.copy()
    terminal = np.zeros(len(early), dtype=bool)
    moved = np.zeros(len(early), dtype=bool)
    for n in range(int(need.max()) if len(need) else 0):
        active = ~terminal & (need > n)
        terminal |= active & last[j]                 # the end finished at j: its result is the target
        nxt = post[j]
        step = active & ~terminal & (nxt >= 0)
        j = np.where(step, nxt, j)
        moved |= step
    use = moved & ~terminal
    T[early[use]] = P1[j[use]]
    return T


def expand_soft(idx: np.ndarray, T: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(row index, class, weight) for fitting a classifier on soft targets: one weighted copy of a row per
    class with probability at least SOFT_MIN_MASS (one-hot rows stay single)."""
    sub = T[idx]
    r, c = np.nonzero(sub >= SOFT_MIN_MASS)
    return idx[r], c, sub[r, c]


def training_rows(target: str, rows: pd.DataFrame, X_f: np.ndarray, y: np.ndarray, tr: np.ndarray,
                  seed: int = 0) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    """(row index, class, sample weight or None) to fit f and g on the training rows `tr` under `target`."""
    if target == "final":
        return tr, y[tr], None
    if target == "phase":
        k = phase_steps(rows)
    elif target.startswith("local:"):
        k = int(target.split(":")[1])
    else:
        raise ValueError(f"unknown target {target!r}")
    return expand_soft(tr, local_targets(rows, X_f, y, tr, k, seed))
