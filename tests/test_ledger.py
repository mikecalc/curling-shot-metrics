import numpy as np
import pandas as pd

from pointsgained.core.traits import TRAITS
from pointsgained.model.ledger import ledger_frame
from pointsgained.model.trait_study import STAGE_NAMES, TERMS


def _weights(stone_h=0.3, stone_n=-0.2):
    """A stone is worth `stone_h` to the hammer team (its own side), a non-hammer stone -stone_n; traits nothing."""
    rows = []
    for st in STAGE_NAMES:
        for team, base in (("hammer", stone_h), ("non-hammer", stone_n)):
            rows += [{"stage": st, "team": team, "trait": t, "target": "pts", "weight": base if t == "stone" else 0.0} for t in TERMS]
    return pd.DataFrame(rows)


def _wide(counts):
    """counts: {shot: (hammer open stones, non-hammer open stones)}"""
    recs = []
    for shot, (h, n) in counts.items():
        r = {"game_key": "g", "end": 1, "shot": shot}
        r.update({f"h_{t}": 0 for t in TRAITS} | {f"n_{t}": 0 for t in TRAITS})
        r["h_open"], r["n_open"] = h, n
        recs.append(r)
    return pd.DataFrame(recs)


def test_build_and_address_signs():
    wide = _wide({1: (0, 1), 2: (1, 1), 3: (1, 0)})
    shots = pd.DataFrame({"game_key": "g", "end": 1, "shot": [1, 2, 3, 4], "pre_source_shot": [0, 1, 2, 3],
                          "has_post": [True, True, True, True], "thrower_has_hammer": [False, True, False, True]})
    led = ledger_frame(shots, wide, _weights()).set_index("shot")
    assert abs(led.loc[1, "build"] - 0.2) < 1e-12 and led.loc[1, "address"] == 0.0     # non-hammer adds a stone
    assert abs(led.loc[2, "build"] - 0.3) < 1e-12 and led.loc[2, "address"] == 0.0     # hammer adds its own
    assert abs(led.loc[3, "build"] + 0.2) < 1e-12 and led.loc[3, "address"] == 0.0     # non-hammer's own stone is removed
    assert led.loc[4, "grade_h"] == 0.0 and abs(led.loc[4, "build"] + 0.3) < 1e-12      # the sheet is cleared
    assert abs(led.loc[2, "total"] - 0.5) < 1e-12


def test_no_diagram_leaves_the_after_unknown():
    wide = _wide({1: (0, 1)})
    shots = pd.DataFrame({"game_key": "g", "end": 1, "shot": [1, 2], "pre_source_shot": [0, 1],
                          "has_post": [True, False], "thrower_has_hammer": [False, True]})
    led = ledger_frame(shots, wide, _weights()).set_index("shot")
    assert np.isnan(led.loc[2, "grade_h"]) and np.isnan(led.loc[2, "build"])


def test_the_last_stone_is_graded_with_the_late_weights():
    wide = _wide({15: (1, 1), 16: (2, 1)})
    shots = pd.DataFrame({"game_key": "g", "end": 1, "shot": [16], "pre_source_shot": [15],
                          "has_post": [True], "thrower_has_hammer": [True]})
    led = ledger_frame(shots, wide, _weights()).set_index("shot")
    assert abs(led.loc[16, "grade_h"] - 0.6) < 1e-12 and abs(led.loc[16, "build"] - 0.3) < 1e-12
