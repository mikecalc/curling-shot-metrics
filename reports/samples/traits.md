# Rock traits

Every stone carries a vector of yes/no traits read off the position it is in (core/traits.py): `four_foot`, `eight_foot`, `twelve_foot`, `above_tee`, `behind_tee`, `wing`, `front`, `controls_4ft`, `guarding`, `shot_rock`, `second_shot`, `third_shot`, `frozen_own`, `frozen_opp`, `open`, `partly_open`, `behind_cover`. No tracking: the question is what positions whose stones carry a trait have been worth, not what happens to the stone.

Rows: 558,694 positions (after stones 1-15) from 37,623 ends. The result is the end's score for the hammer team: **pts** is the mean, then steal / blank / one / two-or-more in %. **Δ** columns are the difference from positions after the same stone in the same situation (discipline, score difference to ±2, two or fewer ends left), with 95% intervals clustered by end; Δ 2+ and Δ steal are percentage points.

## Baseline by stage

| stage        |      n |   pts |   steal |   blank |   one |   two |
|:-------------|-------:|------:|--------:|--------:|------:|------:|
| stones 1-5   | 185925 |  0.79 |   20.96 |   12.88 | 34.41 | 31.74 |
| stones 6-10  | 186380 |  0.79 |   21.02 |   12.58 | 34.52 | 31.88 |
| stones 11-15 | 186389 |  0.79 |   21.04 |   12.51 | 34.54 | 31.92 |

## 3a. How often each trait appears

% of positions in which the team has at least one stone with the trait.

| trait        |   hammer stones 1-5 |   hammer stones 6-10 |   hammer stones 11-15 |   non-hammer stones 1-5 |   non-hammer stones 6-10 |   non-hammer stones 11-15 |
|:-------------|--------------------:|---------------------:|----------------------:|------------------------:|-------------------------:|--------------------------:|
| four_foot    |                17.4 |                 30.3 |                  31.4 |                    40.5 |                     45.6 |                      43.8 |
| eight_foot   |                30.1 |                 56.7 |                  58.3 |                    57.1 |                     69.5 |                      71.2 |
| twelve_foot  |                38.5 |                 72.2 |                  74.4 |                    65.1 |                     81.2 |                      85.2 |
| above_tee    |                29.3 |                 54.7 |                  52.9 |                    52.7 |                     63.2 |                      64.9 |
| behind_tee   |                12.3 |                 33.2 |                  44.3 |                    18.6 |                     39.9 |                      54.7 |
| wing         |                12.7 |                 38.1 |                  46.5 |                     7.3 |                     31.8 |                      52.3 |
| front        |                45.7 |                 61.2 |                  60.3 |                    61.6 |                     57.9 |                      57.6 |
| controls_4ft |                15   |                 34   |                  33.2 |                    72.5 |                     61.1 |                      53.4 |
| guarding     |                15.3 |                 46.4 |                  51.5 |                    43.2 |                     53.8 |                      56   |
| shot_rock    |                26.2 |                 39.5 |                  39.8 |                    55.7 |                     56   |                      57.2 |
| second_shot  |                14.1 |                 35   |                  34.7 |                    21.5 |                     40.3 |                      44.6 |
| third_shot   |                 5.3 |                 22.7 |                  25   |                     5.4 |                     25   |                      33.6 |
| frozen_own   |                 0.6 |                  2.9 |                   4.3 |                     2.1 |                      4.2 |                       5.6 |
| frozen_opp   |                 2.4 |                  7.1 |                   8.9 |                     3.2 |                      7.7 |                       9.1 |
| open         |                57   |                 84.1 |                  84.4 |                    94.9 |                     87.8 |                      89.4 |
| partly_open  |                 8.6 |                 21.5 |                  26.3 |                    13.8 |                     25.3 |                      31   |
| behind_cover |                22.3 |                 38.8 |                  42.6 |                    28.5 |                     42.1 |                      47.2 |

Overlap between traits (Jaccard: share of stones with either trait that have both) is in `traits_overlap.csv`. Pairs above 0.5 (candidates to merge or to read together):

| a           | b           |   jaccard |
|:------------|:------------|----------:|
| eight_foot  | twelve_foot |      0.72 |
| twelve_foot | above_tee   |      0.62 |
| eight_foot  | above_tee   |      0.52 |
| four_foot   | eight_foot  |      0.51 |
| front       | open        |      0.51 |

## 3b. One trait at a time

Positions where the team has at least one stone with the trait against the rest, at each stage. `pts without` is the mean of the rest; Δ is against the same stone and situation (both with and without are in it), so a trait that comes with more stones in play is not separated from them here: section 3d does that. By discipline: `traits_effects_by_discipline.csv`.

### Hammer team, stones 1-5

| trait        |   share % |      n |   pts |   pts without | Δ pts         |   2+ % | Δ 2+      |   steal % | Δ steal    |
|:-------------|----------:|-------:|------:|--------------:|:--------------|-------:|:----------|----------:|:-----------|
| four_foot    |     17.43 |  32399 |  0.97 |          0.75 | 0.084 ± 0.029 |  36.76 | 3.1 ± 0.9 |     18.94 | -0.0 ± 0.7 |
| eight_foot   |     30.11 |  55991 |  0.94 |          0.72 | 0.077 ± 0.021 |  35.78 | 2.5 ± 0.7 |     18.95 | -0.4 ± 0.6 |
| twelve_foot  |     38.54 |  71655 |  0.91 |          0.71 | 0.06 ± 0.019  |  34.93 | 1.8 ± 0.6 |     19.04 | -0.5 ± 0.5 |
| above_tee    |     29.27 |  54412 |  0.94 |          0.72 | 0.082 ± 0.021 |  35.39 | 2.3 ± 0.7 |     18.24 | -1.3 ± 0.5 |
| behind_tee   |     12.34 |  22944 |  0.9  |          0.77 | 0.025 ± 0.034 |  34.9  | 1.4 ± 1.0 |     20.77 | 1.4 ± 0.9  |
| wing         |     12.72 |  23644 |  0.9  |          0.77 | 0.078 ± 0.029 |  34.19 | 1.6 ± 0.9 |     18.08 | -2.3 ± 0.7 |
| front        |     45.7  |  84964 |  0.76 |          0.81 | 0.037 ± 0.02  |  32.2  | 1.6 ± 0.6 |     23.01 | 0.6 ± 0.6  |
| controls_4ft |     15.04 |  27962 |  0.84 |          0.78 | -0.0 ± 0.03   |  33.27 | 0.4 ± 0.9 |     21.3  | 1.5 ± 0.8  |
| guarding     |     15.29 |  28422 |  0.9  |          0.77 | 0.098 ± 0.025 |  35.36 | 3.2 ± 0.8 |     20.9  | 0.3 ± 0.7  |
| shot_rock    |     26.24 |  48794 |  0.95 |          0.73 | 0.058 ± 0.023 |  35.57 | 1.7 ± 0.7 |     17.89 | -0.9 ± 0.6 |
| second_shot  |     14.13 |  26265 |  0.93 |          0.76 | 0.097 ± 0.024 |  35.92 | 3.2 ± 0.8 |     19.92 | -0.3 ± 0.6 |
| third_shot   |      5.32 |   9892 |  0.92 |          0.78 | 0.082 ± 0.036 |  35.78 | 2.8 ± 1.1 |     20.45 | 0.5 ± 1.0  |
| frozen_own   |      0.64 |   1195 |  1.15 |          0.78 | 0.207 ± 0.107 |  40.75 | 6.0 ± 3.5 |     16.32 | -2.4 ± 2.6 |
| frozen_opp   |      2.41 |   4472 |  0.85 |          0.78 | 0.046 ± 0.06  |  34.55 | 2.4 ± 1.9 |     21.98 | 1.9 ± 1.7  |
| open         |     56.95 | 105887 |  0.77 |          0.81 | 0.02 ± 0.017  |  31.88 | 0.7 ± 0.5 |     21.64 | -0.1 ± 0.5 |
| partly_open  |      8.62 |  16034 |  0.91 |          0.77 | 0.063 ± 0.034 |  35.52 | 2.5 ± 1.1 |     21.27 | 1.4 ± 0.9  |
| behind_cover |     22.35 |  41546 |  0.96 |          0.74 | 0.094 ± 0.025 |  36.97 | 3.6 ± 0.8 |     20.04 | 0.6 ± 0.7  |

### Non-Hammer team, stones 1-5

