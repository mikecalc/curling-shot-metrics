"""Page-level classification and parsing of non-diagram pages (Game Results)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .panel_text import group_lines, parse_header, PageHeader


def page_kind(text: str) -> str:
    if "Game - Shot by Shot" in text or ("Shot by Shot" in text and "End" in text):
        return "shot_by_shot"
    if "Game Results" in text and ("LSFE" in text or "Sheet Team" in text):
        return "game_results"
    if "Cumulative Player Statistics" in text:
        return "player_stats"
    if "Session Results" in text or "Final Standings" in text or "Standings" in text:
        return "standings"
    if "Team Line-up" in text or "Line-up" in text:
        return "lineup"
    return "other"


@dataclass
class LineScore:
    code: str
    name: str
    lsfe: bool
    ends: list[str]          # per end: digit string or 'X'
    extra: list[str]
    total: int | None


@dataclass
class GameResults:
    header: PageHeader
    n_ends: int
    line_scores: list[LineScore] = field(default_factory=list)
    players: list[dict] = field(default_factory=list)     # code, position, function, name, game_pct, all_pct
    lsd: list[dict] = field(default_factory=list)


def parse_game_results(words) -> GameResults | None:
    header = parse_header(words)
    lines = group_lines(words)
    tl = [(t, [w["text"] for w in ws], ws) for t, ws in lines]
    n_ends = None
    start = None
    for i, (t, toks, _) in enumerate(tl):
        if toks[:2] == ["Sheet", "Team"] or (toks[:1] == ["Team"] and "LSFE" in toks):
            nums = [int(x) for x in toks if x.isdigit()]
            n_ends = max(nums) if nums else None
            start = i
            break
    if start is None or not n_ends:
        return None
    gr = GameResults(header=header, n_ends=n_ends)
    for t, toks, ws in tl[start + 1: start + 6]:
        if toks[:1] == ["Shot"]:
            break
        m = [i for i, x in enumerate(toks) if re.fullmatch(r"[A-Z]{3}", x) and i + 1 < len(toks) and toks[i + 1] == "-"]
        if not m:
            continue
        i = m[0]
        code = toks[i]
        rest = toks[i + 2:]
        lsfe = "*" in rest
        rest = [x for x in rest if x != "*"]
        # name tokens until the first score-like token
        name = []
        k = 0
        while k < len(rest) and not re.fullmatch(r"\d+|X", rest[k]):
            name.append(rest[k]); k += 1
        vals = rest[k:]
        if not vals:
            continue
        total = int(vals[-1]) if vals[-1].isdigit() else None
        body = vals[:-1]
        ends = body[:n_ends]
        extra = body[n_ends:]
        gr.line_scores.append(LineScore(code, " ".join(name), lsfe, ends, extra, total))
    # players: rows like '4 V HOESLI Philipp 85% 87%' possibly two teams side by side
    codes = [ls.code for ls in gr.line_scores]
    for t, toks, ws in tl[start + 1:]:
        if toks[:2] == ["Last", "Stone"] or toks[:2] == ["Shot", "Success", "Analysis"][:2] and "Analysis" in toks:
            pass
        # split by x: left half < 300
        halves = [[w for w in ws if w["x0"] < 300], [w for w in ws if w["x0"] >= 300]]
        for side, hw in enumerate(halves):
            ht = [w["text"] for w in hw]
            if len(ht) >= 3 and re.fullmatch(r"[1-4A]", ht[0]):
                j = 1
                func = None
                if j < len(ht) and ht[j] in ("S", "V"):
                    func = ht[j]; j += 1
                pcts = [x for x in ht[j:] if re.fullmatch(r"\d{1,3}%|-", x)]
                name = " ".join(x for x in ht[j:] if not re.fullmatch(r"\d{1,3}%|-", x))
                if len(pcts) >= 2 and side < len(codes) and t < 400:
                    gr.players.append({
                        "code": codes[side], "position": ht[0], "function": func, "name": name,
                        "game_pct": None if pcts[0] == "-" else int(pcts[0].rstrip("%")),
                        "all_pct": None if pcts[1] == "-" else int(pcts[1].rstrip("%")),
                    })
            # LSD rows: 'NAME Name 3.4cm'
            if len(ht) >= 2 and re.fullmatch(r"[\d.]+cm", ht[-1]) and ht[0] != "Total" and side < len(codes):
                gr.lsd.append({"code": codes[side], "name": " ".join(ht[:-1]), "cm": float(ht[-1][:-2])})
    return gr
