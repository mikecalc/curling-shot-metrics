import numpy as np
import pandas as pd
from pointsgained.model.winprob import build_table, ends_from_line_scores


def synthetic_ends(n_games=400, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for g in range(n_games):
        d = 0; hammer = 1
        for e in range(1, 11):
            o = rng.choice([-2, -1, 0, 1, 2, 3], p=[.03, .12, .10, .40, .30, .05])
            rows.append({"game_key": g, "end": e, "n_ends": 10, "ends_remaining": 11 - e,
                         "diff_hammer": d, "outcome_hammer": int(o)})
            d = -(d + o) if o > 0 else d + o   # hammer switches on a score; diff from new hammer team's view
    return pd.DataFrame(rows)


def test_table_monotone_and_symmetric():
    t = build_table(synthetic_ends())
    assert t.P(0, 10, 1) > 0.5 > t.P(0, 10, 0)
    assert t.P(3, 5, 1) > t.P(0, 5, 1) > t.P(-3, 5, 1)
    assert abs(t.P(0, 8, 1) + t.P(0, 8, 0) - 1.0) < 0.05     # zero-sum, roughly
    assert t.P(2, 1, 0) > 0.75                               # up two, last end, no hammer: strong favourite


def test_v_vector_last_end_tied():
    t = build_table(synthetic_ends())
    v = t.v_vector(0, 1)
    assert v[4] == 1.0 and v[5] == 1.0          # +1 and +2 both win
    assert v[2] == 0.0                           # steal loses
    assert 0 < v[3] < 1                          # blank -> extra end with hammer


def test_ends_from_line_scores():
    ls = pd.DataFrame([
        {"game_key": "g", "team": "A", "lsfe": True, "n_ends": 10, "ends": ["0", "2", "0", "1", "0", "0", "1", "0", "0", "X"], "extra": [], "discipline": "M"},
        {"game_key": "g", "team": "B", "lsfe": False, "n_ends": 10, "ends": ["1", "0", "0", "0", "2", "0", "0", "1", "3", "X"], "extra": [], "discipline": "M"},
    ])
    e = ends_from_line_scores(ls)
    assert len(e) == 9
    assert e.iloc[0]["team_hammer"] == "A" and e.iloc[0]["outcome_hammer"] == -1   # stolen
    assert e.iloc[1]["team_hammer"] == "A" and e.iloc[1]["outcome_hammer"] == 2     # kept hammer after steal
    assert e.iloc[2]["team_hammer"] == "B"                                          # hammer switched after score
