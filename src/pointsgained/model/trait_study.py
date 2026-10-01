"""The rock-trait study (`pointsgained traits`, reports/traits.md): what positions whose stones carry a
given trait have been worth, by team and stage of the end, and a first additive stone grade.

Rows are unmirrored shots with a post-shot diagram, stones 1-15; the position is the one after the shot
and the label is the end's result for the hammer team. Each end appears once per stone number, so the
rows of one stone number are independent; bands of stone numbers are summarised with confidence
intervals clustered by end. Differences are read against the same stone number and the same game
situation (discipline, score difference clipped to +/-2, two or fewer ends left): each row's outcome less
the mean outcome of its stratum, so a trait that turns up mostly when a team is ahead is not credited
with the lead's effect.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

from ..core.traits import TRAITS, type_name
from .trait_features import KEYS, TRAIT_COLUMNS, counts_at, load_tables

STAGES = [(1, 5, "stones 1-5"), (6, 10, "stones 6-10"), (11, 15, "stones 11-15")]
OUTCOME_COLS = ["pts", "steal", "blank", "one", "two"]
ADJUSTED = ["pts", "two", "steal"]
TEAMS = (("h", "hammer"), ("n", "non-hammer"))


def stage_of(shot: np.ndarray) -> np.ndarray:
    return np.select([shot <= hi for _, hi, _ in STAGES], [name for _, _, name in STAGES], "")


# ---- rows ------------------------------------------------------------------------------------------

def load_rows(parquet_root: str, inventory_csv: str | None = None, tier1: bool = False) -> pd.DataFrame:
    """One row per unmirrored shot 1-15 with a diagram: the trait counts of the position after it, the
    end's result and the situation strata, with each outcome's residual against its stratum."""
    cols = ["game_key", "end", "shot", "mirror", "book", "discipline", "has_post", "end_score_hammer",
            "diff_hammer", "ends_remaining", "censored"]
    rows = pd.read_parquet(os.path.join(parquet_root, "features.parquet"), columns=cols)
    rows = rows[(rows["mirror"] == 0) & rows["has_post"].fillna(False).astype(bool) & (rows["shot"] <= 15) & ~rows["censored"]]
    rows = rows.drop(columns=["mirror", "has_post", "censored"]).reset_index(drop=True)
    rows["end_score_hammer"] = rows["end_score_hammer"].astype(int)
    if inventory_csv:
        from .experiment import attach_tier
        rows = attach_tier(rows, inventory_csv)
        if tier1:
            rows = rows[rows["tier"] == 1].reset_index(drop=True)
    long, wide = load_tables(parquet_root)
    rows = pd.concat([rows, counts_at(rows, wide, "shot")], axis=1)
    n = long.groupby(KEYS).size().rename("stones")
    rows["stones"] = n.reindex(pd.MultiIndex.from_frame(rows[KEYS])).fillna(0).astype(int).to_numpy()
    s = rows["end_score_hammer"].to_numpy(float)
    rows["pts"], rows["steal"], rows["blank"] = s, (s < 0).astype(float), (s == 0).astype(float)
    rows["one"], rows["two"] = (s == 1).astype(float), (s >= 2).astype(float)
    rows["stage"] = stage_of(rows["shot"].to_numpy())
    rows["stratum"] = (rows["discipline"].astype(str) + "|" + rows["diff_hammer"].fillna(0).clip(-2, 2).astype(int).astype(str)
                       + "|" + (rows["ends_remaining"].fillna(10) <= 2).map({True: "late", False: "early"}))
    for c in ADJUSTED:
        rows["r_" + c] = rows[c] - rows.groupby(["shot", "stratum"])[c].transform("mean")
    return rows


# ---- the outcome block -----------------------------------------------------------------------------

def _clustered_ci(r: np.ndarray, cluster: np.ndarray) -> float:
    """95% half-width of the mean of r with errors clustered (by end)."""
    n = len(r)
    if n < 2:
        return float("nan")
    e = r - r.mean()
    sums = pd.Series(e).groupby(cluster).sum().to_numpy()
    return float(1.96 * np.sqrt((sums ** 2).sum()) / n)


def outcome_block(d: pd.DataFrame) -> dict:
    """n, the end's results (mean hammer points; steal, blank, one, two-or-more in %), and the differences
    from the same stone number and situation (points, and percentage points of two-or-more and steal)."""
    out = {"n": len(d)}
    if not len(d):
        return out
    out["pts"] = d["pts"].mean()
    for c in ("steal", "blank", "one", "two"):
        out[c] = 100 * d[c].mean()
    cl = (d["game_key"] + "|" + d["end"].astype(str)).to_numpy()
    for c in ADJUSTED:
        k = 1 if c == "pts" else 100
        r = d["r_" + c].to_numpy()
        out["d_" + c], out["ci_" + c] = k * r.mean(), k * _clustered_ci(r, cl)
    return out


def outcome_table(rows: pd.DataFrame, by: list[str] | str, min_n: int = 1) -> pd.DataFrame:
    """The outcome block for every group of `rows`."""
    t = pd.DataFrame([{**dict(zip([by] if isinstance(by, str) else by, k if isinstance(k, tuple) else (k,))), **outcome_block(g)}
                      for k, g in rows.groupby(by, sort=True, observed=True)])
    return t[t["n"] >= min_n].reset_index(drop=True)


# ---- 3a prevalence and overlap ---------------------------------------------------------------------

def prevalence(rows: pd.DataFrame) -> pd.DataFrame:
    """% of positions in which each team has at least one stone with the trait, by stage."""
    out = []
    for t in TRAITS:
        r = {"trait": t}
        for team, name in TEAMS:
            for _, _, st in STAGES:
                r[f"{name} {st}"] = 100 * (rows.loc[rows["stage"] == st, f"{team}_{t}"] > 0).mean()
        out.append(r)
    return pd.DataFrame(out)


def overlap(long: pd.DataFrame) -> pd.DataFrame:
    """Stone-level Jaccard overlap between traits (share of stones with either that have both)."""
    m = long[TRAITS].to_numpy(bool).astype(np.int64)
    both = m.T @ m
    tot = np.diag(both)
    either = tot[:, None] + tot[None, :] - both
    return pd.DataFrame(np.where(either > 0, both / np.maximum(either, 1), 0.0), index=TRAITS, columns=TRAITS)


# ---- 3b one trait at a time ------------------------------------------------------------------------

def trait_effects(rows: pd.DataFrame, by: list[str] = ()) -> pd.DataFrame:
    """For each stage, team and trait: positions where the team has at least one stone with the trait,
    against the rest (the outcome block of each, and the share of positions with it)."""
    out = []
    for keys, g in (rows.groupby(list(by)) if by else [((), rows)]):
        keys = keys if isinstance(keys, tuple) else (keys,)
        for _, _, st in STAGES:
            s = g[g["stage"] == st]
            for team, name in TEAMS:
                for t in TRAITS:
                    has = s[f"{team}_{t}"] > 0
                    w, wo = outcome_block(s[has]), outcome_block(s[~has])
                    out.append({**dict(zip(by, keys)), "stage": st, "team": name, "trait": t,
                                "share": 100 * has.mean(), **w, "pts_without": wo.get("pts", np.nan)})
    return pd.DataFrame(out)


# ---- 3c stone types --------------------------------------------------------------------------------

def single_stone(rows: pd.DataFrame, long: pd.DataFrame, shots=(1, 2, 3), min_n: int = 40) -> pd.DataFrame:
    """Positions with exactly one stone in play after stone k: the outcome by that stone's team and type."""
    s = rows[rows["shot"].isin(shots) & (rows["stones"] == 1)]
    st = long.merge(s[KEYS], on=KEYS)[KEYS + ["owner", "type"]]
    s = s.merge(st, on=KEYS)
    s["team"] = np.where(s["owner"] == 1, "hammer", "non-hammer")
    t = outcome_table(s, ["shot", "team", "type"], min_n=min_n)
    t.insert(3, "stone", t.pop("type").map(type_name))
    return t


