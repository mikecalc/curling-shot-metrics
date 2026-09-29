"""The life of a stone: stone tracking and the stone study (`pointsgained stones`, reports/stones.md).

`build_lives` follows every stone of every end through the diagrams (core/tracking.py) and writes
`stone_lives.parquet`: one row per stone per diagram, with the stone's identity, team (hammer or not),
position, how it got there, and whether it counted and was shot rock when the end was over. The lives
serve studies that need to know what happened to a particular stone (peels, runbacks, late risers).

`final_roles` says what each stone was doing when the end was over: counting, covering a counter of its
own team, or backing up a counter of the other team; `role_tables` gives the rates by team, zone and
stage. These rates were once summed into "rock potential" as a model input; the model now reads rocks
by their traits instead (model/trait_features.py, model/ledger.py), and the potential code is at the tag
handcrafted-features-final.
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
    thrown = lives[lives["status"] == "thrown"]
    marked = round(100 * float(thrown["marked"].mean()), 1) if "marked" in lives and len(thrown) else 0.0
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
           f"{status.get('thrown', 0)}% ({marked}% of them marked on the diagram, the rest the one new stone of the "
           f"thrower's colour), new {int((lives['status'] == 'new').sum()):,} stones (origin unknown), moved {status.get('moved', 0)}%.\n",
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
