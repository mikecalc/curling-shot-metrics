# Curling Analytics: A Shot-by-Shot Ingestion Pipeline and Corpus, Points Gained, and Sample Studies — Design Document

**What this is.** We're sharing a method for ingesting data about curling games that are consistent with the format in what are called the "Results Books", which are made available by the World Curling Federation (and via partners like CurlIt) for every major WCF-sponsored curling event, and the Olympic Games, going back to 2013. We've used this pipeline to create a corpus that reads every stone of every end of 4,150 international games into tables: where every stone was before and after every shot, who threw it, what was called, how it was graded, and how the end and the game came out, which in turn forms the basis for doing shot-by-shot analysis.

**How this document is organised.** Part I describes the ingestion pipeline and the existing corpus: where it comes from, how it is extracted and validated, and how a position is described, from the raw stones to the configurations a skip reads (a split house, the steal is on, a runback on the shot rock). Part II introduces a system for valuing individual curling shots that we call **Points Gained**. It creates an expectation model for curling positions, f and g, which says what a position and a call have been worth under the field's play, and a value for every stone as the change it made to that expectation. It is the general tool built on top of the corpus for studying curling shots, and we use it to rate execution, but also to value certain types of shots in strategic analysis, such as how to price a split house, how the setup battle is scored and how a runback is valued. We expect this to improve with more data, and envision that the framework will be useful both for our own curling analysis and those of others. Part III describes a collection of initial studies that the corpus has made possible so far, most of which build upon the shot data and the Points Gained system. Part IV describes how to contribute, and records open questions and status.

**Status (September 2026).** The corpus is built and validated: 92 results books with shot-by-shot pages, 609,014 shots. The expectation models are fitted on hand-built position features, the game situation, the event's level of play, the struck stone and the configuration labels, with early positions trained on the value two stones later (Section 7.6). Studies done: shot geometry for doubles and runbacks (Section 12), the early end (Section 13), runbacks by player (Section 14), player execution (Section 10). Next: common strategic situations (Section 15).

---

## Part I. The ingestion pipeline and the corpus

## 1. What the project provides

Four layers, each usable on its own and each open to contributions (Section 16):

- **An ingestion pipeline** (Section 2). It reads the results-book PDFs directly: the per-shot diagrams are decoded from the embedded images rather than rendered, stones are detected and placed in inches on a fixed sheet frame, the panel text gives the thrower, call, turn and grade, and validation gates check every book before it is used. The output is six tables per book with a documented schema, and that schema is the contract for any other source: a new source of games needs an adapter into the same tables, and everything downstream runs unchanged (Section 2.6).
- **A corpus** (Section 3). The pipeline run over every results book with shot-by-shot pages: 92 books, 4,150 games, 609,014 shots, with stratum labels (event, tier, discipline, era, player, position) on every row.
- **A position vocabulary** (Section 4). A position described from the raw stones up: the exact count, a compact feature vector, and configurations in the terms a skip uses (a split house, flat or staggered; the deuce is loose; the steal is on; a runback on the shot rock; a lonely steal), with continuous measures for the double and the runback.
- **Points Gained** (Part II). An expectation model for positions and calls, and a value for every stone in two currencies (hammer-adjusted points and win probability), split into the call and the execution. Every value is a difference of model outputs, so any grouping of stones (a player, a phase of the end, a shot family, a configuration) can be valued the same way.

The studies of Part III are examples of what the four layers support, each produced by a command in the package, and templates for further studies.

## 2. The ingestion pipeline

### 2.1 Source

The pipeline reads World Curling results books, as published in the CURLIT results-book directory at `curlit.com/results`: one PDF per event, with a shot-by-shot page for every end of every game in the events that have them. The directory lists 310 results books; 208 are team-of-four men's or women's books from 2013 onward and in scope. All 208 were downloaded (2.3 GB). Only 92 contain shot-by-shot pages: 25 tier 1, 42 tier 2, 23 tier 3, 2 tier 4. The other 116 (Europeans B and C, Seniors, Junior-B, Pan Continental B, the qualifiers and the Universiade) are line scores and standings only; they still feed the win-probability table. Any PDF in the same format, from any event, goes through the pipeline unchanged; other sources enter through an adapter (Section 2.6).

Jordan Myslik's earlier extraction (`jwmyslik/curling-analytics`) is the precedent for this work. It could not be rerun: its source host no longer exists and its parser depended on rendered page images. Nothing here depends on it.

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

Player names need care. The books use surname plus initial, in varying case, and a player's team code changes between events (Scotland at the Worlds, Great Britain at the Olympics); reports key on the upper-cased, whitespace-normalised name within a discipline. Genuine name changes ("SCHWARZ B" in 2022, "SCHWARZ-VAN BERKEL" from 2025) are handled by an alias table (`data/player_aliases.csv`, Section 17).

## 4. Positions as a skip reads them

### 4.1 Principles

The subtleties that decide a curling position live at the inch level: whether a double is on, where a roll ends up, whether a guard actually covers the line. Any hand-built classification of positions throws that away. Two representations with different jobs:

- **Raw geometry (built, rejected).** The model sees the stones themselves; whatever matters is learned from outcomes. A convolutional network on the rasterised sheet was trained and lost to the feature model in every band of rocks remaining (Section 7.5).
- **Baseline features (the model).** A compact hand-built vector: originally a baseline to beat and an interpretability layer, now the representation the system runs on. No claim is made that these features capture what a skip evaluates; the results in Section 7 say the models, on either representation, know little early in an end.

### 4.2 Count function

Sort all stones by distance from the pin; a stone is in the house if that distance is at most 72 inches plus the stone radius (5.7 in). The team owning the closest in-house stone scores the number of its in-house stones closer than the nearest in-house opposing stone; an empty house is a blank. Exact, not a judgment; used for terminal positions and as the reconstruction gate.

### 4.3 Baseline feature set

Twenty-eight numbers per position, in the canonical frame ("own" means the hammer team):

- **Situation:** rocks remaining (whose parity says who throws next), rule era, stones in play.
- **Lie:** count (clipped ±3), shot-rock ring, margin (inches between the shot rock and the first opposing stone), owners of the second and third stones, boundary gap (inches between the last counting stone and the first opposing stone) and a near-tie flag (boundary gap under two inches).
- **House occupancy:** own and opposing stones in the house and behind the tee.
- **Guards:** counts per team by lane (left, centre, right; centre is |x| ≤ 24 in) and the depth of the nearest centre guard.
- **Cover (crude):** shot rock covered, button covered, by a straight-line corridor test. Known to be wrong at the margins.
- **Nearest stone** distance per team.

**Near-tie positions.** Stones within about two inches at the ownership boundary are tied on the sheet and unresolvable in the data; these are the ends where reconstruction disagrees with the recorded score. They are a real game state rather than noise: the skip cannot tell which rock is second either, and the call made there (peel, freeze, play for the measure, draw for the sure one) is a strategic response to that uncertainty. D stays a full distribution rather than collapsing on the count, the count function is never ground truth for those ends, and the baseline names the state so that calls in tied positions can be studied.

### 4.4 Configurations

The baseline features describe stones; a skip reads configurations. The two are different in kind: "lying two" is a count, but "the deuce is loose" is a judgement about what the opponent can do about it. The configuration layer (`core/configurations.py`) puts that vocabulary into deterministic tests on the canonical position, multi-label, so a position can be a split house with a corner guard up. The vocabulary and thresholds were developed by Mike Calcagno; where the corpus can test a threshold it has (Section 12). One of the "Hilbert problems" we have is a way to learn these configurations from data.  

| Label | Test ("own" is the hammer team) |
|---|---|
| `empty`, `guards_only`, `open_house` | No stones; no stone in the house; no guards |
| `own_` / `opp_centre_guard`, `own_` / `opp_corner_guard` | A guard within 24 in of the centre line, or outside it |
| `own_shot`, `opp_shot`, `own_` / `opp_two_plus` | Who lies shot; lying two or more |
| `split_house` | Hammer has two or more in the house, every pair at least 3 ft apart, the opponent none |
| `split_flat` | A split whose pairs are 4 ft or more apart and within 15° of level: the double is nearly off |
| `split_staggered` | A split that is not flat: staggered in depth (the walked split); the double is on |
| `own_shot_covered` | Hammer's shot rock has a stone in front of it (straight-line test) |
| `deuce_loose` | From stone 9 (the hammer team's first four thrown): a flat split, or a covered hammer stone that will count second (no opponent stone closer) with the centre open |
| `steal_setup` | Non-hammer has two or more centre guards |
| `steal_on` | Non-hammer lies shot, covered |
| `opp_exposed` | Non-hammer has a stone in the house with nothing in front of it: the premature rock |
| `open_shot_own` / `open_shot_opp` | A team lies shot with no guards anywhere: only a freeze gets the other side shot and hidden |
| `shot_runback_straight` / `shot_runback_angled` | A stone of either team up to 15 ft in front of the shot rock, within 10° of its line, or at 10–35° |
| `lonely_steal` | Non-hammer lies one and the hammer team counts two or more without it |
| `lonely_steal_exposed` | A lonely steal with a runback on it: guarding it risks the big end |
| `busy_house`, `near_tie` | Four or more in the house; a boundary gap under two inches |

Alongside the labels, seven continuous measures: the separation and stagger of each team's two best stones in the house (the double on them), the angle and distance of the best runback on the shot rock, and `swing_if_shot_removed`, the change in the count (hammer team's view) if the shot rock goes. The last is what is at stake: a lonely steal stone in front of the hammer team's two, three and four is a swing of three to five.

