# Curling Analytics: A Shot-by-Shot Ingestion Pipeline and Corpus, Points Gained, and Sample Studies — Design Document

**What this is.** We're sharing a method for ingesting data about curling games that are consistent with the format in what are called the "Results Books", which are made available by the World Curling Federation (and via partners like CURLIT) for every major WCF-sponsored curling event, and the Olympic Games, going back to 2013. We've used this pipeline to create a corpus that reads every stone of every end of 4,150 international games into tables: where every stone was before and after every shot, who threw it, what was called, how it was graded, and how the end and the game came out, which in turn forms the basis for doing shot-by-shot analysis.

**How this document is organised.** Part I describes the ingestion pipeline and the corpus: where it comes from, how it is extracted and validated. Part II describes how a position is read: rock by rock, every rock described by objective yes/no traits, re-read after every stone, with what rocks like that have been worth taken from the corpus. We also codify a few relations between rocks, where the data suggests that individual rock traits don't capture the full potential or complexity of the position. These usually occur late in ends, or involve multiple rock combinations (e.g., a draw against multiple stones, doubles and runbacks). Part III introduces **Points Gained**, a system for valuing individual curling shots: an expectation model for positions, f and g, which says what a position and a call have been worth under the field's play, and a value for every stone as the change it made to that expectation; see Section 8 for a walkthrough of one end of the 2026 Olympic final stone by stone. The expectation model can be used a variety of ways, and we use it to rate execution, but also to value positions and shots in strategic analysis. Part IV describes a collection of initial studies that the corpus has made possible, most of which build upon the shot data and Points Gained. Part V describes how to contribute, the open problems and the project's status. Appendix A records the approaches that were built and retired along the way.

**Status (October 2026).** The corpus is built and validated: 92 results books with shot-by-shot pages, 609,014 shots. The expectation models read positions rock by rock (Part II) with the game situation, the event's level of play and, for the call, the called shot and its target; early positions are trained on the value two stones later (Section 7.5).

---

## Part I. The ingestion pipeline and the corpus

## 1. What the project provides

Four subprojects, each usable on its own and each open to contributions (Section 13):

- **An ingestion pipeline** (Section 2). It reads the results-book PDFs directly: the per-shot diagrams are decoded from the embedded images rather than rendered, stones are detected and placed in inches on a fixed sheet frame, the panel text gives the thrower, call, turn and grade, and validation gates check every book before it is used. The output is six tables per book with a documented schema, and that schema is the contract for any other source: a new source of games needs an adapter into the same tables, and everything downstream runs unchanged (Section 2.6).
- **A corpus** (Section 3). The pipeline run over every results book with shot-by-shot pages: 92 books, 4,150 games, 609,014 shots, with stratum labels (event, tier, discipline, era, player, position) on every row.
- **A way of reading positions** (Part II). Rock by rock: the exact count, every rock's traits (in the four-foot, behind cover, frozen, on the wing, ...), each team's rocks graded by what rocks like them have been worth, and a small set of relations that emerge from how stones are configured (a draw against multiple stones, a possible double and a possible runback). We've introduced a configuration vocabulary in the terms a skip might use (a split house, the deuce is loose, the steal is on) in order to facilitate studies, but these terms aren't part of the position expectation or any subsequent model.
- **Points Gained** (Part III). An expectation model for positions and calls, and a value for every stone in two currencies (hammer-adjusted points and win probability), split into the call and the execution. Every value is a difference of model outputs, so any grouping of stones (a player, a phase of the end, a shot family, a configuration) can be valued the same way.

The studies of Part IV are examples of what the four subprojects support, each produced by a command in the package, and templates for further studies.

## 2. The ingestion pipeline

### 2.1 Source

The pipeline reads World Curling results books, as published in the CURLIT results-book directory at `curlit.com/results`: one PDF per event, with a shot-by-shot page for every end of every game in the events that have them. The directory lists 310 results books; 208 are team-of-four men's or women's books from 2013 onward and in scope. All 208 were downloaded (2.3 GB). Only 92 contain shot-by-shot pages: 25 tier 1, 42 tier 2, 23 tier 3, 2 tier 4. The other 116 (Europeans B and C, Seniors, Junior-B, Pan Continental B, the qualifiers and the Universiade) are line scores and standings only; they still feed the win-probability table. Any PDF in the same format, from any event, goes through the pipeline unchanged; other sources enter through an adapter (Section 2.6).

Jordan Myslik's earlier extraction (`jwmyslik/curling-analytics`) is the precedent for this work, and showed that the shot diagrams could be read at scale. It can no longer be rerun because its source host no longer responds. It converted the PDF pages to XML and images; this pipeline reads the embedded diagram images directly. Nothing here depends on it.

### 2.2 What the diagrams are and what they carry

The per-shot diagrams are not drawn on the page; they are embedded raster images (300×600 pixels, in nearly every book 4-bit indexed colour with an exact 16-entry palette). The extractor never renders a page: it reads each image and its palette from the PDF, classifies pixels by colour, finds stones with a stone-sized disk template, and reads the panel's text by its position. The sheet's geometry is the same in every diagram (0.61 in per pixel); coordinates are in inches with the pin at (0, 0) and y positive towards the hog line.

Besides the stones at rest after the shot, a diagram carries a mark on the delivered stone (absent when it left play, about 11% of shots), hollow rings where moved stones were before the shot, and counters of the stones each team has still to throw and has had removed. The counters give the main extraction check: thrown plus on the sheet plus removed must equal eight per colour, which holds in 99.9% of panels.

At 0.61 in per pixel, stones within about an inch of each other, or of the edge of the twelve-foot, cannot be told apart; on the ice they were measured. The count read from the final diagram agrees with the recorded end score in 96 to 98% of ends in recent books and about 89% in 2014–2017 books, so the recorded score is the label and the reconstruction is a check (Section 2.3).

The books' templates differ in colours, stone glyphs, marker styles, text layout and the orientation of alternate ends. Each difference, and how the extractor handles it, is recorded in `docs/extraction_notes.md` for anyone building another reader of the books.

### 2.3 Pipeline

**Inventory.** `pointsgained inventory --check` fetches the directory page, which is plain HTML with direct PDF links, classifies each book by event family, tier and discipline, and HEAD-checks every in-scope link. Mixed doubles, wheelchair, mixed-team and youth (Youth Olympic Games, European Youth) books are out of scope; the World Junior Championships are in.

**Download.** `pointsgained download` fetches in-scope books sequentially with a delay, resuming from disk. These download links are provided as-is, and depend on an entity (CURLIT) outside of the project's control. If you feel that you might not have permission to download resources from CURLIT, please contact them and confirm before downloading.

**Survey and extraction.** `pointsgained batch` runs, per book and in parallel: a survey (does it have shot-by-shot pages; which template, grade style and image format), extraction, and validation, and writes the gate results back to the inventory. Books without shot-by-shot pages are marked excluded.

**Validation gates.** A book is `validated` when the stone census holds in at least 95% of panels, score reconstruction agrees with the recorded score in at least 85% of ends, hammer alternation is violated in at most 1% of ends, and at least one game was found. The thresholds are set to catch extraction failures, which show up as agreement rates near 50 to 60%, while admitting the older books' higher rate of inch-level ties. Every book with shot-by-shot pages passed.

**Audit.** `pointsgained audit` draws random panels with detected stones, delivered marker and prior rings overlaid onto a contact sheet.

**Storage.** Raw PDFs by year; Parquet tables per book; the inventory CSV as manifest; nothing enters training that is not validated and in scope.

### 2.4 Tables

Extraction writes six Parquet tables per book. Every row records the book, page and panel it was extracted from, so it can be traced back to the original diagram.

| Table | Content |
|---|---|
| `games` | Book, discipline, date, start time, session, sheet, the two team codes and names, their colours, report code |
| `ends` | Per end: running score before and after for both teams, this end's score, conceded flag, hammer team (inferred), Total Score and Time left box, colour source |
| `shots` | Per shot (1–16): team, colour, player, shot type, turn, grade (raw and 0–100), note line, stone counters (remaining and removed per colour), stones detected per colour, delivered-stone colour, orientation flag |
| `stones` | Per stone per shot: colour, pixel and inch coordinates, delivered flag, and prior-position rings as separate rows |
| `line_scores` | From the Game Results pages: per team, last-stone-first-end flag, score per end, extra ends, total |
| `players` | From the Game Results pages: position, function (skip / vice), game and cumulative percentage |

The `turn` field is kept: it is free, and it matters for in-turn versus out-turn execution modelling. Mirroring (Section 2.5) should flip it and does not yet (Section 7.2).

### 2.5 Preprocessing

1. Convert coordinates to inches and rotate alternate ends into the thrower's frame.
2. For each shot, assemble the pre-position (after the previous shot; empty for shot 1) and the post-position.
3. Determine hammer from shot order (the team throwing shot 1 does not have hammer) and check alternation against the recorded scores.
4. Attach the recorded end score as the label. An end scored X (the trailing team ran out of rocks: the end is not completed and the score reverts to the last completed end; 579 ends, 14% of games, 7,990 stones, always the last end of the game) carries none: its rows are kept as censored rows, valued for Points Gained but never used to train or evaluate a model. Its last stone has no realised score: in points its post value is the model's value of the position it left, and in win probability it is the game's result, so the stone that ended the game carries the swing. An end in which the hammer team does not throw its last stone and the score stands is an ordinary end with 15 shots.
5. Assign rule era: four-rock free guard zone before the 2018–19 season, five-rock after.
6. Relabel stones `hammer` / `non_hammer` (Section 6.4) and record whether the thrower holds hammer.
7. Mirror every position left-right (labels unchanged). Early on, we explored mirroring to support what we hoped was a purely geometric model of expectation. As it turns out, we did not have enough data for this effort to succeed, in spite of mirroring, but we have kept the possibility in the data. Which models train on the mirrored rows is set out in Section 7.2.
8. Attach stratum keys.

### 2.6 Adding a source

Everything after extraction reads six Parquet tables per book, so a new source of games (another federation's results, a national championship, a tour event, a club's own records) enters the system through an adapter that writes them. The columns the downstream code uses:

