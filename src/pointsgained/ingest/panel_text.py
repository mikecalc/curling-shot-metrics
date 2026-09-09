"""Parse the text of a CURLIT 'Game - Shot by Shot' page.

Text is real text with coordinates; panels sit on a fixed grid (six columns,
three rows) that is identical in every book seen from 2014 to 2026.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date

PANEL_X0 = [36, 128, 219, 310, 402, 493]          # PDF points
PANEL_TEXT_BANDS = [(318, 348), (496, 528), (674, 708)]   # (top_min, top_max) of the text rows
DIAGRAM_TOPS = [167, 346, 525]                     # image 'top' per panel row
SCORE_BOX_X = 488
END_HEADER_BAND = (146, 158)

MONTHS = {m: i for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], start=1)}
WEEKDAYS = {"MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"}

TURN_TOKENS = {"↻": "cw", "↺": "ccw", "In": "in", "Out": "out", "-": None}
TYPE_NORMALISE = {
    "Takeout": "Take-out",
    "Double Takeout": "Double Take-out",
    "Promotion Takeout": "Promotion Take-out",
    "Take-Out": "Take-out",
    "Hit & Roll": "Hit and Roll",
    "Through": "Through",
    "through": "Through",
}
KNOWN_TYPES = {
    "Draw", "Take-out", "Hit and Roll", "Guard", "Front", "Freeze", "Raise", "Clearing",
    "Double Take-out", "Promotion Take-out", "Wick / Soft Peeling", "Through",
}


@dataclass
class ShotText:
    panel: int                  # 1..16
    team: str | None = None
    player: str | None = None
    shot_type: str | None = None
    turn: str | None = None
    grade_raw: str | None = None
    grade_pct: float | None = None
    grade_scale: str | None = None    # 'pct' or 'four'
    note: str | None = None
    raw_lines: list[str] = field(default_factory=list)


@dataclass
class TeamHeader:
    code: str
    name: str
    score_before: int | None
    score_this_end: int | None
    score_after: int | None
    x0: float
    conceded: bool = False      # 'X' in the header: the end was not completed


@dataclass
class PageHeader:
    event_left: str = ""
    event_right: str = ""
    discipline: str | None = None      # 'M', 'W', 'MD', 'MX', or None
    date: date | None = None
    session: str = ""
    sheet: str | None = None
    start_time: str | None = None
    end_number: int | None = None
    teams: list[TeamHeader] = field(default_factory=list)
    total_score: dict = field(default_factory=dict)   # code -> int
    time_left: dict = field(default_factory=dict)     # code -> 'mm:ss'
    page_in_report: int | None = None
    pages_in_report: int | None = None
    report_code: str | None = None
    languages_extra: bool = False


def group_lines(words, tol: float = 3.0):
    """Group words into lines by 'top', return list of (top, [words sorted by x0])."""
    lines = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if lines and abs(lines[-1][0] - w["top"]) <= tol:
            lines[-1][1].append(w)
        else:
            lines.append([w["top"], [w]])
    return [(t, sorted(ws, key=lambda w: w["x0"])) for t, ws in lines]


def panel_column(x0: float) -> int | None:
    for i, px in enumerate(PANEL_X0):
        if px - 4 <= x0 < px + 86:
            return i
    return None


def text_bands_from_rows(row_tops: list[float] | None) -> list[tuple[float, float]]:
    """Text band per panel row: from below the diagrams to just above the next row's diagrams."""
    if not row_tops:
        return list(PANEL_TEXT_BANDS)
    tops = sorted(row_tops)
    bands = []
    for i, t in enumerate(tops):
        lo = t + 150
        hi = tops[i + 1] - 5 if i + 1 < len(tops) else t + 190
        bands.append((lo, hi))
    return bands


def panel_row_from_top(top: float, bands=None) -> int | None:
    for i, (lo, hi) in enumerate(bands or PANEL_TEXT_BANDS):
        if lo <= top <= hi:
            return i
    return None


def panel_index_from_image(x0: float, top: float, row_tops: list[float] | None = None) -> int | None:
    col = panel_column(x0)
    row = None
    for i, t in enumerate(sorted(row_tops) if row_tops else DIAGRAM_TOPS):
        if abs(top - t) <= 6:
            row = i
    if col is None or row is None:
        return None
    idx = row * 6 + col + 1
    return idx if idx <= 16 else None


GRADE_PCT = re.compile(r"^(\d{1,3})%$")
GRADE_FOUR = re.compile(r"^(In|Out)?([0-4X])$")


