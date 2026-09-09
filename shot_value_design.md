# Points Gained: A Shot-Value Metric for Curling — Design Document

**Status:** Revised draft (2026-09-09) after review; see Section 13 for the implementation milestones.
**Scope:** Within-end valuation with a hammer-adjusted value mapping. The full game-situation layer (win probability) shares the same interface and is built in Phase 1 from line scores, with hammer-adjusted points remaining the reporting currency.

---

## 1. Goal

Assign every shot a value, **Points Gained (PG)**, that measures how much it changed the expected scoring of the end, from the throwing team's point of view. The name is chosen by analogy with strokes gained in golf: it is measured against the field, it is additive, and it decomposes. Two properties are required:

1. **Situation-aware.** A made draw against an opponent stone in the four-foot is worth more than the same draw into an empty house, because the expectation before the shot was lower.
2. **Conserved.** The values of all shots in an end sum to the final score minus the expected score at the start of the end. No credit is created or lost.

The output is a per-shot Points Gained, decomposable into **PG: Call** (selection — what the call was worth) and **PG: Throw** (execution — what the throw delivered against the call).

### 1.1 Philosophy

Every shot in curling has two parts. First a call is made — by the skip, often with the whole team — and the call sets up a menu of possible outcomes with their odds: the roll-out that blanks, the stick that scores one, the miss that gives up a point, the flash that gives up two. Then the shot is thrown, swept and called on line, and one outcome from that menu happens. The call is a decision; the throw is an event, and what can be judged is its effect against the menu the call created. The best calls create menus whose expectation, weighted by how this team actually executes, is highest relative to the position; that is not always the menu with the biggest upside, because a bigger upside usually comes with a lower make rate and a worse downside, and the right trade-off depends on who is throwing. A slightly worse call creates a menu that is worth a little less in expectation, sometimes by giving up upside and sometimes by exposing the team to a downside the better call avoided.

The model evaluates every rock in both dimensions. Selection asks what the call's menu was worth compared with the position the team was handed. Execution asks what the throw produced compared with the menu the throw was handed. Neither is judged by the other: the execution value does not penalise a poor call or reward a brilliant one, and the selection value does not credit a lucky throw or blame a bad one. The two components sum to the shot's total contribution to the end.

### 1.2 Strategy: how game situation enters

Within an end the structure is recursive. Every shot before the last one builds a **position**, every position carries an **outcome distribution** (the chances of blanking, scoring one, scoring two, giving up one, and so on), and the last rock realises one outcome from it. The rock before the last is thrown to make that distribution as bad as possible for the thrower of the last rock; the rock before that, to make it as good as possible two rocks down the line; and so on back to the first stone. The two teams are pulling on the same quantity in opposite directions, which is exact rather than approximate: whatever currency an outcome is valued in, the opponent's value is the negation.

Strategy is the observation that not all outcome distributions are equally useful to a team, and which ones are useful depends on the game. Curlers have a vocabulary for this: *must steal*, *force one*, *two or blank*, *don't give up more than two*, *score or go to the extra end*. A default middle-game strategy is "take two with the hammer, force one without it," which in distribution terms means the hammer team wants mass on two and on blank, and as little as possible on one. Late in a close game, or in a lopsided one, the preferred distributions look completely different.

In this model those goals are not a separate layer and are not enumerated by hand. They are the *shape* of the value mapping v(outcome | game situation): tied in the last end with hammer, one and two are both worth a win, a blank is worth roughly the chance of winning an extra end with hammer, and a steal is worth nothing, and maximising expected value under that shape simply *is* "score or don't get stolen on." The win-probability table (Section 9.4) generates every one of the named strategies as a consequence, per tier and gender, in the same way the hammer-adjusted lookahead of Section 9.2 generates "don't take one in the middle ends." The names remain useful as a readout: any game situation can be labelled by which strategic regime its v-shape implies, and that label is how a value gets explained to a coach.

Two things follow for the design. First, a position's outcome distribution depends on the regime, because it depends on how both teams will play the remaining rocks, and they play differently when a steal is mandatory than when a blank is welcome. The outcome models therefore take game situation as input (Section 7.2), and "a strategically favourable position" means a position whose distribution, under regime-appropriate play, sits where that regime's v is high. Second, differences in strategy between tiers or between men's and women's play can be either a different v (a different win-probability landscape) or a different policy under the same v, and the two are estimated from different tables — game results and shot selection respectively — so the data can tell them apart.

### 1.3 Terminology

| Term | Meaning |
|---|---|
| **Position** (S) | The stones on the ice plus rocks remaining, hammer and rule era, from the thrower's perspective. Pre-shot and post-shot positions bracket every shot. |
| **Game situation** | Score difference, ends remaining and hammer at the start of the end. Not part of the position. |
| **Regime** | The strategic goal implied by a game situation (must steal, force one, two or blank, ...), derived from the shape of v. |
| **Call** (C) | The shot as called: type and subtype as recorded. Its outcome distribution D(S \| C) is informally the call's **menu**. |
| **Outcome** | The end result from the thrower's perspective: blank, +1, +2, ..., −1, −2, ... |
| **Outcome distribution** (D) | Probabilities over outcomes for a position, or for a position and call. Output of f and g. |
| **Value mapping** (v) | The worth of each outcome in the current currency: hammer-adjusted points (Phase 1) or win probability (later). |
| **Value** (V) | Expected worth of an outcome distribution under v. |
| **Points Gained** (PG) | V after the shot minus V before it. The metric. |
| **PG: Call** | The selection component: the call's menu against the position. |
| **PG: Throw** | The execution component: what happened against the call's menu. |
| **Field baseline** | D(S) under the field's typical play; the Phase 1 reference for PG: Call. |
| **Best-call baseline** | D(S) under the best available call; Phase 2. |
| **Hammer net** (N) | Expected net score of the hammer team in one end; sets the value of a blank in Phase 1. |
| **Event effect** | The field's execution on this event's ice, absorbed statistically rather than modelled. |
| **Skill scalar** | A per-thrower level-of-play number estimated from execution grades. |