Three situations shaped the vocabulary. A **split house**: the hammer team's third hits and sticks to restore it, and whether it is restored flat or staggered decides whether the opponent has a double; each hit-and-stick tends to walk the stagger deeper, the best teams roll a little to restore it, and when they cannot they call something else, a guard, which leads to the deuce being loose. **The steal**: a team that needs a steal wants two guards up before it puts a stone in the house, because an exposed stone is a free hit. **The runback**: a skip can use either team's stone against the other; a guard placed too close to a lonely steal stone, or a stone tucked not far enough behind an opponent's, invites the runback. The question behind all of them is what the position leaves the opponent.

The labels and measures enter f and g as the feature set `config` (Section 7.2), and the front-end report uses them to calibrate the model configuration by configuration and to measure how often each survives the next stone.

---

## Part II. Points Gained: an expectation model for positions

Part II is the framework: a model of what a position and a call have been worth under the field's play, and a value for every stone as the change it made. The studies in Part III use it to put a number on a position, a shot or a phase of the end, and the player and team reports are built from it. Its models, targets and gates are all open to improvement; the open questions in Section 17 are the current list. Worked examples in Sections 5, 6, 7.3 and 10.2 quote the model as it stood at the end of the modelling phase (2026-09-10); the configuration labels and the local target moved them in the second decimal (Jacobs' ninth-end call from −5.7 to −5.5 percentage points of win probability, his throw from +22.7 to +19.3), and `reports/samples/` carries the current values.

## 5. Goal

Assign every shot a value, **Points Gained (PG)**, that measures how much it changed the expected scoring of the end, from the throwing team's point of view. The name is chosen by analogy with strokes gained in golf: it is measured against the field, it is additive, and it decomposes. Two properties are required:

1. **Situation-aware.** A made draw against an opponent stone in the four-foot is worth more than the same draw into an empty house, because the expectation before the shot was lower.
2. **Conserved.** The values of all shots in an end sum to the final score minus the expected score at the start of the end. No credit is created or lost.

The output is a per-shot Points Gained, decomposable into **PG: Call** (selection: what the call was worth) and **PG: Throw** (execution: what the throw delivered against the call).

### 5.1 Philosophy

Every shot in curling has two parts. First a call is made, by the skip and often with the whole team, and the call sets up a menu of possible outcomes with their odds: the roll-out that blanks, the stick that scores one, the miss that gives up a point, the flash that gives up two. Then the shot is thrown, swept and called on line, and one outcome from that menu happens. The call is a decision; the throw is an event, and what can be judged is its effect against the menu the call created.

The model evaluates every rock in both dimensions. Selection asks what the call's menu was worth compared with the position the team was handed. Execution asks what the throw produced compared with the menu the throw was handed. Neither is judged by the other: the execution value does not penalise a poor call or reward a brilliant one, and the selection value does not credit a lucky throw or blame a bad one. A call reads the same on a make and on a miss. The two components sum to the shot's total contribution to the end.

The best calls create menus whose expectation, weighted by how *this* team executes, is highest relative to the position. That is not always the menu with the biggest upside, and the right trade-off depends on who is throwing. The clearest example in the data is Brad Jacobs' last rock in the ninth end of the 2026 Olympic final: down one with hammer, he called a runback through traffic that scored three and decided the gold medal. Against the field's usual call from that position, a draw, the type-only model priced the call at −16.7 percentage points of win probability and the throw at +31.9; with the struck stone as part of the call (Section 7.3) it is −5.7 and +22.7. That is not a verdict that the call was wrong. It says the field does not call that shot, because for the median skip it is a poor menu; whether it was the right menu for Jacobs is a question about geometry (was the shot there?) and about level of play (how often does he make it?), and answering it properly is what Sections 7.5 and 7.4 are for.

### 5.2 Strategy: how game situation enters

Within an end the structure is recursive. Every shot before the last one builds a **position**, every position carries an **outcome distribution** (the chances of blanking, scoring one, scoring two, giving up one, and so on), and the last rock realises one outcome from it. The rock before the last is thrown to make that distribution as bad as possible for the thrower of the last rock; the rock before that, to make it as good as possible two rocks down the line; and so on back to the first stone. The two teams are pulling on the same quantity in opposite directions, which is exact rather than approximate: whatever currency an outcome is valued in, the opponent's value is the negation.

Strategy is the observation that not all outcome distributions are equally useful, and which ones are useful depends on the game. Curlers have a vocabulary for this: *must steal*, *force one*, *two or blank*, *don't give up more than two*, *score or go to the extra end*. In this model those goals are not a separate layer and are not enumerated by hand. They are the *shape* of the value mapping v(outcome | game situation): tied in the last end with hammer, one and two are both worth a win, a blank is worth the chance of winning an extra end with hammer, and a steal is worth nothing, and maximising expected value under that shape simply *is* "score or don't get stolen on." The win-probability table (Section 9.3) generates every one of the named strategies as a consequence.

The two currencies disagree in a way that is itself informative. In hammer-adjusted points, a team protecting a three-point lead reads as calling badly, because points reward aggression whatever the game; in win probability the same calls are neutral. On the four development books, the strongest teams' call values were slightly negative in points and zero in win probability for exactly this reason: they are ahead more often. Rachel Homan's raise with her last rock in the eighth end against Italy at the 2026 Olympics, up two with three ends to play, costs 0.12 points but only 0.4 percentage points of win probability; the game barely depended on that end. Both currencies are kept, and reports say which one they are in.

### 5.3 Terminology

| Term | Meaning |
|---|---|
| **Position** (S) | The stones on the ice plus rocks remaining and rule era, in the canonical hammer-team frame. Pre-shot and post-shot positions bracket every shot. |
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
| **Skill scalar** | A per-thrower level-of-play number estimated from execution grades. Built as a report (Section 7.4); not an input to the models, whose level of play is the event's. |

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

Two of Homan's shots at the 2026 Olympics show the split doing its job. In the fifth end against Sweden, up two without hammer with six ends left, she called a double with the fifteenth rock and missed; Sweden scored three. The call is worth −0.16 points and −2.2 percentage points of win probability against the field's usual call from there, and the throw −0.83 points: a call the field would not make, then a miss. In the seventh end against Switzerland, up three with four to play, she called a take-out and missed; Switzerland scored four. That call is worth +0.02 points, at or above the field's, and the whole cost (−0.79 points) is execution. Same player, same week, same-sized disasters, different diagnoses.

### 6.4 Perspective convention

Every physical position is evaluated **once**, from a canonical perspective: the team holding hammer in the current end. Stones are labelled `hammer` / `non_hammer`, and f is fitted and evaluated only in this frame. A thrower's value is V from the canonical frame, multiplied by +1 if the thrower holds hammer and −1 otherwise.

This is deliberate rather than cosmetic. If f were evaluated from the thrower's perspective, the same physical position would be evaluated twice, once for the team that just threw and once for the team about to throw, and a learned model is not exactly antisymmetric under the swap, so the sum of Points Gained over an end would not telescope. With a single canonical evaluation per position the identity in Section 6.5 holds by construction. Who throws next is determined by the parity of rocks remaining.

### 6.5 Conservation check

With D(final position) defined as the actual score, summing canonical Points Gained over the shots of an end gives

    Σ PG = actual_score − V(D(S₀))

where S₀ is the empty-sheet position at the start of the end. On the full archive the largest residual over 37,585 ends was 9 × 10⁻¹⁶ with the Phase 1 models. It is a unit test, not a diagnostic: in the current table one end breaks it, from a bug in rebuilding a post position that the configuration columns exposed, fixed for the next refit (Section 17).

---

## 7. The expectation models

### 7.1 Insight

