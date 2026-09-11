# Points Gained: A Shot-Value Metric for Curling — Design Document

**Status:** Phase 1 built and run on the full CURLIT archive, then a modelling phase that added the game situation, the event's level of play and the struck stone to the models, tried and rejected a raw-geometry network, and settled the reporting on execution first (September 2026). This document describes the system as it exists, the reasoning behind its choices, what was tried and withdrawn, and what the results say. Section 13 records status.

**Scope:** Within-end valuation in two currencies, hammer-adjusted points and win probability, with call and throw components, computed for 609,014 shots from 92 World Curling results books. The models are boosted trees on hand-built features plus the game situation, the event's strength rating and the struck stone; a raw-geometry network was built and lost to them (Section 5.2), and a per-thrower skill scalar was built and withdrawn as an input (Section 3.5).

---

## 1. Goal

Assign every shot a value, **Points Gained (PG)**, that measures how much it changed the expected scoring of the end, from the throwing team's point of view. The name is chosen by analogy with strokes gained in golf: it is measured against the field, it is additive, and it decomposes. Two properties are required:

1. **Situation-aware.** A made draw against an opponent stone in the four-foot is worth more than the same draw into an empty house, because the expectation before the shot was lower.
2. **Conserved.** The values of all shots in an end sum to the final score minus the expected score at the start of the end. No credit is created or lost.

The output is a per-shot Points Gained, decomposable into **PG: Call** (selection: what the call was worth) and **PG: Throw** (execution: what the throw delivered against the call).

### 1.1 Philosophy

Every shot in curling has two parts. First a call is made, by the skip and often with the whole team, and the call sets up a menu of possible outcomes with their odds: the roll-out that blanks, the stick that scores one, the miss that gives up a point, the flash that gives up two. Then the shot is thrown, swept and called on line, and one outcome from that menu happens. The call is a decision; the throw is an event, and what can be judged is its effect against the menu the call created.

The model evaluates every rock in both dimensions. Selection asks what the call's menu was worth compared with the position the team was handed. Execution asks what the throw produced compared with the menu the throw was handed. Neither is judged by the other: the execution value does not penalise a poor call or reward a brilliant one, and the selection value does not credit a lucky throw or blame a bad one. A call reads the same on a make and on a miss. The two components sum to the shot's total contribution to the end.

The best calls create menus whose expectation, weighted by how *this* team executes, is highest relative to the position. That is not always the menu with the biggest upside, and the right trade-off depends on who is throwing. The clearest example in the data is Brad Jacobs' last rock in the ninth end of the 2026 Olympic final: down one with hammer, he called a runback through traffic that scored three and decided the gold medal. Against the field's usual call from that position, a draw, the type-only model priced the call at −16.7 percentage points of win probability and the throw at +31.9; with the struck stone as part of the call (Section 6) it is −5.7 and +22.7. That is not a verdict that the call was wrong. It says the field does not call that shot, because for the median skip it is a poor menu; whether it was the right menu for Jacobs is a question about geometry (was the shot there?) and about level of play (how often does he make it?), and answering it properly is what Sections 5.2 and 3.5 are for.

### 1.2 Strategy: how game situation enters

Within an end the structure is recursive. Every shot before the last one builds a **position**, every position carries an **outcome distribution** (the chances of blanking, scoring one, scoring two, giving up one, and so on), and the last rock realises one outcome from it. The rock before the last is thrown to make that distribution as bad as possible for the thrower of the last rock; the rock before that, to make it as good as possible two rocks down the line; and so on back to the first stone. The two teams are pulling on the same quantity in opposite directions, which is exact rather than approximate: whatever currency an outcome is valued in, the opponent's value is the negation.

Strategy is the observation that not all outcome distributions are equally useful, and which ones are useful depends on the game. Curlers have a vocabulary for this: *must steal*, *force one*, *two or blank*, *don't give up more than two*, *score or go to the extra end*. In this model those goals are not a separate layer and are not enumerated by hand. They are the *shape* of the value mapping v(outcome | game situation): tied in the last end with hammer, one and two are both worth a win, a blank is worth the chance of winning an extra end with hammer, and a steal is worth nothing, and maximising expected value under that shape simply *is* "score or don't get stolen on." The win-probability table (Section 9.4) generates every one of the named strategies as a consequence.

The two currencies disagree in a way that is itself informative. In hammer-adjusted points, a team protecting a three-point lead reads as calling badly, because points reward aggression whatever the game; in win probability the same calls are neutral. On the four development books, the strongest teams' call values were slightly negative in points and zero in win probability for exactly this reason: they are ahead more often. Rachel Homan's raise with her last rock in the eighth end against Italy at the 2026 Olympics, up two with three ends to play, costs 0.12 points but only 0.4 percentage points of win probability; the game barely depended on that end. Both currencies are kept, and reports say which one they are in.

