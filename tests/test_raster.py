"""Rasteriser geometry, mirroring, pre-position arrays and the probe cases."""
import numpy as np
import pytest

torch = pytest.importorskip("torch")

from pointsgained.model.raster import rasterise, pre_position_arrays, build_net, H, W, X_MIN, Y_MIN, MAX_STONES, scalar_matrix
from pointsgained.model.dataset import build_dataset
from pointsgained.model import probe as PR
from tests.test_dataset import synthetic_tabs


def test_rasterise_disc_geometry_and_mirror():
    x = torch.tensor([[10.0, -30.0] + [0.0] * 14]); y = torch.tensor([[0.0, 100.0] + [0.0] * 14])
    own = torch.tensor([[1.0, 0.0] + [0.0] * 14]); valid = torch.zeros((1, MAX_STONES), dtype=torch.bool); valid[0, :2] = True
    img = rasterise(x, y, own, valid)
    assert img.shape == (1, 2, H, W)
    r0, c0 = torch.nonzero(img[0, 0], as_tuple=True)          # own stone -> channel 0
    assert abs(float(c0.float().mean()) - (10.0 - X_MIN)) < 0.6 and abs(float(r0.float().mean()) - (0.0 - Y_MIN)) < 0.6
    assert 95 <= int(img[0, 0].sum()) <= 110 and 95 <= int(img[0, 1].sum()) <= 110
    m = rasterise(x, y, own, valid, mirror=torch.tensor([True]))
    assert torch.equal(m[0, 0], torch.flip(img[0, 0], dims=[1])) or abs(float(torch.nonzero(m[0, 0], as_tuple=True)[1].float().mean()) - (-10.0 - X_MIN)) < 0.6
    t = rasterise(x, y, own, valid, target_xy=torch.tensor([[-30.0, 100.0]]))
    assert t.shape[1] == 3 and torch.equal(t[0, 2], t[0, 1])    # target channel drawn where the opponent stone is


def test_pre_position_arrays_and_scalars():
    ds = build_dataset(synthetic_tabs())
    a = pre_position_arrays(ds)
    u = ds.rows[ds.rows["mirror"] == 0].reset_index(drop=True)
    assert a.x.shape == (len(u), MAX_STONES)
    first = u.index[(u["end"] == 1) & (u["shot"] == 1)][0]
    assert not a.valid[first].any()                             # empty sheet before the first stone
    k3 = u.index[(u["end"] == 1) & (u["shot"] == 3)][0]        # pre of shot 3 = post of shot 1 (shot 2 had no diagram)
    assert a.valid[k3].sum() == 1 and a.owner[k3, 0] == 0
    S, cols = scalar_matrix(u, ds.X[(ds.rows["mirror"] == 0).to_numpy()], "g")
    assert S.shape == (len(u), len(cols)) and "type_0" in cols and "expected_grade" in cols
    net = build_net(2, S.shape[1] - 0)
    out = net(torch.zeros((2, 2, H, W)), torch.zeros((2, S.shape[1])))
    assert out.shape == (2, 7)


def test_monotonicity_cases_and_curve_summary():
    cases = PR.monotonicity_cases()
    assert len(cases) == 120 and all(c[3] == "B<=A" for c in cases)
    curves = np.tile(np.array([0.3, 0.2, 0.1, 0.0, -0.1, -0.2, -0.3]), (5, 1))
    s = PR.curve_summary(curves)
    assert s == {"1in": 0.1, "2in": 0.2, "4in": 0.3}
    rep = PR.monotonicity_report(lambda ps: np.array([float((p.owner == 1).sum() - (p.owner == 0).sum()) for p in ps]))   # own minus opp stones
    assert rep["opponent stone appears inside own shot rock"] == 1.0 and rep["own counting stone removed"] == 1.0