def two_stones(rows: pd.DataFrame, long: pd.DataFrame, shots=(2,), min_n: int = 40) -> pd.DataFrame:
    """Positions with exactly two stones in play after stone k: the outcome by the pair of stone types."""
    s = rows[rows["shot"].isin(shots) & (rows["stones"] == 2)]
    st = long.merge(s[KEYS], on=KEYS)
    st["label"] = np.where(st["owner"] == 1, "H: ", "N: ") + st["type"].map(type_name)
    pair = st.sort_values("label").groupby(KEYS)["label"].agg(" / ".join).rename("pair").reset_index()
    s = s.merge(pair, on=KEYS)
    return outcome_table(s, ["shot", "pair"], min_n=min_n).sort_values(["shot", "n"], ascending=[True, False])


def type_coverage(rows: pd.DataFrame, long: pd.DataFrame) -> pd.DataFrame:
    """How many distinct stone types (team x trait vector) there are by stage, and how concentrated."""
    st = long.merge(rows[KEYS + ["stage"]], on=KEYS)
    out = []
    for _, _, name in STAGES:
        c = st[st["stage"] == name].groupby(["owner", "type"]).size().sort_values(ascending=False)
        out.append({"stage": name, "stones": int(c.sum()), "types": len(c),
                    "types_with_500+": int((c >= 500).sum()), "stones_in_top_30_%": 100 * c.head(30).sum() / c.sum(),
                    "stones_in_types_500+_%": 100 * c[c >= 500].sum() / c.sum()})
    return pd.DataFrame(out)