---

## 2. Framework

### 2.1 Definitions

- **S**: the pre-shot **position** (stones on the ice, rocks remaining, hammer, rule era), normalized to the thrower's perspective.
- **C**: the called shot (the shot type as recorded, possibly with inferred target).
- **S′**: the post-shot position.
- **D(S)**: the **outcome distribution**: a probability distribution over end outcomes given position S, where the outcome space is {blank, +1, +2, +3, ..., −1, −2, −3, ...} from the thrower's perspective, clipped at ±3 (or ±4; see open questions).
- **V(D)**: a scalar value of an outcome distribution. In Phase 1, V is hammer-adjusted expected points using a one-end lookahead (Section 9.2), so that a blank is valued as keeping hammer rather than as zero. Later, V will map each outcome to a fully game-situation-dependent value (Section 9.4). Everything below is written so that swapping V is a one-line change.

### 2.2 Points Gained

    PG(S, C, S′) = V(D(S′)) − V(D(S))

For the last shot of an end, D(S′) is a point mass on the actual result, so this reduces to the original formulation: actual minus expected.

### 2.3 Decomposition

Insert the called shot as an intermediate baseline:

    PG: Throw (execution) = V(D(S′))    − V(D(S | C))
    PG: Call  (selection) = V(D(S | C)) − V(D(S))

where D(S | C) is the outcome distribution given the position *and* the call actually made. Execution measures how the result compares to what that call usually produces; selection measures what the call was worth relative to the position. A missed blank that scores one is entirely an execution event. Whether blanking was the right idea is a selection event.

Two baselines for selection are useful, and both will be computed:

- **Field baseline** (Phase 1): D(S) is the outcome distribution under the observed shot-selection policy at the elite level. Selection can be positive or negative and reads as "better or worse than the field would call."
- **Best-call baseline** (Phase 2): D(S) is the distribution under the best available call. Selection is always ≤ 0 and reads as regret.

### 2.4 Perspective convention

Every physical position is evaluated **once**, from a canonical perspective: the team holding hammer in the current end. Stones are labelled `hammer` / `non_hammer`, and f is fitted and evaluated only in this frame. A thrower's value is then V from the canonical frame, multiplied by +1 if the thrower holds hammer and −1 otherwise.

This is deliberate rather than cosmetic. If f were evaluated from the thrower's perspective, the same physical position would be evaluated twice — once for the team that just threw and once for the team about to throw — and a learned model is not exactly antisymmetric under the swap, so the sum of Points Gained over an end would not telescope. With a single canonical evaluation per position, the telescoping identity in Section 2.5 holds by construction. `has_hammer` is no longer an input to f: the canonical frame always has hammer, and who throws next is determined by `rocks_remaining` parity. Reporting flips the sign back to the thrower's point of view.

### 2.5 Conservation check

With D(final position) defined as the actual score, summing Points Gained over the 16 shots of an end gives:

    Σ PG = actual_score − V(D(S₀))

where S₀ is the empty-sheet position at the start of the end. Under the canonical-frame convention of Section 2.4 this identity is exact; it is kept as a unit test of any implementation, not as an approximation to be monitored.

---

## 3. Data

### 3.1 Source

One corpus: the CURLIT results-book directory (`curlit.com/results`), covering every World Curling event from 2013 onward plus a sparser set back to 2001, at roughly 20 team-of-four books per season. The directory lists about 300 Results Books, of which roughly 200 are in scope (Section 3.6.1); estimated at 10,000+ games and 1.5–2M shots once processed. Section 3.6 specifies the pipeline.

Four books held locally (WMCC 2026, WWCC 2025, OWG 2026, WJCC 2025 Men; roughly 250–300 games and 40,000 shots) serve as the development fixtures for the extractor and as the first data for the count function, calibration and the hammer net.

Jordan Myslik's earlier extraction (`jwmyslik/curling-analytics`) is the precedent for this work and its schema is the starting point for Section 3.2, but it cannot be rerun: its source (`odf2.worldcurling.co`) no longer exists, and its parser depended on rendered page images. Nothing here depends on it.

### 3.2 Tables used

| Table | Fields used |
|---|---|
| `ends` | `number`, `color_hammer`, `score_red`, `score_yellow` (where present), `time_left_red`, `time_left_yellow` |
| `shots` | `number`, `color`, `team`, `player_name`, `type`, `subtype`, `turn` (clockwise / counter-clockwise), `grade` (percentage, or 0–4 in older books), `red_remaining`, `yellow_remaining`, `red_removed`, `yellow_removed` |
| `stones` | `shot_id`, `color`, `x`, `y`, `delivered` (this stone was the one thrown), `prev_x`, `prev_y` (prior position if the diagram shows the stone was moved) |
| `games` | `type` (Men/Women), `event_id`, `sheet`, `session`, dates (for rule era) |

The diagrams carry more than the original schema recorded: stones-remaining counters per colour (top corners), stones-removed counters (bottom), hollow circles at the prior positions of moved stones, and a mark on the stone just delivered. All of these are extracted. The `turn` field is kept: it is free, matters for in-turn versus out-turn execution modelling, and mirroring (Section 4) must flip it.

### 3.3 Known data issues and handling

