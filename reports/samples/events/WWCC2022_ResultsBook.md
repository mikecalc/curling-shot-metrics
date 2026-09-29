# World Women's Curling Championship (WWCC2022_ResultsBook)

Prince George, BC, Canada, 2022; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Women

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| SUI    |      14 | 14-0     |               68.2 |
| SWE    |      14 | 9-5      |               50   |
| KOR    |      12 | 8-4      |               48.6 |
| CAN    |      14 | 10-4     |               44.5 |
| USA    |      12 | 7-5      |               28.3 |
| DEN    |      12 | 6-6      |               28.3 |
| JPN    |      10 | 5-5      |               19.1 |
| NOR    |      11 | 4-7      |               15.7 |
| GER    |      11 | 4-7      |               13.1 |
| CZE    |      12 | 2-10     |                3.8 |
| TUR    |      11 | 1-10     |                3.2 |
| ITA    |      11 | 3-8      |               -2.7 |
| SCO    |       2 | 0-2      |              -22.8 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| SCO    |      127 |   0.026 |    -0.082 |          0.74  |                2.244 |                   2.807 |
| KOR    |      912 |   0.022 |     0.005 |          0.616 |                2.037 |                   2.293 |
| DEN    |      889 |   0.013 |    -0.004 |          0.616 |                2.267 |                   2.145 |
| GER    |      809 |   0.01  |    -0.01  |          0.618 |                1.995 |                   2.144 |
| NOR    |      807 |   0.007 |    -0.014 |          0.641 |                2.167 |                   2.061 |
| USA    |      885 |   0.003 |    -0.011 |          0.609 |                1.96  |                   2.35  |
| CZE    |      857 |   0.002 |    -0.012 |          0.608 |                2.024 |                   2.023 |
| SWE    |     1046 |  -0.002 |     0.014 |          0.595 |                1.92  |                   1.966 |
| JPN    |      715 |  -0.003 |     0.006 |          0.606 |                2.174 |                   2.05  |
| TUR    |      779 |  -0.003 |    -0.012 |          0.62  |                2.17  |                   2.035 |
| ITA    |      785 |  -0.012 |    -0.008 |          0.587 |                1.944 |                   1.889 |
| CAN    |      990 |  -0.017 |     0.017 |          0.576 |                2.329 |                   2.186 |
| SUI    |      960 |  -0.021 |     0.03  |          0.544 |                2.198 |                   1.994 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| PAETZ A       | SUI    |     238 |      14 |         0.693 |      0.273 |     -0.271 |          22 |           12 |   -5.455 |  0.106 |             43 |              17 |      1.3   |      -1.001 |  0.008 |  89.301 |
| KIM E         | KOR    |     231 |      12 |         0.623 |      0.247 |     -0.284 |          21 |           16 |   -7.318 |  0.047 |             36 |              23 |      1.336 |      -1.888 | -0.004 |  77.851 |
| HASSELBORG A  | SWE    |     264 |      14 |         0.614 |      0.25  |     -0.218 |          18 |           14 |   -4.886 |  0.069 |             26 |              21 |      1.16  |      -0.914 |  0.007 |  82.414 |
| EINARSON K    | CAN    |     247 |      14 |         0.611 |      0.293 |     -0.356 |          25 |           27 |   -6.8   |  0.041 |             32 |              31 |      1.317 |      -1.291 |  0.013 |  80.466 |
| CHRISTENSEN C | USA    |     224 |      12 |         0.585 |      0.245 |     -0.275 |          18 |           19 |   -5.616 |  0.029 |             28 |              25 |      1.014 |      -1.55  | -0.003 |  79.709 |
| JENTSCH D     | GER    |     205 |      11 |         0.532 |      0.279 |     -0.275 |          20 |           19 |   -5.562 |  0.02  |             22 |              26 |      0.705 |      -0.952 |  0.028 |  76.478 |
| YILDIZ D      | TUR    |     198 |      11 |         0.53  |      0.277 |     -0.4   |          19 |           20 |   -9.288 | -0.041 |             18 |              28 |      0.838 |      -0.821 |  0.001 |  68.846 |
| DUPONT M      | DEN    |     217 |      12 |         0.525 |      0.33  |     -0.32  |          25 |           24 |   -6.898 |  0.021 |             36 |              34 |      1.632 |      -1.018 | -0.004 |  73.585 |
| SKASLIEN K    | NOR    |     204 |      11 |         0.51  |      0.285 |     -0.335 |          17 |           22 |   -8.695 | -0.019 |             18 |              32 |      0.887 |      -0.941 | -0.014 |  75.373 |
| KITAZAWA I    | JPN    |     180 |      10 |         0.5   |      0.245 |     -0.304 |          12 |           18 |   -7.39  | -0.03  |             22 |              22 |      0.744 |      -1.334 |  0.011 |  75.424 |
| BAUDYSOVA A   | CZE    |     217 |      12 |         0.484 |      0.301 |     -0.337 |          20 |           26 |   -7.673 | -0.028 |             23 |              30 |      0.974 |      -1.271 |  0.011 |  72.079 |
| CONSTANTINI S | ITA    |     202 |      11 |         0.446 |      0.224 |     -0.286 |          11 |           21 |   -6.929 | -0.059 |             15 |              34 |      0.76  |      -1.3   |  0.004 |  72.125 |
| AITKEN G      | SCO    |      32 |       2 |         0.438 |      0.272 |     -0.655 |           4 |            7 |   -8.46  | -0.249 |              2 |               5 |      0.227 |      -0.8   |  0.039 |  56.25  |

