# Curling Analytics: A Shot-by-Shot Ingestion Pipeline and Corpus, Points Gained, and Sample Studies — Design Document

**What this is.** We're sharing a method for ingesting data about curling games that are consistent with the format in what are called the "Results Books", which are made available by the World Curling Federation (and via partners like CurlIt) for every major WCF-sponsored curling event, and the Olympic Games, going back to 2013. We've used this pipeline to create a corpus that reads every stone of every end of 4,150 international games into tables: where every stone was before and after every shot, who threw it, what was called, how it was graded, and how the end and the game came out, which in turn forms the basis for doing shot-by-shot analysis.

**How this document is organised.** Part I describes the ingestion pipeline and the corpus: where it comes from, how it is extracted and validated. Part II describes how a position is read: rock by rock, every rock described by objective yes/no traits, re-read after every stone, with what rocks like that have been worth taken from the corpus, and a few relations between rocks (the draw to beat, doubles and runbacks) for the rocks that decide the end. Part III introduces **Points Gained**, a system for valuing individual curling shots: an expectation model for positions, f and g, which says what a position and a call have been worth under the field's play, and a value for every stone as the change it made to that expectation; Section 8 walks through one end of the 2026 Olympic final stone by stone. We use it to rate execution, but also to value positions and shots in strategic analysis. Part IV describes a collection of initial studies that the corpus has made possible, most of which build upon the shot data and Points Gained. Part V describes how to contribute, and records open questions and status. Appendix A records the approaches that were built and retired along the way.

**Status (September 2026).** The corpus is built and validated: 92 results books with shot-by-shot pages, 609,014 shots. The expectation models read positions rock by rock (Part II) with the game situation, the event's level of play and, for the call, the called shot and its target; early positions are trained on the value two stones later (Section 7.5). This replaced a stack of hand-built descriptions and matches or beats it on held-out events (Section 7.6, Appendix A). Studies done: rock traits (Section 4.4), shot geometry for doubles and runbacks (Section 13), the early end (Section 14), runbacks by player (Section 15), player execution (Section 11). Next: common strategic situations (Section 16).

---

## Part I. The ingestion pipeline and the corpus

## 1. What the project provides

Four layers, each usable on its own and each open to contributions (Section 17):

- **An ingestion pipeline** (Section 2). It reads the results-book PDFs directly: the per-shot diagrams are decoded from the embedded images rather than rendered, stones are detected and placed in inches on a fixed sheet frame, the panel text gives the thrower, call, turn and grade, and validation gates check every book before it is used. The output is six tables per book with a documented schema, and that schema is the contract for any other source: a new source of games needs an adapter into the same tables, and everything downstream runs unchanged (Section 2.6).
- **A corpus** (Section 3). The pipeline run over every results book with shot-by-shot pages: 92 books, 4,150 games, 609,014 shots, with stratum labels (event, tier, discipline, era, player, position) on every row.
- **A way of reading positions** (Part II). Rock by rock: the exact count, every rock's traits (in the four-foot, behind cover, frozen, on the wing, ...), each team's rocks graded by what rocks like them have been worth, the rocks that matter kept whole, and the relations the thrower plays against (the draw to beat, doubles and runbacks). A configuration vocabulary in the terms a skip uses (a split house, the deuce is loose, the steal is on) remains for studies.
- **Points Gained** (Part III). An expectation model for positions and calls, and a value for every stone in two currencies (hammer-adjusted points and win probability), split into the call and the execution. Every value is a difference of model outputs, so any grouping of stones (a player, a phase of the end, a shot family, a configuration) can be valued the same way.

The studies of Part IV are examples of what the four layers support, each produced by a command in the package, and templates for further studies.

## 2. The ingestion pipeline

### 2.1 Source

The pipeline reads World Curling results books, as published in the CURLIT results-book directory at `curlit.com/results`: one PDF per event, with a shot-by-shot page for every end of every game in the events that have them. The directory lists 310 results books; 208 are team-of-four men's or women's books from 2013 onward and in scope. All 208 were downloaded (2.3 GB). Only 92 contain shot-by-shot pages: 25 tier 1, 42 tier 2, 23 tier 3, 2 tier 4. The other 116 (Europeans B and C, Seniors, Junior-B, Pan Continental B, the qualifiers and the Universiade) are line scores and standings only; they still feed the win-probability table. Any PDF in the same format, from any event, goes through the pipeline unchanged; other sources enter through an adapter (Section 2.6).

Jordan Myslik's earlier extraction (`jwmyslik/curling-analytics`) is the precedent for this work, and showed that the shot diagrams could be read at scale. It can no longer be rerun because its source host no longer responds. It converted the PDF pages to XML and images; this pipeline reads the embedded diagram images directly. Nothing here depends on it.

### 2.2 What the diagrams are and what they carry

The per-shot diagrams are not drawn on the page; they are embedded raster images, 300×600 pixels (occasionally 301×601), 4-bit indexed colour with an exact 16-entry palette, losslessly compressed, in every book examined from 2014 to 2026. A few recent small books (2026 juniors) use lossy 8-bit images. The extractor never renders a page: it reads the image stream and palette from the PDF, classifies pixels by nearest reference colour, and reads the panel's text by coordinates.

Geometry is fixed: centre line at column 149, tee line at row 439, 12-foot outer radius 118.5 px, hog line at row 20, back line at row 560; 1.646 px per inch, or 0.61 in per pixel, in both axes. Coordinates are in inches with the pin at (0, 0) and y positive towards the hog line.

Facts established while building the extractor, each of which cost a bug before it was known:

- **Alternate ends are drawn with the house at the top.** Play changes direction each end and the sheet is drawn from a fixed vantage point. The extractor detects the orientation from the ring position and rotates the image 180° into the thrower's frame; the stones-remaining and stones-removed counters swap strips accordingly. Before this was handled, half the ends reconstructed the wrong score.
- **Palettes vary by template.** Yellow is (255,200,50) in the WCF template, (255,230,0) in the Olympic template, (255,255,0) in older books; the 12-foot is blue in most books and green in the 2024–2026 World Championship books; the four-foot is pale yellow, green or pink. Orientation and calibration use any ring colour rather than a specific one, and unseen colours far from every reference are treated as house paint.
- **Yellow glyphs carry crosses.** Plain in the WCF template, a blue cross in the Olympic template, a black X in 2014-era books, anti-aliased into arbitrary tones in lossy books. Stones are therefore detected by a disk template: the fraction of stone colour inside a stone-sized disk, with local maxima above half coverage taken as stones. A filled disk scores near one whether or not a line crosses it, a hollow ring scores about a quarter, and two touching stones give two peaks eighteen pixels apart.
- **Delivered-stone marker.** A small black mark at the stone's centre in the WCF and Olympic templates; a two-pixel outline in the 2014 and Cortina templates. Both are read, the dot rule excluding pixels that a cross would place at the centre. The marker is absent when the delivered stone left play, which is most clearing and take-out shots, so about 11% of shots have no marked stone. The delivered stone's colour agrees with the thrower's team in 99.8% of marked shots, which is also the cross-check for team colours.
- **Prior positions.** Hollow rings mark where moved stones were before the shot. They are stored as separate rows.
- **Counters.** Small glyphs at the top of the diagram count stones not yet thrown per colour; full-size glyphs at the bottom count stones removed. The census, thrown plus on the sheet plus removed equals eight per colour, holds in 99.9% of panels and is the main extraction gate.
- **Text variants.** Percentages with arrow glyphs for the turn from 2015; 0–4 grades written "Out4" or "In 0" in 2014 and as a bare digit in 2017; type names without hyphens; glued header tokens ("End1", "CAN-Canada", "0+0(this", "11+") in the 2017 template and whenever a running score reaches double digits; an `X` in place of the end score for an end that was not completed; a note line ("Free guard zone violation") that pushes the panel rows below it down the page. One tokeniser and a row grid derived from the image positions handle all of them.
- **Duplicated reports.** The 2014 Olympic book carries one game's shot-by-shot report twice; the first copy is kept.
- **Resolution limit.** The count function (Section 4.2) applied to the final position agrees with the recorded end score in 96 to 98% of ends in recent books and about 89% in 2014–2017 books. The disagreements are stones within an inch of each other or of the twelve-foot edge, which a 0.61 in/px diagram cannot resolve and which were measured on the ice; sweeping the biting radius does not improve agreement. The recorded score is therefore the label and the reconstruction is the gate.

### 2.3 Pipeline

**Inventory.** `pointsgained inventory --check` fetches the directory page, which is plain HTML with direct PDF links, classifies each book by event family, tier and discipline, and HEAD-checks every in-scope link. Mixed doubles, wheelchair, mixed-team and youth books are out of scope.

**Download.** `pointsgained download` fetches in-scope books sequentially with a delay, resuming from disk.

**Survey and extraction.** `pointsgained batch` runs, per book and in parallel: a survey (does it have shot-by-shot pages; which template, grade style and image format), extraction, and validation, and writes the gate results back to the inventory. Books without shot-by-shot pages are marked excluded.

**Validation gates.** A book is `validated` when the stone census holds in at least 95% of panels, score reconstruction agrees with the recorded score in at least 85% of ends, hammer alternation is violated in at most 1% of ends, and at least one game was found. The thresholds are set to catch extraction failures, which show up as agreement rates near 50 to 60%, while admitting the older books' higher rate of inch-level ties. Every book with shot-by-shot pages passed.

**Audit.** `pointsgained audit` draws random panels with detected stones, delivered marker and prior rings overlaid onto a contact sheet.

**Storage.** Raw PDFs by year; Parquet tables per book; the inventory CSV as manifest; nothing enters training that is not validated and in scope.

### 2.4 Tables

Extraction writes six Parquet tables per book, with the book, page and panel of every row as provenance.

| Table | Content |
|---|---|
| `games` | Book, discipline, date, start time, session, sheet, the two team codes and names, their colours, report code |
| `ends` | Per end: running score before and after for both teams, this end's score, conceded flag, hammer team (inferred), Total Score and Time left box, colour source |
| `shots` | Per shot (1–16): team, colour, player, shot type, turn, grade (raw and 0–100), note line, stone counters (remaining and removed per colour), stones detected per colour, delivered-stone colour, orientation flag |
| `stones` | Per stone per shot: colour, pixel and inch coordinates, delivered flag, and prior-position rings as separate rows |
| `line_scores` | From the Game Results pages: per team, last-stone-first-end flag, score per end, extra ends, total |
| `players` | From the Game Results pages: position, function (skip / vice), game and cumulative percentage |

The `turn` field is kept: it is free, it matters for in-turn versus out-turn execution modelling, and mirroring (Section 2.5) must flip it.

### 2.5 Preprocessing

