import json, os
import numpy as np
from PIL import Image
from pointsgained.ingest import diagram as D

FIX = os.path.join(os.path.dirname(__file__), "fixtures")


def test_fixture_panels():
    expected = json.load(open(os.path.join(FIX, "expected.json")))
    for name, exp in expected.items():
        rgb = np.asarray(Image.open(os.path.join(FIX, f"{name}.png")).convert("RGB"))
        dg = D.read_diagram(rgb)
        assert dg.flipped == exp["flipped"], name
        assert sum(s.color == "red" for s in dg.stones) == exp["n_red"], name
        assert sum(s.color == "yellow" for s in dg.stones) == exp["n_yellow"], name
        assert dg.counters == exp["counters"], name
        assert next((s.color for s in dg.stones if s.delivered), None) == exp["delivered"], name
        assert len(dg.priors) == exp["n_priors"], name
        for c in ("red", "yellow"):
            assert dg.counters[f"{c}_remaining"] + sum(s.color == c for s in dg.stones) + dg.counters[f"{c}_removed"] == 8, name


def test_calibration_on_fixture():
    rgb = np.asarray(Image.open(os.path.join(FIX, "wcf_odd_end_two_touching.png")).convert("RGB"))
    cal = D.measure_calibration(D.classify_pixels(rgb))
    assert abs(cal.pin_col - 149) <= 1 and abs(cal.pin_row - 439) <= 1
    assert abs(cal.r12_px - 118.5) <= 1.5
