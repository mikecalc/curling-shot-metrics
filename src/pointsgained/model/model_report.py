"""The model report (design Section 10): the models' report card, then the whole-corpus performance
tables under the currency rule (teams in win probability, players and shot types by execution), then
the stratified model checks. Written at the end of `pointsgained model`; `pointsgained model-report`
rewrites it from the saved run summary and the Points Gained table without refitting."""
from __future__ import annotations

import os

import pandas as pd

from . import aggregate as agg


def build_tables(pg: pd.DataFrame, reports_dir: str, min_shots: int, inventory_csv: str | None) -> tuple[dict, dict]:
    """Leaderboards and stratified tables; each is also written as CSV under reports_dir."""
    lb = {"players": agg.by_player(pg, min_shots=min_shots), "teams": agg.by_team(pg),
          "shot_types": agg.by_shot_type(pg), "shot_numbers": agg.by_shot_number(pg)}
    for k, df in lb.items():
        df.to_csv(os.path.join(reports_dir, f"leaderboard_{k}.csv"), index=False)
    pgs = agg.attach_strata(pg, inventory_csv=inventory_csv)
    strata = agg.strata_tables(pgs, min_shots_player=min_shots)
    for k, df in strata.items():
        df.to_csv(os.path.join(reports_dir, f"strata_{k}.csv"), index=False)
    return lb, strata


def write_model_report(path: str, rep: dict, lb: dict, strata: dict, min_shots: int,
                       player_rows: int = 12, player_min_shots: int = 200, team_min_games: int = 20) -> None:
    sets = rep.get("feature_sets", [])
    out = ["# Points Gained: Phase 1 model report\n",
           f"Games {rep['n_games']}, ends {rep['n_ends']}, shots {rep['n_shots']}, training rows {rep['n_rows']}. "
           f"Feature sets: {', '.join(sets)}. Run time {rep['seconds']:.0f}s.\n",
           f"Hammer outcome distribution (hammer perspective, clipped): {rep['hammer_outcome_dist']}\n",
           f"N (hammer net) = {rep['N_all']}, H (Markov hammer value) = {rep['H_all']}\n"]
    out.append("\n".join(f"- {d}: N = {rep[f'N_{d}']}, H = {rep[f'H_{d}']} over {rep[f'ends_{d}']} ends"
                         for d in ("M", "W") if f"N_{d}" in rep) + "\n")
    cv = rep["cv"]
    out.append("## Cross-validated outcome models (held out by book)\n")
    out.append("| model | log-loss | Brier |\n|---|---|---|\n" +
               "\n".join(f"| {m} | {cv[m + '_logloss']:.4f} | {cv[m + '_brier']:.4f} |" for m in ("trivial", "f", "g")) + "\n")
    out.append("Log-loss by rocks remaining (f vs trivial):\n\n| rocks remaining | n | f | trivial |\n|---|---|---|---|\n" +
               "\n".join(f"| {r} | {v['n']} | {v['f']} | {v['trivial']} |" for r, v in sorted(cv["logloss_by_rocks_remaining"].items())) + "\n")
    if "logloss_by_abs_diff" in cv:
        out.append("Log-loss by |score difference| (f vs trivial):\n\n| abs diff | n | f | trivial |\n|---|---|---|---|\n" +
                   "\n".join(f"| {r} | {v['n']} | {v['f']} | {v['trivial']} |" for r, v in sorted(cv["logloss_by_abs_diff"].items())) + "\n")
    out.append(f"## Conservation\n\nMax |sum PG - (final - start)| over ends: {rep['conservation_max_abs_residual']:.2e}; "
               f"terminal distribution equals the actual score in {100 * rep['conservation_terminal_ok_rate']:.1f}% of ends.\n")
    out.append(f"Mean V(f(S0)) = {rep['V_S0_mean']} versus H = {rep['H_used']} (calibration check).\n")
    if "wp_examples" in rep:
        out.append("## Win probability (from line scores)\n\n" + "\n".join(f"- {k}: {v}" for k, v in rep["wp_examples"].items()) + "\n")
        out.append("Regimes: " + "; ".join(f"{k}: {v}" for k, v in rep["regimes"].items()) + "\n")

    # ---- performance: the currency rule ----------------------------------------------------
    out.append("## Performance across the corpus\n")
    out.append("Two kinds of table, by the rule the reports follow. A team's standing is in win probability: its record and what "
               "its own stones did to its chance of winning, with no execution columns. A player is judged on what they were asked "
               "to throw: execution (PGAA, points gained above average) relative to the field for the same shot type and hammer "
               "state, read as a distribution rather than an average. `reliability` is the share of shots at or above the field's "
               "expectation; `avg_make` how good the shot was when above, `avg_miss` how bad when below; `big_makes_100` and "
               "`big_misses_100` are shots beyond half a point either way, per 100 shots; `net` is the mean, kept as the single "
               "number that folds these together. `net_wp` is the same execution in percentage points of win probability per "
               "shot, for reference; `call` is the call component (secondary). The full tables are in the leaderboard CSVs.\n")
    t = lb["teams"]
    t = t[t["games"] >= team_min_games].copy()
    t["record"] = t["wins"].astype(str) + "-" + t["losses"].astype(str)
    t["win rate"] = (100 * t["win_rate"]).round(0)
    t = t[["discipline", "team", "games", "record", "win rate", "wp_gain"]].rename(columns={"wp_gain": "WP gained / game"})
    out.append(f"### Teams (min {team_min_games} games)\n\nRecord and the summed effect of the team's own stones on its chance of "
               "winning, per game, in percentage points (calls and throws together), across every book the team appears in.\n\n"
               + t.round(1).to_markdown(index=False) + "\n")
    p = lb["players"]
    p = p[p["shots"] >= player_min_shots]
    cols = ["discipline", "player", "teams", "shots", "games", "reliability", "avg_make", "avg_miss",
            "big_makes_100", "big_misses_100", "net", "net_wp", "call", "grade"]
    out.append(f"### Players (min {player_min_shots} shots; top {player_rows} per position by reliability, then average miss)\n")
    for pos in ("FOURTH", "THIRD", "SECOND", "LEAD"):
        pp = p[p["position"] == pos].head(player_rows)
        if len(pp):
            out.append(f"#### {pos.title()}s\n\n" + pp[cols].round(3).to_markdown(index=False) + "\n")
    out.append("### Shot types\n\nExecution by call type against the call's own usual result (not field-relative): how often the "
               "delivered stone beat it, how good the makes and how bad the misses were, and the net (`pg_throw`).\n\n"
               + lb["shot_types"].round(3).to_markdown(index=False) + "\n")

    # ---- stratified model checks -----------------------------------------------------------
    out.append("## Stratified model checks (pg in hammer-adjusted points; _wp columns in win probability)\n")
    out.append("Mean value per shot by stratum. These are checks on the models rather than performance tables: the means "
               "should sit near zero within a stratum unless the stratum is a selection (a tier, a hammer state).\n")
    for k, title in [("discipline_tier", "By discipline and tier"), ("discipline_hammer", "By discipline and hammer"),
                     ("game_state_hammer", "By game state (thrower's view) and hammer"),
                     ("shot_type_hammer", "By shot type and hammer")]:
        out.append(f"### {title}\n\n" + strata[k].round(4).to_markdown(index=False) + "\n")
    with open(path, "w") as f:
        f.write("\n".join(out))