Every shot's pre-position is labelled with the end's final outcome. Sparsity of exact positions does not matter once the model can generalise across positions. The outcomes are high-variance per example, but that variance is what the model averages over. This is a supervised problem, not a dynamic-programming problem, and it is deliberately outcomes-biased: it says what positions and calls have been worth given how the field has played, not what they should be worth under optimal play.

### 7.2 Models

- **f(S) → D**: distribution over end outcomes from the position, in the canonical frame. This is D(S) under the field baseline.
- **g(S, C) → D**: the same with the called shot type and turn as inputs. This is D(S | C).

Both are gradient-boosted tree classifiers over seven outcome classes on the Section 4.3 features plus discipline and, since the modelling phase, the **game situation**: the hammer team's score difference (clipped at ±6), ends remaining (clipped at 10) and an extra-end flag. Situation in f changes what D(S) means, from "what this position is worth under typical play" to "what it is worth given how teams play from here in this situation": up three in the ninth, the field runs the end clean, and f now expects that rather than scoring the blank as a failure. The value mapping still carries the situation in the win-probability currency (Section 9.3); the two uses are complementary and the conservation identity is unaffected because V is fixed within an end. Neither model takes an event effect or a skill input yet (Sections 7.4 and 8).

Feature sets are named (`base`, `situation`, `call`, `level`, `intent`, `config`) so that an experiment can toggle them, and the training table is cached once per corpus, so a single-split experiment on 1.2 million rows takes about a hundred seconds. The adopted model adds `config`, the configuration labels and measures of Section 4.4, to f and g, and trains early positions on a local target (Section 7.6); with the target rebuilt inside each fold the full pipeline takes about ninety minutes.

**Regularisation was the whole story on the small corpus.** On four books, about 2,900 labelled ends, the model had to be held to eight leaves, 300 samples per leaf and 60 to 80 boosting rounds to beat the trivial model (rocks remaining, hammer, count) on held-out books; anything richer lost to it. On the archive the plateau is 15 leaves and 200 rounds: 31 leaves and 300 rounds score the same at twenty-five times the cost, 63 leaves are worse. Points Gained are always computed from out-of-fold predictions, so no position is valued by a model that saw its book.

### 7.3 Called shot and intent

The `type` field records the call: Draw, Take-out, Hit and Roll, Guard, Front, Freeze, Raise, Clearing, Double Take-out, Promotion Take-out, Wick / Soft Peeling, Through. Phase 1 uses it as recorded. The type leaves the target ambiguous, and the consequence is visible in the results: a call component an order of magnitude smaller than the throw component, and call verdicts that judge the *family* of shot rather than the shot. Every one of the five "worst calls" of the 2026 men's Olympic tournament by win probability is a last-rock runback or double that the field usually does not play from that position, and three of the five were made and won the end. The model can see that runbacks are usually a worse menu; it cannot see that this runback was on.

The delivered-stone marker (Section 2.2) is the way forward, and the modelling phase built it with one rule that matters more than the rest: **the call must never be read from the outcome.** On a made draw the delivered stone's rest is the target; on a missed draw it is the miss, and on the last rock it is the score. The first attempt used the rest for every draw and cut g's log-loss from 1.430 to 1.415 on the time split, almost all of it at one rock left (0.815 to 0.658): execution had leaked into the call. Gating the rest on the grade did not help, because a flag saying "the target is known" then meant "the draw was made".

What g takes instead (feature set `intent`):

- **Draws** (Draw, Guard, Front, Freeze, Through): the *modal* target from a target model P(target cell | position, call), fitted on made draws with a marker (out of fold by book) and applied to every draw whatever its grade. The cells are three lanes (centre is |x| ≤ 24 in) by six depth bands from through the house to the far guard zone. On made draws the modal cell agrees with the realised one about 56% of the time; the rest is the spread the field's targets have from a given position. Because it is a function of position and call only, it cannot leak, and it adds little: the tree could read the same thing from the position. Its value is as the field's menu for Phase 2.
- **Hits** (Take-out, Hit and Roll, Double, Clearing, Raise, Promotion, Wick): the **struck stone**, the prior-position ring furthest up the sheet (the shooter arrives from the hog line), at any grade: which stone was hit is intent, not outcome. Its columns are the pre-shot position (x, y), owner, ring, whether it was the shot rock and whether it was a guard. Without rings, the modal struck-stone class from a second target model.
- Whether the shooter stayed and whether the target was realised are kept for diagnostics and the Phase 2 error model but are not columns of g.

With that rule the gain is honest and modest: g from 1.4297 to 1.4278 on the time split, from 1.4366 to 1.4342 by book and from 1.447 to 1.444 in the five-fold cross-validation, every band of rocks remaining slightly better, the last rock most (0.815 to 0.796). The information is in the hits. What changes more than the log-loss is the call component: its mean absolute size per shot is now 0.064 points against 0.137 for execution, about half rather than a tenth, and it is largest on the hit family (0.07 to 0.10 on take-outs, doubles, raises and promotions). On the six-shot test set (Section 18) the made runbacks moved the way they should: Jacobs' ninth-end call from −12.0 to −5.7 percentage points of win probability, Retornaz's tied-last-end promotion from −3.7 to +9.7, Muskatewitz's raise from −8.1 to +8.2; Casper's two moved to about neutral (−0.2 and −1.1), and Schwarz-van Berkel's missed clearing got worse as a call (−2.2 to −7.4). These are the final model's numbers, with the event rating and no per-player input (Section 7.4). The rings were missing from the 2016–2019 books because those templates draw them two pixels thick in the moved stone's colour; a second ring rule in the detector recovered them, and those thirty books were re-extracted. The Through / Draw distinction on a last rock with an empty house remains the blank-versus-score decision and is handled by the type alone.

### 7.4 Level of play

A six-foot double is worth less to an elite team than to a club team because the elite team makes it more often: D(S | C) is higher, so the PG: Throw for making it is smaller. Level of play is a property of the **execution distribution** and enters through g.

The archive shows the effect plainly. Execution value per shot, measured against the whole field, is about 0.040 points at tier 1, 0.030 at tier 2 and 0.019 at tier 3, in both disciplines. Today the only level input is the tier and discipline of the event, so a junior's execution is measured against a field that is mostly Olympians, and junior leaderboards are meaningful only within their own event.

The remedy is the **shot-difficulty model** on the official grade, built in the modelling phase. Stage one is a gradient-boosted regression of the grade (0, 25, 50, 75, 100, the same scale in every book since 2013) on the shot's difficulty: type, turn, the position features, rocks remaining, situation and discipline. Stage two is a fractional logistic regression on the stage-one logit with two event-level covariates, the hand-rated **event strength** (`data/event_strength.csv`, men's Worlds = 100) and a **field strength** derived from game results (the mean Bradley–Terry strength of the teams in the book, fitted leaving that book out), plus L2-shrunk effects for team, player and book. Level of play is a property of the *event*: who is in it says how strong it is, and a player's grades are read against the fields they played in. Team rankings inform how strong a field is; they are not a per-player input.

