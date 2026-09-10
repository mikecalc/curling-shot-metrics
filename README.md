# Curling shot metrics: Points Gained

Shot-level metrics for the sport of curling, built from World Curling's shot-by-shot results books. The first metric is **Points Gained**, a shot-value measure by analogy with strokes gained in golf. Every shot is valued by
how much it changed the expected value of the end, decomposed into a selection component
(PG: Call) and an execution component (PG: Throw). The design is in `shot_value_design.md`.

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

# 3. Phase 1 models and Points Gained (reports/model_report.md, data/parquet/points_gained.parquet)
pointsgained model

# Archive: inventory of curlit.com/results, polite download, batch survey/extract/validate
pointsgained inventory --check
pointsgained download --tiers 1 2
pointsgained batch
```

## Layout

- `src/pointsgained/ingest/` PDF page classification, diagram decoding and stone detection, panel text parsing, book assembly, validation gates
- `src/pointsgained/core/` sheet geometry, the count function, canonical-frame position assembly
- `src/pointsgained/model/` value mappings (hammer-adjusted points, win probability), baseline features, f and g models, Points Gained, leaderboards
- `src/pointsgained/corpus/` archive inventory, event family and tier table, downloader, batch processing
- `tests/` unit tests
- `data/raw/` PDFs (not committed), `data/parquet/` extracted tables (not committed), `reports/` validation and model reports (not committed)

## Conventions

- Coordinates in inches, pin at (0, 0), y positive towards the hog line (in front of the tee).
- Positions are expressed in the canonical hammer-team frame; a thrower's value is the canonical value times +1 with hammer and -1 without. This makes the per-end conservation identity exact.
- End outcomes are clipped to [-3, +3] from the hammer team's perspective.

## Data and license

The code is MIT licensed (see `LICENSE`). The Results Books are published by World Curling and produced by CURLIT (`https://curlit.com/results`); they and the tables extracted from them are not part of this repository. Thanks to the CURLIT team for making the books available.
