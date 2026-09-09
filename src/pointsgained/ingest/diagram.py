"""Decode and read a CURLIT shot diagram.

The per-shot diagrams in CURLIT Results Books are embedded raster images
(300x600 px, 4-bit indexed colour, lossless). This module decodes the image
stream, classifies pixels by nearest palette colour, and reads:

- stones in play (colour, centre in px and inches)
- the delivered stone (black centre mark, or a thick outline in some templates)
- prior positions of moved stones (hollow rings)
- corner counters: stones remaining (top strip) and removed (bottom strip)
"""
from __future__ import annotations

import io
from dataclasses import dataclass, field

import numpy as np
from scipy import ndimage
from scipy.signal import fftconvolve

from ..core import geometry as G

# Reference colours per class. Anti-aliased variants map to the nearest class.
REFERENCE = {
    "red": [(255, 0, 0)],
    "yellow": [(255, 200, 50), (255, 230, 0), (255, 255, 0)],
    "white": [(255, 255, 255)],
    "black": [(0, 0, 0)],
    "ring12": [(200, 200, 255)],
    "ring4": [(255, 255, 160), (160, 255, 192), (255, 200, 200)],
    "grey": [(80, 80, 80)],
    "mark": [(0, 25, 255)],          # blue cross drawn on yellow stones in some templates
}
CLASSES = list(REFERENCE)
CLASS_INDEX = {c: i for i, c in enumerate(CLASSES)}

STONE_FILL_AREA = 200        # px, nominal filled-disk area of one stone (r ~ 8 px inside outline)
MIN_STONE_AREA = 60
MIN_COUNTER_AREA = 6
STONE_RADIUS_PX = 9
STONE_COVER_MIN = 0.5        # disk-template coverage needed for a stone peak (rings ~0.25, crossed disks > 0.6)
NMS_RADIUS = 12              # peaks closer than this are the same stone (touching stones are 18 px apart)
TEMPLATE_RADIUS = 7
_yy, _xx = np.mgrid[-TEMPLATE_RADIUS:TEMPLATE_RADIUS + 1, -TEMPLATE_RADIUS:TEMPLATE_RADIUS + 1]
_DISK = (np.hypot(_yy, _xx) <= TEMPLATE_RADIUS).astype(np.float32)
_DISK_AREA = float(_DISK.sum())
THICK_OUTLINE_MIN = 85       # own black px in the 6-12 px annulus; a 1 px outline gives ~55-65, a 2 px one >= 95


class DecodeError(ValueError):
    pass


def _resolve(obj):
    """Resolve pdfminer indirect objects."""
    try:
        from pdfminer.pdftypes import resolve1
        return resolve1(obj)
    except Exception:
        return obj


