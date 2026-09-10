"""Difficulty model and team strength on synthetic data: skill ordering recovered, junior keys separate."""
import numpy as np
import pandas as pd

from pointsgained.model.difficulty import fit_difficulty, attach_level, apply_aliases, reference_skill
from pointsgained.model.features import FEATURE_NAMES
from pointsgained.model.strength import fit_bradley_terry, season_of
from pointsgained.model.train import column


def synthetic_rows(n_per_player=400, seed=0):
    rng = np.random.default_rng(seed)
    players = {"A": 1.0, "B": 0.4, "C": -0.2, "D": -0.8}          # true skill (logit units)
    teams = {"A": "CAN", "B": "CAN", "C": "BRA", "D": "BRA"}
    books = {"BK1": 0.3, "BK2": -0.3}                            # ice effect
    recs, X = [], []
    for p, sk in players.items():
        for b, ice in books.items():
            for i in range(n_per_player):
                draw = rng.random() < 0.5
                difficulty = -0.8 if not draw else 0.4          # take-outs harder in this world
                z = 1.0 + difficulty + sk + ice
                grade = rng.choice([0, 25, 50, 75, 100], p=_grade_probs(z))
                recs.append({"game_key": f"{b}|G{i % 20}", "end": 1 + i % 8, "shot": 1 + i % 16, "mirror": 0, "book": b,
                             "discipline": "M", "date": pd.Timestamp("2025-01-15"), "team": teams[p], "player": p,
                             "shot_type": "Draw" if draw else "Take-out", "shot_type_code": 0 if draw else 1, "turn": "cw",
                             "grade_pct": float(grade), "diff_hammer": 0, "ends_remaining": 5, "is_extra_end": False})
                x = np.zeros(len(FEATURE_NAMES)); x[FEATURE_NAMES.index("rocks_remaining")] = 16 - (i % 16)
                X.append(x)
    return pd.DataFrame(recs), np.vstack(X)


def _grade_probs(z):
    p = 1 / (1 + np.exp(-z))
    w = np.array([(1 - p) ** 2, 2 * (1 - p) * p * 0.5, 2 * (1 - p) * p * 0.5, p ** 2 * 0.3, p ** 2 * 0.7])
    return w / w.sum()


def test_difficulty_recovers_skill_order_and_event_effect():
    rows, X = synthetic_rows()
    es = np.where(rows["book"] == "BK1", 100.0, 100.0)
    ts = np.where(rows["book"] == "BK1", 1.0, -1.0)
    res = fit_difficulty(rows, X, es, ts, rows["player"], lam_player=1.0, lam_team=1.0, lam_book=1.0)
    p = res["players"].set_index("player")["skill"]
    assert p["A"] > p["B"] > p["C"] > p["D"]
    e = res["events"].set_index("book")["event_effect"]
    assert e["BK1"] > e["BK2"]
    assert res["shots"]["grade_logit_base"].notna().all() and len(res["shots"]) == len(rows)
    # attached level columns and the expected-grade design column
    lv = attach_level(rows, res["players"], res["events"], rows["player"], res["shots"])
    assert {"skill_thrower", "event_effect", "grade_logit_base"} <= set(lv.columns)
    eg = column(lv, X, "expected_grade")
    assert 0 < eg.min() and eg.max() < 1
    assert eg[lv["player"] == "A"].mean() > eg[lv["player"] == "D"].mean()
    ref = reference_skill(lv, lv["skill_thrower"].to_numpy())
    assert np.allclose(ref, np.median(lv["skill_thrower"]))


def test_aliases_and_junior_team_key():
    aliases = pd.DataFrame([{"discipline": "M", "alias": "SMITH JA", "canonical": "SMITH J", "keep": "yes"},
                            {"discipline": "M", "alias": "KIM S", "canonical": "KIM SH", "keep": "check: several extensions"}])
    keys = pd.Series(["SMITH JA", "KIM S", "OTHER X"])
    out = apply_aliases(keys, pd.Series(["M", "M", "M"]), aliases)
    assert out.tolist() == ["SMITH J", "KIM S", "OTHER X"]
    rows, X = synthetic_rows(n_per_player=100)
    tk = rows["team"] + np.where(rows["book"] == "BK2", "-J", "")
    res = fit_difficulty(rows, X, np.full(len(rows), 100.0), np.zeros(len(rows)), rows["player"], team_key=tk, lam_player=1.0)
    assert set(res["teams"]["key"]) == {"M|CAN", "M|BRA", "M|CAN-J", "M|BRA-J"}


def test_bradley_terry_order():
    rng = np.random.default_rng(1)
    true = {"CAN": 1.5, "SWE": 0.8, "KOR": 0.0, "BRA": -1.5}
    recs = []
    for i in range(600):
        a, b = rng.choice(list(true), 2, replace=False)
        p = 1 / (1 + np.exp(-(true[a] - true[b])))
        recs.append({"game_key": f"G{i}", "book": "B", "discipline": "M", "season": 2024 + (i % 2),
                     "team_a": a, "team_b": b, "score_a": 0, "score_b": 0, "winner": "a" if rng.random() < p else "b"})
    st = fit_bradley_terry(pd.DataFrame(recs))
    m = st.drop_duplicates("nation").set_index("nation")["nation_mean"]
    assert m["CAN"] > m["SWE"] > m["KOR"] > m["BRA"]
    assert list(season_of(["2024-03-01", "2024-11-01"])) == [2023, 2024]
