# Sample reports

The `reports/` directory is not committed (it holds logs, validation output and one leaderboard per book), except for this
folder, which keeps a few finished reports so that the output of the system can be read without running it. Every number
in them comes from the fitted Phase 1 models described in `shot_value_design.md`; nothing is edited by hand.

| File | What it is | Produced by |
|---|---|---|
| `model_report.md` | The model's own report card: corpus counts, hammer values, held-out accuracy, conservation, whole-corpus leaderboards and strata | `pointsgained model --features base,situation,level,intent` |
| `testset.md` | Six pinned last-rock shots from the 2026 Olympics, both currencies, used as a face-validity check whenever the model changes | `pointsgained testset` |
| `events/OWG2026_ResultsBook.md` | Per-player leaderboards for the 2026 Olympic tournaments | `pointsgained events --match OWG2026` |
| `events/WMCC2026_ResultsBook.md`, `events/WWCC2026_ResultsBook.md` | The same for the 2026 World Championships | `pointsgained events --match WMCC2026 WWCC2026` |
| `events/OWG2022_ResultsBook.md` | Beijing 2022, the tournament the design document uses for its worked examples | `pointsgained events --match OWG2022` |
| `games/..._Gold_Medal_Game_CAN-GBR.md`, `games/..._Gold_Medal_Game_SUI-SWE.md` | The two 2026 Olympic finals shot by shot | `pointsgained game --match OWG2026 Gold_Medal` |

## How a report is built

Everything starts from one table, `data/parquet/points_gained.parquet`, with one row per delivered stone (601,663 of them
over 4,154 games). For each stone the two models produce three distributions over the end's result: `D(S)`, what the
field usually gets from the position before the shot; `D(S | C)`, what the field usually gets when it makes this call
(shot type, turn, struck stone) from this position; and `D(S')`, the position after the stone came to rest. A value mapping
turns each distribution into a number, in two currencies: hammer-adjusted points (the end's expected score, with the hammer
handover priced in at H ≈ 0.58 of a point) and win probability (from the score, the ends remaining and the hammer). The
shot's value is the difference after minus before, split at the call:

- **PG: Call** = V(S | C) − V(S), what the call was worth against what the field usually does from here;
- **PG: Throw** = V(S') − V(S | C), what the delivered stone was worth against what the call usually produces;
- **PG** = the sum, signed so that a gain for the thrower's team is positive.

Because every value is a difference of model outputs on consecutive positions, the values in an end telescope: the hammer
team's total minus the other team's total is exactly the end's result minus the expectation at its start. The game reports
print that residual (it is at machine precision) and the model report checks it over the whole corpus.

The three report levels are just different groupings of that table.

**Game report** (`pointsgained game`). The substrate itself, for one game: an end-by-end table with each team's summed call
and throw values and the win probability before and after each end; a per-player table with sums over the game and each
player's best and worst stone; the ten largest win-probability swings; and every stone with its three values. This is the
report to read when a leaderboard number looks surprising, because it shows which stones produced it.

**Event leaderboard** (`pointsgained events`). One file per Results Book. Execution (PG: Throw) is the pivot, and it is
reported relative to that event's field for the same shot type and hammer state, so that a fourth who throws doubles all
week is compared with the other fourths' doubles rather than with a lead's guards. Players are grouped by throwing position,
from the throwing order, and sorted by their median shot. The columns are the ones the design settled on after the first
season of reading these tables (`shot_value_design.md`, Section 10.2): the median for the typical shot, the mean for the
tail, the tenth percentile as the floor, reliability as the share of shots at or above the field's expectation, the counts
of big misses and big makes, the sum of the five costliest shots, and the same tail in win probability. The call component
and the book's official percentage sit at the right. A team table above each position group is the shot-weighted mean.

**Model report** (`pointsgained model`). Written at the end of a full run. Its first half is about the models (accuracy held
out by book, by rocks remaining and by score difference; conservation; calibration; the win-probability table) and its second
half is the whole-corpus view: value by shot type, the top players and teams across all 92 books, and the stratified tables
by discipline, tier, hammer, game state and shot type.

## What the samples say

**The men's final, Canada 9, Great Britain 6.** The per-player table has Jacobs at +5.05 points of execution over his
twenty stones and Mouat at +3.24; the two fourths account for nearly all of either team's value, which is what the leverage
of the last two stones of every end does. The book graded Mouat at 80 percent and McMillan, Britain's lead, at 98.75; the
model has McMillan slightly negative, because a lead's fronts move the expectation by hundredths and his two tenth-end
fronts cost more than the rest of his week's stones earned. The game turned in the ninth end: Canada, one down with hammer,
scored three, and the end table shows Britain's summed throw value at −0.48 (a raise graded zero, two doubles graded 50, a
freeze graded 25) before Jacobs' clearing for three, which the model values at +0.81 points and 22.7 points of win
probability. That stone is the first row of `testset.md`. The largest swing of the game is the next end: after Mouat's
double had restored a route to two (+0.70), Jacobs' double took Britain's expectation from 1.18 to 0.05 points, 26.9 points
of win probability, and Mouat's last stone missed for the steal.