| trait        |   share % |      n |   pts |   pts without | Δ pts          |   2+ % | Δ 2+       |   steal % | Δ steal    |
|:-------------|----------:|-------:|------:|--------------:|:---------------|-------:|:-----------|----------:|:-----------|
| four_foot    |     40.53 |  75362 |  0.69 |          0.85 | -0.024 ± 0.022 |  30.35 | -0.2 ± 0.6 |     23.22 | 0.7 ± 0.6  |
| eight_foot   |     57.08 | 106125 |  0.72 |          0.88 | -0.012 ± 0.018 |  30.7  | -0.1 ± 0.5 |     22.33 | 0.2 ± 0.5  |
| twelve_foot  |     65.15 | 121130 |  0.73 |          0.89 | -0.006 ± 0.017 |  30.88 | -0.0 ± 0.5 |     21.89 | -0.0 ± 0.5 |
| above_tee    |     52.66 |  97900 |  0.71 |          0.87 | -0.022 ± 0.019 |  30.49 | -0.3 ± 0.6 |     22.33 | 0.3 ± 0.5  |
| behind_tee   |     18.6  |  34588 |  0.79 |          0.79 | 0.057 ± 0.03   |  32.1  | 1.3 ± 0.9  |     20.81 | -1.2 ± 0.8 |
| wing         |      7.26 |  13501 |  0.76 |          0.79 | -0.018 ± 0.035 |  29.08 | -2.3 ± 1.1 |     18.12 | -2.7 ± 0.9 |
| front        |     61.58 | 114495 |  0.86 |          0.66 | 0.019 ± 0.018  |  33.77 | 1.0 ± 0.6  |     21.29 | 1.6 ± 0.5  |
| controls_4ft |     72.5  | 134793 |  0.83 |          0.68 | 0.009 ± 0.017  |  32.92 | 0.6 ± 0.5  |     21.56 | 1.2 ± 0.5  |
| guarding     |     43.16 |  80247 |  0.83 |          0.75 | 0.029 ± 0.018  |  33.83 | 1.7 ± 0.6  |     22.11 | 1.4 ± 0.5  |
| shot_rock    |     55.68 | 103527 |  0.69 |          0.91 | -0.025 ± 0.019 |  29.81 | -0.6 ± 0.6 |     22.42 | 0.0 ± 0.5  |
| second_shot  |     21.53 |  40035 |  0.74 |          0.8  | -0.0 ± 0.023   |  31.53 | 0.5 ± 0.7  |     22.58 | 0.4 ± 0.6  |
| third_shot   |      5.39 |  10018 |  0.87 |          0.78 | 0.088 ± 0.034  |  34.38 | 2.6 ± 1.1  |     21.17 | -0.2 ± 0.9 |
| frozen_own   |      2.08 |   3872 |  0.62 |          0.79 | -0.095 ± 0.076 |  29.05 | -1.6 ± 2.0 |     25.85 | 2.7 ± 2.0  |
| frozen_opp   |      3.16 |   5883 |  0.83 |          0.78 | -0.047 ± 0.053 |  32.86 | -0.9 ± 1.7 |     21.43 | 2.8 ± 1.5  |
| open         |     94.86 | 176375 |  0.79 |          0.68 | 0.005 ± 0.015  |  32.02 | 0.3 ± 0.5  |     21.29 | 0.3 ± 0.4  |
| partly_open  |     13.77 |  25604 |  0.78 |          0.79 | -0.008 ± 0.028 |  32.07 | 0.2 ± 0.8  |     23.06 | 1.8 ± 0.8  |
| behind_cover |     28.52 |  53024 |  0.79 |          0.79 | 0.001 ± 0.021  |  32.54 | 0.8 ± 0.6  |     23.22 | 2.1 ± 0.6  |

### Hammer team, stones 6-10

| trait        |   share % |      n |   pts |   pts without | Δ pts         |   2+ % | Δ 2+      |   steal % | Δ steal    |
|:-------------|----------:|-------:|------:|--------------:|:--------------|-------:|:----------|----------:|:-----------|
| four_foot    |     30.33 |  56534 |  1    |          0.7  | 0.16 ± 0.026  |  38.52 | 5.7 ± 0.8 |     20.6  | 0.4 ± 0.7  |
| eight_foot   |     56.7  | 105669 |  0.96 |          0.57 | 0.146 ± 0.019 |  37.45 | 5.1 ± 0.6 |     20.13 | -0.6 ± 0.5 |
| twelve_foot  |     72.21 | 134582 |  0.91 |          0.47 | 0.11 ± 0.017  |  36.15 | 3.9 ± 0.5 |     20.18 | -0.7 ± 0.4 |
| above_tee    |     54.67 | 101889 |  0.96 |          0.58 | 0.16 ± 0.019  |  37.53 | 5.3 ± 0.6 |     19.48 | -1.3 ± 0.5 |
| behind_tee   |     33.22 |  61911 |  0.95 |          0.71 | 0.133 ± 0.025 |  37.89 | 5.3 ± 0.8 |     20.92 | 0.4 ± 0.6  |
| wing         |     38.13 |  71058 |  0.97 |          0.68 | 0.18 ± 0.022  |  37.86 | 5.9 ± 0.7 |     18.61 | -2.6 ± 0.6 |
| front        |     61.19 | 114037 |  0.76 |          0.84 | 0.002 ± 0.019 |  32.17 | 0.9 ± 0.6 |     23.45 | 1.7 ± 0.5  |
| controls_4ft |     33.98 |  63337 |  0.82 |          0.77 | 0.021 ± 0.024 |  34.24 | 2.0 ± 0.7 |     23.68 | 2.9 ± 0.7  |
| guarding     |     46.39 |  86471 |  0.9  |          0.69 | 0.117 ± 0.021 |  36.52 | 4.6 ± 0.6 |     22.84 | 1.5 ± 0.6  |
| shot_rock    |     39.47 |  73572 |  1.05 |          0.62 | 0.214 ± 0.02  |  39.46 | 6.7 ± 0.7 |     16.35 | -3.6 ± 0.5 |
| second_shot  |     35.03 |  65293 |  1.03 |          0.66 | 0.216 ± 0.022 |  39.88 | 7.4 ± 0.7 |     19.8  | -0.9 ± 0.6 |
| third_shot   |     22.72 |  42351 |  0.98 |          0.73 | 0.172 ± 0.028 |  38.86 | 6.4 ± 0.8 |     22.01 | 1.0 ± 0.7  |
| frozen_own   |      2.9  |   5405 |  1.17 |          0.78 | 0.316 ± 0.076 |  42.68 | 9.5 ± 2.3 |     20.26 | 0.2 ± 1.9  |
| frozen_opp   |      7.08 |  13198 |  0.86 |          0.78 | 0.096 ± 0.049 |  36.51 | 5.0 ± 1.5 |     24.53 | 3.0 ± 1.3  |
| open         |     84.06 | 156676 |  0.8  |          0.73 | 0.021 ± 0.016 |  32.66 | 0.9 ± 0.5 |     21.33 | 0.1 ± 0.4  |
| partly_open  |     21.54 |  40148 |  0.94 |          0.75 | 0.14 ± 0.027  |  37.79 | 5.5 ± 0.8 |     22.34 | 1.5 ± 0.7  |
| behind_cover |     38.8  |  72317 |  0.98 |          0.67 | 0.169 ± 0.023 |  39.01 | 6.6 ± 0.7 |     22.07 | 1.4 ± 0.6  |

### Non-Hammer team, stones 6-10

