"""The rock ledger: what each stone did to the rocks in play, read from the trait grades (no tracking).

After every stone the house is re-read: each rock's traits are what they are in the new position, a
removed rock is gone, a moved rock is graded where it now sits. Each team's **grade** is the sum of its
rocks' grades, from its own side (model/trait_study.py: a rock's grade is its team's per-stone weight plus
the weights of its traits, fitted on the end's result for the stage of the end). A stone's
**build** is the rise in its own team's grade, its **address** the fall in the other team's, and the
end's **temperature** is both teams' grades together. The position before and after a stone are graded
with the weights of that stone's stage, so a stone is never credited with the change of stage itself.
The ledger describes positions; the Points Gained values are the model's.

`style_table` reads it per team at an event: how much its stones built and addressed against the field
at the same stage of the end.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

from .trait_features import counts_at, load_tables
from .trait_study import fit_weights, load_rows, position_grades

LEDGER_COLUMNS = ["grade_h_before", "grade_n_before", "grade_h", "grade_n", "build", "address", "net_change", "total"]


def ledger_frame(shots: pd.DataFrame, wide: pd.DataFrame, weights: pd.DataFrame) -> pd.DataFrame:
    """Per stone: each team's grade (its own side) before and after, and the thrower's build and address.
    `shots` needs game_key, end, shot, pre_source_shot, has_post and thrower_has_hammer. A shot without a
    diagram has no position after it (NaN)."""
    shot = shots["shot"].to_numpy()
    pre = position_grades(counts_at(shots, wide, "pre_source_shot"), shot, weights)
    post = position_grades(counts_at(shots, wide, "shot"), shot, weights)
    has_post = shots["has_post"].fillna(False).to_numpy(dtype=bool)
    gh_b, gn_b = pre["h_grade"].to_numpy(), -pre["n_grade"].to_numpy()          # each team's own side
    gh_a = np.where(has_post, post["h_grade"].to_numpy(), np.nan)
    gn_a = np.where(has_post, -post["n_grade"].to_numpy(), np.nan)
    ham = shots["thrower_has_hammer"].fillna(False).to_numpy(dtype=bool)
    own_b, opp_b = np.where(ham, gh_b, gn_b), np.where(ham, gn_b, gh_b)
    own_a, opp_a = np.where(ham, gh_a, gn_a), np.where(ham, gn_a, gh_a)
    out = shots[["game_key", "end", "shot"]].copy()
    out["grade_h_before"], out["grade_n_before"], out["grade_h"], out["grade_n"] = gh_b, gn_b, gh_a, gn_a
    out["build"] = own_a - own_b
    out["address"] = opp_b - opp_a
    out["net_change"] = out["build"] + out["address"]
    out["total"] = gh_a + gn_a
    return out


def rock_ledger(parquet_root: str) -> pd.DataFrame:
    """The ledger for every stone of the corpus, with weights fitted on the whole corpus (`rock_ledger.parquet`)."""
    rows = pd.read_parquet(os.path.join(parquet_root, "features.parquet"),
                           columns=["game_key", "end", "shot", "mirror", "pre_source_shot", "has_post", "thrower_has_hammer"])
    rows = rows[rows["mirror"] == 0].drop(columns="mirror").reset_index(drop=True)
    _, wide = load_tables(parquet_root)
    led = ledger_frame(rows, wide, fit_weights(load_rows(parquet_root), targets=("pts",)))
    led.to_parquet(os.path.join(parquet_root, "rock_ledger.parquet"), index=False)
    return led


def style_table(df: pd.DataFrame) -> pd.DataFrame:
    """Build or address, per team at one event (rows of one event and discipline, with the ledger columns):
    the team's mean build and mean address per stone relative to the event's field at the same stage of the
    end (rocks left 16-12, 11-8, 7-4, 3-1), the share of its stones that built more than they addressed,
    and the mean peak temperature (both teams' grades together) of its ends with and without hammer."""
    d = df[df["build"].notna()].copy()
    stage = pd.cut(17 - d["shot"], [0, 3, 7, 11, 16])
    for c in ("build", "address"):
        d[c + "_rel"] = d[c] - d.groupby(stage, observed=True)[c].transform("mean")
    d["builds"] = (d["build"] > d["address"]).astype(float)
    peak = d.groupby(["game_key", "end"]).agg(peak=("total", "max"), hammer=("hammer_team", "first"))
    rows = []
    for team, g in d.groupby("team"):
        ends = peak.loc[peak.index.isin(set(zip(g["game_key"], g["end"])))]
        rows.append(dict(team=team, stones=len(g), build=g["build_rel"].mean(), address=g["address_rel"].mean(),
                         builds_share=g["builds"].mean(),
                         temperature_hammer=ends.loc[ends["hammer"] == team, "peak"].mean(),
                         temperature_no_hammer=ends.loc[ends["hammer"] != team, "peak"].mean()))
    return pd.DataFrame(rows).sort_values("build", ascending=False)