def decode_image(im: dict) -> np.ndarray:
    """Decode a pdfplumber image dict to an (h, w, 3) uint8 RGB array."""
    stream = im["stream"]
    w, h = im["srcsize"]
    bits = int(im.get("bits") or 8)
    filters = [str(f) for f in (stream.get("Filter") or [])] if isinstance(stream.get("Filter"), list) \
        else [str(stream.get("Filter"))]
    if any("DCT" in f or "JPX" in f for f in filters):
        from PIL import Image
        return np.asarray(Image.open(io.BytesIO(stream.get_rawdata())).convert("RGB"))

    data = stream.get_data()
    cs = _resolve(im.get("colorspace"))
    if isinstance(cs, list) and len(cs) == 1:
        cs = _resolve(cs[0])
    if isinstance(cs, list) and cs and "Indexed" in str(cs[0]):
        base = str(_resolve(cs[1]))
        hival = int(_resolve(cs[2]))
        lookup = _resolve(cs[3])
        pal_bytes = lookup.get_data() if hasattr(lookup, "get_data") else bytes(lookup)
        ncomp = 3 if "RGB" in base else (1 if "Gray" in base else 4)
        pal = np.frombuffer(pal_bytes, dtype=np.uint8)
        pal = pal[: (hival + 1) * ncomp].reshape(-1, ncomp)
        if ncomp == 1:
            pal = np.repeat(pal, 3, axis=1)
        elif ncomp == 4:  # CMYK, crude
            c, m, y, k = [pal[:, i].astype(float) / 255 for i in range(4)]
            pal = np.stack([(1 - c) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k)], axis=1) * 255
            pal = pal.astype(np.uint8)
        rowbytes = (w * bits + 7) // 8
        arr = np.frombuffer(data, dtype=np.uint8)
        if arr.size < rowbytes * h:
            raise DecodeError(f"short image data: {arr.size} < {rowbytes * h}")
        arr = arr[: rowbytes * h].reshape(h, rowbytes)
        if bits == 8:
            idx = arr[:, :w]
        elif bits == 4:
            idx = np.stack([arr >> 4, arr & 15], axis=2).reshape(h, -1)[:, :w]
        elif bits == 2:
            idx = np.stack([arr >> 6, (arr >> 4) & 3, (arr >> 2) & 3, arr & 3], axis=2).reshape(h, -1)[:, :w]
        elif bits == 1:
            idx = np.unpackbits(arr, axis=1)[:, :w]
        else:
            raise DecodeError(f"unsupported bits {bits}")
        idx = np.clip(idx, 0, len(pal) - 1)
        return pal[idx].astype(np.uint8)
    # Non-indexed
    if "RGB" in str(cs) and bits == 8 and len(data) >= w * h * 3:
        return np.frombuffer(data, dtype=np.uint8)[: w * h * 3].reshape(h, w, 3).copy()
    if ("Gray" in str(cs) or bits == 1) and len(data) >= ((w * bits + 7) // 8) * h:
        rowbytes = (w * bits + 7) // 8
        arr = np.frombuffer(data, dtype=np.uint8)[: rowbytes * h].reshape(h, rowbytes)
        g = np.unpackbits(arr, axis=1)[:, :w] * 255 if bits == 1 else arr[:, :w]
        return np.repeat(g[:, :, None], 3, axis=2).astype(np.uint8)
    raise DecodeError(f"unsupported image: cs={str(cs)[:60]} bits={bits}")


_REF_ARRAY = np.array([r for refs in REFERENCE.values() for r in refs], dtype=float)
_REF_CLASS = np.array([CLASS_INDEX[k] for k, refs in REFERENCE.items() for _ in refs], dtype=np.int8)


def classify_colours(colours: np.ndarray) -> np.ndarray:
    """Class index for each RGB row of `colours` (n, 3) by nearest reference colour."""
    c = colours.astype(float)
    d = ((c[:, None, :] - _REF_ARRAY[None, :, :]) ** 2).sum(axis=2)
    return _REF_CLASS[np.argmin(d, axis=1)]


def classify_pixels(rgb: np.ndarray) -> np.ndarray:
    """Map each pixel to a class index by nearest reference colour.

    Fast path: pack RGB into 24-bit ints and classify the unique values only.
    """
    packed = (rgb[:, :, 0].astype(np.int32) << 16) | (rgb[:, :, 1].astype(np.int32) << 8) | rgb[:, :, 2].astype(np.int32)
    u, inv = np.unique(packed.ravel(), return_inverse=True)
    cols = np.stack([(u >> 16) & 255, (u >> 8) & 255, u & 255], axis=1)
    return classify_colours(cols)[inv].reshape(rgb.shape[:2])


@dataclass
class Stone:
    color: str
    col: float
    row: float
    area: int
    inner_black: int = 0
    mid_black: int = 0          # dark px between the centre zone and the outline: an X or cross, not a dot
    outline_black: int = 0
    delivered: bool = False
    split_from: int = 1     # >1 if this stone came from splitting a merged component


@dataclass
class Prior:
    color: str              # red / yellow / grey
    col: float
    row: float


@dataclass
class Calibration:
    pin_col: float = G.PIN_COL
    pin_row: float = G.PIN_ROW
    r12_px: float = G.RING_12_RADIUS_PX
    top_border: int = G.TOP_BORDER_ROW
    back_line: int = G.BACK_LINE_ROW

    @property
    def ppi(self) -> float:
        return self.r12_px / G.RING_12_RADIUS


@dataclass
class Diagram:
    width: int
    height: int
    calibration: Calibration
    stones: list[Stone] = field(default_factory=list)
    priors: list[Prior] = field(default_factory=list)
    counters: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    flipped: bool = False        # the source image had the house at the top (rotated before reading)


def is_house_at_top(cls: np.ndarray) -> bool:
    """True if the 12-foot ring sits in the upper half of the image (alternate-end drawing)."""
    ring = cls == CLASS_INDEX["ring12"]
    rows = np.nonzero(ring.any(axis=1))[0]
    if len(rows) == 0:
        return False
    return float(rows.mean()) < cls.shape[0] / 2


def measure_calibration(cls: np.ndarray) -> Calibration:
    """Find the sheet lines and the 12-foot radius in one diagram."""
    h, w = cls.shape
    black = cls == CLASS_INDEX["black"]
    row_black = black.sum(axis=1)
    col_black = black.sum(axis=0)
    full_rows = np.nonzero(row_black > 0.8 * w)[0]
    cal = Calibration()
    top_candidates = [r for r in full_rows if 5 < r < 60]
    back_candidates = [r for r in full_rows if h * 0.85 < r < h - 5]
    if top_candidates:
        cal.top_border = int(top_candidates[0])
    if back_candidates:
        cal.back_line = int(back_candidates[0])
    # tee line: the row with most black pixels inside the play area, near the 12-foot centre
    play = slice(cal.top_border + 1, cal.back_line)
    rb = row_black.copy(); rb[: cal.top_border + 1] = 0; rb[cal.back_line:] = 0
    cal.pin_row = float(np.argmax(rb))
    cb = col_black.copy(); cb[:2] = 0; cb[-2:] = 0
    cal.pin_col = float(np.argmax(cb))
    ring = cls[play] == CLASS_INDEX["ring12"]
    cols = np.nonzero(ring.any(axis=0))[0]
    if len(cols) > 50:
        cal.r12_px = float(cols.max() - cols.min()) / 2.0
    return cal


def _components(mask: np.ndarray):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3), dtype=int))
    if n == 0:
        return lab, []
    objs = ndimage.find_objects(lab)
    out = []
    for i, sl in enumerate(objs, start=1):
        sub = lab[sl] == i
        area = int(sub.sum())
        rows, cols = np.nonzero(sub)
        out.append({
            "id": i, "area": area, "slice": sl,
            "row": float(rows.mean() + sl[0].start), "col": float(cols.mean() + sl[1].start),
            "h": sl[0].stop - sl[0].start, "w": sl[1].stop - sl[1].start,
            "fill": area / max(1, (sl[0].stop - sl[0].start) * (sl[1].stop - sl[1].start)),
            "pixels": (rows + sl[0].start, cols + sl[1].start),
        })
    return lab, out


