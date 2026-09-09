"""Extract one Results Book into tables: games, ends, shots, stones, line scores."""
from __future__ import annotations

import logging
import os
import re
import statistics
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import pdfplumber

from . import diagram as D
from .panel_text import (PageHeader, parse_header, parse_panels, parse_score_box,
                         panel_index_from_image, group_lines)
from .pdf_pages import page_kind, parse_game_results

log = logging.getLogger(__name__)

IN_SCOPE_DISCIPLINES = {"M", "W"}


@dataclass
class BookTables:
    book_id: str
    pages: pd.DataFrame
    games: pd.DataFrame
    ends: pd.DataFrame
    shots: pd.DataFrame
    stones: pd.DataFrame
    line_scores: pd.DataFrame
    players: pd.DataFrame
    warnings: list[str] = field(default_factory=list)

    def tables(self) -> dict[str, pd.DataFrame]:
        return {"pages": self.pages, "games": self.games, "ends": self.ends, "shots": self.shots,
                "stones": self.stones, "line_scores": self.line_scores, "players": self.players}


def _team_colours_from_images(page, hdr: PageHeader) -> dict[str, str]:
    """Map team code -> 'red'/'yellow' using the small colour-dot images on the end-header row."""
    colours = {}
    dots = [im for im in page.images if im["srcsize"][0] <= 80 and im["srcsize"][1] <= 80
            and 140 <= im["top"] <= 162]
    for th in hdr.teams:
        left = [im for im in dots if im["x1"] <= th.x0 + 2]
        if not left:
            continue
        im = max(left, key=lambda im: im["x1"])
        try:
            rgb = D.decode_image(im)
        except Exception:
            continue
        cls = D.classify_pixels(rgb)
        n_red = int((cls == D.CLASS_INDEX["red"]).sum())
        n_yel = int((cls == D.CLASS_INDEX["yellow"]).sum() + (cls == D.CLASS_INDEX["mark"]).sum())
        if max(n_red, n_yel) > 5:
            colours[th.code] = "red" if n_red >= n_yel else "yellow"
    return colours


def _game_key(hdr: PageHeader, codes: list[str]) -> str:
    d = hdr.date.isoformat() if hdr.date else "nodate"
    sess = re.sub(r"[^A-Za-z0-9]+", "_", hdr.session).strip("_")
    return f"{d}|{hdr.start_time or ''}|{sess}|{'-'.join(sorted(codes))}"


def extract_book(pdf_path: str, book_id: str | None = None, max_pages: int | None = None,
                 progress: bool = False) -> BookTables:
    book_id = book_id or os.path.splitext(os.path.basename(pdf_path))[0]
    page_rows, game_rows, end_rows, shot_rows, stone_rows, ls_rows, pl_rows = [], {}, [], [], [], [], []
    warnings: list[str] = []
    cal_samples: list[D.Calibration] = []

    with pdfplumber.open(pdf_path) as pdf:
        n = len(pdf.pages) if max_pages is None else min(max_pages, len(pdf.pages))
        for pi in range(n):
            page = pdf.pages[pi]
            try:
                text = page.extract_text() or ""
                kind = page_kind(text)
                prow = {"book": book_id, "page": pi + 1, "kind": kind, "discipline": None, "game_key": None}
                if kind in ("shot_by_shot", "game_results"):
                    words = page.extract_words()
                    if kind == "game_results":
                        gr = parse_game_results(words)
                        if gr is not None:
                            codes = [ls.code for ls in gr.line_scores]
                            key = _game_key(gr.header, codes)
                            prow["discipline"] = gr.header.discipline
                            prow["game_key"] = key
                            for ls in gr.line_scores:
                                ls_rows.append({"book": book_id, "page": pi + 1, "game_key": key,
                                                "discipline": gr.header.discipline, "date": gr.header.date,
                                                "session": gr.header.session, "sheet": gr.header.sheet,
                                                "team": ls.code, "team_name": ls.name, "lsfe": ls.lsfe,
                                                "n_ends": gr.n_ends, "ends": ls.ends, "extra": ls.extra,
                                                "total": ls.total})
                            for p in gr.players:
                                pl_rows.append({"book": book_id, "page": pi + 1, "game_key": key, **p})
                    else:
                        _extract_sbs_page(page, words, pi + 1, book_id, prow, game_rows, end_rows,
                                          shot_rows, stone_rows, warnings, cal_samples)
                page_rows.append(prow)
            except Exception as e:  # keep going; record the failure
                warnings.append(f"page {pi + 1}: {type(e).__name__}: {e}")
                page_rows.append({"book": book_id, "page": pi + 1, "kind": "error", "discipline": None, "game_key": None})
            finally:
                page.flush_cache()
                try:
                    page.close()
                except Exception:
                    pass
            if progress and (pi + 1) % 100 == 0:
                log.info("%s: page %d/%d, %d shots", book_id, pi + 1, n, len(shot_rows))

    games = pd.DataFrame(list(game_rows.values()))
    ends = pd.DataFrame(end_rows)
    shots = pd.DataFrame(shot_rows)
    stones = pd.DataFrame(stone_rows)
    if not stones.empty:
        # book-level calibration: median across panels, then recompute inches for consistency
        pin_col = statistics.median(c.pin_col for c in cal_samples)
        pin_row = statistics.median(c.pin_row for c in cal_samples)
        r12 = statistics.median(c.r12_px for c in cal_samples)
        ppi = r12 / 72.0
        stones["x_in"] = (stones["col"] - pin_col) / ppi
        stones["y_in"] = (pin_row - stones["row"]) / ppi
        if not games.empty:
            games["pin_col"], games["pin_row"], games["r12_px"] = pin_col, pin_row, r12
    if not ends.empty and not games.empty:
        _infer_hammer(ends, shots, games)
    return BookTables(book_id, pd.DataFrame(page_rows), games, ends, shots, stones,
                      pd.DataFrame(ls_rows), pd.DataFrame(pl_rows), warnings)