**The women's final, Sweden 6, Switzerland 5.** The report shows what the two currencies are for. Hasselborg's winning
stone, a take-out graded 100 for one point in the tenth end, has an execution value of −0.57 points and +5 points of win
probability. In the points currency the field usually gets more than one from that position, so taking one is a loss; in
win probability one point ends the game, so it is a gain. The points currency is the one to read in the middle of a game
and the win-probability currency at the end of it. The other lines worth reading are the Swiss blanks in ends two and three
(the call column credits them, the field's usual call from those positions being worth less), Paetz's fifth-end double that
held Sweden to one (the largest swing of the game at +15 points of win probability), and her missed double in the eighth
(graded 25, −12 points), the steal that decided the match.

**Milano Cortina 2026, the fields.** Among the men's fourths Schwarz-van Berkel leads by median, mean and floor, with seven
big misses against Mouat's thirteen; among the women Homan has the best median but the lowest floor and the most big misses
of the top three, the pattern the design document describes for her cycle. The team tables put Switzerland, Great Britain
and Canada in that order on the men's side, and Switzerland first on the women's.

**The 2026 Worlds.** Einarson leads every execution column among the women's fourths. On the men's side Yanagisawa has the
best median and Whyte the best mean, floor and reliability; Dunstone's five worst stones cost 3.9 points, the shortest tail
in the group. The bottom of each table shows how the tail behaves at the other end: the fourths with the lowest medians also
have floors a third to half a point deeper and three times the big-miss counts of the leaders.

**Beijing 2022.** Included because Section 10.2 of the design document builds its argument on it: Shuster's mid-pack median
and negative mean, Retornaz's low median and positive mean, and the final between the field's two most reliable fourths.
The numbers in that section are the numbers in this file.

## Things to keep in view

- **Event-relative means event-relative.** A +0.05 at the Olympics and a +0.05 at a Europeans are measured against
  different fields. The combined CSV that `pointsgained events` also writes carries `pg_throw_rel`, the same execution
  against the whole corpus, for comparisons across events.
- **The call component runs against execution in every sample event.** In all five leaderboards the teams with the best
  execution have negative call values and the teams with the worst have positive ones. A check over the whole corpus
  says this is situation, not judgement: good teams are scored on less, hold hammer less and throw from different
  situations, and within the same situation their calls are valued no differently from anyone else's. Where teams do
  separate is on the downside of the call: the best teams execute the calls with the fattest bad tail as well as their
  safe ones, and the weakest teams execute them worse. The design records this as a hypothesis still to be validated
  (Section 10.3). Read the call column as "the call the field usually makes here" and not as "the best call".
- **Points and win probability disagree at the end of a game**, by construction. The hammer value H is an infinite-horizon
  quantity and the last end has no next end. Use the `_wp` columns for anything that depends on the ends remaining.
- **The official grade and the model measure different things.** The grade counts every stone once against the caller's
  intent; the model weighs it by what it did to the end. A missed hit that leaves a better position is a miss on the sheet
  and a gain here; a perfectly executed low-leverage stone is a 100 on the sheet and a few hundredths here.
- **Coverage.** Shot-by-shot pages exist for all games in the major books and for a handful of games in some others; the
  index that `pointsgained events` writes flags the books with fewer than ten games. Leaderboards need thirty stones.
- **A label variant.** The corpus carries `Wick/Softpeeling` (120 stones) alongside `Wick / Soft Peeling`; the shot type is
  a model input, so merging them is a change for the next refit rather than a report fix.

## Regenerating

The commands in the table above write to `reports/`; copy the files here to refresh the samples. `events`, `game` and
`testset` read the Points Gained table and take seconds; `model` refits the models and takes about fifteen minutes on the
full corpus. The Results Books themselves are not part of the repository (see the README).