Out of that come two numbers. The **skill scalar** per player (team effect plus shrunk player deviation, in logit units) ranges from about −1.2 to +0.9; Jacobs, Kennedy, Gushue and Sundgren head the men, McEwen and Homan the women, and Chinese Taipei, Australia and Lithuania fill the bottom. The **event effect** per book is what remains once field strength is accounted for: ice, conditions, and the grader, since the grade is a judgement (the 2026 junior men's book sits 0.6 logit above the rest, which is at least partly leniency).

**How it enters g.** Not as the raw numbers. Per-player and per-book values identify the player and the book, and a tree fits book-specific outcome rates on them that do not transfer: with `skill` and `event effect` as columns, g got *worse* out of book (1.4373 to 1.4407 log-loss on the time split). What g takes is the **expected grade of this shot for this thrower** at this event, sigmoid(difficulty + skill), a single continuous number. With it g improves from 1.4373 to 1.4297 on the time split and from 1.4426 to 1.4366 by book, about half the size of the call's own contribution over f. The signal is plainly in the data: on last-rock draws with the hammer team not lying shot, the scoring rate rises from 54% to 78% across skill quartiles.

**Then set aside.** There was some back and forth over whether the individual player's skill scalar should affect our evaluation of the call, and in turn reward or penalize execution against the call. In a similar system, like strokes gained in golf, the system does not evaluate a fairway shot against Tiger Woods' putting, it evaluates it against a tour professional's. Level of play belongs to the *field*, never to the player being measured, and the grade is a judgement whose leniency varies by grader, so it is a poor thing to rate players on. So the per-player expected grade was built, measured, and withdrawn as an input. What g takes as `level` is the **event's strength rating** alone (`data/event_strength.csv`, men's Worlds = 100), a handful of distinct values that cannot identify a book. On the time split it keeps part of the gain (g 1.4325 without any level, 1.4311 with the event rating, 1.4278 with the rejected per-player grade) at no cost in identity. The difficulty model remains as a report (`pointsgained difficulty`: skill leaderboards, event effects, the field strengths next to the ratings) and as the error scale for the Phase 2 transition model; it is not an input to f or g, and Points Gained have a single decomposition again.

### 7.5 Raw geometry (built, rejected)

A position is a set of up to 16 stones, each (x, y, owner) in inches, plus rocks remaining and rule era. Two encodings were planned: a **raster** (the play area as an image fed to a small convolutional network) and a **set** encoding (a permutation-invariant network over stones). The raster was built in the modelling phase: 171 by 325 pixels at one inch per pixel (the full sheet width, from the back line to the hog line), two channels (hammer team, opponent) with stones as filled discs, a third channel marking the intent target for g, rasterised on the Apple GPU per batch from the stone arrays, with mirroring as a training-time augmentation. Two lessons from making it learn at all: the sheet is anchored at the pin, so the network needs *coordinate channels* and must not end in global pooling, which made it blind to location; and a wide flattened head memorises positions (training loss 1.34 against validation 1.63 in three epochs), so a 1×1 bottleneck to eight channels and heavy dropout are needed before the dense layer (293k parameters in all).

**Result (f, time split, five epochs, about 45 minutes on the M3 Pro).** Log-loss 1.493 against 1.455 for the trees, and worse in every band of rocks remaining, including the early end (1.594 against 1.584 at twelve left, 1.644 against 1.627 at sixteen) where the hand features were supposed to be blind. It passes the monotonicity checks of Section 7.9 at 100% where the trees fail one of them: the trees *raise* the hammer team's value when an opponent stone appears inside its shot rock in 22% of synthetic cases, a flaw the geometry model does not have. A hybrid, the same network with the 28 hand features fed to its dense layer, was the last test of whether raw geometry adds anything on top of the features: 1.487, again worse than the trees in every band, and it recovered only part of the monotonicity result (68% on the steal case). A dense layer on tabular features loses to boosted trees on the same features, and the raster path did not add enough to close that gap, let alone overtake. The trees remain the model. What the exercise leaves behind is the rasteriser and training loop (`pointsgained raster`), the probe and monotonicity gates, and one finding about the trees themselves. The set encoding was not built.

### 7.6 Training targets

Labelling every position with the end's final score (the Phase 1 models) is unbiased but noisy early in an end, where ten or more stones remain between the position and the label. The target is a choice (`model/targets.py`):

- **final**: every row labelled with the end's result.
- **local:k** (adopted with k = 2): rows with nine or more rocks remaining are trained on the value of the position k stones later, as a soft label: the out-of-fold f distribution there, from a first-stage f fitted on final labels within the training books, or the end's result if the end finishes first. The classifier is fitted on each such row expanded into its outcome classes with the probabilities as weights. Positions are valued more locally, and the noise of everything after them is averaged by the model rather than carried in the label.
- **phase**: setup stones trained on the value at the end of the free guard zone, the middle game on local:2. Not adopted (Section 13.2).

In the full pipeline the soft targets are rebuilt inside each cross-validation fold from that fold's training books only, so no held-out book shapes the targets its models are trained on; the run takes about 90 minutes rather than 15.

Every experiment is now also scored on **front-end gates** (`reports/experiments/frontend_gates.md`): Points Gained on the held-out events from the experiment's f and g, and whether early execution see-saws (the correlation with the next stone, and between opposing leads in the same game), agreement with grades as a check, repeatability, and the setup battle's repeatability and correlation with win rate.

| Held out | Model | f | g | See-saw, stones 1–4 | Opposing leads | Second vs grade | Setup battle vs win rate |
|---|---|---|---|---|---|---|---|
| Time (2025–26) | final, no configurations | 1.4542 | 1.4311 | −0.178 | −0.526 | 0.079 | 0.651 |
| | configurations + local:2 | 1.4531 | 1.4309 | −0.015 | +0.114 | 0.209 | 0.744 |
| | configurations + local:4 | 1.4525 | 1.4298 | −0.022 | +0.190 | 0.204 | |
| By book (one fold) | final, no configurations | 1.4613 | 1.4382 | −0.197 | −0.606 | 0.082 | 0.601 |
| | configurations + local:2 | 1.4580 | 1.4362 | −0.015 | +0.095 | 0.420 | 0.635 |
| | configurations + local:4 | 1.4577 | 1.4353 | +0.022 | +0.157 | 0.442 | |

local:4 is marginally more accurate but pulls leads away from their grades (−0.25 on the time split, −0.15 by book, against about −0.05 for local:2) for no reason that is understood, so local:2 was adopted.

### 7.7 Results

Held out by book on the full archive, five folds, with and without the game situation:

| Model | Log-loss (base) | Log-loss (with situation) | Brier (with situation) |
|---|---|---|---|
| Trivial (rocks remaining, hammer, count; plus situation) | 1.593 | 1.559 | 0.742 |
| f (position features) | 1.494 | 1.470 | 0.708 |
| g (position and call) | 1.472 | 1.453 | 0.701 |
| g with the struck stone (Section 7.3) and the event rating (Section 7.4) | | 1.447 | 0.699 |
| *rejected:* g with the per-player expected grade | | 1.447 | 0.699 |
| *rejected:* g with the per-player expected grade and the struck stone | | 1.444 | 0.698 |

On the time split (train through 2024, test on the 2025 and 2026 events, 219,000 held-out rows) the same story: f 1.477 to 1.454 and g 1.455 to 1.437. The situation helps in every band of rocks remaining and in every score-difference band, most at tied scores (1.403 to 1.366 on the time split), where ends remaining decides whether the end is "two or blank" or "must score". It was adopted on that evidence (experiment log in `reports/experiments/`). The regime label and the v-vector as alternative encodings were not needed.

The gain over the trivial model is real and its location is the important finding. With one rock left the features cut log-loss from 1.23 to 0.94; with four left, from 1.51 to 1.38; with twelve or more left, by 0.04 or less. The model knows what a position is worth once the end is nearly decided and knows almost nothing early. Since tree capacity no longer matters, this is the hand-built features' limit rather than the data's: the geometry a skip reads in the first eight rocks is not in the twenty-eight numbers. It is the case for the raw-geometry model.

The situation also removed most of the reporting artefact of Section 5.2. In hammer-adjusted points the hammer team's call value when up three or more was −0.026 per shot before and is −0.014 after; the non-hammer team's when down three or more went from −0.025 to −0.011, and its execution value in that state from −0.029 to +0.005. What remains is the residual that only the win-probability currency removes.

Two consequences for the reports. Execution values early in an end are noise around a flat baseline, so leaderboards are effectively about the last six rocks of each end. And the call component is small (about 0.005 points per shot against 0.05 for execution) because the call is a type.

**With configurations and the local target (September 2026).** The adopted model (`--features base,situation,level,intent,config --target local:2`) cross-validates at f 1.4677 and g 1.4457 held out by book, from 1.4704 and 1.4472. The gain is in the middle and the end of an end, where the configurations are; with twelve or more rocks left f is still within 0.02 of the trivial model. What changed for early stones is not accuracy but what their values mean: Section 13.2. The statement above that early-end execution values are noise around a flat baseline described the final-score target and no longer holds for leads and seconds.

### 7.8 Training set construction

One row per shot for f, with the pre-position and the end's outcome from the hammer team's perspective; one per shot for g with the call. Mirrored rows are added. Conceded ends and books that failed the gates are excluded. Held-out splits are by book, never by shot or end.

### 7.9 Validation

- Held-out log-loss and Brier score against the trivial model, overall and by rocks remaining; calibration by outcome class.
- Conservation to numerical precision (Section 6.5).
- Calibration at the empty sheet: V(f(S₀)) with hammer should equal H. On the archive, 0.582 against 0.582.
- Face validity of the leaderboards against the game (Section 10).
- For the raw-geometry model, the **subtlety probe** (built in `pointsgained raster`, not run: the geometry model failed the log-loss gate on f, so g was never trained): take real positions where a double was made, translate the target stone by ±1, ±2, ±4 inches, and plot g(S, Double) against the offset. A model that has learned the geometry shows a sharp drop where the double closes; a model that has not shows a flat line.

**Acceptance cases for model changes** (Section 13.4), after the adopted refit. The split-house restores are now ordered as they play: restored flat 1.053 (realised 1.082), staggered 0.976 (0.972), two in but not split 0.886 (0.658), where the first model valued all three at about 0.96; the last is still too high. The peel when the hammer team must score still fails: after a peel that removes no guard in a tied last end the model puts the hammer team's chance at 77% and those ends were won 69.5% of the time (a steal 30% of the time against the model's 23%), so the miss is still not charged.

---

## 8. Conditions and Field Adjustment

Ice varies: swing, speed, pebble, flatness, and how they change over a game and a week. The design does not model any of it. It follows strokes gained in golf, where the difficulty of a green is never modelled; it falls out of how the field putted on it that week, and a player is measured against that field. If draws to the four-foot are made 65% of the time at one event and 80% at another, that difference *is* the ice, and a made draw at the first event earns more.

This is done at two levels. At the reporting layer, a player's execution at an event is reported relative to that event's field for the same shot type and hammer state (Section 10). At the model level, g takes the event's strength rating, so the field a shot was played in sets the expectation; the residual per-book effect that the difficulty model estimates (ice, conditions, grader) is reported but not fed to g, because a per-book value identifies the book and the trees fit book-specific outcome rates on it that do not transfer. Sheet and session effects, shrunk hard towards the event, are a later step. The value function f is not conditioned on event: a position's worth under typical play is a property of the game, and ice effects on value are assumed to wash through execution.

---

## 9. Value Mapping V

### 9.1 Why blank cannot be zero

With V = expected points and blank = 0, a skip who faces two on the last rock and executes the called double-and-roll-out is scored *below* a skip who sticks and takes one. In the middle ends that is backwards: the blank keeps hammer, and at the elite level hammer is worth more than the point.

### 9.2 Hammer-adjusted points

Let **N** be the hammer team's expected net score in one end and **H** the infinite-horizon value of holding hammer: treating the game as a Markov chain over ends with a stationary outcome distribution, H = N + (P(blank) + P(steal) − P(score)) · H. From the thrower's perspective,

    v(outcome) = points + H × hammer_after

with `hammer_after` = +1 if the thrower's team keeps hammer (blank or steal) and −1 if it scores. Blank outranks a single exactly when H > 0.5.

On the archive, from 19,175 men's and 18,410 women's ends:

| | N | H |
|---|---|---|
| Men | 0.81 | 0.61 |
| Women | 0.72 | 0.55 |

so a blank is worth 0.61 to a men's team and a single 0.39, and "don't take one in the middle ends" is a fact about elite play rather than a maxim. The hammer team's outcome distribution is 13% blank, 34% one, 23% two, 9% three or more, and 21% stolen on.

### 9.3 Win probability

V(D; situation) = Σ D(o) · v(o | score difference, ends remaining, hammer), where v is the win probability after the end, from a table built by backward induction over an end-outcome distribution conditioned on the situation and shrunk towards the pooled distribution. The table comes from line scores, which every results book carries, including the 116 without shot-by-shot pages. Same interface as 9.2; every shot carries both currencies.

Some values from the table: tied at the start with hammer, 63%; tied in the last end with hammer, 80%; up two without hammer with three ends left, 81%; down one with hammer with five left, 44%. The named regimes fall out of the shape of v: tied in the last end with hammer, one and two are each worth a win; up three with hammer in the fourth, the call values in points are −0.02 per shot and in win probability zero.

Hammer-adjusted points is the default reporting currency because it is easier to read and does not compress blowout ends; win probability is used for situation questions and to keep points from scolding a team for protecting a lead.

---

## 10. Outputs and Reporting

### 10.1 Per shot

Every shot carries D(S), D(S | C), D(S′), the three values in both currencies, `pg`, `pg_call`, `pg_throw` and their win-probability counterparts, the thrower, the call, the grade, and the game situation. This table is the substrate for every report and for any future question interface.

### 10.2 Player reporting conventions

Building the player reports taught several things about what a shot value should be aggregated into.

**Execution relative to the field.** Raw PG: Throw averages positive, about 0.05 points per shot, because every throw is an opportunity to improve one's own position; and fourths carry most of the leverage. Players are therefore reported as execution minus the field's mean for the same shot type and hammer state, either the whole corpus or that event's field. A second baseline, the same shot number and hammer state, puts leads and fourths on one footing; the shot-type baseline reads more naturally position against position, which is how curling people compare players, and is the default.

**Median, mean and the tail.** The per-shot distribution is heavily skewed, and the skew is where the metric earns its keep. The 2022 Olympic men's tournament makes the point. Among the fourths, John Shuster's median shot (+0.020) was mid-pack, but his mean was −0.019: his five worst shots cost 7.9 points, nineteen shots cost more than half a point each, and the list of them is the list of last rocks stolen for two and four. Joël Retornaz is the mirror image, the lowest official percentage (79%) and the lowest median in the group (−0.001) but a positive mean (+0.026), because fifteen of his shots earned more than half a point: a high-variance skip whose misses were cheap and whose makes were expensive. The official percentage, which counts every shot once, cannot see either pattern. Reports therefore carry the mean, the median, the counts of shots beyond half a point either way, and the sum of the five costliest shots.

**Outcome first.** Execution, PG: Throw, is the primary pivot in both currencies. It is the part of the shot's value that does not depend on reading the skip's mind, and it credits what curlers credit: the position left, whatever the scorer wrote down. A hit that ticks a guard through a port and improves the position is a miss on the sheet and a gain here; a skip who calls plan B while the rock is moving gets the position that plan B produced. The tail columns below are reported in points and again in win probability (`floor10_wp`, `big_misses_wp` counting shots that cost five or more points of win probability, `worst5_wp`), because a costly miss in a decided game and one in a tied last end are different events. The call component is reported after execution, and its fairness to an elite skip is a secondary concern (Section 7.3).

**Consistency.** Variance is mostly the leverage of the position, not the person, and a symmetric spread treats the gambler and the choker alike. Two positive-is-good numbers are reported instead: the **floor**, the tenth percentile of event-relative execution ("on a bad day this cost this much"), and **reliability**, the share of shots at or above the field's expectation for that shot type and hammer state. A leverage-free version, execution divided by the width of the call's menu, is a next step.

**The distribution, not its average (2026-09-14).** The leaderboards now sort on reliability and show the distribution split: the average make, the average miss, the big-make and big-miss counts and the worst five, with the mean kept as `net`; the median and the floor are retired from the tables (still in the combined CSV). Over 95 fourth-at-event rows from the six major books (OWG2022, OWG2026, WMCC2025/2026, WWCC2025/2026) the mean correlates with the team's win rate at 0.79 (Spearman), reliability at 0.70 and the median at 0.67, and reliability and the median carry the same information (0.95 between them). The split shows why the mean ranks best and what it hides: the size of the average make is unrelated to winning (0.04) and barely varies across fourths, +0.25 to +0.30 nearly everywhere, while the size of the average miss is (0.53 overall, 0.62 within the top two terciles by reliability). The two shapes a median cannot distinguish are both in the data: Jacobs and Mouat at Milano Cortina 2026 sit on nearly the same reliability with average misses of −0.22 and −0.29 and win rates of 82 and 55 percent. Fourths only so far; for the front end the misses are small in points and the split may separate players less.

**The Beijing final.** Those columns for the two 2022 Olympic finalists:

| | shots | median | mean | floor | reliability | big misses | grade |
|---|---|---|---|---|---|---|---|
| Edin | 213 | 0.043 | 0.031 | −0.362 | 61.5% | 15 | 84.1 |
| Mouat | 206 | 0.047 | 0.050 | −0.312 | 62.6% | 8 | 89.0 |

Mouat edges every column, the big-miss count most; both separate from the other fourths and from each other on nothing by much. Sweden won the final 5–4 in an extra end. The model's read of the tournament is the field's two most reliable fourths playing to a draw.

**Homan across the cycle.** Rachel Homan's three tier-1 events show the arc a skip can have:

| Event | median | mean | floor | reliability | big misses | big makes | grade |
|---|---|---|---|---|---|---|---|
| Worlds 2024 | 0.110 | 0.131 | −0.244 | 66.4% | 8 | 25 | 88.5 |
| Worlds 2025 | 0.090 | 0.118 | −0.324 | 66.0% | 12 | 29 | 87.6 |
| Olympics 2026 | 0.053 | 0.050 | −0.438 | 57.3% | 14 | 20 | 77.7 |

Worlds 2024 is the most dominant single-event line in the cycle by any column: first among thirteen fourths on all of them, a floor no other fourth at any tier-1 event of the cycle approaches, and a median double the next skip's. Olympics 2026 is third by median, sixth by floor, with a tail the size of Shuster's in 2022. Her typical shot barely changed; the floor fell. Her eight costliest shots that week were three last-rock runbacks that became steals, three fifteenth rocks that let the opponent score three or four, and a hammer draw for one, five of them in one-point losses.

### 10.3 Reports produced

- **Model report:** corpus counts, the hammer distribution, N and H by discipline, held-out log-loss by model and by rocks remaining, conservation and calibration, win-probability examples; then the whole-corpus performance tables under the currency rule (teams by record and win probability gained per game; players per position by the execution block with big makes and misses per 100 shots; execution by shot type) and the stratified model checks. `pointsgained model-report` rewrites it from the saved run summary without refitting.
- **Strata:** by discipline and tier, by hammer, by game state and hammer, by shot type and hammer, players relative to the field, teams by hammer; all in both currencies.
- **Per-event leaderboards** (`pointsgained events`): one row per player and event with position, shots, games and the execution block relative to the event's field: reliability, average make, average miss, big makes and misses, worst five, and the mean as `net`; then the effect on win probability for reference (big makes and misses, best and worst five), the call value and the official grade. Sorted by reliability, then average miss. The CSV also carries the median, floor, variability and slot-relative execution. The team table above the position groups is the team-level view: record and the summed effect of the team's own stones on its chance of winning per game, with no execution columns (the currency rule: teams in win probability, individuals by execution).
- **Game report** (`pointsgained game`): one game from the per-shot table. The currency follows the level of the table: team-level tables are in win probability, the currency that knows which end it is (Section 9.3); individual tables lead with execution in hammer-adjusted points, the leaderboard measure, with the effect on win probability beside it. So: an end table with the running score, one team's win probability before and after the end and the swing, and nothing else; a players table with each player's PGAA (points gained above average, `pg_throw` in the tables) summed over the game, their worst and best stones, the grade, and their stones' summed win-probability effect as a reference; the ten largest swings; and every stone in the order situation, shot, execution (PGAA and call), effect (win probability after and the change). The conservation identity holds in win probability too (one team's changes minus the other's is the end's swing); the report warns only if it fails. It is the report that lets a leaderboard number be traced to the stones that produced it.

