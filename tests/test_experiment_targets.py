import numpy as np
import pandas as pd

from pointsgained.model import targets as ex


def test_expand_soft_drops_small_mass_and_keeps_weights():
    T = np.array([[0, 0, 0, 1.0, 0, 0, 0], [0.002, 0.1, 0.2, 0.3, 0.398, 0, 0]])
    idx, cls, w = ex.expand_soft(np.array([0, 1]), T)
    assert list(idx) == [0, 1, 1, 1, 1] and list(cls) == [3, 1, 2, 3, 4]
    assert np.allclose(w, [1.0, 0.1, 0.2, 0.3, 0.398])


def test_local_targets_chain(monkeypatch):
    """One end of 12 stones in each of 10 books. Stage-1 predictions are replaced by a marker distribution per
    row, so the target of an early row must be the marker of the row k stones later, and rows that reach the
    end's last stone within k take the end's result."""
    n_books, n_shots = 10, 12
    recs = []
    for b in range(n_books):
        for s in range(1, n_shots + 1):
            recs.append(dict(book=f"b{b}", shot=s, rocks_remaining=17 - s, is_last_shot=s == n_shots))
    rows = pd.DataFrame(recs)
    rows["post_row"] = np.where(rows["is_last_shot"], -1, np.arange(len(rows)) + 1)
    y = np.full(len(rows), 5)
    X_f = np.zeros((len(rows), 1))

    class Marker:
        def fit(self, X, y, sample_weight=None):
            return self

    def fake_proba(model, X):
        return np.full((len(X), 7), 1 / 7)

    monkeypatch.setattr(ex, "make_model", lambda seed=0, cat=None: Marker())
    monkeypatch.setattr(ex, "_full_proba", fake_proba)
    T = ex.local_targets(rows, X_f, y, np.arange(len(rows)), k=2)
    rr = rows["rocks_remaining"].to_numpy()
    early = rr >= ex.LOCAL_MIN_ROCKS
    assert np.allclose(T[early], 1 / 7)                       # moved two stones on: the stage-1 distribution there
    assert np.allclose(T[~early][:, 5], 1.0)                  # late rows keep their one-hot label
    # a 3-stone end: stone 1 (16 left) reaches the last stone before two steps -> the end's result
    rows3 = rows[rows["shot"] <= 3].reset_index(drop=True).assign(is_last_shot=lambda d: d["shot"] == 3)
    rows3["post_row"] = np.where(rows3["is_last_shot"], -1, np.arange(len(rows3)) + 1)
    T3 = ex.local_targets(rows3, np.zeros((len(rows3), 1)), np.full(len(rows3), 2), np.arange(len(rows3)), k=5)
    assert np.allclose(T3[:, 2], 1.0)


def test_phase_steps_reach_the_end_of_the_setup():
    rows = pd.DataFrame({"shot": np.arange(1, 17), "rocks_remaining": 17 - np.arange(1, 17), "fgz_rocks": 5})
    k = ex.phase_steps(rows)
    assert list(k[:5]) == [5, 4, 3, 2, 1]                 # stones 1-5 all reach the position after stone 5
    assert list(k[5:8]) == [2, 2, 2] and (k[8:] == 0).all()
    old = ex.phase_steps(rows.assign(fgz_rocks=4))
    assert list(old[:4]) == [4, 3, 2, 1] and old[4] == 2


def test_local_targets_per_row_steps(monkeypatch):
    """With per-row steps, every setup row lands on the same boundary row (a marker distribution per row)."""
    rows = pd.DataFrame({"book": np.repeat([f"b{i}" for i in range(10)], 16), "shot": np.tile(np.arange(1, 17), 10)})
    rows["rocks_remaining"] = 17 - rows["shot"]
    rows["fgz_rocks"] = 5
    rows["is_last_shot"] = rows["shot"] == 16
    rows["post_row"] = np.where(rows["is_last_shot"], -1, np.arange(len(rows)) + 1)
    y = np.full(len(rows), 3)

    class M:
        def fit(self, X, y, sample_weight=None):
            return self

    def marker(model, X):
        P = np.zeros((len(X), 7))
        P[np.arange(len(X)), (X[:, 0].astype(int) % 7)] = 1.0      # class = shot number mod 7
        return P

    monkeypatch.setattr(ex, "make_model", lambda seed=0, cat=None: M())
    monkeypatch.setattr(ex, "_full_proba", marker)
    X_f = rows[["shot"]].to_numpy(float)
    T = ex.local_targets(rows, X_f, y, np.arange(len(rows)), ex.phase_steps(rows))
    setup = rows["shot"] <= 5
    assert (T[setup.to_numpy()].argmax(1) == 6 % 7).all()          # the row for stone 6: the position after stone 5
    mid = rows["shot"].between(6, 8).to_numpy()
    assert (T[mid].argmax(1) == ((rows["shot"][mid] + 2) % 7)).all()