def parse_shot_line(tokens: list[str]) -> tuple[str | None, str | None, str | None, float | None, str | None]:
    """Return (shot_type, turn, grade_raw, grade_pct, grade_scale) from the type/turn/grade tokens."""
    toks = []
    for t in tokens:
        for arrow in ("↻", "↺"):
            if arrow in t and t != arrow:
                a, b = t.split(arrow, 1)
                for part in (a, arrow, b):
                    if part:
                        toks.append(part)
                break
        else:
            toks.append(t)
    turn = None
    grade_raw = None
    grade_pct = None
    scale = None
    if toks:
        m = GRADE_PCT.match(toks[-1])
        if m:
            grade_raw = toks.pop()
            grade_pct = float(m.group(1))
            scale = "pct"
        else:
            m = GRADE_FOUR.match(toks[-1])
            if m:
                grade_raw = toks.pop()
                grade_pct = None if m.group(2) == "X" else 25.0 * int(m.group(2))
                scale = "four"
                if m.group(1):
                    turn = TURN_TOKENS[m.group(1)]
            elif toks[-1] == "-":
                grade_raw = toks.pop()
    if toks and toks[-1] in TURN_TOKENS and turn is None:
        turn = TURN_TOKENS[toks.pop()]
    if toks and toks[-1] == "-":
        toks.pop()
    shot_type = " ".join(toks).strip() or None
    if shot_type:
        shot_type = TYPE_NORMALISE.get(shot_type, shot_type)
        shot_type = shot_type.replace("Takeout", "Take-out")
        if shot_type.lower() == "through":
            shot_type = "Through"
    return shot_type, turn, grade_raw, grade_pct, scale


def parse_panels(words, row_tops: list[float] | None = None) -> tuple[list[ShotText], list]:
    """Split words in the panel text bands into per-panel ShotText; also return score-box words."""
    per_panel: dict[int, list] = {}
    score_box = []
    bands = text_bands_from_rows(row_tops)
    for w in words:
        row = panel_row_from_top(w["top"], bands)
        if row is None:
            continue
        if w["x0"] >= SCORE_BOX_X and row == 2:
            score_box.append(w)
            continue
        col = panel_column(w["x0"])
        if col is None:
            continue
        idx = row * 6 + col + 1
        if idx > 16:
            score_box.append(w)
            continue
        per_panel.setdefault(idx, []).append(w)
    shots = []
    for idx in sorted(per_panel):
        lines = group_lines(per_panel[idx])
        st = ShotText(panel=idx)
        st.raw_lines = [" ".join(w["text"] for w in ws) for _, ws in lines]
        text_lines = [[w["text"] for w in ws] for _, ws in lines]
        # line 1: TEAM: PLAYER
        li = 0
        if text_lines and text_lines[0] and text_lines[0][0].endswith(":"):
            st.team = text_lines[0][0].rstrip(":")
            st.player = " ".join(text_lines[0][1:]).strip() or None
            li = 1
        if len(text_lines) > li:
            st.shot_type, st.turn, st.grade_raw, st.grade_pct, st.grade_scale = parse_shot_line(text_lines[li])
            li += 1
        if len(text_lines) > li:
            st.note = " ".join(" ".join(t) for t in text_lines[li:]).strip() or None
        shots.append(st)
    return shots, score_box


def parse_score_box(words, header: PageHeader) -> None:
    lines = group_lines(words)
    codes = []
    for _, ws in lines:
        toks = [w["text"] for w in ws]
        if not toks:
            continue
        if all(re.fullmatch(r"[A-Z]{3}", t) for t in toks) and 1 <= len(toks) <= 2:
            codes = toks
        elif toks[:2] == ["Total", "Score"]:
            vals = toks[2:]
            for c, v in zip(codes, vals):
                try:
                    header.total_score[c] = int(v)
                except ValueError:
                    pass
        elif toks[:2] == ["Time", "left"]:
            for c, v in zip(codes, toks[2:]):
                header.time_left[c] = v


DATE_RE = re.compile(r"^\d{1,2}$")