# ---- 3d additive grades ----------------------------------------------------------------------------

# Every stone is exactly one of open / partly open / behind cover, and nearly every stone is either in the
# house or in front of it, so those traits are folded into a per-stone base: the reference stone is an open
# guard, and every other weight is what a trait adds to a stone that has it.
REFERENCE = ("front", "open")
TERMS = ["stone"] + [t for t in TRAITS if t not in REFERENCE]
STAGE_NAMES = [name for _, _, name in STAGES]


def term_matrix(counts: pd.DataFrame) -> np.ndarray:
    """(positions, 2 x len(TERMS)): per team, the number of stones and the counts of the non-reference traits."""
    cols = []
    for team, _ in TEAMS:
        cols.append(counts[[f"{team}_{t}" for t in ("open", "partly_open", "behind_cover")]].sum(axis=1).to_numpy(float))
        cols += [counts[f"{team}_{t}"].to_numpy(float) for t in TERMS[1:]]
    return np.column_stack(cols)


def stone_terms(mask: int) -> np.ndarray:
    """The TERMS vector of one stone type (1 for the stone itself, then its non-reference traits)."""
    return np.array([1.0] + [float((int(mask) >> TRAITS.index(t)) & 1) for t in TERMS[1:]])


def _design(d: pd.DataFrame) -> np.ndarray:
    dummies = pd.get_dummies(d["stratum"] + "#" + d["shot"].astype(str), dtype=float)
    return np.hstack([term_matrix(d), dummies.to_numpy()])


def fit_weights(rows: pd.DataFrame, targets=("pts", "two", "steal"), alpha: float = 1.0) -> pd.DataFrame:
    """Per stage: linear weights of each team's stones and trait counts on the end's result (hammer points;
    the two-or-more and steal rates in percentage points), with the stone number and the situation as
    stratum effects. A stone's grade is its team's `stone` weight plus the weights of its traits."""
    from sklearn.linear_model import Ridge
    names = [(team, t) for _, team in TEAMS for t in TERMS]
    out = []
    for st in STAGE_NAMES:
        d = rows[rows["stage"] == st]
        X = _design(d)
        for tgt in targets:
            k = 1 if tgt == "pts" else 100
            coef = Ridge(alpha=alpha).fit(X, k * d[tgt].to_numpy(float)).coef_[:len(names)]
            out += [{"stage": st, "team": team, "trait": t, "target": tgt, "weight": w} for (team, t), w in zip(names, coef)]
    return pd.DataFrame(out)


def weight_table(w: pd.DataFrame, target: str = "pts") -> pd.DataFrame:
    t = w[w["target"] == target].pivot_table(index="trait", columns=["team", "stage"], values="weight")
    t = t.reindex(TERMS)[[(team, st) for _, team in TEAMS for st in STAGE_NAMES]]
    t.columns = [f"{a} {b}" for a, b in t.columns]
    return t.reset_index()


def _weights(w: pd.DataFrame, stage: str, team: str, target: str = "pts") -> np.ndarray:
    ws = w[(w["stage"] == stage) & (w["team"] == team) & (w["target"] == target)].set_index("trait")["weight"]
    return ws.reindex(TERMS).fillna(0.0).to_numpy()