def _extract_sbs_page(page, words, page_no, book_id, prow, game_rows, end_rows, shot_rows, stone_rows,
                      warnings, cal_samples):
    hdr = parse_header(words)
    prow["discipline"] = hdr.discipline
    if not hdr.teams or hdr.end_number is None:
        warnings.append(f"page {page_no}: could not parse end header")
        return
    codes = [t.code for t in hdr.teams]
    key = _game_key(hdr, codes)
    prow["game_key"] = key
    if hdr.discipline not in IN_SCOPE_DISCIPLINES:
        prow["kind"] = "shot_by_shot_out_of_scope"
        return
    colours = _team_colours_from_images(page, hdr)
    big = [im for im in page.images if is_diagram_image(im)]
    row_tops = _cluster_rows([im["top"] for im in big])
    shots_text, score_words = parse_panels(words, row_tops)
    parse_score_box(score_words, hdr)

    # diagrams
    diags = {}
    for im in big:
        idx = panel_index_from_image(im["x0"], im["top"], row_tops)
        if idx is None:
            warnings.append(f"page {page_no}: diagram at ({im['x0']:.0f},{im['top']:.0f}) not on grid")
            continue
        try:
            rgb = D.decode_image(im)
            dg = D.read_diagram(rgb)
            diags[idx] = dg
            cal_samples.append(dg.calibration)
        except Exception as e:
            warnings.append(f"page {page_no} panel {idx}: {type(e).__name__}: {e}")

    # colour fallback / check from delivered stones
    votes: dict[str, dict[str, int]] = {}
    for st in shots_text:
        dg = diags.get(st.panel)
        if dg is None or st.team is None:
            continue
        for s in dg.stones:
            if s.delivered:
                votes.setdefault(st.team, {}).setdefault(s.color, 0)
                votes[st.team][s.color] += 1
    vote_colours = {t: max(v, key=v.get) for t, v in votes.items() if v}
    if len(colours) < 2 and len(vote_colours) == 2 and len(set(vote_colours.values())) == 2:
        colours = vote_colours
    if len(colours) == 1 and len(codes) == 2:
        other = [c for c in codes if c not in colours][0]
        colours[other] = "yellow" if list(colours.values())[0] == "red" else "red"

    g = game_rows.setdefault(key, {
        "book": book_id, "game_key": key, "discipline": hdr.discipline, "date": hdr.date,
        "start_time": hdr.start_time, "session": hdr.session, "sheet": hdr.sheet,
        "event_left": hdr.event_left, "event_right": hdr.event_right,
        "team_a": codes[0], "team_b": codes[1] if len(codes) > 1 else None,
        "team_a_name": hdr.teams[0].name, "team_b_name": hdr.teams[1].name if len(codes) > 1 else None,
        "color_a": colours.get(codes[0]), "color_b": colours.get(codes[1]) if len(codes) > 1 else None,
        "report_code": hdr.report_code, "first_page": page_no, "n_ends": 0,
    })
    g["n_ends"] += 1
    g["last_page"] = page_no

    erow = {"book": book_id, "page": page_no, "game_key": key, "end": hdr.end_number,
            "team_a": codes[0], "team_b": codes[1] if len(codes) > 1 else None}
    for side, th in zip(("a", "b"), hdr.teams[:2]):
        erow[f"score_before_{side}"] = th.score_before
        erow[f"score_end_{side}"] = th.score_this_end
        erow[f"score_after_{side}"] = th.score_after
        erow[f"total_box_{side}"] = hdr.total_score.get(th.code)
        erow[f"time_left_{side}"] = hdr.time_left.get(th.code)
    erow["conceded"] = any(t.conceded for t in hdr.teams)
    erow["n_shots"] = len(shots_text)
    erow["n_diagrams"] = len(diags)
    erow["colour_source"] = "images" if len(_team_colours_from_images(page, hdr)) == 2 else ("votes" if vote_colours else "none")
    end_rows.append(erow)

    for st in shots_text:
        dg = diags.get(st.panel)
        srow = {"book": book_id, "page": page_no, "panel": st.panel, "game_key": key, "end": hdr.end_number,
                "shot": st.panel, "team": st.team, "color": colours.get(st.team), "player": st.player,
                "shot_type": st.shot_type, "turn": st.turn, "grade_raw": st.grade_raw,
                "grade_pct": st.grade_pct, "grade_scale": st.grade_scale, "note": st.note,
                "has_diagram": dg is not None}
        if dg is not None:
            srow.update({f"cnt_{k}": v for k, v in dg.counters.items()})
            srow["n_red"] = sum(1 for s in dg.stones if s.color == "red")
            srow["n_yellow"] = sum(1 for s in dg.stones if s.color == "yellow")
            srow["delivered_color"] = next((s.color for s in dg.stones if s.delivered), None)
            srow["n_priors"] = len(dg.priors)
            srow["diagram_flipped"] = dg.flipped
            srow["diagram_warnings"] = "; ".join(dg.warnings) or None
            for s in dg.stones:
                stone_rows.append({"book": book_id, "page": page_no, "panel": st.panel, "game_key": key,
                                   "end": hdr.end_number, "shot": st.panel, "kind": "stone", "color": s.color,
                                   "col": s.col, "row": s.row, "area": s.area, "delivered": s.delivered,
                                   "inner_black": s.inner_black, "outline_black": s.outline_black,
                                   "split_from": s.split_from})
            for p in dg.priors:
                stone_rows.append({"book": book_id, "page": page_no, "panel": st.panel, "game_key": key,
                                   "end": hdr.end_number, "shot": st.panel, "kind": "prior", "color": p.color,
                                   "col": p.col, "row": p.row, "area": None, "delivered": False,
                                   "inner_black": None, "outline_black": None, "split_from": 1})
        shot_rows.append(srow)


def is_diagram_image(im) -> bool:
    """A shot diagram is a tall image with a 1:2 aspect ratio (300x600 nominal)."""
    w, h = im["srcsize"]
    return h >= 400 and w >= 200 and 1.8 <= h / w <= 2.2


def _cluster_rows(tops: list[float], gap: float = 50) -> list[float]:
    """Cluster diagram image tops into panel rows (they shift when a note line is present)."""
    out: list[float] = []
    for t in sorted(tops):
        if out and t - out[-1] < gap:
            continue
        out.append(t)
    return out


def _infer_hammer(ends: pd.DataFrame, shots: pd.DataFrame, games: pd.DataFrame) -> None:
    """Hammer = the team that did not throw shot 1 (teams alternate)."""
    first = shots[shots["shot"] == 1][["game_key", "end", "team"]].rename(columns={"team": "first_team"})
    m = ends.merge(first, on=["game_key", "end"], how="left")
    ends["first_team"] = m["first_team"].values
    ends["hammer"] = np.where(m["first_team"] == m["team_a"], m["team_b"],
                              np.where(m["first_team"] == m["team_b"], m["team_a"], None))
