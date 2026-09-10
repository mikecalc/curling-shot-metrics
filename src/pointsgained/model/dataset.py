"""Training rows for f and g from extracted tables (design Section 7.4).

One row per (shot, mirror). Rows carry the strata (book, discipline, date, team, player), the call
(shot type, turn), the game situation (score difference and ends remaining, hammer perspective),
the label (clipped end outcome, hammer perspective) and the 28 baseline position features of the
pre-shot position. `post_row` is the index of the row holding the post-shot position (the next
shot's pre-position, same mirror), -1 when there is none.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..core.positions import build_positions, Position
from .features import position_features, FEATURE_NAMES
from .value import clip_outcome

TABLES = ("pages", "games", "ends", "shots", "stones", "line_scores", "players")

SHOT_TYPES = ["Draw", "Take-out", "Hit and Roll", "Guard", "Front", "Freeze", "Raise", "Clearing",
              "Double Take-out", "Promotion Take-out", "Wick / Soft Peeling", "Through", "Other"]
TYPE_INDEX = {t: i for i, t in enumerate(SHOT_TYPES)}

SITUATION_COLS = ["diff_hammer", "ends_remaining", "ends_total", "is_extra_end"]
META_COLS = ["game_key", "end", "shot", "mirror", "book", "discipline", "date", "hammer_team",
             "thrower_has_hammer", "team", "player", "shot_type", "shot_type_code", "turn", "grade_pct",
             "label", "end_score_hammer", "is_last_shot", "has_post", "pre_source_shot", "post_row"]


def load_books(parquet_root: str, books: list[str] | None = None) -> dict[str, pd.DataFrame]:
    """Concatenate the per-book Parquet tables under parquet_root (all book directories, or `books`)."""
    out = {t: [] for t in TABLES}
    names = books if books is not None else sorted(os.listdir(parquet_root))
    for book in names:
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
                        books_ = df["book"].astype(str)
                        old = has & ~np.array([str(k).startswith(str(b) + "|") for k, b in zip(keys, books_)])
                        df.loc[old, "game_key"] = books_[old] + "|" + keys[old]
                    out[t].append(df)
    return {t: (pd.concat(v, ignore_index=True) if v else pd.DataFrame()) for t, v in out.items()}


def book_dirs(parquet_root: str) -> list[str]:
    return sorted(b for b in os.listdir(parquet_root)
                  if os.path.isdir(os.path.join(parquet_root, b)) and os.path.exists(os.path.join(parquet_root, b, "shots.parquet")))


def shot_type_code(t) -> int:
    return TYPE_INDEX.get(t, TYPE_INDEX["Other"]) if isinstance(t, str) else TYPE_INDEX["Other"]


def situation_table(tabs: dict) -> pd.DataFrame:
    """One row per (game_key, end): diff_hammer (hammer team minus other, before the end),
    ends_remaining (including this one), ends_total, is_extra_end. From the ends table and line scores."""
    ends, ls = tabs["ends"], tabs.get("line_scores")
    e = ends.drop_duplicates(["game_key", "end"])
    ok = e["hammer"].notna() & e["score_before_a"].notna() & e["score_before_b"].notna()
    e = e[ok]
    hammer_is_a = e["hammer"].to_numpy() == e["team_a"].to_numpy()
    diff = np.where(hammer_is_a, e["score_before_a"] - e["score_before_b"], e["score_before_b"] - e["score_before_a"]).astype(int)
    total = pd.Series(10, index=e.index)
    if ls is not None and len(ls):
        n_ends = ls.groupby("game_key")["n_ends"].first()
        total = e["game_key"].map(n_ends).fillna(10).astype(int)
    endno = e["end"].astype(int).to_numpy()
    return pd.DataFrame({"game_key": e["game_key"].to_numpy(), "end": endno, "diff_hammer": diff,
                         "ends_remaining": np.maximum(1, total.to_numpy() - endno + 1),
                         "ends_total": total.to_numpy(), "is_extra_end": endno > total.to_numpy()})


@dataclass
class Dataset:
    rows: pd.DataFrame            # one row per (shot, mirror): META_COLS + SITUATION_COLS + FEATURE_NAMES
    X: np.ndarray                 # rows[FEATURE_NAMES]
    y: np.ndarray                 # class index 0..6 of the clipped hammer-perspective outcome
    stones: pd.DataFrame          # canonical post-shot stones per (game_key, end, shot): x, y, owner (unmirrored)

    @classmethod
    def from_frame(cls, rows: pd.DataFrame, stones: pd.DataFrame) -> "Dataset":
        X = rows[FEATURE_NAMES].to_numpy(dtype=float) if len(rows) else np.zeros((0, len(FEATURE_NAMES)))
        y = (rows["label"].to_numpy() + 3).astype(int) if len(rows) else np.zeros(0, dtype=int)
        return cls(rows=rows, X=X, y=y, stones=stones)

    def position(self, game_key: str, end: int, shot: int, mirror: int = 0) -> Position | None:
        """Rebuild the post-shot Position of a shot from the stones table (None when no diagram)."""
        r = self.rows[(self.rows["game_key"] == game_key) & (self.rows["end"] == end) & (self.rows["shot"] == shot) & (self.rows["mirror"] == 0)]
        if not len(r):
            return None
        fgz = int(r["fgz_rocks"].iloc[0])
        s = self.stones[(self.stones["game_key"] == game_key) & (self.stones["end"] == end) & (self.stones["shot"] == shot)]
        x = s["x"].to_numpy(float) * (-1.0 if mirror else 1.0)
        return Position(x, s["y"].to_numpy(float), s["owner"].to_numpy(int), 16 - shot, fgz)


def canonical_stones(pos: pd.DataFrame) -> pd.DataFrame:
    """Explode the post positions to one row per stone in the canonical (hammer) frame."""
    gk, en, sh, xs, ys, ow = [], [], [], [], [], []
    for r in pos.itertuples(index=False):
        p = r.post
        if p is None or p.n == 0:
            continue
        gk.append(np.full(p.n, r.game_key, dtype=object)); en.append(np.full(p.n, r.end)); sh.append(np.full(p.n, r.shot))
        xs.append(p.x); ys.append(p.y); ow.append(p.owner)
    if not gk:
        return pd.DataFrame(columns=["game_key", "end", "shot", "x", "y", "owner"])
    return pd.DataFrame({"game_key": np.concatenate(gk), "end": np.concatenate(en).astype(int), "shot": np.concatenate(sh).astype(int),
                         "x": np.concatenate(xs).astype(float), "y": np.concatenate(ys).astype(float), "owner": np.concatenate(ow).astype(int)})


def build_dataset(tabs: dict[str, pd.DataFrame], mirror: bool = True) -> Dataset:
    shots, stones, ends, games = tabs["shots"], tabs["stones"], tabs["ends"], tabs["games"]
    pos = build_positions(shots, stones, ends, games)
    if not len(pos):
        return Dataset.from_frame(pd.DataFrame(columns=META_COLS + SITUATION_COLS + FEATURE_NAMES), canonical_stones(pos))
    pos = pos[pos["end_score_hammer"].notna() & pos["pre"].notna()].reset_index(drop=True)
    base = pos[["game_key", "end", "shot", "hammer_team", "thrower_has_hammer", "end_score_hammer",
                "is_last_shot", "pre_source_shot"]].copy()
    base["has_post"] = pos["post"].notna().to_numpy()
    base["end_score_hammer"] = base["end_score_hammer"].astype(int)
    shot_meta = shots.drop_duplicates(["game_key", "end", "shot"])[["game_key", "end", "shot", "shot_type", "turn", "grade_pct", "team", "player"]]
    game_meta = games.drop_duplicates("game_key")[["game_key", "book", "discipline", "date"]]
    base["_order"] = np.arange(len(base))
    base = base.merge(shot_meta, on=["game_key", "end", "shot"], how="inner")
    base = base.merge(game_meta, on="game_key", how="left")
    base = base.merge(situation_table(tabs), on=["game_key", "end"], how="left")
    base = base.sort_values("_order")
    keep = base["_order"].to_numpy()
    pre = pos["pre"].to_numpy(dtype=object)[keep]
    base = base.drop(columns="_order").reset_index(drop=True)
    base["shot_type_code"] = base["shot_type"].map(shot_type_code).astype(int)
    base["label"] = base["end_score_hammer"].map(clip_outcome).astype(int)
    base["diff_hammer"] = base["diff_hammer"].fillna(0).astype(int)
    base["ends_remaining"] = base["ends_remaining"].fillna(10).astype(int)
    base["ends_total"] = base["ends_total"].fillna(10).astype(int)
    base["is_extra_end"] = base["is_extra_end"].fillna(False).astype(bool)
    n = len(base)
    X_unm = np.vstack([position_features(p) for p in pre]) if n else np.zeros((0, len(FEATURE_NAMES)))
    if mirror:
        X_mir = np.vstack([position_features(p.mirrored()) for p in pre]) if n else X_unm
        rows = base.loc[np.repeat(np.arange(n), 2)].reset_index(drop=True)
        rows["mirror"] = np.tile([0, 1], n)
        X = np.empty((2 * n, len(FEATURE_NAMES)))
        X[0::2] = X_unm
        X[1::2] = X_mir
    else:
        rows = base.copy()
        rows["mirror"] = 0
        X = X_unm
    # post_row: the row of the next shot in the same end and mirror; its pre-position is this shot's post
    key = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["shot"], rows["mirror"]])
    lookup = pd.Series(np.arange(len(rows)), index=key)
    nxt = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["shot"] + 1, rows["mirror"]])
    rows["post_row"] = lookup.reindex(nxt).fillna(-1).to_numpy().astype(int)
    for i, name in enumerate(FEATURE_NAMES):
        rows[name] = X[:, i]
    rows = rows[META_COLS + SITUATION_COLS + FEATURE_NAMES]
    return Dataset.from_frame(rows, canonical_stones(pos))
