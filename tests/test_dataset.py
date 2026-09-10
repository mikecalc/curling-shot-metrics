"""Dataset build, situation columns, post-row linkage and the Points Gained identities on a synthetic corpus."""
from datetime import date

import numpy as np
import pandas as pd

from pointsgained.model.dataset import build_dataset, situation_table, FEATURE_NAMES, META_COLS, SITUATION_COLS
from pointsgained.model.pg import compute_points_gained, conservation_check, point_mass
from pointsgained.model.train import FittedModels, design_columns, design_matrices
from pointsgained.model.value import HammerAdjustedPoints, N_OUT
from pointsgained.model.experiment import split_rows


GK = "BOOK|G1"


def synthetic_tabs():
    games = pd.DataFrame([{"game_key": GK, "book": "BOOK", "discipline": "M", "date": date(2025, 3, 1),
                           "team_a": "AAA", "team_b": "BBB", "color_a": "red", "color_b": "yellow", "n_ends": 8}])
    ends = pd.DataFrame([
        {"game_key": GK, "end": 1, "team_a": "AAA", "team_b": "BBB", "hammer": "BBB", "score_before_a": 0, "score_before_b": 0,
         "score_end_a": 0, "score_end_b": 2, "conceded": False},
        {"game_key": GK, "end": 2, "team_a": "AAA", "team_b": "BBB", "hammer": "AAA", "score_before_a": 0, "score_before_b": 2,
         "score_end_a": 1, "score_end_b": 0, "conceded": False},
    ])
    shots, stones = [], []
    for e, hammer in ((1, "BBB"), (2, "AAA")):
        non_hammer = "AAA" if hammer == "BBB" else "BBB"
        for k in range(1, 5):
            team = non_hammer if k % 2 == 1 else hammer
            colour = "red" if team == "AAA" else "yellow"
            shots.append({"game_key": GK, "end": e, "shot": k, "team": team, "color": colour, "player": f"P{k}",
                          "shot_type": "Draw" if k % 2 else "Take-out", "turn": "cw", "grade_pct": 100.0,
                          "has_diagram": k != 2})
            if k == 2:
                continue                                 # no diagram for shot 2: post position missing
            for j in range(k):                           # k stones in play after shot k
                stones.append({"game_key": GK, "end": e, "shot": k, "kind": "stone", "color": "red" if j % 2 == 0 else "yellow",
                               "x_in": 10.0 * j - 5.0, "y_in": 3.0 * j, "delivered": j == k - 1})
    line_scores = pd.DataFrame([
        {"game_key": GK, "team": "AAA", "lsfe": False, "n_ends": 8, "ends": ["0", "1"], "extra": [], "total": 1, "discipline": "M"},
        {"game_key": GK, "team": "BBB", "lsfe": True, "n_ends": 8, "ends": ["2", "0"], "extra": [], "total": 2, "discipline": "M"},
    ])
    return {"games": games, "ends": ends, "shots": pd.DataFrame(shots), "stones": pd.DataFrame(stones),
            "line_scores": line_scores, "pages": pd.DataFrame(), "players": pd.DataFrame()}


class StubModel:
    """A 7-class model whose distribution depends on the position (via the count feature)."""
    classes_ = np.arange(N_OUT)

    def __init__(self, col):
        self.col = col

    def predict_proba(self, X):
        z = np.outer(X[:, self.col], np.linspace(-1, 1, N_OUT)) + np.linspace(0.2, -0.2, N_OUT)
        p = np.exp(z); return p / p.sum(axis=1, keepdims=True)


def stub_models():
    f_cols, g_cols = design_columns(("base",))
    col = f_cols.index("stones_in_play")
    return FittedModels(StubModel(col), StubModel(col), StubModel(col), f_cols, g_cols, ("base",), {}, [], "book")


def test_situation_table():
    t = situation_table(synthetic_tabs()).set_index("end")
    assert t.loc[1, "diff_hammer"] == 0 and t.loc[2, "diff_hammer"] == -2       # hammer AAA is down two before end 2
    assert t.loc[1, "ends_remaining"] == 8 and t.loc[2, "ends_remaining"] == 7
    assert not t["is_extra_end"].any()


