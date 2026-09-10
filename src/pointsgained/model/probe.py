"""Gates for the raw-geometry model (design Section 7.5): the subtlety probe and monotonicity checks.

Subtlety probe: real positions where a Double Take-out was made and the struck stone is known;
translate that stone laterally by -4..+4 in and plot the value of g(S, Double) against the offset
for the raster model and for the tree model. A model that has learned the geometry shows a sharp
change where the double closes; the trees, which see the position through 28 numbers, show a
flat line.

Monotonicity: adding an opposing guard in front of the shot rock must not raise own value; moving
own shot rock from the eight-foot to the button must not lower the count probability.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..core.geometry import STONE_DIAMETER
from .dataset import Dataset
from .features import position_features, FEATURE_NAMES
from .value import OUTCOMES
from ..core.positions import Position

OFFSETS = np.array([-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0])


def probe_positions(ds: Dataset, intent: pd.DataFrame, shot_type: str = "Double Take-out", n: int = 300, seed: int = 0):
    """Rows (unmirrored) of made `shot_type` shots with a known struck stone, with the index of that
    stone in the pre-position. Returns a DataFrame with row index, stone arrays and the struck index."""
    rows = ds.rows[ds.rows["mirror"] == 0].reset_index()
    it = intent.set_index(["game_key", "end", "shot"])
    cand = rows[(rows["shot_type"] == shot_type) & (rows["grade_pct"] == 100.0)]
    keys = pd.MultiIndex.from_frame(cand[["game_key", "end", "shot"]])
    known = it.reindex(keys)
    cand = cand[(known["target_known"].to_numpy() == 1.0)]
    known = known[known["target_known"] == 1.0]
    rng = np.random.default_rng(seed)
    pick = rng.choice(len(cand), size=min(n, len(cand)), replace=False)
    out = []
    grp = ds.stones.groupby(["game_key", "end", "shot"]).indices
    sx, sy, so = ds.stones["x"].to_numpy(), ds.stones["y"].to_numpy(), ds.stones["owner"].to_numpy()
    for i in pick:
        r = cand.iloc[i]; k = known.iloc[i]
        idx = grp.get((r["game_key"], r["end"], int(r["pre_source_shot"])))
        if idx is None:
            continue
        x, y, o = sx[idx], sy[idx], so[idx]
        d = np.hypot(x - k["realised_x"], y - k["realised_y"])
        j = int(np.argmin(d))
        if d[j] > STONE_DIAMETER:
            continue
        out.append({"row": int(r["index"]), "x": x, "y": y, "owner": o, "struck": j, "rocks_remaining": int(r["rocks_remaining"])})
    return pd.DataFrame(out)


def translated(p: dict, dx: float) -> Position:
    x = p["x"].copy(); x[p["struck"]] += dx
    return Position(x, p["y"].copy(), p["owner"].astype(int), p["rocks_remaining"])


def tree_curve(models, ds: Dataset, probes: pd.DataFrame, v: np.ndarray) -> np.ndarray:
    """Value of g(S, call) under the tree model for each probe and offset: (n_probes, n_offsets)."""
    rows = ds.rows.iloc[probes["row"].to_numpy()].reset_index(drop=True)
    out = np.zeros((len(probes), len(OFFSETS)))
    for j, dx in enumerate(OFFSETS):
        X = np.vstack([position_features(translated(p, dx)) for p in probes.to_dict("records")])
        _, X_g = models.design(rows, X)
        out[:, j] = models.predict_g(X_g) @ v
    return out


def raster_curve(fit, ds: Dataset, probes: pd.DataFrame, v: np.ndarray, S: np.ndarray, target_xy: np.ndarray | None) -> np.ndarray:
    """Same under the raster model. S / target_xy are the scalar rows and targets for probes["row"]."""
    from .raster import StoneArrays, MAX_STONES
    out = np.zeros((len(probes), len(OFFSETS)))
    n = len(probes)
    for j, dx in enumerate(OFFSETS):
        x = np.zeros((n, MAX_STONES), np.float32); y = np.zeros_like(x); o = np.zeros_like(x); valid = np.zeros((n, MAX_STONES), bool)
        t = None if target_xy is None else target_xy.copy()
        for i, p in enumerate(probes.to_dict("records")):
            m = min(len(p["x"]), MAX_STONES)
            xx = p["x"].copy(); xx[p["struck"]] += dx
            x[i, :m], y[i, :m], o[i, :m], valid[i, :m] = xx[:m], p["y"][:m], p["owner"][:m], True
            if t is not None:
                t[i, 0] += dx                      # the target moves with the stone
        out[:, j] = fit.predict(StoneArrays(x, y, o, valid), S, t) @ v
    return out


def curve_summary(curves: np.ndarray) -> dict:
    """How much the value moves with the offset: mean absolute change from 0 to ±1, ±2, ±4 in."""
    c0 = curves[:, list(OFFSETS).index(0.0)]
    return {f"{int(abs(d))}in": round(float(np.mean(np.abs(curves[:, j] - c0))), 4) for j, d in enumerate(OFFSETS) if d > 0}


def monotonicity_cases(rng=None) -> list[tuple[str, Position, Position, str]]:
    """(name, position A, position B, 'B<=A'): the hammer team's value must not rise from A to B.
    Three unambiguous checks: an opponent stone appearing inside own shot rock (a steal position),
    own counting stone removed, and own guard removed from in front of own shot rock."""
    rng = rng or np.random.default_rng(0)
    cases = []
    for k in range(40):
        ang = rng.uniform(0, 2 * np.pi); r_own = rng.uniform(30, 44)
        sx, sy = r_own * np.cos(ang), r_own * np.sin(ang)
        ox, oy = 8.0 * np.cos(ang + 1.0), 8.0 * np.sin(ang + 1.0)          # opponent stone near the button, inside own
        gx, gy = sx * 0.6, 115.0                                            # own guard up the sheet in front of own stone
        rr = int(rng.integers(3, 10))
        a = Position(np.array([sx]), np.array([sy]), np.array([1]), rr)
        b = Position(np.array([sx, ox]), np.array([sy, oy]), np.array([1, 0]), rr)
        cases.append(("opponent stone appears inside own shot rock", a, b, "B<=A"))
        a2 = Position(np.array([sx, 60.0]), np.array([sy, -20.0]), np.array([1, 0]), rr)
        b2 = Position(np.array([60.0]), np.array([-20.0]), np.array([0]), rr)
        cases.append(("own counting stone removed", a2, b2, "B<=A"))
        a3 = Position(np.array([sx, 60.0, gx]), np.array([sy, -20.0, gy]), np.array([1, 0, 1]), rr)
        cases.append(("own guard removed from in front of own shot rock", a3, a2, "B<=A"))
    return cases


def monotonicity_report(value_fn) -> dict:
    """value_fn(list[Position]) -> array of values (hammer view). Share of cases respecting the expectation."""
    cases = monotonicity_cases()
    A = value_fn([c[1] for c in cases]); B = value_fn([c[2] for c in cases])
    out = {}
    for name in sorted(set(c[0] for c in cases)):
        m = np.array([c[0] == name for c in cases])
        out[name] = round(float(np.mean(B[m] <= A[m] + 1e-9)), 3)
    return out


def v_points(vm) -> np.ndarray:
    return np.asarray(vm.v, dtype=float)
