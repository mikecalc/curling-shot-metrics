"""Feature cache: the training table built once per corpus and reused by every fit and experiment.

`features.parquet` holds one row per (shot, mirror) with strata, situation, label and the baseline
features; `stones_canonical.parquet` holds the post-shot stones in the hammer frame. `features.json`
records the cache version and the book directories so that a changed corpus or feature definition
rebuilds automatically.
"""
from __future__ import annotations

import json
import logging
import os
import time

import pandas as pd

from .dataset import Dataset, build_dataset, load_books, book_dirs
from .features import FEATURE_NAMES

CACHE_VERSION = "2"     # bump when rows, features or the stones table change shape or meaning

log = logging.getLogger(__name__)


def _paths(root: str):
    return (os.path.join(root, "features.parquet"), os.path.join(root, "stones_canonical.parquet"),
            os.path.join(root, "features.json"))


def _signature(root: str, books: list[str] | None, mirror: bool) -> dict:
    return {"version": CACHE_VERSION, "books": books if books is not None else book_dirs(root),
            "mirror": mirror, "features": list(FEATURE_NAMES)}


def is_current(root: str, books: list[str] | None = None, mirror: bool = True) -> bool:
    fp, sp, mp = _paths(root)
    if not (os.path.exists(fp) and os.path.exists(sp) and os.path.exists(mp)):
        return False
    try:
        return json.load(open(mp)) == _signature(root, books, mirror)
    except (OSError, ValueError):
        return False


def build_cache(root: str, books: list[str] | None = None, mirror: bool = True) -> Dataset:
    t0 = time.time()
    tabs = load_books(root, books)
    log.info("loaded %d games, %d ends, %d shots in %.0fs", len(tabs["games"]), len(tabs["ends"]), len(tabs["shots"]), time.time() - t0)
    ds = build_dataset(tabs, mirror=mirror)
    log.info("dataset: %d rows (%d unmirrored), %d stones in %.0fs", len(ds.rows), int((ds.rows["mirror"] == 0).sum()),
             len(ds.stones), time.time() - t0)
    fp, sp, mp = _paths(root)
    ds.rows.to_parquet(fp, index=False)
    ds.stones.to_parquet(sp, index=False)
    with open(mp, "w") as f:
        json.dump(_signature(root, books, mirror), f, indent=1)
    return ds


def load_cache(root: str) -> Dataset:
    fp, sp, _ = _paths(root)
    rows = pd.read_parquet(fp)
    stones = pd.read_parquet(sp)
    return Dataset.from_frame(rows, stones)


def load_or_build(root: str, books: list[str] | None = None, mirror: bool = True, rebuild: bool = False) -> Dataset:
    if not rebuild and is_current(root, books, mirror):
        t0 = time.time()
        ds = load_cache(root)
        log.info("feature cache: %d rows loaded in %.0fs", len(ds.rows), time.time() - t0)
        return ds
    return build_cache(root, books, mirror)
