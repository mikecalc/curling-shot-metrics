"""The front-end diagnostic (early-end positions): are leads', seconds' and early thirds' execution values
measuring execution, and does the model price the configurations a skip reads?

Four parts, all from the Points Gained table, the feature cache and the canonical stones, no refit:
- measurement: repeatability, agreement with grades (a check only; grades never enter the models),
  the shared team component between positions, and the spread of values per stone;
- configuration calibration: for each configuration label and band of rocks remaining, the model's
  value of the position against the realised value of the end;
- scenario probes: one call family from one kind of position, split by what the shot left, with the
  model's credit against the realised gap between those outcomes;
- configuration survival: what a configuration leaves the opponent, as how often it survives the next
  stone and what the end was worth when it survived or was wrecked, with the field's double rate on a
  pair of hammer stones by separation and stagger;
- style check: how much of a team's front-end execution is explained by what it calls and from where.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

from ..core.configurations import LABELS, MEASURES
from .aggregate import POSITION_NAMES, normalise_player
from .config_features import load_table, pre_and_post

BANDS = [(13, 16, "16-13"), (9, 12, "12-9"), (5, 8, "8-5"), (1, 4, "4-1")]
HIT_CALLS = {"Take-out", "Hit and Roll"}
PEEL_CALLS = {"Double Take-out", "Clearing", "Wick / Soft Peeling", "Wick/Softpeeling", "Take-out"}
GUARD_CALLS = {"Guard", "Front"}
DRAW_CALLS = {"Draw", "Freeze"}
GUARD_COLS = ["own_guard_left", "own_guard_center", "own_guard_right", "opp_guard_left", "opp_guard_center", "opp_guard_right"]
FEATURE_COLS = ["own_in_house", "opp_in_house", "count"] + GUARD_COLS


# ---- assembly ----------------------------------------------------------------------------------

def load_frame(parquet_root: str) -> pd.DataFrame:
    """One row per unmirrored shot: the Points Gained values, the pre-shot features, the post-shot features
    (the next shot's pre-shot row), the configuration labels before and after (`pre_*`, `post_*`), the
    realised value of the end in both currencies, and the event-relative execution."""
    pg = pd.read_parquet(os.path.join(parquet_root, "points_gained.parquet"))
    feats = pd.read_parquet(os.path.join(parquet_root, "features.parquet"))
    feats = feats.reset_index(drop=True)
    post_feats = feats.loc[feats["post_row"].clip(lower=0), FEATURE_COLS].reset_index(drop=True)
    post_feats.loc[feats["post_row"].to_numpy() < 0] = np.nan
    post_feats.columns = ["post_" + c for c in FEATURE_COLS]
    feats = pd.concat([feats, post_feats], axis=1)
    feats = feats[feats["mirror"] == 0][["game_key", "end", "shot", "pre_source_shot", "has_post"] + FEATURE_COLS
                                        + list(post_feats.columns)]
    df = pg.merge(feats, on=["game_key", "end", "shot"], how="left")

    pre, post = pre_and_post(df, load_table(parquet_root), df["has_post"])
    for c in LABELS + MEASURES:
        df["pre_" + c] = pre[c].to_numpy()
        df["post_" + c] = post[c].to_numpy()

    last = pg[pg["is_last_shot"]][["game_key", "end", "V_post", "V_post_wp"]].rename(
        columns={"V_post": "real_v", "V_post_wp": "real_wp"})
    df = df.merge(last.drop_duplicates(["game_key", "end"]), on=["game_key", "end"], how="left")
    D = np.vstack(df["D_post"].to_numpy())
    df["model_p_steal"] = D[:, :3].sum(axis=1)
    df["model_p_two"] = D[:, 5:].sum(axis=1)
    df["real_steal"] = (df["end_score_hammer"] < 0).astype(float)
    df["real_two"] = (df["end_score_hammer"] >= 2).astype(float)
    df["player_key"] = df["player"].map(normalise_player)
    df["pos_code"] = ((((df["shot"] + 1) // 2) + 1) // 2).clip(1, 4)
    df["position"] = df["pos_code"].map(POSITION_NAMES)
    keys = ["book", "discipline", "shot_type", "thrower_has_hammer"]
    df["rel"] = df["pg_throw"] - df.groupby(keys, observed=True)["pg_throw"].transform("mean")
    df["rel_wp"] = df["pg_throw_wp"] - df.groupby(keys, observed=True)["pg_throw_wp"].transform("mean")
    return df[~df["post_missing"]].reset_index(drop=True)


# ---- measurement -------------------------------------------------------------------------------

def _spearman(a: pd.Series, b: pd.Series) -> float:
    ok = a.notna() & b.notna()
    return float(a[ok].corr(b[ok], method="spearman")) if ok.sum() > 2 else float("nan")


def split_half(df: pd.DataFrame, value: str, min_half: int = 40) -> pd.DataFrame:
    """Per player and event, the mean of `value` over odd and even games (the player's own game order)."""
    d = df[df["player_key"] != ""]
    order = d.groupby(["player_key", "book"])["game_key"].rank(method="dense").astype(int) % 2
    g = d.assign(half=order).groupby(["player_key", "book", "half"])[value].agg(["mean", "size"]).unstack("half")
    g = g[(g[("size", 0)] >= min_half) & (g[("size", 1)] >= min_half)]
    return pd.DataFrame({"a": g[("mean", 0)], "b": g[("mean", 1)]})


def opponent_same_game(d: pd.DataFrame) -> dict:
    """Spearman between the two teams' mean execution (and mean grade) at one position in the same game.
    Execution measured against a model that prices the positions correctly should not see-saw between
    opponents; grades rise and fall together with the ice."""
    g = d.groupby(["game_key", "team"]).agg(rel=("rel", "mean"), grade_pct=("grade_pct", "mean")).reset_index()
    pair = g.merge(g, on="game_key")
    pair = pair[pair["team_x"] != pair["team_y"]]
    return {c: _spearman(pair[c + "_x"], pair[c + "_y"]) for c in ("rel", "grade_pct")}


def next_stone(df: pd.DataFrame) -> pd.DataFrame:
    """Spearman between a stone's execution and the next stone's in the same end. A mispriced position
    credits one stone and charges the next: the see-saw shows as a negative lag-one correlation."""
    s = df[["game_key", "end", "shot", "rel"]]
    m = s.merge(s.assign(shot=s["shot"] - 1), on=["game_key", "end", "shot"], suffixes=("", "_next"))
    return m.groupby("shot").apply(lambda x: _spearman(x["rel"], x["rel_next"]), include_groups=False).rename("next_stone").reset_index()


def measurement(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """(by position, by stone, team-event correlation between positions)."""
    rows = []
    for code, name in POSITION_NAMES.items():
        d = df[df["pos_code"] == code]
        opp = opponent_same_game(d)
        sh, shw, shg = split_half(d, "rel"), split_half(d, "rel_wp"), split_half(d, "grade_pct")
        pl = d[d["player_key"] != ""].groupby(["player_key", "book"]).agg(rel=("rel", "mean"), grade=("grade_pct", "mean"),
                                                                           n=("rel", "size"))
        pl = pl[pl["n"] >= 80]
        rows.append(dict(position=name.title(), shots=len(d), player_events=len(sh),
                         repeatability=_spearman(sh["a"], sh["b"]),
                         repeatability_wp=_spearman(shw["a"], shw["b"]),
                         grade_repeatability=_spearman(shg["a"], shg["b"]),
                         grade_agreement_player=_spearman(pl["rel"], pl["grade"]),
                         grade_agreement_shot=_spearman(d["pg_throw"], d["grade_pct"]),
                         opponent_same_game=opp["rel"], opponent_same_game_grade=opp["grade_pct"]))
    by_pos = pd.DataFrame(rows)
    by_stone = df.groupby("shot").apply(lambda s: pd.Series(dict(
        sd=s["pg_throw"].std(), sd_wp_pp=100 * s["pg_throw_wp"].std(), mean_abs=s["pg_throw"].abs().mean(),
        grade_agreement=_spearman(s["pg_throw"], s["grade_pct"]))), include_groups=False).reset_index()
    by_stone = by_stone.merge(next_stone(df), on="shot", how="left")
    te = df.groupby(["book", "team", "position"])["rel"].mean().unstack()
    te = te[[POSITION_NAMES[k] for k in (1, 2, 3, 4)]]
    te.columns = [c.title() for c in te.columns]
    return by_pos, by_stone, te.corr(method="spearman")


# ---- configuration calibration -----------------------------------------------------------------

def calibration(df: pd.DataFrame, min_n: int = 200) -> pd.DataFrame:
    """For each configuration label (before the shot) and band of rocks remaining: the model's value of the
    position against the realised value of the end, in points (hammer-adjusted) and win probability."""
    rr = 17 - df["shot"]
    rows = []
    for lab in LABELS:
        m = df["pre_" + lab]
        for lo, hi, band in BANDS:
            s = df[m & rr.between(lo, hi)]
            if len(s) < min_n:
                continue
            rows.append(dict(configuration=lab, rocks_left=band, n=len(s),
                             model_v=s["V_pre"].mean(), real_v=s["real_v"].mean(),
                             gap=s["real_v"].mean() - s["V_pre"].mean(),
                             model_wp=100 * s["V_pre_wp"].mean(), real_wp=100 * s["real_wp"].mean(),
                             gap_wp_pp=100 * (s["real_wp"].mean() - s["V_pre_wp"].mean())))
    return pd.DataFrame(rows)


# ---- scenario probes ---------------------------------------------------------------------------

def _guards(df: pd.DataFrame, prefix: str = "") -> pd.Series:
    return df[[prefix + c for c in GUARD_COLS]].sum(axis=1)


def probe_table(s: pd.DataFrame, state: pd.Series) -> pd.DataFrame:
    """One row per outcome state: the model's value after the shot and the execution it credited, against
    the realised value of the end and the realised steal and two-or-more rates."""
    s = s.assign(state=state)
    s = s[s["state"].notna()]
    t = s.groupby("state").agg(
        n=("shot", "size"), model_v_after=("V_post", "mean"), real_v=("real_v", "mean"),
        pg_throw=("pg_throw", "mean"), model_wp_after=("V_post_wp", "mean"), real_wp=("real_wp", "mean"),
        pg_throw_wp_pp=("pg_throw_wp", "mean"), model_p_steal=("model_p_steal", "mean"),
        real_p_steal=("real_steal", "mean"), model_p_two=("model_p_two", "mean"), real_p_two=("real_two", "mean"),
        grade=("grade_pct", "mean")).reset_index()
    for c in ("model_wp_after", "real_wp", "pg_throw_wp_pp"):
        t[c] = 100 * t[c]
    return t


def probes(df: pd.DataFrame) -> list[tuple[str, str, pd.DataFrame]]:
    """(title, description, table) per scenario."""
    out = []
    ham, shot, call = df["thrower_has_hammer"], df["shot"], df["shot_type"]

    m = ham & shot.between(6, 14) & (df["own_in_house"] == 1) & (df["opp_in_house"] == 1) & (_guards(df) == 0) & call.isin(HIT_CALLS)
    s = df[m]
    st = pd.Series(np.select(
        [s["post_split_flat"], s["post_split_staggered"], (s["post_own_in_house"] >= 2) & (s["post_opp_in_house"] == 0),
         (s["post_own_in_house"] == 1) & (s["post_opp_in_house"] == 0), s["post_opp_in_house"] >= 1],
        ["split restored, flat", "split restored, staggered", "two in, not split", "rolled out (one in)", "opponent still in"],
        "other"), index=s.index)
    out.append(("Split house restored, and the walk", "Hammer team's hit, stones 6-14, one stone each in the house and no guards. "
                "The make restores the split; whether it restores a flat split (the double nearly off) or a staggered one "
                "(the walked split, double on) is what the opponent is left.", probe_table(s, st)))

    for d_h, label in ((0, "tied"), (-1, "down one")):
        m = ham & shot.between(5, 8) & (df["ends_remaining"] == 1) & (df["diff_hammer"] == d_h) & (_guards(df) >= 2) & call.isin(PEEL_CALLS)
        s = df[m]
        g0, g1 = _guards(s), _guards(s, "post_")
        st = pd.Series(np.select([g1 == 0, g1 < g0, g1 >= g0], ["all guards gone", "one or more removed", "none removed"], None),
                       index=s.index).where(g1.notna())
        out.append((f"Peel with hammer, last end, {label}", f"Hammer team's peel, double or take-out, stones 5-8, last end {label} "
                    "with hammer, two or more guards up. The peel gives up points expectation to take the steal away; the "
                    "question is whether the second is credited for that in win probability, and charged for the miss.",
                    probe_table(s, st)))

    m = ham & shot.between(4, 8) & df["pre_own_corner_guard"] & ~df["pre_own_shot"] & call.isin(DRAW_CALLS)
    s = df[m]
    st = pd.Series(np.select([s["post_own_shot_covered"], s["post_own_shot"]], ["shot rock, covered", "shot rock, open"], "not shot rock"),
                   index=s.index)
    out.append(("Come-around behind a corner guard", "Hammer team's draw or freeze, stones 4-8, with its own corner guard up "
                "and not lying shot.", probe_table(s, st)))

    m = ~ham & shot.isin([1, 3]) & call.isin(GUARD_CALLS)
    s = df[m]
    cg = s["post_opp_guard_center"] > s["opp_guard_center"]
    ih = s["post_opp_in_house"] > s["opp_in_house"]
    st = pd.Series(np.select([cg, ih], ["centre guard placed", "in the house"], "neither (through or corner)"), index=s.index)
    out.append(("Centre guard without hammer", "Non-hammer team's guard or front, stones 1 and 3.", probe_table(s, st)))

    m = ~ham & shot.between(9, 14) & df["pre_opp_shot"] & ~df["pre_opp_two_plus"] & ~df["pre_steal_on"] \
        & (df["pre_swing_if_shot_removed"] >= 2)
    for lo, hi, stake in ((2, 2, "the hammer team counts one behind"), (3, 9, "the hammer team counts two or more behind (a lonely steal)")):
        s = df[m & df["pre_swing_if_shot_removed"].between(lo, hi)]
        guarded = s["post_steal_on"] & s["post_opp_shot"]
        tight = (s["post_shot_runback_angle"] <= 35) & (s["post_shot_runback_dist"] < 96)
        st = pd.Series(np.select(
            [guarded & tight, guarded, s["post_opp_shot"] & (s["post_own_in_house"] < s["own_in_house"]), s["post_own_shot"]],
            ["guarded tight (runback from under 8 ft)", "guarded long", "hammer stone removed", "hammer now lies shot"], "other"),
            index=s.index)
        out.append((f"Guard the steal or take the house: {stake}", "Non-hammer team to throw, stones 9-14, lying one in the open "
                    f"with {stake}. Guard it and keep the steal (a tight guard, under 8 ft in front, leaves the easier runback), or remove a hammer "
                    "stone and settle for holding the hammer team to less.", probe_table(s, st)))

    m = ham & shot.between(10, 14) & df["pre_steal_on"]
    s = df[m]
    st = pd.Series(np.select([s["post_own_shot"], s["post_steal_on"]], ["hammer lies shot", "steal still on (covered)"],
                             "opponent shot, open"), index=s.index)
    out.append(("The steal is on", "Hammer team to throw, stones 10-14, the opponent lying shot behind cover. Any call.",
                probe_table(s, st)))
    return out


# ---- what a configuration leaves the opponent -----------------------------------------------

def survival(df: pd.DataFrame, min_n: int = 200) -> pd.DataFrame:
    """For each configuration before a stone, by who throws it: how often it survives that stone, and what
    the end was worth (hammer team's view) when it survived or was wrecked, realised and as the model
    valued the position left. A configuration whose realised gap exceeds the model's gap is one the model
    under-credits keeping and under-charges losing."""
    rows = []
    for lab in LABELS:
        if lab == "empty":
            continue
        for ham in (False, True):
            s = df[df["pre_" + lab] & (df["thrower_has_hammer"] == ham) & (df["shot"] < 16)]
            if len(s) < min_n:
                continue
            kept = s["post_" + lab]
            if kept.all() or not kept.any():
                continue
            rv, mv = s["real_v"], s["V_post"]
            rows.append(dict(configuration=lab, thrower="hammer" if ham else "non-hammer", n=len(s), survives=kept.mean(),
                             real_kept=rv[kept].mean(), real_wrecked=rv[~kept].mean(),
                             real_gap=rv[kept].mean() - rv[~kept].mean(),
                             model_gap=mv[kept].mean() - mv[~kept].mean(),
                             real_gap_wp_pp=100 * (s["real_wp"][kept].mean() - s["real_wp"][~kept].mean()),
                             model_gap_wp_pp=100 * (s["V_post_wp"][kept].mean() - s["V_post_wp"][~kept].mean())))
    return pd.DataFrame(rows)


def double_table(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """How often the non-hammer team's hit removes both stones when the hammer team has two in the house and
    the opponent none, by the pair's separation and stagger (percent, and counts)."""
    m = (~df["thrower_has_hammer"]) & (df["own_in_house"] == 2) & (df["opp_in_house"] == 0) & df["shot"].between(5, 15) \
        & df["shot_type"].isin(HIT_CALLS | {"Double Take-out"}) & (df["pre_own_pair_sep"] >= 24)
    s = df[m].assign(sep=pd.cut(df["pre_own_pair_sep"], [24, 36, 48, 72, 200], labels=["2-3 ft", "3-4 ft", "4-6 ft", "6 ft+"]),
                     stagger=pd.cut(df["pre_own_pair_angle"], [-1, 10, 20, 35, 55, 90],
                                    labels=["<10°", "10-20°", "20-35°", "35-55°", "55-90°"]),
                     both_gone=(df["post_own_in_house"] == 0).astype(float))
    rate = 100 * s.pivot_table(index="sep", columns="stagger", values="both_gone", aggfunc="mean", observed=False)
    n = s.pivot_table(index="sep", columns="stagger", values="both_gone", aggfunc="size", observed=False)
    return rate, n


def runback_table(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """How often a runback (Promotion Take-out) on the opponent's shot rock leaves the thrower's team lying shot,
    by the angle of the best runback off the line of delivery and the distance of the stone in front (percent,
    and counts)."""
    thrower_opp_shot = np.where(df["thrower_has_hammer"], df["pre_opp_shot"], df["pre_own_shot"])
    thrower_shot_after = np.where(df["thrower_has_hammer"], df["post_own_shot"], df["post_opp_shot"])
    m = thrower_opp_shot & (df["shot_type"] == "Promotion Take-out") & (df["pre_shot_runback_angle"] <= 35)
    s = df[m].assign(angle=pd.cut(df["pre_shot_runback_angle"], [-0.1, 5, 10, 20, 35], labels=["<5°", "5-10°", "10-20°", "20-35°"]),
                     distance=pd.cut(df["pre_shot_runback_dist"], [0, 48, 96, 144, 180], labels=["<4 ft", "4-8 ft", "8-12 ft", "12-15 ft"]),
                     made=thrower_shot_after[m].astype(float))
    rate = 100 * s.pivot_table(index="distance", columns="angle", values="made", aggfunc="mean", observed=False)
    n = s.pivot_table(index="distance", columns="angle", values="made", aggfunc="size", observed=False)
    return rate, n


def runback_players(df: pd.DataFrame, min_runbacks: int = 40) -> pd.DataFrame:
    """Runbacks by player across the corpus: Promotion Take-outs on the opponent's shot rock with a stone in
    front (either team's) within 35 degrees. How many, how many were angled (10 degrees or more) and from a
    busy house, how often the thrower's team lay shot afterwards, execution relative to the event's field
    (points), the effect on win probability (percentage points per runback) and the big makes (execution
    above half a point). Sorted by execution."""
    thrower_opp_shot = np.where(df["thrower_has_hammer"], df["pre_opp_shot"], df["pre_own_shot"])
    thrower_shot_after = np.where(df["thrower_has_hammer"], df["post_own_shot"], df["post_opp_shot"])
    m = thrower_opp_shot & (df["shot_type"] == "Promotion Take-out") & (df["pre_shot_runback_angle"] <= 35) & (df["player_key"] != "")
    s = df[m].assign(made=thrower_shot_after[m].astype(float), angled=(df["pre_shot_runback_angle"] >= 10).astype(float),
                     busy=df["pre_busy_house"].astype(float))
    t = s.groupby(["discipline", "player_key"]).agg(
        runbacks=("made", "size"), teams=("team", lambda x: "/".join(sorted(set(x)))), angled=("angled", "mean"),
        busy=("busy", "mean"), lies_shot=("made", "mean"), execution=("rel", "mean"), wp_pp=("pg_throw_wp", "mean"),
        big_makes=("rel", lambda x: int((x > 0.5).sum())), grade=("grade_pct", "mean")).reset_index()
    t = t[t["runbacks"] >= min_runbacks]
    t["wp_pp"] = 100 * t["wp_pp"]
    return t.sort_values("execution", ascending=False)


# ---- style check -------------------------------------------------------------------------------

def style_check(df: pd.DataFrame, min_stones: int = 60) -> dict:
    """How much of a team's front-end execution at an event is explained by what it calls and from where
    (its mix of call types and pre-shot configurations), and the lead-second correlation before and after."""
    d = df[df["pos_code"].isin([1, 2])]
    mix_cols = ["pre_" + k for k in LABELS]
    X_calls = pd.get_dummies(d["shot_type"].where(d["shot_type"].isin(d["shot_type"].value_counts().index[:8]), "other"),
                             prefix="call").astype(float)
    feats = pd.concat([d[["book", "team", "position", "rel"]], d[mix_cols].astype(float), X_calls], axis=1)
    g = feats.groupby(["book", "team", "position"])
    te = g.mean()
    te["n"] = g.size()
    te = te[te["n"] >= min_stones]
    res = {}
    resid = {}
    for pos in ("LEAD", "SECOND"):
        t = te.xs(pos, level="position")
        X = t.drop(columns=["rel", "n"]).to_numpy()
        X = np.column_stack([np.ones(len(X)), (X - X.mean(0)) / np.where(X.std(0) > 0, X.std(0), 1)])
        y = t["rel"].to_numpy()
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        r = y - X @ beta
        res[f"r2_{pos.lower()}"] = float(1 - r.var() / y.var())
        resid[pos] = pd.Series(r, index=t.index)
        res[f"team_events_{pos.lower()}"] = len(t)
    both = pd.concat({"raw_l": te.xs("LEAD", level="position")["rel"], "raw_s": te.xs("SECOND", level="position")["rel"],
                      "res_l": resid["LEAD"], "res_s": resid["SECOND"]}, axis=1).dropna()
    res["lead_second_raw"] = _spearman(both["raw_l"], both["raw_s"])
    res["lead_second_residual"] = _spearman(both["res_l"], both["res_s"])
    return res


# ---- report ------------------------------------------------------------------------------------

def write_report(df: pd.DataFrame, reports_dir: str) -> str:
    by_pos, by_stone, te_corr = measurement(df)
    cal = calibration(df)
    prb = probes(df)
    sty = style_check(df)
    surv = survival(df)
    dbl_rate, dbl_n = double_table(df)
    rb_rate, rb_n = runback_table(df)
    rb_players = runback_players(df)
    rb_players.to_csv(os.path.join(reports_dir, "front_end_runback_players.csv"), index=False)
    surv.to_csv(os.path.join(reports_dir, "front_end_survival.csv"), index=False)
    by_pos.to_csv(os.path.join(reports_dir, "front_end_positions.csv"), index=False)
    by_stone.to_csv(os.path.join(reports_dir, "front_end_stones.csv"), index=False)
    cal.to_csv(os.path.join(reports_dir, "front_end_calibration.csv"), index=False)
    pd.concat([t.assign(scenario=name) for name, _, t in prb]).to_csv(os.path.join(reports_dir, "front_end_probes.csv"), index=False)

    out = ["# Front end: what early-end execution values measure\n",
           f"{len(df):,} shots with a post-shot position. Execution is `pg_throw` relative to the event's field for the same "
           "shot type and hammer state. Grades appear only as a check; they are never a model input.\n",
           "## Measurement by position\n",
           "`repeatability`: Spearman between a player's mean execution in their odd and even games at an event (40+ shots in "
           "each half). `grade_agreement_player`: Spearman between a player-event's mean execution and mean grade (80+ shots). "
           "`grade_agreement_shot`: Spearman between a shot's execution and its grade. `opponent_same_game`: Spearman between "
           "the two teams' mean execution at the position in the same game, and the same for grades.\n",
           by_pos.round(3).to_markdown(index=False) + "\n",
           "Team-event correlation of mean execution between positions (a shared component that is not the player's):\n",
           te_corr.round(2).to_markdown() + "\n",
           "Spread of execution per stone (points, and percentage points of win probability), agreement with the grade, and "
           "`next_stone`, the correlation with the next stone's execution in the same end (negative: the see-saw of a mispriced "
           "position):\n",
           by_stone.round(3).to_markdown(index=False) + "\n",
           "## Style check (leads and seconds)\n",
           "Team-event mean execution regressed on the team's mix of calls and pre-shot configurations at that position.\n",
           "\n".join(f"- {k}: {v:.3f}" if isinstance(v, float) else f"- {k}: {v}" for k, v in sty.items()) + "\n",
           "## Configuration calibration\n",
           "For each configuration before the shot and band of rocks remaining: the model's value of the position (`model_v`, "
           "hammer-adjusted points, hammer team's view) against the realised value of the end (`real_v`), and the same in win "
           "probability (percent). A configuration the field converts better than the model expects has a positive gap.\n",
           cal.round(3).to_markdown(index=False) + "\n",
           "## What each configuration leaves the opponent\n",
           "Before a stone (not the last), by who throws it: how often the configuration survives the stone, and the end's "
           "realised value (hammer-adjusted points, hammer team's view) when it survived and when it was wrecked. `model_gap` "
           "is the model's gap between the positions left; where `real_gap` is larger, the model under-credits keeping the "
           "configuration and under-charges losing it. The `_wp_pp` columns are the same gaps in percentage points of win "
           "probability.\n",
           surv.round(3).to_markdown(index=False) + "\n",
           "The double on a split: how often the non-hammer team's hit removes both hammer stones (hammer two in the house, "
           "the opponent none; percent), by the separation of the pair and its stagger from level:\n",
           dbl_rate.round(0).to_markdown() + "\n\nCounts:\n\n" + dbl_n.to_markdown() + "\n",
           "The runback on the shot rock: how often a Promotion Take-out on the opponent's shot rock leaves the thrower's "
           "team lying shot (percent), by the angle of the stone in front off the line of delivery and its distance in front:\n",
           rb_rate.round(0).to_markdown() + "\n\nCounts:\n\n" + rb_n.to_markdown() + "\n",
           "Runbacks by player (40 or more across the corpus): `angled` and `busy` are the shares of their runbacks at 10 "
           "degrees or more and from a house with four or more stones; `lies_shot` how often their team lay shot after; "
           "`execution` the mean relative to the event's field for the same call and hammer state (points); `wp_pp` the "
           "effect on win probability per runback; `big_makes` runbacks worth half a point or more above the field. The top "
           "and bottom fifteen per discipline:\n",
           "\n".join(f"### {d}\n\n" + pd.concat([g.head(15), g.tail(15)]).drop_duplicates().round(3).to_markdown(index=False) + "\n"
                     for d, g in rb_players.groupby("discipline")),
           "## Scenario probes\n",
           "One call family from one kind of position, split by what the shot left. `model_v_after` and `model_wp_after` are "
           "the model's value of the position the shot left; `real_v` and `real_wp` what the ends from those positions were "
           "actually worth; `pg_throw` and `pg_throw_wp_pp` the execution credited. Where the model's gap between two states is "
           "smaller than the realised gap, it under-credits the make and under-charges the miss.\n"]
    for name, desc, t in prb:
        out.append(f"### {name}\n\n{desc}\n\n" + t.round(3).to_markdown(index=False) + "\n")
    path = os.path.join(reports_dir, "front_end.md")
    with open(path, "w") as f:
        f.write("\n".join(out))
    return path