- **Pixel coordinates.** The diagrams are 300×600 pixel images (Section 3.6.4) with fixed geometry: centre line at column 149, tee line at row 439, 12-foot outer radius 118.5 px, hog line at row 20 and back line at row 560. That is 1.646 px per inch (0.61 in per pixel), consistent in both axes and across every book checked from 2014 to 2026. Calibration is verified per book from the ring radii, and stone radius ≈ 5.7 in is used for in-house determination.
- **Missing end scores** (~30% of score boxes). Reconstruct every end's score from the final stone configuration using the count function (Section 5.3). Use the recorded score only as a cross-check; disagreements are flagged for inspection.
- **Missing hammer indicator** (~0.1% of ends). Infer from shot order (the team throwing shot 16 has hammer).
- **Rule era.** Four-rock free guard zone before the 2018–19 season, five-rock after. Store `fgz_rocks ∈ {4, 5}` as a position feature derived from event date. Early-end values are expected to differ across eras.
- **Shot type label hygiene.** Merge case variants ("through"/"Through"); drop "None", "no statistics", "not played" from training but keep the shot in sequence so position transitions remain continuous.
- **Percent score.** The officials' 0–100 execution grade. Not used as an outcome target (it's a judgment, not a result) but used to identify well-executed shots for intent modelling (Section 6) and as the training signal for the skill model (Section 3.5).

### 3.4 Strata labels

Every training row carries a full set of stratum keys so that the pooled model can be re-fit on any subset later without re-running the pipeline. Pooling is the default; separation is a filter.

| Key | Source | Reliability |
|---|---|---|
| `gender` | `games.type` | High |
| `season`, `fgz_rocks` | event dates | High |
| `event_id`, `event_name` | `events` | High |
| `event_tier` | hand-written mapping from event name (Olympics, Worlds, Europeans, Pacific-Asia, Juniors, B-division, Mixed, ...) | High once mapped; the corpus is WCF-only, so tour events are not present and not inferable |
| `team` | `shots.team` | High |
| `team_rating` | within-corpus Elo or win % by season; optionally joined to external world rankings by country and season | Medium |
| `player_name`, `player_id` | `shots.player_name`, normalized | Medium (name variants) |
| `position` | shot number within end (1–2 lead, 3–4 second, 5–6 vice, 7–8 skip) | Medium (lineup changes are noise) |
| `stage` | session name (round robin / playoff) | Low; recorded but not relied on |

### 3.5 Level of play

A six-foot double is worth less to an elite team than to a club team because the elite team makes it more often: the expected outcome given the call, D(S | C), is higher, so the PG: Throw for making it is smaller. Level of play is therefore a property of the **execution distribution**, not of the position, and it enters the framework through g, not through f alone.

Two mechanisms, used together:

1. **Categorical level features.** `event_tier`, `gender`, `team_rating`, and `position` are included as features in f and g. This gives per-level values within the range the corpus covers (roughly junior B-division to Olympic finalist) with one pooled fit.

2. **Continuous skill scalar.** Fit a shot-difficulty model on the execution grade: P(grade | shot type, position features, skill), where `skill` is a per-player (or per-team) scalar estimated from that player's grade history, with `event_tier` and `team_rating` as priors. This places every thrower on one continuous scale. Level of play is then a number, not a category, and data from lower levels added later will appear as new points on the same scale rather than a new class the model has never seen. The skill scalar is included as a feature in g, and at prediction time can be set to a chosen level ("value this shot as if thrown by a mid-tier club team").

The categorical features are the near-term deliverable; the skill scalar is built in Phase 1b once the grade model is validated, because it is also the input to the Phase 2 transition model's error scale.

Caveat: neither mechanism extrapolates reliably below the corpus's weakest stratum. Values for club-level play will be estimates until club-level data exists; the design ensures they can be replaced by fitted values without changing anything else.

### 3.6 Full-corpus pipeline

#### 3.6.1 Scope

**In scope:** every Men's and Women's team-of-four results book with shot-by-shot pages. The event families present in the directory, with their tier assignment:

| Tier | Event families |
|---|---|
| 1 | Olympic Winter Games; World Men's / Women's Championships |
| 2 | European Championships A-Division; Pan Continental Championships A-Division (and predecessor Pacific-Asia Championships); Olympic Qualification Event |
| 3 | European B-Division; Pan Continental B-Division; World Championship Pre-Qualifiers; Pre-Olympic Qualification Event; World Junior Championships |
| 4 | World Junior-B Championships; World Senior Championships; Winter Universiade |

Tier is a starting label, not a claim that all teams in a tier are equal; team rating and the skill scalar (Section 3.5) carry the within-tier variation.

**Out of scope:** Mixed Doubles (all variants, including Junior MD and MD qualification events), Wheelchair and Paralympic curling, Youth Olympic Games (mixed teams, short games), and any skins or exhibition formats. These are catalogued in the inventory (3.6.2) but not downloaded or processed. Mixed Doubles is a distinct game and would need its own position representation and models.

#### 3.6.2 Inventory

Deliverable: `data/inventory.csv`, one row per results book, built by fetching `https://curlit.com/results`. The page is server-rendered HTML with direct `href="PDF/<name>.pdf"` links, so a plain HTTP fetch and a regex over the anchors is sufficient; no headless browser is needed. Some listed links return 404, so each in-scope URL is checked with a HEAD request and its status and size recorded.

Columns: `season`, `event_name`, `event_family`, `tier`, `gender`, `location`, `start_date`, `url`, `http_status`, `file_size`, `in_scope`, `has_shot_by_shot` (filled in 3.6.3), `style_family` (filled in 3.6.3), `status` (pending / downloaded / surveyed / extracted / validated / excluded), `notes`.

`event_family` and `tier` come from a hand-written regex table over event names. The table is part of the repo and is the single place event tiers are defined.

#### 3.6.3 Survey pass

Before extraction, every in-scope book is opened and characterised:

1. Detect whether shot-by-shot pages exist (page-level text search for "Game - Shot by Shot"). Books without them (Results Summaries, or older books that only carry line scores; ECC 2013 A-Division is one) are marked `has_shot_by_shot = false` and skipped.
2. Characterise one shot-by-shot page per book: are the diagrams embedded indexed images of the standard size (3.6.4); which palette (WCF or Olympic template); which text variant (percentage grades with arrow glyphs for turn, 2015 onward; 0–4 grades with In/Out words and unhyphenated type names, 2014 and earlier); whether a sub-type line is present. Assign each book a `style_family` id from these facts.
3. Produce a contact sheet of one decoded panel per style family, with detected stones overlaid, for manual review.

The survey confirms which books the standard extractor covers. Only a style family whose diagrams are not embedded indexed images would need the fallback in 3.6.4.

#### 3.6.4 Extraction

One interface: `extract_book(pdf_path) -> (games, ends, shots, stones)`.

The per-shot diagrams are not drawn on the page; they are embedded raster images, 300×600 pixels (occasionally 301×601), 4-bit indexed colour with an exact 16-entry palette, losslessly compressed. This was verified on every book examined from WMCC 2014 to OWG 2026. The extractor therefore never renders a page:

- **Diagrams.** Read each image stream and its palette directly from the PDF (`pdfplumber` exposes both), unpack the nibbles, and map to RGB by palette value (palette *order* varies between images, so classification is by colour, never by index). Stones are exact colour regions — red (255,0,0); yellow (255,200,50) in the WCF template or (255,230,0) in the Olympic template — found by connected components and split, when touching, with the known 9 px stone radius. Grey (80,80,80) or coloured hollow rings are prior positions of moved stones; a black mark inside a stone identifies the delivered stone; the corner counters give stones remaining and removed per colour.
- **Text.** Real text with coordinates: player, shot type, sub-type line where present, turn, grade, the end header with running score, Total Score and Time left, and the page header (event, date, session, sheet, start time). Panels are located by the fixed grid (six columns, three rows, identical in every book seen). The text parser dispatches on the style family for the per-era variants listed in 3.6.3.
- **Fallback.** If the survey finds a style family whose diagrams are not embedded indexed images, a small object detector (two classes, red and yellow stone, as in Suzumura et al., Applied Sciences 2026) is trained for that family only. It must emit the same tables.

Coordinate convention: house at the bottom, pin at (0,0), converted to inches at 1.646 px/in (Section 3.3). Diagram pixel coordinates are retained alongside the calibrated values.

Facts established while building the extractor on the four local books and WMCC 2014:

- **Alternate ends are drawn with the house at the top.** Odd ends have the house at the bottom, even ends at the top (the sheet is drawn from a fixed vantage point and play changes direction). The extractor detects the orientation from the ring position and rotates the image 180° so every position is in the thrower's frame; the stones-remaining and stones-removed counters swap strips accordingly.
- **Delivered-stone marker.** A small black mark at the stone centre in the WCF and Olympic templates; a 2 px outline (instead of 1 px) in the 2014 template. Both are detected. The marker is absent when the delivered stone left play, which is the case for most clearing and take-out shots, so about 11% of shots have no marked stone.
- **Yellow stone glyphs.** Plain yellow (WCF), yellow with a blue cross (Olympic template), or yellow with a black X (2014). The cross pixels are filled before detection; the fill rule requires stone colour on all four sides so that touching stones' shared outlines are never merged.
- **Conceded ends.** An `X` in place of the end score in the page header marks an end that was not completed. Such ends are kept for position continuity but carry no outcome label.
- **Team colours** come from the colour-dot images beside the team names in the end header, cross-checked against the colour of the delivered stone per shot (agreement above 99.9%).
- **Resolution limit.** Score reconstruction from the final position agrees with the recorded score in about 96.5% of ends; the remainder are stones within an inch of each other or of the 12-foot edge, which a 0.61 in/px diagram cannot resolve and which were measured on the ice. The recorded score is therefore the label and the reconstruction is the gate. A biting tolerance does not improve agreement.

Fields added to the `shots` table beyond Jordan's schema:
- `shot_subtype` (the second line under the shot type in newer books, e.g. "Slow Take-out"), nullable
- `style_family`, `book_url`, `page_number`, `panel_index` (provenance, so any extracted position can be traced back to its diagram)

#### 3.6.5 Validation gates

A book moves to `validated` only if it passes all of the following:

- **Stone count consistency.** After shot k in an end, the number of each colour on the sheet plus removed plus unthrown equals 8. Mismatch rate per book below 0.5%; ends failing this are flagged, not silently kept.
- **Score reconstruction.** The count function (Section 5.3) applied to the final position of each end must match the recorded end score wherever the score box is present. Agreement rate per book above 99%; disagreements are reviewed on the contact sheet.
- **Hammer consistency.** The team that throws shot 16 must match the recorded hammer, and hammer must alternate correctly given the reconstructed scores.
- **Shot count.** 16 shots per end unless the end is conceded; concessions must appear at the end of a game, not mid-game.
- **Position sanity.** No stone outside the play area; no two stones of any colour closer than one stone diameter (overlap indicates a duplicate detection or a previous-position marker mistaken for a stone).
- **Counter consistency.** The stones-remaining and stones-removed counters read from each diagram must agree with the census of detected stones and with the shot number.
- **Player statistics.** Per-player shot counts and average grades computed from the extracted shots must reproduce the book's Cumulative Player Statistics pages.
- **Sampled visual audit.** For each style family, 30 random panels are overlaid with extracted positions and reviewed by eye. Any systematic offset triggers a recalibration of that family.

Per-book validation metrics are written back to the inventory so the corpus can be filtered to validated books at training time.

#### 3.6.6 Storage

- Raw PDFs kept as downloaded, organised by season (25–115 MB each; on the order of 8 GB for the in-scope set).
- Extracted tables as Parquet (`books`, `games`, `ends`, `shots`, `stones`), queried with DuckDB, with the provenance columns above and the stratum keys from Section 3.4 attached at extraction time.
- The inventory CSV is the manifest; nothing enters training that isn't `validated` and `in_scope`.

