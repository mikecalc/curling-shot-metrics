# World Women's Curling Championship (WWCC2022_ResultsBook)

Prince George, BC, Canada, 2022; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Women

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| SUI    |      14 | 14-0     |               68.1 |
| SWE    |      14 | 9-5      |               53.1 |
| KOR    |      12 | 8-4      |               51.3 |
| CAN    |      14 | 10-4     |               47   |
| USA    |      12 | 7-5      |               37.2 |
| JPN    |      10 | 5-5      |               36.4 |
| DEN    |      12 | 6-6      |               30.9 |
| NOR    |      11 | 4-7      |               27   |
| GER    |      11 | 4-7      |               25   |
| ITA    |      11 | 3-8      |                8.8 |
| TUR    |      11 | 1-10     |                7.6 |
| CZE    |      12 | 2-10     |                1   |
| SCO    |       2 | 0-2      |              -20.5 |

### Build or address

How each team played the stones, in rock potential (descriptive, not a ranking): `build` is how much a stone added to the team's own potential and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' potential together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| SCO    |      127 |   0.025 |    -0.031 |          0.803 |                2.949 |                   3.57  |
| GER    |      809 |   0.011 |    -0.017 |          0.749 |                2.608 |                   2.637 |
| KOR    |      912 |   0.008 |    -0.003 |          0.731 |                2.258 |                   2.855 |
| USA    |      885 |   0.004 |    -0.019 |          0.721 |                2.323 |                   3.114 |
| JPN    |      715 |   0.003 |    -0.01  |          0.737 |                2.952 |                   2.536 |
| NOR    |      807 |   0.002 |     0.001 |          0.737 |                2.559 |                   2.403 |
| DEN    |      889 |   0.002 |     0.008 |          0.704 |                2.761 |                   2.458 |
| SWE    |     1046 |  -0.003 |     0.006 |          0.709 |                2.218 |                   2.428 |
| ITA    |      785 |  -0.004 |    -0.001 |          0.717 |                2.58  |                   2.336 |
| TUR    |      779 |  -0.004 |    -0.001 |          0.734 |                2.944 |                   2.335 |
| CZE    |      857 |  -0.005 |     0.003 |          0.718 |                2.488 |                   2.31  |
| CAN    |      990 |  -0.008 |     0.007 |          0.702 |                2.719 |                   2.771 |
| SUI    |      960 |  -0.01  |     0.022 |          0.682 |                2.638 |                   2.551 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| PAETZ A       | SUI    |     238 |      14 |         0.685 |      0.285 |     -0.264 |          28 |           11 |   -5.601 |  0.112 |             44 |              17 |      1.252 |      -0.959 |  0.002 |  89.301 |
| EINARSON K    | CAN    |     247 |      14 |         0.636 |      0.298 |     -0.354 |          26 |           22 |   -7.049 |  0.06  |             37 |              31 |      1.317 |      -1.378 |  0.006 |  80.466 |
| HASSELBORG A  | SWE    |     264 |      14 |         0.633 |      0.259 |     -0.215 |          27 |           12 |   -4.358 |  0.085 |             28 |              18 |      1.139 |      -0.847 |  0.006 |  82.414 |
| KIM E         | KOR    |     231 |      12 |         0.602 |      0.252 |     -0.274 |          20 |           17 |   -6.594 |  0.042 |             39 |              23 |      1.274 |      -1.789 |  0.005 |  77.851 |
| CHRISTENSEN C | USA    |     224 |      12 |         0.571 |      0.26  |     -0.271 |          22 |           19 |   -5.568 |  0.033 |             39 |              24 |      0.957 |      -1.476 | -0.001 |  79.709 |
| JENTSCH D     | GER    |     205 |      11 |         0.556 |      0.28  |     -0.294 |          20 |           18 |   -5.059 |  0.025 |             24 |              28 |      0.743 |      -0.825 |  0.031 |  76.478 |
| YILDIZ D      | TUR    |     198 |      11 |         0.53  |      0.292 |     -0.381 |          16 |           24 |   -8.973 | -0.024 |             22 |              29 |      0.956 |      -0.797 | -0.011 |  68.846 |
| SKASLIEN K    | NOR    |     204 |      11 |         0.525 |      0.3   |     -0.331 |          17 |           22 |   -8.419 |  0     |             22 |              29 |      0.941 |      -0.852 | -0.002 |  75.373 |
| DUPONT M      | DEN    |     217 |      12 |         0.521 |      0.315 |     -0.305 |          21 |           21 |   -7.04  |  0.018 |             30 |              29 |      1.675 |      -1.031 | -0.003 |  73.585 |
| KITAZAWA I    | JPN    |     180 |      10 |         0.517 |      0.277 |     -0.323 |          14 |           22 |   -7.812 | -0.013 |             26 |              23 |      0.692 |      -1.367 |  0.022 |  75.424 |
| CONSTANTINI S | ITA    |     202 |      11 |         0.485 |      0.226 |     -0.305 |           9 |           24 |   -7.306 | -0.047 |             19 |              31 |      0.725 |      -1.342 |  0.007 |  72.125 |
| BAUDYSOVA A   | CZE    |     217 |      12 |         0.479 |      0.295 |     -0.33  |          18 |           26 |   -7.253 | -0.031 |             23 |              35 |      0.855 |      -1.153 |  0.017 |  72.079 |
| AITKEN G      | SCO    |      32 |       2 |         0.406 |      0.314 |     -0.641 |           3 |            7 |   -8.76  | -0.253 |              2 |               5 |      0.212 |      -0.773 |  0.052 |  56.25  |