1. Convert coordinates to inches and rotate alternate ends into the thrower's frame.
2. For each shot, assemble the pre-position (after the previous shot; empty for shot 1) and the post-position.
3. Determine hammer from shot order (the team throwing shot 1 does not have hammer) and check alternation against the recorded scores.
4. Attach the recorded end score as the label; conceded ends carry none.
5. Assign rule era: four-rock free guard zone before the 2018–19 season, five-rock after.
6. Relabel stones `hammer` / `non_hammer` (Section 6.4) and record whether the thrower holds hammer.
7. Mirror every position left-right at training time (labels unchanged, turn flipped).
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

Player names need care. The books use surname plus initial, in varying case, and a player's team code changes between events (Scotland at the Worlds, Great Britain at the Olympics); reports key on the upper-cased, whitespace-normalised name within a discipline. Genuine name changes ("SCHWARZ B" in 2022, "SCHWARZ-VAN BERKEL" from 2025) are handled by an alias table (`data/player_aliases.csv`, Section 18).

---

## Part II. Reading a position rock by rock

## 4. The idea

### 4.1 Principles

A skip standing in the house does not see a feature vector. They see rocks: this one is buried in the four-foot, that one is sitting open on the wing, that guard is doing nothing, those two are frozen and will not come apart. The expectation of a position is, to a first approximation, the sum of what its rocks are good for, adjusted for the few relationships between rocks that decide the end (can the last rock draw inside the shot rock, is the double on, is there a runback).

The system reads a position the same way:

- **Every rock is described by objective yes/no traits** (Section 4.3): in or touching the 4-, 8- or 12-foot, in front of or behind the tee, on the wing, in the guard zone, controlling the path to the 4-foot, guarding a rock in the house, shot, second or third shot, frozen onto its own colour or the other, and open, partly open or behind cover. The traits overlap by design; a rock in the four-foot is also in the eight and the twelve.
- **The house is re-read after every stone.** A rock's traits are whatever they are in the new position: a rock that was open is behind cover once a guard lands in front of it; a rock that was shot is second once another comes to rest inside it; a removed rock is simply gone. Nothing is tracked. What happened to a particular rock is a question for studies (the corpus keeps stone identities, Appendix A.3), not for the expectation.
- **The corpus says what rocks like that have been worth** (Section 4.4): for each trait, held by the hammer or the non-hammer team at a given stage of the end, the distribution of the end's results. Added up, those become grades for every rock (Section 4.5), and the change in each team's grade across a stone is that stone's contribution to the rocks in play, the **rock ledger**.
- **The rocks that matter are kept whole** (Section 4.6). Counting traits per team loses which rock has which trait: "the shot rock is open" and "a guard is open and the shot rock is covered" can give the same counts. The shot rock, second and third shot and each team's nearest guard are therefore passed to the model with their whole trait vectors.
- **A few relations are computed directly** (Section 4.7): the draw to beat, and doubles and runbacks, from the thrower's side. These are the geometric configurations that unlock more than playing against one rock; they are what the last few stones of an end are about.

The expectation model (Part III) reads exactly these: rock traits per team, grades, the rocks that matter, and the relations, plus the count, the game situation, the event's level and, for the call, the called shot and its target. It replaced a stack of hand-built descriptions (26 summary numbers, 27 configuration labels and 7 measures, and a tracked "rock potential"), matched or beat it everywhere on held-out events, and is much simpler to read and to extend. The retired approaches are in Appendix A.

The idea came from a question about the setup: not all rocks in play are equal. A rock in front of the tee gets better when it is bumped and guards the others; a rock behind the tee is poor even when it is shot, because it backs up the opponent; guards do not count but are worth a great deal to a team that needs a steal. Rock potential (Appendix A.3) was the first attempt to measure that, from where each rock ended up. Traits measure it from where the rock is.

### 4.2 Count function

Sort all stones by distance from the pin; a stone is in the house if that distance is at most 72 inches plus the stone radius (5.7 in). The team owning the closest in-house stone scores the number of its in-house stones closer than the nearest in-house opposing stone; an empty house is a blank. Exact, not a judgment; used for terminal positions and as the reconstruction gate.

**Near-tie positions.** Stones within about two inches at the ownership boundary are tied on the sheet and unresolvable in the data; these are the ends where reconstruction disagrees with the recorded score. They are a real game state rather than noise: the skip cannot tell which rock is second either, and the call made there (peel, freeze, play for the measure, draw for the sure one) is a strategic response to that uncertainty. The outcome distribution stays a full distribution rather than collapsing on the count, the count function is never ground truth for those ends, and the model carries the margin at the ownership boundary and a near-tie flag.

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

A single centre guard at the start of an end is `front`, `controls_4ft` and `open`, and nothing else. A rock's whole vector is its **type**; across the corpus there are about 1,100 types with 1 to 5 stones thrown, rising to about 2,100 late in the end, and 89% of rocks fall in types seen 500 times or more. The vocabulary was written by Mike Calcagno, the tests and thresholds are the obvious ones, and all of them are open to change: the point of the study that follows is that the corpus says which traits matter.

Three traits pair up often enough to read together (Jaccard overlap above 0.5): the nested rings, the twelve-foot with above the tee, and the guard zone with open.

### 4.4 What traits have been worth

`pointsgained traits` (`reports/traits.md`, with a Tier 1 version) takes every position after stones 1 to 15, 558,694 of them from 37,623 ends, reads each rock's traits, and sets beside them the end's result for the hammer team: the mean points, and the share of steals, blanks, singles and two or more. Each end appears once per stone number, so the positions after a given stone are independent; results are read against positions after the same stone in the same game situation (discipline, score difference to ±2, two or fewer ends left) so that a trait that turns up when a team is ahead is not credited with the lead, and intervals are clustered by end. Across the corpus the hammer team scores 0.79 points per end: a steal 21%, a blank 13%, a single 34%, two or more 32%.

One trait at a time, the positions where a team has at least one rock with it against the rest:

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

The table reads as skips would expect, with some sharpness they might not: a non-hammer rock frozen onto its own is the strongest steal trait in the vocabulary, and a hammer rock on the wing late in the end is worth nearly as much as a counter, because a wing rock is a second counter waiting for the draw to the centre (the asymmetry skips describe, Section 14.4). Some rows are the situation leaking through: the hammer team's rock controlling the four-foot late in the end goes with more steals (+6.3), because a hammer centre guard that late is usually a catch-up call or a missed come-around.

**One rock in play.** Positions with a single rock, by its team and type, are the cleanest reading of what a rock is worth. After the first stone of an end the non-hammer team's rock is almost always a centre guard or a draw into the four-foot:

| After stone 1, non-hammer rock | Ends | Hammer points | Two or more | Steal |
|---|---|---|---|---|
| Centre guard (front, controls the 4-foot, open) | 18,267 | 0.88 | 34% | 21% |
| Four-foot, in front of the tee | 8,905 | 0.62 | 28% | 22% |
| Four-foot, behind the tee | 2,749 | 0.68 | 29% | 20% |
| Eight-foot, behind the tee | 758 | 0.85 | 33% | 17% |
| Twelve-foot, behind the tee | 340 | 0.86 | 31% | 18% |

The raw gap between the guard and the draw is mostly the score (the non-hammer team draws when it is ahead and the hammer team is chasing); within the same situation the two are within 0.06 of each other. The depth of the draw is not: the deeper behind the tee it comes to rest, the better for the hammer team, the counting study of the non-hammer first stone in another form.

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

Early in the end the same rocks are graded very differently: a hammer rock of any kind is worth +0.29 in the first five stones and +0.01 late, because early it is a rock the hammer team has kept in play in the free guard zone, and late a guard is just a guard.

The grades agree with rock potential, the earlier tracked measure (Appendix A.3), without following any rock anywhere: across the corpus each team's summed grade correlates with its potential at 0.60 to 0.78 (Spearman) at every stage.

**The rock ledger.** After every stone the house is re-read and re-graded. A stone's **build** is the rise in its own team's grade, its **address** the fall in the other team's, and the end's **temperature** is both teams' grades together. The position before and after a stone are graded with the weights of that stone's stage, so a stone is never credited with the stage changing under it. That is the whole of the accounting: an added rock enters with its grade, a removed rock leaves with its grade, a moved rock is graded where it now sits, and a rock that did not move can still change grade because its traits changed (it lost shot rock, or a guard now covers it). The ledger is printed in the game reports and summarised per team in the event reports as a build-or-address table (Section 11). It describes the rocks; the model's values are the model's.

### 4.6 The rocks that matter

Counts of traits per team say how many of a team's rocks are open, and separately how many are shot rock; they cannot say whether *the shot rock* is open, which is the first thing a skip asks. The model therefore also takes five rocks whole, each with its owner and its traits as they are in this position: the shot rock, second shot and third shot (either team's), and each team's guard nearest the pin (`model/slot_features.py`). Late in an end these are most of the rocks in play, and the last few stones are close to a lookup on them: in chess terms, the endgame is calculation over a few pieces, and the slots are the key. Adding them cut the log-loss at the last rock more than anything else tried (Section 7.6).

### 4.7 Relations

The last stones of an end are about a few geometric relations between rocks, which a sum of rocks cannot see. Three are computed for the team about to throw.

**The draw to beat** (`core/draw.py`). "Draw against n": the other team lies n, and a draw that finishes closer to the pin than its best rock turns that into a count for the thrower. The features are the distance of the rock to beat, how many the other team lies, what a made draw would leave the thrower lying, whether the path is open, and whether there is backing. The path follows Mike Calcagno's description of how the draw is actually played:

- The final draw comes on an in-turn or an out-turn, curling in from one side or the other. Any rock along that curved path blocks it: rocks on the wing on the side it curls in from, and rocks tighter to the four-foot lane the nearer it gets to the house. A straight-line centre guard does not block it. Often one side is closed and the other open.
- The path is the curve of a stone that decelerates uniformly while curling with a constant sideways acceleration: with u the distance still to travel and U the length of the curl, the stone is D(2r − r²) to the side of where it finishes, r = √(u/U), with D about four feet. The approach comes in at an angle and the path is widest far up the sheet. A rock blocks it when its centre is within a stone's diameter of the path where the path passes it.
- The finishing points are the spots in the four-foot inside the rock to beat that no rock occupies, plus a freeze onto the front of every rock in the house. A side is open when at least half of them can be reached from it.
- The draw is close to a sure thing, high 90s at this level, with **backing**: the rock to beat is behind the tee, so a draw onto it outcounts it, or another rock sits just behind a finishing point and will stop a heavy draw.

On the hammer team's last rock, with the other team lying two, the hammer team scored 51% of the time with both sides closed, 68% with one open and 75% with both; lying one, backing added 10 to 18 points. Where both sides are open and the rock to beat is out in the eight or twelve, the hammer team usually does not draw at all: it hits and rolls out for the blank (61% of those ends), because doubling out two or more to blank is much harder than removing one. With no side open, the usual shot is the hit and stick.