#### 3.6.7 Implications for the models

With an order of magnitude more data, several earlier design compromises can be replaced by brute force:

- **Rule eras.** Rather than relying on a single `fgz_rocks` flag, fit f separately per era as well as pooled, and compare held-out performance. The five-rock era (2018 onward) is already the majority of the corpus and is the one that matters going forward. Note that execution does not change with the free guard zone rule: g and the skill model (Section 3.5) can pool across eras freely; only the value function f, and only in early-end positions, is era-sensitive.
- **Held-out splits by event** become cheap enough to use tier-stratified folds, so per-tier calibration can be reported.
- **Shot type grouping** (Section 6) is dropped in favour of the full twelve types plus sub-type.
- **Fixtures-then-refit.** Phase 1 models are first fitted on the four local books while the archive is processed, then refit; the feature extractor and validation gates should not need to change.

---

## 4. Preprocessing

1. Calibrate coordinates to inches (per-axis).
2. For each shot, assemble the **pre-position** (positions after the previous shot; empty for shot 1) and **post-position** (positions after this shot).
3. Reconstruct the end score from the final position; compare with recorded score.
4. Determine hammer team and thrower for each shot; compute `rocks_remaining` (stones not yet thrown after this one, 0–15) and whether the thrower has hammer.
5. Assign rule era.
6. Normalize perspective: relabel stones as `hammer` / `non_hammer` (the canonical frame of Section 2.4); record for each shot whether the thrower holds hammer so values can be reported from the thrower's point of view.
7. Mirror every position left-right to produce a second training example (labels unchanged, turn flipped). Applied at training time only.
8. Attach all stratum keys (Section 3.4) to every row.

---

## 5. Position Representation

### 5.1 Principles

The subtleties that decide a curling position live at the inch level: whether a double is on, where a roll ends up, whether a guard actually covers the line. Any hand-built classification of positions throws that away. The design therefore uses two representations with different jobs:

- **Raw geometry (primary).** The model sees the stones themselves. Nothing about the position is classified by hand; whatever matters is learned from outcomes. This needs the full corpus (Section 3.6) to work well.
- **Baseline features (secondary).** A compact hand-built vector used for three purposes: a baseline to beat, an interpretability layer for reporting, and the working representation on the four local books before the archive is ready. No claim is made that these features capture what a skip evaluates.

Everything below is expressed in the canonical hammer-team frame (`hammer` / `non_hammer`; Section 2.4) with left-right mirroring applied at training time. Where the text says "own" it means the hammer team.

### 5.2 Raw geometry representation

A position is a set of up to 16 stones, each described by (x, y, owner), in calibrated inches with the pin at (0,0), plus the situation variables `rocks_remaining` and `fgz_rocks` and the strata / level features of Sections 3.4–3.5 (`has_hammer` is implicit in the canonical frame). Two model-input encodings will be tried:

- **Set encoding.** Stones as an unordered set fed to a permutation-invariant network (DeepSets or a small transformer over stones). Handles variable stone count naturally; no rasterisation loss.
- **Raster encoding.** The play area rendered as a two-channel image (own / opp occupancy, with stone footprints) at roughly 1-inch resolution, fed to a small CNN. Simpler to reason about; loses sub-pixel precision but 1 inch is below the source data's own recording error.

This is the approach used by the Hokkaido group's expected-score-distribution model, which takes each stone's coordinates and ownership as input and was trained on results-book data; their reported improvement from adding end-situation variables confirms the situation variables belong in the input.

### 5.3 Count function

Given a position: sort all stones by distance from the pin; a stone is in the house if distance ≤ 72 in + stone radius. The team owning the closest in-house stone scores the number of its in-house stones closer than the nearest in-house opposing stone. Empty house scores 0 (blank). This function also produces the reconstructed end score in Section 4. It is exact, not a judgment, and is used by both representations.

### 5.4 Baseline feature set

**Situation:** `rocks_remaining` (whose parity says who throws next), `fgz_rocks`, `stones_in_play`.

**Level / strata:** `event_tier`, `gender`, `team_rating`, `position`; `skill` in g once available (Section 3.5).

**Lie:** `count` (clipped ±3), `shot_rock_ring`, `margin` (inches between shot rock and first opposing stone), `second_stone_owner`, `third_stone_owner`, `boundary_gap` (inches between the last counting stone and the first opposing stone) and `near_tie` (boundary gap under two inches).

**Near-tie positions.** The diagrams resolve about 0.6 in per pixel, so stones within roughly two inches at the ownership boundary are tied on the sheet and unresolvable in the data. These are the 3–4% of ends where the count function disagrees with the recorded score, and they are a real game state rather than noise: the skip cannot tell which rock is second either, and the call made there (peel, freeze, play for the measure, draw for the sure one) is a strategic response to that uncertainty. The recorded score remains the label, the count function is never ground truth for those ends, D stays a full distribution rather than collapsing on the count, and the baseline features name the state explicitly so that calls in tied positions can be studied. The raw-geometry model is expected to learn it unaided.

**House occupancy:** `own_in_house`, `opp_in_house`, `own_behind_tee`, `opp_behind_tee`.

**Guards:** counts per team by lane (left / center / right, center = |x| ≤ 24 in), and depth of the nearest center guard.

**Cover (crude):** `shot_rock_covered`, `button_covered`, `open_hit_available`, each computed by a straight-line corridor test from the hack with a fixed curl allowance. These are known to be wrong at the margins — they cannot tell an open double from a double that is one inch off — and exist only so the baseline has something in this dimension. Phase 2 replaces them with simulated shot-availability probabilities (Section 11).

---

## 6. Called Shot and Intent