### Thirds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| NAKAJIMA S   | JPN    |     110 |       6 |         0.618 |      0.128 |     -0.156 |           0 |            2 |   -2.152 |  0.02  |              2 |               4 |      0.246 |      -0.3   |  0.014 |  82.045 |
| ROERVIK M    | NOR    |     204 |      11 |         0.564 |      0.122 |     -0.14  |           2 |            2 |   -2.671 |  0.008 |              4 |               4 |      0.33  |      -0.349 |  0.004 |  81.373 |
| KIM K        | KOR    |     232 |      12 |         0.547 |      0.142 |     -0.139 |           2 |            5 |   -3.078 |  0.015 |             13 |              14 |      0.539 |      -0.569 |  0.008 |  85.129 |
| MCMANUS S    | SWE    |     266 |      14 |         0.545 |      0.125 |     -0.112 |           1 |            2 |   -2.613 |  0.017 |             11 |               8 |      0.403 |      -0.541 | -0.01  |  86.842 |
| SWEETING V   | CAN    |     248 |      14 |         0.54  |      0.147 |     -0.139 |           7 |            4 |   -2.52  |  0.016 |             10 |              10 |      0.609 |      -0.406 | -0.017 |  84.173 |
| TIRINZONI S  | SUI    |     228 |      14 |         0.504 |      0.121 |     -0.13  |           0 |            3 |   -2.717 | -0.004 |              5 |              10 |      0.293 |      -0.438 | -0.006 |  87.061 |
| ANDERSON S   | USA    |     224 |      12 |         0.451 |      0.107 |     -0.114 |           1 |            1 |   -2.174 | -0.014 |              3 |               7 |      0.344 |      -0.425 | -0.008 |  78.46  |
| HALSE M      | DEN    |     224 |      12 |         0.442 |      0.12  |     -0.138 |           1 |            4 |   -3.444 | -0.024 |              7 |              12 |      0.338 |      -0.513 |  0     |  76.562 |
| POLAT O      | TUR    |     198 |      11 |         0.439 |      0.118 |     -0.145 |           1 |            2 |   -2.573 | -0.029 |              9 |               6 |      0.342 |      -0.387 |  0.003 |  77.904 |
| SINCLAIR S   | SCO    |      48 |       2 |         0.438 |      0.095 |     -0.121 |           0 |            1 |   -1.735 | -0.026 |              1 |               1 |      0.166 |      -0.152 |  0.015 |  80.729 |
| ABBES E      | GER    |     206 |      11 |         0.427 |      0.116 |     -0.154 |           0 |            4 |   -2.925 | -0.039 |              3 |              12 |      0.354 |      -0.358 |  0.018 |  74.515 |
| MATSUMURA C  | JPN    |     112 |       6 |         0.402 |      0.109 |     -0.093 |           3 |            0 |   -1.701 | -0.012 |              3 |               2 |      0.362 |      -0.249 |  0.008 |  84.152 |
| LO DESERTO M | ITA    |     202 |      11 |         0.391 |      0.117 |     -0.136 |           2 |            4 |   -2.902 | -0.037 |              6 |               9 |      0.371 |      -0.405 |  0.014 |  78.094 |
| VINSOVA P    | CZE    |     218 |      12 |         0.358 |      0.111 |     -0.159 |           1 |            7 |   -3.234 | -0.062 |              8 |              16 |      0.382 |      -0.483 | -0.002 |  75.229 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HOWALD C         | SUI    |      60 |       7 |         0.55  |      0.061 |     -0.062 |           0 |            0 |   -0.57  |  0.005 |              1 |               0 |      0.131 |      -0.09  | -0.013 |  86.667 |
| PERSINGER V      | USA    |     218 |      12 |         0.541 |      0.086 |     -0.087 |           0 |            1 |   -1.782 |  0.007 |              5 |               2 |      0.277 |      -0.285 |  0.003 |  85.55  |
| KIM C            | KOR    |     232 |      12 |         0.491 |      0.069 |     -0.076 |           0 |            0 |   -1.223 | -0.005 |              1 |               1 |      0.213 |      -0.257 | -0.008 |  82.684 |
| SUZUKI M         | JPN    |     166 |       9 |         0.482 |      0.067 |     -0.098 |           0 |            3 |   -2.552 | -0.018 |              1 |               1 |      0.213 |      -0.215 |  0.004 |  80.723 |
| DUPONT D         | DEN    |     224 |      12 |         0.478 |      0.075 |     -0.086 |           0 |            1 |   -1.876 | -0.009 |              2 |               2 |      0.232 |      -0.269 |  0.007 |  83.482 |
| BIRCHARD S       | CAN    |     248 |      14 |         0.464 |      0.078 |     -0.075 |           0 |            1 |   -1.808 | -0.004 |              0 |               2 |      0.173 |      -0.251 | -0.008 |  84.173 |
| HOEHNE M         | GER    |     206 |      11 |         0.461 |      0.075 |     -0.096 |           0 |            3 |   -2.487 | -0.017 |              0 |               4 |      0.175 |      -0.415 |  0.004 |  74.272 |
| ROMEI A          | ITA    |     202 |      11 |         0.46  |      0.067 |     -0.09  |           0 |            1 |   -2.435 | -0.018 |              1 |               2 |      0.222 |      -0.301 |  0.01  |  81.592 |
| HASLEV NORDBYE M | NOR    |     196 |      11 |         0.459 |      0.065 |     -0.08  |           0 |            1 |   -1.68  | -0.013 |              1 |               1 |      0.167 |      -0.22  |  0.009 |  85.842 |
| NEUENSCHWANDER E | SUI    |     214 |      13 |         0.439 |      0.088 |     -0.074 |           0 |            0 |   -1.452 | -0.003 |              3 |               0 |      0.321 |      -0.198 | -0.001 |  91.197 |
| KNOCHENHAUER A   | SWE    |     246 |      13 |         0.439 |      0.069 |     -0.073 |           1 |            0 |   -1.155 | -0.01  |              1 |               1 |      0.261 |      -0.185 | -0.001 |  83.709 |
| SENGUL B         | TUR    |     142 |       8 |         0.401 |      0.081 |     -0.1   |           0 |            0 |   -1.774 | -0.027 |              3 |               2 |      0.265 |      -0.241 | -0     |  68.662 |
| POLAT M          | TUR    |      90 |       6 |         0.378 |      0.051 |     -0.072 |           0 |            1 |   -1.295 | -0.025 |              0 |               0 |      0.092 |      -0.149 |  0.006 |  78.889 |
| BAUDYSOVA M      | CZE    |     218 |      12 |         0.362 |      0.048 |     -0.083 |           0 |            0 |   -1.477 | -0.036 |              0 |               0 |      0.119 |      -0.22  |  0.001 |  77.179 |

