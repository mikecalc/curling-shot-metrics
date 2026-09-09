"""Polite sequential downloader for in-scope Results Books."""
from __future__ import annotations

import hashlib
import logging
import os
import time

import pandas as pd

log = logging.getLogger(__name__)


def read_inventory(path: str) -> pd.DataFrame:
    """Read the inventory with text columns as object dtype (an all-empty column reads back as float)."""
    inv = pd.read_csv(path)
    for c in ("notes", "status", "style_family", "has_shot_by_shot", "gender", "division", "location"):
        if c in inv:
            inv[c] = inv[c].astype(object).where(inv[c].notna(), None)
    return inv


def download_books(inventory_csv: str, raw_dir: str, delay: float = 3.0, limit: int | None = None,
                   tiers: list[int] | None = None) -> pd.DataFrame:
    import requests
    inv = read_inventory(inventory_csv)
    todo = inv[inv["in_scope"] == True]
    if tiers:
        todo = todo[todo["tier"].isin(tiers)]
    if "http_status" in todo:
        todo = todo[(todo["http_status"].isna()) | (todo["http_status"] == 200)]
    n = 0
    for i, r in todo.iterrows():
        if limit is not None and n >= limit:
            break
        year = int(r["year"]) if pd.notna(r["year"]) else 0
        dest_dir = os.path.join(raw_dir, str(year))
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, r["file_name"])
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            inv.at[i, "status"] = "downloaded"
            continue
        log.info("downloading %s", r["url"])
        try:
            with requests.get(r["url"], stream=True, timeout=120, headers={"User-Agent": "pointsgained-download/0.1"}) as resp:
                if resp.status_code != 200:
                    inv.at[i, "http_status"] = resp.status_code
                    inv.at[i, "status"] = "missing"
                    continue
                h = hashlib.sha1()
                with open(dest + ".part", "wb") as f:
                    for chunk in resp.iter_content(1 << 20):
                        f.write(chunk); h.update(chunk)
            os.replace(dest + ".part", dest)
            inv.at[i, "http_status"] = 200
            inv.at[i, "file_size"] = os.path.getsize(dest)
            inv.at[i, "status"] = "downloaded"
            inv.at[i, "notes"] = f"sha1={h.hexdigest()[:12]}"
            n += 1
        except Exception as e:
            inv.at[i, "status"] = "error"
            inv.at[i, "notes"] = str(e)[:120]
        inv.to_csv(inventory_csv, index=False)
        time.sleep(delay)
    inv.to_csv(inventory_csv, index=False)
    return inv
