"""Sheet geometry in inches, pin at (0, 0), house at the bottom of the diagram.

Convention: x is positive to the right as seen from the hack; y is positive
towards the hog line (in front of the tee), negative behind the tee.
"""
from __future__ import annotations

import math

RING_12_RADIUS = 72.0   # inches
RING_8_RADIUS = 48.0
RING_4_RADIUS = 24.0
BUTTON_RADIUS = 6.0
STONE_RADIUS = 5.7      # inches, for in-house (biting) determination
STONE_DIAMETER = 2 * STONE_RADIUS
HOG_TO_TEE = 252.0      # inches, 21 feet
BACK_LINE_Y = -72.0     # back line is tangent to the 12-foot behind the tee
HOG_LINE_Y = HOG_TO_TEE

# Diagram pixel geometry, verified on every CURLIT book examined (2014-2026).
DIAGRAM_WIDTH = 300
DIAGRAM_HEIGHT = 600
PIN_COL = 149.5
PIN_ROW = 439.5
RING_12_RADIUS_PX = 118.5
PX_PER_INCH = RING_12_RADIUS_PX / RING_12_RADIUS   # 1.6458
STONE_RADIUS_PX = 9.0
TOP_BORDER_ROW = 20      # hog line
BACK_LINE_ROW = 560


def distance_to_pin(x: float, y: float) -> float:
    return math.hypot(x, y)


def in_house(x: float, y: float, stone_radius: float = STONE_RADIUS) -> bool:
    """A stone is in the house if any part of it touches the 12-foot."""
    return distance_to_pin(x, y) <= RING_12_RADIUS + stone_radius


def ring_of(x: float, y: float) -> str:
    d = distance_to_pin(x, y)
    if d <= BUTTON_RADIUS:
        return "button"
    if d <= RING_4_RADIUS:
        return "4ft"
    if d <= RING_8_RADIUS:
        return "8ft"
    if d <= RING_12_RADIUS + STONE_RADIUS:
        return "12ft"
    return "out"


def px_to_inches(col: float, row: float, pin_col: float = PIN_COL,
                 pin_row: float = PIN_ROW, ppi: float = PX_PER_INCH) -> tuple[float, float]:
    return (col - pin_col) / ppi, (pin_row - row) / ppi


def inches_to_px(x: float, y: float, pin_col: float = PIN_COL,
                 pin_row: float = PIN_ROW, ppi: float = PX_PER_INCH) -> tuple[float, float]:
    return pin_col + x * ppi, pin_row - y * ppi
