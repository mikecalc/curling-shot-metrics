import numpy as np
from pointsgained.model.value import (OUTCOMES, HammerAdjustedPoints, ValueSet, hammer_net,
                                     markov_hammer_value, clip_outcome)


def test_clip():
    assert clip_outcome(5) == 3 and clip_outcome(-4) == -3 and clip_outcome(1) == 1


def test_worked_example_from_design():
    # last rock, hammer, facing two, call is a double: 60% blank, 20% +1, 15% -1, 5% -2 ; N = 0.7
    m = HammerAdjustedPoints(0.7)
    d = np.zeros(7); d[3] = .6; d[4] = .2; d[2] = .15; d[1] = .05
    assert abs(m.V(d) - 0.37) < 1e-9
    assert abs(m.value_of_outcome(0) - 0.7) < 1e-9        # blank keeps hammer
    assert abs(m.value_of_outcome(1) - 0.3) < 1e-9        # single gives hammer away
    assert abs(m.value_of_outcome(-1) - (-0.3)) < 1e-9


def test_blank_beats_single_iff_h_above_half():
    assert HammerAdjustedPoints(0.6).value_of_outcome(0) > HammerAdjustedPoints(0.6).value_of_outcome(1)
    assert HammerAdjustedPoints(0.4).value_of_outcome(0) < HammerAdjustedPoints(0.4).value_of_outcome(1)


def test_markov_value_consistency():
    # hammer distribution: 10% blank, 35% steal (all -1), 55% score (40% +1, 15% +2)
    d = np.zeros(7); d[3] = .10; d[2] = .35; d[4] = .40; d[5] = .15
    N = hammer_net(d)
    H = markov_hammer_value(d)
    # H satisfies H = N + (P(blank)+P(steal)-P(score)) * H
    assert abs(H - (N + (.10 + .35 - .55) * H)) < 1e-9


def test_valueset_from_outcomes():
    vs = ValueSet.from_outcomes([0, 1, 2, -1, 1, 0, 2, 1])
    assert abs(vs.dist.sum() - 1) < 1e-9
    assert vs.N > 0