Every per-shot value is a difference of model outputs, so these tables are exactly reproducible from the Parquet tables and the fitted models. `reports/samples/` keeps finished copies in the repository (the model report, the test set, the 2026 Olympic and World Championship leaderboards, Beijing 2022, and the two 2026 Olympic finals shot by shot) with a README on how each is built and what it says. One pattern from those samples is recorded here because it bears on Section 7.3: in every event sampled, the teams with the best execution have negative call values and the teams with the worst have positive ones. A first check over 777 team-events (300 or more stones each) says the sign is situation, not judgement. Split each shot's call value into an event mean, a situation component (score, ends remaining, hammer, stone number) and the remainder within the situation: only the situation component correlates with execution (−0.20), and the within-situation call is flat (+0.02). Good teams are scored on less, so they hold hammer less and throw from different situations; within the same situation their calls are valued no differently from anyone else's. Neither reading of the column survives: the best skips are not calling worse, and they are not knowingly taking lower-expectation calls.

**The tail hypothesis.** Where the teams do separate is on the downside of the call. One hypothesis: the best teams call shots whose field distribution D(S | C) has a fat bad tail because they know their own team will not produce it, an instinct for which part of the distribution is safe to ignore, where an average skip weighs the misses. The same first check supports it. Measure a call's downside as the expected shortfall below the pre-shot expectation under D(S | C), and split each situation's stones into downside terciles. The best teams accept slightly more downside than the field in the same situation (+0.13). The execution gap between the best and worst quartile of teams grows with the downside of the call: 0.028, 0.041 and 0.059 points per stone across the terciles, and 0.041, 0.050 and 0.062 after dividing execution by the width of the call's distribution, so it is not the leverage of risky calls doing the work. Top-quartile teams execute risky calls as well as safe ones relative to the field; bottom-quartile teams execute them worse. The same split by the call's mean value discriminates far less (+0.09): it is the tail, not the expectation. The precise form of the hypothesis is then that the bad tail of the field's distribution for a risky call is produced by the weaker teams, and a top skip's estimate of the downside is lower than the field's because their team is the source of little of it.