| Table | Required | Useful |
|---|---|---|
| `games` | `book`, `game_key`, `discipline` (M or W), `date`, `team_a`, `team_b`, `color_a`, `color_b` | `session`, `sheet`, team names |
| `ends` | `game_key`, `end`, `team_a`, `score_before_a`, `score_before_b`, `score_end_a`, `score_end_b`, `hammer` | `conceded` |
| `shots` | `game_key`, `end`, `shot` (1–16), `team` | `player`, `shot_type` (the twelve call types of Section 7.3), `turn`, `grade_pct`, `has_diagram` |
| `stones` | `game_key`, `end`, `shot`, `kind` ("stone"), `color`, `x_in`, `y_in` after the shot, in inches with the pin at (0, 0) and y towards the hog line | `delivered`, and prior positions of moved stones (`kind` "prior") for the struck stone |
| `line_scores` | per team per game: `team`, `lsfe` (last stone in the first end), `n_ends`, `ends` and `extra` (points per end), `total` | usable without any shot data: line scores alone feed the win-probability table |
| `players` | | positions and official percentages |

The minimum for Points Gained is the stones after every shot, the shot order, the end scores and the hammer. Without the call, g sees every shot as the same type, so each shot's total value holds but its split into call and execution means little; without the thrower, values aggregate to teams but not players. Of the validation gates (Section 2.3), score reconstruction against the recorded score and hammer alternation run on any source; the stone census needs the counters a results-book diagram carries. Once a source's books pass them, `pointsgained features` and `pointsgained model` take it in with the rest of the corpus, and the event field for execution comparisons is that book's own.

## 3. The corpus

### 3.1 Coverage

The pipeline run over every in-scope results book gives the corpus the rest of this document works from (`data/parquet/`, one directory of tables per book, not committed; the pipeline rebuilds it from the PDFs):

| | Count |
|---|---|
| Books with shot-by-shot pages | 92 |
| Games | 4,150 |
| Ends | 38,163 |
| Shots | 609,014 |
| Stone positions | about 3 million |
| Line-score team rows (all books) | 3,078 |

So the shot-level corpus is roughly 600,000 shots rather than the 1.5 to 2 million estimated before the archive was surveyed, concentrated in the Olympics, the World Championships, the Europeans A-Division, the Pan Continental A-Division and the World Juniors. Some junior books carry shot-by-shot pages only for the playoffs.

### 3.2 Strata labels

Every row carries stratum keys so that models and reports can be re-cut without re-running the pipeline: discipline (from the page header), event family and tier (from a regex table over event names, the single place tiers are defined), season and rule era (from the date), team code, player name, throwing position (from shot order), session and sheet.

Player names need care. The books use surname plus initial, in varying case, and a player's team code changes between events (Scotland at the Worlds, Great Britain at the Olympics); reports key on the upper-cased, whitespace-normalised name within a discipline. Genuine name changes ("SCHWARZ B" in 2022, "SCHWARZ-VAN BERKEL" from 2025) are handled by an alias table (`data/player_aliases.csv`: 31 confirmed pairs, 23 to check, and 7 rejected because both names appear in one book).

---

## Part II. Reading a position rock by rock

## 4. The idea

### 4.1 Principles