def test_build_dataset_rows_and_links():
    ds = build_dataset(synthetic_tabs())
    assert list(ds.rows.columns) == META_COLS + SITUATION_COLS + FEATURE_NAMES
    assert len(ds.rows) == 16 and (ds.rows["mirror"].to_numpy() == np.tile([0, 1], 8)).all()
    u = ds.rows[ds.rows["mirror"] == 0].set_index(["end", "shot"])
    assert u.loc[(1, 1), "label"] == 2 and u.loc[(2, 1), "label"] == 1
    assert u.loc[(2, 3), "diff_hammer"] == -2 and u.loc[(2, 3), "ends_remaining"] == 7
    assert not u.loc[(1, 2), "has_post"] and u.loc[(1, 3), "has_post"]
    assert u.loc[(1, 3), "pre_source_shot"] == 1 and u.loc[(1, 4), "pre_source_shot"] == 3   # shot 2 had no diagram
    # post_row links to the next shot in the same end and mirror; the last shot links nowhere
    full = ds.rows.reset_index()
    r = full[(full["end"] == 1) & (full["shot"] == 1) & (full["mirror"] == 1)].iloc[0]
    nxt = full.loc[int(r["post_row"])]
    assert (nxt["end"], nxt["shot"], nxt["mirror"]) == (1, 2, 1)
    assert (u.loc[(1, 4), "post_row"], u.loc[(2, 4), "post_row"]) == (-1, -1)
    # mirrored features: left and right guards swap, everything else identical
    xa = ds.X[0::2]; xb = ds.X[1::2]
    i_l, i_r = FEATURE_NAMES.index("own_guard_left"), FEATURE_NAMES.index("own_guard_right")
    assert np.allclose(xa[:, i_l], xb[:, i_r])
    keep = [i for i, n in enumerate(FEATURE_NAMES) if "guard_left" not in n and "guard_right" not in n and n != "shot_rock_covered"]
    assert np.allclose(xa[:, keep], xb[:, keep])
    # canonical stones: 1 + 3 + 4 stones per end, owner 1 = hammer team
    assert len(ds.stones) == 16
    s = ds.stones[(ds.stones["end"] == 1) & (ds.stones["shot"] == 1)]
    assert s["owner"].tolist() == [0]        # red = AAA = non-hammer in end 1
    p = ds.position(GK, 2, 3)
    assert p is not None and p.n == 3 and p.rocks_remaining == 13


def test_points_gained_identities():
    ds = build_dataset(synthetic_tabs())
    models = stub_models()
    vm = HammerAdjustedPoints(0.6)
    pg = compute_points_gained(ds, models, vm)
    assert len(pg) == 8
    pg = pg.sort_values(["end", "shot"]).reset_index(drop=True)
    # post distribution of shot k is the pre distribution of shot k+1; the last shot realises the outcome
    for e in (1, 2):
        g = pg[pg["end"] == e].reset_index(drop=True)
        for k in range(3):
            assert np.allclose(g.loc[k, "D_post"], g.loc[k + 1, "D_pre"])
        assert np.allclose(g.loc[3, "D_post"], point_mass(int(g.loc[3, "end_score_hammer"])))
        assert g.loc[3, "V_post"] == vm.value_of_outcome(int(g.loc[3, "end_score_hammer"]))
    # decomposition and perspective
    assert np.allclose(pg["pg_call"] + pg["pg_throw"], pg["pg"])
    sign = np.where(pg["thrower_has_hammer"], 1.0, -1.0)
    assert np.allclose(pg["pg"], sign * pg["pg_canonical"])
    assert pg["post_missing"].tolist() == [False, True, False, False] * 2
    cons = conservation_check(pg, vm)
    assert cons["residual"].abs().max() < 1e-12 and cons["terminal_is_actual"].all()


def test_reference_skill_decomposition():
    ds = build_dataset(synthetic_tabs())
    ds.rows["skill_thrower"] = np.where(ds.rows["team"] == "AAA", 0.8, -0.2)
    ds.rows["grade_logit_base"] = 0.5
    ds.rows["event_effect"] = 0.0
    f_cols, g_cols = design_columns(("level",))
    col = f_cols.index("stones_in_play")
    class SkillModel(StubModel):
        def predict_proba(self, X):                       # outcome shifts with the expected grade (last column)
            z = np.outer(X[:, self.col] + 3 * X[:, -1], np.linspace(-1, 1, N_OUT))
            p = np.exp(z); return p / p.sum(axis=1, keepdims=True)
    models = FittedModels(StubModel(col), SkillModel(g_cols.index("stones_in_play")), StubModel(col), f_cols, g_cols, ("level",), {}, [], "book")
    assert g_cols[-1] == "expected_grade"
    vm = HammerAdjustedPoints(0.6)
    pg = compute_points_gained(ds, models, vm, skill_reference=np.zeros(len(ds.rows)))
    assert {"pg_call_own", "pg_throw_own", "D_call_own"} <= set(pg.columns)
    assert np.allclose(pg["pg_call_own"] + pg["pg_throw_own"], pg["pg"])
    assert not np.allclose(pg["pg_call_own"], pg["pg_call"])       # own skill differs from the reference
    assert np.allclose(pg["pg_call"] + pg["pg_throw"], pg["pg"])


def test_design_columns_and_sets():
    f_cols, g_cols = design_columns(("base",))
    assert f_cols == FEATURE_NAMES + ["is_women"] and g_cols == f_cols + ["shot_type_code", "turn_code"]
    f2, g2 = design_columns(("situation", "level"))
    assert f2 == f_cols + ["diff_hammer_clip", "ends_remaining_clip", "is_extra_end"]
    assert g2[-1:] == ["expected_grade"] and "shot_type_code" in g2
    ds = build_dataset(synthetic_tabs())
    X_f, fc, X_g, gc = design_matrices(ds.rows, ds.X, ("situation",))
    assert X_f.shape == (16, len(fc)) and X_g.shape == (16, len(gc))
    assert set(X_f[:, fc.index("diff_hammer_clip")]) == {0.0, -2.0}


def test_time_split():
    ds = build_dataset(synthetic_tabs())
    tr, te = split_rows(ds.rows, "time", cutoff_year=2024)
    assert len(tr) == 0 and len(te) == 16
    tr, te = split_rows(ds.rows, "time", cutoff_year=2025)
    assert len(tr) == 16 and len(te) == 0
