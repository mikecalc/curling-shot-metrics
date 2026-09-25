import numpy as np
import pandas as pd

from pointsgained.model import split as sp
from pointsgained.model.value import HammerAdjustedPoints


def _rows(fgz=5, n_books=10):
    recs = []
    for b in range(n_books):
        for s in range(1, 17):
            recs.append(dict(book=f"b{b}", game_key=f"b{b}|g", end=1, shot=s, mirror=0, fgz_rocks=fgz,
                             rocks_remaining=17 - s))
    return pd.DataFrame(recs)


def test_setup_mask_and_handover_in_both_eras():
    r5, r4 = _rows(5, 1), _rows(4, 1)
    assert list(sp.setup_mask(r5)) == [True] * 5 + [False] * 11
    assert list(sp.setup_mask(r4)) == [True] * 4 + [False] * 12
    h5, h4 = sp.handover_rows(r5), sp.handover_rows(r4)
    assert (h5 == 5).all() and (h4 == 4).all()          # the row of stone 6 (or 5): its pre-shot position is H
    assert (sp.handover_rows(r5[r5["shot"] != 6].reset_index(drop=True))[:5] == -1).all()


def test_teacher_targets_come_from_the_handover(monkeypatch):
    rows = _rows()
    y = np.full(len(rows), 3)

    class M:
        def fit(self, X, y, sample_weight=None):
            return self

    def marker(model, X):                                  # class = shot number mod 7, so the source row is visible
        P = np.zeros((len(X), 7))
        P[np.arange(len(X)), X[:, 0].astype(int) % 7] = 1.0
        return P

    monkeypatch.setattr(sp, "make_model", lambda seed=0, cat=None: M())
    monkeypatch.setattr(sp, "_full_proba", marker)
    X = rows[["shot"]].to_numpy(float)
    T = sp.teacher_targets(rows, X, y, np.arange(len(rows)), sp.setup_mask(rows))
    setup = sp.setup_mask(rows)
    assert (T[setup].argmax(1) == 6 % 7).all()            # every setup row takes the value of the stone-6 row
    late = rows["shot"].to_numpy()[~setup]
    assert (T[~setup].argmax(1) == late % 7).all()        # endgame rows (the blend's transition) take their own value


def test_conservation_across_the_bridge():
    """An end valued by two different models still telescopes: each position is valued once, so the sum of
    per-stone values is the result minus the empty-sheet value, whatever the models say."""
    rng = np.random.default_rng(1)
    v = HammerAdjustedPoints(0.58).v
    D_E = rng.dirichlet(np.ones(7), size=5)                # setup positions (before stones 1-5)
    D_L = rng.dirichlet(np.ones(7), size=11)               # the handover and later (before stones 6-16)
    D_pre = np.vstack([D_E, D_L])
    result = 4                                             # class index: the hammer team scores one
    terminal = np.zeros(7); terminal[result] = 1.0
    D_post = np.vstack([D_pre[1:], terminal])
    pg = (D_post - D_pre) @ v
    assert abs(pg.sum() - (v[result] - D_pre[0] @ v)) < 1e-12
    assert abs(pg[4] - (D_L[0] @ v - D_E[4] @ v)) < 1e-12  # stone 5 is credited the endgame value of H


def test_blend_weight_and_mixture():
    rows = _rows(5, 1)
    w = sp.blend_weight(rows, (3, 9))
    assert list(w[:3]) == [1.0, 1.0, 1.0] and w[8] == 0.0 and 0 < w[5] < 1
    assert np.allclose(np.diff(w[2:9]), -1 / 6)
    assert list(sp.blend_weight(rows, None)) == [1.0] * 5 + [0.0] * 11

    class Const:
        def __init__(self, k):
            self.k = k

        def predict_proba(self, X):
            P = np.zeros((len(X), 7)); P[:, self.k] = 1.0
            return P
        classes_ = np.arange(7)

    X = np.zeros((len(rows), 26))
    rows = rows.assign(discipline="M", diff_hammer=0, ends_remaining=5, is_extra_end=False, shot_type_code=0, turn="cw")
    m = sp.SplitModels(Const(0), Const(0), Const(6), Const(6), ("base",), ("base",), blend=(3, 9))
    Pf, Pg = m.predict(rows, X, np.arange(len(rows)))
    assert np.allclose(Pf.sum(1), 1.0)
    assert np.allclose(Pf[:, 0], w) and np.allclose(Pf[:, 6], 1 - w)