| trait        |   share % |      n |   pts |   pts without | Δ pts          |   2+ % | Δ 2+       |   steal % | Δ steal    |
|:-------------|----------:|-------:|------:|--------------:|:---------------|-------:|:-----------|----------:|:-----------|
| four_foot    |     45.56 |  84911 |  0.66 |          0.9  | -0.103 ± 0.022 |  29.6  | -1.9 ± 0.6 |     26.03 | 4.2 ± 0.6  |
| eight_foot   |     69.45 | 129445 |  0.73 |          0.93 | -0.048 ± 0.018 |  30.79 | -0.9 ± 0.5 |     23.88 | 2.4 ± 0.5  |
| twelve_foot  |     81.17 | 151290 |  0.76 |          0.91 | -0.018 ± 0.017 |  31.5  | -0.2 ± 0.5 |     22.87 | 1.5 ± 0.5  |
| above_tee    |     63.25 | 117878 |  0.72 |          0.91 | -0.054 ± 0.018 |  30.59 | -1.1 ± 0.5 |     23.86 | 2.3 ± 0.5  |
| behind_tee   |     39.89 |  74344 |  0.79 |          0.79 | 0.025 ± 0.023  |  32.51 | 1.0 ± 0.7  |     22.85 | 1.3 ± 0.6  |
| wing         |     31.79 |  59254 |  0.8  |          0.79 | 0.033 ± 0.024  |  31.98 | 0.6 ± 0.7  |     21.32 | -0.2 ± 0.6 |
| front        |     57.9  | 107919 |  0.86 |          0.69 | 0.05 ± 0.019   |  34.82 | 2.6 ± 0.6  |     22.67 | 2.1 ± 0.5  |
| controls_4ft |     61.11 | 113893 |  0.8  |          0.77 | -0.003 ± 0.019 |  33.14 | 1.0 ± 0.6  |     23.88 | 3.0 ± 0.5  |
| guarding     |     53.84 | 100346 |  0.82 |          0.75 | 0.022 ± 0.02   |  34.25 | 2.1 ± 0.6  |     24.46 | 3.5 ± 0.5  |
| shot_rock    |     56.01 | 104383 |  0.62 |          1.01 | -0.135 ± 0.019 |  27.4  | -3.8 ± 0.5 |     24.83 | 3.0 ± 0.5  |
| second_shot  |     40.33 |  75161 |  0.69 |          0.85 | -0.071 ± 0.022 |  30.18 | -1.3 ± 0.6 |     24.57 | 2.8 ± 0.6  |
| third_shot   |     25.05 |  46680 |  0.8  |          0.79 | 0.031 ± 0.027  |  34.06 | 2.4 ± 0.8  |     24.16 | 2.5 ± 0.7  |
| frozen_own   |      4.19 |   7812 |  0.56 |          0.8  | -0.194 ± 0.067 |  28.73 | -2.6 ± 1.7 |     30.18 | 8.0 ± 1.8  |
| frozen_opp   |      7.65 |  14261 |  0.86 |          0.78 | -0.003 ± 0.047 |  34.03 | 0.7 ± 1.4  |     23.79 | 4.0 ± 1.3  |
| open         |     87.83 | 163696 |  0.8  |          0.73 | 0.009 ± 0.016  |  32.3  | 0.4 ± 0.5  |     21.74 | 0.7 ± 0.4  |
| partly_open  |     25.32 |  47192 |  0.75 |          0.8  | -0.029 ± 0.026 |  32.09 | 0.4 ± 0.7  |     25.6  | 4.1 ± 0.7  |
| behind_cover |     42.11 |  78483 |  0.74 |          0.82 | -0.039 ± 0.022 |  32.13 | 0.4 ± 0.6  |     26    | 4.7 ± 0.6  |

### Hammer team, stones 11-15

| trait        |   share % |      n |   pts |   pts without | Δ pts          |   2+ % | Δ 2+       |   steal % | Δ steal    |
|:-------------|----------:|-------:|------:|--------------:|:---------------|-------:|:-----------|----------:|:-----------|
| four_foot    |     31.4  |  58517 |  1.14 |          0.63 | 0.33 ± 0.024   |  43.8  | 11.4 ± 0.8 |     20.1  | -0.8 ± 0.6 |
| eight_foot   |     58.31 | 108675 |  1.06 |          0.41 | 0.261 ± 0.019  |  42.57 | 10.4 ± 0.6 |     20.41 | -0.7 ± 0.5 |
| twelve_foot  |     74.43 | 138730 |  0.98 |          0.24 | 0.185 ± 0.017  |  40.08 | 8.0 ± 0.5  |     20.75 | -0.3 ± 0.4 |
| above_tee    |     52.93 |  98657 |  1.05 |          0.49 | 0.255 ± 0.02   |  42.39 | 10.2 ± 0.6 |     20.52 | -0.5 ± 0.5 |
| behind_tee   |     44.35 |  82662 |  1.06 |          0.57 | 0.259 ± 0.022  |  42.45 | 10.1 ± 0.7 |     20.92 | -0.0 ± 0.6 |
| wing         |     46.47 |  86622 |  1.08 |          0.54 | 0.287 ± 0.021  |  43.4  | 11.3 ± 0.7 |     19.14 | -2.0 ± 0.5 |
| front        |     60.33 | 112450 |  0.74 |          0.87 | -0.041 ± 0.02  |  31.33 | -0.3 ± 0.6 |     24.65 | 3.3 ± 0.6  |
| controls_4ft |     33.2  |  61878 |  0.78 |          0.79 | -0.019 ± 0.027 |  34.41 | 2.2 ± 0.8  |     27.18 | 6.3 ± 0.7  |
| guarding     |     51.51 |  96014 |  0.9  |          0.67 | 0.118 ± 0.022  |  37.68 | 5.8 ± 0.6  |     25.04 | 3.7 ± 0.6  |
| shot_rock    |     39.8  |  74179 |  1.33 |          0.43 | 0.522 ± 0.018  |  49.39 | 17.0 ± 0.6 |     11.28 | -9.3 ± 0.4 |
| second_shot  |     34.68 |  64636 |  1.26 |          0.54 | 0.457 ± 0.022  |  49.92 | 17.6 ± 0.7 |     19.68 | -1.2 ± 0.5 |
| third_shot   |     24.98 |  46568 |  1.04 |          0.71 | 0.23 ± 0.028   |  40.61 | 8.1 ± 0.8  |     25.54 | 4.5 ± 0.7  |
| frozen_own   |      4.27 |   7958 |  1.24 |          0.77 | 0.432 ± 0.075  |  45.46 | 13.0 ± 2.0 |     22.25 | 1.5 ± 1.7  |
| frozen_opp   |      8.91 |  16611 |  0.84 |          0.79 | 0.075 ± 0.043  |  36.16 | 4.6 ± 1.3  |     26.68 | 4.9 ± 1.2  |
| open         |     84.36 | 157242 |  0.83 |          0.6  | 0.037 ± 0.016  |  33.87 | 2.0 ± 0.5  |     21.8  | 0.7 ± 0.4  |
| partly_open  |     26.31 |  49041 |  1.01 |          0.71 | 0.216 ± 0.027  |  40.9  | 8.7 ± 0.8  |     23.32 | 2.3 ± 0.7  |
| behind_cover |     42.59 |  79386 |  1.02 |          0.62 | 0.22 ± 0.023   |  41.52 | 9.4 ± 0.7  |     23.56 | 2.5 ± 0.6  |

### Non-Hammer team, stones 11-15

| trait        |   share % |      n |   pts |   pts without | Δ pts          |   2+ % | Δ 2+        |   steal % | Δ steal    |
|:-------------|----------:|-------:|------:|--------------:|:---------------|-------:|:------------|----------:|:-----------|
| four_foot    |     43.77 |  81587 |  0.52 |          1    | -0.265 ± 0.022 |  26.08 | -5.7 ± 0.6  |     31.21 | 9.7 ± 0.6  |
| eight_foot   |     71.15 | 132624 |  0.67 |          1.09 | -0.114 ± 0.018 |  28.82 | -3.0 ± 0.5  |     25.91 | 4.6 ± 0.5  |
| twelve_foot  |     85.17 | 158752 |  0.75 |          1.04 | -0.038 ± 0.016 |  30.7  | -1.1 ± 0.5  |     23.55 | 2.3 ± 0.5  |
| above_tee    |     64.92 | 120996 |  0.67 |          1.01 | -0.109 ± 0.018 |  29.12 | -2.6 ± 0.5  |     25.9  | 4.5 ± 0.5  |
| behind_tee   |     54.7  | 101951 |  0.76 |          0.83 | -0.018 ± 0.02  |  31.21 | -0.5 ± 0.6  |     24.13 | 2.7 ± 0.6  |
| wing         |     52.26 |  97408 |  0.8  |          0.78 | 0.031 ± 0.02   |  31.6  | 0.0 ± 0.6   |     21.84 | 0.4 ± 0.5  |
| front        |     57.64 | 107429 |  0.85 |          0.71 | 0.051 ± 0.02   |  35.25 | 3.2 ± 0.6   |     23.42 | 2.6 ± 0.5  |
| controls_4ft |     53.37 |  99475 |  0.74 |          0.84 | -0.052 ± 0.021 |  32.67 | 0.6 ± 0.6   |     26.58 | 5.6 ± 0.6  |
| guarding     |     56.05 | 104462 |  0.79 |          0.79 | 0.0 ± 0.021    |  34.56 | 2.6 ± 0.6   |     27.05 | 5.9 ± 0.6  |
| shot_rock    |     57.21 | 106630 |  0.43 |          1.27 | -0.341 ± 0.017 |  20.86 | -10.7 ± 0.4 |     28.47 | 7.1 ± 0.5  |
| second_shot  |     44.65 |  83221 |  0.59 |          0.95 | -0.183 ± 0.02  |  25.97 | -5.6 ± 0.5  |     26.76 | 5.1 ± 0.6  |
| third_shot   |     33.57 |  62563 |  0.78 |          0.8  | 0.016 ± 0.024  |  35.12 | 3.6 ± 0.7   |     25.23 | 3.5 ± 0.6  |
| frozen_own   |      5.57 |  10376 |  0.4  |          0.81 | -0.368 ± 0.063 |  26.09 | -5.5 ± 1.5  |     35.31 | 13.5 ± 1.6 |
| frozen_opp   |      9.06 |  16884 |  0.85 |          0.78 | 0.032 ± 0.042  |  34.35 | 1.8 ± 1.3   |     26.1  | 5.4 ± 1.2  |
| open         |     89.37 | 166575 |  0.79 |          0.81 | -0.0 ± 0.016   |  31.99 | 0.1 ± 0.5   |     21.91 | 0.8 ± 0.4  |
| partly_open  |     30.99 |  57754 |  0.69 |          0.83 | -0.082 ± 0.025 |  31.37 | -0.3 ± 0.7  |     27.86 | 6.4 ± 0.7  |
| behind_cover |     47.23 |  88024 |  0.66 |          0.9  | -0.119 ± 0.022 |  30.51 | -1.3 ± 0.6  |     29.18 | 7.8 ± 0.6  |

