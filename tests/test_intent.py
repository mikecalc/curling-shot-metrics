"""Realised intent from the delivered stone and prior rings on a synthetic end."""
import numpy as np
import pandas as pd

from pointsgained.model.intent import realised_intent, attach_intent, INTENT_COLS
from tests.test_dataset import synthetic_tabs, GK


def tabs_with_intent():
    tabs = synthetic_tabs()
    # end 1 (hammer BBB = yellow). shot 3 (AAA, red, Draw): delivered red stone rests at (4, -10).
    # shot 4 (BBB, yellow, Take-out): strikes the red stone that was shot rock at (4, -10); a prior ring
    # marks it; the shooter (yellow, delivered) stays at (6, 20); a red stone remains at (40, 0).
    st = tabs["stones"]
    st = st[~((st["end"] == 1) & (st["shot"].isin([3, 4])))]
    extra = pd.DataFrame([
        {"game_key": GK, "end": 1, "shot": 3, "kind": "stone", "color": "yellow", "x_in": 40.0, "y_in": 0.0, "delivered": False},
        {"game_key": GK, "end": 1, "shot": 3, "kind": "stone", "color": "red", "x_in": 4.0, "y_in": -10.0, "delivered": True},
        {"game_key": GK, "end": 1, "shot": 4, "kind": "stone", "color": "yellow", "x_in": 40.0, "y_in": 0.0, "delivered": False},
        {"game_key": GK, "end": 1, "shot": 4, "kind": "stone", "color": "yellow", "x_in": 6.0, "y_in": 20.0, "delivered": True},
        {"game_key": GK, "end": 1, "shot": 4, "kind": "prior", "color": "red", "x_in": 4.0, "y_in": -10.0, "delivered": False},
    ])
    tabs["stones"] = pd.concat([st, extra], ignore_index=True)
    return tabs


def test_realised_intent_draw_and_hit():
    it = realised_intent(tabs_with_intent()).set_index(["end", "shot"])
    draw = it.loc[(1, 3)]
    assert draw["family"] == "draw" and draw["target_known"] == 1.0
    assert (draw["target_x"], draw["target_y"]) == (4.0, -10.0) and draw["target_ring"] == 1.0   # four-foot
    hit = it.loc[(1, 4)]
    assert hit["family"] == "hit" and hit["target_known"] == 1.0
    assert (hit["target_x"], hit["target_y"]) == (4.0, -10.0)
    assert hit["target_owner"] == -1.0                 # struck a non-hammer (red) stone; hammer is BBB = yellow
    assert hit["target_is_shot_rock"] == 1.0 and hit["target_is_guard"] == 0.0 and hit["shooter_stays"] == 1.0
    # shot 2 had no diagram: unknown target, zero columns
    s2 = it.loc[(1, 2)]
    assert s2["target_known"] == 0.0 and s2["target_x"] == 0.0


def test_attach_intent_mirrors_x():
    from pointsgained.model.dataset import build_dataset
    tabs = tabs_with_intent()
    ds = build_dataset(tabs)
    rows = attach_intent(ds.rows, realised_intent(tabs))
    assert set(INTENT_COLS) <= set(rows.columns)
    u = rows[(rows["mirror"] == 0) & (rows["end"] == 1) & (rows["shot"] == 4)].iloc[0]
    m = rows[(rows["mirror"] == 1) & (rows["end"] == 1) & (rows["shot"] == 4)].iloc[0]
    assert u["target_x"] == 4.0 and m["target_x"] == -4.0 and u["target_y"] == m["target_y"]