**Doubles and runbacks** (`core/combos.py`). Doubles and runbacks are truly positional: geometric configurations that unlock a bigger result than playing against a single rock. A double that is not there does not get called, and the skip plays something else; a runback gets called for its upside and is weighed against its downside. The aftermath of either, made or missed, is valued by re-reading the house, so the features describe only availability and stakes:

- **Double**: two of the other team's rocks, the first hittable (nothing within half a stone of its line in front), the second behind it, the pair not flat (at least 15° from level, the threshold at which the field's double rate collapses, Section 13.1) and within eight feet; whether both are in the house, the pair's separation and stagger, and the count swing if both go.
- **Runback**: a hittable rock of either colour within 35° and fifteen feet in front of the other team's best rock; straight (under 10°) or angled, its distance, whether the front rock is the thrower's own, and the swing if the target goes.

**The tap (a candidate).** The same shape describes a shot not yet built in: the tap, a stone thrown to move one of the thrower's own rocks to a better place, the shooter usually staying around, and the double tap (red onto yellow onto red, or red onto red onto red). The long tap is a very hard shot: at an elite skills competition of doubles, hit and rolls and taps, almost no elite skip was good at the tap. Before building it, the make rate by distance should be read from the Raise calls in the corpus: if the field rarely makes a long tap, its availability should add little to a position, which would itself be worth knowing.

### 4.8 The configuration vocabulary

Before rock traits, positions were read by configurations: deterministic, multi-label tests on the whole position in the terms a skip uses (`core/configurations.py`). They are no longer a model input, but they remain the vocabulary the studies select positions in and the mispricing report reads the model against (Section 7.7 and Part IV), and some of their thresholds (the flat split, the runback angles) are now the thresholds of the relations above.

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

Part III is the framework: a model of what a position and a call have been worth under the field's play, read rock by rock (Part II), and a value for every stone as the change it made. The studies in Part IV use it to put a number on a position, a shot or a phase of the end, and the player and team reports are built from it. Its models, targets and gates are all open to improvement; the open questions in Section 18 are the current list. Worked examples quote the adopted model; `reports/samples/` carries the current values.

## 5. Goal

Assign every shot a value, **Points Gained (PG)**, that measures how much it changed the expected scoring of the end, from the throwing team's point of view. The name is chosen by analogy with strokes gained in golf: it is measured against the field, it is additive, and it decomposes. Two properties are required:

1. **Situation-aware.** A made draw against an opponent stone in the four-foot is worth more than the same draw into an empty house, because the expectation before the shot was lower.
2. **Conserved.** The values of all shots in an end sum to the final score minus the expected score at the start of the end. No credit is created or lost.

The output is a per-shot Points Gained, decomposable into **PG: Call** (selection: what the call was worth) and **PG: Throw** (execution: what the throw delivered against the call).

### 5.1 Philosophy

Every shot in curling has two parts. First a call is made, by the skip and often with the whole team, and the call sets up a menu of possible outcomes with their odds: the roll-out that blanks, the stick that scores one, the miss that gives up a point, the flash that gives up two. Then the shot is thrown, swept and called on line, and one outcome from that menu happens. The call is a decision; the throw is an event, and what can be judged is its effect against the menu the call created.

The model evaluates every rock in both dimensions. Selection asks what the call's menu was worth compared with the position the team was handed. Execution asks what the throw produced compared with the menu the throw was handed. Neither is judged by the other: the execution value does not penalise a poor call or reward a brilliant one, and the selection value does not credit a lucky throw or blame a bad one. A call reads the same on a make and on a miss. The two components sum to the shot's total contribution to the end.

The best calls create menus whose expectation, weighted by how *this* team executes, is highest relative to the position. That is not always the menu with the biggest upside, and the right trade-off depends on who is throwing. The clearest example in the data is Brad Jacobs' last rock in the ninth end of the 2026 Olympic final: down one with hammer, he called a runback through traffic that scored three and decided the gold medal. Against the field's usual call from that position, a draw, the first model, which knew only the shot type, priced the call at −16.7 percentage points of win probability and the throw at +31.9; with the struck stone as part of the call (Section 7.3) and the position read rock by rock it is −3.4 and +18.1. That is not a verdict that the call was wrong. It says the field does not call that shot, because for the median skip it is a poor menu; whether it was the right menu for Jacobs is a question about geometry (was the shot there?) and about level of play (how often does he make it?), and answering it properly is what the relations of Section 4.7, the level of play (Section 7.4) and Phase 2 (Section 12) are for.

### 5.2 Strategy: how game situation enters

Within an end the structure is recursive. Every shot before the last one builds a **position**, every position carries an **outcome distribution** (the chances of blanking, scoring one, scoring two, giving up one, and so on), and the last rock realises one outcome from it. The rock before the last is thrown to make that distribution as bad as possible for the thrower of the last rock; the rock before that, to make it as good as possible two rocks down the line; and so on back to the first stone. The two teams are pulling on the same quantity in opposite directions, which is exact rather than approximate: whatever currency an outcome is valued in, the opponent's value is the negation.

Strategy is the observation that not all outcome distributions are equally useful, and which ones are useful depends on the game. Curlers have a vocabulary for this: *must steal*, *force one*, *two or blank*, *don't give up more than two*, *score or go to the extra end*. In this model those goals are not a separate layer and are not enumerated by hand. They are the *shape* of the value mapping v(outcome | game situation): tied in the last end with hammer, one and two are both worth a win, a blank is worth the chance of winning an extra end with hammer, and a steal is worth nothing, and maximising expected value under that shape simply *is* "score or don't get stolen on." The win-probability table (Section 10.3) generates every one of the named strategies as a consequence.

The two currencies disagree in a way that is itself informative. In hammer-adjusted points, a team protecting a three-point lead reads as calling badly, because points reward aggression whatever the game; in win probability the same calls are neutral. On the four development books, the strongest teams' call values were slightly negative in points and zero in win probability for exactly this reason: they are ahead more often. Rachel Homan's raise with her last rock in the eighth end against Italy at the 2026 Olympics, up two with three ends to play, costs 0.15 points but only 0.8 percentage points of win probability; the game barely depended on that end. Both currencies are kept, and reports say which one they are in.

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
| **Event-relative execution** | PG: Throw minus the event field's mean for the same call and hammer state; the reporting unit for players. |
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

Execution measures how the result compares with what that call usually produces; selection measures what the call was worth relative to the position, under the field baseline: D(S) is the outcome distribution under the observed shot-selection policy of the field, so selection reads as "better or worse than the field would call." The best-call baseline of Phase 2 replaces D(S) with the best available menu and reads as regret.

Two of Homan's shots at the 2026 Olympics show the split doing its job. In the fifth end against Sweden, up two without hammer with six ends left, she called a double with the fifteenth rock and missed; Sweden scored three. The call is worth −0.11 points and −1.4 percentage points of win probability against the field's usual call from there, and the throw −1.10 points. In the seventh end against Switzerland, up three with four to play, she called a take-out and missed; Switzerland scored four. That call is worth +0.03, at or above the field's points, and the throw −0.72: the whole cost is execution. Same player, same week, same-sized disasters, different diagnoses.

### 6.4 Perspective convention

Every physical position is evaluated **once**, from a canonical perspective: the team holding hammer in the current end. Stones are labelled `hammer` / `non_hammer`, and f is fitted and evaluated only in this frame. A thrower's value is V from the canonical frame, multiplied by +1 if the thrower holds hammer and −1 otherwise.

This is deliberate rather than cosmetic. If f were evaluated from the thrower's perspective, the same physical position would be evaluated twice, once for the team that just threw and once for the team about to throw, and a learned model is not exactly antisymmetric under the swap, so the sum of Points Gained over an end would not telescope. With a single canonical evaluation per position the identity in Section 6.5 holds by construction. Who throws next is determined by the parity of rocks remaining.

### 6.5 Conservation check

With D(final position) defined as the actual score, summing canonical Points Gained over the shots of an end gives

    Σ PG = actual_score − V(D(S₀))

where S₀ is the empty-sheet position at the start of the end. On the full archive the largest residual is 6 × 10⁻¹⁶ over 37,585 ends. It is a unit test, not a diagnostic: a rebuilt post position (where a diagram is missing) must carry every input the training rows carry, and a bug there once broke the identity by 0.076 in one end.

## 7. The expectation model

### 7.1 Insight

Every shot's pre-position is labelled with the end's final outcome. Sparsity of exact positions does not matter once the model can generalise across positions. The outcomes are high-variance per example, but that variance is what the model averages over. This is a supervised problem, not a dynamic-programming problem, and it is deliberately outcomes-biased: it says what positions and calls have been worth given how the field has played, not what they should be worth under optimal play.

### 7.2 What f and g read

- **f(S) → D**: distribution over end outcomes from the position, in the canonical frame. This is D(S) under the field baseline.
- **g(S, C) → D**: the same with the called shot. This is D(S | C).

Both are gradient-boosted tree classifiers over seven outcome classes (`model/train.py`). Their inputs are named sets, so an experiment can toggle them; the adopted model uses all of these:

| Set | What it is | Columns |
|---|---|---|
| `core` | Rocks remaining (whose parity says who throws next), the free-guard-zone rule, stones in play, the count, discipline | 6 |
| `situation` | The hammer team's score difference (±6), ends remaining (≤10), an extra-end flag | 3 |
| `traits` | Each team's number of rocks with each trait (Section 4.3) | 34 |
| `grades` | Each team's summed rock grade and their sum (Section 4.5), cross-fitted so that a held-out book is graded by weights fitted without it | 3 |
| `margin`, `shotdist` | The count's margins at the ownership boundary and a near-tie flag; each team's nearest stone to the pin | 5 |
| `slots` | The shot rock, second and third shot and each team's nearest guard, each whole (Section 4.6) | 50 |
| `draw` | The draw to beat for the thrower (Section 4.7) | 7 |
| `combo` | Doubles and runbacks for the thrower (Section 4.7) | 11 |
| `call` (g) | The shot type as recorded and the turn | 2 |
| `level` (g) | The event's strength rating (Section 7.4) | 1 |
| `intent` (g) | The target of the call: the struck stone for hits, the field's modal target for draws (Section 7.3) | 6 |

Situation in f changes what D(S) means, from "what this position is worth under typical play" to "what it is worth given how teams play from here in this situation": up three in the ninth, the field runs the end clean, and f expects that rather than scoring the blank as a failure. The value mapping still carries the situation in the win-probability currency (Section 10.3); the two uses are complementary, and the conservation identity is unaffected because V is fixed within an end.