This has not been validated beyond that one check: one measure of downside, terciles within coarse situation strata, team-events as the unit, and the field defined as the teams at the event. It points at a way to talk about aggressiveness in terms of the shape of the outcome distribution a call accepts, the upside, the downside tail, and which part of it a team produces, rather than in terms of shot types; a report built on it is a next step (Section 17).

---

## 11. Phase 2: Physics, Transitions, and the Best Call

Phase 1 answers "what has this been worth." Phase 2 answers "what could this have been worth," which needs counterfactual calls, and therefore a model of what happens when a shot is thrown.

- **Simulator.** Collision geometry, rolls, raises and runbacks are deterministic physics; the Digital Curling platform and similar simulators implement them. A simulator answers the inch-level questions the raw-geometry model has to learn statistically: is the double on, where does the shooter roll, does the raise reach.
- **Execution error model.** The only stochastic component. Learned from the delivered-stone marker: for each (type, inferred target, skill scalar, event effect), the distribution of where the thrown stone arrived relative to the target. Seeded in the modelling phase: `pointsgained intent` writes the delivered stone's rest relative to the modal target for every draw with a marker, by grade, skill tercile and rocks-remaining band (`reports/execution_error.md`). On late-end draws graded 100% the median lateral error is about 8 in and the depth interquartile range about 27 in, part of which is the target cell's coarseness; at 75% the depth spread is 41 in.
- **Transition model.** P(S′ | S, call) = simulator applied to the call with delivery sampled from the error model. It replaces the crude cover features of Section 4.3 with simulated shot-availability probabilities.
- **Rollouts.** From any position, simulate the remainder of the end under a policy, initially the empirical policy P(C | S, situation), evaluating with f at a fixed depth. When the policy is replaced by an optimising one, there is a single objective for both teams, since v is zero-sum, and the named strategies emerge from the shape of v.
- **Best-call baseline.** For each position, evaluate each candidate call by rollout and take the maximum; selection under this baseline is the regret of the call made. The best call is skill-dependent, so it must be evaluated at the thrower's skill scalar. Jacobs' ninth-end runback in the 2026 final is the test: at the field's skill the field baseline calls it a poor menu; at his, it may have been the best shot on the sheet. Elite skips disagree in exactly the positions where it matters, so the best-call baseline is reported with uncertainty and is never the headline number.

---

## Part III. Sample studies

Each study below is produced by a command in the package, from the corpus tables and the Points Gained table, and each is a template: change the position, the call family or the situation and the same code answers a different question. The samples are in `reports/samples/`.

| Study | Question | What it found | Command | Section |
|---|---|---|---|---|
| The double on a split | How often does the opponent double off two stones, by how far apart and how staggered they are? | Four to six feet apart and level: 2%; staggered 20–35°: 14%. The field calls the double 6% and 32% of the time. | `frontend` | 12.1 |
| The runback | How often does a runback on the shot rock leave the thrower lying shot? | From under four feet 46–71%, from eight to twelve feet 28–39%. Angle shows no penalty: skips call angled ones only when they are on. | `frontend` | 12.2 |
| The early end | What do lead and second values measure, and who wins the battle over the setup? | The first model see-sawed between consecutive stones; a nearer training target removed it, and a team's setup result tracks its win rate (0.74 on held-out events). | `frontend`, `experiment` | 13 |
| The opening | Non-hammer ahead, a draw into the rings, a hammer corner guard: who wins? | The non-hammer team holds the hammer team to one or fewer 69% of the time (9,023 ends). | (analysis in 13.3) | 13.3 |
| Runbacks by player | Are the dominant skips the best at runbacks? | Jacobs first of 60 men; Homan the largest win-probability effect per runback in either field. | `frontend` | 14 |
| Player execution | Who executes best against the field, and how: typical shot, misses, tail? | Reliability and the size of the average miss separate the fourths; the mean tracks win rate best. | `events`, `game`, `model-report` | 10.2 |

## 12. Shot geometry: doubles and runbacks

Two tables that exist only because every stone is on file. Both read the pre-shot geometry from the diagrams and the result from the next diagram, and both count what the field did, at the field's level; they are written by `pointsgained frontend` (`reports/samples/front_end.md`).

### 12.1 The double on a split

The hammer team has two stones in the house and the opponent none; the non-hammer team throws a hit (10,755 of them, stones 5–15). How often are both hammer stones gone afterwards, by the pair's separation and its stagger (the angle of the line between the stones from level)?

| Separation | Level (<10°) | 10–20° | 20–35° | 35–55° | 55–90° |
|---|---|---|---|---|---|
| 2–3 ft | 25% | 26% | 21% | 8% | 22% |
| 3–4 ft | 9% | 14% | 20% | 8% | 17% |
| 4–6 ft | 2% | 8% | 14% | 6% | 13% |
| 6 ft+ | 0% | 2% | 7% | 5% | 9% |