## 3c. Stone types

A stone's type is its whole trait vector (the nested rings shown once). How far exact lookup can go:

| stage        |   stones |   types |   types_with_500+ |   stones_in_top_30_% |   stones_in_types_500+_% |
|:-------------|---------:|--------:|------------------:|---------------------:|-------------------------:|
| stones 1-5   |   476531 |    1139 |               105 |                 72.3 |                     89.1 |
| stones 6-10  |   789057 |    1817 |               259 |                 51.6 |                     89.5 |
| stones 11-15 |   954847 |    2078 |               306 |                 46.6 |                     89.5 |

### One stone in play

Positions with exactly one stone in play after stone 1, 2 or 3, by that stone's team and type (40 or more).

|   shot | team       |     n | stone                                             |   pts |   steal |   blank |   one |   two |   d_pts |   ci_pts |   d_two |   ci_two |   d_steal |   ci_steal |
|-------:|:-----------|------:|:--------------------------------------------------|------:|--------:|--------:|------:|------:|--------:|---------:|--------:|---------:|----------:|-----------:|
|      1 | non-hammer |   163 | front+open                                        |  1.11 |   19.02 |   10.43 | 30.06 | 40.49 |    0.24 |     0.23 |    7.09 |     7.51 |     -0.64 |       6.05 |
|      1 | non-hammer | 18267 | front+controls_4ft+open                           |  0.88 |   20.7  |   10.87 | 34.72 | 33.71 |    0.01 |     0.02 |    0.54 |     0.68 |      1.55 |       0.58 |
|      1 | non-hammer |    75 | four_foot+shot_rock+open                          |  0.73 |   17.33 |   13.33 | 44    | 25.33 |    0.07 |     0.28 |   -4.53 |     9.82 |     -6.67 |       8.47 |
|      1 | non-hammer |   162 | eight_foot+above_tee+shot_rock+open               |  0.75 |   21.6  |    7.41 | 39.51 | 31.48 |    0.05 |     0.23 |    1.36 |     7.17 |     -1.07 |       6.31 |
|      1 | non-hammer |  8905 | four_foot+above_tee+shot_rock+open                |  0.62 |   22.32 |   15.36 | 34.08 | 28.23 |   -0.05 |     0.03 |   -1.41 |     0.93 |     -0.85 |       0.86 |
|      1 | non-hammer |   340 | twelve_foot+behind_tee+shot_rock+open             |  0.86 |   17.94 |   14.71 | 36.76 | 30.59 |    0.17 |     0.15 |    0.81 |     4.85 |     -4.71 |       4.04 |
|      1 | non-hammer |   758 | eight_foot+behind_tee+shot_rock+open              |  0.85 |   17.15 |   14.12 | 35.62 | 33.11 |    0.17 |     0.1  |    3.53 |     3.35 |     -5.75 |       2.66 |
|      1 | non-hammer |  2749 | four_foot+behind_tee+shot_rock+open               |  0.68 |   20.41 |   15.97 | 34.67 | 28.96 |    0    |     0.06 |   -0.69 |     1.69 |     -2.6  |       1.49 |
|      1 | non-hammer |  2186 | twelve_foot+above_tee+controls_4ft+shot_rock+open |  0.78 |   19.62 |   16.74 | 31.43 | 32.2  |    0.02 |     0.06 |    0.89 |     1.96 |     -1.55 |       1.65 |
|      1 | non-hammer |  3137 | eight_foot+above_tee+controls_4ft+shot_rock+open  |  0.69 |   21.39 |   15.46 | 34.01 | 29.14 |   -0.01 |     0.05 |   -0.95 |     1.59 |     -1.07 |       1.42 |
|      2 | hammer     |   123 | open                                              |  0.39 |   17.07 |   42.28 | 25.2  | 15.45 |   -0.41 |     0.19 |  -16.2  |     6.4  |     -2.07 |       6.58 |
|      2 | hammer     |   541 | front+open                                        |  1.02 |   16.82 |   10.72 | 33.09 | 39.37 |    0.27 |     0.12 |    7.76 |     4.12 |     -5.45 |       3.19 |
|      2 | hammer     |   197 | front+controls_4ft+open                           |  0.93 |   17.26 |   15.74 | 29.95 | 37.06 |    0.09 |     0.2  |    4.01 |     6.66 |     -1.94 |       5.26 |
|      2 | hammer     |    64 | eight_foot+above_tee+shot_rock+open               |  0.53 |   12.5  |   45.31 | 25    | 17.19 |   -0.26 |     0.29 |  -14.4  |     9.19 |     -6.37 |       7.91 |
|      2 | hammer     |   591 | four_foot+above_tee+shot_rock+open                |  0.46 |    9.64 |   52.62 | 20.98 | 16.75 |   -0.32 |     0.09 |  -14.67 |     3.01 |     -8.96 |       2.36 |
|      2 | hammer     |    43 | eight_foot+behind_tee+shot_rock+open              |  0.42 |    6.98 |   55.81 | 18.6  | 18.6  |   -0.41 |     0.36 |  -14.18 |    11.64 |    -11.02 |       7.55 |
|      2 | hammer     |   135 | four_foot+behind_tee+shot_rock+open               |  0.39 |    7.41 |   54.81 | 22.22 | 15.56 |   -0.42 |     0.23 |  -16.53 |     6.12 |    -10.7  |       4.48 |
|      2 | hammer     |   365 | twelve_foot+above_tee+wing+shot_rock+open         |  0.71 |   13.15 |   34.52 | 24.38 | 27.95 |   -0.17 |     0.15 |   -6    |     4.63 |     -5.17 |       3.46 |
|      2 | hammer     |   298 | eight_foot+above_tee+wing+shot_rock+open          |  0.67 |    9.73 |   40.94 | 24.16 | 25.17 |   -0.15 |     0.14 |   -7.22 |     4.92 |     -9.02 |       3.34 |
|      2 | hammer     |   223 | twelve_foot+behind_tee+wing+shot_rock+open        |  0.7  |    9.87 |   38.12 | 26.91 | 25.11 |   -0.11 |     0.15 |   -6.68 |     5.67 |     -8.71 |       3.9  |
|      2 | hammer     |   169 | eight_foot+behind_tee+wing+shot_rock+open         |  0.79 |    7.1  |   37.87 | 27.81 | 27.22 |   -0.03 |     0.17 |   -5.01 |     6.7  |    -11.12 |       3.87 |
|      2 | hammer     |   298 | twelve_foot+above_tee+controls_4ft+shot_rock+open |  0.73 |   12.75 |   34.23 | 25.5  | 27.52 |   -0.13 |     0.14 |   -5.72 |     4.99 |     -5.5  |       3.78 |
|      2 | hammer     |   394 | eight_foot+above_tee+controls_4ft+shot_rock+open  |  0.57 |   10.66 |   44.92 | 24.11 | 20.3  |   -0.24 |     0.12 |  -11.82 |     3.93 |     -7.62 |       2.97 |
|      2 | non-hammer |    75 | front+open                                        |  0.83 |   14.67 |    4    | 61.33 | 20    |   -0.07 |     0.23 |  -11.43 |     8.62 |     -6.88 |       7.99 |
|      2 | non-hammer |   944 | front+controls_4ft+open                           |  0.61 |   25.64 |    9.43 | 42.06 | 22.88 |   -0.28 |     0.09 |   -9.28 |     2.62 |      5.22 |       2.76 |
|      2 | non-hammer |   164 | four_foot+above_tee+shot_rock+open                |  0.18 |   33.54 |   15.85 | 31.1  | 19.51 |   -0.52 |     0.25 |  -10.54 |     6.08 |     11.36 |       7.14 |
|      2 | non-hammer |    55 | four_foot+behind_tee+shot_rock+open               |  0.33 |   21.82 |   30.91 | 27.27 | 20    |   -0.37 |     0.39 |  -10.02 |    10.58 |     -0.45 |      10.76 |
|      2 | non-hammer |    48 | twelve_foot+above_tee+controls_4ft+shot_rock+open |  0.21 |   33.33 |   12.5  | 29.17 | 25    |   -0.54 |     0.55 |   -5.95 |    11.9  |     12.19 |      12.9  |
|      2 | non-hammer |    62 | eight_foot+above_tee+controls_4ft+shot_rock+open  |  0.39 |   29.03 |   12.9  | 33.87 | 24.19 |   -0.33 |     0.36 |   -6.24 |    10.59 |      6.69 |      11.13 |
|      3 | hammer     |   166 | front+open                                        |  1.25 |    6.63 |    6.02 | 51.2  | 36.14 |    0.57 |     0.15 |    4.07 |     7.31 |    -19.41 |       3.84 |
|      3 | non-hammer |    59 | open                                              |  0.63 |   18.64 |   33.9  | 18.64 | 28.81 |   -0.14 |     0.32 |   -2.33 |    11.55 |     -0.53 |       9.86 |
|      3 | non-hammer |    69 | front+open                                        |  0.7  |   20.29 |   23.19 | 26.09 | 30.43 |   -0.1  |     0.35 |   -1.19 |    10.81 |      1.51 |       9.57 |
|      3 | non-hammer |   479 | front+controls_4ft+open                           |  0.66 |   20.88 |   19.21 | 35.49 | 24.43 |   -0.18 |     0.13 |   -7.99 |     3.81 |      1.9  |       3.6  |
|      3 | non-hammer |    54 | eight_foot+above_tee+shot_rock+open               |  0.33 |   14.81 |   44.44 | 24.07 | 16.67 |   -0.41 |     0.3  |  -13.8  |    10.01 |     -4.89 |       9.17 |
|      3 | non-hammer |   514 | four_foot+above_tee+shot_rock+open                |  0.31 |   12.26 |   50.58 | 25.29 | 11.87 |   -0.44 |     0.1  |  -18.75 |     2.8  |     -7.5  |       2.79 |
|      3 | non-hammer |    75 | eight_foot+behind_tee+shot_rock+open              |  0.8  |    5.33 |   38.67 | 29.33 | 26.67 |    0.05 |     0.26 |   -4.01 |    10.09 |    -13.95 |       4.96 |
|      3 | non-hammer |   172 | four_foot+behind_tee+shot_rock+open               |  0.3  |   12.21 |   45.35 | 30.23 | 12.21 |   -0.45 |     0.23 |  -18.42 |     4.91 |     -7.68 |       4.92 |
|      3 | non-hammer |   232 | twelve_foot+above_tee+wing+shot_rock+open         |  0.54 |   10.34 |   46.12 | 21.55 | 21.98 |   -0.25 |     0.15 |   -9.59 |     5.32 |     -8.1  |       3.89 |
|      3 | non-hammer |   245 | eight_foot+above_tee+wing+shot_rock+open          |  0.4  |   10.61 |   48.98 | 24.49 | 15.92 |   -0.37 |     0.14 |  -15    |     4.59 |     -8.44 |       3.77 |
|      3 | non-hammer |   125 | twelve_foot+behind_tee+wing+shot_rock+open        |  0.48 |    9.6  |   50.4  | 22.4  | 17.6  |   -0.29 |     0.18 |  -13.18 |     6.67 |     -8.96 |       5.12 |
|      3 | non-hammer |   106 | eight_foot+behind_tee+wing+shot_rock+open         |  0.53 |    6.6  |   52.83 | 21.7  | 18.87 |   -0.25 |     0.22 |  -12.2  |     7.49 |    -11.54 |       4.71 |
|      3 | non-hammer |   206 | twelve_foot+above_tee+controls_4ft+shot_rock+open |  0.52 |   10.19 |   45.63 | 25.73 | 18.45 |   -0.27 |     0.15 |  -13.05 |     5.31 |     -8.75 |       4.01 |
|      3 | non-hammer |   355 | eight_foot+above_tee+controls_4ft+shot_rock+open  |  0.4  |   11.27 |   49.86 | 25.35 | 13.52 |   -0.38 |     0.1  |  -17.66 |     3.57 |     -7.55 |       3.22 |