**Regularisation.** On four books, about 2,900 labelled ends, the trees had to be held to eight leaves, 300 samples per leaf and 60 to 80 boosting rounds to beat the trivial model (rocks remaining, hammer, count) on held-out books. On the archive the plateau is 15 leaves and 200 rounds; 31 leaves and 300 rounds score the same at twenty-five times the cost, and 63 leaves are worse. Points Gained are always computed from out-of-fold predictions, so no position is valued by a model that saw its book.

### 7.3 Called shot and intent

The `type` field records the call: Draw, Take-out, Hit and Roll, Guard, Front, Freeze, Raise, Clearing, Double Take-out, Promotion Take-out, Wick / Soft Peeling, Through. The type leaves the target ambiguous, so g also takes the target, with one rule that matters more than the rest: **the call must never be read from the outcome.** On a made draw the delivered stone's rest is the target; on a missed draw it is the miss, and on the last rock it is the score. A first attempt that used the rest for every draw cut g's log-loss sharply at the last rock, almost all of it execution leaking into the call.

What g takes instead:

- **Draws** (Draw, Guard, Front, Freeze, Through): the *modal* target from a target model P(target cell | position, call), fitted on made draws with a marker and applied to every draw whatever its grade. The cells are three lanes by six depth bands. Because it is a function of position and call only, it cannot leak.
- **Hits** (Take-out, Hit and Roll, Double, Clearing, Raise, Promotion, Wick): the **struck stone**, from the prior-position ring furthest up the sheet (the shooter arrives from the hog line), at any grade: which stone was hit is intent, not outcome. Without rings, the modal struck-stone class from a second target model.

The information is in the hits: with the struck stone, the call component's mean size per shot is about half the execution component's rather than a tenth, and largest on take-outs, doubles, raises and promotions.

### 7.4 Level of play

A six-foot double is worth less to an elite team than to a club team because the elite team makes it more often: D(S | C) is higher, so PG: Throw for making it is smaller. Level of play is a property of the **execution distribution** and enters through g, as the **event's strength rating** (`data/event_strength.csv`, men's Worlds = 100), a handful of distinct values that cannot identify a book. Level of play belongs to the field, never to the player being measured: strokes gained does not evaluate a fairway shot against Tiger Woods' putting, it evaluates it against a tour professional's. A per-player skill input was built and withdrawn (Appendix A.6); the shot-difficulty model behind it remains as a report (`pointsgained difficulty`: skill leaderboards, event effects, field strengths beside the ratings).

### 7.5 Training target

Labelling every position with the end's final score is unbiased but noisy early in an end, where ten or more stones remain between the position and the label, and it made early execution see-saw: a mispriced position credited the stone that created it and charged the stone that followed (Section 14.1). The adopted target (`model/targets.py`, `local:2`) trains rows with nine or more rocks remaining on the value of the position two stones later, as a soft label: the out-of-fold f distribution there, from a first-stage f fitted on final labels within the training books, or the end's result if the end finishes first. The soft targets are rebuilt inside each cross-validation fold from that fold's training books only.

### 7.6 Results

**The ladder** (held-out 2025–26 events, trained on everything through 2024, local target; log-loss, lower is better). Each row adds to the one above unless it says otherwise; the reference is the hand-built model it replaced (Appendix A):

| Model | f | g | Last rock (f) | 12+ rocks left (f) |
|---|---|---|---|---|
| Trivial (rocks remaining, hammer, count, situation) | 1.5484 | | 1.2295 | |
| Hand-built: base features, configurations, rock potential | 1.4521 | 1.4299 | 0.9046 | 1.6065 |
| Rock traits only (no base, configurations or potential) | 1.4532 | 1.4307 | 0.9156 | 1.6068 |
| + rock grades | 1.4525 | 1.4306 | 0.9182 | 1.6056 |
| + the count's margins and each team's nearest stone | 1.4524 | 1.4305 | 0.9117 | 1.6060 |
| + the draw to beat | 1.4516 | 1.4302 | 0.9120 | 1.6060 |
| + the rocks that matter (slots) | 1.4499 | 1.4300 | 0.9028 | 1.6059 |
| + doubles and runbacks (**adopted**) | **1.4497** | **1.4299** | **0.9019** | **1.6060** |

Rock traits alone came within 0.001 of the hand-built stack; the relations and the slots then carried the model past it, and the slots did most of the work at the last rock. On a held-out fold of books from every year the adopted model is better again (f 1.4555 against 1.4571, g 1.4349 against 1.4353). f is better, or within 0.0005, at every number of rocks remaining on both splits. g is level overall and slightly behind at the last rock (0.007 on the time split, 0.004 by book): the one place the old stack still knew something extra, recorded as an open question.

**The full cross-validation** (five folds by book over the whole corpus, as `pointsgained model` runs it): f 1.4660 and g 1.4447 against a trivial 1.5595 (the hand-built model: 1.4665 and 1.4450), Brier 0.706 and 0.697. With one rock left f is at 0.923 against 1.229 for the trivial model; with twelve left, 1.598 against 1.633. Conservation holds to 6 × 10⁻¹⁶ in every end, and the value of the empty sheet with hammer is 0.586 against H = 0.582.

**Credit.** Accuracy was not the only test. Held out by book:

| | Hand-built | Adopted |
|---|---|---|
| Setup battle vs win rate, within the same score and ends left | 0.025 | **0.21** |
| Calibration slope with 12 or more rocks left (1 is right) | 0.918 | **0.954** |
| The lead's first rock, back 8–12 ft against front 4-foot: model gap (real 0.086) | 0.042 | **0.065** |
| Seconds' execution against their grades | 0.30 | **0.44** |
| Leads' execution repeatability (split-half) | 0.59 | 0.63 |
| Seconds' execution repeatability (split-half) | **0.47** | 0.41 |

The first row is the result this work was for. The setup battle (Section 14.3) is the change in value over the free guard zone; every earlier model valued it as a repeatable team trait that, within the same score, said nothing about winning. Read rock by rock, the setup a team builds relates to how often it wins (0.21 by book, 0.18 to 0.20 on the time split). The early values are also less flat, and the lead's draw behind the tee, which the field has always valued more than the model did, is priced closer to what it is worth. Seconds' repeatability fell; it is the one credit measure that went the wrong way.

### 7.7 Validation

