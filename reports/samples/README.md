# Sample reports

This folder keeps a few finished reports so that the output of the system can be read without running it. Every number
in them comes from the corpus and the fitted expectation models described in `shot_value_design.md` (Parts II to IV); nothing is edited by hand. The expectation models read positions rock by rock (Part II of the design document).

| File | What it is | Produced by |
|---|---|---|
| `model_report.md` | The model's own report card: corpus counts, hammer values, held-out accuracy, conservation, whole-corpus leaderboards and strata | `pointsgained model` (the adopted rock-trait feature sets and the local target are the defaults) |
| `traits.md` | The rock-trait study: every rock's yes/no traits, what positions whose rocks carry each trait have been worth by team and stage, one- and two-rock positions by type, and the additive rock grades | `pointsgained traits` (also writes the rock ledger used by `game` and `events`) |
| `front_end.md` | The early-end study: what front-end execution values measure (repeatability, the see-saw, agreement with grades), configuration calibration and survival, the field's double and runback rates by geometry, runbacks by player, and scenario probes | `pointsgained frontend` |
| `stones.md` | The stone study: every stone followed through the end, what stones end up doing (count, cover, back up the opponent), late risers, and how flat the model is by stage of the end | `pointsgained stones` |
| `testset.md` | Six pinned last-rock shots from the 2026 Olympics, both currencies, used as a face-validity check whenever the model changes | `pointsgained testset` |
| `events/` (index in `events/README.md`) | Per-player leaderboards for every Tier 1 event since 2018: the Olympics of 2018, 2022 and 2026 and the men's and women's World Championships of 2018, 2019 and 2021 to 2026 (none were held in 2020), nineteen books | `pointsgained events --match OWG2018 OWG2022 OWG2026 WMCC2018 WMCC2019 WMCC2021 ... WWCC2026` (each book named) |
| `games/..._Gold_Medal_Game_CAN-GBR.md`, `games/..._Gold_Medal_Game_SUI-SWE.md` | The two 2026 Olympic finals shot by shot | `pointsgained game --match OWG2026 Gold_Medal` |

## How a report is built