### Thirds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| TIRINZONI S  | SUI    |     228 |      14 |         0.579 |      0.131 |     -0.14  |           1 |            2 |   -2.821 |  0.017 |              7 |              12 |      0.358 |      -0.467 | -0.005 |  87.061 |
| KIM K        | KOR    |     232 |      12 |         0.578 |      0.156 |     -0.158 |           1 |            7 |   -3.861 |  0.023 |             14 |              11 |      0.738 |      -0.739 |  0.01  |  85.129 |
| SWEETING V   | CAN    |     248 |      14 |         0.565 |      0.154 |     -0.149 |           5 |            2 |   -2.632 |  0.022 |             13 |              12 |      0.56  |      -0.383 | -0.015 |  84.173 |
| ROERVIK M    | NOR    |     204 |      11 |         0.564 |      0.148 |     -0.137 |           5 |            1 |   -2.617 |  0.024 |              7 |               3 |      0.404 |      -0.266 | -0.007 |  81.373 |
| MCMANUS S    | SWE    |     266 |      14 |         0.56  |      0.128 |     -0.12  |           3 |            3 |   -2.512 |  0.019 |             11 |               9 |      0.443 |      -0.495 | -0.005 |  86.842 |
| NAKAJIMA S   | JPN    |     110 |       6 |         0.536 |      0.162 |     -0.138 |           0 |            1 |   -2.214 |  0.023 |              6 |               4 |      0.369 |      -0.339 |  0.015 |  82.045 |
| ANDERSON S   | USA    |     224 |      12 |         0.509 |      0.095 |     -0.129 |           2 |            2 |   -2.652 | -0.015 |              3 |              10 |      0.316 |      -0.514 | -0.01  |  78.46  |
| POLAT O      | TUR    |     198 |      11 |         0.485 |      0.156 |     -0.151 |           3 |            4 |   -3.028 | -0.002 |             10 |              10 |      0.478 |      -0.467 |  0.004 |  77.904 |
| MATSUMURA C  | JPN    |     112 |       6 |         0.446 |      0.105 |     -0.087 |           2 |            0 |   -1.2   | -0.001 |              4 |               0 |      0.331 |      -0.189 |  0.012 |  84.152 |
| ABBES E      | GER    |     206 |      11 |         0.442 |      0.111 |     -0.166 |           2 |            5 |   -3.13  | -0.044 |              4 |              16 |      0.374 |      -0.569 |  0.017 |  74.515 |
| SINCLAIR S   | SCO    |      48 |       2 |         0.438 |      0.13  |     -0.135 |           0 |            1 |   -1.809 | -0.019 |              1 |               0 |      0.203 |      -0.148 |  0.031 |  80.729 |
| HALSE M      | DEN    |     224 |      12 |         0.406 |      0.139 |     -0.132 |           3 |            4 |   -3.177 | -0.022 |              5 |              10 |      0.393 |      -0.528 |  0.001 |  76.562 |
| VINSOVA P    | CZE    |     218 |      12 |         0.404 |      0.132 |     -0.163 |           2 |            7 |   -3.851 | -0.044 |              9 |               9 |      0.457 |      -0.551 | -0     |  75.229 |
| LO DESERTO M | ITA    |     202 |      11 |         0.391 |      0.124 |     -0.119 |           3 |            2 |   -2.535 | -0.024 |              6 |              11 |      0.376 |      -0.44  |  0.009 |  78.094 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| NEUENSCHWANDER E | SUI    |     214 |      13 |         0.523 |      0.093 |     -0.075 |           1 |            0 |   -1.309 |  0.013 |              3 |               0 |      0.372 |      -0.183 |  0.001 |  91.197 |
| PERSINGER V      | USA    |     218 |      12 |         0.523 |      0.096 |     -0.073 |           0 |            1 |   -1.938 |  0.015 |              7 |               2 |      0.351 |      -0.294 |  0.003 |  85.55  |
| HOWALD C         | SUI    |      60 |       7 |         0.517 |      0.056 |     -0.055 |           0 |            0 |   -0.689 |  0.002 |              1 |               0 |      0.128 |      -0.066 | -0.009 |  86.667 |
| BIRCHARD S       | CAN    |     248 |      14 |         0.512 |      0.078 |     -0.088 |           0 |            0 |   -1.883 | -0.003 |              2 |               3 |      0.219 |      -0.289 | -0.01  |  84.173 |
| KNOCHENHAUER A   | SWE    |     246 |      13 |         0.504 |      0.073 |     -0.079 |           1 |            0 |   -1.442 | -0.002 |              4 |               1 |      0.314 |      -0.196 | -0.003 |  83.709 |
| KIM C            | KOR    |     232 |      12 |         0.496 |      0.072 |     -0.075 |           0 |            0 |   -1.436 | -0.002 |              3 |               2 |      0.283 |      -0.234 | -0.007 |  82.684 |
| HASLEV NORDBYE M | NOR    |     196 |      11 |         0.464 |      0.079 |     -0.084 |           0 |            0 |   -1.562 | -0.008 |              0 |               1 |      0.138 |      -0.196 |  0.005 |  85.842 |
| DUPONT D         | DEN    |     224 |      12 |         0.451 |      0.099 |     -0.083 |           0 |            1 |   -1.91  | -0.001 |              3 |               4 |      0.282 |      -0.272 |  0.008 |  83.482 |
| ROMEI A          | ITA    |     202 |      11 |         0.436 |      0.068 |     -0.078 |           0 |            0 |   -1.76  | -0.014 |              3 |               2 |      0.259 |      -0.26  |  0.011 |  81.592 |
| HOEHNE M         | GER    |     206 |      11 |         0.432 |      0.077 |     -0.093 |           0 |            1 |   -2.23  | -0.02  |              2 |               3 |      0.223 |      -0.313 |  0.006 |  74.272 |
| SUZUKI M         | JPN    |     166 |       9 |         0.416 |      0.063 |     -0.093 |           0 |            5 |   -2.815 | -0.028 |              1 |               4 |      0.198 |      -0.317 |  0.01  |  80.723 |
| BAUDYSOVA M      | CZE    |     218 |      12 |         0.385 |      0.058 |     -0.09  |           0 |            0 |   -1.845 | -0.033 |              0 |               2 |      0.162 |      -0.246 |  0.004 |  77.179 |
| SENGUL B         | TUR    |     142 |       8 |         0.373 |      0.09  |     -0.122 |           0 |            1 |   -2.47  | -0.043 |              3 |               3 |      0.3   |      -0.311 |  0.002 |  68.662 |
| POLAT M          | TUR    |      90 |       6 |         0.367 |      0.068 |     -0.084 |           0 |            0 |   -1.403 | -0.028 |              0 |               0 |      0.129 |      -0.139 |  0.004 |  78.889 |

