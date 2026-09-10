"""Shot-difficulty model on the official grade: the skill scalar and the event effect (design 3.5, 8).

Response: grade / 100 as a fractional outcome in [0, 1].
Stage one: a gradient-boosted regressor of the grade on the shot's difficulty features (call, turn,
position features, rocks remaining, situation, discipline) gives the field's expected grade.
Stage two: a weighted logistic regression on the stage-one logit plus two event-level covariates
(the hand-rated event strength and the field strength derived from game results) and L2-penalised
dummies for team, player and book. The player coefficient is a shrunk deviation from the team,
measured against the level of the fields the player has played in; the book coefficient is what
remains of the event once field strength is accounted for, i.e. the ice, conditions and grader.
Level of play is a property of the event (Mike, 2026-09-10): team rankings only inform how strong
an event's field is, they are not a per-player covariate.

Outputs: skill per (discipline, player key), event effect per book.
"""
from __future__ import annotations

import logging
import time

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.sparse import csr_matrix, hstack
from sklearn.ensemble import HistGradientBoostingRegressor

from .features import FEATURE_NAMES
from .train import column, FEATURE_SETS

log = logging.getLogger(__name__)

DIFFICULTY_COLS = FEATURE_NAMES + ["is_women", "shot_type_code", "turn_code"] + FEATURE_SETS["situation"]


def normalise_player(name) -> str:
    return " ".join(str(name).upper().split()) if isinstance(name, str) else ""


def apply_aliases(keys: pd.Series, disciplines: pd.Series, aliases: pd.DataFrame | None) -> pd.Series:
    """Map alias player keys to their canonical key (alias table rows with keep == 'yes')."""
    if aliases is None or not len(aliases):
        return keys
    a = aliases[aliases["keep"].astype(str).str.startswith("yes")]
    m = {(d, k): c for d, k, c in zip(a["discipline"], a["alias"], a["canonical"])}
    return pd.Series([m.get((d, k), k) for d, k in zip(disciplines, keys)], index=keys.index)


def _logit(p, eps=1e-3):
    p = np.clip(p, eps, 1 - eps)
    return np.log(p / (1 - p))


def fit_difficulty(rows: pd.DataFrame, X: np.ndarray, event_strength: np.ndarray, field_strength: np.ndarray,
                   player_key: pd.Series, team_key: pd.Series | None = None, lam_player: float = 20.0, lam_team: float = 5.0,
                   lam_book: float = 5.0, lam_cov: float = 0.01, seed: int = 0) -> dict:
    """Fit on unmirrored rows with a grade. Returns skill / event / team tables, a per-shot table of
    the field difficulty logit (expected grade at skill 0: sigmoid(grade_logit_base + skill)) and diagnostics.
    `team_key` distinguishes teams that share a code (junior CAN is not senior CAN); defaults to the team code."""
    t0 = time.time()
    ok = (rows["mirror"].to_numpy() == 0) & rows["grade_pct"].notna().to_numpy()
    r = rows[ok]
    tk = (team_key if team_key is not None else rows["team"]).astype(str)
    y = (r["grade_pct"].to_numpy(dtype=float) / 100.0).clip(0, 1)
    Xd = np.column_stack([column(r, X[ok], c) for c in DIFFICULTY_COLS])
    # stage one: field expected grade from the shot's difficulty
    reg = HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, max_leaf_nodes=15, min_samples_leaf=300,
                                        l2_regularization=10.0, categorical_features=[DIFFICULTY_COLS.index("shot_type_code")],
                                        random_state=seed).fit(Xd, y)
    base = reg.predict(Xd)
    log.info("difficulty stage one fitted in %.0fs (r2 %.3f)", time.time() - t0, 1 - np.var(y - base) / np.var(y))
    # stage two: sparse design [logit(base), event_strength, team_strength, team dummies, player dummies, book dummies]
    pk = player_key[ok].to_numpy()
    teams = (r["discipline"] + "|" + tk[ok]).to_numpy()
    players = (r["discipline"] + "|" + pk).to_numpy()
    books = r["book"].to_numpy()
    t_idx, t_lv = pd.factorize(teams); p_idx, p_lv = pd.factorize(players); b_idx, b_lv = pd.factorize(books)
    n = len(r)
    es, fs = event_strength[ok], field_strength[ok]
    es = (es - np.nanmean(es)) / (np.nanstd(es) + 1e-9)
    fs = (fs - np.nanmean(fs)) / (np.nanstd(fs) + 1e-9)
    cov = np.column_stack([np.ones(n), _logit(base), np.nan_to_num(es), np.nan_to_num(fs)])
    D = hstack([csr_matrix(cov),
                csr_matrix((np.ones(n), (np.arange(n), t_idx)), shape=(n, len(t_lv))),
                csr_matrix((np.ones(n), (np.arange(n), p_idx)), shape=(n, len(p_lv))),
                csr_matrix((np.ones(n), (np.arange(n), b_idx)), shape=(n, len(b_lv)))]).tocsr()
    pen = np.concatenate([[0.0, 0.0, lam_cov, lam_cov], np.full(len(t_lv), lam_team), np.full(len(p_lv), lam_player), np.full(len(b_lv), lam_book)])

    def obj(w):
        z = D @ w
        p = 1 / (1 + np.exp(-z))
        ll = np.sum(y * z - np.logaddexp(0, z))       # fractional-response Bernoulli likelihood
        grad = D.T @ (y - p)
        return -(ll - 0.5 * np.sum(pen * w * w)), -(grad - pen * w)

    w0 = np.zeros(D.shape[1]); w0[1] = 1.0
    w = minimize(obj, w0, jac=True, method="L-BFGS-B", options={"maxiter": 500}).x
    k = 4
    w_cov, w_t, w_p, w_b = w[:k], w[k:k + len(t_lv)], w[k + len(t_lv):k + len(t_lv) + len(p_lv)], w[k + len(t_lv) + len(p_lv):]
    z = D @ w
    fitted = 1 / (1 + np.exp(-z))
    log.info("difficulty stage two fitted in %.0fs (r2 %.3f); coefficients base %.3f event-rating %.3f field-strength %.3f",
             time.time() - t0, 1 - np.var(y - fitted) / np.var(y), w_cov[1], w_cov[2], w_cov[3])
    # skill: what the thrower adds over the field of the events played, in logit units: team + player deviation
    team_of_player = pd.Series(t_idx).groupby(p_idx).agg(lambda s: s.mode().iloc[0]).to_numpy()
    shots_p = np.bincount(p_idx, minlength=len(p_lv))
    level_p = (w_cov[2] * pd.Series(np.nan_to_num(es)).groupby(p_idx).mean() + w_cov[3] * pd.Series(np.nan_to_num(fs)).groupby(p_idx).mean()).to_numpy()
    skill = w_p + w_t[team_of_player]
    players_tab = pd.DataFrame({"key": p_lv, "discipline": [s.split("|")[0] for s in p_lv], "player": [s.split("|", 1)[1] for s in p_lv],
                                "team": [t_lv[i].split("|", 1)[1] for i in team_of_player], "shots": shots_p,
                                "skill": skill, "player_dev": w_p, "team_effect": w_t[team_of_player],
                                "event_level": level_p, "grade": pd.Series(y).groupby(p_idx).mean().to_numpy() * 100})
    events_tab = pd.DataFrame({"book": b_lv, "event_effect": w_b, "shots": np.bincount(b_idx, minlength=len(b_lv))})
    # per-shot field difficulty: everything except the thrower's skill (team + player deviation + strength prior)
    base_logit = w_cov[0] + w_cov[1] * _logit(base) + w_cov[2] * np.nan_to_num(es) + w_cov[3] * np.nan_to_num(fs) + w_b[b_idx]
    shots_tab = pd.DataFrame({"game_key": r["game_key"].to_numpy(), "end": r["end"].to_numpy(), "shot": r["shot"].to_numpy(),
                              "grade_logit_base": base_logit, "grade_expected_own": fitted})
    teams_tab = pd.DataFrame({"key": t_lv, "team_effect": w_t, "shots": np.bincount(t_idx, minlength=len(t_lv))})
    return {"players": players_tab, "events": events_tab, "teams": teams_tab, "shots": shots_tab, "coef": dict(zip(["intercept", "base_logit", "event_rating", "field_strength"], w_cov)),
            "stage_one": reg, "seconds": round(time.time() - t0, 1)}