The `type` field records the shot called, and newer books add a `shot_subtype` line. Phase 1 uses these as recorded, without grouping if the full corpus supports all categories (the twelve types seen so far: Draw, Take-out, Hit and Roll, Guard, Front, Freeze, Raise, Clearing, Double Take-out, Promotion Take-out, Wick / Soft Peeling, Through). If sparsity forces it on the four local books, the grouping is Draw {Draw, Freeze}, Guard {Guard, Front}, Hit {Take-out, Hit and Roll, Clearing, Double, Promotion}, Raise/Wick, Through.

The type leaves the target ambiguous (a draw to the button vs. the 8-foot). In Phase 1 the raw-geometry model conditioned on the type is left to learn what targets are typical from that position; no target inference is attempted. In Phase 2, a target distribution per (type, position) is learned from shots graded 100%, with lower-graded shots treated as noisy realisations of that target; this is the input to the execution error model (Section 11).

The Through/Draw distinction on a last rock with an empty house is the blank-vs-score decision and is handled by the type alone.

---

## 7. Phase 1: Direct Outcome Models

### 7.1 Insight

Every shot's pre-position is labeled with the end's final outcome. Sparsity of exact positions does not matter once the model can generalise across positions; there are roughly 40k (position, outcome) pairs in the four local books (80k with mirroring) and an estimated 1.5–2M in the full corpus. The outcomes are high-variance per example, but that variance is what the model averages over. This is a supervised problem, not a dynamic-programming problem.

**Phase 1 is deliberately outcomes-biased.** It says what positions and calls have been worth, on average, given how the field has actually played and executed. It makes no claim about what a position *should* be worth under optimal play, and it does not model physics or ice. Those are Phase 2 (Section 11), and everything in Phase 1 is built so that Phase 2 can replace components without changing the framework.

### 7.2 Models

- **f(S) → D**: distribution over end outcomes from the position. This is D(S) under the field baseline.
- **g(S, C) → D**: same, with the called shot type (and subtype) as an additional input. This is D(S | C).

Both models also take the strata / level inputs (Sections 3.4–3.5), the event effect (Section 8), and the game situation (`score_diff`, `ends_remaining`, or a compressed regime label derived from them; Section 1.2). On the four local books the game-situation inputs may need to be coarsened or dropped; on the full corpus they are core.

Two model families, in order:

1. **Baseline: gradient-boosted trees** on the Section 5.4 feature vector. Fast, interpretable, and adequate on the four local books. Kept permanently as the reference point. On the four local books (about 2,900 labelled ends) the model must be strongly regularised: eight leaves, 300 samples per leaf and 60–80 boosting rounds beat the trivial (rocks remaining, hammer, count) model on held-out books, while a richer configuration overfits and loses to it. Points Gained are always computed from out-of-fold predictions, so no position is valued by a model that saw its book.
2. **Primary: raw-geometry model** (Section 5.2) trained on the full corpus. Adopted as the production f and g only if it beats the baseline on held-out log-loss by a margin that survives tier-stratified evaluation.

### 7.3 Boundary conditions