def grade_card(rows: pd.DataFrame, long: pd.DataFrame, w: pd.DataFrame, top: int = 15) -> pd.DataFrame:
    """The most common stone types per stage and team, with their grade in each currency."""
    st = long.merge(rows[KEYS + ["stage"]], on=KEYS)
    targets = list(dict.fromkeys(w["target"]))
    out = []
    for name in STAGE_NAMES:
        s = st[st["stage"] == name]
        for owner, team in ((1, "hammer"), (0, "non-hammer")):
            c = s[s["owner"] == owner].groupby("type").size().sort_values(ascending=False).head(top)
            for typ, n in c.items():
                v = stone_terms(typ)
                out.append({"stage": name, "team": team, "stone": type_name(typ), "n": int(n),
                            **{f"grade_{k}": float(v @ _weights(w, name, team, k)) for k in targets}})
    return pd.DataFrame(out)


def position_grades(counts: pd.DataFrame, shot: np.ndarray, w: pd.DataFrame) -> pd.DataFrame:
    """h_grade, n_grade, net_grade (hammer points) of positions from their trait counts, with the weights of
    the stage the position's stone number falls in (stone 16 with the late weights; the empty sheet grades 0)."""
    stage = stage_of(np.clip(shot, 1, 15))                 # the last stone is graded with the late weights
    X = term_matrix(counts)
    k = len(TERMS)
    h, n = np.zeros(len(counts)), np.zeros(len(counts))
    for st in STAGE_NAMES:
        m = stage == st
        if m.any():
            h[m] = X[m, :k] @ _weights(w, st, "hammer")
            n[m] = X[m, k:] @ _weights(w, st, "non-hammer")
    return pd.DataFrame({"h_grade": h, "n_grade": n, "net_grade": h + n}, index=counts.index)


GRADE_COLUMNS = ["h_grade", "n_grade", "net_grade"]
TAP_GRADE_COLUMNS = ["tap_grade_gain"]


def attach_grades(train_rows: pd.DataFrame, parquet_root: str, n_groups: int = 5, fit_books: set | None = None,
                  groups: dict | None = None, tap: bool = False) -> pd.DataFrame:
    """The `grades` design columns: each row's pre-shot position graded with additive trait weights (hammer
    points). With `fit_books` (an experiment's training books) the weights are fitted once on those books and
    applied to every row, so held-out rows are graded by weights that never saw them. Otherwise cross-fitted:
    each book is graded with weights fitted on the other groups of books, `groups` (book -> group, the
    model's cross-validation folds) or book index mod n_groups. net_grade is the sum of the two teams'
    grades, both from the hammer team's side.
    With `tap`, also `tap_grade_gain` (set `tapgrade`): the position after the thrower's best tap
    (core/taps.py) rescored with the same weights, less the position now, from the thrower's side; both are
    graded with the weights of the thrower's stage, as in the rock ledger."""
    study = load_rows(parquet_root)
    _, wide = load_tables(parquet_root)
    counts = counts_at(train_rows, wide, "pre_source_shot")
    pre_stones = train_rows["shot"].to_numpy() - 1
    cols = GRADE_COLUMNS + (TAP_GRADE_COLUMNS if tap else [])
    out = pd.DataFrame(0.0, index=counts.index, columns=cols)
    if tap:
        from .draw_features import load_table, tap_counts_at
        after = tap_counts_at(train_rows.reset_index(drop=True), load_table(parquet_root, name="tap"))
        after = after.fillna(counts)                                  # no position to tap from: nothing changes
        sign = np.where(train_rows["thrower_has_hammer"].fillna(False).to_numpy(dtype=bool), 1.0, -1.0)
        shot = train_rows["shot"].to_numpy()

    def fill(m, w):
        out.loc[m, GRADE_COLUMNS] = position_grades(counts[m], pre_stones[m], w).to_numpy()
        if tap:
            gain = (position_grades(after[m], shot[m], w)["net_grade"] - position_grades(counts[m], shot[m], w)["net_grade"])
            out.loc[m, "tap_grade_gain"] = sign[m] * gain.to_numpy()

    if fit_books is not None:
        fill(np.ones(len(counts), dtype=bool), fit_weights(study[study["book"].isin(fit_books)], targets=("pts",)))
    else:
        books = sorted(set(study["book"]) | set(train_rows["book"]))
        group = groups if groups is not None else {b: i % n_groups for i, b in enumerate(books)}
        tg = train_rows["book"].map(group).to_numpy()
        sg = study["book"].map(group).to_numpy()
        for g in sorted(set(group.values())):
            m = tg == g
            if m.any():
                fill(m, fit_weights(study[sg != g], targets=("pts",)))
    # rounded: the matrix product's last bit depends on how many rows it is computed over (BLAS blocking),
    # and a one-ulp change moves the model's bin edges
    return train_rows.assign(**{c: out[c].to_numpy().round(9) for c in cols})


