import numpy as np
import pandas as pd

from pointsgained.model.stone_value import ROLES, cells, final_roles, role_tables, zone_of


def test_zone_of_front_back_and_guards():
    x = np.array([0.0, 0.0, 40.0, -50.0, 0.0, 0.0, 60.0, 60.0, 0.0])
    y = np.array([10.0, -10.0, 30.0, -40.0, 120.0, 200.0, 120.0, 200.0, -100.0])
    assert list(zone_of(x, y)) == ["house front 4ft", "house back 4ft", "house front 8-12", "house back 8-12",
                                   "centre guard <6ft", "centre guard long", "corner guard <6ft", "corner guard long", "out"]


def test_final_roles_count_cover_and_backstop():
    # final diagram: hammer counts one on the button, covered by its own guard; a non-hammer stone sits
    # right behind the counter (a backstop); a second hammer stone is far out
    lives = pd.DataFrame({"game_key": "g", "end": 1, "shot": 16, "end_complete": True,
                          "sid": [1, 2, 3, 4], "owner": [1, 1, 0, 1],
                          "x": [0.0, 2.0, 1.0, 200.0], "y": [0.0, 110.0, -15.0, 0.0]})
    r = final_roles(lives).set_index("sid")
    assert r.loc[1, "r_count"] and not r.loc[1, "r_cover"]
    assert r.loc[2, "r_cover"] and not r.loc[2, "r_count"]
    assert r.loc[3, "r_backs_opp"] and not r.loc[3, "r_count"]
    assert not r.loc[4, ROLES].any()


def test_role_tables_shrink_small_cells_to_the_zone():
    n = 400
    rows = pd.DataFrame({"owner": 1, "rocks_remaining": 14, "x": np.r_[np.zeros(n - 2), [15.0, 15.0]],
                         "y": np.r_[np.full(n - 2, 10.0), [10.0, 10.0]], "r_count": np.r_[np.zeros(n - 2), [1, 1]] > 0,
                         "r_cover": False, "r_backs_opp": False})
    z, cell = role_tables(rows, prior=100.0)
    zone_rate = z.loc[(1, 3, "house front 4ft"), "r_count"]
    small = cell.xs((1, 3, "house front 4ft", 1, 6), level=["owner", "band", "zone", "cx", "cy"])["r_count"].iloc[0]
    assert abs(zone_rate - 2 / n) < 1e-12
    assert zone_rate < small < 0.05          # two of two counted, pulled most of the way to the zone's rate
    assert list(cells(rows.iloc[:1])["zone"]) == ["house front 4ft"]