### 1.3 Terminology

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
| **Skill scalar** | A per-thrower level-of-play number estimated from execution grades. Built as a report (Section 3.5); not an input to the models, whose level of play is the event's. |

---

## 2. Framework

### 2.1 Definitions

- **S**: the pre-shot **position** (stones on the ice, rocks remaining, rule era) in the canonical frame of Section 2.4.
- **C**: the called shot (the shot type as recorded).
- **S′**: the post-shot position.
- **D(S)**: the **outcome distribution**: a probability distribution over end outcomes given position S, over {−3, −2, −1, blank, +1, +2, +3} from the hammer team's perspective, with larger scores folded into ±3.
- **V(D)**: a scalar value of an outcome distribution: Σ D(o) · v(o). Swapping v is a one-line change and both currencies are computed for every shot.

### 2.2 Points Gained

    PG(S, C, S′) = V(D(S′)) − V(D(S))

For the last shot of an end, D(S′) is a point mass on the actual result, so this reduces to actual minus expected.

### 2.3 Decomposition

Insert the called shot as an intermediate baseline:

    PG: Throw (execution) = V(D(S′))    − V(D(S | C))
    PG: Call  (selection) = V(D(S | C)) − V(D(S))

Execution measures how the result compares with what that call usually produces; selection measures what the call was worth relative to the position, under the field baseline: D(S) is the outcome distribution under the observed shot-selection policy of the field, so selection reads as "better or worse than the field would call." The best-call baseline of Phase 2 replaces D(S) with the best available menu and reads as regret.

Two of Homan's shots at the 2026 Olympics show the split doing its job. In the fifth end against Sweden, up two without hammer with six ends left, she called a double with the fifteenth rock and missed; Sweden scored three. The call is worth −0.16 points and −2.2 percentage points of win probability against the field's usual call from there, and the throw −0.83 points: a call the field would not make, then a miss. In the seventh end against Switzerland, up three with four to play, she called a take-out and missed; Switzerland scored four. That call is worth +0.02 points, at or above the field's, and the whole cost (−0.79 points) is execution. Same player, same week, same-sized disasters, different diagnoses.

### 2.4 Perspective convention

Every physical position is evaluated **once**, from a canonical perspective: the team holding hammer in the current end. Stones are labelled `hammer` / `non_hammer`, and f is fitted and evaluated only in this frame. A thrower's value is V from the canonical frame, multiplied by +1 if the thrower holds hammer and −1 otherwise.

This is deliberate rather than cosmetic. If f were evaluated from the thrower's perspective, the same physical position would be evaluated twice, once for the team that just threw and once for the team about to throw, and a learned model is not exactly antisymmetric under the swap, so the sum of Points Gained over an end would not telescope. With a single canonical evaluation per position the identity in Section 2.5 holds by construction. Who throws next is determined by the parity of rocks remaining.

### 2.5 Conservation check

With D(final position) defined as the actual score, summing canonical Points Gained over the shots of an end gives

    Σ PG = actual_score − V(D(S₀))

where S₀ is the empty-sheet position at the start of the end. On the full archive the largest residual over 37,585 ends is 9 × 10⁻¹⁶. It is a unit test, not a diagnostic.

---

## 3. Data

### 3.1 Source and coverage

The corpus is the CURLIT results-book directory at `curlit.com/results`: one PDF per World Curling event, with a shot-by-shot page for every end of every game in the events that have them. The directory lists 310 Results Books; 208 are team-of-four men's or women's books from 2013 onward and in scope. All 208 were downloaded (2.3 GB). Only 92 contain shot-by-shot pages: 25 tier 1, 42 tier 2, 23 tier 3, 2 tier 4. The other 116 (Europeans B and C, Seniors, Junior-B, Pan Continental B, the qualifiers and the Universiade) are line scores and standings only; they still feed the win-probability table.

| | Count |
|---|---|
| Books with shot-by-shot pages | 92 |
| Games | 4,150 |
| Ends | 38,163 |
| Shots | 609,014 |
| Stone positions | about 3 million |
| Line-score team rows (all books) | 3,078 |

So the shot-level corpus is roughly 600,000 shots rather than the 1.5 to 2 million estimated before the archive was surveyed, concentrated in the Olympics, the World Championships, the Europeans A-Division, the Pan Continental A-Division and the World Juniors. Some junior books carry shot-by-shot pages only for the playoffs.

Jordan Myslik's earlier extraction (`jwmyslik/curling-analytics`) is the precedent for this work. It could not be rerun: its source host no longer exists and its parser depended on rendered page images. Nothing here depends on it.