def attach_level(rows: pd.DataFrame, players_tab: pd.DataFrame, events_tab: pd.DataFrame, player_key: pd.Series,
                 shots_tab: pd.DataFrame | None = None) -> pd.DataFrame:
    """Add skill_thrower, event_effect and grade_logit_base to a row table (all rows, mirrored included).
    The design column expected_grade = sigmoid(grade_logit_base + skill_thrower) is built from these."""
    sk = players_tab.set_index("key")["skill"]
    keys = rows["discipline"] + "|" + player_key
    rows = rows.copy()
    rows["skill_thrower"] = sk.reindex(keys.to_numpy()).fillna(0.0).to_numpy()
    rows["event_effect"] = events_tab.set_index("book")["event_effect"].reindex(rows["book"].to_numpy()).fillna(0.0).to_numpy()
    if shots_tab is not None:
        gl = shots_tab.set_index(["game_key", "end", "shot"])["grade_logit_base"]
        idx = pd.MultiIndex.from_arrays([rows["game_key"], rows["end"], rows["shot"]])
        rows["grade_logit_base"] = gl.reindex(idx).to_numpy()
        med = float(np.nanmedian(rows["grade_logit_base"]))
        rows["grade_logit_base"] = rows["grade_logit_base"].fillna(med)
    return rows


def load_level(parquet_root: str, rows: pd.DataFrame, aliases_csv: str | None = None) -> pd.DataFrame:
    """Attach skill_thrower and event_effect from skill.parquet / event_effects.parquet (run `pointsgained difficulty`)."""
    import os
    sk = pd.read_parquet(os.path.join(parquet_root, "skill.parquet"))
    ev = pd.read_parquet(os.path.join(parquet_root, "event_effects.parquet"))
    sh = pd.read_parquet(os.path.join(parquet_root, "shot_difficulty.parquet"))
    aliases = pd.read_csv(aliases_csv) if aliases_csv and os.path.exists(aliases_csv) else None
    pk = apply_aliases(rows["player"].map(normalise_player), rows["discipline"], aliases)
    return attach_level(rows, sk, ev, pk, sh)


def reference_skill(rows: pd.DataFrame, skill: np.ndarray, tier: pd.Series | None = None) -> np.ndarray:
    """A reference skill per row for level-comparable reporting: the median thrower skill at the
    row's discipline and tier (discipline alone when tiers are unknown)."""
    key = rows["discipline"].astype(str) + "|" + (tier.astype(str) if tier is not None else "")
    med = pd.Series(skill).groupby(key.to_numpy()).median()
    return med.reindex(key.to_numpy()).fillna(float(np.median(skill))).to_numpy()