Everything starts from one table, `data/parquet/points_gained.parquet`, with one row per delivered stone (609,653 of them
over 4,154 games, including the 7,990 stones of ends scored X, where the trailing team ran out of rocks: they have no end
score, so the models never train on them, but they are valued, and the last of them carries the game's result). For each stone the two models produce three distributions over the end's result: `D(S)`, what the
field usually gets from the position before the shot; `D(S | C)`, what the field usually gets when it makes this call
(shot type, turn, struck stone) from this position; and `D(S')`, the position after the stone came to rest. A value mapping
turns each distribution into a number, in two currencies: hammer-adjusted points (the end's expected score, with the hammer
handover priced in at H ≈ 0.58 of a point) and win probability (from the score, the ends remaining and the hammer). The
shot's value is the difference after minus before, split at the call:

- **PG: Call** = V(S | C) − V(S), what the call was worth against what the field usually does from here;
- **PG: Throw** = V(S') − V(S | C), what the delivered stone was worth against what the call usually produces;
- **PG** = the sum, signed so that a gain for the thrower's team is positive.

The game reports label the execution part **PGAA**, points gained above average; the leaderboards and the model report
call the same quantity `pg_throw`. Which currency leads depends on the level of the table: team-level tables (the ends of
a game) are in win probability, because that is what a team plays for; individual tables (players, shots, leaderboards)
lead with execution in hammer-adjusted points, because a player is judged on what they were asked to throw, with the
effect on win probability beside it for reference.

Because every value is a difference of model outputs on consecutive positions, the values in an end telescope: the hammer
team's total minus the other team's total is exactly the end's result minus the expectation at its start. The game reports
print that residual (it is at machine precision) and the model report checks it over the whole corpus.

The three report levels are just different groupings of that table.

**Game report** (`pointsgained game`). The substrate itself, for one game. An end-by-end table with the running score,
one team's chance of winning before and after each end, and the swing, and nothing else. A players table about execution:
each player's PGAA summed over the game, their worst and best stones by the same measure, the book's grade, and their
stones' summed effect on the team's chance of winning as a reference. The ten largest swings. And every stone in the order
situation (the end header and the throwing team's chance before the stone), shot (type, turn, grade), execution (PGAA and
the call's value, in hammer-adjusted points) and effect (the chance after the stone and the change). Within an end the two
teams' changes net exactly to the end's swing; the report warns only if they do not. Beside the values every stone carries
the rock ledger: each team's rock grade after the stone (its rocks read afresh by their traits), and the stone's build (its
own team's grade up) and address (the other team's grade down). This is the report to read when a
leaderboard number looks surprising, because it shows which stones produced it.

**Event leaderboard** (`pointsgained events`). One file per Results Book. Execution (PG: Throw) is the pivot, and it is
reported relative to that event's field for the same shot type and hammer state, so that a fourth who throws doubles all
week is compared with the other fourths' doubles rather than with a lead's guards. Players are grouped by throwing position,
from the throwing order, and sorted by `net`, their mean execution over every shot against the field's expectation, then by
reliability, the share of their shots at or above it. The execution block reads the player's distribution as well as its average (`shot_value_design.md`,
Section 11.2): reliability, the average make and the average miss, and `net`, which folds the three together; then the big shots: the counts of big makes and big misses and the sum of the
five costliest shots. The effect on win
probability follows for reference: shots that gained or cost five or more points, and the five best and five worst stones
summed. The call component and the book's official percentage sit at the right. The team table above the position groups
follows the team-level rule, in win probability per game and with no execution columns: `net` is the record (a win +50, a
loss -50) and the sort, and it adds up from `dsc` (the start from first-end hammer, won in the draw shot challenge or by
seeding), `own` and `allowed` (the team's and the other team's stones, each against this field's stones at the same point
of the end) and `other` (what no stone accounts for: concessions between ends, a missing page or a misread score header);
`control`, the mean chance of winning at the start of each end, is the second sort and credits the team that leads early
and keeps the game quiet.

**Model report** (`pointsgained model`, or `pointsgained model-report` to rewrite it from the saved run without refitting).
Its first half is about the models (accuracy held out by book, by rocks remaining and by score difference; conservation;
calibration; the win-probability table). Its second half is the whole-corpus performance view under the same rule as the
other reports: a team table in win probability (record, win rate and the same per-game columns as the event reports,
`net`, `dsc`, `own`, `allowed`, `other` and `control`, across every book the team appears in), a player table per position with the execution block
(reliability, average make, average miss, big makes and misses per 100 shots, net, with the win-probability version of
the net as reference), and execution by shot type. The stratified tables by discipline, tier, hammer, game state and shot
type close it as model checks.

## What the samples say

**The men's final, Canada 9, Great Britain 6.** The players table has Jacobs at +4.05 points of execution over his
twenty stones and Mouat at +3.73; the two fourths account for most of either team's value, which is what the leverage
of the last two stones of every end does. The book graded Mouat at 80 percent and McMillan, Britain's lead, at 98.75; the
model has McMillan at +0.37 over the game, a lead's stones moving the expectation by hundredths. The game turned in the
ninth end: Canada, one down with hammer, scored three, and the end table shows Britain's chance falling from 65 to 17
percent. The shot rows for that end show four British stones below average (Lammie's raise graded zero and three doubles
graded 50) and then Jacobs' clearing for three, +0.59 points of execution, which took Canada from 67 to 83 percent. That
stone is the first row of `testset.md`. The tenth end is walked through stone by stone in Section 8 of the design
document: Mouat's double lifted Britain from 16 to 31 percent, Jacobs' double (+1.01) took Canada from 69 to 94, and
Mouat's last stone missed for the steal.

**The women's final, Sweden 6, Switzerland 5.** The report shows why the two currencies sit side by side. Hasselborg's
winning stone, a take-out graded 100 for one point in the tenth end, has an execution value of −0.38 points and took
Sweden from 87 to 100 percent. In points the field usually gets more than one from that position, so taking one is below
average; in win probability one point ends the game. The points currency treats every end alike, which is what makes
execution comparable across a week; the win-probability columns know which end it is. The other lines worth reading are
the Swiss blanks in ends two and three (Paetz's clearing stones score in both columns, the call worth more than the
field's usual call from those positions), Paetz's fifth-end double that held Sweden to one (+0.93, Switzerland from 16 to
30 percent), and her missed double in the eighth (graded 25, −0.58, the largest swing of the game, Switzerland from 29
to 13 percent), the steal that decided the match.

**Milano Cortina 2026, the fields.** Among the men's fourths Schwarz-van Berkel, Mouat and Jacobs lead on reliability
(65.5, 65 and 64 percent of shots at or above the field) and separate on the miss: Jacobs' and Schwarz-van Berkel's average
misses are −0.22 and −0.24 with eleven and nine big misses, Mouat's −0.30 with thirteen. Among the women Hasselborg, Homan,
Paetz and Morrison sit within three points on reliability; Homan's seventeen big misses are the most among them, the
pattern the design document describes for her cycle. The men's team table shows what the team columns are for:
Switzerland went 10-1 with the largest start from first-end hammer (+9.8 points of win probability per game) and the
highest control (77): ahead early and rarely in a close game. Canada, 9-2, held only 58 on average and earned its record
with its stones (own +15.4, allowed +11.4).

**The 2026 Worlds.** Einarson leads the women's fourths on reliability (66 percent) and net; Han has the smallest average
miss in that field, −0.23, on a reliability of 58 percent, the consistent shape: not often above the field, rarely far
below it. On the men's side Edin, Whyte and Dunstone are within a point and a half of each other on reliability (65.5, 64
and 64 percent), and Dunstone's misses are the smallest, −0.21, with his five worst stones costing 4.2 points, the
shortest tail in the group. The bottom of each table shows the other shape: Stych among the men, Williams and Strouse
among the women have average misses a tenth to a quarter of a point deeper than the leaders and two to three times
their big misses.

**Beijing 2022.** Included because Section 11.2 of the design document builds its argument on it: Shuster's reliability
in the lower half of the field (53 percent) with misses deep enough to make his net negative, Retornaz's reliability
level with Krause's at the bottom of the field with the largest average make and a positive net, and the final between the field's two most
reliable fourths, Mouat and Edin (62.7 and 60.7 percent). The median and floor columns the section
quotes live only in the combined CSV.

**What the October refit changed.** Two things (October 1, 2026). The 7,990 stones of ends scored X are now in every
table: they include the game-ending doubles of the last end, the largest worth twenty to twenty-eight points of win
probability. And the team tables replaced the summed win probability of a team's own stones, which grew with long, close
games, with the record and where it came from. Per stone the values already in the tables moved very little
(correlation 0.996 with the previous model), so the figures quoted above shifted by hundredths; where an order changed
it was between players already level (Mouat and Edin at Beijing, the leaders at Milano Cortina).

**What the rock-trait refit changed.** Every value in these files was recomputed when the model changed from hand-built
position features to rocks read by their traits (September 2026). The fourths' execution barely moved (per-stone
correlation 0.96 with the old values; their event rankings by net 0.98); the front end moved most (leads 0.70), which
is where the old model knew least. Because the leaderboards then sorted on reliability, where players sit within a point or two
of each other, the order within a position group changed often, mostly among leads and seconds; among the fourths the top
of a table changed only between players who were already level. The design document's Section 19 has the details.

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
  (Section 11.3). Read the call column as "the call the field usually makes here" and not as "the best call".
- **Points and win probability disagree at the end of a game**, by construction. The hammer value H is an infinite-horizon
  quantity and the last end has no next end, so a blank in the ninth is worth the same 0.58 in points as a blank in the
  first and twenty-four points more in win probability. The game reports' end tables are in win probability for this
  reason; in the leaderboards use the `_wp` columns for anything that depends on the ends remaining.
- **The official grade and the model measure different things.** The grade counts every stone once against the caller's
  intent; the model weighs it by what it did to the end. A missed hit that leaves a better position is a miss on the sheet
  and a gain here; a perfectly executed low-leverage stone is a 100 on the sheet and a few hundredths here.
- **Coverage.** Shot-by-shot pages exist for all games in the major books and for a handful of games in some others; the
  index that `pointsgained events` writes flags the books with fewer than ten games. Leaderboards need thirty stones.
- **A label variant.** The corpus carries `Wick/Softpeeling` (120 stones) alongside `Wick / Soft Peeling`; the shot type is
  a model input, so merging them is a change for the next refit rather than a report fix.

## Regenerating

The commands in the table above write to the directory given by `--reports`; copy the files here to refresh the samples.
`events`, `game` and `testset` read the Points Gained table and take seconds; `model` refits the models and takes about
ninety minutes on the full corpus with the adopted local target. The Results Books themselves are not part of the repository (see the README).
