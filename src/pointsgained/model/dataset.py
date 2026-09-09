"""Training rows for f and g from extracted tables (design Section 7.4)."""
from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..core.positions import build_positions, Position
from .features import position_features, FEATURE_NAMES
from .value import clip_outcome

TABLES = ("pages", "games", "ends", "shots", "stones", "line_scores", "players")


def load_books(parquet_root: str) -> dict[str, pd.DataFrame]:
    """Concatenate the per-book Parquet tables under parquet_root."""
    out = {t: [] for t in TABLES}
    for book in sorted(os.listdir(parquet_root)):
        d = os.path.join(parquet_root, book)
        if not os.path.isdir(d):
            continue
        for t in TABLES:
            f = os.path.join(d, f"{t}.parquet")
            if os.path.exists(f):
                df = pd.read_parquet(f)
                if len(df):
                    if "game_key" in df and "book" in df:
                        # corpus-unique keys: books extracted before keys carried the book id
                        has = df["game_key"].notna().to_numpy()
                        keys = df["game_key"].where(has, "").astype(str)
                        books = df["book"].astype(str)
                        old = has & ~np.array([str(k).startswith(str(b) + "|") for k, b in zip(keys, books)])
                        df.loc[old, "game_key"] = books[old] + "|" + keys[old]
                    out[t].append(df)
    return {t: (pd.concat(v, ignore_index=True) if v else pd.DataFrame()) for t, v in out.items()}


@dataclass
class Dataset:
    rows: pd.DataFrame            # one row per (shot, mirror) with features, label, strata
    X: np.ndarray
    y: np.ndarray                 # class index 0..6 of the clipped hammer-perspective outcome
    positions: pd.DataFrame       # from build_positions (unmirrored)


SHOT_TYPES = ["Draw", "Take-out", "Hit and Roll", "Guard", "Front", "Freeze", "Raise", "Clearing",
              "Double Take-out", "Promotion Take-out", "Wick / Soft Peeling", "Through", "Other"]
TYPE_INDEX = {t: i for i, t in enumerate(SHOT_TYPES)}


def shot_type_code(t) -> int:
    return TYPE_INDEX.get(t, TYPE_INDEX["Other"]) if isinstance(t, str) else TYPE_INDEX["Other"]


def build_dataset(tabs: dict[str, pd.DataFrame], mirror: bool = True) -> Dataset:
    shots, stones, ends, games = tabs["shots"], tabs["stones"], tabs["ends"], tabs["games"]
    pos = build_positions(shots, stones, ends, games)
    game_meta = games.set_index("game_key")[["book", "discipline", "date"]]
    shot_meta = shots.set_index(["game_key", "end", "shot"])[["shot_type", "turn", "grade_pct", "team", "player", "color"]]
    recs, feats = [], []
    for r in pos.itertuples(index=False):
        if r.end_score_hammer is None or (isinstance(r.end_score_hammer, float) and np.isnan(r.end_score_hammer)):
            continue
        pre: Position = r.pre
        if pre is None:
            continue
        try:
            sm = shot_meta.loc[(r.game_key, r.end, r.shot)]
        except KeyError:
            continue
        gm = game_meta.loc[r.game_key]
        variants = [(pre, 0)] + ([(pre.mirrored(), 1)] if mirror else [])
        for p, m in variants:
            feats.append(position_features(p))
            recs.append({"game_key": r.game_key, "end": r.end, "shot": r.shot, "mirror": m,
                         "book": gm["book"], "discipline": gm["discipline"], "date": gm["date"],
                         "hammer_team": r.hammer_team, "thrower_has_hammer": r.thrower_has_hammer,
                         "team": sm["team"], "player": sm["player"], "shot_type": sm["shot_type"],
                         "shot_type_code": shot_type_code(sm["shot_type"]), "turn": sm["turn"],
                         "grade_pct": sm["grade_pct"], "label": clip_outcome(int(r.end_score_hammer)),
                         "is_last_shot": r.is_last_shot})
    rows = pd.DataFrame(recs)
    X = np.vstack(feats) if feats else np.zeros((0, len(FEATURE_NAMES)))
    y = (rows["label"].to_numpy() + 3) if len(rows) else np.zeros(0, dtype=int)
    return Dataset(rows=rows, X=X, y=y.astype(int), positions=pos)