### Leads

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KIM S       | KOR    |     226 |      12 |         0.602 |      0.038 |     -0.039 |           0 |            0 |   -0.659 |  0.008 |              0 |               0 |      0.094 |      -0.09  | -0.003 |  86.947 |
| MEILLEUR B  | CAN    |     248 |      14 |         0.593 |      0.042 |     -0.036 |           0 |            0 |   -0.834 |  0.01  |              0 |               0 |      0.118 |      -0.099 |  0.001 |  88.71  |
| BARBEZAT M  | SUI    |     228 |      14 |         0.57  |      0.042 |     -0.035 |           0 |            0 |   -0.657 |  0.009 |              0 |               0 |      0.087 |      -0.099 |  0.002 |  87.004 |
| ROENNING M  | NOR    |     204 |      11 |         0.559 |      0.032 |     -0.029 |           0 |            0 |   -0.541 |  0.005 |              0 |               0 |      0.115 |      -0.073 |  0.002 |  88.235 |
| JENTSCH A   | GER    |     206 |      11 |         0.558 |      0.034 |     -0.043 |           0 |            0 |   -0.879 | -0     |              0 |               0 |      0.105 |      -0.123 | -0.002 |  81.22  |
| GOZUTOK A   | TUR    |     164 |       9 |         0.555 |      0.025 |     -0.046 |           0 |            0 |   -1.025 | -0.007 |              0 |               0 |      0.072 |      -0.141 | -0.002 |  80.64  |
| MABERGS S   | SWE    |     262 |      14 |         0.534 |      0.036 |     -0.037 |           0 |            0 |   -0.811 |  0.002 |              0 |               0 |      0.106 |      -0.11  |  0.001 |  89.559 |
| ZAPPONE V   | ITA    |     178 |      10 |         0.522 |      0.037 |     -0.042 |           0 |            0 |   -0.794 | -0     |              0 |               0 |      0.104 |      -0.13  |  0.007 |  83.708 |
| ANDERSON T  | USA    |     224 |      12 |         0.522 |      0.039 |     -0.032 |           0 |            0 |   -0.574 |  0.005 |              0 |               0 |      0.127 |      -0.089 |  0.003 |  89.062 |
| LARSEN M    | DEN    |     224 |      12 |         0.522 |      0.036 |     -0.035 |           0 |            0 |   -0.596 |  0.002 |              0 |               0 |      0.107 |      -0.093 |  0.003 |  87.5   |
| ISHIGOOKA H | JPN    |     152 |       8 |         0.5   |      0.034 |     -0.045 |           0 |            0 |   -0.844 | -0.005 |              0 |               0 |      0.101 |      -0.094 |  0.001 |  81.126 |
| JACKSON S   | SCO    |      48 |       2 |         0.479 |      0.03  |     -0.054 |           0 |            0 |   -0.725 | -0.014 |              0 |               0 |      0.061 |      -0.097 |  0.011 |  79.688 |
| SVATONOVA K | CZE    |     218 |      12 |         0.454 |      0.042 |     -0.044 |           0 |            0 |   -0.74  | -0.005 |              0 |               0 |      0.098 |      -0.119 |  0.003 |  83.486 |