Two stones side by side at the same depth and four or more feet apart are close to impossible to double: 2%, and essentially none in 989 attempts beyond six feet. Staggered 20–35° at the same separation, the double comes off seven times as often. The skips knew: from the four-to-six-foot pairs the double is called 6% of the time when the pair is level and 32% when it is staggered. Separation alone, which is what a first definition of a split used, misses the effect; the `split_flat` and `split_staggered` labels encode it. The 35–55° column is the stacked pair, one stone nearly behind the other, a different shot.

### 12.2 The runback on the shot rock

A Promotion Take-out on the opponent's shot rock with a stone in front of it: how often does the thrower's team lie shot afterwards, by the distance of the stone in front and the angle of the line from it to the shot rock?

| Distance in front | <5° | 5–10° | 10–20° | 20–35° |
|---|---|---|---|---|
| under 4 ft | 46% (1,537) | 58% (611) | 62% (472) | 71% (143) |
| 4–8 ft | 37% (5,300) | 37% (1,141) | 44% (303) | 39% (100) |
| 8–12 ft | 28% (3,639) | 31% (485) | 38% (164) | 39% (77) |
| 12–15 ft | 31% (878) | 39% (93) | 52% (61) | 27% (15) |

Distance matters sharply: a stone within four feet of the shot rock is run back successfully about half to two-thirds of the time, one eight to twelve feet away about a third. That is why a guard placed tight on a lonely steal stone is dangerous. Angle, which skips rightly say makes a runback harder, shows no penalty here, and that is a selection effect: most runbacks are called nearly straight (13,700 of 15,000 within 10°), and the angled ones are called only when they are on. A difficulty table from outcomes measures the shot as chosen, not the shot in general; separating the two needs the call rate from every position where the runback was available, called or not, which the configuration table makes possible.

### 12.3 By level (next)

Both tables pool the corpus. Split by the event's strength rating (Worlds and Olympics, Europeans A, Pan Continental A, juniors), they become a statement about how the double and the runback change with the level of the field, and the call rates a statement about how the skips at each level read them.

## 13. The early end

### 13.1 What front-end values measured

The first Points Gained model valued the first eight rocks of an end at hundredths of a point, and the values did not behave like execution. A lead's execution was about as repeatable across an event as a fourth's (split-half 0.45 against 0.43) but bore no relation to the grade (−0.10 at player level, against 0.81 for fourths); at team level the lead's and second's values moved together (0.57) and neither moved with the fourth's. The diagnostic that explained it: a stone's execution value correlated −0.28 with the next stone's (stones 1 and 2), and a lead's game correlated −0.40 with the opposing lead's in the same game, while their grades moved together (+0.21). The model priced early positions badly, and each mispricing credited the stone that created the position and charged the stone that followed it: the two leads were trading the model's error.

### 13.2 A nearer target

Every training row had been labelled with the end's final score, so an early position carried the noise of the ten or twelve stones still to come. The fix is to value early positions locally: rows with nine or more rocks remaining are trained on the model's own out-of-fold value of the position two stones later, as a soft label, and the rest on the end's result (Section 7.6). Accuracy against final outcomes is unchanged or better; the front end changes completely. On the whole corpus after the refit:

| | Before | After |
|---|---|---|
| Lead repeatability (split-half) | 0.447 | 0.653 |
| Opposing leads, same game (grades +0.21) | −0.403 | +0.151 |
| Second: execution against grade (player) | 0.015 | 0.214 |
| Third: execution against grade (player) | 0.352 | 0.454 |

