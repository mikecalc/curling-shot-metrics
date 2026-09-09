"""Event family and tier assignment from the curlit event name (design Section 3.6.1).

This regex table is the single place event tiers are defined.
"""
from __future__ import annotations

import re

# (regex on the event name, family, tier, in_scope). First match wins.
FAMILIES = [
    (r"mixed doubles", "MixedDoubles", None, False),
    (r"wheelchair|paralympic", "Wheelchair", None, False),
    (r"youth olympic|european youth", "Youth", None, False),
    (r"mixed curling|world mixed|mixed team", "Mixed", None, False),
    (r"olympic winter games|olympic games", "Olympics", 1, True),
    (r"world (men's|women's) curling championship", "Worlds", 1, True),
    (r"olympic qualification event|olympic qualif", "OQE", 2, True),
    (r"european curling championships?.*\bb[- ]division|\bb[- ]division.*european", "EuropeansB", 3, True),
    (r"european curling championships?.*\bc[- ]division|\bc[- ]division.*european", "EuropeansC", 4, True),
    (r"european curling championship", "EuropeansA", 2, True),
    (r"pan continental.*\bb[- ]division|\bb[- ]division.*pan continental", "PanContinentalB", 3, True),
    (r"pan continental", "PanContinentalA", 2, True),
    (r"pacific[- ]asia", "PacificAsia", 2, True),
    (r"pre-qualif|pre qualif", "PreQualifier", 3, True),
    (r"world junior[- ]b|junior b curling", "JuniorB", 4, True),
    (r"world junior", "Juniors", 3, True),
    (r"world senior", "Seniors", 4, True),
    (r"universiade|university games", "Universiade", 4, True),
    (r"qualification", "Qualification", 3, True),
]


def classify_event(name: str) -> tuple[str, int | None, bool]:
    low = name.lower()
    for pat, fam, tier, in_scope in FAMILIES:
        if re.search(pat, low):
            return fam, tier, in_scope
    return "Other", None, False