def parse_header(words, has_images_at_row=None) -> PageHeader:
    hdr = PageHeader()
    lines = group_lines(words)
    # locate the 'Game - Shot by Shot' title row to bound the header
    title_top = None
    for t, ws in lines:
        txt = " ".join(w["text"] for w in ws)
        if "Shot by Shot" in txt and t < 140:
            title_top = t
            break
    # Date: weekday token followed by day, month, year
    date_row = None
    for t, ws in lines:
        if title_top is not None and t > title_top:
            break
        toks = [w["text"] for w in ws]
        for i, tok in enumerate(toks):
            if tok in WEEKDAYS and i + 3 < len(toks) and DATE_RE.match(toks[i + 1]) and toks[i + 2][:3].upper() in MONTHS:
                try:
                    hdr.date = date(int(toks[i + 3]), MONTHS[toks[i + 2][:3].upper()], int(toks[i + 1]))
                    date_row = t
                except ValueError:
                    pass
                break
        if date_row is not None:
            break
    # Session descriptor: words on rows within 4pt of the date row (or the row above it in 2014 books), x0 > 250
    sess_words = []
    for t, ws in lines:
        if date_row is not None and abs(t - date_row) <= 4:
            sess_words += [w for w in ws if w["x0"] > 250]
    if not sess_words and date_row is not None:
        for t, ws in lines:
            if date_row - 12 <= t < date_row:
                sess_words += [w for w in ws if w["x0"] > 250]
    hdr.session = " ".join(w["text"] for w in sorted(sess_words, key=lambda w: w["x0"]))
    m = re.search(r"Sheet\s+([A-Z0-9]+)", hdr.session)
    if m:
        hdr.sheet = m.group(1)
    # Event title rows: the first line(s) above the date
    header_text = []
    for t, ws in lines:
        if title_top is not None and t >= title_top:
            break
        if date_row is not None and t >= date_row - 2:
            continue
        left = " ".join(w["text"] for w in ws if w["x0"] < 250)
        right = " ".join(w["text"] for w in ws if w["x0"] >= 250)
        header_text.append((left, right))
    if header_text:
        hdr.event_left = header_text[0][0]
        hdr.event_right = header_text[0][1]
    all_header = " ".join(l + " " + r for l, r in header_text)
    hdr.languages_extra = any("/" in l or "/" in r for l, r in header_text)
    low = all_header.lower()
    if "mixed doubles" in low or "mixed doubl" in low:
        hdr.discipline = "MD"
    elif "mixed team" in low or "mixed / " in low or re.search(r"\bmixed\b", low):
        hdr.discipline = "MX"
    elif "women" in low or "ladies" in low:
        hdr.discipline = "W"
    elif re.search(r"\bmen\b|men's|mens\b", low):
        hdr.discipline = "M"
    # Start time
    for t, ws in lines:
        toks = [w["text"] for w in ws]
        if "Start" in toks and "Time" in toks:
            i = toks.index("Time")
            if i + 1 < len(toks) and re.match(r"^\d{1,2}:\d{2}$", toks[i + 1]):
                hdr.start_time = toks[i + 1]
            break
    # End header
    for t, ws in lines:
        if END_HEADER_BAND[0] <= t <= END_HEADER_BAND[1]:
            _parse_end_header(ws, hdr)
    # Footer
    for t, ws in lines:
        toks = [w["text"] for w in ws]
        if "Page" in toks and t > 700:
            i = toks.index("Page")
            if i + 1 < len(toks):
                m = re.match(r"^(\d+)/(\d+)$", toks[i + 1])
                if m:
                    hdr.page_in_report, hdr.pages_in_report = int(m.group(1)), int(m.group(2))
            for tok in toks:
                if tok.startswith("CUR") or tok.startswith("CUM"):
                    hdr.report_code = tok
    return hdr


HEADER_TOKEN = re.compile(r"\(this|end\)|[A-Za-z][A-Za-z'.]*|\d+|X|[+=\-]")


def _parse_end_header(ws, hdr: PageHeader) -> None:
    # Some templates glue pieces together ('End1', 'CAN-Canada', '0+0(this', 'end)=0', '11+'):
    # re-tokenise every word into names, numbers and punctuation.
    toks, xs = [], []
    for w in ws:
        for piece in HEADER_TOKEN.findall(w["text"]):
            toks.append(piece); xs.append(w["x0"])
    # End number
    for i, tok in enumerate(toks):
        if tok == "End" and i + 1 < len(toks) and toks[i + 1].isdigit():
            hdr.end_number = int(toks[i + 1])
    # Team blocks: CODE '-' Name... numbers
    starts = [i for i, tok in enumerate(toks) if re.fullmatch(r"[A-Z]{3}", tok) and i + 1 < len(toks) and toks[i + 1] == "-"]
    for bi, i in enumerate(starts):
        j_end = starts[bi + 1] if bi + 1 < len(starts) else len(toks)
        block = toks[i:j_end]
        # stop the block at 'End'
        if "End" in block:
            block = block[: block.index("End")]
        code = block[0]
        name_toks = []
        vals = []          # score tokens in order: before, this_end, [after]; 'X' = end not completed
        for tok in block[2:]:
            if re.fullmatch(r"-?\d+|X", tok):
                vals.append(tok)
            elif tok in ("+", "=", "(this", "end)"):
                continue
            elif not vals:
                name_toks.append(tok)
        def num(v):
            return None if v is None or v == "X" else int(v)
        before = num(vals[0]) if len(vals) > 0 else None
        this_end = num(vals[1]) if len(vals) > 1 else None
        conceded = len(vals) > 1 and vals[1] == "X"
        after = num(vals[2]) if len(vals) > 2 else (before + this_end if before is not None and this_end is not None else None)
        hdr.teams.append(TeamHeader(code, " ".join(name_toks), before, this_end, after, xs[i], conceded))
