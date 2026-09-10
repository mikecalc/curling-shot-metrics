"""Team strength per (nation, discipline, season) from game results: a Bradley-Terry model.

Self-contained prior for the skill scalar (design Sections 3.5 and 12). Game results come from
the ends table of every shot-by-shot book (final score after the last recorded end). Strength is
fitted per season with a ridge penalty that shrinks each nation-season towards the nation's
all-season strength, and that towards zero, so nations with few games get a cautious estimate.

`leave_out_book` refits without that book's games, so a book's shots are never valued with a
strength that saw their own outcomes.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.sparse import csr_matrix, hstack


def season_of(dates) -> np.ndarray:
    """Curling season label: the year it starts (July to June)."""
    d = pd.to_datetime(pd.Series(dates))
    return np.where(d.dt.month >= 7, d.dt.year, d.dt.year - 1).astype(int)


def game_results(tabs: dict, junior_books: set | None = None) -> pd.DataFrame:
    """One row per game: book, discipline, season, team_a, team_b, score_a, score_b, winner (a/b/None).
    Teams from junior and university books are separate nations (suffix '-J'): a junior CAN is not the senior CAN."""
    ends, games = tabs["ends"], tabs["games"]
    e = ends.sort_values(["game_key", "end"]).groupby("game_key").last()[["score_after_a", "score_after_b", "team_a", "team_b"]]
    g = games.drop_duplicates("game_key").set_index("game_key")[["book", "discipline", "date"]]
    df = e.join(g, how="inner").reset_index()
    df = df[df["score_after_a"].notna() & df["score_after_b"].notna() & df["discipline"].isin(["M", "W"])]
    df["season"] = season_of(df["date"])
    df["score_a"], df["score_b"] = df["score_after_a"].astype(int), df["score_after_b"].astype(int)
    df["winner"] = np.select([df["score_a"] > df["score_b"], df["score_b"] > df["score_a"]], ["a", "b"], None)
    if junior_books:
        j = df["book"].isin(junior_books)
        df.loc[j, "team_a"] = df.loc[j, "team_a"] + "-J"
        df.loc[j, "team_b"] = df.loc[j, "team_b"] + "-J"
    return df[["game_key", "book", "discipline", "season", "team_a", "team_b", "score_a", "score_b", "winner"]]


def fit_bradley_terry(results: pd.DataFrame, lam_season: float = 2.0, lam_nation: float = 0.5) -> pd.DataFrame:
    """Strength s[nation, season] = u[nation] + v[nation, season]; P(a beats b) = sigmoid(s_a - s_b).
    Penalty: lam_nation * |u|^2 + lam_season * |v|^2. Returns one row per (nation, season) with
    strength, the nation mean and game counts. Fitted per discipline."""
    out = []
    for disc, r in results.groupby("discipline"):
        r = r[r["winner"].notna()]
        nations = sorted(set(r["team_a"]) | set(r["team_b"]))
        ns = sorted(set(zip(r["team_a"], r["season"])) | set(zip(r["team_b"], r["season"])))
        ni = {n: i for i, n in enumerate(nations)}
        si = {k: i for i, k in enumerate(ns)}
        n, m, G = len(nations), len(ns), len(r)
        rows = np.repeat(np.arange(G), 2)
        a, b = r["team_a"].to_numpy(), r["team_b"].to_numpy()
        se = r["season"].to_numpy()
        U = csr_matrix((np.tile([1.0, -1.0], G), (rows, np.concatenate([[ni[x], ni[y]] for x, y in zip(a, b)]))), shape=(G, n))
        V = csr_matrix((np.tile([1.0, -1.0], G), (rows, np.concatenate([[si[(x, s)], si[(y, s)]] for x, y, s in zip(a, b, se)]))), shape=(G, m))
        X = hstack([U, V]).tocsr()
        y = (r["winner"].to_numpy() == "a").astype(float)
        pen = np.concatenate([np.full(n, lam_nation), np.full(m, lam_season)])

        def obj(w):
            z = X @ w
            ll = np.sum(y * z - np.logaddexp(0, z))
            grad = X.T @ (y - 1 / (1 + np.exp(-z)))
            return -(ll - 0.5 * np.sum(pen * w * w)), -(grad - pen * w)

        w = minimize(obj, np.zeros(n + m), jac=True, method="L-BFGS-B").x
        u, v = w[:n], w[n:]
        played = pd.concat([r[["team_a", "season"]].rename(columns={"team_a": "nation"}),
                            r[["team_b", "season"]].rename(columns={"team_b": "nation"})]).groupby(["nation", "season"]).size()
        for (nation, s), i in si.items():
            out.append({"discipline": disc, "nation": nation, "season": int(s), "strength": float(u[ni[nation]] + v[i]),
                        "nation_mean": float(u[ni[nation]]), "games": int(played.get((nation, s), 0))})
    return pd.DataFrame(out)


def junior_books_from_inventory(inventory_csv: str) -> set:
    inv = pd.read_csv(inventory_csv)
    fam = inv["event_family"].astype(str).str.lower()
    j = inv[fam.str.contains("junior") | fam.str.contains("univ") | inv["file_name"].str.startswith(("WJCC", "WU"))]
    return set(j["file_name"].str.replace(r"\.pdf$", "", regex=True))


def strength_table(tabs: dict, junior_books: set | None = None, leave_out_book: str | None = None, **kw) -> pd.DataFrame:
    res = game_results(tabs, junior_books)
    if leave_out_book is not None:
        res = res[res["book"] != leave_out_book]
    return fit_bradley_terry(res, **kw)


def _lookup(rows: pd.DataFrame, table: pd.DataFrame, nation: pd.Series) -> np.ndarray:
    key = table.set_index(["discipline", "nation", "season"])["strength"]
    mean = table.drop_duplicates(["discipline", "nation"]).set_index(["discipline", "nation"])["nation_mean"]
    season = season_of(rows["date"])
    s = key.reindex(pd.MultiIndex.from_arrays([rows["discipline"], nation, season])).to_numpy()
    fallback = mean.reindex(pd.MultiIndex.from_arrays([rows["discipline"], nation])).to_numpy()
    return np.where(np.isnan(s), np.where(np.isnan(fallback), 0.0, fallback), s)


def strength_for_rows(rows: pd.DataFrame, tabs: dict, junior_books: set | None = None, leave_out: bool = True, **kw) -> np.ndarray:
    """Strength of the thrower's nation in the season of the shot: the nation mean when the season
    is unseen, 0 when the nation is unseen. With leave_out, each book's rows use a fit without that
    book's games, so no shot is described by a strength that saw its own outcomes."""
    jb = junior_books or set()
    nation = rows["team"].astype(str) + np.where(rows["book"].isin(jb), "-J", "")
    out = np.zeros(len(rows))
    if not leave_out:
        return _lookup(rows, strength_table(tabs, jb, **kw), nation)
    for book, idx in rows.groupby("book").indices.items():
        t = strength_table(tabs, jb, leave_out_book=book, **kw)
        out[idx] = _lookup(rows.iloc[idx], t, nation.iloc[idx])
    return out


