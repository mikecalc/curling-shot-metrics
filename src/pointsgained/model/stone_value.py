"""The life and value of a stone (design Section 4, the stone-value study).

`build_lives` follows every stone of every end through the diagrams (core/tracking.py) and writes
`stone_lives.parquet`: one row per stone per diagram, with the stone's identity, team (hammer or not),
position, how it got there, and whether it counted and was shot rock when the end was over.

From the lives, the **future value** of a stone: what a stone of a given team, in a given place, with a
given number of rocks still to come, ends up doing when the end is over. Three roles: it counts, it
covers a counting stone of its own team, or it backs up a counting stone of the other team. A guard
earns its value by covering, a stone behind the tee is as likely to back up the opponent as to count.
It is the skip's sense that some stones matter and some can be ignored, measured from the field's play.
`position_features` sums the roles per team for every position (cross-fitted by book) for the models.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

from ..core.tracking import Frame, track_end

KEYS = ["game_key", "end"]


def _book_extras(parquet_root: str, books: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Delivered flags for stones and prior-position rings, from each book's raw stones table."""
    dl, pr = [], []
    for b in books:
        p = os.path.join(parquet_root, b, "stones.parquet")
        if not os.path.exists(p):
            continue
        st = pd.read_parquet(p, columns=["game_key", "end", "shot", "kind", "x_in", "y_in", "delivered"])
        st["game_key"] = b + "|" + st["game_key"]
        s = st[st["kind"] == "stone"]
        dl.append(s[s["delivered"].fillna(False).astype(bool)][["game_key", "end", "shot", "x_in", "y_in"]])
        pr.append(st[st["kind"] == "prior"][["game_key", "end", "shot", "x_in", "y_in"]])
    return (pd.concat(dl, ignore_index=True) if dl else pd.DataFrame(columns=["game_key", "end", "shot", "x_in", "y_in"]),
            pd.concat(pr, ignore_index=True) if pr else pd.DataFrame(columns=["game_key", "end", "shot", "x_in", "y_in"]))


def build_lives(parquet_root: str) -> pd.DataFrame:
    stones = pd.read_parquet(os.path.join(parquet_root, "stones_canonical.parquet"))
    rows = pd.read_parquet(os.path.join(parquet_root, "features.parquet"),
                           columns=["game_key", "end", "shot", "mirror", "book", "has_post", "is_last_shot"])
    rows = rows[rows["mirror"] == 0].sort_values(["game_key", "end", "shot"])
    delivered, priors = _book_extras(parquet_root, sorted(rows["book"].unique()))
    dkey = set(zip(delivered["game_key"], delivered["end"], delivered["shot"],
                   delivered["x_in"].round(3), delivered["y_in"].round(3)))
    pidx = priors.groupby(["game_key", "end", "shot"]).indices
    px, py = priors["x_in"].to_numpy(float), priors["y_in"].to_numpy(float)
    sidx = stones.groupby(["game_key", "end", "shot"]).indices
    sx, sy, so = stones["x"].to_numpy(float), stones["y"].to_numpy(float), stones["owner"].to_numpy(int)
    empty = np.zeros(0)
    out = []
    for (gk, e), grp in rows.groupby(KEYS, sort=False):
        frames = []
        for shot, has_post in zip(grp["shot"].to_numpy(), grp["has_post"].to_numpy()):
            if not has_post:
                continue                                   # no diagram: the next one is compared with the last seen
            i = sidx.get((gk, e, shot), [])
            x, y, o = sx[i], sy[i], so[i]
            d = np.array([(gk, e, shot, round(a, 3), round(b, 3)) in dkey for a, b in zip(x, y)], dtype=bool)
            pi = pidx.get((gk, e, shot), [])
            frames.append(Frame(int(shot), x, y, o, d, px[pi] if len(pi) else empty, py[pi] if len(pi) else empty))
        if not frames:
            continue
        complete = bool(grp["is_last_shot"].to_numpy()[-1] and grp["has_post"].to_numpy()[-1])
        recs = track_end(frames)
        for r in recs:
            r["game_key"], r["end"], r["end_complete"] = gk, e, complete
        out.extend(recs)
    lives = pd.DataFrame(out)
    lives["rocks_remaining"] = 16 - lives["shot"]
    return lives