# ---- the report ------------------------------------------------------------------------------------

def _md(df: pd.DataFrame, digits: int = 2) -> str:
    return df.round(digits).to_markdown(index=False)


def _effect_view(eff: pd.DataFrame, stage: str, team: str) -> pd.DataFrame:
    e = eff[(eff["stage"] == stage) & (eff["team"] == team)]
    v = pd.DataFrame({"trait": e["trait"], "share %": e["share"], "n": e["n"], "pts": e["pts"],
                      "pts without": e["pts_without"],
                      "Δ pts": e["d_pts"].round(3).astype(str) + " ± " + e["ci_pts"].round(3).astype(str),
                      "2+ %": e["two"], "Δ 2+": e["d_two"].round(1).astype(str) + " ± " + e["ci_two"].round(1).astype(str),
                      "steal %": e["steal"], "Δ steal": e["d_steal"].round(1).astype(str) + " ± " + e["ci_steal"].round(1).astype(str)})
    return v


JAM_VS_COVER = ["partly_open", "partly_backed", "behind_cover", "backed", "frozen_own", "frozen_opp", "guarding"]


def jam_vs_cover(w: pd.DataFrame, target: str = "pts") -> pd.DataFrame:
    """The additive weights of the exposure and jam traits side by side, per stage and team (Mike Calcagno,
    2026-09-30: a jam should count about as much as partial cover). Exposure weights are relative to an open
    stone, jam weights to a stone with a clear exit behind it."""
    t = w[(w["target"] == target) & w["trait"].isin(JAM_VS_COVER)]
    t = t.pivot_table(index=["team", "stage"], columns="trait", values="weight")[JAM_VS_COVER]
    return t.reindex([(team, st) for _, team in TEAMS for st in STAGE_NAMES]).reset_index()