def field_strength_by_book(rows: pd.DataFrame, tabs: dict, junior_books: set | None = None, **kw) -> pd.DataFrame:
    """Mean Bradley-Terry strength of the teams in each book, in the book's season, from a fit that
    leaves that book's games out: an objective measure of how strong the event's field was. One row
    per (book, discipline). Nations unseen elsewhere get the lowest strength seen in the fit."""
    jb = junior_books or set()
    out = []
    u = rows[rows["mirror"] == 0] if "mirror" in rows else rows
    for book, grp in u.groupby("book"):
        t = strength_table(tabs, jb, leave_out_book=book, **kw)
        for disc, g in grp.groupby("discipline"):
            teams = sorted(set(g["team"].astype(str)))
            season = int(season_of(g["date"].iloc[:1])[0])
            td = t[t["discipline"] == disc]
            floor = float(td["strength"].min()) if len(td) else 0.0
            sub = pd.DataFrame({"discipline": disc, "team": teams, "date": g["date"].iloc[0], "book": book})
            nation = sub["team"] + ("-J" if book in jb else "")
            vals = _lookup(sub, t, nation)
            known = td.set_index("nation").index
            vals = np.where(nation.isin(known).to_numpy(), vals, floor)
            out.append({"book": book, "discipline": disc, "season": season, "n_teams": len(teams),
                        "field_strength": float(np.mean(vals)), "top4_strength": float(np.mean(np.sort(vals)[-4:]))})
    return pd.DataFrame(out)
