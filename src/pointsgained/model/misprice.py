"""Where does a model over- or under-price positions? (`pointsgained misprice`, reports/experiments/misprice.md)

Reads the held-out predictions an experiment saved (`experiment --save-predictions`) and sets each model's
expectation for the position before the shot beside what the end actually produced, in groups: by
configuration label and stage, by stones in play, by count, and the last rock (the beam probe: the
hammer team throwing last, by the other team's count and how close its shot rock is to the pin).
Gap = realised - model; positive means the model under-prices the position for the hammer team.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

from ..core.configurations import LABELS
from .config_features import load_table, pre_and_post
from .dataset import scored_rows
from .value import OUTCOMES

KEYS = ["game_key", "end", "shot"]
BANDS = [(12, 16, "12-16 left"), (8, 11, "8-11 left"), (4, 7, "4-7 left"), (1, 3, "1-3 left")]


def load(parquet_root: str, names: list[str], which: str = "f") -> pd.DataFrame:
    """One row per held-out unmirrored shot: the pre-shot position's descriptors, the realised result, and
    each named experiment's expected points, P(2+) and P(steal) under `which` (f or g)."""
    cols = ["game_key", "end", "shot", "mirror", "pre_source_shot", "discipline", "rocks_remaining", "count",
            "stones_in_play", "own_min_dist", "opp_min_dist", "margin", "shot_rock_covered", "button_covered"]
    rows = scored_rows(pd.read_parquet(os.path.join(parquet_root, "features.parquet"), columns=cols + ["censored"]))
    rows = rows[rows["mirror"] == 0].drop(columns=["mirror", "censored"])
    df = None
    for n in names:
        p = pd.read_parquet(os.path.join(parquet_root, "experiments", f"{n}.parquet"))
        P = p[[f"{which}_{i}" for i in range(len(OUTCOMES))]].to_numpy()
        q = p[KEYS + ["label"]].copy()
        q[f"pts_{n}"] = P @ OUTCOMES
        q[f"two_{n}"] = P[:, 5:].sum(axis=1)
        q[f"steal_{n}"] = P[:, :3].sum(axis=1)
        df = q if df is None else df.merge(q.drop(columns="label"), on=KEYS)
    df = df.merge(rows, on=KEYS, how="left").reset_index(drop=True)
    pre, _ = pre_and_post(df, load_table(parquet_root))
    for c in LABELS:
        df["cfg_" + c] = pre[c].to_numpy()
    df["real_pts"] = df["label"].astype(float)
    df["real_two"] = (df["label"] >= 2).astype(float)
    df["real_steal"] = (df["label"] < 0).astype(float)
    rr = df["rocks_remaining"].to_numpy()
    df["band"] = pd.Categorical(np.select([(rr >= lo) & (rr <= hi) for lo, hi, _ in BANDS], [b for _, _, b in BANDS], ""),
                                categories=[b for _, _, b in BANDS], ordered=True)
    return df


def _ci(r: np.ndarray, cl: np.ndarray) -> float:
    e = r - r.mean()
    return float(1.96 * np.sqrt((pd.Series(e).groupby(cl).sum().to_numpy() ** 2).sum()) / len(r)) if len(r) > 1 else np.nan


def gap_table(df: pd.DataFrame, by: list[str], names: list[str], metric: str = "pts", min_n: int = 300,
              shift: dict | None = None) -> pd.DataFrame:
    """Per group: n, the realised value and each model's gap (realised - model), with a 95% interval
    (clustered by end) on the first model's gap."""
    k = 1.0 if metric == "pts" else 100.0
    out = []
    for key, g in df.groupby(by, observed=True):
        if len(g) < min_n:
            continue
        key = key if isinstance(key, tuple) else (key,)
        r = {**dict(zip(by, key)), "n": len(g), f"real_{metric}": k * g[f"real_{metric}"].mean()}
        cl = (g["game_key"] + "|" + g["end"].astype(str)).to_numpy()
        for i, n in enumerate(names):
            resid = (g[f"real_{metric}"] - g[f"{metric}_{n}"]).to_numpy()
            r[f"gap_{n}"] = k * resid.mean() - (shift or {}).get(n, 0.0)
            if i == 0:
                r["ci"] = k * _ci(resid, cl)
        out.append(r)
    return pd.DataFrame(out)