def write_report(parquet_root: str, reports_dir: str, inventory_csv: str | None = None, tier1: bool = False) -> str:
    rows = load_rows(parquet_root, inventory_csv, tier1)
    long, _ = load_tables(parquet_root)
    long = long.merge(rows[KEYS], on=KEYS)
    suffix = "_tier1" if tier1 else ""
    os.makedirs(reports_dir, exist_ok=True)

    base = outcome_table(rows, "stage").set_index("stage").loc[STAGE_NAMES].reset_index()
    prev = prevalence(rows)
    ov = overlap(long)
    eff = trait_effects(rows)
    eff_disc = trait_effects(rows, by=["discipline"])
    single = single_stone(rows, long)
    pairs = two_stones(rows, long)
    cov = type_coverage(rows, long)
    w = fit_weights(rows)
    card = grade_card(rows, long, w)

    eff.to_csv(os.path.join(reports_dir, f"traits_effects{suffix}.csv"), index=False)
    eff_disc.to_csv(os.path.join(reports_dir, f"traits_effects_by_discipline{suffix}.csv"), index=False)
    single.to_csv(os.path.join(reports_dir, f"traits_single_stone{suffix}.csv"), index=False)
    pairs.to_csv(os.path.join(reports_dir, f"traits_two_stones{suffix}.csv"), index=False)
    w.to_csv(os.path.join(reports_dir, f"traits_weights{suffix}.csv"), index=False)
    card.to_csv(os.path.join(reports_dir, f"traits_grade_card{suffix}.csv"), index=False)
    ov.round(3).to_csv(os.path.join(reports_dir, f"traits_overlap{suffix}.csv"))

    ends = rows.groupby(["game_key", "end"]).ngroups
    out = [f"# Rock traits{' (Tier 1)' if tier1 else ''}\n",
           "Every stone carries a vector of yes/no traits read off the position it is in (core/traits.py): "
           + ", ".join(f"`{t}`" for t in TRAITS) + ". No tracking: the question is what positions whose stones "
           "carry a trait have been worth, not what happens to the stone.\n",
           f"Rows: {len(rows):,} positions (after stones 1-15) from {ends:,} ends. The result is the end's score for the "
           "hammer team: **pts** is the mean, then steal / blank / one / two-or-more in %. **Δ** columns are the difference "
           "from positions after the same stone in the same situation (discipline, score difference to ±2, two or fewer "
           "ends left), with 95% intervals clustered by end; Δ 2+ and Δ steal are percentage points.\n",
           "## Baseline by stage\n", _md(base.drop(columns=[c for c in base if c.startswith(("d_", "ci_"))])) + "\n",
           "## 3a. How often each trait appears\n",
           "% of positions in which the team has at least one stone with the trait.\n", _md(prev, 1) + "\n",
           "Overlap between traits (Jaccard: share of stones with either trait that have both) is in `traits_overlap.csv`. "
           "Pairs above 0.5 (candidates to merge or to read together):\n",
           _md(_top_overlaps(ov)) + "\n",
           "## 3b. One trait at a time\n",
           "Positions where the team has at least one stone with the trait against the rest, at each stage. `pts without` "
           "is the mean of the rest; Δ is against the same stone and situation (both with and without are in it), so "
           "a trait that comes with more stones in play is not separated from them here: section 3d does that. "
           "By discipline: `traits_effects_by_discipline.csv`.\n"]
    for _, _, st in STAGES:
        for _, team in TEAMS:
            out += [f"### {team.title()} team, {st}\n", _md(_effect_view(eff, st, team)) + "\n"]
    out += ["## 3c. Stone types\n",
            "A stone's type is its whole trait vector (the nested rings shown once). How far exact lookup can go:\n",
            _md(cov, 1) + "\n",
            "### One stone in play\n",
            "Positions with exactly one stone in play after stone 1, 2 or 3, by that stone's team and type (40 or more).\n",
            _md(single) + "\n",
            "### Two stones in play after stone 2\n",
            "The 25 most common pairs of types (`H:` hammer team, `N:` non-hammer).\n",
            _md(pairs[pairs["shot"] == 2].head(25)) + "\n",
            "## 3d. Additive grades\n",
            "Per stage, a linear fit of the end's result on each team's trait counts, with the stone number and the "
            "situation as stratum effects. `stone` is the weight of the reference stone, an open guard (a stone in "
            "front of the house with nothing in front of it); every other weight is what that trait adds to a stone "
            "that has it, holding the others fixed. The rings are nested, so a 4-foot stone gets four_foot + "
            "eight_foot + twelve_foot. A stone's grade is `stone` plus its traits' weights, always from the hammer "
            "team's side (a non-hammer stone that helps its team has a negative grade).\n",
            "### Weights, hammer points\n", _md(weight_table(w, "pts"), 3) + "\n",
            "### Weights, two-or-more (percentage points)\n", _md(weight_table(w, "two"), 1) + "\n",
            "### Weights, steal (percentage points)\n", _md(weight_table(w, "steal"), 1) + "\n",
            "### The jam against cover\n",
            "A stone is partly backed when some of its exit cone (30 degrees either side of straight back) runs into a "
            "stone behind it, and backed when half or more does: a takeout is likely to jam. The question is whether "
            "being backed is worth about as much as being partly covered. Exposure weights are relative to an open "
            "stone, jam weights to a stone with a clear exit; a freeze is also backed, so frozen_* adds to backed. "
            "Hammer points:\n", _md(jam_vs_cover(w, "pts"), 3) + "\n",
            "Two-or-more (percentage points):\n", _md(jam_vs_cover(w, "two"), 1) + "\n",
            "### Grade card\n",
            "The most common stone types per stage and team with their grades (hammer points; two-or-more and steal in "
            "percentage points; always from the hammer team's side).\n", _md(card) + "\n"]
    path = os.path.join(reports_dir, f"traits{suffix}.md")
    with open(path, "w") as f:
        f.write("\n".join(out))
    return path


def _top_overlaps(ov: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    rows = [{"a": a, "b": b, "jaccard": ov.loc[a, b]} for i, a in enumerate(TRAITS) for b in TRAITS[i + 1:]
            if ov.loc[a, b] >= threshold]
    return pd.DataFrame(rows, columns=["a", "b", "jaccard"]).sort_values("jaccard", ascending=False)