### Two stones in play after stone 2

The 25 most common pairs of types (`H:` hammer team, `N:` non-hammer).

|   shot | pair                                                                                               |    n |   pts |   steal |   blank |   one |   two |   d_pts |   ci_pts |   d_two |   ci_two |   d_steal |   ci_steal |
|-------:|:---------------------------------------------------------------------------------------------------|-----:|------:|--------:|--------:|------:|------:|--------:|---------:|--------:|---------:|----------:|-----------:|
|      2 | H: front+open / N: four_foot+above_tee+shot_rock+open                                              | 6709 |  0.66 |   24.49 |    8.87 | 35.68 | 30.96 |   -0    |     0.04 |    1.32 |     1.1  |      0.64 |       1.02 |
|      2 | H: front+open / N: front+controls_4ft+open                                                         | 4415 |  0.84 |   22.72 |    7.84 | 34.93 | 34.52 |    0.05 |     0.04 |    2.6  |     1.4  |      2.39 |       1.23 |
|      2 | H: four_foot+above_tee+shot_rock+behind_cover / N: front+controls_4ft+guarding+open                | 3068 |  1.07 |   16.1  |   12.42 | 31.88 | 39.6  |    0.15 |     0.05 |    5.35 |     1.72 |     -2.12 |       1.3  |
|      2 | H: front+open / N: eight_foot+above_tee+controls_4ft+shot_rock+open                                | 2304 |  0.72 |   23.74 |    8.64 | 36.37 | 31.25 |    0.04 |     0.06 |    1.36 |     1.89 |      0.37 |       1.73 |
|      2 | H: front+open / N: four_foot+behind_tee+shot_rock+open                                             | 2077 |  0.76 |   21.95 |    8.91 | 37.17 | 31.97 |    0.09 |     0.07 |    2.25 |     2    |     -1.68 |       1.77 |
|      2 | H: eight_foot+above_tee+controls_4ft+shot_rock+behind_cover / N: front+controls_4ft+guarding+open  | 1343 |  0.94 |   18.24 |   12.96 | 33.8  | 35    |    0.03 |     0.07 |    0.79 |     2.54 |      0.05 |       2.06 |
|      2 | H: front+open / N: twelve_foot+above_tee+controls_4ft+shot_rock+open                               | 1246 |  0.83 |   21.75 |    8.99 | 33.95 | 35.31 |    0.14 |     0.08 |    5.08 |     2.65 |     -1.11 |       2.28 |
|      2 | H: four_foot+above_tee+shot_rock+partly_open / N: front+controls_4ft+guarding+open                 |  963 |  1.01 |   17.24 |   10.8  | 37.59 | 34.37 |    0.09 |     0.09 |   -0.09 |     2.96 |     -1.41 |       2.38 |
|      2 | H: four_foot+behind_tee+shot_rock+behind_cover / N: front+controls_4ft+guarding+open               |  830 |  0.85 |   23.25 |    9.64 | 33.25 | 33.86 |   -0.06 |     0.1  |   -0.57 |     3.19 |      4.84 |       2.86 |
|      2 | H: front+open / N: eight_foot+behind_tee+shot_rock+open                                            |  573 |  0.88 |   18.5  |   10.12 | 37.52 | 33.86 |    0.2  |     0.12 |    4.13 |     3.88 |     -4.9  |       3.16 |
|      2 | H: twelve_foot+behind_tee+wing+shot_rock+open / N: front+controls_4ft+open                         |  491 |  0.82 |   21.18 |   15.07 | 31.57 | 32.18 |   -0.12 |     0.13 |   -2.68 |     4.16 |      2.66 |       3.61 |
|      2 | H: twelve_foot+above_tee+wing+shot_rock+open / N: front+controls_4ft+open                          |  483 |  0.69 |   24.02 |   14.91 | 32.09 | 28.99 |   -0.2  |     0.14 |   -4.67 |     4.04 |      4.77 |       3.81 |
|      2 | H: eight_foot+above_tee+controls_4ft+shot_rock+partly_open / N: front+controls_4ft+guarding+open   |  438 |  0.98 |   17.81 |   16.21 | 29.45 | 36.53 |    0.07 |     0.13 |    1.98 |     4.48 |     -0.45 |       3.56 |
|      2 | H: eight_foot+behind_tee+wing+shot_rock+open / N: front+controls_4ft+open                          |  423 |  0.86 |   20.8  |   16.31 | 31.21 | 31.68 |   -0.07 |     0.15 |   -2.87 |     4.44 |      1.82 |       3.86 |
|      2 | H: front+open / N: front+open                                                                      |  409 |  0.88 |   18.58 |    6.6  | 50.37 | 24.45 |   -0.03 |     0.12 |   -7.79 |     4.04 |     -2.16 |       3.76 |
|      2 | H: eight_foot+behind_tee+shot_rock+behind_cover / N: front+controls_4ft+guarding+open              |  371 |  0.95 |   19.95 |    8.89 | 36.66 | 34.5  |    0.05 |     0.15 |    0.46 |     4.79 |      1.53 |       4.04 |
|      2 | H: four_foot+behind_tee+shot_rock+partly_open / N: front+controls_4ft+guarding+open                |  352 |  0.92 |   21.88 |   10.51 | 30.68 | 36.93 |    0.02 |     0.17 |    2.76 |     4.98 |      3.46 |       4.29 |
|      2 | H: twelve_foot+above_tee+controls_4ft+shot_rock+behind_cover / N: front+controls_4ft+guarding+open |  321 |  0.81 |   23.68 |    8.72 | 35.51 | 32.09 |   -0.08 |     0.16 |   -1.83 |     5.07 |      5.13 |       4.62 |
|      2 | H: front+controls_4ft+open / N: front+controls_4ft+open                                            |  320 |  0.57 |   31.87 |    6.88 | 32.5  | 28.75 |   -0.26 |     0.18 |   -4.15 |     5    |     12.31 |       5.1  |
|      2 | H: eight_foot+above_tee+wing+shot_rock+open / N: front+controls_4ft+open                           |  318 |  0.92 |   19.5  |   12.89 | 34.59 | 33.02 |   -0    |     0.17 |   -1.88 |     5.17 |      0.48 |       4.31 |
|      2 | H: twelve_foot+above_tee+wing+second_shot+open / N: four_foot+above_tee+shot_rock+open             |  253 |  0.56 |   19.76 |   17.79 | 39.13 | 23.32 |   -0.1  |     0.18 |   -6.02 |     5.22 |     -3.96 |       4.85 |
|      2 | H: front+open / N: twelve_foot+behind_tee+shot_rock+open                                           |  240 |  0.95 |   17.08 |   10.83 | 38.75 | 33.33 |    0.26 |     0.17 |    3.46 |     5.9  |     -5.53 |       4.75 |
|      2 | H: four_foot+above_tee+shot_rock+open / N: front+controls_4ft+open                                 |  239 |  0.84 |   22.18 |   15.48 | 27.62 | 34.73 |   -0.08 |     0.19 |    0.51 |     5.94 |      3.71 |       5.28 |
|      2 | H: twelve_foot+above_tee+controls_4ft+shot_rock+partly_open / N: front+controls_4ft+guarding+open  |  201 |  0.9  |   19.4  |   11.44 | 35.32 | 33.83 |    0.01 |     0.21 |    0.12 |     6.46 |      1.2  |       5.42 |
|      2 | H: eight_foot+behind_tee+shot_rock+partly_open / N: front+controls_4ft+guarding+open               |  184 |  0.78 |   26.09 |   11.41 | 32.61 | 29.89 |   -0.1  |     0.23 |   -3.58 |     6.6  |      7.43 |       6.31 |