def config_gaps(df: pd.DataFrame, names: list[str], metric: str = "pts", min_n: int = 300, shift: dict | None = None) -> pd.DataFrame:
    parts = []
    for lab in LABELS:
        s = df[df["cfg_" + lab]]
        if len(s):
            t = gap_table(s, ["band"], names, metric, min_n, shift)
            t.insert(0, "configuration", lab)
            parts.append(t)
    return pd.concat(parts, ignore_index=True)


def beam_probe(df: pd.DataFrame, names: list[str], shift: dict | None = None) -> pd.DataFrame:
    """The last rock, the hammer team throwing: by the count before it and how far the shot rock is from the
    pin, the realised chance that the hammer team scores against each model's."""
    s = df[df["rocks_remaining"] == 1].copy()
    shot_d = np.minimum(s["own_min_dist"], s["opp_min_dist"])
    s["shot_rock_at"] = pd.cut(shot_d, [-1, 6 + 5.7, 24 + 5.7, 48 + 5.7, 77.7, 1e9],
                               labels=["button", "4-foot", "8-foot", "12-foot", "empty house"])
    def lying(c):
        if c == 0:
            return "empty house"
        who = "hammer" if c > 0 else "other"
        return f"{who} lies {int(abs(c))}{'+' if abs(c) >= 3 else ''}"
    s["lying"] = s["count"].map(lying)
    s["real_score"] = (s["label"] > 0).astype(float)
    out = []
    for key, g in s.groupby(["lying", "shot_rock_at"], observed=True):
        if len(g) < 60:
            continue
        r = {"lying": key[0], "shot rock in": key[1], "n": len(g), "real P(score) %": 100 * g["real_score"].mean(),
             "real pts": g["real_pts"].mean()}
        for i, n in enumerate(names):
            resid = (g["real_pts"] - g[f"pts_{n}"]).to_numpy()
            r[f"gap {n}"] = resid.mean() - (shift or {}).get(n, 0.0)
            if i == 0:
                r["±"] = _ci(resid, (g["game_key"] + "|" + g["end"].astype(str)).to_numpy())
        out.append(r)
    return pd.DataFrame(out)


def write_report(parquet_root: str, reports_dir: str, names: list[str], which: str = "f") -> str:
    df = load(parquet_root, names, which)
    ref = names[0]
    lines = [f"# Where the models misprice ({which}, held-out rows)\n",
             f"Models: {', '.join(f'`{n}`' for n in names)}. Gap = realised − model in the hammer team's points (clipped ±3); "
             "positive means the model under-prices the position for the hammer team. The ± is a 95% interval for the "
             f"first model (`{ref}`), clustered by end. {len(df):,} positions.\n"]
    overall = gap_table(df.assign(all="all"), ["all"], names, min_n=1)
    shift = {n: float(overall[f"gap_{n}"].iloc[0]) for n in names}
    lines += ["## Overall\n", overall.round(4).to_markdown(index=False) + "\n",
              "On a time split the held-out years can simply score differently from the training years, which shows "
              "as the same gap everywhere. **Every table below is net of each model's overall gap**, so it shows "
              "where a model misprices relative to its own average.\n"]
    by_band = gap_table(df, ["band"], names, shift=shift)
    lines += ["## By stage\n", by_band.round(4).to_markdown(index=False) + "\n"]
    df["stones_band"] = pd.cut(df["stones_in_play"], [-1, 0, 2, 4, 6, 8, 16], labels=["0", "1-2", "3-4", "5-6", "7-8", "9+"])
    st = gap_table(df, ["band", "stones_band"], names, shift=shift)
    lines += ["## By stage and stones in play\n", st.round(4).to_markdown(index=False) + "\n"]
    cg = config_gaps(df, names, shift=shift)
    cg["worst"] = cg[[f"gap_{n}" for n in names[1:]]].abs().max(axis=1) if len(names) > 1 else cg[f"gap_{ref}"].abs()
    lines += ["## By configuration (before the shot) and stage, largest gaps first\n",
              "Groups of 300 or more; the 30 with the largest gap in any model after the first.\n",
              cg.sort_values("worst", ascending=False).drop(columns="worst").head(30).round(3).to_markdown(index=False) + "\n"]
    cg.to_csv(os.path.join(reports_dir, "experiments", "misprice_config.csv"), index=False)
    lines += ["## The last rock (beam probe)\n",
              "The hammer team's last stone: the count before it and where the shot rock sits. `real P(score)` is how "
              "often the hammer team scored; gaps are in points, net of the overall gap; ± is the first model's 95% interval.\n", beam_probe(df, names, shift).round(3).to_markdown(index=False) + "\n"]
    path = os.path.join(reports_dir, "experiments", "misprice.md")
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return path