- Held-out log-loss and Brier score against the trivial model, overall and by rocks remaining; calibration by outcome class.
- Conservation to numerical precision (Section 6.5).
- Calibration at the empty sheet: V(f(S₀)) with hammer should equal H.
- The front-end gates (`reports/experiments/frontend_gates.md`): the see-saw, agreement with grades, repeatability, the setup battle, calibration slopes by stage.
- **Where the model misprices** (`pointsgained misprice`, from an experiment's saved held-out predictions): the model's value against the realised result by stage, by stones in play, by configuration label and stage, and the last-rock beam probe, the hammer team's last stone by the count and where the shot rock sits. On a time split the held-out years can score differently from the training years (hammer teams scored 0.80 and 0.85 per end in 2025 and 2026 against about 0.75 before), so the report is read net of each model's overall gap. Two last-rock cells that looked under-priced by about 0.2 on the time split (the other team lying two or three with its best rock only in the eight or twelve) disappear by book: they were 2025–26, not a missing relation.
- **Acceptance cases** (Section 14.4): the split house restored flat, staggered or not split, and the peel when the hammer team must score.

## 8. An end, rock by rock

The tenth end of the 2026 Olympic men's final shows the whole system at work. Great Britain has hammer, is two down and has one end to play: it needs two to force an extra end, and Canada needs to hold it to one or steal. Canada starts the end at 84.6% to win. Every row below is one stone: the call, the book's grade, what the thrown rock is when it comes to rest (its traits, read in the position after the stone), each team's rock grade after the stone (the sum of its rocks' grades, from its own side), the stone's **build** (its own team's grade up) and **address** (the other team's grade down), Canada's chance of winning after the stone, and the stone's execution value (PGAA, points gained above average, the model's PG: Throw in hammer-adjusted points from the thrower's side). The report `reports/samples/games/..._Gold_Medal_Game_CAN-GBR.md` has the same end with the model's values in full.

|   stone | team   | player     | call            |   grade % | thrown rock                                                            |   rocks GBR |   rocks CAN |   build |   address |   CAN win % after |   PGAA |
|--------:|:-------|:-----------|:----------------|----------:|:-----------------------------------------------------------------------|------------:|------------:|--------:|----------:|------------------:|-------:|
|       1 | CAN    | Hebert B   | Draw            |       100 | 4-ft, high, shot, open                                                 |        0.00 |        0.09 |    0.09 |      0.00 |             85.10 |   0.03 |
|       2 | GBR    | McMillan H | Front           |       100 | guard zone, controls 4-ft, guarding, open                              |        0.23 |        0.22 |    0.23 |     -0.13 |             83.60 |  -0.01 |
|       3 | CAN    | Hebert B   | Draw            |       100 | 4-ft, high, guarding, second, frozen (own), behind cover               |        0.23 |        0.43 |    0.21 |      0.00 |             88.20 |   0.19 |
|       4 | GBR    | McMillan H | Front           |       100 | guard zone, open                                                       |        0.52 |        0.38 |    0.29 |      0.05 |             86.50 |  -0.01 |
|       5 | CAN    | Gallant B  | Draw            |       100 | 8-ft, high, controls 4-ft, guarding, third, frozen (own), behind cover |        0.52 |        0.61 |    0.23 |      0.00 |             88.90 |   0.06 |
|       6 | GBR    | Lammie B   | Raise           |       100 | 8-ft, high, controls 4-ft, guarding, partly open                       |        0.47 |        0.82 |    0.29 |      0.05 |             92.40 |  -0.27 |
|       7 | CAN    | Gallant B  | Clearing        |       100 | removed from play                                                      |        0.37 |        0.82 |    0.00 |      0.10 |             92.10 |   0.09 |
|       8 | GBR    | Lammie B   | Draw            |        75 | 4-ft, high, guarding, frozen (opp), behind cover                       |        0.78 |        0.82 |    0.42 |      0.00 |             86.80 |   0.20 |
|       9 | CAN    | Kennedy M  | Clearing        |       100 | removed from play                                                      |        0.64 |        0.82 |    0.00 |      0.14 |             88.20 |   0.04 |
|      10 | GBR    | Hardie G   | Draw            |       100 | 4-ft, back, behind cover                                               |        0.84 |        0.86 |    0.21 |     -0.04 |             87.60 |  -0.07 |
|      11 | CAN    | Kennedy M  | Raise           |        75 | 8-ft, high, controls 4-ft, guarding, open                              |        0.84 |        1.69 |    0.28 |     -0.04 |             90.90 |   0.42 |
|      12 | GBR    | Hardie G   | Raise           |        75 | 8-ft, high, wing, open                                                 |        1.25 |        1.21 |    0.41 |      0.49 |             90.00 |   0.01 |
|      13 | CAN    | Jacobs B   | Double Take-out |       100 | 8-ft, high, wing, second, open                                         |        0.51 |        0.66 |   -0.55 |      0.74 |             89.70 |  -0.08 |
|      14 | GBR    | Mouat B    | Double Take-out |       100 | 4-ft, high, shot, partly open                                          |        2.01 |        0.29 |    1.50 |      0.37 |             70.20 |   0.78 |
|      15 | CAN    | Jacobs B   | Double Take-out |       100 | 12-ft, high, controls 4-ft, guarding, second, frozen (own), open       |        0.37 |        0.56 |    0.27 |      1.64 |             96.40 |   1.18 |
|      16 | GBR    | Mouat B    | Double Take-out |         0 | 12-ft, high, wing, third, open                                         |        1.33 |        0.34 |    0.96 |      0.21 |            100.00 |  -0.50 |

**The setup (stones 1–5).** Hebert draws to the top of the four-foot: four-foot, in front of the tee, shot, open, a rock worth 0.09 to Canada at that stage. McMillan's centre guard is the hammer team's standard answer when it needs two: `guard zone, controls 4-ft, guarding, open`. Its build is +0.23, but its address is −0.13: the guard also puts Canada's shot rock behind cover, and a rock behind cover is graded higher whoever put the cover there. The model agrees that the guard helped Great Britain (Canada 85.1 → 83.6%) but barely; it is the stone the field throws here. Hebert then comes around and freezes to Canada's shot rock (`4-ft, high, guarding, second, frozen (own), behind cover`): build +0.21, Canada 88.2%, and the largest execution value of the setup (+0.19). A frozen non-hammer rock behind cover is exactly the trait the study found most dangerous to the hammer team (Section 4.4). Gallant adds a third, frozen again.

**The middle (stones 6–12).** The re-read after every stone shows what each shot did to the rocks already there. Lammie's raise (stone 6) puts a British rock in the eight-foot, partly open, but leaves Canada's buried rocks untouched and still behind cover: build +0.29 and Canada's grade up, the model's verdict −0.27 and Canada to 92.4%. Canada spends two stones clearing the guards (Gallant, Kennedy): they build nothing and address +0.10 and +0.14, the price of opening the house. Lammie's draw (stone 8, graded 75) comes to rest frozen onto a Canadian rock, behind cover: +0.42 of build and +0.20 of execution, Canada down to 86.8%. Where the grades jump between rows 10 and 11, the stage of the end has changed (stones 6–10 to 11–15 are graded with different weights); a stone's own build and address are always read with a single stage's weights, so no stone is credited with the change.

**The end game (stones 13–16).** This is where the relations and the rocks that matter take over, and where the ledger and the model part company. Jacobs' double (stone 13) removes two British rocks (address +0.74) but leaves his own rocks open and off the button (build −0.55): the rocks moved a lot and the chance of winning did not (89.7%), because the model reads what the position leaves Mouat. Mouat's double (stone 14) is the best British stone of the end: Britain lies shot in the four-foot with more behind it (grade 2.01), and Canada falls to 70.2%, +0.78 of execution. Jacobs answers with the stone of the game: a double that takes out Britain's counters and leaves Canada second and frozen at the top of the twelve (address +1.64, execution +1.18, Canada 70.2 → 96.4%). Mouat's last stone, a double graded 0, misses: Canada steals one and wins.

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

Building the player reports taught several things about what a shot value should be aggregated into.

**Execution relative to the field.** Raw PG: Throw averages positive, about 0.05 points per shot, because every throw is an opportunity to improve one's own position; and fourths carry most of the leverage. Players are therefore reported as execution minus the field's mean for the same shot type and hammer state, either the whole corpus or that event's field. A second baseline, the same shot number and hammer state, puts leads and fourths on one footing; the shot-type baseline reads more naturally position against position, which is how curling people compare players, and is the default.

**Median, mean and the tail.** The per-shot distribution is heavily skewed, and the skew is where the metric earns its keep. The 2022 Olympic men's tournament makes the point. Among the fourths, John Shuster's median shot (+0.021) was mid-pack, but his mean was −0.026: his five worst shots cost 8.3 points, twenty-one shots cost more than half a point each, and the list of them is the list of last rocks stolen for two and four. Joël Retornaz is the mirror image, one of the two lowest official percentages (79%) and the lowest median in the group (+0.001) but a positive mean (+0.020), because fifteen of his shots earned more than half a point: a high-variance skip whose misses were cheap and whose makes were expensive. The official percentage, which counts every shot once, cannot see either pattern. Reports therefore carry the mean, the median, the counts of shots beyond half a point either way, and the sum of the five costliest shots.

**Outcome first.** Execution, PG: Throw, is the primary pivot in both currencies. It is the part of the shot's value that does not depend on reading the skip's mind, and it credits what curlers credit: the position left, whatever the scorer wrote down. A hit that ticks a guard through a port and improves the position is a miss on the sheet and a gain here; a skip who calls plan B while the rock is moving gets the position that plan B produced. The tail columns below are reported in points and again in win probability (`floor10_wp`, `big_misses_wp` counting shots that cost five or more points of win probability, `worst5_wp`), because a costly miss in a decided game and one in a tied last end are different events. The call component is reported after execution, and its fairness to an elite skip is a secondary concern (Section 7.3).

**Consistency.** Variance is mostly the leverage of the position, not the person, and a symmetric spread treats the gambler and the choker alike. Two positive-is-good numbers are reported instead: the **floor**, the tenth percentile of event-relative execution ("on a bad day this cost this much"), and **reliability**, the share of shots at or above the field's expectation for that shot type and hammer state. A leverage-free version, execution divided by the width of the call's menu, is a next step.

**The distribution, not its average (2026-09-14).** The leaderboards now sort on reliability and show the distribution split: the average make, the average miss, the big-make and big-miss counts and the worst five, with the mean kept as `net`; the median and the floor are retired from the tables (still in the combined CSV). Over 95 fourth-at-event rows from the six major books (OWG2022, OWG2026, WMCC2025/2026, WWCC2025/2026) the mean correlates with the team's win rate at 0.78 (Spearman), reliability at 0.69 and the median at 0.64, and reliability and the median carry the same information (0.95 between them). The split shows why the mean ranks best and what it hides: the size of the average make is unrelated to winning (0.01) and barely varies across fourths (+0.24 to +0.28 for the middle half), while the size of the average miss is (0.59 overall, 0.70 within the top two terciles by reliability). The two shapes a median cannot distinguish are both in the data: Jacobs and Mouat at Milano Cortina 2026 sit on nearly the same reliability (67 and 65 percent) with average misses of −0.22 and −0.29 and win rates of 82 and 55 percent. Fourths only so far; for the front end the misses are small in points and the split may separate players less.

**The Beijing final.** Those columns for the two 2022 Olympic finalists:

| | shots | median | mean | floor | reliability | big misses | grade |
|---|---|---|---|---|---|---|---|
| Edin | 213 | 0.053 | 0.034 | −0.331 | 61.5% | 12 | 84.1 |
| Mouat | 206 | 0.047 | 0.047 | −0.302 | 59.7% | 9 | 89.0 |

They split the columns: Edin is the more reliable, with the higher median; Mouat has the better mean, the better floor and three fewer big misses. Sweden won the final 5–4 in an extra end. The model's read of the tournament is the field's two best fourths, first and second on reliability (Mouat level with Gushue), playing to a draw.

**Homan across the cycle.** Rachel Homan's three tier-1 events show the arc a skip can have:

| Event | median | mean | floor | reliability | big misses | big makes | grade |
|---|---|---|---|---|---|---|---|
| Worlds 2024 | 0.078 | 0.123 | −0.218 | 64.4% | 8 | 29 | 88.5 |
| Worlds 2025 | 0.066 | 0.105 | −0.317 | 62.7% | 10 | 27 | 87.6 |
| Olympics 2026 | 0.040 | 0.045 | −0.414 | 56.3% | 18 | 17 | 77.7 |

Worlds 2024 is the most dominant single-event line in the cycle: first among thirteen fourths on the mean, the median, the floor and the big-miss count, and second on reliability by less than a point (Constantini 65.2%, Homan 64.4%). Olympics 2026 is second by median and fourth by floor among ten fourths, with a tail the size of Shuster's in 2022. Her typical shot barely changed; the floor fell. Her eight costliest shots that week were four late stones without hammer after which the opponent scored three or four, a raise after which China scored two, the semi-final runback that became a steal, and two hammer draws, one stolen and one held to a single.

### 11.3 Reports produced

- **Model report:** corpus counts, the hammer distribution, N and H by discipline, held-out log-loss by model and by rocks remaining, conservation and calibration, win-probability examples; then the whole-corpus performance tables under the currency rule (teams by record and win probability gained per game; players per position by the execution block with big makes and misses per 100 shots; execution by shot type) and the stratified model checks. `pointsgained model-report` rewrites it from the saved run summary without refitting.
- **Strata:** by discipline and tier, by hammer, by game state and hammer, by shot type and hammer, players relative to the field, teams by hammer; all in both currencies.
- **Per-event leaderboards** (`pointsgained events`): one row per player and event with position, shots, games and the execution block relative to the event's field: reliability, average make, average miss, big makes and misses, worst five, and the mean as `net`; then the effect on win probability for reference (big makes and misses, best and worst five), the call value and the official grade. Sorted by reliability, then average miss. The CSV also carries the median, floor, variability and slot-relative execution. The team table above the position groups is the team-level view: record and the summed effect of the team's own stones on its chance of winning per game, with no execution columns (the currency rule: teams in win probability, individuals by execution); beside it a build-or-address table per team from the rock ledger, relative to the field at the same stage of the end.
- **Game report** (`pointsgained game`): one game from the per-shot table. The currency follows the level of the table: team-level tables are in win probability, the currency that knows which end it is (Section 10.3); individual tables lead with execution in hammer-adjusted points, the leaderboard measure, with the effect on win probability beside it. So: an end table with the running score, one team's win probability before and after the end and the swing, and nothing else; a players table with each player's PGAA (points gained above average, `pg_throw` in the tables) summed over the game, their worst and best stones, the grade, and their stones' summed win-probability effect as a reference; the ten largest swings; and every stone in the order situation, shot, execution (PGAA and call), effect (win probability after and the change). The conservation identity holds in win probability too (one team's changes minus the other's is the end's swing); the report warns only if it fails. Beside every stone it prints the rock ledger (Section 4.5): each team's rock grade after the stone, and the stone's build and address; under each end header, each team's grade after the free guard zone, after stone 12 and before the last stone, and the end's peak temperature. It is the report that lets a leaderboard number be traced to the stones that produced it.