## 3d. Additive grades

Per stage, a linear fit of the end's result on each team's trait counts, with the stone number and the situation as stratum effects. `stone` is the weight of the reference stone, an open guard (a stone in front of the house with nothing in front of it); every other weight is what that trait adds to a stone that has it, holding the others fixed. The rings are nested, so a 4-foot stone gets four_foot + eight_foot + twelve_foot. A stone's grade is `stone` plus its traits' weights, always from the hammer team's side (a non-hammer stone that helps its team has a negative grade).

### Weights, hammer points

| trait        |   hammer stones 1-5 |   hammer stones 6-10 |   hammer stones 11-15 |   non-hammer stones 1-5 |   non-hammer stones 6-10 |   non-hammer stones 11-15 |
|:-------------|--------------------:|---------------------:|----------------------:|------------------------:|-------------------------:|--------------------------:|
| stone        |               0.288 |                0.101 |                 0.007 |                   0.083 |                    0.077 |                     0.056 |
| four_foot    |              -0.05  |               -0.052 |                 0.025 |                  -0.103 |                   -0.12  |                    -0.174 |
| eight_foot   |               0.086 |                0.068 |                 0.079 |                  -0.042 |                   -0.068 |                    -0.078 |
| twelve_foot  |              -0.205 |                0.146 |                 0.11  |                  -0.078 |                   -0.157 |                    -0.053 |
| above_tee    |               0.122 |               -0.013 |                 0.026 |                   0.027 |                    0.114 |                    -0.009 |
| behind_tee   |               0.01  |               -0.126 |                -0.064 |                   0.102 |                    0.172 |                     0.083 |
| wing         |               0.014 |                0.014 |                 0.018 |                  -0.051 |                   -0.037 |                    -0     |
| controls_4ft |              -0.112 |               -0.088 |                -0.096 |                  -0.083 |                   -0.1   |                    -0.094 |
| guarding     |               0.058 |                0.061 |                 0.032 |                   0.029 |                   -0.038 |                    -0.101 |
| shot_rock    |               0.062 |                0.101 |                 0.602 |                   0.021 |                   -0.091 |                    -0.243 |
| second_shot  |               0.117 |                0.246 |                 0.799 |                   0.051 |                    0.089 |                     0.207 |
| third_shot   |               0.118 |                0.104 |                 0.236 |                   0.066 |                    0.006 |                    -0.01  |
| frozen_own   |               0.009 |                0.013 |                 0.067 |                  -0.055 |                   -0.008 |                    -0.016 |
| frozen_opp   |               0.005 |                0.035 |                 0.075 |                  -0.143 |                   -0.111 |                    -0.142 |
| partly_open  |               0.016 |                0.018 |                 0.054 |                  -0.108 |                   -0.061 |                    -0.059 |
| behind_cover |               0.051 |                0.07  |                 0.078 |                  -0.125 |                   -0.114 |                    -0.127 |

### Weights, two-or-more (percentage points)

| trait        |   hammer stones 1-5 |   hammer stones 6-10 |   hammer stones 11-15 |   non-hammer stones 1-5 |   non-hammer stones 6-10 |   non-hammer stones 11-15 |
|:-------------|--------------------:|---------------------:|----------------------:|------------------------:|-------------------------:|--------------------------:|
| stone        |                10.4 |                  4.7 |                   1.2 |                     2.6 |                      3.1 |                       1.9 |
| four_foot    |                -0.7 |                 -1.3 |                  -1.7 |                    -1.3 |                     -1.9 |                      -1.8 |
| eight_foot   |                 2.1 |                  1.4 |                   2   |                    -1   |                     -1.3 |                      -1.2 |
| twelve_foot  |                -7.8 |                  5   |                   0.8 |                    -3.7 |                     -6.4 |                      -1.7 |
| above_tee    |                 4   |                 -3.2 |                   0.5 |                     1.6 |                      4.5 |                       0.5 |
| behind_tee   |                 1.8 |                 -5.4 |                  -1.8 |                     3.6 |                      6   |                       2   |
| wing         |                 0.1 |                  1.2 |                   2.5 |                    -1.4 |                     -1   |                      -1.1 |
| controls_4ft |                -2.5 |                 -1.2 |                  -1.3 |                    -0.9 |                     -1.8 |                      -1.8 |
| guarding     |                 1.3 |                  1.4 |                   0.8 |                     1   |                     -0.9 |                      -2   |
| shot_rock    |                 2.4 |                  6.5 |                  25.1 |                     1.2 |                     -1.7 |                      -9.2 |
| second_shot  |                 4   |                 10   |                  33.5 |                     2.2 |                      3.6 |                       7.3 |
| third_shot   |                 2.8 |                  4.1 |                   9.6 |                     1.2 |                      0.5 |                       0.7 |
| frozen_own   |                -0.3 |                 -0.6 |                   0.2 |                    -1.5 |                      0.5 |                       0.7 |
| frozen_opp   |                 0.5 |                  1.7 |                   1.7 |                    -4.7 |                     -4.7 |                      -7.1 |
| partly_open  |                 0.5 |                  0.4 |                   0.9 |                    -3.7 |                     -2.1 |                      -1.3 |
| behind_cover |                 1.6 |                  1.6 |                   1.2 |                    -4   |                     -3.4 |                      -3.3 |