def fill_thin_lines(mask: np.ndarray, black: np.ndarray, passes: int = 2) -> np.ndarray:
    """Add to `mask` the black pixels that are 1-px lines drawn inside a coloured disk
    (the X on yellow stones in older templates). A black pixel with colour immediately
    on both sides (left/right or up/down) is such a line pixel; outlines are not."""
    m = mask.copy()
    for _ in range(passes):
        lr = np.zeros_like(m); lr[:, 1:-1] = m[:, :-2] & m[:, 2:]
        ud = np.zeros_like(m); ud[1:-1, :] = m[:-2, :] & m[2:, :]
        # all four neighbours coloured: a diagonal line pixel inside a disk, never a shared outline
        add = black & lr & ud & ~m
        if not add.any():
            break
        m = m | add
    return m


def read_diagram(rgb: np.ndarray, calibration: Calibration | None = None) -> Diagram:
    """Read stones, priors and counters from a decoded diagram image."""
    cls = classify_pixels(rgb)
    h, w = cls.shape
    flipped = is_house_at_top(cls)
    if flipped:
        cls = cls[::-1, ::-1]      # rotate 180 degrees: thrower's perspective, house at the bottom
    cal = calibration or measure_calibration(cls)
    d = Diagram(width=w, height=h, calibration=cal, flipped=flipped)
    black = cls == CLASS_INDEX["black"]
    top, back = cal.top_border, cal.back_line
    filled_any = np.zeros_like(black)

    counters = {}
    for color in ("red", "yellow"):
        mask = cls == CLASS_INDEX[color]
        if color == "yellow":
            mask = mask | (cls == CLASS_INDEX["mark"])
        mask = fill_thin_lines(mask, np.ones_like(mask))   # any enclosed pixel: lines inside a disk take any tone in lossy books
        filled_any |= mask
        _, raw = _components(mask)
        n_top = 0
        n_bottom = 0
        in_play_raw = []
        top_comps = [c for c in raw if c["row"] < top + 4 and c["area"] >= MIN_COUNTER_AREA]
        if top_comps:
            # glyphs may merge under image noise: count by area relative to the smallest glyph
            unit = max(MIN_COUNTER_AREA, min(c["area"] for c in top_comps))
            n_top = sum(max(1, int(round(c["area"] / unit))) for c in top_comps)
        for c in raw:
            if c["row"] < top + 4:
                continue
            elif c["row"] > back + 6:
                if c["area"] >= MIN_COUNTER_AREA:
                    n_bottom += max(1, int(round((c["w"] + 2) / 18.0)))   # glyphs may overlap
            else:
                in_play_raw.append(c)
        counters[f"{color}_remaining"] = n_top
        counters[f"{color}_removed"] = n_bottom

        play_mask = np.zeros_like(mask)
        for c in in_play_raw:
            play_mask[c["pixels"]] = True
        # Stones by disk template: fraction of stone colour inside a stone-sized disk around each
        # pixel. A filled disk scores ~1 (with an X or cross drawn on it still > 0.6), a hollow
        # 1 px ring < 0.3, and two touching stones give two separate peaks 18 px apart.
        cover = fftconvolve(play_mask.astype(np.float32), _DISK, mode="same") / _DISK_AREA
        peaks = (cover >= STONE_COVER_MIN) & (cover == ndimage.maximum_filter(cover, size=2 * NMS_RADIUS + 1))
        prow, pcol = np.nonzero(peaks)
        taken = []
        for r_, c_ in sorted(zip(prow, pcol), key=lambda rc: -cover[rc[0], rc[1]]):
            if any(abs(r_ - tr) <= NMS_RADIUS and abs(c_ - tc) <= NMS_RADIUS for tr, tc in taken):
                continue     # plateau of the same peak
            taken.append((r_, c_))
            r0, r1 = max(0, r_ - 10), min(h, r_ + 11)
            c0, c1 = max(0, c_ - 10), min(w, c_ + 11)
            rr, cc = np.mgrid[r0:r1, c0:c1]
            local = play_mask[r0:r1, c0:c1] & (np.hypot(rr - r_, cc - c_) <= STONE_RADIUS_PX + 1)
            area = int(local.sum())
            if area < MIN_STONE_AREA:
                continue
            d.stones.append(Stone(color, float(cc[local].mean()), float(rr[local].mean()), area))
        # Priors: in-play components that are thin rings (vanish under erosion) and not a detected stone
        eroded = ndimage.binary_erosion(play_mask, structure=np.ones((3, 3), dtype=bool))
        for c in in_play_raw:
            if c["area"] >= 20 and c["w"] >= 10 and c["h"] >= 10 and not eroded[c["pixels"]].any():
                if not any(abs(c["row"] - s.row) < 6 and abs(c["col"] - s.col) < 6 for s in d.stones if s.color == color):
                    d.priors.append(Prior(color, c["col"], c["row"]))
    # grey rings
    grey = cls == CLASS_INDEX["grey"]
    grey[: top + 1, :] = False
    grey[back:, :] = False
    _, gcomps = _components(grey)
    for c in gcomps:
        if c["area"] >= 20 and c["w"] >= 10 and c["h"] >= 10:
            d.priors.append(Prior("grey", c["col"], c["row"]))
    d.counters = counters

    # Delivered stone: black centre mark (inner black, excluding filled cross lines) or thick outline.
    black_solid = black & ~filled_any
    centres = np.array([(s.row, s.col) for s in d.stones]) if d.stones else np.zeros((0, 2))
    for si, s in enumerate(d.stones):
        r0, r1 = int(max(0, s.row - 13)), int(min(h, s.row + 14))
        c0, c1 = int(max(0, s.col - 13)), int(min(w, s.col + 14))
        rr, cc = np.mgrid[r0:r1, c0:c1]
        dist = np.hypot(rr - s.row, cc - s.col)
        # pixels nearer to another stone's centre belong to that stone's outline, not this one's
        own = np.ones_like(dist, dtype=bool)
        for oj, (orow, ocol) in enumerate(centres):
            if oj != si:
                own &= dist < np.hypot(rr - orow, cc - ocol)
        s.inner_black = int((black_solid[r0:r1, c0:c1] & (dist <= 3.5)).sum())
        s.mid_black = int((black_solid[r0:r1, c0:c1] & (dist > 3.5) & (dist < 6.5)).sum())
        s.outline_black = int((black[r0:r1, c0:c1] & own & (dist >= 6) & (dist <= 12)).sum())
    if d.stones:
        # centre dot: dark pixels at the centre but not in the zone an X or cross would cross
        dots = [s for s in d.stones if s.inner_black >= 3 and s.mid_black <= 2]
        if dots:
            max(dots, key=lambda s: s.inner_black).delivered = True
        else:
            # thick (2 px) outline: about twice the ~57 px of a normal 1 px outline, and clearly the thickest
            ranked = sorted(d.stones, key=lambda s: -s.outline_black)
            second = ranked[1].outline_black if len(ranked) > 1 else 0
            if ranked[0].outline_black >= THICK_OUTLINE_MIN and ranked[0].outline_black >= 1.2 * second:
                ranked[0].delivered = True
    return d


def stone_inches(s: Stone | Prior, cal: Calibration) -> tuple[float, float]:
    return G.px_to_inches(s.col, s.row, cal.pin_col, cal.pin_row, cal.ppi)