Every per-shot value is a difference of model outputs, so these tables are exactly reproducible from the Parquet tables and the fitted models. `reports/samples/` keeps finished copies in the repository (the model report, the test set, the 2026 Olympic and World Championship leaderboards, Beijing 2022, and the two 2026 Olympic finals shot by shot) with a README on how each is built and what it says. One pattern from those samples is recorded here because it bears on Section 7.3: in every event sampled, the teams with the best execution have negative call values and the teams with the worst have positive ones. A first check over 777 team-events (300 or more stones each) says the sign is situation, not judgement. Split each shot's call value into an event mean, a situation component (score, ends remaining, hammer, stone number) and the remainder within the situation: only the situation component correlates with execution (−0.20), and the within-situation call is flat (+0.02). Good teams are scored on less, so they hold hammer less and throw from different situations; within the same situation their calls are valued no differently from anyone else's. Neither reading of the column survives: the best skips are not calling worse, and they are not knowingly taking lower-expectation calls.

**The tail hypothesis.** Where the teams do separate is on the downside of the call. One hypothesis: the best teams call shots whose field distribution D(S | C) has a fat bad tail because they know their own team will not produce it, an instinct for which part of the distribution is safe to ignore, where an average skip weighs the misses. The same first check supports it. Measure a call's downside as the expected shortfall below the pre-shot expectation under D(S | C), and split each situation's stones into downside terciles. The best teams accept slightly more downside than the field in the same situation (+0.13). The execution gap between the best and worst quartile of teams grows with the downside of the call: 0.028, 0.041 and 0.059 points per stone across the terciles, and 0.041, 0.050 and 0.062 after dividing execution by the width of the call's distribution, so it is not the leverage of risky calls doing the work. Top-quartile teams execute risky calls as well as safe ones relative to the field; bottom-quartile teams execute them worse. The same split by the call's mean value discriminates far less (+0.09): it is the tail, not the expectation. The precise form of the hypothesis is then that the bad tail of the field's distribution for a risky call is produced by the weaker teams, and a top skip's estimate of the downside is lower than the field's because their team is the source of little of it.

This has not been validated beyond that one check: one measure of downside, terciles within coarse situation strata, team-events as the unit, and the field defined as the teams at the event. It points at a way to talk about aggressiveness in terms of the shape of the outcome distribution a call accepts, the upside, the downside tail, and which part of it a team produces, rather than in terms of shot types; a report built on it is a next step (Section 18).

---

## 12. Phase 2: Physics, Transitions, and the Best Call

Phase 1 answers "what has this been worth." Phase 2 answers "what could this have been worth," which needs counterfactual calls, and therefore a model of what happens when a shot is thrown.

- **Simulator.** Collision geometry, rolls, raises and runbacks are deterministic physics; the Digital Curling platform and similar simulators implement them. A simulator answers the inch-level questions the raw-geometry model has to learn statistically: is the double on, where does the shooter roll, does the raise reach.
- **Execution error model.** The only stochastic component. Learned from the delivered-stone marker: for each (type, inferred target, skill scalar, event effect), the distribution of where the thrown stone arrived relative to the target. Seeded in the modelling phase: `pointsgained intent` writes the delivered stone's rest relative to the modal target for every draw with a marker, by grade, skill tercile and rocks-remaining band (`reports/execution_error.md`). On late-end draws graded 100% the median lateral error is about 8 in and the depth interquartile range about 27 in, part of which is the target cell's coarseness; at 75% the depth spread is 41 in.
- **Transition model.** P(S′ | S, call) = simulator applied to the call with delivery sampled from the error model. It turns the geometric relations of Section 4.7 (is the draw open, is the double on) into simulated shot-availability probabilities.
- **Rollouts.** From any position, simulate the remainder of the end under a policy, initially the empirical policy P(C | S, situation), evaluating with f at a fixed depth. When the policy is replaced by an optimising one, there is a single objective for both teams, since v is zero-sum, and the named strategies emerge from the shape of v.
- **Best-call baseline.** For each position, evaluate each candidate call by rollout and take the maximum; selection under this baseline is the regret of the call made. The best call is skill-dependent, so it must be evaluated at the thrower's skill scalar. Jacobs' ninth-end runback in the 2026 final is the test: at the field's skill the field baseline calls it a poor menu; at his, it may have been the best shot on the sheet. Elite skips disagree in exactly the positions where it matters, so the best-call baseline is reported with uncertainty and is never the headline number.

---

## Part IV. Sample studies

Each study below is produced by a command in the package, from the corpus tables and the Points Gained table, and each is a template: change the position, the call family or the situation and the same code answers a different question. The samples are in `reports/samples/`.

| Study | Question | What it found | Command | Section |
|---|---|---|---|---|
| The double on a split | How often does the opponent double off two stones, by how far apart and how staggered they are? | Four to six feet apart and level: 2%; staggered 20–35°: 14%. The field calls the double 6% and 32% of the time. | `frontend` | 13.1 |
| The runback | How often does a runback on the shot rock leave the thrower lying shot? | From under four feet 46–71%, from eight to twelve feet 28–39%. Angle shows no penalty: skips call angled ones only when they are on. | `frontend` | 13.2 |
| Rock traits | What have rocks with each trait, held by each team at each stage, been worth? | A non-hammer rock frozen onto its own is the strongest steal trait (+13.5 points late); a hammer rock on the wing late is worth nearly a counter. | `traits` | 4.4 |
| The early end | What do lead and second values measure, and who wins the battle over the setup? | The first model see-sawed between consecutive stones; a nearer training target removed it. Read rock by rock, the setup battle relates to winning within the same score and ends left (0.21 held out by book), where every earlier model found nothing. | `frontend`, `experiment` | 14 |
| The opening | Non-hammer ahead, a draw into the rings, a hammer corner guard: who wins? | The non-hammer team holds the hammer team to one or fewer 69% of the time (9,023 ends). | (analysis in 14.3) | 14.3 |
| Runbacks by player | Are the dominant skips the best at runbacks? | Jacobs first of 60 men; Homan the largest win-probability effect per runback in either field. | `frontend` | 15 |
| Player execution | Who executes best against the field, and how: typical shot, misses, tail? | Reliability and the size of the average miss separate the fourths; the mean tracks win rate best. | `events`, `game`, `model-report` | 11.2 |

## 13. Shot geometry: doubles and runbacks

Two tables that exist only because every stone is on file. Both read the pre-shot geometry from the diagrams and the result from the next diagram, and both count what the field did, at the field's level; they are written by `pointsgained frontend` (`reports/samples/front_end.md`).

### 13.1 The double on a split

The hammer team has two stones in the house and the opponent none; the non-hammer team throws a hit (10,755 of them, stones 5–15). How often are both hammer stones gone afterwards, by the pair's separation and its stagger (the angle of the line between the stones from level)?

| Separation | Level (<10°) | 10–20° | 20–35° | 35–55° | 55–90° |
|---|---|---|---|---|---|
| 2–3 ft | 25% | 26% | 21% | 8% | 22% |
| 3–4 ft | 9% | 14% | 20% | 8% | 17% |
| 4–6 ft | 2% | 8% | 14% | 6% | 13% |
| 6 ft+ | 0% | 2% | 7% | 5% | 9% |

Two stones side by side at the same depth and four or more feet apart are close to impossible to double: 2%, and essentially none in 989 attempts beyond six feet. Staggered 20–35° at the same separation, the double comes off seven times as often. The skips knew: from the four-to-six-foot pairs the double is called 6% of the time when the pair is level and 32% when it is staggered. Separation alone, which is what a first definition of a split used, misses the effect; the `split_flat` and `split_staggered` labels encode it, and the double relation of Section 4.7 uses the same 15° threshold. The 35–55° column is the stacked pair, one stone nearly behind the other, a different shot.

### 13.2 The runback on the shot rock

A Promotion Take-out on the opponent's shot rock with a stone in front of it: how often does the thrower's team lie shot afterwards, by the distance of the stone in front and the angle of the line from it to the shot rock?

| Distance in front | <5° | 5–10° | 10–20° | 20–35° |
|---|---|---|---|---|
| under 4 ft | 46% (1,537) | 58% (611) | 62% (472) | 71% (143) |
| 4–8 ft | 37% (5,300) | 37% (1,141) | 44% (303) | 39% (100) |
| 8–12 ft | 28% (3,639) | 31% (485) | 38% (164) | 39% (77) |
| 12–15 ft | 31% (878) | 39% (93) | 52% (61) | 27% (15) |

Distance matters sharply: a stone within four feet of the shot rock is run back successfully about half to two-thirds of the time, one eight to twelve feet away about a third. That is why a guard placed tight on a lonely steal stone is dangerous. Angle, which skips rightly say makes a runback harder, shows no penalty here, and that is a selection effect: most runbacks are called nearly straight (13,700 of 15,000 within 10°), and the angled ones are called only when they are on. A difficulty table from outcomes measures the shot as chosen, not the shot in general; separating the two needs the call rate from every position where the runback was available, called or not, which the configuration table makes possible.

### 13.3 By level (next)

Both tables pool the corpus. Split by the event's strength rating (Worlds and Olympics, Europeans A, Pan Continental A, juniors), they become a statement about how the double and the runback change with the level of the field, and the call rates a statement about how the skips at each level read them.

## 14. The early end

### 14.1 What front-end values measured

The first Points Gained model valued the first eight rocks of an end at hundredths of a point, and the values did not behave like execution. A lead's execution was about as repeatable across an event as a fourth's (split-half 0.45 against 0.43) but bore no relation to the grade (−0.10 at player level, against 0.81 for fourths); at team level the lead's and second's values moved together (0.57) and neither moved with the fourth's. The diagnostic that explained it: a stone's execution value correlated −0.28 with the next stone's (stones 1 and 2), and a lead's game correlated −0.40 with the opposing lead's in the same game, while their grades moved together (+0.21). The model priced early positions badly, and each mispricing credited the stone that created the position and charged the stone that followed it: the two leads were trading the model's error.

### 14.2 A nearer target

Every training row had been labelled with the end's final score, so an early position carried the noise of the ten or twelve stones still to come. The fix is to value early positions locally: rows with nine or more rocks remaining are trained on the model's own out-of-fold value of the position two stones later, as a soft label, and the rest on the end's result (Section 7.5). Accuracy against final outcomes is unchanged or better; the front end changes completely. On the whole corpus, in the hand-built model of the time (Appendix A):

| | Before | After |
|---|---|---|
| Lead repeatability (split-half) | 0.447 | 0.653 |
| Opposing leads, same game (grades +0.21) | −0.403 | +0.151 |
| Second: execution against grade (player) | 0.015 | 0.214 |
| Third: execution against grade (player) | 0.352 | 0.454 |