### Weights, steal (percentage points)

| trait        |   hammer stones 1-5 |   hammer stones 6-10 |   hammer stones 11-15 |   non-hammer stones 1-5 |   non-hammer stones 6-10 |   non-hammer stones 11-15 |
|:-------------|--------------------:|---------------------:|----------------------:|------------------------:|-------------------------:|--------------------------:|
| stone        |                -1   |                  1.4 |                   2   |                     3.9 |                      1.9 |                       0.6 |
| four_foot    |                 1.6 |                  2   |                  -0.5 |                     3.5 |                      4.5 |                       6   |
| eight_foot   |                -1.8 |                 -1   |                  -0.8 |                     0.4 |                      0.7 |                       0.8 |
| twelve_foot  |                 2   |                 -4   |                  -1.3 |                    -0.9 |                      1.7 |                      -0.2 |
| above_tee    |                -2.2 |                 -0.8 |                  -2.3 |                    -1.5 |                     -3.5 |                      -0.2 |
| behind_tee   |                 1.8 |                  2.9 |                   0.2 |                    -2.2 |                     -4   |                      -2.3 |
| wing         |                -0.5 |                  0.7 |                   0.7 |                     1.4 |                      1.4 |                      -0   |
| controls_4ft |                 3.3 |                  3.9 |                   3.7 |                     3.4 |                      4.4 |                       4   |
| guarding     |                -1   |                 -1   |                  -0.4 |                    -0.3 |                      0.6 |                       2.1 |
| shot_rock    |                -3.2 |                 -0.6 |                  -8.3 |                    -1.2 |                      3.9 |                       8.1 |
| second_shot  |                -2.4 |                 -0.8 |                   0.1 |                    -0.2 |                      1.8 |                       6.5 |
| third_shot   |                -2.9 |                 -1.2 |                   1.2 |                    -1.3 |                      0.3 |                       2   |
| frozen_own   |                -1.2 |                 -0.1 |                  -0.2 |                     0.4 |                      0   |                       0.4 |
| frozen_opp   |                -0.3 |                 -1   |                  -2.7 |                     2.2 |                      0.9 |                       0.2 |
| partly_open  |                 0.8 |                  0.3 |                  -1   |                     1.4 |                      0.9 |                       0.9 |
| behind_cover |                -0.3 |                 -0.5 |                  -1.8 |                     1.6 |                      1.7 |                       2.2 |

### Grade card

