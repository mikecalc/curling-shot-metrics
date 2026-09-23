import numpy as np
import pandas as pd

from pointsgained.core.configurations import LABELS
from pointsgained.model.frontend import calibration, next_stone, opponent_same_game, probe_table, split_half


def _frame(n_games=30, seesaw=True, seed=0):
    """Games of one end, four stones (leads only), teams A (odd stones) and B (even stones). With `seesaw`,
    each stone's execution carries the negative of the previous stone's pricing error, as a mispriced
    position does; grades are independent noise."""
    rng = np.random.default_rng(seed)
    rows = []
    for g in range(n_games):
        err_prev = 0.0
        for shot in range(1, 5):
            err = rng.normal(0, 0.05)
            rel = err - (err_prev if seesaw else 0.0) + rng.normal(0, 0.01)
            err_prev = err
            team = "A" if shot % 2 else "B"
            rows.append(dict(game_key=f"g{g}", end=1, shot=shot, team=team, book="b",
                             player_key=f"{team}_lead", rel=rel, grade_pct=float(rng.integers(50, 101)),
                             V_pre=0.5, V_post=0.5 + rel, real_v=0.5, V_pre_wp=0.6, real_wp=0.6))
    df = pd.DataFrame(rows)
    for k in LABELS:
        df["pre_" + k] = False
    df["pre_empty"] = df["shot"] == 1
    return df


def test_next_stone_detects_the_seesaw():
    ns = next_stone(_frame(200)).set_index("shot")["next_stone"]
    assert (ns < -0.4).all()
    flat = next_stone(_frame(200, seesaw=False)).set_index("shot")["next_stone"]
    assert (flat.abs() < 0.2).all()


def test_opponent_same_game_is_negative_under_the_seesaw():
    opp = opponent_same_game(_frame(200))
    assert opp["rel"] < -0.2 and abs(opp["grade_pct"]) < 0.2


def test_split_half_needs_both_halves():
    df = _frame(30)
    sh = split_half(df, "rel", min_half=20)       # 15 games per half, 2 stones each = 30 per half
    assert len(sh) == 2 and set(sh.columns) == {"a", "b"}
    assert len(split_half(df, "rel", min_half=40)) == 0


def test_probe_table_states_and_units():
    df = _frame(10).assign(pg_throw=0.1, V_post_wp=0.7, pg_throw_wp=0.02, model_p_steal=0.2, real_steal=0.0,
                           model_p_two=0.3, real_two=1.0)
    state = pd.Series(np.where(df["shot"] % 2, "made", "missed"), index=df.index)
    t = probe_table(df, state).set_index("state")
    assert list(t.index) == ["made", "missed"] and t.loc["made", "n"] == 20
    assert abs(t.loc["made", "model_wp_after"] - 70.0) < 1e-9 and abs(t.loc["made", "pg_throw_wp_pp"] - 2.0) < 1e-9


def test_calibration_gap_is_realised_minus_model():
    df = _frame(300)
    cal = calibration(df, min_n=100)
    row = cal[(cal["configuration"] == "empty") & (cal["rocks_left"] == "16-13")].iloc[0]
    assert row["n"] == 300 and abs(row["gap"]) < 1e-12 and abs(row["gap_wp_pp"]) < 1e-9