The lead–second team correlation survived the fix (0.64 raw, 0.36 after removing the team's mix of calls and configurations), so it was not the see-saw. What remains is shared by the front end: sweeping, ice reading, the skip's broom, or a team's style. Leads' execution still does not track their grades; lead grades sit near 100% and hardly separate players, which fits conventional observations about the lead position: "relatively little variety, relatively high grades, and mistakes affecting the battle for control more than makes."

A second variant, **phase-aligned** targets, trained every setup stone on the value at the end of the free guard zone; it made the setup battle less repeatable and was not adopted (Appendix A.4).

### 14.3 The battle for the type of end

We assumed in building this that an end had a particular structure: both teams have a goal set by the situation (the hammer team two or a blank and not forced, or just not stolen on; the non-hammer team a steal or a force); the first four or five rocks set up a position compatible with those goals, "almost a battle for a type of end"; a middle game maintains or erases the advantage; the skips cash it in. The corpus has the first phase exactly: the free guard zone, five rocks from the 2018–19 season and four before.

The **setup battle** is the change in value from the empty sheet to the position after the free guard zone, from each team's view. It is small per end (a standard deviation of about 2 percentage points of win probability, against 15 for the rest of the end) but persistent: a team's mean over an event repeats between halves of the event. Its raw correlation with the team's win rate is high, but that is mostly the score: good teams lead more often, and the setup swing correlates with the score difference. The test that matters is within the same score and ends left. For every model before rock traits it was flat: 0.015 on the time split and 0.025 by book for the hand-built model, 0.05–0.06 for the split models of Appendix A.4. The setup looked like a repeatable team trait that predicted nothing about winning.

Read rock by rock, it does. With the adopted model the within-situation correlation between a team's setup battle and its win rate is 0.21 on a held-out fold of books and 0.18 on the 2025–26 events: the setup a team builds, valued by the rocks it leaves and what rocks like them have been worth, is part of how it wins. That is the first evidence in this project for the structure the analysis started from, a battle for the type of end in the first four or five rocks, and it is what the early values had been missing: not a better target or a separate model for the setup, but a better description of the rocks.

**The opening.** The non-hammer team ahead draws into the rings in front of the tee; the hammer team plays a corner guard. Both are graded 98% on average and both goals are intact. It is the standard opening, 9,023 of the 19,308 ends in which the non-hammer team is ahead. The non-hammer team holds the hammer team to one or fewer 69% of the time: a force 36%, a steal 25%, a blank 8%, two or more for the hammer team 31%. The third stone is where the battle is fought: the grade falls to 84%, and the choice between a second stone in the house (4,742 ends, hammer held to one or fewer 71%) and a centre guard (3,750, 68%) is worth three points of that rate. How well leads and seconds contribute is then measured at two levels: the team's setup battle against the field's expectation for the same opening and situation, and within it each stone's execution against the local value, which leaves a routine draw or corner guard near zero and gives the swing to the stone that tipped the type of end.

### 14.4 Scenario probes

A probe fixes a kind of position and a call family, splits the stones by what they left, and sets the model's value of each result beside what those ends were actually worth. They are the acceptance tests for the expectation model (Section 7.7) and the raw material for the strategic studies (Section 16). The report carries six: the split house restored (flat, staggered, or two in but not split), the peel when the hammer team must score, the come-around behind a corner guard, the centre guard without hammer, the steal is on, and guard the steal or take the house (by how many the hammer team counts behind the steal stone, and whether the guard is tight or long).

Generally, the goal of these scenario probes is to validate strategic conventional wisdom in the outcomes, and it sometimes works and it sometimes doesn't. At this level of maturity, we think it's a safe assumption that it is likely a problem with the model and not with conventional wisdom, but it is our hope that we'll eventually be able to challenge or add subtlety to conventional wisdom by analyzing outcomes and the value of those outcomes at scale. In one of the cases studied, with a lonely steal stone in front of two or more hammer stones, the ends where the guard went tight (a runback from under eight feet) were worth 0.688 to the hammer team and the ends where it went long 0.608: the tight guard gives the hammer team more. The model has them the other way round (0.607 and 0.672), before and after the rock-trait refit. It is 400 ends each, and the model's miss is recorded as an open question (Section 18).

**The rock ledger.** The rocks read stone by stone (Section 4.5): after every stone, each team's rock grade, the thrower's **build** (grade added to its own team) and **address** (grade taken from the other team), and the end's **temperature** (both teams' grades together). The game report prints it beside the values, and under each end header each team's grade after the free guard zone, after stone 12 and before the last stone: the setup, the middle game and the conversion. The event reports add a build-or-address table per team, relative to the field at the same stage of the end: a measured form of aggressive and conservative play, building while leaving the other team's rocks standing, against taking them away. The first version of this ledger was built on tracked rock potential (Appendix A.3), whose stone tables supported the asymmetry skips describe: hammer stones in the house end up counting or covering about as often on the wing as in the centre lane (11–16% with eight or more rocks left), while non-hammer stones on the wings do so about half as often as in the centre lane (3–4% against 6–7%), because the hammer team always has the draw to the centre to fall back on. The trait study finds the same from the other direction: a hammer rock on the wing late in the end is worth nearly as much as a counter (Section 4.4).