The most common stone types per stage and team with their grades (hammer points; two-or-more and steal in percentage points; always from the hammer team's side).

| stage        | team       | stone                                                               |     n |   grade_pts |   grade_two |   grade_steal |
|:-------------|:-----------|:--------------------------------------------------------------------|------:|------------:|------------:|--------------:|
| stones 1-5   | hammer     | front+open                                                          | 74678 |        0.29 |       10.43 |         -0.98 |
| stones 1-5   | hammer     | four_foot+above_tee+shot_rock+behind_cover                          | 12944 |        0.35 |       11.95 |         -4.87 |
| stones 1-5   | hammer     | front+guarding+open                                                 |  8286 |        0.35 |       11.72 |         -1.95 |
| stones 1-5   | hammer     | front+controls_4ft+open                                             |  4319 |        0.18 |        7.89 |          2.27 |
| stones 1-5   | hammer     | eight_foot+above_tee+controls_4ft+shot_rock+behind_cover            |  3872 |        0.29 |       10.13 |         -3.23 |
| stones 1-5   | hammer     | four_foot+behind_tee+shot_rock+behind_cover                         |  3409 |        0.24 |        9.74 |         -0.86 |
| stones 1-5   | hammer     | front+controls_4ft+guarding+open                                    |  2972 |        0.23 |        9.18 |          1.31 |
| stones 1-5   | hammer     | four_foot+above_tee+shot_rock+partly_open                           |  2823 |        0.32 |       10.88 |         -3.77 |
| stones 1-5   | hammer     | twelve_foot+above_tee+wing+shot_rock+open                           |  2502 |        0.28 |        9.11 |         -4.85 |
| stones 1-5   | hammer     | four_foot+above_tee+shot_rock+open                                  |  2329 |        0.3  |       10.39 |         -4.56 |
| stones 1-5   | hammer     | twelve_foot+above_tee+wing+second_shot+open                         |  2144 |        0.34 |       10.79 |         -4.11 |
| stones 1-5   | hammer     | eight_foot+above_tee+wing+shot_rock+open                            |  2136 |        0.37 |       11.21 |         -6.68 |
| stones 1-5   | hammer     | open                                                                |  2041 |        0.29 |       10.43 |         -0.98 |
| stones 1-5   | hammer     | twelve_foot+behind_tee+wing+shot_rock+open                          |  1846 |        0.17 |        6.9  |         -0.84 |
| stones 1-5   | hammer     | eight_foot+above_tee+controls_4ft+guarding+second_shot+behind_cover |  1802 |        0.41 |       13.1  |         -3.46 |
| stones 1-5   | non-hammer | front+controls_4ft+guarding+open                                    | 64328 |        0.03 |        2.78 |          6.97 |
| stones 1-5   | non-hammer | front+controls_4ft+open                                             | 47778 |        0    |        1.74 |          7.28 |
| stones 1-5   | non-hammer | four_foot+above_tee+shot_rock+open                                  | 23494 |       -0.09 |       -0.54 |          4.25 |
| stones 1-5   | non-hammer | four_foot+above_tee+shot_rock+behind_cover                          | 17457 |       -0.22 |       -4.55 |          5.88 |
| stones 1-5   | non-hammer | eight_foot+above_tee+controls_4ft+shot_rock+open                    |  8576 |       -0.07 |       -0.1  |          4.11 |
| stones 1-5   | non-hammer | four_foot+behind_tee+shot_rock+open                                 |  8405 |       -0.02 |        1.45 |          3.55 |
| stones 1-5   | non-hammer | front+open                                                          |  7490 |        0.08 |        2.63 |          3.9  |
| stones 1-5   | non-hammer | four_foot+above_tee+shot_rock+partly_open                           |  5900 |       -0.2  |       -4.21 |          5.62 |
| stones 1-5   | non-hammer | front+controls_4ft+guarding+behind_cover                            |  5864 |       -0.1  |       -1.23 |          8.59 |
| stones 1-5   | non-hammer | four_foot+behind_tee+shot_rock+behind_cover                         |  5712 |       -0.14 |       -2.56 |          5.17 |
| stones 1-5   | non-hammer | twelve_foot+above_tee+controls_4ft+shot_rock+open                   |  4910 |       -0.03 |        0.87 |          3.67 |
| stones 1-5   | non-hammer | eight_foot+above_tee+controls_4ft+shot_rock+behind_cover            |  4509 |       -0.2  |       -4.11 |          5.73 |
| stones 1-5   | non-hammer | eight_foot+above_tee+controls_4ft+guarding+second_shot+open         |  3880 |       -0.01 |        1.95 |          4.79 |
| stones 1-5   | non-hammer | front+controls_4ft+guarding+partly_open                             |  3481 |       -0.08 |       -0.89 |          8.33 |
| stones 1-5   | non-hammer | twelve_foot+above_tee+controls_4ft+guarding+second_shot+open        |  3218 |        0.03 |        2.93 |          4.35 |
| stones 6-10  | hammer     | front+open                                                          | 85272 |        0.1  |        4.65 |          1.41 |
| stones 6-10  | hammer     | front+guarding+open                                                 | 29849 |        0.16 |        6.05 |          0.45 |
| stones 6-10  | hammer     | front+controls_4ft+guarding+open                                    | 17469 |        0.07 |        4.85 |          4.31 |
| stones 6-10  | hammer     | front+controls_4ft+open                                             | 12023 |        0.01 |        3.44 |          5.27 |
| stones 6-10  | hammer     | four_foot+above_tee+shot_rock+behind_cover                          | 11898 |        0.42 |       14.76 |         -3.47 |
| stones 6-10  | hammer     | open                                                                |  9874 |        0.1  |        4.65 |          1.41 |
| stones 6-10  | hammer     | four_foot+above_tee+shot_rock+open                                  |  4863 |        0.35 |       13.17 |         -2.97 |
| stones 6-10  | hammer     | four_foot+behind_tee+shot_rock+behind_cover                         |  4479 |        0.31 |       12.57 |          0.28 |
| stones 6-10  | hammer     | twelve_foot+above_tee+wing+second_shot+open                         |  4203 |        0.49 |       17.73 |         -3.61 |
| stones 6-10  | hammer     | front+behind_cover                                                  |  4095 |        0.17 |        6.24 |          0.9  |
| stones 6-10  | hammer     | eight_foot+above_tee+wing+shot_rock+open                            |  4062 |        0.42 |       15.65 |         -4.33 |
| stones 6-10  | hammer     | twelve_foot+behind_tee+wing+second_shot+open                        |  3695 |        0.38 |       15.54 |          0.14 |
| stones 6-10  | hammer     | four_foot+above_tee+guarding+shot_rock+behind_cover                 |  3636 |        0.48 |       16.16 |         -4.44 |
| stones 6-10  | hammer     | eight_foot+above_tee+wing+second_shot+open                          |  3572 |        0.56 |       19.17 |         -4.56 |
| stones 6-10  | hammer     | four_foot+above_tee+shot_rock+partly_open                           |  3543 |        0.37 |       13.54 |         -2.66 |
| stones 6-10  | non-hammer | front+controls_4ft+guarding+open                                    | 59138 |       -0.06 |        0.39 |          6.95 |
| stones 6-10  | non-hammer | front+open                                                          | 27086 |        0.08 |        3.09 |          1.92 |
| stones 6-10  | non-hammer | front+controls_4ft+open                                             | 26421 |       -0.02 |        1.24 |          6.32 |
| stones 6-10  | non-hammer | four_foot+above_tee+shot_rock+behind_cover                          | 17317 |       -0.36 |       -7.11 |         10.93 |
| stones 6-10  | non-hammer | four_foot+above_tee+shot_rock+open                                  | 12116 |       -0.25 |       -3.7  |          9.2  |
| stones 6-10  | non-hammer | open                                                                | 10457 |        0.08 |        3.09 |          1.92 |
| stones 6-10  | non-hammer | four_foot+behind_tee+shot_rock+behind_cover                         |  8125 |       -0.3  |       -5.63 |         10.5  |
| stones 6-10  | non-hammer | four_foot+behind_tee+shot_rock+open                                 |  7444 |       -0.19 |       -2.22 |          8.77 |
| stones 6-10  | non-hammer | front+guarding+open                                                 |  6980 |        0.04 |        2.24 |          2.56 |
| stones 6-10  | non-hammer | four_foot+above_tee+shot_rock+partly_open                           |  6713 |       -0.31 |       -5.77 |         10.12 |
| stones 6-10  | non-hammer | front+controls_4ft+guarding+behind_cover                            |  5319 |       -0.17 |       -3.03 |          8.68 |
| stones 6-10  | non-hammer | eight_foot+above_tee+controls_4ft+shot_rock+open                    |  4589 |       -0.22 |       -3.69 |          9.11 |
| stones 6-10  | non-hammer | twelve_foot+above_tee+wing+second_shot+open                         |  4528 |        0.09 |        3.78 |          3.21 |
| stones 6-10  | non-hammer | twelve_foot+above_tee+wing+third_shot+open                          |  3964 |        0    |        0.64 |          1.76 |
| stones 6-10  | non-hammer | front+controls_4ft+guarding+partly_open                             |  3895 |       -0.12 |       -1.69 |          7.87 |
| stones 11-15 | hammer     | front+open                                                          | 78500 |        0.01 |        1.21 |          1.97 |
| stones 11-15 | hammer     | front+guarding+open                                                 | 39662 |        0.04 |        2.01 |          1.56 |
| stones 11-15 | hammer     | front+controls_4ft+guarding+open                                    | 22197 |       -0.06 |        0.73 |          5.31 |
| stones 11-15 | hammer     | open                                                                | 18099 |        0.01 |        1.21 |          1.97 |
| stones 11-15 | hammer     | front+controls_4ft+open                                             | 10677 |       -0.09 |       -0.07 |          5.72 |
| stones 11-15 | hammer     | four_foot+above_tee+shot_rock+behind_cover                          |  7699 |        0.93 |       29.07 |        -12.97 |
| stones 11-15 | hammer     | twelve_foot+behind_tee+wing+open                                    |  7258 |        0.07 |        2.79 |          1.5  |
| stones 11-15 | hammer     | four_foot+above_tee+shot_rock+open                                  |  5076 |        0.85 |       27.91 |        -11.21 |
| stones 11-15 | hammer     | twelve_foot+above_tee+wing+open                                     |  4863 |        0.16 |        5.03 |         -0.91 |
| stones 11-15 | hammer     | front+behind_cover                                                  |  4510 |        0.08 |        2.36 |          0.21 |
| stones 11-15 | hammer     | four_foot+above_tee+guarding+shot_rock+behind_cover                 |  4378 |        0.96 |       29.87 |        -13.38 |
| stones 11-15 | hammer     | four_foot+behind_tee+shot_rock+behind_cover                         |  4265 |        0.84 |       26.82 |        -10.56 |
| stones 11-15 | hammer     | twelve_foot+behind_tee+wing+second_shot+open                        |  4067 |        0.87 |       36.28 |          1.61 |
| stones 11-15 | hammer     | four_foot+behind_tee+shot_rock+open                                 |  4002 |        0.76 |       25.67 |         -8.8  |
| stones 11-15 | hammer     | eight_foot+above_tee+wing+shot_rock+open                            |  3968 |        0.84 |       32.11 |        -10.03 |
| stones 11-15 | non-hammer | front+controls_4ft+guarding+open                                    | 54490 |       -0.14 |       -1.89 |          6.7  |
| stones 11-15 | non-hammer | front+open                                                          | 36552 |        0.06 |        1.93 |          0.62 |
| stones 11-15 | non-hammer | front+controls_4ft+open                                             | 20665 |       -0.04 |        0.13 |          4.58 |
| stones 11-15 | non-hammer | open                                                                | 19861 |        0.06 |        1.93 |          0.62 |
| stones 11-15 | non-hammer | front+guarding+open                                                 | 14764 |       -0.04 |       -0.09 |          2.75 |
| stones 11-15 | non-hammer | four_foot+above_tee+shot_rock+behind_cover                          | 12088 |       -0.63 |      -14.82 |         17.31 |
| stones 11-15 | non-hammer | four_foot+above_tee+shot_rock+open                                  | 10208 |       -0.5  |      -11.55 |         15.06 |
| stones 11-15 | non-hammer | twelve_foot+behind_tee+wing+open                                    |  9368 |        0.09 |        1.06 |         -1.96 |
| stones 11-15 | non-hammer | twelve_foot+above_tee+wing+open                                     |  8218 |       -0.01 |       -0.43 |          0.18 |
| stones 11-15 | non-hammer | four_foot+behind_tee+shot_rock+open                                 |  7769 |       -0.41 |      -10.06 |         12.92 |
| stones 11-15 | non-hammer | four_foot+behind_tee+shot_rock+behind_cover                         |  7476 |       -0.54 |      -13.33 |         15.17 |
| stones 11-15 | non-hammer | twelve_foot+above_tee+wing+third_shot+open                          |  5488 |       -0.02 |        0.26 |          2.2  |
| stones 11-15 | non-hammer | twelve_foot+behind_tee+wing+third_shot+open                         |  5373 |        0.07 |        1.75 |          0.06 |
| stones 11-15 | non-hammer | twelve_foot+above_tee+wing+second_shot+open                         |  5176 |        0.2  |        6.82 |          6.72 |
| stones 11-15 | non-hammer | front+controls_4ft+guarding+behind_cover                            |  5077 |       -0.27 |       -5.16 |          8.95 |