def load_lives(parquet_root: str, rebuild: bool = False) -> pd.DataFrame:
    path = os.path.join(parquet_root, "stone_lives.parquet")
    src = os.path.join(parquet_root, "stones_canonical.parquet")
    if not rebuild and os.path.exists(path) and os.path.getmtime(path) >= os.path.getmtime(src):
        return pd.read_parquet(path)
    lives = build_lives(parquet_root)
    lives.to_parquet(path, index=False)
    return lives


# ---- roles at the end of the end ----------------------------------------------------------------

STONE_DIAMETER_IN = 11.4
BANDS = [(0, 3), (4, 7), (8, 11), (12, 15)]
ROLES = ["r_count", "r_cover", "r_backs_opp"]
CB_ROLES = ["r_count", "r_cover_h", "r_cover_n", "r_back_h", "r_back_n"]     # colour-blind cover and backing
ZONES = ["house front 4ft", "house front 8-12", "house back 4ft", "house back 8-12",
         "centre guard <6ft", "centre guard long", "corner guard <6ft", "corner guard long", "out"]


def final_roles(lives: pd.DataFrame) -> pd.DataFrame:
    """Per (game_key, end, sid) in the end's final diagram: whether the stone counts, covers a counting
    stone of its own team (in front of it within a stone's width, not counting itself), or backs up a
    counting stone of the other team (behind it within two stone widths)."""
    from ..core.tracking import count_ids
    L = lives[lives["end_complete"]]
    last = L[L["shot"] == L.groupby(KEYS)["shot"].transform("max")]
    out = []
    for (g, e), grp in last.groupby(KEYS, sort=False):
        x, y, o, sid = grp["x"].to_numpy(), grp["y"].to_numpy(), grp["owner"].to_numpy(), grp["sid"].to_numpy()
        idx, _ = count_ids(x, y, o)
        cnt = np.zeros(len(x), dtype=bool)
        cnt[idx] = True
        dx, dy = np.abs(x[:, None] - x[None, :]), y[:, None] - y[None, :]         # [i, j]: stone i relative to j
        same = o[:, None] == o[None, :]
        cover = (~cnt) & ((same & cnt[None, :] & (dy > STONE_DIAMETER_IN / 2) & (dx <= STONE_DIAMETER_IN)).any(axis=1))
        backs = ((~same) & cnt[None, :] & (dy < 0) & (np.hypot(dx, dy) <= 2 * STONE_DIAMETER_IN)).any(axis=1)
        # colour-blind: a stone in front of a counter covers it, and a stone just behind a counter backs it,
        # for whichever team the counter belongs to (a beaked shooter is cover for the other side)
        in_front = (~cnt)[:, None] & cnt[None, :] & (dy > STONE_DIAMETER_IN / 2) & (dx <= STONE_DIAMETER_IN)
        behind = (~cnt)[:, None] & cnt[None, :] & (dy < 0) & (np.hypot(dx, dy) <= 2 * STONE_DIAMETER_IN)
        ham_counter = (o == 1)[None, :]
        out.append(pd.DataFrame({"game_key": g, "end": e, "sid": sid, "r_count": cnt, "r_cover": cover, "r_backs_opp": backs,
                                 "r_cover_h": (in_front & ham_counter).any(axis=1), "r_cover_n": (in_front & ~ham_counter).any(axis=1),
                                 "r_back_h": (behind & ham_counter).any(axis=1), "r_back_n": (behind & ~ham_counter).any(axis=1)}))
    return pd.concat(out, ignore_index=True)