## 15. Runbacks and players

 Top Canadian skips like Rachel Homan, Brad Jacobs and Kevin Koe are exciting players, and some of their dominance is attributed to their ability to see, call and execute runbacks, an ability to read a house with a lot of junk in it and find the runback that maximises their scoring. The runback table by player (Promotion Take-outs on the opponent's shot rock with a stone in front within 35°; players with 40 or more across the corpus) is the first test.

- **Jacobs** is first of 60 men: 40 runbacks, his team lying shot after 72.5% of them against 38% for the men's field, +0.23 points of execution against the event's field and +4.1 percentage points of win probability per runback, 62% of them from a house with four or more stones.
- **Homan** is first of 40 women by execution (+0.16) and has the largest effect on win probability per runback in either field (+4.4 percentage points), lying shot after 61%, 69% of them from a busy house.
- **Koe** is in the corpus at four events from 2014 to 2019 with 38 runbacks, just under the table's cut-off: lying shot after 50% of them against the field's 38%, but not above the field in execution.

Forty runbacks is a small sample, and the table needs the by-level split of Section 13.3 before it says more than that the two names at the top of their fields in general are also at the top on this shot. It becomes a leaderboard of high-value shots (runbacks, doubles, peels and clearing) in the reports to come.

## 16. Strategic situations: next studies

The probes of Section 14.4 are one step from studies of common strategic situations: a situation, the decision, and the outcomes of each choice as the field played them. The raw comparisons need matching, because the choice is not independent of the score: in the guard-or-take probe, after the ends where the non-hammer team removed a hammer stone the hammer team's chance of winning stood at about a third, and after the ends where it guarded at 50 to 65 percent, mostly because teams choose differently when ahead and when behind. A study matches on the score, ends remaining and the position, then compares the choices. Mike Calcagno has suggested the following examples:

- **Guard the steal or take the house**: lying one in the open without hammer, the hammer team's stones behind; guard (tight or long) or remove a hammer stone and settle for the force.
- **The opening**: after the draw and the corner guard, the third stone's options and their outcomes by situation.
- **The peel when the hammer team must score**: tied or down one in the last end; the peel against the draw, and what a miss costs.
- **Restoring the split**: the hit-and-stick that walks the stagger against the roll that restores it, and the guard that loosens the deuce instead.
- **The freeze-only position**: shot rock in the open with nothing to come around; how often the freeze works, and what the position was worth to the team that left it.
- **The tuck and the runback**: a stone tucked behind an opponent's, by how far behind, and how often it is run back.

---

## Part V. Contributing, open questions and status

## 17. Contributing

The project is built to grow in three directions, and each has a place to start.

**Data.** The corpus is international championship curling from the World Curling results books. The single most useful contribution is more games in shot-by-shot form: national championships (the Brier and the Scotties above all), the Grand Slams, and World Curling Tour events, then anything else with the stones recorded after every shot. A source enters through an adapter that writes the six tables of Section 2.6; a source that is itself a results-book PDF in the CURLIT format needs nothing but the file. Line scores alone are useful too: they feed the win-probability table. If you hold or know of such data, open an issue on the repository.

**Points Gained.** The expectation models are gradient-boosted trees on rock traits, grades, the rocks that matter and the thrower's relations (Part II), trained with a local target, and the evaluation harness is in place: `pointsgained experiment` fits a variant on a time split or a held-out-book fold and scores it on log-loss against the end's result and on the front-end gates, and `pointsgained misprice` shows where it over- or under-prices positions (Section 7.7). The trait vocabulary and the relations are the natural places to contribute: a new trait is a line in `core/traits.py`, a new relation a function like `core/draw.py`. Section 18 lists the known weaknesses; the positions the model misprices are concrete targets, and the scenario probes are their tests.

**Studies.** Every study in Part IV reads the same tables: `points_gained.parquet` (one row per stone, with the three outcome distributions, both currencies, the call and execution split, the thrower and the situation), `rock_traits.parquet` (every rock's traits in every position), `rock_ledger.parquet`, `configurations.parquet` (the labels and measures of every position), `stone_lives.parquet` (every stone tracked through the end), the per-book extraction tables, and the feature cache. `model/trait_study.py` and `model/frontend.py` are worked examples of study modules. The strategic situations of Section 16 and the open problems of Section 17.1 are open; a study that matches on the score, ends remaining and position and compares the choices is the natural next contribution, and finished reports belong in `reports/samples/` with a line in its README.


### 17.1 Open problems

Seven problems that the work so far runs into directly, stated for contributors. `open_problems.md` states these and three more (comparing fields, credit beyond the thrower, uncertainty) in plain curling terms, for readers outside the project. Section 18 is the finer-grained list of known issues.

1. **The value of an early position.** With twelve or more rocks left f is still within about 0.02 log-loss of the trivial model. Reading rocks by their traits made early values less flat (calibration slope 0.95 against 0.92) and, for the first time, related the setup battle to winning (Section 14.3), but the early end is still where the model knows least. Whether it is intrinsically unpredictable or the vocabulary is still missing what a skip reads is open. Start: the log-loss by rocks remaining, the trait study (`pointsgained traits`), the scenario probes.
2. **Learning the vocabulary from data.** The rock traits (Section 4.3) are a hand-written vocabulary whose worth the corpus measures; the configuration labels (Section 4.8) were hand-written tests with hand-set thresholds. Can rocks and positions be grouped by what they lead to, so that the vocabulary is discovered rather than written, and which traits can merge (the Jaccard overlaps of Section 4.3) or should split (open to one side only, a curl-aware exposure)? Start: `rock_traits.parquet`, the stone-type tables of the trait report, `configurations.parquet`.
3. **The best call, and the skip against it.** PG: Call is measured against the field's usual call, not the best available one (Section 6.3); Jacobs' ninth-end runback in the 2026 final is the test case. A best call depends on geometry, the ice (how much it curls decides whether a come-around or a chip is on, as the angle does for a take-out; the books do not record it, so it has to be inferred from how shots behaved), the thrower's make rate and the value of each outcome in the game, and skips manage risk across several stones. Start: the empirical menu (calls the field made from similar positions, valued by g), then the transition model of Section 12.
4. **Strategy and execution together.** A call's value depends on who throws it. The tail hypothesis (Section 11.3) says the best teams accept calls with a fat bad tail because they do not produce it. Separating the right call for a team from the right call for the field without circularity is open. Start: the downside-by-tercile check of Section 11.3, D(S | C) by team.
5. **Execution error from the diagrams.** The delivered-stone marker and prior-position rings (Section 2.2) record where draws came to rest and which stone a hit struck; `pointsgained intent` seeds an error model (`reports/execution_error.md`). The target is never recorded, and inferring it from the result leaks execution into the call (Section 7.3). Start: `intent.py`, the execution-error report.
6. **Difficulty without selection.** Make rates measure shots as chosen: the angled runback shows no penalty because it is called only when it is on (Section 13.2). The correction needs every position where a shot was available, called or not, and a definition of available; the double and runback relations of Section 4.7 are one. Start: the double and runback tables, `combo_features.parquet`.
7. **Rare, decisive situations.** The trees cannot carve out small high-stakes states: the peel miss in a tied last end and the tight guard on a lonely steal stone (Section 14.4). Candidates: targeted relations, a situation-weighted correction. Start: the scenario probes as tests, `pointsgained misprice`.

---

## 18. Open Questions

Resolved in Phase 1: outcome clipping at ±3; full shot types without grouping; men and women pooled with a discipline flag; canonical perspective; recorded score as label; gates as set in Section 2.3; the event tier table; raster before set encoding for the geometry model.

Resolved in the modelling phase: the game-state encoding for f and g is the raw pair (score difference, ends remaining) plus an extra-end flag (Section 7.2); evaluation by time (train through 2024, test 2025–2026) runs alongside the by-book split for every experiment; level of play is the strength of the *event*, hand-rated (Section 7.4); no per-player skill and no grade enters f or g; per-book and per-player values never enter as columns; player identity is a normalised name key per discipline with an alias table (`data/player_aliases.csv`: 31 confirmed pairs such as SCHWARZ B → SCHWARZ-VAN BERKEL, 23 to check, 7 rejected because both names appear in one book); the skill scalar is per player with the team effect as its prior, pooled across seasons for now.

Open:

1. **Event ratings.** The ratings in `data/event_strength.csv` are tier defaults (Worlds 100, Europeans A 85, juniors 70). The derived field strengths already disagree with them in places: the Olympics sit above the Worlds, the Olympic qualifiers and the Pan-Continental championships well below Europeans A.
2. **Event effect granularity.** Event first; sheet and session with shrinkage once the model-level effect exists.
3. **Skill scalar granularity.** Per player with a team-level prior, falling back to team for players with few shots.
4. **Free guard zone eras.** Pooled with an era flag versus per-era f in early-end positions. Only f is affected; g pools across eras.
5. **Player identity.** An alias table for name changes and a stable player id across events.
6. **Leverage-normalised consistency.** Execution divided by the width of the call's menu, so that steadiness is comparable across positions.
7. **Aggressiveness as the shape of the accepted distribution.** The tail hypothesis of Section 11.3 needs validating and then a report: per call, the upside and the downside of D(S | C); per team and per skip, how much downside they accept relative to the field in the same situation, and how much of it they produce. This is the analysis-phase form of the second task in Section 5, capturing the upper end of the outcome distribution.
8. **Situation-specific configurations the trees cannot carve out.** The peel miss in a tied last end and the tight guard on a lonely steal stone (Section 14.4, a few hundred ends each) are rarer than the trees' minimum leaf. A targeted relation (guards remaining when the hammer team must score; the runback distance on a lonely steal) or a situation-weighted correction are the candidates.
9. **The front end's shared component.** A team's lead and second values move together (0.64, 0.36 after the team's call and configuration mix) and not with the fourth's. Sweeping, ice reading, the skip's broom or style; the corpus cannot separate them directly, but the component's relation to results can be measured.
10. **Selection in difficulty tables.** Make rates by geometry measure shots as chosen (Section 13.2). The call rate from every position where a shot was available, from the double and runback relations, is the correction.
11. **g at the last rock.** The rock-trait model matches or beats the hand-built one everywhere except g with one rock left (0.007 behind on the time split, 0.004 by book). The call is known there, so the gap is something the old configuration measures told g about the called shot's geometry that the relations do not yet: a candidate is the relation between the called shot's target (the struck stone) and the double and runback geometry.
12. **The tap.** A relation not yet built (Section 4.7): the tap and double tap onto the thrower's own rocks, with make rates by distance from the Raise calls first.
13. **Seconds' repeatability.** The one credit measure the rock-trait model made worse (0.47 to 0.41 by book).

---

## 19. Status

Built and run, September 2026:

| Milestone | State |
|---|---|
| M1 Ingestion (decoder, detector, text parser, assembly, gates, audit) | Done; 92 books validated, all templates 2014–2026 |
| M2 Core (count function, canonical positions, mirroring) | Done |
| M3 Value mappings, baseline models, Points Gained, reports | Done; f 1.494 / g 1.472 / trivial 1.593 held out by book |
| M4 Archive (inventory, download, survey, parallel batch) | Done; 208 books downloaded, 116 line-score only |
| M6 Plumbing: feature cache, vectorised build and PG, experiment command | Done; full pipeline 2.5 h to 17 min, identical results |
| M7 Game situation in f and g | Done; f 1.470 / g 1.453 / trivial 1.559 held out by book |
| M8 Difficulty model (skill scalar, event effect) built as a report; g takes the event rating | Done; per-player input withdrawn (Appendix A.6) |
| M9 Intent from the delivered stone; target model; ring detector for 2016–2019 | Done |
| M10 Raster geometry model | Built and retired (Appendix A.5) |
| M11 Configurations, the front-end study, local targets | Done; local:2 adopted; configurations retired as inputs (Appendix A.2) |
| M12 Stone tracking, rock potential, the potential ledger; split model tried | Done; potential retired as an input (Appendix A.3), split model not adopted (A.4) |
| M13 Rock traits: the trait study, grades and the rock ledger, slots, the draw to beat, doubles and runbacks; the hand-built stack retired | Done; CV f 1.4660 / g 1.4447; time split f 1.4497 / g 1.4299; one book fold f 1.4555 / g 1.4349; setup battle within situation 0.21 |
| M14 Studies: geometry by level, high-value-shot leaderboards, build-or-address studies, strategic situations; the tap | Next |
| M15 Phase 2 | After M14 |

**September 2026.** The project is organised as a system for others to build on: the ingestion pipeline and corpus (Part I), a way of reading positions rock by rock (Part II), Points Gained as the general expectation tool (Part III), and sample studies built on all three (Part IV), with contributions invited everywhere (Section 17), more game data above all.

**What the rock-trait refit changed in the reports.** Every stone's value was recomputed. Per stone the new values correlate with the old at 0.93 (execution 0.92, the call 0.85); the fourths' execution barely moved (0.96), the front end's most (leads 0.70, seconds 0.79), which is where the old model knew least. On the leaderboards, event-relative execution per player correlates 0.95 with the old (rank 0.98 for fourths, 0.79 for leads), the average miss 0.99 and the big-miss count 0.98; reliability moved more (0.81), because it counts shots above or below the field's expectation and the expectation moved. As the leaderboards sort on reliability, where many players sit within a point or two, positions reshuffle often (a third of players in the nineteen sample books moved three or more places, most of them leads and seconds). Among the fourths the top of each table changed only between players already level: at Milano Cortina Jacobs, Mouat and Schwarz-van Berkel (within about three points of reliability, now in that order), Hasselborg, Morrison, Paetz and Homan among the women (within 1.3 points); at the 2024 Worlds Constantini ahead of Homan on reliability by 0.8 points while Homan still leads on the mean, the median, the floor and the big-miss count. Team win probability gained per game correlates 0.98 with the old (a mean change of 4.7 points per game). Conservation now holds exactly in every end (the one broken end of the previous table is fixed).

The earlier history of the models (September 10 to 26) is in Appendix A; the pinned test set (`pointsgained testset`) remains the face-validity check for every refit: Jacobs' ninth-end clearing in the 2026 final is now −3.4 points of win probability as a call and +18.1 as a throw.

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

A convolutional network on the rasterised sheet (171 × 325 pixels at an inch per pixel, a channel per team, coordinate channels, a narrow bottleneck against memorisation) lost to the trees in every band of rocks remaining (f 1.493 against 1.455 on the time split), and a hybrid with the hand features in its dense layer did too (1.487). It passed the monotonicity checks the trees failed (an opponent stone appearing inside the hammer team's shot rock raised the hammer team's value in 22% of synthetic cases), which is one reason the slots keep the shot rock whole. The set encoding (a permutation-invariant network over stones) was never built; slots are the tabular version of the same idea for the rocks that matter.

### A.6 Per-player skill in g

A shot-difficulty model on the official grade estimated a skill scalar per player and an effect per event, and g briefly took the expected grade of each shot at the thrower's skill (time split g 1.4373 → 1.4297). It was withdrawn: level of play belongs to the field, never to the player being measured (a fairway shot is not judged against Tiger Woods' putting), and grades are too grader-dependent to rate players with. g takes the event's strength rating instead, and the difficulty model survives as a report (`pointsgained difficulty`).

### A.7 What the old model read, and what replaced it

| Retired input | What replaced it |
|---|---|
| 26 position features | Rock traits per team, the count and its margins, each team's nearest stone |
| Configuration labels and measures | The rocks that matter (slots); the draw to beat; doubles and runbacks |
| Rock potential (tracked) | Rock grades (read off the position); the rock ledger |
| Regime and goals columns | Nothing: the game situation columns and the value mapping carry the regime |
| Monotone ordinal model | Nothing: the slots and the trees' inputs fixed most of what it was for |

On the time split the replacement's f is better at every number of rocks remaining except before stones 1 and 3, where it ties (f 1.4497 against 1.4521 overall), and its g ties overall (1.4299 against 1.4299) while giving up 0.007 at the last rock; on a held-out fold of books from every year it is better on both (f 1.4555 against 1.4571, g 1.4349 against 1.4353), again with g slightly behind at the last rock (0.004).