### 3.2 Tables

Extraction writes six Parquet tables per book, with the book, page and panel of every row as provenance.

| Table | Content |
|---|---|
| `games` | Book, discipline, date, start time, session, sheet, the two team codes and names, their colours, report code |
| `ends` | Per end: running score before and after for both teams, this end's score, conceded flag, hammer team (inferred), Total Score and Time left box, colour source |
| `shots` | Per shot (1–16): team, colour, player, shot type, turn, grade (raw and 0–100), note line, stone counters (remaining and removed per colour), stones detected per colour, delivered-stone colour, orientation flag |
| `stones` | Per stone per shot: colour, pixel and inch coordinates, delivered flag, and prior-position rings as separate rows |
| `line_scores` | From the Game Results pages: per team, last-stone-first-end flag, score per end, extra ends, total |
| `players` | From the Game Results pages: position, function (skip / vice), game and cumulative percentage |

The `turn` field is kept: it is free, it matters for in-turn versus out-turn execution modelling, and mirroring (Section 4) must flip it.

### 3.3 What the diagrams are and what they carry

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
- **Resolution limit.** The count function (Section 5.3) applied to the final position agrees with the recorded end score in 96 to 98% of ends in recent books and about 89% in 2014–2017 books. The disagreements are stones within an inch of each other or of the twelve-foot edge, which a 0.61 in/px diagram cannot resolve and which were measured on the ice; sweeping the biting radius does not improve agreement. The recorded score is therefore the label and the reconstruction is the gate.

### 3.4 Strata labels

Every row carries stratum keys so that models and reports can be re-cut without re-running the pipeline: discipline (from the page header), event family and tier (from a regex table over event names, the single place tiers are defined), season and rule era (from the date), team code, player name, throwing position (from shot order), session and sheet.

Player names need care. The books use surname plus initial, in varying case, and a player's team code changes between events (Scotland at the Worlds, Great Britain at the Olympics); reports key on the upper-cased, whitespace-normalised name within a discipline. Genuine name changes ("SCHWARZ B" in 2022, "SCHWARZ-VAN BERKEL" from 2025) are handled by an alias table (`data/player_aliases.csv`, Section 12).

### 3.5 Level of play

A six-foot double is worth less to an elite team than to a club team because the elite team makes it more often: D(S | C) is higher, so the PG: Throw for making it is smaller. Level of play is a property of the **execution distribution** and enters through g.

The archive shows the effect plainly. Execution value per shot, measured against the whole field, is about 0.040 points at tier 1, 0.030 at tier 2 and 0.019 at tier 3, in both disciplines. Today the only level input is the tier and discipline of the event, so a junior's execution is measured against a field that is mostly Olympians, and junior leaderboards are meaningful only within their own event.

The remedy is the **shot-difficulty model** on the official grade, built in the modelling phase. Stage one is a gradient-boosted regression of the grade (0, 25, 50, 75, 100, the same scale in every book since 2013) on the shot's difficulty: type, turn, the position features, rocks remaining, situation and discipline. Stage two is a fractional logistic regression on the stage-one logit with two event-level covariates, the hand-rated **event strength** (`data/event_strength.csv`, men's Worlds = 100) and a **field strength** derived from game results (the mean Bradley–Terry strength of the teams in the book, fitted leaving that book out), plus L2-shrunk effects for team, player and book. Level of play is a property of the *event*: who is in it says how strong it is, and a player's grades are read against the fields they played in. Team rankings inform how strong a field is; they are not a per-player input.