def zone_of(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    d = np.hypot(x, y)
    return np.select([(d <= 29.7) & (y >= 0), (d <= 77.7) & (y >= 0), (d <= 29.7) & (y < 0), d <= 77.7,
                      (y > 0) & (np.abs(x) <= 24) & (y <= 150), (y > 0) & (np.abs(x) <= 24), (y > 0) & (y <= 150), y > 0],
                     ZONES[:8], "out")


def band_of(rocks_remaining: np.ndarray) -> np.ndarray:
    return np.select([rocks_remaining <= hi for _, hi in BANDS], list(range(len(BANDS))), len(BANDS) - 1)


def cells(frame: pd.DataFrame) -> pd.DataFrame:
    """Cell keys for stones: team, band of rocks remaining, zone, and a 1-ft cell (|x|, y) inside it."""
    x, y = frame["x"].to_numpy(float), frame["y"].to_numpy(float)
    return pd.DataFrame({"owner": frame["owner"].to_numpy(int), "band": band_of(frame["rocks_remaining"].to_numpy()),
                         "zone": zone_of(x, y), "cx": np.minimum(np.abs(x) // 12, 8).astype(int),
                         "cy": np.clip((y + 72) // 12, 0, 30).astype(int)}, index=frame.index)


def role_tables(lives_roles: pd.DataFrame, prior: float = 100.0, roles: list[str] = ROLES) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(zone table, cell table): the rate of each role by team, band and zone, and by 1-ft cell shrunk
    towards its zone's rate with `prior` pseudo-stones."""
    c = cells(lives_roles).join(lives_roles[roles].astype(float))
    z = c.groupby(["owner", "band", "zone"])[roles].mean()
    cc = c.groupby(["owner", "band", "zone", "cx", "cy"])[roles].agg(["sum", "count"])
    zr = z.reindex(cc.index.droplevel(["cx", "cy"])).to_numpy()
    n = cc.xs("count", axis=1, level=1).to_numpy()
    s = cc.xs("sum", axis=1, level=1).to_numpy()
    shrunk = (s + prior * zr) / (n + prior)
    return z, pd.DataFrame(shrunk, index=cc.index, columns=roles)


STONE_FEATURES = ["own_ev_count", "own_ev_cover", "own_ev_backs_opp", "opp_ev_count", "opp_ev_cover", "opp_ev_backs_opp",
                  "own_best_sleeper", "opp_best_sleeper"]


def _lookup(frame: pd.DataFrame, z: pd.DataFrame, cell: pd.DataFrame) -> np.ndarray:
    c = cells(frame)
    ci = pd.MultiIndex.from_frame(c[["owner", "band", "zone", "cx", "cy"]])
    v = cell.reindex(ci).to_numpy()
    zi = pd.MultiIndex.from_frame(c[["owner", "band", "zone"]])
    vz = z.reindex(zi).to_numpy()
    v = np.where(np.isnan(v), vz, v)
    return np.nan_to_num(v)


def position_features(lives: pd.DataFrame, n_groups: int = 5) -> pd.DataFrame:
    """Per post-shot position (game_key, end, shot): each team's summed expected roles and its best stone
    not counting now (the highest chance of counting at the end among its stones not counting yet).
    Cross-fitted: a book's positions are valued with tables built from the other groups of books."""
    from ..core.tracking import count_ids
    lives = lives.copy()
    lives["book"] = lives["game_key"].str.split("|").str[0]
    books = sorted(lives["book"].unique())
    group = {b: i % n_groups for i, b in enumerate(books)}
    lives["grp"] = lives["book"].map(group)
    roles = final_roles(lives)
    # every stone of a complete end has a role row; a stone removed before the end did none of the three
    lr = lives[lives["end_complete"]].merge(roles, on=KEYS + ["sid"], how="left")
    all_roles = sorted(set(ROLES) | set(CB_ROLES))
    lr[all_roles] = lr[all_roles].fillna(False).astype(bool)
    vals = np.zeros((len(lives), len(ROLES)))
    cb = np.zeros((len(lives), len(CB_ROLES)))
    for g in range(n_groups):
        tr = lr[lr["grp"] != g]
        m = (lives["grp"] == g).to_numpy()
        z, cell = role_tables(tr)
        vals[m] = _lookup(lives[m], z, cell)
        z, cell = role_tables(tr, roles=CB_ROLES)
        cb[m] = _lookup(lives[m], z, cell)
    lives[["v_count", "v_cover", "v_backs"]] = vals
    ham = (lives["owner"] == 1).to_numpy()
    # colour-blind potential: counting stays with the stone's colour, cover and backing go to the team whose
    # counter the stone ends up protecting or supporting
    lives["pot_h"] = np.where(ham, cb[:, 0], 0.0) + cb[:, 1] + cb[:, 3]
    lives["pot_n"] = np.where(~ham, cb[:, 0], 0.0) + cb[:, 2] + cb[:, 4]
    # stones counting now, per position
    now = np.zeros(len(lives), dtype=bool)
    for _, idx in lives.groupby(KEYS + ["shot"], sort=False).indices.items():
        k, _s = count_ids(lives["x"].to_numpy()[idx], lives["y"].to_numpy()[idx], lives["owner"].to_numpy()[idx])
        now[idx[k]] = True
    lives["sleeper"] = np.where(now, 0.0, lives["v_count"])
    agg = lives.groupby(KEYS + ["shot", "owner"])[["v_count", "v_cover", "v_backs", "sleeper"]].agg(
        {"v_count": "sum", "v_cover": "sum", "v_backs": "sum", "sleeper": "max"}).unstack("owner", fill_value=0.0)
    out = pd.DataFrame(index=agg.index)
    for who, o in (("own", 1), ("opp", 0)):
        for name, col in (("ev_count", "v_count"), ("ev_cover", "v_cover"), ("ev_backs_opp", "v_backs")):
            out[f"{who}_{name}"] = agg[(col, o)] if (col, o) in agg.columns else 0.0
        out[f"{who}_best_sleeper"] = agg[("sleeper", o)] if ("sleeper", o) in agg.columns else 0.0
    pots = lives.groupby(KEYS + ["shot"])[["pot_h", "pot_n"]].sum()
    out = out.join(pots)
    return out.reset_index()


def load_position_features(parquet_root: str, rebuild: bool = False) -> pd.DataFrame:
    path = os.path.join(parquet_root, "stone_features.parquet")
    lives_path = os.path.join(parquet_root, "stone_lives.parquet")
    if not rebuild and os.path.exists(path) and os.path.exists(lives_path) and os.path.getmtime(path) >= os.path.getmtime(lives_path):
        return pd.read_parquet(path)
    feats = position_features(load_lives(parquet_root))
    feats.to_parquet(path, index=False)
    return feats


POTENTIAL_FEATURES = ["own_pot", "opp_pot", "net_pot"]
POTENTIAL_CB_FEATURES = ["h_pot_cb", "n_pot_cb", "net_pot_cb"]      # colour-blind cover and backing


def attach_stones(rows: pd.DataFrame, feats: pd.DataFrame) -> pd.DataFrame:
    """The `stones` and `potential` design columns for training rows, from each row's pre-shot position (the
    post position of `pre_source_shot`; zeros for the empty sheet). Rock potential per team is the stones'
    chance of counting or covering a counter of their own team, less their chance of backing up a counter
    of the other team; `net_pot` is the hammer team's less the other team's."""
    t = feats.set_index(["game_key", "end", "shot"])[STONE_FEATURES]
    idx = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["pre_source_shot"]])
    v = t.reindex(idx).fillna(0.0).to_numpy()
    out = rows.assign(**{c: v[:, i] for i, c in enumerate(STONE_FEATURES)})
    own = out["own_ev_count"] + out["own_ev_cover"] - out["own_ev_backs_opp"]
    opp = out["opp_ev_count"] + out["opp_ev_cover"] - out["opp_ev_backs_opp"]
    out = out.assign(own_pot=own.to_numpy(), opp_pot=opp.to_numpy(), net_pot=(own - opp).to_numpy())
    if "pot_h" in feats:
        cbt = feats.set_index(["game_key", "end", "shot"])[["pot_h", "pot_n"]].reindex(idx).fillna(0.0).to_numpy()
        out = out.assign(h_pot_cb=cbt[:, 0], n_pot_cb=cbt[:, 1], net_pot_cb=cbt[:, 0] - cbt[:, 1])
    return out


REGIME_FEATURES = ["reg_steal", "reg_single", "reg_deuce",
                   "x_opp_cover_steal", "x_opp_count_steal", "x_own_count_deuce", "x_own_cover_deuce"]


def attach_regime(rows: pd.DataFrame, wp_table) -> pd.DataFrame:
    """The `regime` design columns: what the game makes each result worth to the hammer team, from the
    win-probability table (a steal of one against a blank, a single against a blank, a deuce against a
    single), and their products with the stone roles, so that a non-hammer guard can be worth more when
    a steal is what that team needs. Needs the `stones` columns."""
    from .value import IDX
    d = rows["diff_hammer"].to_numpy(int)
    n = rows["ends_remaining"].to_numpy(int)
    pairs = {}
    for k in set(zip(d, n)):
        v = wp_table.v_vector(int(k[0]), int(k[1]))
        pairs[k] = (v[IDX[0]] - v[IDX[-1]], v[IDX[1]] - v[IDX[0]], v[IDX[2]] - v[IDX[1]])
    arr = np.array([pairs[k] for k in zip(d, n)])
    out = rows.assign(reg_steal=arr[:, 0], reg_single=arr[:, 1], reg_deuce=arr[:, 2])
    return out.assign(x_opp_cover_steal=out["opp_ev_cover"] * out["reg_steal"],
                      x_opp_count_steal=out["opp_ev_count"] * out["reg_steal"],
                      x_own_count_deuce=out["own_ev_count"] * out["reg_deuce"],
                      x_own_cover_deuce=out["own_ev_cover"] * out["reg_deuce"])


def load_wp_table(parquet_root: str):
    """The win-probability table from every book's line scores (as `pointsgained model` builds it)."""
    from .winprob import build_table, ends_from_line_scores
    ls = []
    for b in sorted(os.listdir(parquet_root)):
        f = os.path.join(parquet_root, b, "line_scores.parquet")
        if os.path.exists(f):
            df = pd.read_parquet(f)
            if len(df):
                df["game_key"] = b + "|" + df["game_key"].astype(str)
                ls.append(df)
    return build_table(ends_from_line_scores(pd.concat(ls, ignore_index=True)))


# ---- the stone study report ------------------------------------------------------------------------

def _counting_now(lives: pd.DataFrame) -> np.ndarray:
    from ..core.tracking import count_ids
    now = np.zeros(len(lives), dtype=bool)
    x, y, o = lives["x"].to_numpy(), lives["y"].to_numpy(), lives["owner"].to_numpy()
    for _, idx in lives.groupby(KEYS + ["shot"], sort=False).indices.items():
        k, _s = count_ids(x[idx], y[idx], o[idx])
        now[idx[k]] = True
    return now


def calibration_by_stage(pg: pd.DataFrame) -> pd.DataFrame:
    """Calibration slope of the end's realised value on the model's value before each stone, by stage of
    the end (1 is right; under 1 the model's values are flatter than the results)."""
    last = pg[pg["is_last_shot"]][KEYS + ["V_post"]].rename(columns={"V_post": "real"})
    d = pg.merge(last.drop_duplicates(KEYS), on=KEYS)
    d["rr"] = 17 - d["shot"]
    rows = []
    for lo, hi in ((12, 16), (8, 11), (4, 7), (1, 3)):
        s = d[d["rr"].between(lo, hi)]
        rows.append(dict(rocks_left=f"{hi}-{lo}", n=len(s), slope=float(np.cov(s["V_pre"], s["real"])[0, 1] / s["V_pre"].var()),
                         model_sd=float(s["V_pre"].std())))
    return pd.DataFrame(rows)


def write_report(parquet_root: str, reports_dir: str) -> str:
    lives = load_lives(parquet_root)
    comp = lives[lives["end_complete"]].copy()
    roles = final_roles(comp)
    lr = comp.merge(roles, on=KEYS + ["sid"], how="left")
    lr[ROLES] = lr[ROLES].fillna(False).astype(bool)
    c = cells(lr)
    lr["zone"], lr["band"] = c["zone"], c["band"]
    lr["team"] = np.where(lr["owner"] == 1, "hammer", "non-hammer")
    band_names = {i: f"{hi}-{lo} left" for i, (lo, hi) in enumerate(BANDS)}
    lr["stage"] = lr["band"].map(band_names)
    role_tab = (100 * lr.groupby(["team", "zone", "stage"])[ROLES].mean()).round(1)
    role_tab["n"] = lr.groupby(["team", "zone", "stage"]).size()
    role_tab = role_tab.reset_index()
    role_tab.to_csv(os.path.join(reports_dir, "stones_roles.csv"), index=False)
    early = role_tab[role_tab["stage"] == band_names[3]].drop(columns="stage")

    # late risers: stones in play after stone 8 that count at the end, and whether they counted then
    s8 = lr[lr["shot"] == 8].copy()
    s8["counting_then"] = _counting_now(s8)
    risers = s8[s8["r_count"]]
    riser_share = float((~risers["counting_then"]).mean())
    riser_zones = (100 * risers[~risers["counting_then"]]["zone"].value_counts(normalize=True)).round(1).rename("share").reset_index()

    status = (100 * lives["status"].value_counts(normalize=True)).round(1)
    cal_now = calibration_by_stage(pd.read_parquet(os.path.join(parquet_root, "points_gained.parquet"),
                                                   columns=KEYS + ["shot", "V_pre", "V_post", "is_last_shot"]))
    old_path = os.path.join(parquet_root, "points_gained_v1_final.parquet")
    cal = cal_now.rename(columns={"slope": "slope (current model)", "model_sd": "sd (current)"})
    if os.path.exists(old_path):
        cal_old = calibration_by_stage(pd.read_parquet(old_path, columns=KEYS + ["shot", "V_pre", "V_post", "is_last_shot"]))
        cal["slope (final-label model)"] = cal_old["slope"].to_numpy()
        cal["sd (final-label)"] = cal_old["model_sd"].to_numpy()

    out = ["# The life of a stone\n",
           f"Every stone of every end followed through the diagrams: {len(lives):,} stone positions over "
           f"{lives.groupby(KEYS).ngroups:,} ends, {comp.groupby(KEYS).ngroups:,} of them with a final diagram. "
           f"How each stone got to where it is after a shot: unmoved {status.get('unmoved', 0)}%, the thrown stone "
           f"(marked) {status.get('thrown', 0)}%, new without a mark {status.get('new', 0)}% (almost all thrown stones "
           f"whose marker is missing), moved {status.get('moved', 0)}%.\n",
           "## What a stone ends up doing\n",
           "For a stone at a given place and stage of the end, the share that, when the end is over, **count**, "
           "**cover** a counting stone of their own team (in front of it within a stone's width, not counting "
           "themselves), or **back up** a counting stone of the other team (behind it within two stone widths). "
           "A stone removed before the end does none of the three. Stones with 12 or more rocks still to come:\n",
           early.to_markdown(index=False) + "\n",
           "A non-hammer stone behind the tee backs up an opponent's counter about as often as it counts itself; "
           "the same stone in front of the tee counts three times as often as it helps the other side. Guards "
           "almost never count themselves; their value is in covering. The full table by stage of the end is in "
           "`stones_roles.csv`.\n",
           "## Late risers\n",
           f"Of the stones in play after stone 8 that count when the end is over, {100 * riser_share:.0f}% were not "
           "counting then: a stone left in play that became a counter. Where they were after stone 8:\n",
           riser_zones.to_markdown(index=False) + "\n",
           "## How flat is the model?\n",
           "The calibration slope of the end's realised value (hammer-adjusted points) on the model's value before "
           "each stone, by stage of the end. At 1 the model's differences between positions are the right size; "
           "under 1 they are too small. `sd` is the spread of the model's values.\n",
           cal.round(3).to_markdown(index=False) + "\n"]
    path = os.path.join(reports_dir, "stones.md")
    with open(path, "w") as f:
        f.write("\n".join(out))
    return path


# ---- the potential ledger --------------------------------------------------------------------------

LEDGER_COLUMNS = ["pot_h_before", "pot_n_before", "pot_h", "pot_n", "build", "address", "net_change", "total"]


def ledger_frame(shots: pd.DataFrame, feats: pd.DataFrame) -> pd.DataFrame:
    """Per stone: each team's rock potential (colour-blind) before and after it, and the thrower's view of
    the change. `build` is the rise in the thrower's team's potential, `address` the fall in the other
    team's, `net_change` their sum; `total` is both teams' potential after the stone, the end's temperature.
    `shots` needs game_key, end, shot, pre_source_shot, has_post and thrower_has_hammer; a position absent
    from `feats` is the empty sheet when the shot has a diagram, unknown otherwise."""
    t = feats.set_index(["game_key", "end", "shot"])[["pot_h", "pot_n"]]
    after = t.reindex(pd.MultiIndex.from_arrays([shots["game_key"], shots["end"], shots["shot"]])).to_numpy()
    before = t.reindex(pd.MultiIndex.from_arrays([shots["game_key"], shots["end"], shots["pre_source_shot"]])).to_numpy()
    before = np.nan_to_num(before)                                     # the empty sheet, or a position with no stones
    has_post = shots["has_post"].fillna(False).to_numpy(dtype=bool)
    after = np.where(np.isnan(after) & has_post[:, None], 0.0, after)
    ham = shots["thrower_has_hammer"].to_numpy(dtype=bool)
    own_b, opp_b = np.where(ham, before[:, 0], before[:, 1]), np.where(ham, before[:, 1], before[:, 0])
    own_a, opp_a = np.where(ham, after[:, 0], after[:, 1]), np.where(ham, after[:, 1], after[:, 0])
    out = shots[["game_key", "end", "shot"]].copy()
    out["pot_h_before"], out["pot_n_before"] = before[:, 0], before[:, 1]
    out["pot_h"], out["pot_n"] = after[:, 0], after[:, 1]
    out["build"] = own_a - own_b
    out["address"] = opp_b - opp_a
    out["net_change"] = out["build"] + out["address"]
    out["total"] = after[:, 0] + after[:, 1]
    return out


def potential_ledger(parquet_root: str) -> pd.DataFrame:
    """The ledger for every stone of the corpus (`potential_ledger.parquet`)."""
    rows = pd.read_parquet(os.path.join(parquet_root, "features.parquet"),
                           columns=["game_key", "end", "shot", "mirror", "pre_source_shot", "has_post", "thrower_has_hammer"])
    rows = rows[rows["mirror"] == 0].drop(columns="mirror")
    led = ledger_frame(rows, load_position_features(parquet_root))
    led.to_parquet(os.path.join(parquet_root, "potential_ledger.parquet"), index=False)
    return led