### Leads

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MEILLEUR B  | CAN    |     248 |      14 |         0.641 |      0.042 |     -0.044 |           0 |            0 |   -0.702 |  0.011 |              0 |               0 |      0.147 |      -0.104 |  0.001 |  88.71  |
| KIM S       | KOR    |     226 |      12 |         0.611 |      0.036 |     -0.038 |           0 |            0 |   -0.632 |  0.007 |              1 |               0 |      0.149 |      -0.15  | -0.005 |  86.947 |
| ANDERSON T  | USA    |     224 |      12 |         0.594 |      0.033 |     -0.045 |           0 |            0 |   -0.652 |  0.001 |              0 |               0 |      0.139 |      -0.098 |  0.001 |  89.062 |
| MABERGS S   | SWE    |     262 |      14 |         0.584 |      0.033 |     -0.048 |           0 |            0 |   -0.743 | -0.001 |              1 |               0 |      0.154 |      -0.107 | -0.001 |  89.559 |
| BARBEZAT M  | SUI    |     228 |      14 |         0.561 |      0.036 |     -0.041 |           0 |            0 |   -0.584 |  0.002 |              0 |               0 |      0.073 |      -0.086 |  0.001 |  87.004 |
| GOZUTOK A   | TUR    |     164 |       9 |         0.549 |      0.028 |     -0.052 |           0 |            0 |   -0.918 | -0.008 |              0 |               0 |      0.089 |      -0.126 | -0.002 |  80.64  |
| JENTSCH A   | GER    |     206 |      11 |         0.549 |      0.031 |     -0.046 |           0 |            0 |   -0.821 | -0.004 |              0 |               0 |      0.119 |      -0.119 | -0.003 |  81.22  |
| ROENNING M  | NOR    |     204 |      11 |         0.52  |      0.03  |     -0.04  |           0 |            0 |   -0.608 | -0.004 |              0 |               0 |      0.143 |      -0.09  | -0.001 |  88.235 |
| LARSEN M    | DEN    |     224 |      12 |         0.513 |      0.035 |     -0.043 |           0 |            0 |   -0.693 | -0.003 |              0 |               0 |      0.103 |      -0.11  |  0.004 |  87.5   |
| ZAPPONE V   | ITA    |     178 |      10 |         0.511 |      0.031 |     -0.048 |           0 |            0 |   -0.745 | -0.008 |              0 |               0 |      0.087 |      -0.136 |  0.007 |  83.708 |
| JACKSON S   | SCO    |      48 |       2 |         0.5   |      0.047 |     -0.055 |           0 |            0 |   -0.755 | -0.004 |              0 |               0 |      0.05  |      -0.094 |  0.009 |  79.688 |
| SVATONOVA K | CZE    |     218 |      12 |         0.495 |      0.038 |     -0.052 |           0 |            0 |   -0.682 | -0.008 |              0 |               1 |      0.135 |      -0.146 |  0.003 |  83.486 |
| ISHIGOOKA H | JPN    |     152 |       8 |         0.474 |      0.029 |     -0.063 |           0 |            1 |   -1.48  | -0.02  |              0 |               0 |      0.095 |      -0.114 |  0.003 |  81.126 |

