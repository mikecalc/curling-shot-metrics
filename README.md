# Curling Analytics: shot-by-shot data, Points Gained, and studies

An open system for shot-by-shot curling analysis, with three major parts:

- **An ingestion pipeline** that reads World Curling's results books (the PDFs published for every major WCF event and
  the Olympics since 2013) and turns every stone of every end into tables: where each stone was after each shot, who
  threw it, what was called, how it was graded, and how the end and the game came out. Its table schema is the
  contract for any other source of games.
- **A corpus** built with it: 92 results books, 4,150 international games, 609,014 shots.
- **Points Gained**, an expectation model for curling positions and a value for every shot as the change it made to the
  end's expected result, split into the call and the execution, in points and in win probability. It rates execution,
  and it is the general tool the studies use to evaluate a position, a shot or a phase of the end.

On top of these sit sample studies: how often a double comes off by the separation and stagger of the two stones, how
often a runback works by the distance of the stone in front, what the first five rocks of an end decide, which skips
are best at runbacks, and per-event leaderboards for every Olympics and World Championship since 2018
(`reports/samples/`). The design document, `shot_value_design.md`, describes the pipeline and corpus (Part I), Points
Gained (Part II), the studies (Part III), and how to contribute (Part IV).

## Contributing

- **Data.** The most useful contribution is more games in shot-by-shot form: national championships (the Brier and the
  Scotties above all), the Grand Slams, and World Curling Tour events. Results books in the CURLIT format go straight
  through the pipeline; any other source needs an adapter into the six tables described in Section 2.6 of the design
  document. Line scores alone help too. If you hold or know of such data, please open an issue.
- **Points Gained.** The models, training targets and evaluation harness (`pointsgained experiment`) are all here, with
  a list of known weaknesses and the positions the model misprices (design document, Section 17).
- **Studies.** Every study reads the same tables: one row per stone with its values, the configuration of every
  position, and the extraction tables. `src/pointsgained/model/frontend.py` is a worked example, and the strategic
  situations in Section 15 of the design document are open.

For a wider view, `open_problems.md` sets out ten open problems in curling analytics in plain curling terms.

Data comes from World Curling shot-by-shot Results Books produced by CURLIT
(`https://curlit.com/results`). The per-shot diagrams in those PDFs are embedded 300x600
indexed-colour images, which this package decodes directly; no page rendering is involved.

## Setup

```
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## Pipeline

```
# 1. extract Results Books to Parquet (data/parquet/<book>/{games,ends,shots,stones,line_scores,players}.parquet)
pointsgained ingest data/raw/*.pdf

# 2. visual audit: random panels with detected stones overlaid
pointsgained audit data/raw/*.pdf --out reports/audit.png

# 3. feature cache: one row per shot and mirror with strata, situation, label and position features
#    (data/parquet/features.parquet; rebuilt automatically when the corpus or feature set changes)
pointsgained features

# 4. level of play: skill per player and effect per event from the grades (data/parquet/skill.parquet,
#    event_effects.parquet, shot_difficulty.parquet; reports/difficulty_report.md)
pointsgained difficulty

# 5. intent: the struck stone for hits, the modal target for draws (data/parquet/intent.parquet;
#    reports/execution_error.md seeds the Phase 2 error model)
pointsgained intent

# 6. models and Points Gained (reports/model_report.md, data/parquet/points_gained.parquet)
pointsgained model --features base,situation,level,intent,config --target local:2

# rewrite the model report's tables from the saved run, without refitting
pointsgained model-report

# the six pinned 2026 Olympic shots, both currencies, call at the reference and at the thrower's own skill
pointsgained testset

# 7. per-event player leaderboards (reports/events/<book>.md, one file per event, index in reports/events/README.md)
pointsgained events --match OWG2026 WMCC2026

# 8. one game shot by shot: ends, players, largest swings, every stone's values (reports/games/<game>.md)
pointsgained game --match OWG2026 Gold_Medal

# 9. the early-end study: front-end measures, configurations, doubles and runbacks by geometry, runbacks by player,
#    scenario probes (reports/front_end.md; configuration labels cached in data/parquet/configurations.parquet)
pointsgained frontend

# one modelling experiment: fit once on a split, score held out (reports/experiments/log.md)
pointsgained experiment --split time --features base,situation,level,intent,config --target local:2

# raw-geometry model (needs torch): time-split log-loss against the trees, subtlety probe, monotonicity
pointsgained raster --features base,situation,level,intent --epochs 6

# Archive: inventory of curlit.com/results, polite download, batch survey/extract/validate
pointsgained inventory --check
pointsgained download --tiers 1 2
pointsgained batch
```

## Layout

- `src/pointsgained/ingest/` PDF page classification, diagram decoding and stone detection, panel text parsing, book assembly, validation gates
- `src/pointsgained/core/` sheet geometry, the count function, canonical-frame position assembly, configurations (the position as a skip reads it)
- `src/pointsgained/model/` value mappings (hammer-adjusted points, win probability), baseline features, configuration features, training targets, f and g models, Points Gained, leaderboards, the front-end study
- `src/pointsgained/corpus/` archive inventory, event family and tier table, downloader, batch processing
- `tests/` unit tests
- `data/raw/` PDFs (not committed), `data/parquet/` extracted tables (not committed), `reports/` validation and model reports (not committed)
- `reports/samples/` finished reports kept in the repository: the model report, the pinned test set, per-event leaderboards for the 2026 Olympics and Worlds and for Beijing 2022, the two 2026 Olympic finals shot by shot, and the early-end study, with a README on how each is built and what it says

## Conventions

- Coordinates in inches, pin at (0, 0), y positive towards the hog line (in front of the tee).
- Positions are expressed in the canonical hammer-team frame; a thrower's value is the canonical value times +1 with hammer and -1 without. This makes the per-end conservation identity exact.
- End outcomes are clipped to [-3, +3] from the hammer team's perspective.

## Data and license

The code is MIT licensed (see `LICENSE`). The Results Books are published by World Curling and produced by CURLIT (`https://curlit.com/results`); they and the tables extracted from them are not part of this repository. Thanks to the CURLIT team for making the books available.