A skip standing in the house does not see a feature vector. They see rocks: this one is buried in the four-foot, that one is sitting open on the wing, that guard is doing nothing, those two are frozen and will not come apart. The expectation of a position is, to a first approximation, the sum of what its rocks are good for, adjusted for a few relationships that seem genuinely positional (i.e., which empirically give different results than we'd expect if we only reason about the rocks individually).

Ideally, we would not try to guess what's important about what a skip takes in, but instead try to learn it from all the situations we have encountered in the data. However, our studies have shown that the amount of data we have is insufficient to predict the distribution of outcomes we see. Thus, we have introduced a small number of inputs that stand in for how a skip might treat a position:

- **Every rock is described by objective yes/no traits** (Section 4.3): in or touching the 4-, 8- or 12-foot, in front of or behind the tee, on the wing, in the guard zone, controlling the path to the 4-foot, guarding a rock in the house, shot, second or third shot, frozen onto its own colour or the other, open, partly open or behind cover, and backed or partly backed by a rock behind it that would jam a take-out. The traits overlap by design; a rock in the four-foot is also in the eight and the twelve. Generally, one of the claims of the system is that the value of a position can be inferred from the values of the rocks that are in play in the position, without necessarily knowing *why* rocks with certain traits lead to higher-scoring or lower-scoring ends.
- **The house is re-read after every stone.** A rock's traits are whatever they are in the new position: a rock that was open is behind cover once a guard lands in front of it; a rock that was shot is second once another comes to rest inside it; a removed rock is simply gone. Nothing is tracked. What happened to a particular rock is a question for studies (the corpus keeps stone identities, Appendix A.3), but we don't use it for the expectation.
- **The corpus says what rocks like that have been worth** (Section 4.4): for each trait, held by the hammer or the non-hammer team at a given stage of the end, the distribution of the end's results. Added up, those become grades for every rock (Section 4.5), and the change in each team's grade across a stone is that stone's contribution to the rocks in play, the **rock ledger**.
- **We do a small amount of reasoning about the relative position of rocks** (Section 4.6). If all we did was count traits per rock and add everything up, we find that certain information about the position is lost. For example, it is critical in evaluating an end to know which rock is shot, which rock is second, and so on, so we pass that information to the model.
- **A few relations are computed directly** (Section 4.7): as with knowing which rocks are outcounting others, we have found in the data a few positions that lead to more or less expectation than the traits themselves would suggest. We search for those configurations and pass them to the model.

The expectation model (Part III) reads exactly these: rock traits per team, grades, the relative positions of the rocks, and any special relations that exist in the position, plus the count, the game situation, the event's level and, for the call, the called shot and its target.

### 4.2 Count function

Sort all stones by distance from the pin; a stone is in the house if that distance is at most 72 inches plus the stone radius (5.7 in). The team owning the closest in-house stone scores the number of its in-house stones closer than the nearest in-house opposing stone; an empty house is a blank.

**Near-tie positions.** When the last counting stone and the nearest opposing stone are within about two inches of the same distance from the pin, they are tied on the diagram and the data cannot say which one counts; these are the ends where reconstruction disagrees with the recorded score. In some cases, they correspond to a real game state rather than noise: the skip cannot tell which rock is second either, and the call made there (peel, freeze, play for the measure, draw for the sure one) is a strategic response to that uncertainty. In the model, we record how far the shot rock and the last counting stone are ahead of the nearest opposing stone, in inches, and we introduce a near-tie flag (under 2 in).

### 4.3 Rock traits

Canonical frame (Section 6.4): inches, pin at (0, 0), y towards the hog line, the hammer team's rocks labelled as such. Every test uses |x|, so traits do not change when the sheet is mirrored. `core/traits.py`.

| Trait | Test | Note |
|---|---|---|
| `four_foot`, `eight_foot`, `twelve_foot` | In or touching the ring (distance ≤ radius + 5.7 in) | Nested; `twelve_foot` is "in the house" |
| `above_tee`, `behind_tee` | In the house, centre in front of / behind the tee line | House rocks only: a centre guard is not "above the tee" |
| `wing` | In the house, outside the 4-foot lane (\|x\| > 24 in) | House rocks only |
| `front` | In front of the house: the guard zone | |
| `controls_4ft` | In the 4-foot lane and in front of the 4-foot (y > 29.7 in) | A centre guard, or a high centre rock at the top of the eight or twelve |
| `guarding` | In front of a rock in the house (either team's), within a stone's width of its line | Colour-blind: a guard's cover serves whoever can use it |
| `shot_rock`, `second_shot`, `third_shot` | Distance rank among rocks in the house, either team | The owner says whose |
| `frozen_own`, `frozen_opp` | Touching a rock behind it (centre distance ≤ a stone's diameter + 2 in) of its own / the other colour | The **front** rock of a freeze is the frozen one: a well-frozen rock is hard to remove. The 2 in is the diagram's resolution |
| `open`, `partly_open`, `behind_cover` | The nearest rock in front of it (straight line): more than a stone's width off its line, within a stone's width, within half a stone's width | Exactly one per rock. A draw tossed into the rings is "four-foot, open"; a draw around a guard is "four-foot, behind cover" |
| `partly_backed`, `backed` | Some, or half or more, of its exit cone (30° either side of straight back) runs into a rock behind it within eight feet | Colour-blind. A backed rock is hard to remove cleanly: a take-out on it may jam, and a shooter can tap it or run it back into the rock behind |


A single centre guard at the start of an end is `front`, `controls_4ft` and `open`, and nothing else. A rock's whole vector is its **type**; across the corpus there are about 1,800 types with 1 to 5 stones thrown, rising to about 3,500 late in the end, and 81–86% of rocks fall in types seen 500 times or more. The vocabulary was written by Mike Calcagno, the tests and thresholds are the obvious ones, and all of them are open to change: the point of the study that follows is that the corpus says which traits matter.

Three traits pair up often enough to read together (Jaccard overlap above 0.5): the nested rings, the twelve-foot with above the tee, and the guard zone with open.

### 4.4 What traits have been worth

`pointsgained traits` (`reports/traits.md`, with a Tier 1 version) takes every position after stones 1 to 15, 558,694 of them from 37,623 ends, reads each rock's traits, and sets beside them the end's result for the hammer team: the mean points, and the share of steals, blanks, singles and two or more. Each end appears once per stone number, so the positions after a given stone are independent; results are read against positions after the same stone in the same game situation (discipline, score difference to ±2, two or fewer ends left) so that a trait that turns up when a team is ahead is not credited with the lead, and intervals are clustered by end. Across the corpus the hammer team scores 0.79 points per end: a steal 21%, a blank 13%, a single 34%, two or more 32%.

One trait at a time, the positions where a team has at least one rock with it against the rest. Δ points is in hammer-adjusted points per end; Δ two or more and Δ steal are in percentage points of the share of ends:

| Late in the end (after stones 11–15) | Share of positions | Hammer points | Δ points (same situation) | Δ two or more | Δ steal |
|---|---|---|---|---|---|
| Hammer team has the shot rock | 40% | 1.33 | +0.52 | +17.0 | −9.3 |
| Hammer team has second shot | 35% | 1.26 | +0.46 | +17.6 | −1.2 |
| Hammer team has a rock on the wing in the house | 46% | 1.08 | +0.29 | +11.3 | −2.0 |
| Hammer team has a rock frozen onto its own | 4% | 1.24 | +0.43 | +13.0 | +1.5 |
| Non-hammer team has the shot rock | 57% | 0.43 | −0.34 | −10.7 | +7.1 |
| Non-hammer team has a rock in the four-foot | 44% | 0.52 | −0.27 | −5.7 | +9.7 |
| Non-hammer team has a rock frozen onto its own | 6% | 0.40 | −0.37 | −5.5 | +13.5 |
| Non-hammer team has a rock behind cover | 47% | 0.66 | −0.12 | −1.3 | +7.8 |

The table reads as skips would expect, with some insights that aren't typically discussed: for example, in the data, we find that a non-hammer rock frozen onto its own is the strongest steal trait in the vocabulary, and a hammer rock on the wing late in the end is worth nearly as much as a counter, due to the ways a wing rock might become an additional counter. Some rows are not completely independent of the game situations in which they are typically found: the hammer team's rock controlling the four-foot late in the end goes with more steals (+6.3), because a hammer centre guard that late is usually a catch-up call or a missed come-around.

**One rock in play.** Positions with a single rock, by its team and type, are the cleanest reading of what a rock is worth. After the first stone of an end the non-hammer team's rock is almost always a centre guard or a draw into the four-foot:

| After stone 1, non-hammer rock | Ends | Hammer points | Two or more | Steal |
|---|---|---|---|---|
| Centre guard (front, controls the 4-foot, open) | 18,267 | 0.88 | 34% | 21% |
| Four-foot, in front of the tee | 8,905 | 0.62 | 28% | 22% |
| Four-foot, behind the tee | 2,749 | 0.68 | 29% | 20% |
| Eight-foot, behind the tee | 758 | 0.85 | 33% | 17% |
| Twelve-foot, behind the tee | 340 | 0.86 | 31% | 18% |

Here, among other things, we see that the depth of the draw bears on the expectation of the end: the deeper behind the tee it comes to rest, the better for the hammer team.

### 4.5 Grades and the rock ledger

One trait at a time cannot say what a rock is worth, because traits come together. The **grade** combines them: per stage of the end (stones 1–5, 6–10, 11–15), a linear fit of the end's result on each team's trait counts, with the stone number and the game situation as stratum effects. Every rock is exactly one of open, partly open or behind cover, and nearly every rock is either in the house or in front of it, so those traits fold into a per-rock base: the reference rock is an open guard, and every other weight is what a trait adds to a rock that has it. A rock's grade is its team's base plus the weights of its traits, in hammer-adjusted points from the hammer team's side; fits for two or more and for a steal give the same in percentage points. `model/trait_study.py`.

A few rocks from the grade card, late in the end (points for the hammer team):

| Rock (after stones 11–15) | Hammer's rock | Non-hammer's rock |
|---|---|---|
| Four-foot, in front of the tee, shot rock, behind cover | +0.93 | −0.63 |
| Four-foot, in front of the tee, shot rock, open | +0.85 | −0.50 |
| Twelve-foot, behind the tee, on the wing, second shot, open | +0.87 | — |
| Open guard (the reference) | +0.01 | +0.06 |
| Centre guard, guarding a rock in the house | −0.06 | −0.14 |

Early in the end the same rocks are graded very differently: a hammer rock of any kind is worth +0.29 in the first five stones and +0.01 late, because early it is a rock the hammer team has kept in play in the free guard zone, whereas late it is a rock that the hammer team is giving up the possibility of scoring with.

### 4.6 Shot rock, second shot, etc.

Counts of traits per team say how many of a team's rocks are open; they cannot say whether (for example) *the shot rock* is open (or second shot is open). The model therefore also describes five rocks individually, each with its owner and its traits as they are in this position: the shot rock, second shot and third shot (either team's), and each team's guard nearest the pin. The code calls these five positions **slots** (`model/slot_features.py`). Picking out these five rocks by hand feels a bit unnatural, but it does improve the fit of the model to the data. Each slot carries its exposure (open, partly open, behind cover) and its jam (clear, partly backed, backed) as ordinals, and the gap to the nearest rock in its exit cone, so for these rocks the model sees how far behind the jam is, not only whether there is one. Late in an end these are most of the rocks in play, and the value of the last few stones depends almost entirely on them: in chess terms, the endgame is calculation over a few pieces. Adding them cut the log-loss at the last rock more than anything else tried (Section 7.6).

### 4.7 Geometric positions in the end game

The last stones of an end are about a few geometric relations between rocks, which a sum of rocks cannot see. Three are computed for the team about to throw.

**The draw against multiple stones** (`core/draw.py`). "Draw against n": the other team lies n, and a draw that finishes closer to the pin than its best rock turns that into a count for the thrower. The features are the distance of the rock to beat, how many the other team lies, what a made draw would leave the thrower lying, whether the path is open, and whether there is backing. The path is modelled on how the draw is actually played:

- The final draw comes on an in-turn or an out-turn, curling in from one side or the other. Any rock along that curved path blocks it: rocks on the wing on the side it curls in from, and rocks tighter to the four-foot lane the nearer it gets to the house. A straight-line centre guard does not block it. Often one side is closed and the other open.
- The path is the curve of a stone that decelerates uniformly while curling with a constant sideways acceleration: with u the distance still to travel and U the length of the curl, the stone is D(2r − r²) to the side of where it finishes, r = √(u/U), with D about four feet. The approach comes in at an angle and the path is widest far up the sheet. A rock blocks it when its centre is within a stone's diameter of the path where the path passes it.
- The finishing points are the spots in the four-foot inside the rock to beat that no rock occupies, plus a freeze onto the front of every rock in the house. A side is open when at least half of them can be reached from it.
- The draw is close to a sure thing, high 90s at this level, with **backing**: the rock to beat is behind the tee, so a draw onto it outcounts it, or another rock sits just behind a finishing point and will stop a heavy draw.

On the hammer team's last rock, with the other team lying two, the hammer team scored 51% of the time with both sides closed, 68% with one open and 75% with both; lying one, backing added 10 to 18 points. Where both sides are open and the rock to beat is out in the eight or twelve, the hammer team usually does not draw at all: it hits and rolls out for the blank (61% of those ends), because doubling out two or more to blank is much harder than removing one. With no side open, the usual shot is the hit and stick.

**Doubles and runbacks** (`core/combos.py`). Doubles and runbacks are truly positional: geometric configurations that unlock a bigger result than playing against a single rock. A double that is not there does not get called, and the skip plays something else; a runback gets called for its upside and is weighed against its downside. The aftermath of either, made or missed, is valued by re-reading the house, so the features describe only availability and stakes:

- **Double**: two of the other team's rocks, the first hittable (nothing within half a stone of its line in front), the second behind it, the pair not flat (at least 15° from level: on a flatter pair the field almost never makes the double) and within eight feet; whether both are in the house, the pair's separation and stagger, the count swing if both go, and whether **the double jams**: the share of the back rock's exit cone blocked by a rock behind it (the jam of Section 4.3).
- **Runback**: a hittable rock of either colour within 35° and fifteen feet in front of the other team's best rock; straight (under 10°) or angled, its distance, whether the front rock is the thrower's own, and the swing if the target goes.

### 4.8 The configuration vocabulary

Early versions of the model did not rely on rock traits, but rather on positions that are commonly identified in a curling end, which could be identified by reasoning about the house as a whole: deterministic tests on the whole position in the terms a skip uses, several of which can hold at once (`core/configurations.py`). They are no longer a model input, but studies still use them to select positions, and the report of where the model misprices positions breaks its results down by them (Section 7.7), and some of their thresholds (the flat split, the runback angles) are now the thresholds of the relations above. This allows a user of the data to talk about things like a "split house" and there is code that will identify those situations for further study. Out of curiosity, you might ask whether these positions might predict end outcomes better than our rock-by-rock traits system, and the answer is no. It does slightly worse, and the rock-by-rock system is much simpler to understand. Skips might argue over whether a position is really conducive to a 2 being in play, but they will rarely argue (or can't argue) over whether a rock is in front of or behind the tee line. We favor the latter kinds of features.

| Label | Test ("own" is the hammer team) |
|---|---|
| `open_house`, `guards_only` | No guards; no stone in the house |
| `own_` / `opp_centre_guard`, `own_` / `opp_corner_guard` | A guard within 24 in of the centre line, or outside it |
| `own_shot`, `opp_shot`, `own_` / `opp_two_plus` | Who lies shot; lying two or more |
| `split_house`, `split_flat`, `split_staggered` | Hammer has two or more in the house, every pair at least 3 ft apart, the opponent none; flat when 4 ft or more apart and within 15° of level (the double is nearly off), staggered otherwise |
| `own_shot_covered`, `steal_on`, `opp_exposed` | Hammer's shot rock covered; non-hammer lies shot, covered; a non-hammer house rock with nothing in front of it |
| `deuce_loose` | From stone 9: a flat split, or a covered hammer rock that will count second with the centre open |
| `steal_setup` | Non-hammer has two or more centre guards |
| `shot_runback_straight` / `_angled`, `lonely_steal`, `lonely_steal_exposed` | A runback on the shot rock within 10° or 10–35°; non-hammer lies one and the hammer team counts two or more without it; with a runback on it |
| `busy_house`, `near_tie` | Four or more in the house; a boundary gap under two inches |

Three situations shaped the vocabulary. A **split house**: the hammer team's third hits and sticks to restore it, and whether it is restored flat or staggered decides whether the opponent has a double. **The steal**: a team that needs a steal wants two guards up before it puts a stone in the house, because an exposed stone is a free hit. **The runback**: a skip can use either team's stone against the other; a guard placed too close to a lonely steal stone, or a stone tucked not far enough behind an opponent's, invites the runback. The question behind all of them is what the position leaves the opponent, and the relations of Section 4.7 now answer it directly for the thrower.

---

## Part III. Points Gained: an expectation model for positions

Part III is the framework: a model of what a position and a call have been worth under the field's play, read rock by rock (Part II), and a value for every stone as the change it made. The studies in Part IV use it to put a number on a position, a shot or a phase of the end, and the player and team reports are built from it. Its models, targets and gates are all open to improvement; the open problems in Section 14 are the current list.
## 5. Goal

Assign every shot a value, **Points Gained (PG)**, that measures how much it changed the expected scoring of the end, from the throwing team's point of view. The name is chosen by analogy with strokes gained in golf: it is measured against the field, it is additive, and it decomposes. Two properties are required:

1. **Situation-aware.** A made draw against an opponent stone in the four-foot is worth more than the same draw into an empty house, because the expectation before the shot was lower.
2. **Conserved.** The values of all shots in an end sum to the final score minus the expected score at the start of the end. No credit is created or lost.

The output is a per-shot Points Gained, decomposable into **PG: Call** (selection: what the call was worth) and **PG: Throw** (execution: what the throw delivered against the call).

### 5.1 An example

To understand the core idea behind Points Gained, consider the following very simple position. It's the last end and the score is tied. We're down to the skip's last rock, and a single opponent's stone sits at the top of the eight-foot. There are two reasonable calls here: (1) a draw to the house for one and the win, and (2) a hit that keeps the shooter in the house for one and the win. The two calls have different expectations. For the draw, we use the field's average ability to outdraw a rock in the eight-foot (let's call it 75 percent). The expectation for the call is then .75(1) + .25(−1) = .5 points (in reality, the points in an end are adjusted for whether or not the hammer changes hands, but since this is the final end, the illustration holds). Compare that to the hit: suppose the team hits and removes the stone 95 percent of the time, but the shooter stays in the rings only 80 percent of the time. That gives .05(−1) + .76(1) + .19(0), for an expectation of .71 points. So the two calls have different values, and you could argue that, if those really are the numbers for those shots, the hit and stick is a "better" call than the draw. PG: Call compares each call's expectation with the expectation of the position itself, before any call is made: what the field, making its usual mix of calls from here, has averaged.

Now consider execution. If the draw is called and the shooter makes it, they get 1. The expectation for the call is .5, so the shot is .5 better than the field's average. If the hit is called and made, the shot is .29 better than the field's average. Both are above zero, so we consider both shots made, but the player who made the draw gets more credit than the player who made the hit. Now consider a miss. Suppose the hit is called, the shooter flashes the opponent's stone, and the team loses the game. That's −1 against an expectation of .71, a loss of 1.71. If they hit and roll out for the blank, that is 0 against the .71 expectation, a loss of .71 (again, we account for the fact that the hammer doesn't change hands in that case, so the blank is not quite worth 0 and the loss is a little smaller). Those numbers, +.5, +.29, −1.71 and −.71, are PG: Throw.

Every other stone of the end is valued the same way. The model gives an expectation for every position, after stone 1, stone 2 and so on up to the last, and each stone is credited with the change from the position before it to the position after it, split into the call and the throw. Because each stone's starting position is the previous stone's finishing position, the values of all the stones in an end add up to the end's actual (hammer-adjusted) result minus the expectation at the start of the end. This is what "conserved" means above.


### 5.2 Strategy: how game situation enters

Within an end the structure is recursive. Every shot before the last one builds a **position**, every position carries an **outcome distribution** (the chances of blanking, scoring one, scoring two, giving up one, and so on), and the last rock realises one outcome from it. The rock before the last is thrown to make that distribution as bad as possible for the thrower of the last rock; the rock before that, to make it as good as possible two rocks down the line; and so on back to the first stone. The two teams are pulling on the same quantity in opposite directions, which is exact rather than approximate: whatever currency an outcome is valued in, the opponent's value is the negation.

Strategy is the observation that not all outcome distributions are equally useful, and which ones are useful depends on the game. Curlers have a vocabulary for this: *must steal*, *force one*, *two or blank*, *don't give up more than two*, *score or go to the extra end*. In this model those goals are not a separate layer and are not enumerated by hand. They are the *shape* of the value mapping v(outcome | game situation): tied in the last end with hammer, one and two are both worth a win, a blank is worth the chance of winning an extra end with hammer, and a steal is worth nothing, and maximising expected value under that shape simply *is* "score or don't get stolen on." The win-probability table (Section 10.3) generates every one of the named strategies as a consequence.

The two currencies disagree in a way that is itself informative. In hammer-adjusted points, a team protecting a three-point lead reads as calling badly, because points reward aggression whatever the game; in win probability the same calls are neutral. In the first test of the model, on four events, the strongest teams' call values were slightly negative in points and zero in win probability for exactly this reason: they are ahead more often. Rachel Homan's raise with her last rock in the eighth end against Italy at the 2026 Olympics, up two with three ends to play, costs 0.15 points but only 0.8 percentage points of win probability; the game barely depended on that end. Both currencies are kept, and reports say which one they are in.

### 5.3 Terminology

| Term | Meaning |
|---|---|
| **Position** (S) | The stones on the ice plus rocks remaining and rule era, in the canonical hammer-team frame. Pre-shot and post-shot positions bracket every shot. |
| **Rock trait** | A yes/no property of one rock in one position (Section 4.3); a rock's whole trait vector is its type. |
| **Rock grade** | What a rock is worth to the hammer team given its traits and the stage of the end; a team's grade is the sum over its rocks (Section 4.5). |
| **Build / address** | A stone's rise in its own team's rock grade / fall in the other team's: the rock ledger (Section 4.5). |
| **Game situation** | Score difference, ends remaining and hammer at the start of the end. Not part of the position. |
| **Regime** | The strategic goal implied by a game situation (must steal, force one, two or blank, ...), derived from the shape of v. |
| **Call** (C) | The shot as called: the type as recorded. Its outcome distribution D(S \| C) is informally the call's **menu**. |
| **Outcome** | The end result from the hammer team's perspective: blank, +1, +2, +3, −1, −2, −3 (clipped). |
| **Outcome distribution** (D) | Probabilities over outcomes for a position, or for a position and call. Output of f and g. |
| **Value mapping** (v) | The worth of each outcome in the current currency: hammer-adjusted points or win probability. |
| **Value** (V) | Expected worth of an outcome distribution under v. |
| **Points Gained** (PG) | V after the shot minus V before it, signed to the thrower's point of view. |
| **PG: Call** | The selection component: the call's menu against the position. |
| **PG: Throw** | The execution component: what happened against the call's menu. |
| **Field baseline** | D(S) under the field's typical play; the reference for PG: Call in Phase 1. |
| **Best-call baseline** | D(S) under the best available call; Phase 2. |
| **Hammer net** (N) | Expected net score of the hammer team in one end. |
| **Hammer value** (H) | Infinite-horizon value of holding hammer; the spacing used in the points currency. |
| **PGAA** | Points gained above average: the name the reports give PG: Throw, the throw's result against the field's average for that call from that position. |
| **Event-relative execution** | PG: Throw minus the event field's mean for the same shot type and hammer state; the reporting unit for players. |
| **Skill scalar** | A per-thrower level-of-play number estimated from execution grades. Built as a report (Section 7.4, Appendix A.6); not an input to the models, whose level of play is the event's. |

---

## 6. Framework

### 6.1 Definitions

- **S**: the pre-shot **position** (stones on the ice, rocks remaining, rule era) in the canonical frame of Section 6.4.
- **C**: the called shot (the shot type as recorded).
- **S′**: the post-shot position.
- **D(S)**: the **outcome distribution**: a probability distribution over end outcomes given position S, over {−3, −2, −1, blank, +1, +2, +3} from the hammer team's perspective, with larger scores folded into ±3.
- **V(D)**: a scalar value of an outcome distribution: Σ D(o) · v(o). Swapping v is a one-line change and both currencies are computed for every shot.

### 6.2 Points Gained

PG(S, C, S′) = V(D(S′)) − V(D(S))

For the last shot of an end, D(S′) is a point mass on the actual result, so this reduces to actual minus expected.

### 6.3 Decomposition

Insert the called shot as an intermediate baseline:

    PG: Throw (execution) = V(D(S′))    − V(D(S | C))
    PG: Call  (selection) = V(D(S | C)) − V(D(S))

Execution measures how the result compares with what that call usually produces; selection measures what the call was worth relative to the position, under the field baseline: D(S) is the outcome distribution under the observed shot-selection policy of the field, so selection reads as "better or worse than the field would call."

The two components add up exactly to the shot's Points Gained: V(D(S | C)) is added in one and subtracted in the other, so it cancels. That holds whatever g says about the call; a misjudged call moves credit between the two components but does not change their sum. Player reports then measure execution against the field for the same shot type and hammer state (Section 11.2), so the execution and call columns in a report do not add up to Points Gained.

### 6.4 Perspective convention

Every physical position is evaluated **once**, from a canonical perspective: the team holding hammer in the current end. Stones are labelled `hammer` / `non_hammer`, and f is fitted and evaluated only in this frame. A thrower's value is V from the canonical frame, multiplied by +1 if the thrower holds hammer and −1 otherwise.

This is deliberate rather than cosmetic. If f were evaluated from the thrower's perspective, the same physical position would be evaluated twice, once for the team that just threw and once for the team about to throw, and a learned model is not exactly antisymmetric under the swap, so the sum of Points Gained over an end would not telescope. With a single canonical evaluation per position the identity in Section 6.5 holds by construction. Who throws next is determined by the parity of rocks remaining.

### 6.5 Conservation check

With D(final position) defined as the actual score, summing canonical Points Gained over the shots of an end gives

    Σ PG = actual_score − V(D(S₀))

where S₀ is the empty-sheet position at the start of the end. On the full archive the largest residual over 37,585 ends is below 10⁻¹⁵, which is rounding error. It is a unit test, not a diagnostic: if it fails, there is a bug, most likely in rebuilding a post-shot position where a diagram is missing, which must carry every input the training rows carry.

## 7. The expectation model

### 7.1 Insight

Every shot's pre-position is labelled with how the end turned out (positions early in the end are labelled a little differently, Section 7.5). Almost no exact position repeats, so the model has to generalise across similar positions. The outcomes are high-variance per example, but that variance is what the model averages over. This is a supervised problem, not a dynamic-programming problem, and it is deliberately outcomes-biased: it says what positions and calls have been worth given how the field has played, not what they should be worth under optimal play.

### 7.2 What f and g read

- **f(S) → D**: distribution over end outcomes from the position. This is D(S) under the field baseline.
- **g(S, C) → D**: the same with the called shot. This is D(S | C).

Both are gradient-boosted tree classifiers over seven outcome classes (`model/train.py`). Their inputs are named sets, so an experiment can toggle them; the current model uses all of these:

| Set | What it is | Columns |
|---|---|---|
| `core` | Rocks remaining (whose parity says who throws next), the free-guard-zone rule, stones in play, the count, discipline | 6 |
| `situation` | The hammer team's score difference (±6), ends remaining (≤10), an extra-end flag | 3 |
| `traits` | Each team's number of rocks with each trait (Section 4.3) | 38 |
| `grades` | Each team's summed rock grade and their sum (Section 4.5), cross-fitted so that a held-out book is graded by weights fitted without it | 3 |
| `margin`, `shotdist` | How far the shot rock and the last counting stone are ahead of the nearest opposing stone, in inches, and a near-tie flag (Section 4.2); each team's nearest stone to the pin | 5 |
| `slots` | The shot rock, second and third shot and each team's nearest guard, each described individually, with exposure and jam (Section 4.6) | 60 |
| `draw` | The draw against multiple stones, for the thrower (Section 4.7) | 7 |
| `combo` | Doubles and runbacks for the thrower, and whether the double jams (Section 4.7) | 12 |
| `call` (g) | The shot type as recorded and the turn | 2 |
| `level` (g) | The event's strength rating (Section 7.4) | 1 |
| `intent` (g) | The target of the call: the struck stone for hits, the field's modal target for draws (Section 7.3) | 6 |

Situation in f changes what D(S) means, from "what this position is worth under typical play" to "what it is worth given how teams play from here in this situation": for example, up three in the ninth, the field might try to keep an end clean, and f expects that rather than scoring the blank as a failure. The value mapping still carries the situation in the win-probability currency (Section 10.3); the two uses are complementary, and the conservation identity is unaffected because V is fixed within an end.

**Isolation.** When we compute Points Gained, the 92 books are split into five groups. For each group, f and g are trained on the other four, and those models value the positions in the group left out. So every shot is valued by a model that never saw any game from that event.

**Mirrored rows.** f does not train on the mirrored rows of Section 2.5. Everything f reads is the same for a position and its mirror, so they would only repeat each shot; f is fitted once per shot instead, with its regularisation halved to match (150 samples per leaf and an L2 penalty of 5, where g, with two rows per shot, keeps 300 and 10). g does train on them, because the target of the call (the `intent` set) moves to the other side of the sheet in the mirror. The shot's turn is not yet flipped with it, so a mirrored row keeps a turn that no longer matches the mirrored shot; making g side-free is open.

### 7.3 Called shot and intent

The `type` field records the call: Draw, Take-out, Hit and Roll, Guard, Front, Freeze, Raise, Clearing, Double Take-out, Promotion Take-out, Wick / Soft Peeling, Through. The type leaves the target ambiguous, so g also takes the target, with one rule that matters more than the rest: **the call must never be read from the outcome.** On a made draw the delivered stone's rest is the target; on a missed draw it is the miss, and on the last rock it is the score.

What g takes instead:

- **Draws** (Draw, Guard, Front, Freeze, Through): the *modal* target from a target model P(target cell | position, call), fitted on made draws with a marker and applied to every draw whatever its grade. The cells are three lanes by six depth bands. Because it is a function of position and call only, it cannot leak.
- **Hits** (Take-out, Hit and Roll, Double, Clearing, Raise, Promotion, Wick): the **struck stone**, from the prior-position ring furthest up the sheet (the shooter arrives from the hog line), at any grade: which stone was hit is intent, not outcome. Without rings, the modal struck-stone class from a second target model.

The information is in the hits: with the struck stone, the call component's mean size per shot is about half the execution component's rather than a tenth, and largest on take-outs, doubles, raises and promotions.

### 7.4 Level of play

A six-foot double is worth less to an elite team than to a club team because the elite team makes it more often: D(S | C) is higher, so PG: Throw for making it is smaller. Level of play is a property of the **execution distribution** and enters through g, as the **event's strength rating** (`data/event_strength.csv`, men's Worlds = 100), a handful of distinct values that cannot identify a book. Level of play belongs to the field, never to the player being measured: strokes gained does not evaluate a fairway shot against Tiger Woods' putting, it evaluates it against a tour professional's. A per-player skill input was built and withdrawn (Appendix A.6); the shot-difficulty model behind it remains as a report (`pointsgained difficulty`: skill leaderboards, event effects, field strengths beside the ratings).

### 7.5 Training target

Labelling every position with the end's final score is unbiased but noisy early in an end, where ten or more stones remain between the position and the label, and it made early execution values see-saw between consecutive stones: when the model over- or under-valued a position, the stone that created it was credited with the error and the next stone was charged with it. The adopted target (`model/targets.py`, `local:2`) trains rows with nine or more rocks remaining on the value of the position two stones later, as a soft label: the out-of-fold f distribution there, from a first-stage f fitted on final labels within the training books, or the end's result if the end finishes first. The soft targets are rebuilt inside each cross-validation fold from that fold's training books only. This is an approach that we hope to improve on as we gather more training data.

### 7.6 Results

Held-out log-loss against the end's result (lower is better), five folds by book over the whole corpus, as `pointsgained model` runs it. The trivial model knows only rocks remaining, hammer, the count and the game situation.

| | Trivial | f | g |
|---|---|---|---|
| All positions | 1.560 | 1.466 | 1.445 |
| One rock left | 1.229 | 0.923 | 0.814 |
| Twelve rocks left | 1.633 | 1.598 | 1.593 |

The Brier scores are 0.706 for f and 0.698 for g, against 0.742 for the trivial model. The model knows most late in an end and least early: with twelve rocks left it is only a little better than the trivial model (Section 14). Conservation holds to rounding error in every end (Section 6.5), and the mean value of the empty sheet with hammer is 0.586 against H = 0.582 (Section 10.2).

**What each part adds.** Trained on everything through 2024 and scored on the 2025–26 events, adding one input set at a time; the reference is the hand-built model it replaced (Appendix A):

| Model | f | g | Last rock (f) | 12+ rocks left (f) |
|---|---|---|---|---|
| Trivial | 1.5484 | | 1.2295 | |
| Hand-built: base features, configurations, rock potential | 1.4521 | 1.4299 | 0.9046 | 1.6065 |
| Rock traits only | 1.4532 | 1.4307 | 0.9156 | 1.6068 |
| + rock grades | 1.4525 | 1.4306 | 0.9182 | 1.6056 |
| + the count's margins and each team's nearest stone | 1.4524 | 1.4305 | 0.9117 | 1.6060 |
| + the draw against multiple stones | 1.4516 | 1.4302 | 0.9120 | 1.6060 |
| + shot rock, second, third and nearest guards described individually (slots) | 1.4499 | 1.4300 | 0.9028 | 1.6059 |
| + doubles and runbacks | 1.4497 | 1.4299 | 0.9019 | 1.6060 |
| + the jam: backed rocks (**current model**) | **1.4502** | **1.4301** | **0.9036** | **1.6059** |

Rock traits alone came within 0.001 of the hand-built model; the relations and the slots carried the model past it, and the slots did most of the work at the last rock. The jam is level overall and was kept because backing is part of how curlers describe a rock. g is level with the hand-built model overall and slightly behind it at the last rock (Section 14).

### 7.7 Validation

- Held-out log-loss and Brier score against the trivial model, overall and by rocks remaining; calibration by outcome class.
- Conservation to numerical precision (Section 6.5).
- Calibration at the empty sheet: V(f(S₀)) with hammer should equal H.
- Checks on early-end credit (`reports/experiments/frontend_gates.md`): whether consecutive stones' values see-saw (Section 7.5), whether execution values agree with the book's grades, whether a player's values repeat from one half of an event to the other, whether a team's early-end values relate to winning, and how well calibrated the model is at each stage of the end.
- **Where the model misprices** (`pointsgained misprice`, from an experiment's saved held-out predictions): the model's value against the realised result by stage, by stones in play, by configuration label and stage, and, for the hammer team's last stone, by the count and where the shot rock sits. On a time split the held-out years can score differently from the training years (hammer teams scored 0.80 and 0.85 per end in 2025 and 2026 against about 0.75 before), so the report is read net of each model's overall gap. Two last-rock cells that looked under-priced by about 0.2 on the time split (the other team lying two or three with its best rock only in the eight or twelve) disappear by book: they were 2025–26, not a missing relation.
- **Scenario probes** (`reports/samples/front_end.md`): positions where curlers agree on the answer, which the model must get in the right order, such as a split house restored flat against staggered, and the peel when the hammer team must score.

## 8. An end, rock by rock

The tenth end of the 2026 Olympic men's final shows the whole system at work. Great Britain has hammer, is two down and has one end to play: it needs two to force an extra end, and Canada needs to hold it to one or steal. Canada starts the end at 84.7% to win. Every row below is one stone: the call, the book's grade, what the thrown rock is when it comes to rest (its traits, read in the position after the stone), each team's rock grade after the stone (the sum of its rocks' grades, from its own side), the stone's **build** (its own team's grade up) and **address** (the other team's grade down), Canada's chance of winning after the stone, and the stone's execution value (PGAA, points gained above average, the model's PG: Throw in hammer-adjusted points from the thrower's side). The report `reports/samples/games/..._Gold_Medal_Game_CAN-GBR.md` has the same end with the model's values in full.

|   stone | team   | player     | call            |   grade % | thrown rock                                                            |   rocks GBR |   rocks CAN |   build |   address |   CAN win % after |   PGAA |
|--------:|:-------|:-----------|:----------------|----------:|:-----------------------------------------------------------------------|------------:|------------:|--------:|----------:|------------------:|-------:|
|       1 | CAN    | Hebert B   | Draw            |       100 | 4-ft, high, shot, open                                                 |        0.00 |        0.09 |    0.09 |      0.00 |             86.14 |   0.05 |
|       2 | GBR    | McMillan H | Front           |       100 | guard zone, controls 4-ft, guarding, open                              |        0.22 |        0.21 |    0.22 |     -0.12 |             85.53 |  -0.04 |
|       3 | CAN    | Hebert B   | Draw            |       100 | 4-ft, high, guarding, second, frozen (own), behind cover               |        0.22 |        0.43 |    0.21 |      0.00 |             88.21 |   0.16 |
|       4 | GBR    | McMillan H | Front           |       100 | guard zone, open                                                       |        0.51 |        0.40 |    0.29 |      0.03 |             86.27 |  -0.02 |
|       5 | CAN    | Gallant B  | Draw            |       100 | 8-ft, high, controls 4-ft, guarding, third, frozen (own), behind cover |        0.52 |        0.60 |    0.20 |      0.00 |             89.65 |   0.11 |
|       6 | GBR    | Lammie B   | Raise           |       100 | 8-ft, high, controls 4-ft, guarding, partly open                       |        0.48 |        0.85 |    0.31 |      0.01 |             92.78 |  -0.41 |
|       7 | CAN    | Gallant B  | Clearing        |       100 | removed from play                                                      |        0.38 |        0.85 |    0.00 |      0.10 |             91.98 |   0.07 |
|       8 | GBR    | Lammie B   | Draw            |        75 | 4-ft, high, guarding, frozen (opp), behind cover                       |        0.80 |        0.85 |    0.42 |      0.00 |             88.44 |   0.10 |
|       9 | CAN    | Kennedy M  | Clearing        |       100 | removed from play                                                      |        0.65 |        0.85 |    0.00 |      0.14 |             87.78 |   0.04 |
|      10 | GBR    | Hardie G   | Draw            |       100 | 4-ft, back, behind cover                                               |        0.86 |        0.93 |    0.21 |     -0.08 |             87.34 |  -0.08 |
|      11 | CAN    | Kennedy M  | Raise           |        75 | 8-ft, high, controls 4-ft, guarding, open                              |        0.87 |        1.73 |    0.28 |     -0.05 |             90.95 |   0.34 |
|      12 | GBR    | Hardie G   | Raise           |        75 | 8-ft, high, wing, open                                                 |        1.29 |        1.21 |    0.42 |      0.52 |             90.31 |  -0.08 |
|      13 | CAN    | Jacobs B   | Double Take-out |       100 | 8-ft, high, wing, second, open                                         |        0.54 |        0.61 |   -0.59 |      0.75 |             84.16 |  -0.41 |
|      14 | GBR    | Mouat B    | Double Take-out |       100 | 4-ft, high, shot, partly open                                          |        2.03 |        0.29 |    1.49 |      0.32 |             69.46 |   0.56 |
|      15 | CAN    | Jacobs B   | Double Take-out |       100 | 12-ft, high, controls 4-ft, guarding, second, frozen (own), open       |        0.40 |        0.53 |    0.24 |      1.63 |             93.70 |   1.01 |
|      16 | GBR    | Mouat B    | Double Take-out |         0 | 12-ft, high, wing, third, open                                         |        1.36 |        0.32 |    0.96 |      0.21 |            100.00 |  -0.61 |

**The setup (stones 1–5).** Hebert draws to the top of the four-foot: four-foot, in front of the tee, shot, open, a rock worth 0.09 to Canada at that stage. McMillan's centre guard is the hammer team's standard answer when it needs two: `guard zone, controls 4-ft, guarding, open`. Its build is +0.22, but its address is −0.12: the guard also puts Canada's shot rock behind cover, and a rock behind cover is graded higher whoever put the cover there. The model agrees that the guard helped Great Britain (Canada 86.1 → 85.5%) but barely; it is the stone the field throws here. Hebert then comes around and freezes to Canada's shot rock (`4-ft, high, guarding, second, frozen (own), behind cover`): build +0.21, Canada 88.2%, and the largest execution value of the setup (+0.16). A frozen non-hammer rock behind cover is exactly the trait the study found most dangerous to the hammer team (Section 4.4). Gallant adds a third, frozen again.

**The middle (stones 6–12).** The re-read after every stone shows what each shot did to the rocks already there. Lammie's raise (stone 6) puts a British rock in the eight-foot, partly open, but leaves Canada's buried rocks untouched and still behind cover: build +0.31 and Canada's grade up, the model's verdict −0.41 and Canada to 92.8%. Canada spends two stones clearing the guards (Gallant, Kennedy): they build nothing and address +0.10 and +0.14, the price of opening the house. Lammie's draw (stone 8, graded 75) comes to rest frozen onto a Canadian rock, behind cover: +0.42 of build and +0.10 of execution, Canada down to 88.4%. Where the grades jump between rows 10 and 11, the stage of the end has changed (stones 6–10 to 11–15 are graded with different weights); a stone's own build and address are always read with a single stage's weights, so no stone is credited with the change.

**The end game (stones 13–16).** This is where the relations (Section 4.7) and the individually described rocks (Section 4.6) take over, and where the ledger and the model part company. Jacobs' double (stone 13) removes two British rocks (address +0.75) but leaves his own rocks open and off the button (build −0.59): the rocks moved a lot in Canada's favour and the chance of winning fell (90.3 → 84.2%, −0.41 of execution), because the model reads what the position leaves Mouat. Mouat's double (stone 14) is the best British stone of the end: Britain lies shot in the four-foot with more behind it (grade 2.03), and Canada falls to 69.5%, +0.56 of execution. Jacobs answers with the stone of the game: a double that takes out Britain's counters and leaves Canada second and frozen at the top of the twelve (address +1.63, execution +1.01, Canada 69.5 → 93.7%). Mouat's last stone, a double graded 0, misses: Canada steals one and wins.

The last row shows what the ledger is not. After Mouat's miss Britain's rocks still grade well (build +0.96): they are in the house, on the wing, counting third. But the end is over, the count is Canada's, and the model's value is the result itself. The ledger reads rocks as rocks-in-play; Points Gained reads the position, which at the last stone is nothing but the count.

---

## 9. Conditions and Field Adjustment

Ice varies: swing, speed, pebble, flatness, and how they change over a game and a week. The design does not model any of it. It follows strokes gained in golf, where the difficulty of a green is never modelled; it falls out of how the field putted on it that week, and a player is measured against that field. If draws to the four-foot are made 65% of the time at one event and 80% at another, that difference *is* the ice, and a made draw at the first event earns more.

This is done at two levels. At the reporting layer, a player's execution at an event is reported relative to that event's field for the same shot type and hammer state (Section 11). At the model level, g takes the event's strength rating, so the field a shot was played in sets the expectation; the residual per-book effect that the difficulty model estimates (ice, conditions, grader) is reported but not fed to g, because a per-book value identifies the book and the trees fit book-specific outcome rates on it that do not transfer. Sheet and session effects, shrunk hard towards the event, are a later step. The value function f is not conditioned on event: a position's worth under typical play is a property of the game, and ice effects on value are assumed to wash through execution.

---

## 10. Value Mapping V

### 10.1 Why blank cannot be zero

With V = expected points and blank = 0, a skip who faces two on the last rock and executes the called double-and-roll-out is scored *below* a skip who sticks and takes one. In the middle ends that is backwards: the blank keeps hammer, and at the elite level hammer is worth more than the point.

### 10.2 Hammer-adjusted points

Let **N** be the hammer team's expected net score in one end and **H** the infinite-horizon value of holding hammer: treating the game as a Markov chain over ends with a stationary outcome distribution, H = N + (P(blank) + P(steal) − P(score)) · H. From the thrower's perspective,

    v(outcome) = points + H × hammer_after

with `hammer_after` = +1 if the thrower's team keeps hammer (blank or steal) and −1 if it scores. Blank outranks a single exactly when H > 0.5.

On the archive, from 19,175 men's and 18,410 women's ends:

| | N | H |
|---|---|---|
| Men | 0.81 | 0.61 |
| Women | 0.72 | 0.55 |

so a blank is worth 0.61 to a men's team and a single 0.39, and "don't take one in the middle ends" is a fact about elite play rather than a maxim. The hammer team's outcome distribution is 13% blank, 34% one, 23% two, 9% three or more, and 21% stolen on.

### 10.3 Win probability

V(D; situation) = Σ D(o) · v(o | score difference, ends remaining, hammer), where v is the win probability after the end, from a table built by backward induction over an end-outcome distribution conditioned on the situation and shrunk towards the pooled distribution. The table comes from line scores, which every results book carries, including the 116 without shot-by-shot pages. Same interface as 10.2; every shot carries both currencies.

Some values from the table: tied at the start with hammer, 63%; tied in the last end with hammer, 80%; up two without hammer with three ends left, 81%; down one with hammer with five left, 44%. The named regimes fall out of the shape of v: tied in the last end with hammer, one and two are each worth a win; up three with hammer in the fourth, the call values in points are −0.02 per shot and in win probability zero.

Hammer-adjusted points is the default reporting currency because it is easier to read and does not compress blowout ends; win probability is used for situation questions and to keep points from scolding a team for protecting a lead.

---

## 11. Outputs and Reporting

### 11.1 Per shot

Every shot carries D(S), D(S | C), D(S′), the three values in both currencies, `pg`, `pg_call`, `pg_throw` and their win-probability counterparts, the thrower, the call, the grade, and the game situation. This table is the substrate for every report and for any future question interface.

### 11.2 Player reporting conventions

**Execution first.** Players are rated on execution, PG: Throw. It is the part of a shot's value that does not depend on reading the skip's mind, and it credits what curlers credit: the position left, whatever the scorer wrote down. A hit that ticks a guard through a port and improves the position is a miss on the sheet and a gain here; a skip who calls plan B while the rock is moving gets the position that plan B produced. The call component is reported beside it, as a secondary column.

**Relative to the field.** Raw PG: Throw averages slightly positive, about 0.05 points per shot, because every throw is a chance to improve one's own position, and fourths carry most of the leverage. Players are therefore reported as execution minus the field's mean for the same shot type and hammer state, either the whole corpus or that event's field, so that a fourth's doubles are compared with other fourths' doubles rather than with a lead's guards.

**The spread, not just the average.** A player's shots are heavily skewed: most land close to the field's expectation, and a few large misses or makes decide games. The official percentage counts every shot once and cannot see this, and a plain standard deviation mostly measures the leverage of the positions a player threw from. The tables therefore show the spread directly: `reliability`, the share of shots at or above the field's expectation; `avg_make` and `avg_miss`, how far above or below it those shots were on average; the counts of big makes and big misses (more than half a point either way); and `worst5`, the five costliest shots summed. `net`, the mean over every shot, combines them and is the sort. The same tail columns are given in win probability (`_wp`), because a costly miss in a decided game and one in a tied last end are different events.

### 11.3 Reports produced

- **Model report:** corpus counts, the hammer distribution, N and H by discipline, held-out log-loss by model and by rocks remaining, conservation and calibration, win-probability examples; then the whole-corpus performance tables, with teams in win probability and players by execution (teams by record and where the result came from: first-end hammer, their own stones, the other team's stones, each against the field; players per position by the execution columns of Section 11.2, with big makes and misses per 100 shots; execution by shot type) and the stratified model checks. `pointsgained model-report` rewrites it from the saved run summary without refitting.
- **Strata:** by discipline and tier, by hammer, by game state and hammer, by shot type and hammer, players relative to the field, teams by hammer; all in both currencies.
- **Per-event leaderboards** (`pointsgained events`): one row per player and event with position, shots, games and the execution columns relative to the event's field: reliability, average make, average miss, big makes and misses, worst five, and the mean as `net`; then the effect on win probability for reference (big makes and misses, best and worst five), the call value and the official grade. Sorted by the mean (`net`), then reliability. The CSV also carries the median, floor, variability and slot-relative execution. The team table above the position groups is the team-level view, in win probability per game: `net`, the record (a win is +50, a loss -50), sorted on, and what it adds up from: `dsc`, the start a team had from first-end hammer (the draw shot challenge; seeding in playoffs), `own`, what the team's stones did to its chance of winning against what this event's field's stones did at the same point of the end (so a team is not credited for throwing more stones, and the parts still add up to the record), `allowed`, the other team's stones the same way from this team's side, and `other`, what no stone accounts for (concessions between ends, missing pages); then `control`, the mean chance of winning at the start of each end, the second sort, which credits a team that leads early and keeps the game quiet. There are no execution columns: teams are reported in win probability, individuals by execution.
- **Game report** (`pointsgained game`): one game from the per-shot table. The currency follows the level of the table: team-level tables are in win probability, the currency that knows which end it is (Section 10.3); individual tables lead with execution in hammer-adjusted points, the leaderboard measure, with the effect on win probability beside it. So: an end table with the running score, one team's win probability before and after the end and the swing, and nothing else; a players table with each player's PGAA (points gained above average, `pg_throw` in the tables) summed over the game, their worst and best stones, the grade, and their stones' summed win-probability effect as a reference; the ten largest swings; and every stone in the order situation, shot, execution (PGAA and call), effect (win probability after and the change). The conservation identity holds in win probability too (one team's changes minus the other's is the end's swing); the report warns only if it fails. Beside every stone it prints the rock ledger (Section 4.5): each team's rock grade after the stone, and the stone's build and address; under each end header, each team's grade after the free guard zone, after stone 12 and before the last stone, and the end's peak **temperature**, both teams' grades added together (high in an aggressive end with many rocks in play, low in a conservative one). It is the report that lets a leaderboard number be traced to the stones that produced it.

Every per-shot value is a difference of model outputs, so these tables are exactly reproducible from the Parquet tables and the fitted models. `reports/samples/` keeps finished copies in the repository (the model report, the test set, per-event leaderboards for every Olympics and World Championship since 2018, the two 2026 Olympic finals shot by shot, and the trait, early-end and stone studies) with a README on how each is built and what it says.

---

## 12. Phase 2: Physics, Transitions, and the Best Call

Phase 1 answers "what has this been worth." Phase 2 answers "what could this have been worth," which needs counterfactual calls, and therefore a model of what happens when a shot is thrown.

- **Simulator.** Collision geometry, rolls, raises and runbacks are deterministic physics; the Digital Curling platform and similar simulators implement them. A simulator answers the inch-level questions the expectation model has to learn statistically: is the double on, where does the shooter roll, does the raise reach.
- **Execution error model.** The only stochastic component. Learned from the delivered-stone marker: for each (type, inferred target, skill scalar, event effect), the distribution of where the thrown stone arrived relative to the target. Seeded in the modelling phase: `pointsgained intent` writes the delivered stone's rest relative to the modal target for every draw with a marker, by grade, skill tercile and rocks-remaining band (`reports/execution_error.md`). On late-end draws graded 100% the median lateral error is about 8 in and the depth interquartile range about 27 in, part of which is the target cell's coarseness; at 75% the depth spread is 41 in.
- **Transition model.** P(S′ | S, call) = simulator applied to the call with delivery sampled from the error model. It turns the geometric relations of Section 4.7 (is the draw open, is the double on) into simulated shot-availability probabilities.
- **Rollouts.** From any position, simulate the remainder of the end under a policy, initially the empirical policy P(C | S, situation), evaluating with f at a fixed depth. When the policy is replaced by an optimising one, there is a single objective for both teams, since v is zero-sum, and the named strategies emerge from the shape of v.
- **Best-call baseline.** For each position, evaluate each candidate call by rollout and take the maximum; selection under this baseline is the regret of the call made. The best call is skill-dependent, so it must be evaluated at the thrower's skill scalar. Jacobs' ninth-end runback clearing in the 2026 final is the test: at the field's skill the field baseline calls it a poor menu; at his, it may have been the best shot on the sheet. Elite skips disagree in exactly the positions where it matters, so the best-call baseline is reported with uncertainty and is never the headline number.

---

## Part IV. Sample studies

Each study below is produced by a command in the package, from the corpus tables and the Points Gained table, and each is a template: change the position, the call family or the situation and the same code answers a different question. The samples are in `reports/samples/`.

| Study | Question | Command | Where |
|---|---|---|---|
| The double on a split | How often does the opponent double off two stones, by how far apart and how staggered they are? | `frontend` | `reports/samples/front_end.md` |
| The runback | How often does a runback on the shot rock leave the thrower lying shot? | `frontend` | `reports/samples/front_end.md` |
| Rock traits | What have rocks with each trait, held by each team at each stage, been worth? | `traits` | Section 4.4; `reports/samples/traits.md` |
| The early end | What do lead and second values measure, and does winning the early end relate to winning the game? | `frontend`, `experiment` | `reports/samples/front_end.md` |
| Runbacks by player | Are the dominant skips the best at runbacks? | `frontend` | `reports/samples/front_end.md` |
| Player execution | Who executes best against the field, and how: typical shot, misses, tail? | `events`, `game`, `model-report` | Section 11.2; `reports/samples/events/` |

---

## Part V. Contributing, open problems and status

## 13. Contributing

The project is built to grow in three directions, and each has a place to start.

**Data.** The corpus is international championship curling from the World Curling results books. The single most useful contribution is more games in shot-by-shot form: national championships (the Brier and the Scotties above all), the Grand Slams, and World Curling Tour events, then anything else with the stones recorded after every shot. A source enters through an adapter that writes the six tables of Section 2.6; a source that is itself a results-book PDF in the CURLIT format needs nothing but the file. Line scores alone are useful too: they feed the win-probability table. If you hold or know of such data, open an issue on the repository.

**Points Gained.** The expectation models are gradient-boosted trees on rock traits, grades, the individually described rocks and the thrower's relations (Part II), trained with a local target, and the evaluation harness is in place: `pointsgained experiment` fits a variant on a time split or a held-out-book fold and scores it on log-loss against the end's result and on the early-end checks of Section 7.7, and `pointsgained misprice` shows where it over- or under-prices positions (Section 7.7). The trait vocabulary and the relations are the natural places to contribute: a new trait is a line in `core/traits.py`, a new relation a function like `core/draw.py`. Section 14 lists the known weaknesses; the positions the model misprices are concrete targets, and the scenario probes are their tests.

**Studies.** Every study in Part IV reads the same tables: `points_gained.parquet` (one row per stone, with the three outcome distributions, both currencies, the call and execution split, the thrower and the situation), `rock_traits.parquet` (every rock's traits in every position), `rock_ledger.parquet`, `configurations.parquet` (the labels and measures of every position), `stone_lives.parquet` (every stone tracked through the end), the per-book extraction tables, and the feature cache. `model/trait_study.py` and `model/frontend.py` are worked examples of study modules. The open problems of Section 14 are open; a study that matches on the score, ends remaining and position and compares the choices is the natural next contribution, and finished reports belong in `reports/samples/` with a line in its README.

---

## 14. Open problems

One list of what is not yet solved, grouped by where it sits; most items say where to start. `open_problems.md` states the main ones, and three more (comparing fields, credit beyond the thrower, uncertainty), in plain curling terms for readers outside the project.

**The expectation model**

1. **The value of an early position.** With twelve or more rocks left f is still within about 0.02 log-loss of the trivial model. Reading rocks by their traits made early values less flat (calibration slope 0.95 against 0.92) and, for the first time, related a team's early-end values to winning the game, but the early end is still where the model knows least. Whether it is intrinsically unpredictable or the vocabulary is still missing what a skip reads is open. Start: the log-loss by rocks remaining, the trait study (`pointsgained traits`), the scenario probes.
2. **Free guard zone eras.** The four-rock and five-rock rules are pooled with an era flag. Whether early-end positions need a separate f per era is untested; only f is affected, since g pools across eras.
3. **Learning the vocabulary from data.** The rock traits (Section 4.3) are a hand-written vocabulary whose worth the corpus measures; the configuration labels (Section 4.8) were hand-written tests with hand-set thresholds. Can rocks and positions be grouped by what they lead to, so that the vocabulary is discovered rather than written, and which traits can merge (the Jaccard overlaps of Section 4.3) or should split (open to one side only, a curl-aware exposure)? Start: `rock_traits.parquet`, the stone-type tables of the trait report, `configurations.parquet`.
4. **Rare, decisive situations.** The peel miss in a tied last end and the tight guard on a lonely steal stone come up a few hundred times each, fewer than the trees need to carve out a state of their own. Candidates: a targeted relation (guards remaining when the hammer team must score; the runback distance on a lonely steal) or a situation-weighted correction. Start: the scenario probes as tests (Section 7.7), `pointsgained misprice`.
5. **g at the last rock.** The rock-trait model matches or beats the hand-built one everywhere except g with one rock left (0.007 behind on the time split, 0.004 by book). The call is known there, so the gap is something the old configuration measures told g about the called shot's geometry that the relations do not yet: a candidate is the relation between the called shot's target (the struck stone) and the double and runback geometry.
6. **The straight tap.** Where a straight tap onto a rock around the four-foot beats the draw, the model under-prices the position by 0.11 to 0.13 points, in every era. A tap relation and a one-column overlay recovered at most a fifth of it, so it is recorded as a known blind spot rather than patched. The double tap is not built.

**Calls and execution**

7. **The best call, and the skip against it.** PG: Call is measured against the field's usual call, not the best available one (Section 6.3); Jacobs' ninth-end runback clearing in the 2026 final is the test case. A best call depends on geometry, the ice (how much it curls decides whether a come-around or a chip is on, as the angle does for a take-out; the books do not record it, so it has to be inferred from how shots behaved), the thrower's make rate and the value of each outcome in the game, and skips manage risk across several stones. Start: the empirical menu (calls the field made from similar positions, valued by g), then the transition model of Section 12.
8. **Aggressiveness, and strategy and execution together.** A call's value depends on who throws it. One hypothesis: the best teams accept calls whose field outcome distribution D(S | C) has a fat bad tail, because the weaker teams, not they, produce that tail. Testing it, and then reporting per team and per skip how much downside they accept relative to the field in the same situation and how much of it they produce, would describe aggressiveness by the shape of the outcomes a call accepts rather than by shot type. Separating the right call for a team from the right call for the field without circularity is open. Start: D(S | C) by team, split by the downside of the call.
9. **Execution error from the diagrams.** The delivered-stone marker and prior-position rings (Section 2.2) record where draws came to rest and which stone a hit struck; `pointsgained intent` seeds an error model (`reports/execution_error.md`). The target is never recorded, and inferring it from the result leaks execution into the call (Section 7.3). Start: `intent.py`, the execution-error report.
10. **Difficulty without selection.** Make rates measure shots as chosen: the angled runback shows no penalty because it is called only when it is on (`reports/samples/front_end.md`). The correction needs every position where a shot was available, called or not, and a definition of available; the double and runback relations of Section 4.7 are one. Start: the double and runback tables, `combo_features.parquet`.

**Player and team reports**

11. **Leverage-normalised consistency.** Execution divided by the width of the call's outcome distribution, so that steadiness is comparable across positions.
12. **The front end's shared component.** A team's lead and second values move together (correlation 0.64, 0.36 after the team's call and configuration mix) and not with the fourth's. Sweeping, ice reading, the skip's broom or style could each be the cause; the corpus cannot separate them directly, but the component's relation to results can be measured.
13. **Seconds' repeatability.** How well a second's execution in one half of an event predicts the other half: the one measure the rock-trait model made worse (correlation 0.47 to 0.41, held out by book).

**Data and level of play**

14. **Event ratings and conditions.** The ratings in `data/event_strength.csv` are tier defaults (Worlds 100, Europeans A 85, juniors 70). The field strengths derived from results already disagree with them in places: the Olympics sit above the Worlds, the Olympic qualifiers and the Pan-Continental championships well below Europeans A. Below the event, sheet and session effects need shrinkage towards the event before they can be used (Section 9).
15. **Player identity.** Name changes are handled by the alias table (Section 3.2); a stable player id across events would replace it.

---

## 15. Status and next steps

Built: the ingestion pipeline and the corpus (Part I), the rock-by-rock reading of positions (Part II), the expectation models, Points Gained and the reports (Part III), and the sample studies (Part IV). Next: studies of shot geometry by level of play, high-value-shot leaderboards, strategic situations and the open problems above; then Phase 2 (Section 12).

The pinned test set (`pointsgained testset`, `reports/samples/testset.md`) is the face-validity check for every refit: six last-rock shots from the 2026 Olympic men's tournament, among them Jacobs' ninth-end runback clearing in the final, whose values must keep their signs and order.

---

## Appendix A. Retired approaches

The ideas below were built, measured and replaced. They are kept here because each taught something the current system relies on, and because the numbers are the baseline any new idea has to beat. The code for all of them is in the repository history at the tag `handcrafted-features-final`; `git checkout handcrafted-features-final` restores it.

### A.1 Hand-built position features

The first expectation models read a compact vector of 26 hand-built numbers per position: rocks remaining, rule era, stones in play; the count clipped at ±3, the shot rock's ring, the margin between the shot rock and the first opposing stone, the owners of the second and third stones, the boundary gap and a near-tie flag; each team's stones in the house and behind the tee; guards per team by lane (left, centre within 24 in, right) and the depth of the nearest centre guard; a crude straight-line cover test on the shot rock and the button; and each team's nearest stone. The cache still computes them (`model/features.py`) as position descriptors for studies and reports, and the model takes a handful directly (the count, its margins, each team's nearest stone). As the model's representation they were the limit by September 2026: tree capacity had plateaued, and with twelve or more rocks left the models were within 0.02 of the trivial model.

### A.2 Configuration labels as model inputs

The configuration vocabulary (Section 4.8) entered f and g as 27 labels and 7 measures (the double on each team's two best stones, the runback on the shot rock, the swing if the shot rock were removed). Adopted with the local target in September 2026 (cross-validated f 1.4704 → 1.4677, g 1.4472 → 1.4457), with the acceptance cases ordered correctly for the first time: the split house restored flat 1.053 (realised 1.082), staggered 0.976 (0.972). The labels remain the studies' vocabulary; as inputs they were replaced by rock traits, slots and the thrower's relations.

### A.3 Rock potential from stone tracking

Every stone of every end is followed through the diagrams (`core/tracking.py`, `stone_lives.parquet`: 75% of stones unmoved within an inch from one diagram to the next, moved ones matched through the prior-position rings). From the final diagram, each stone's role: it counts, it covers a counter (in front within a stone's width), or it backs up a counter (just behind). Role rates by team, stage of the end, zone and one-foot cell, shrunk towards the zone and cross-fitted by book, gave each position a **rock potential** per team. A colour-blind version credited cover and backing to the team whose counter they served, because a beaked shooter left in front is cover for the other side (the beaked peel costs about as much steal as leaving a guard). Adopted as `potential_cb` in September 2026 (cross-validated f 1.4665, g 1.4450) and read stone by stone as the potential ledger (build, address, temperature), the first measured form of aggressive and conservative play. A version with monotone constraints (six cumulative binary models so that expectation must rise with the hammer team's potential) lost 0.017–0.018 in f and was not adopted. Rock potential was the right idea measured the long way round: rock traits read the same thing from where the rock is, without following it anywhere, and agree with it at 0.60–0.78.

### A.4 The split model

The free guard zone valued by its own models, on a lean description built around rock potential, taught by the endgame model's value at the handover (hard or blended). It valued early positions slightly better (twelve or more rocks left 1.6048 against 1.6068 on the time split) but made credit worse in every variant: the see-saw returned and seconds' agreement with their grades fell, because training every setup position on one distant point flattens the differences between consecutive positions. The same failure sank the **phase target** (setup stones trained on the value at the end of the free guard zone), and a **blended target** (the local target mixed with the end's result) was not needed.

### A.5 Raw geometry

A convolutional network on the rasterised sheet (171 × 325 pixels at an inch per pixel, a channel per team, coordinate channels, a narrow bottleneck against memorisation) lost to the trees in every band of rocks remaining (f 1.493 against 1.455 on the time split), and a hybrid with the hand features in its dense layer did too (1.487). It passed the monotonicity checks the trees failed (an opponent stone appearing inside the hammer team's shot rock raised the hammer team's value in 22% of synthetic cases), which is one reason the slots describe the shot rock individually. The set encoding (a permutation-invariant network over stones) was never built; slots are the tabular version of the same idea for the few rocks that decide the end.

### A.6 Per-player skill in g

A shot-difficulty model on the official grade estimated a skill scalar per player and an effect per event, and g briefly took the expected grade of each shot at the thrower's skill (time split g 1.4373 → 1.4297). It was withdrawn: level of play belongs to the field, never to the player being measured (a fairway shot is not judged against Tiger Woods' putting), and grades are too grader-dependent to rate players with. g takes the event's strength rating instead, and the difficulty model survives as a report (`pointsgained difficulty`).

### A.7 What the old model read, and what replaced it

| Retired input | What replaced it |
|---|---|
| 26 position features | Rock traits per team, the count and its margins, each team's nearest stone |
| Configuration labels and measures | Shot rock, second, third and nearest guards described individually (slots); the draw against multiple stones; doubles and runbacks |
| Rock potential (tracked) | Rock grades (read off the position); the rock ledger |
| Regime and goals columns | Nothing: the game situation columns and the value mapping carry the regime |
| Monotone ordinal model | Nothing: the slots and the trees' inputs fixed most of what it was for |

On the time split the replacement's f is better at every number of rocks remaining except before stones 1 and 3, where it ties (f 1.4497 against 1.4521 overall), and its g ties overall (1.4299 against 1.4299) while giving up 0.007 at the last rock; on a held-out fold of books from every year it is better on both (f 1.4555 against 1.4571, g 1.4349 against 1.4353), again with g slightly behind at the last rock (0.004).
