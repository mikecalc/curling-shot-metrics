"""Inventory of the CURLIT results-book directory (design Section 3.6.2).

`https://curlit.com/results` is server-rendered HTML: one table row per event with the
event name and location in the first cell and direct `PDF/<name>.pdf` links titled
'Results Book' / 'Results Book Men' / 'Results Summary' ...
"""
from __future__ import annotations

import csv
import logging
import os
import re
import time

import pandas as pd

from .event_families import classify_event

log = logging.getLogger(__name__)
RESULTS_URL = "https://curlit.com/results"
BASE = "https://curlit.com/"
ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S | re.I)
CELL_RE = re.compile(r"<td[^>]*>(.*?)</td>", re.S | re.I)
LINK_RE = re.compile(r'<a\s+href="(PDF/[^"]+\.pdf)(?:\?[^"]*)?"[^>]*title="([^"]*)"', re.I)
TAG_RE = re.compile(r"<[^>]+>")
NAME_RE = re.compile(r"^(?P<event>.*?)(?:\s+(?P<year>(?:19|20)\d{2}))?(?:\s+in\s+(?P<location>.*))?$")
INVENTORY_COLUMNS = ["season", "year", "event_name", "location", "event_family", "tier", "gender", "division",
                     "doc_type", "file_name", "url", "http_status", "file_size", "in_scope",
                     "has_shot_by_shot", "style_family", "status", "notes"]


def fetch_results_html(timeout: int = 60) -> str:
    import requests
    r = requests.get(RESULTS_URL, timeout=timeout, headers={"User-Agent": "pointsgained-inventory/0.1"})
    r.raise_for_status()
    return r.text


def parse_results_html(html: str) -> pd.DataFrame:
    rows = []
    for m in ROW_RE.finditer(html):
        cells = CELL_RE.findall(m.group(1))
        if not cells:
            continue
        links = LINK_RE.findall(m.group(1))
        if not links:
            continue
        title_cell = TAG_RE.sub("", cells[0]).strip()
        nm = NAME_RE.match(title_cell)
        event = (nm.group("event") if nm else title_cell).strip()
        year = int(nm.group("year")) if nm and nm.group("year") else None
        location = (nm.group("location") or "").strip() if nm else ""
        for href, title in links:
            file_name = os.path.basename(href)
            doc_type = "ResultsBook" if "ResultsBook" in file_name or "Results Book" in title else \
                       ("ResultsSummary" if "Summary" in file_name or "Summary" in title else "Other")
            gender = None
            low = (title + " " + file_name).lower()
            if "women" in low:
                gender = "W"
            elif "men" in low or "_m." in low:
                gender = "M"
            division = None
            dm = re.search(r"([ABC])[-_ ]Division", file_name + " " + title, re.I)
            if dm:
                division = dm.group(1).upper()
            fam_name = event + (f" {division}-Division" if division else "")
            family, tier, in_scope = classify_event(fam_name)
            if year is None:
                ym = re.search(r"(19|20)\d{2}", file_name)
                year = int(ym.group(0)) if ym else None
            if gender is None and family in ("Worlds",):
                gender = "M" if "men's" in event.lower() and "women" not in event.lower() else ("W" if "women" in event.lower() else None)
            rows.append({
                "season": f"{year - 1}-{year}" if year and year >= 2000 and _autumn_event(family) else (str(year) if year else None),
                "year": year, "event_name": event, "location": location, "event_family": family, "tier": tier,
                "gender": gender, "division": division, "doc_type": doc_type, "file_name": file_name,
                "url": BASE + href, "http_status": None, "file_size": None,
                "in_scope": bool(in_scope and doc_type == "ResultsBook" and (year or 0) >= 2013),
                "has_shot_by_shot": None, "style_family": None, "status": "pending", "notes": "",
            })
    return pd.DataFrame(rows, columns=INVENTORY_COLUMNS)


def _autumn_event(family: str) -> bool:
    return family in ("EuropeansA", "EuropeansB", "EuropeansC", "PanContinentalA", "PanContinentalB", "PacificAsia", "OQE", "PreQualifier", "Qualification")


def head_check(df: pd.DataFrame, delay: float = 1.0, only_in_scope: bool = True) -> pd.DataFrame:
    import requests
    df = df.copy()
    for i, r in df.iterrows():
        if only_in_scope and not r["in_scope"]:
            continue
        try:
            h = requests.head(r["url"], timeout=30, allow_redirects=True, headers={"User-Agent": "pointsgained-inventory/0.1"})
            df.at[i, "http_status"] = h.status_code
            df.at[i, "file_size"] = int(h.headers.get("Content-Length", 0)) or None
        except Exception as e:
            df.at[i, "http_status"] = -1
            df.at[i, "notes"] = f"head failed: {e}"
        time.sleep(delay)
    return df


def build_inventory(out_csv: str, html: str | None = None, check: bool = False) -> pd.DataFrame:
    html = html or fetch_results_html()
    df = parse_results_html(html)
    if check:
        df = head_check(df)
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    df.to_csv(out_csv, index=False)
    return df