The lead–second team correlation survived the fix (0.64 raw, 0.36 after removing the team's mix of calls and configurations), so it was not the see-saw. What remains is shared by the front end: sweeping, ice reading, the skip's broom, or a team's style. Leads' execution still does not track their grades; lead grades sit near 100% and hardly separate players, which fits conventional observations about the lead position: "relatively little variety, relatively high grades, and mistakes affecting the battle for control more than makes."

A second variant, **phase-aligned** targets, trained every setup stone on the value at the end of the free guard zone, so the whole setup would be judged by the position it produced. It was no more accurate and made the setup battle less repeatable (0.40 against 0.46 on the time split, 0.23 against 0.30 by book) and less related to winning, and was not adopted.

### 13.3 The battle for the type of end

We assumed in building this that an end had a particular structure: both teams have a goal set by the situation (the hammer team two or a blank and not forced, or just not stolen on; the non-hammer team a steal or a force); the first four or five rocks set up a position compatible with those goals, "almost a battle for a type of end"; a middle game maintains or erases the advantage; the skips cash it in. The corpus has the first phase exactly: the free guard zone, five rocks from the 2018–19 season and four before.

The **setup battle** is the change in value from the empty sheet to the position after the free guard zone, from each team's view. It is small per end (a standard deviation of 2 percentage points of win probability, against 15 for the rest of the end) but persistent: a team's mean over an event repeats between halves of the event and correlates with its win rate (0.74 on the held-out 2025–26 events with the adopted model, 0.65 before). Classified by which outcome the setup made more likely, ends sort as the vocabulary says: setups that moved towards two or more for the hammer team produced two or more 39% of the time; setups that moved towards a steal produced a steal 27% of the time.

**The opening.** The non-hammer team ahead draws into the rings in front of the tee; the hammer team plays a corner guard. Both are graded 98% on average and both goals are intact. It is the standard opening, 9,023 of the 19,308 ends in which the non-hammer team is ahead. The non-hammer team holds the hammer team to one or fewer 69% of the time: a force 36%, a steal 25%, a blank 8%, two or more for the hammer team 31%. The third stone is where the battle is fought: the grade falls to 84%, and the choice between a second stone in the house (4,742 ends, hammer held to one or fewer 71%) and a centre guard (3,750, 68%) is worth three points of that rate. How well leads and seconds contribute is then measured at two levels: the team's setup battle against the field's expectation for the same opening and situation, and within it each stone's execution against the local value, which leaves a routine draw or corner guard near zero and gives the swing to the stone that tipped the type of end.

### 13.4 Scenario probes

A probe fixes a kind of position and a call family, splits the stones by what they left, and sets the model's value of each result beside what those ends were actually worth. They are the acceptance tests for the expectation model (Section 7.9) and the raw material for the strategic studies (Section 15). The report carries six: the split house restored (flat, staggered, or two in but not split), the peel when the hammer team must score, the come-around behind a corner guard, the centre guard without hammer, the steal is on, and guard the steal or take the house (by how many the hammer team counts behind the steal stone, and whether the guard is tight or long).

Generally, the goal of these scenario probes is to validate strategic conventional wisdom in the outcomes, and it sometimes works and it sometimes doesn't. At this level of maturity, we think it's a safe assumption that it is likely a problem with the model and not with conventional wisdom, but it is our hope that we'll eventually be able to challenge or add subtlety to conventional wisdom by analyzing outcomes and the value of those outcomes at scale. In one of the cases studied, with a lonely steal stone in front of two or more hammer stones, the ends where the guard went tight (a runback from under eight feet) were worth 0.688 to the hammer team and the ends where it went long 0.608: the tight guard gives the hammer team more. The model has them the other way round (0.586 and 0.620). It is 400 ends each, and the model's miss is recorded as an open question (Section 17).

## 14. Runbacks and players

 Top Canadian skips like Rachel Homan, Brad Jacobs and Kevin Koe are exciting players, and some of their dominance is attributed to their ability to see, call and execute runbacks, an ability to read a house with a lot of junk in it and find the runback that maximises their scoring. The runback table by player (Promotion Take-outs on the opponent's shot rock with a stone in front within 35°; players with 40 or more across the corpus) is the first test.

- **Jacobs** is first of 60 men: 40 runbacks, his team lying shot after 72.5% of them against 38% for the men's field, +0.23 points of execution against the event's field and +4.1 percentage points of win probability per runback, 62% of them from a house with four or more stones.
- **Homan** is third of 40 women by execution (+0.13) and has the largest effect on win probability per runback in either field (+4.2 percentage points), lying shot after 61%, 69% of them from a busy house.
- **Koe** is in the corpus at four events from 2014 to 2019 with 38 runbacks, just under the table's cut-off: lying shot after 50% of them against the field's 38%, but not above the field in execution.

Forty runbacks is a small sample, and the table needs the by-level split of Section 12.3 before it says more than that the two names at the top of their fields in general are also at the top on this shot. It becomes a leaderboard of high-value shots (runbacks, doubles, peels and clearing) in the reports to come.

## 15. Strategic situations: next studies

The probes of Section 13.4 are one step from studies of common strategic situations: a situation, the decision, and the outcomes of each choice as the field played them. The raw comparisons need matching, because the choice is not independent of the score: in the guard-or-take probe, after the ends where the non-hammer team removed a hammer stone the hammer team's chance of winning stood at about a third, and after the ends where it guarded at 50 to 65 percent, mostly because teams choose differently when ahead and when behind. A study matches on the score, ends remaining and the position, then compares the choices. Mike Calcagno has suggested the following examples:

- **Guard the steal or take the house**: lying one in the open without hammer, the hammer team's stones behind; guard (tight or long) or remove a hammer stone and settle for the force.
- **The opening**: after the draw and the corner guard, the third stone's options and their outcomes by situation.
- **The peel when the hammer team must score**: tied or down one in the last end; the peel against the draw, and what a miss costs.
- **Restoring the split**: the hit-and-stick that walks the stagger against the roll that restores it, and the guard that loosens the deuce instead.
- **The freeze-only position**: shot rock in the open with nothing to come around; how often the freeze works, and what the position was worth to the team that left it.
- **The tuck and the runback**: a stone tucked behind an opponent's, by how far behind, and how often it is run back.

---

## Part IV. Contributing, open questions and status

## 16. Contributing

The project is built to grow in three directions, and each has a place to start.

**Data.** The corpus is international championship curling from the World Curling results books. The single most useful contribution is more games in shot-by-shot form: national championships (the Brier and the Scotties above all), the Grand Slams, and World Curling Tour events, then anything else with the stones recorded after every shot. A source enters through an adapter that writes the six tables of Section 2.6; a source that is itself a results-book PDF in the CURLIT format needs nothing but the file. Line scores alone are useful too: they feed the win-probability table. If you hold or know of such data, open an issue on the repository.

**Points Gained.** The expectation models are gradient-boosted trees on hand-built features and configurations, trained with a local target, and the evaluation harness is in place: `pointsgained experiment` fits a variant on a time split or a held-out-book fold and scores it on log-loss against the end's result and on the front-end gates (Section 7.6). Section 17 lists the known weaknesses; the positions the model misprices (the peel miss when the hammer team must score, the tight guard on a lonely steal stone, two stones in the house that are not split) are concrete targets, and the scenario probes are their tests.

**Studies.** Every study in Part III reads the same tables: `points_gained.parquet` (one row per stone, with the three outcome distributions, both currencies, the call and execution split, the thrower and the situation), `configurations.parquet` (the labels and measures of every position), the per-book extraction tables, and the feature cache. `model/frontend.py` is a worked example of a study module. The strategic situations of Section 15 are open; a study that matches on the score, ends remaining and position and compares the choices is the natural next contribution, and finished reports belong in `reports/samples/` with a line in its README.

---

## 17. Open Questions

Resolved in Phase 1: outcome clipping at ±3; full shot types without grouping; men and women pooled with a discipline flag; canonical perspective; recorded score as label; gates as set in Section 2.3; the event tier table; raster before set encoding for the geometry model.

Resolved in the modelling phase: the game-state encoding for f and g is the raw pair (score difference, ends remaining) plus an extra-end flag (Section 7.7); evaluation by time (train through 2024, test 2025–2026) runs alongside the by-book split for every experiment; level of play is the strength of the *event*, hand-rated (Section 7.4); no per-player skill and no grade enters f or g; per-book and per-player values never enter as columns; player identity is a normalised name key per discipline with an alias table (`data/player_aliases.csv`: 31 confirmed pairs such as SCHWARZ B → SCHWARZ-VAN BERKEL, 23 to check, 7 rejected because both names appear in one book); the skill scalar is per player with the team effect as its prior, pooled across seasons for now.

Open:

1. **Event ratings.** The ratings in `data/event_strength.csv` are tier defaults (Worlds 100, Europeans A 85, juniors 70). The derived field strengths already disagree with them in places: the Olympics sit above the Worlds, the Olympic qualifiers and the Pan-Continental championships well below Europeans A.
2. **Event effect granularity.** Event first; sheet and session with shrinkage once the model-level effect exists.
3. **Skill scalar granularity.** Per player with a team-level prior, falling back to team for players with few shots.
4. **Free guard zone eras.** Pooled with an era flag versus per-era f in early-end positions. Only f is affected; g pools across eras.
5. **Player identity.** An alias table for name changes and a stable player id across events.
6. **Leverage-normalised consistency.** Execution divided by the width of the call's menu, so that steadiness is comparable across positions.
7. **Aggressiveness as the shape of the accepted distribution.** The tail hypothesis of Section 10.3 needs validating and then a report: per call, the upside and the downside of D(S | C); per team and per skip, how much downside they accept relative to the field in the same situation, and how much of it they produce. This is the analysis-phase form of the second task in Section 5, capturing the upper end of the outcome distribution.
8. **Situation-specific configurations the trees cannot carve out.** The peel miss in a tied last end (276 ends) and the tight guard on a lonely steal stone (Section 13.4, about 400 ends each) are priced wrongly; both are rarer than the trees' minimum leaf. A targeted feature (guards remaining when the hammer team must score; the runback distance on a lonely steal) or a situation-weighted correction are the candidates.
9. **The front end's shared component.** A team's lead and second values move together (0.64, 0.36 after the team's call and configuration mix) and not with the fourth's. Sweeping, ice reading, the skip's broom or style; the corpus cannot separate them directly, but the component's relation to results can be measured.
10. **Selection in difficulty tables.** Make rates by geometry measure shots as chosen (Section 12.2). The call rate from every position where a shot was available, from the configuration table, is the correction.
11. **Conservation.** One end (2014 World Championship bronze-medal game, end 5, stones 9 and 10 missing from the book) breaks the identity by 0.076 in the current table because a rebuilt post position took the pre-shot configuration columns; fixed in the code, exact from the next refit.

---

## 18. Status

Built and run, September 2026:

| Milestone | State |
|---|---|
| M1 Ingestion (decoder, detector, text parser, assembly, gates, audit) | Done; 92 books validated, all templates 2014–2026 |
| M2 Core (count function, canonical positions, mirroring) | Done |
| M3 Value mappings, baseline models, Points Gained, reports | Done; f 1.494 / g 1.472 / trivial 1.593 held out by book |
| M4 Archive (inventory, download, survey, parallel batch) | Done; 208 books downloaded, 116 line-score only |
| M6 Plumbing: feature cache, vectorised build and PG, experiment command | Done; full pipeline 2.5 h to 17 min, identical results |
| M7 Game situation in f and g | Done; f 1.470 / g 1.453 / trivial 1.559 held out by book |
| M8 Difficulty model (skill scalar, event effect) built as a report; g takes the event rating | Done; per-player input withdrawn (Section 7.4) |
| M9 Intent from the delivered stone; target model; ring detector for 2016–2019 | Done; g 1.4373 → 1.4325 on the time split without level, 1.4311 with the event rating |
| M10 Raster geometry model, probe and monotonicity gates | Built and rejected: plain raster f 1.493, hybrid 1.487, trees 1.455 on the time split |
| M11 Configurations, the front-end study, local targets | Done; adopted `config` + local:2, CV f 1.4677 / g 1.4457; see-saw removed |
| M12 Studies: geometry by level, high-value-shot leaderboards, the setup battle report, strategic situations | Next |
| M13 Phase 2 | After M12 |

**September 2026.** The project is organised as a system for others to build on: the ingestion pipeline and corpus (Part I), Points Gained as the general expectation tool (Part II), and sample studies built on both (Part III), with contributions invited in all three (Section 16), more game data above all. The adopted expectation model adds the configuration labels and the local target (M11). The next milestone is studies: the geometry tables by level, leaderboards for high-value shots, the setup-battle report per team and lead, and the strategic situations of Section 15.

**At the end of the modelling phase (2026-09-10)**, before the configurations and the local target, the system was: f and g as boosted trees on the position features, the game situation, the event rating and, for g, the call type, turn and the struck stone; held out by book, f 1.470 and g 1.447 against a trivial 1.559; the full pipeline in about fifteen minutes; per-event reports with execution first in both currencies. Mike Calcagno's suggestion for what follows (2026-09-10): the metric is outcome-first. Execution (PG: Throw) is the primary pivot in both currencies, with the tail statistics of Section 10 (floor, reliability, big misses, the five costliest shots) alongside it in points and in win probability; the call component is reported second, and no further work goes into intent. Skips call plan B and plan C while the rock is moving, and the position they leave is what the metric should credit. The five last-rock hit calls the model rates worst at the 2026 Olympics and Jacobs' ninth-end clearing are the pinned test set (`pointsgained testset`) for all three.