Out of that come two numbers. The **skill scalar** per player (team effect plus shrunk player deviation, in logit units) ranges from about −1.2 to +0.9; Jacobs, Kennedy, Gushue and Sundgren head the men, McEwen and Homan the women, and Chinese Taipei, Australia and Lithuania fill the bottom. The **event effect** per book is what remains once field strength is accounted for: ice, conditions, and the grader, since the grade is a judgement (the 2026 junior men's book sits 0.6 logit above the rest, which is at least partly leniency).

**How it enters g.** Not as the raw numbers. Per-player and per-book values identify the player and the book, and a tree fits book-specific outcome rates on them that do not transfer: with `skill` and `event effect` as columns, g got *worse* out of book (1.4373 to 1.4407 log-loss on the time split). What g takes is the **expected grade of this shot for this thrower** at this event, sigmoid(difficulty + skill), a single continuous number. With it g improves from 1.4373 to 1.4297 on the time split and from 1.4426 to 1.4366 by book, about half the size of the call's own contribution over f. The signal is plainly in the data: on last-rock draws with the hammer team not lying shot, the scoring rate rises from 54% to 78% across skill quartiles.

**Then set aside.** Mike's objection, and the decision: strokes gained does not evaluate a fairway shot against Tiger Woods' putting, it evaluates it against a tour professional's. Level of play belongs to the *field*, never to the player being measured, and the grade is a judgement whose leniency varies by grader, so it is a poor thing to rate players on. So the per-player expected grade was built, measured, and withdrawn as an input. What g takes as `level` is the **event's strength rating** alone (`data/event_strength.csv`, men's Worlds = 100), a handful of distinct values that cannot identify a book. On the time split it keeps part of the gain (g 1.4325 without any level, 1.4311 with the event rating, 1.4278 with the rejected per-player grade) at no cost in identity. The difficulty model remains as a report (`pointsgained difficulty`: skill leaderboards, event effects, the field strengths next to the ratings) and as the error scale for the Phase 2 transition model; it is not an input to f or g, and Points Gained have a single decomposition again.

### 3.6 Pipeline

**Inventory.** `pointsgained inventory --check` fetches the directory page, which is plain HTML with direct PDF links, classifies each book by event family, tier and discipline, and HEAD-checks every in-scope link. Mixed doubles, wheelchair, mixed-team and youth books are out of scope.

**Download.** `pointsgained download` fetches in-scope books sequentially with a delay, resuming from disk.

**Survey and extraction.** `pointsgained batch` runs, per book and in parallel: a survey (does it have shot-by-shot pages; which template, grade style and image format), extraction, and validation, and writes the gate results back to the inventory. Books without shot-by-shot pages are marked excluded.

**Validation gates.** A book is `validated` when the stone census holds in at least 95% of panels, score reconstruction agrees with the recorded score in at least 85% of ends, hammer alternation is violated in at most 1% of ends, and at least one game was found. The thresholds are set to catch extraction failures, which show up as agreement rates near 50 to 60%, while admitting the older books' higher rate of inch-level ties. Every book with shot-by-shot pages passed.

**Audit.** `pointsgained audit` draws random panels with detected stones, delivered marker and prior rings overlaid onto a contact sheet.

**Storage.** Raw PDFs by year; Parquet tables per book; the inventory CSV as manifest; nothing enters training that is not validated and in scope.

---

## 4. Preprocessing

1. Convert coordinates to inches and rotate alternate ends into the thrower's frame.
2. For each shot, assemble the pre-position (after the previous shot; empty for shot 1) and the post-position.
3. Determine hammer from shot order (the team throwing shot 1 does not have hammer) and check alternation against the recorded scores.
4. Attach the recorded end score as the label; conceded ends carry none.
5. Assign rule era: four-rock free guard zone before the 2018–19 season, five-rock after.
6. Relabel stones `hammer` / `non_hammer` (Section 2.4) and record whether the thrower holds hammer.
7. Mirror every position left-right at training time (labels unchanged, turn flipped).
8. Attach stratum keys.

---

## 5. Position Representation

### 5.1 Principles

The subtleties that decide a curling position live at the inch level: whether a double is on, where a roll ends up, whether a guard actually covers the line. Any hand-built classification of positions throws that away. Two representations with different jobs:

- **Raw geometry (built, rejected).** The model sees the stones themselves; whatever matters is learned from outcomes. A convolutional network on the rasterised sheet was trained and lost to the feature model in every band of rocks remaining (Section 5.2).
- **Baseline features (the model).** A compact hand-built vector: originally a baseline to beat and an interpretability layer, now the representation the system runs on. No claim is made that these features capture what a skip evaluates; the results in Section 7 say the models, on either representation, know little early in an end.

### 5.2 Raw geometry representation

A position is a set of up to 16 stones, each (x, y, owner) in inches, plus rocks remaining and rule era. Two encodings were planned: a **raster** (the play area as an image fed to a small convolutional network) and a **set** encoding (a permutation-invariant network over stones). The raster was built in the modelling phase: 171 by 325 pixels at one inch per pixel (the full sheet width, from the back line to the hog line), two channels (hammer team, opponent) with stones as filled discs, a third channel marking the intent target for g, rasterised on the Apple GPU per batch from the stone arrays, with mirroring as a training-time augmentation. Two lessons from making it learn at all: the sheet is anchored at the pin, so the network needs *coordinate channels* and must not end in global pooling, which made it blind to location; and a wide flattened head memorises positions (training loss 1.34 against validation 1.63 in three epochs), so a 1×1 bottleneck to eight channels and heavy dropout are needed before the dense layer (293k parameters in all).

**Result (f, time split, five epochs, about 45 minutes on the M3 Pro).** Log-loss 1.493 against 1.455 for the trees, and worse in every band of rocks remaining, including the early end (1.594 against 1.584 at twelve left, 1.644 against 1.627 at sixteen) where the hand features were supposed to be blind. It passes the monotonicity checks of Section 7.5 at 100% where the trees fail one of them: the trees *raise* the hammer team's value when an opponent stone appears inside its shot rock in 22% of synthetic cases, a flaw the geometry model does not have. A hybrid, the same network with the 28 hand features fed to its dense layer, was the last test of whether raw geometry adds anything on top of the features: 1.487, again worse than the trees in every band, and it recovered only part of the monotonicity result (68% on the steal case). A dense layer on tabular features loses to boosted trees on the same features, and the raster path did not add enough to close that gap, let alone overtake. The trees remain the model. What the exercise leaves behind is the rasteriser and training loop (`pointsgained raster`), the probe and monotonicity gates, and one finding about the trees themselves. The set encoding was not built.

### 5.3 Count function

Sort all stones by distance from the pin; a stone is in the house if that distance is at most 72 inches plus the stone radius (5.7 in). The team owning the closest in-house stone scores the number of its in-house stones closer than the nearest in-house opposing stone; an empty house is a blank. Exact, not a judgment; used for terminal positions and as the reconstruction gate.

### 5.4 Baseline feature set

Twenty-eight numbers per position, in the canonical frame ("own" means the hammer team):

- **Situation:** rocks remaining (whose parity says who throws next), rule era, stones in play.
- **Lie:** count (clipped ±3), shot-rock ring, margin (inches between the shot rock and the first opposing stone), owners of the second and third stones, boundary gap (inches between the last counting stone and the first opposing stone) and a near-tie flag (boundary gap under two inches).
- **House occupancy:** own and opposing stones in the house and behind the tee.
- **Guards:** counts per team by lane (left, centre, right; centre is |x| ≤ 24 in) and the depth of the nearest centre guard.
- **Cover (crude):** shot rock covered, button covered, by a straight-line corridor test. Known to be wrong at the margins.
- **Nearest stone** distance per team.

**Near-tie positions.** Stones within about two inches at the ownership boundary are tied on the sheet and unresolvable in the data; these are the ends where reconstruction disagrees with the recorded score. They are a real game state rather than noise: the skip cannot tell which rock is second either, and the call made there (peel, freeze, play for the measure, draw for the sure one) is a strategic response to that uncertainty. D stays a full distribution rather than collapsing on the count, the count function is never ground truth for those ends, and the baseline names the state so that calls in tied positions can be studied.

---

## 6. Called Shot and Intent

The `type` field records the call: Draw, Take-out, Hit and Roll, Guard, Front, Freeze, Raise, Clearing, Double Take-out, Promotion Take-out, Wick / Soft Peeling, Through. Phase 1 uses it as recorded. The type leaves the target ambiguous, and the consequence is visible in the results: a call component an order of magnitude smaller than the throw component, and call verdicts that judge the *family* of shot rather than the shot. Every one of the five "worst calls" of the 2026 men's Olympic tournament by win probability is a last-rock runback or double that the field usually does not play from that position, and three of the five were made and won the end. The model can see that runbacks are usually a worse menu; it cannot see that this runback was on.

The delivered-stone marker (Section 3.3) is the way forward, and the modelling phase built it with one rule that matters more than the rest: **the call must never be read from the outcome.** On a made draw the delivered stone's rest is the target; on a missed draw it is the miss, and on the last rock it is the score. The first attempt used the rest for every draw and cut g's log-loss from 1.430 to 1.415 on the time split, almost all of it at one rock left (0.815 to 0.658): execution had leaked into the call. Gating the rest on the grade did not help, because a flag saying "the target is known" then meant "the draw was made".

What g takes instead (feature set `intent`):

- **Draws** (Draw, Guard, Front, Freeze, Through): the *modal* target from a target model P(target cell | position, call), fitted on made draws with a marker (out of fold by book) and applied to every draw whatever its grade. The cells are three lanes (centre is |x| ≤ 24 in) by six depth bands from through the house to the far guard zone. On made draws the modal cell agrees with the realised one about 56% of the time; the rest is the spread the field's targets have from a given position. Because it is a function of position and call only, it cannot leak, and it adds little: the tree could read the same thing from the position. Its value is as the field's menu for Phase 2.
- **Hits** (Take-out, Hit and Roll, Double, Clearing, Raise, Promotion, Wick): the **struck stone**, the prior-position ring furthest up the sheet (the shooter arrives from the hog line), at any grade: which stone was hit is intent, not outcome. Its columns are the pre-shot position (x, y), owner, ring, whether it was the shot rock and whether it was a guard. Without rings, the modal struck-stone class from a second target model.
- Whether the shooter stayed and whether the target was realised are kept for diagnostics and the Phase 2 error model but are not columns of g.

With that rule the gain is honest and modest: g from 1.4297 to 1.4278 on the time split, from 1.4366 to 1.4342 by book and from 1.447 to 1.444 in the five-fold cross-validation, every band of rocks remaining slightly better, the last rock most (0.815 to 0.796). The information is in the hits. What changes more than the log-loss is the call component: its mean absolute size per shot is now 0.064 points against 0.137 for execution, about half rather than a tenth, and it is largest on the hit family (0.07 to 0.10 on take-outs, doubles, raises and promotions). On the six-shot test set (Section 13) the made runbacks moved the way they should: Jacobs' ninth-end call from −12.0 to −5.7 percentage points of win probability, Retornaz's tied-last-end promotion from −3.7 to +9.7, Muskatewitz's raise from −8.1 to +8.2; Casper's two moved to about neutral (−0.2 and −1.1), and Schwarz-van Berkel's missed clearing got worse as a call (−2.2 to −7.4). These are the final model's numbers, with the event rating and no per-player input (Section 3.5). The rings were missing from the 2016–2019 books because those templates draw them two pixels thick in the moved stone's colour; a second ring rule in the detector recovered them, and those thirty books were re-extracted. The Through / Draw distinction on a last rock with an empty house remains the blank-versus-score decision and is handled by the type alone.

---

## 7. Phase 1: Direct Outcome Models

### 7.1 Insight

Every shot's pre-position is labelled with the end's final outcome. Sparsity of exact positions does not matter once the model can generalise across positions. The outcomes are high-variance per example, but that variance is what the model averages over. This is a supervised problem, not a dynamic-programming problem, and it is deliberately outcomes-biased: it says what positions and calls have been worth given how the field has played, not what they should be worth under optimal play.

### 7.2 Models

- **f(S) → D**: distribution over end outcomes from the position, in the canonical frame. This is D(S) under the field baseline.
- **g(S, C) → D**: the same with the called shot type and turn as inputs. This is D(S | C).

Both are gradient-boosted tree classifiers over seven outcome classes on the Section 5.4 features plus discipline and, since the modelling phase, the **game situation**: the hammer team's score difference (clipped at ±6), ends remaining (clipped at 10) and an extra-end flag. Situation in f changes what D(S) means, from "what this position is worth under typical play" to "what it is worth given how teams play from here in this situation": up three in the ninth, the field runs the end clean, and f now expects that rather than scoring the blank as a failure. The value mapping still carries the situation in the win-probability currency (Section 9.3); the two uses are complementary and the conservation identity is unaffected because V is fixed within an end. Neither model takes an event effect or a skill input yet (Sections 3.5 and 8).

Feature sets are named (`base`, `situation`, `call`, `level`, `intent`) so that an experiment can toggle them, and the training table is cached once per corpus, so a single-split experiment on 1.2 million rows takes about a hundred seconds and the full pipeline about seventeen minutes.

**Regularisation was the whole story on the small corpus.** On four books, about 2,900 labelled ends, the model had to be held to eight leaves, 300 samples per leaf and 60 to 80 boosting rounds to beat the trivial model (rocks remaining, hammer, count) on held-out books; anything richer lost to it. On the archive the plateau is 15 leaves and 200 rounds: 31 leaves and 300 rounds score the same at twenty-five times the cost, 63 leaves are worse. Points Gained are always computed from out-of-fold predictions, so no position is valued by a model that saw its book.

### 7.3 Results

Held out by book on the full archive, five folds, with and without the game situation:

| Model | Log-loss (base) | Log-loss (with situation) | Brier (with situation) |
|---|---|---|---|
| Trivial (rocks remaining, hammer, count; plus situation) | 1.593 | 1.559 | 0.742 |
| f (position features) | 1.494 | 1.470 | 0.708 |
| g (position and call) | 1.472 | 1.453 | 0.701 |
| g with the struck stone (Section 6) and the event rating (Section 3.5) | | 1.447 | 0.699 |
| *rejected:* g with the per-player expected grade | | 1.447 | 0.699 |
| *rejected:* g with the per-player expected grade and the struck stone | | 1.444 | 0.698 |

On the time split (train through 2024, test on the 2025 and 2026 events, 219,000 held-out rows) the same story: f 1.477 to 1.454 and g 1.455 to 1.437. The situation helps in every band of rocks remaining and in every score-difference band, most at tied scores (1.403 to 1.366 on the time split), where ends remaining decides whether the end is "two or blank" or "must score". It was adopted on that evidence (experiment log in `reports/experiments/`). The regime label and the v-vector as alternative encodings were not needed.

The gain over the trivial model is real and its location is the important finding. With one rock left the features cut log-loss from 1.23 to 0.94; with four left, from 1.51 to 1.38; with twelve or more left, by 0.04 or less. The model knows what a position is worth once the end is nearly decided and knows almost nothing early. Since tree capacity no longer matters, this is the hand-built features' limit rather than the data's: the geometry a skip reads in the first eight rocks is not in the twenty-eight numbers. It is the case for the raw-geometry model.

The situation also removed most of the reporting artefact of Section 1.2. In hammer-adjusted points the hammer team's call value when up three or more was −0.026 per shot before and is −0.014 after; the non-hammer team's when down three or more went from −0.025 to −0.011, and its execution value in that state from −0.029 to +0.005. What remains is the residual that only the win-probability currency removes.

Two consequences for the reports. Execution values early in an end are noise around a flat baseline, so leaderboards are effectively about the last six rocks of each end. And the call component is small (about 0.005 points per shot against 0.05 for execution) because the call is a type.

### 7.4 Training set construction

One row per shot for f, with the pre-position and the end's outcome from the hammer team's perspective; one per shot for g with the call. Mirrored rows are added. Conceded ends and books that failed the gates are excluded. Held-out splits are by book, never by shot or end.

### 7.5 Validation

- Held-out log-loss and Brier score against the trivial model, overall and by rocks remaining; calibration by outcome class.
- Conservation to numerical precision (Section 2.5).
- Calibration at the empty sheet: V(f(S₀)) with hammer should equal H. On the archive, 0.582 against 0.582.
- Face validity of the leaderboards against the game (Section 10).
- For the raw-geometry model, the **subtlety probe** (built in `pointsgained raster`, not run: the geometry model failed the log-loss gate on f, so g was never trained): take real positions where a double was made, translate the target stone by ±1, ±2, ±4 inches, and plot g(S, Double) against the offset. A model that has learned the geometry shows a sharp drop where the double closes; a model that has not shows a flat line.

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

**Outcome first.** Execution, PG: Throw, is the primary pivot in both currencies. It is the part of the shot's value that does not depend on reading the skip's mind, and it credits what curlers credit: the position left, whatever the scorer wrote down. A hit that ticks a guard through a port and improves the position is a miss on the sheet and a gain here; a skip who calls plan B while the rock is moving gets the position that plan B produced. The tail columns below are reported in points and again in win probability (`floor10_wp`, `big_misses_wp` counting shots that cost five or more points of win probability, `worst5_wp`), because a costly miss in a decided game and one in a tied last end are different events. The call component is reported after execution, and its fairness to an elite skip is a secondary concern (Section 6).

**Consistency.** Variance is mostly the leverage of the position, not the person, and a symmetric spread treats the gambler and the choker alike. Two positive-is-good numbers are reported instead: the **floor**, the tenth percentile of event-relative execution ("on a bad day this cost this much"), and **reliability**, the share of shots at or above the field's expectation for that shot type and hammer state. A leverage-free version, execution divided by the width of the call's menu, is a next step.

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

- **Model report:** corpus counts, the hammer distribution, N and H by discipline, held-out log-loss by model and by rocks remaining, conservation and calibration, win-probability examples, leaderboards by player, team and shot type.
- **Strata:** by discipline and tier, by hammer, by game state and hammer, by shot type and hammer, players relative to the field, teams by hammer; all in both currencies.
- **Per-event leaderboards** (`pointsgained events`): one row per player and event with position, shots, games, event-relative execution (median and mean), variability, floor, reliability, big misses and makes, worst five, slot-relative execution, call value, win-probability execution, and the official grade.

Every per-shot value is a difference of model outputs, so these tables are exactly reproducible from the Parquet tables and the fitted models.

---

## 11. Phase 2: Physics, Transitions, and the Best Call

Phase 1 answers "what has this been worth." Phase 2 answers "what could this have been worth," which needs counterfactual calls, and therefore a model of what happens when a shot is thrown.

- **Simulator.** Collision geometry, rolls, raises and runbacks are deterministic physics; the Digital Curling platform and similar simulators implement them. A simulator answers the inch-level questions the raw-geometry model has to learn statistically: is the double on, where does the shooter roll, does the raise reach.
- **Execution error model.** The only stochastic component. Learned from the delivered-stone marker: for each (type, inferred target, skill scalar, event effect), the distribution of where the thrown stone arrived relative to the target. Seeded in the modelling phase: `pointsgained intent` writes the delivered stone's rest relative to the modal target for every draw with a marker, by grade, skill tercile and rocks-remaining band (`reports/execution_error.md`). On late-end draws graded 100% the median lateral error is about 8 in and the depth interquartile range about 27 in, part of which is the target cell's coarseness; at 75% the depth spread is 41 in.
- **Transition model.** P(S′ | S, call) = simulator applied to the call with delivery sampled from the error model. It replaces the crude cover features of Section 5.4 with simulated shot-availability probabilities.
- **Rollouts.** From any position, simulate the remainder of the end under a policy, initially the empirical policy P(C | S, situation), evaluating with f at a fixed depth. When the policy is replaced by an optimising one, there is a single objective for both teams, since v is zero-sum, and the named strategies emerge from the shape of v.
- **Best-call baseline.** For each position, evaluate each candidate call by rollout and take the maximum; selection under this baseline is the regret of the call made. The best call is skill-dependent, so it must be evaluated at the thrower's skill scalar. Jacobs' ninth-end runback in the 2026 final is the test: at the field's skill the field baseline calls it a poor menu; at his, it may have been the best shot on the sheet. Elite skips disagree in exactly the positions where it matters, so the best-call baseline is reported with uncertainty and is never the headline number.

---

## 12. Open Questions

Resolved in Phase 1: outcome clipping at ±3; full shot types without grouping; men and women pooled with a discipline flag; canonical perspective; recorded score as label; gates as set in Section 3.6; the event tier table; raster before set encoding for the geometry model.

Resolved in the modelling phase: the game-state encoding for f and g is the raw pair (score difference, ends remaining) plus an extra-end flag (Section 7.3); evaluation by time (train through 2024, test 2025–2026) runs alongside the by-book split for every experiment; level of play is the strength of the *event*, hand-rated (Section 3.5); no per-player skill and no grade enters f or g; per-book and per-player values never enter as columns; player identity is a normalised name key per discipline with an alias table (`data/player_aliases.csv`: 31 confirmed pairs such as SCHWARZ B → SCHWARZ-VAN BERKEL, 23 to check, 7 rejected because both names appear in one book); the skill scalar is per player with the team effect as its prior, pooled across seasons for now.

Open:

1. **Event ratings.** The ratings in `data/event_strength.csv` are tier defaults (Worlds 100, Europeans A 85, juniors 70) pending Mike's rating. The derived field strengths already disagree with them in places: the Olympics sit above the Worlds, the Olympic qualifiers and the Pan-Continental championships well below Europeans A.
2. **Event effect granularity.** Event first; sheet and session with shrinkage once the model-level effect exists.
3. **Skill scalar granularity.** Per player with a team-level prior, falling back to team for players with few shots.
4. **Free guard zone eras.** Pooled with an era flag versus per-era f in early-end positions. Only f is affected; g pools across eras.
5. **Player identity.** An alias table for name changes and a stable player id across events.
6. **Leverage-normalised consistency.** Execution divided by the width of the call's menu, so that steadiness is comparable across positions.

---

## 13. Status

Built and run, September 2026:

| Milestone | State |
|---|---|
| M1 Ingestion (decoder, detector, text parser, assembly, gates, audit) | Done; 92 books validated, all templates 2014–2026 |
| M2 Core (count function, canonical positions, mirroring) | Done |
| M3 Value mappings, baseline models, Points Gained, reports | Done; f 1.494 / g 1.472 / trivial 1.593 held out by book |
| M4 Archive (inventory, download, survey, parallel batch) | Done; 208 books downloaded, 116 line-score only |
| M6 Plumbing: feature cache, vectorised build and PG, experiment command | Done; full pipeline 2.5 h to 17 min, identical results |
| M7 Game situation in f and g | Done; f 1.470 / g 1.453 / trivial 1.559 held out by book |
| M8 Difficulty model (skill scalar, event effect) built as a report; g takes the event rating | Done; per-player input withdrawn (Section 3.5) |
| M9 Intent from the delivered stone; target model; ring detector for 2016–2019 | Done; g 1.4373 → 1.4325 on the time split without level, 1.4311 with the event rating |
| M10 Raster geometry model, probe and monotonicity gates | Built and rejected: plain raster f 1.493, hybrid 1.487, trees 1.455 on the time split |
| M11 Phase 2 | After M10 |

The modelling phase is complete. The system that comes out of it: f and g as boosted trees on the position features, the game situation, the event rating and, for g, the call type, turn and the struck stone; held out by book, f 1.470 and g 1.447 against a trivial 1.559; the full pipeline in about fifteen minutes; per-event reports with execution first in both currencies. Mike's direction for what follows (2026-09-10): the metric is outcome-first. Execution (PG: Throw) is the primary pivot in both currencies, with the tail statistics of Section 10 (floor, reliability, big misses, the five costliest shots) alongside it in points and in win probability; the call component is reported second, and no further work goes into intent. Skips call plan B and plan C while the rock is moving, and the position they leave is what the metric should credit. The five last-rock hit calls the model rates worst at the 2026 Olympics and Jacobs' ninth-end clearing are the pinned test set (`pointsgained testset`) for all three.