- **Final position** (after shot 16, or when the end is conceded/finished early): D is a point mass on the reconstructed score. f is not evaluated here.
- **Start of end**: S₀ is the empty-sheet position with `rocks_remaining = 16` (in the canonical frame the hammer team's view). f(S₀) is the end's opening expectation and is expected to be close to the empirical average for that era/tier combination; this is a calibration check.

### 7.4 Training set construction

One row per shot for f: the pre-position, label = end outcome from the thrower's perspective. One row per shot for g: the same, plus called shot. Mirrored rows are added. Rows from ends with unresolved score reconstruction, or from books that failed the validation gates (3.6.5), are excluded. Held-out split by **event**, stratified by tier, never by shot or end, to avoid leakage between shots in the same end.

### 7.5 Validation

- Held-out multiclass log-loss and Brier score for: (a) a trivial model on (rocks_remaining, has_hammer, count); (b) the feature baseline; (c) the raw-geometry model. Reported overall and per tier.
- Calibration plots per outcome class.
- Conservation: Σ PG over each end equals actual − V(f(S₀)) to numerical precision.
- Sanity tables: for last-rock draws, compare f/g outputs to the hand-derived matrices (empty house ≈ 0.97 / 0.03; opponent in the four-foot ≈ 0.70 / 0.29 or whatever the data says).
- Monotonicity spot-checks: adding an opponent guard in front of an own shot rock should not raise the thrower's expected value; removing a covered opposing stone should not lower it.
- **Subtlety probe** (raw-geometry model only): take real positions where a double was made, translate the target stone by ±1, ±2, ±4 inches, and plot g(S, Double) against the offset. A model that has learned the geometry shows a sharp drop where the double closes; a model that hasn't shows a flat line. This is the single most informative diagnostic for whether the representation is doing its job.

---

## 8. Conditions and Field Adjustment

Ice varies: swing, speed, pebble, flatness, and how all of these change over a game and a week. The design does not model any of it. Instead it follows the strokes-gained approach from golf, where the difficulty of a course's greens is never modelled directly; it falls out of how the whole field putted on those greens that week, and a player is measured against that field. No attempt is made to represent undulation or break; distance is the only input, and everything else is absorbed by the field.

The curling equivalent: a shot's expectation is conditioned on the **event** (and, where the data supports it, the **sheet** within the event, and the **session** or day). If draws to the four-foot are made 65% of the time by the field at one event and 80% at another, that difference *is* the ice, and a made draw at the first event earns more than at the second. Execution value becomes "versus the field, on this ice, this week."

Mechanically, the event effect enters as a random effect (or an embedding) in g and in the execution-grade model of Section 3.5. Two things follow:

- **Separating ice from field strength.** An event effect on its own conflates the ice with who was playing. The skill scalar is per player and stable across events; the event effect is per event and shared across players. Fitting them jointly (a mixed model, as in Broadie's field-adjusted strokes gained) separates the two, provided players appear at multiple events — which at this level they do.
- **Sheet and session effects.** The data records the sheet for every game and the session for every draw. Sheet-within-event effects are worth fitting because sheets are known to differ; session effects capture ice evolving over the week. These are only as good as their sample sizes (a sheet hosts perhaps 10–12 games per event), so they should be shrunk hard toward the event effect.

The value function f is not conditioned on event: a position's worth under typical play is treated as a property of the game, and ice effects on value are assumed to wash through execution. This is a simplification that Phase 2's simulator, which can vary the curl and speed parameters, would let you test.

Direct ice measurements that exist in the books — the Draw Shot Challenge / Last Stone Draw distances — are stored but not used in Phase 1; they measure a team's draw precision on that sheet on that day, which the event and session effects already absorb.

---

## 9. Value Mapping V

### 9.1 Why blank cannot be zero

With V = expected points and blank = 0, a skip who faces two on the last rock and executes the called double-and-roll-out (blank) is scored *below* a skip who sticks and takes one. In the middle ends that is backwards: the blank keeps hammer, and at the elite level hammer is worth more than the point. Any value mapping that ignores who holds hammer next end will misrank blanks against singles, and will do so on a large share of hammer-team last rocks.

### 9.2 Phase 1 mapping: one-end lookahead

Let **N** (the **hammer net**) be the expected net score of the hammer team in a single end, estimated from the corpus per (tier, gender, era). From the thrower's perspective, with `hammer_after` = +1 if the thrower's team holds hammer in the next end and −1 otherwise:

    v(outcome) = points + N × hammer_after

| Outcome | hammer_after | v (N = 0.7) |
|---|---|---|
| +2 | −1 | 1.3 |
| +1 | −1 | 0.3 |
| blank | +1 | 0.7 |
| −1 (steal) | +1 | −0.3 |
| −2 (steal) | +1 | −1.3 |

V(D) = Σ P(outcome) × v(outcome). Blank outranks a single exactly when N > 0.5, which is the empirical content of "don't take one in the middle ends." Because Points Gained values are differences of V's, any additive constant in v cancels; only the spacing matters.

The one-end lookahead truncates the chain after one end. A cheap and slightly better hammer value is the infinite-horizon one, **H**: treat the game as a Markov chain over ends in which the hammer team's end-outcome distribution is stationary, so that H = N + (P(blank) + P(steal) − P(score)) × H, i.e. H = N / (1 − P(blank) − P(steal) + P(score)). H replaces N in v; with the elite men's distribution the difference is modest (H is a little under N), but H is the self-consistent choice and is what the win-probability layer reduces to in a long, tied game. Both are reported.

Worked example: last rock, hammer, facing two, call is a double. Suppose g gives 60% blank, 20% score one, 15% give up one, 5% give up two. V(before) = 0.42 + 0.06 − 0.045 − 0.065 = 0.37. PG: double and roll out +0.33; double and stick (or miss and score one) −0.07; miss and give up one −0.67; flash −1.67. The "score one" outcomes come out slightly negative, matching the curling judgment that they are misses.

Nothing upstream changes: f and g output distributions with blank as its own category, and v is applied afterward. This is why D must be a full distribution rather than a mean.

**Calibration check:** f evaluated at the empty sheet with hammer, mapped through v with the same N, should equal N (the hammer team's expected net for the end is by definition N). Disagreement means either f or the N estimate is off.

**Era dependence:** N is expected to differ between the four-rock and five-rock eras, since the five-rock rule was introduced partly to make blanking harder. Estimate N per era and confirm.

### 9.3 Limits of the lookahead

The one-end lookahead assumes a neutral game situation: middle ends, close score. It is wrong in the last end tied (a single wins, a blank does not), in the extra end, and when the score is lopsided enough that points and hammer trade at a different rate. These are exactly the situations where curlers already know game context matters, and they are handled by the full layer below.

### 9.4 Full game-situation layer (built in Phase 1)

V(D; game_situation) = Σ P(outcome) × v(outcome | score_diff, ends_remaining, hammer), where v comes from a win-probability table built from line scores (which every results book carries on its Game Results pages, so the table is available before shot extraction is complete), estimated per tier and gender by backward induction over an empirical end-outcome distribution with smoothing. Same interface as 9.2; swapping it in changes nothing in f or g. Hammer-adjusted points (9.2) remains the default reporting currency because it is easier to read; win probability is used for game-situation questions and for the regime label. A points-equivalent rescaling of the win-probability values is available if leaderboards in "points" are preferred.

The shape of v across outcomes in a given game situation is the model's representation of strategy (Section 1.2). A **regime label** — the named strategic goal implied by that shape (must steal, force one, two or blank, ...) — is derived from v for reporting, and can be used as a compressed game-situation input to f and g where the raw (score_diff, ends_remaining) pair is too sparse.

### 9.5 Coupling with shot selection

The observed shot-selection policy depends on game situation (teams blank more often when it's rational to, and the non-hammer team plays for the steal when it must). This is why f and g take game situation as input (Section 7.2): the outcome distribution from a position is a property of the position *and* of how both teams will play the remaining rocks. Note also that intent (e.g. roll-out vs. stick on a double) is not recorded in the data; it affects only the execution/selection split, never the total Points Gained, and is partly recoverable from the officials' grade and the game-situation prior.

---

## 10. Outputs and Aggregation

Per shot:
- `pg`, `pg_call`, `pg_throw`
- The three distributions D(S), D(S | C), D(S′) (stored, so V can be re-applied later)

Aggregations:
- By player (PG: Throw, per game / per event / per shot type)
- By team and skip (PG: Call)
- By shot type and situation (which calls earn the most in which positions)
- Leaderboards normalized per shot to compare positions with different shot counts

---

## 11. Phase 2: Physics, Transitions, and the Best Call

Phase 1 answers "what has this been worth." Phase 2 answers "what could this have been worth," which needs counterfactual calls, and therefore a model of what happens when a shot is thrown. Everything here is deferred; it is specified so the Phase 1 outputs and data are shaped to feed it, and because collaborators with an interest in the physics can see where their work plugs in.

- **Simulator.** Collision geometry, rolls, raises and run-backs are deterministic physics; the Digital Curling platform and similar simulators already implement them. A simulator answers exactly the inch-level questions the raw-geometry model has to learn statistically: is the double on, where does the shooter roll, does the raise reach.
- **Execution error model.** The only stochastic component. Learned from the results books: for each (type, target inferred from shots graded 100%, level / skill scalar, event effect), the distribution of where the thrown stone actually arrived relative to target. Section 8's event effects become the calibration of the error model to that week's ice.
- **Transition model.** P(S′ | S, call) = simulator applied to the call with delivery sampled from the error model. This replaces the crude cover features of Section 5.4 with simulated shot-availability probabilities, which can also be fed back into Phase 1's f as derived features.
- **Rollouts.** From any position, simulate the remainder of the end under a policy (initially the empirical policy P(C | S, game situation)), evaluating with f at a fixed depth. This gives better-calibrated distributions in rare positions. When the policy is replaced by an optimising one, there is a single objective for both teams — maximise E[v | game situation] for the thrower, which the opponent minimises, since v is zero-sum — so no separate strategic modes are needed; the named strategies of Section 1.2 emerge from the shape of v.
- **Best-call baseline.** For each position, evaluate each candidate call via rollout and take the maximum; selection under this baseline is the regret of the call actually made. Two cautions stated up front: the best call is skill-dependent (the right call for a team that makes doubles 85% of the time is not the right call for one that makes them 60%), so it must be evaluated at the thrower's skill scalar; and elite skips disagree in exactly the subtle positions where it matters, so the best-call baseline is reported with uncertainty and is never the headline number.

Phase 2 reuses all Phase 1 infrastructure and is only worth building once Phase 1 outputs have been reviewed.

---

## 12. Open Questions for Review

1. **Outcome clipping.** ±3 loses little; ±4 keeps rare big ends but thins the tails. Proposal: ±3 with +4 and above folded into +3.
2. **Lane boundaries and curl allowance** in the baseline features. Not worth tuning carefully; they are a baseline, and the raw-geometry model is expected to replace them.
3. **Shot type grouping.** Full types plus subtype on the full corpus; grouping only if the four local books force it.
4. **Free guard zone eras.** With the full corpus, fit both a pooled model with an era flag and per-era models, and compare (Section 3.6.7). Only f in early-end positions is affected; g and the skill model pool across eras.
5. **Men/Women pooling.** Jordan found small but real differences in shot selection. Proposal: pool with a gender flag; the data volume matters more. All stratum keys are retained so this can be revisited.
6. **Skill scalar granularity.** Per player is more informative but noisier; per team is stabler. Proposal: per player with a team-level prior (hierarchical), falling back to team when a player has few shots.
7. **Event tier mapping.** Starting assignment in Section 3.6.1; the regex table over directory event names is the source of truth. Whether the Olympic Qualification Event sits in tier 2 or tier 3 is a judgment call.
8. **Shots with missing or invalid types.** Keep in sequence for position continuity, exclude from g's training rows, include in f's.
9. **Ends ending early** (concessions, fewer than 16 shots). Treat the last recorded position as final and score it with the count function; verify against recorded score where available.
10. **Extraction backend.** Colour mask per style family vs. object detector; decided by the survey pass (3.6.3). Both are acceptable if they pass the validation gates.
11. **Raw-geometry encoding.** Set encoding vs. raster. Proposal: raster first (simpler to debug, subtlety probe is easy to run), set encoding if raster plateaus.
12. **Event effect granularity.** Event only, or event × sheet × session with shrinkage. Proposal: event first; add sheet once the full corpus is in, since a sheet effect needs many games to estimate.
13. **Game-state encoding for f and g.** Three candidates: (a) raw `score_diff` and `ends_remaining`, exact but sparse in the tails; (b) a small set of regime labels derived from v, dense but coarse (loses "up two in the 8th" vs "up two in the 9th"); (c) the v-vector itself — v(−2), v(−1), v(blank), v(+1), v(+2) for that game situation — continuous and dense, and carrying exactly the information the policy responds to. (c) is attractive but makes f depend on the win-probability table, so the two must be versioned together. Decide after the full corpus is in and the table exists.

---

## 13. Implementation Plan

One extractor, developed on the four local books and then run over the archive. The code lives in the `pointsgained` Python package in this repository.

| Milestone | Deliverable | Depends on |
|---|---|---|
| M1 | Ingestion of the four local books: page classification, diagram decoding and stone detection, panel text parsing, game/end/shot assembly with provenance, validation gates (3.6.5), Parquet output, contact sheet | — |
| M2 | Core geometry: count function, end-score reconstruction and cross-check, hammer inference, canonical-frame position assembly, mirroring; unit tests on hand-built positions | M1 |
| M3 | Value mapping (N, H, win-probability table from line scores) and first models: baseline features, f and g by gradient-boosted trees with event-level splits, Points Gained per shot with the conservation test, validation report (7.5), first leaderboards | M2 |
| M4 | Archive: inventory of the CURLIT directory (3.6.2), polite downloader, survey pass (3.6.3), batch extraction with gates written back to the inventory; per-era text variants | M1 |
| M5 | Refit on the validated archive; raw-geometry f and g with the subtlety probe; per-era and per-tier comparison | M3, M4 |
| M5b | Execution-grade model and per-thrower skill scalar; refit g with `skill` | M5 |
| M6 | Phase 2: simulator integration, execution error model (seeded by the delivered-stone marker), rollouts, best-call baseline | M5b, review of M5 |

M1 stone detection and M2 are where the judgment lives; everything after is mechanical.
