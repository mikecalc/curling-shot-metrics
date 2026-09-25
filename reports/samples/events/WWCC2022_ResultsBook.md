# World Women's Curling Championship (WWCC2022_ResultsBook)

Prince George, BC, Canada, 2022; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Women

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| SUI    |      14 | 14-0     |               68.5 |
| SWE    |      14 | 9-5      |               52.9 |
| KOR    |      12 | 8-4      |               50.1 |
| CAN    |      14 | 10-4     |               47   |
| JPN    |      10 | 5-5      |               37.5 |
| USA    |      12 | 7-5      |               37   |
| DEN    |      12 | 6-6      |               31.1 |
| NOR    |      11 | 4-7      |               29   |
| GER    |      11 | 4-7      |               21.2 |
| TUR    |      11 | 1-10     |                6.2 |
| CZE    |      12 | 2-10     |                4.6 |
| ITA    |      11 | 3-8      |                4.6 |
| SCO    |       2 | 0-2      |              -21.3 |

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
| PAETZ A       | SUI    |     238 |      14 |         0.676 |      0.275 |     -0.251 |          24 |            8 |   -5.826 |  0.105 |             46 |              18 |      1.323 |      -0.956 |  0.005 |  89.301 |
| HASSELBORG A  | SWE    |     264 |      14 |         0.617 |      0.255 |     -0.213 |          22 |           13 |   -4.591 |  0.076 |             29 |              17 |      1.053 |      -0.876 |  0.014 |  82.414 |
| EINARSON K    | CAN    |     247 |      14 |         0.615 |      0.306 |     -0.346 |          25 |           20 |   -7.039 |  0.055 |             39 |              32 |      1.336 |      -1.401 |  0.012 |  80.466 |
| KIM E         | KOR    |     231 |      12 |         0.584 |      0.243 |     -0.271 |          16 |           15 |   -6.524 |  0.03  |             40 |              25 |      1.148 |      -1.778 |  0.009 |  77.851 |
| CHRISTENSEN C | USA    |     224 |      12 |         0.545 |      0.262 |     -0.266 |          18 |           14 |   -5.609 |  0.021 |             38 |              25 |      0.997 |      -1.459 |  0.008 |  79.709 |
| JENTSCH D     | GER    |     205 |      11 |         0.537 |      0.281 |     -0.311 |          18 |           22 |   -5.178 |  0.007 |             21 |              30 |      0.699 |      -0.899 |  0.036 |  76.478 |
| SKASLIEN K    | NOR    |     204 |      11 |         0.529 |      0.293 |     -0.325 |          17 |           23 |   -7.967 |  0.002 |             24 |              27 |      0.959 |      -0.847 | -0.005 |  75.373 |
| YILDIZ D      | TUR    |     198 |      11 |         0.515 |      0.299 |     -0.374 |          17 |           22 |   -9.004 | -0.027 |             20 |              29 |      0.848 |      -0.82  | -0.014 |  68.846 |
| KITAZAWA I    | JPN    |     180 |      10 |         0.511 |      0.269 |     -0.31  |          11 |           16 |   -7.594 | -0.014 |             24 |              24 |      0.619 |      -1.287 |  0.022 |  75.424 |
| DUPONT M      | DEN    |     217 |      12 |         0.493 |      0.324 |     -0.3   |          19 |           22 |   -7.119 |  0.008 |             30 |              31 |      1.634 |      -1.026 |  0.001 |  73.585 |
| BAUDYSOVA A   | CZE    |     217 |      12 |         0.479 |      0.295 |     -0.329 |          18 |           27 |   -7.282 | -0.03  |             25 |              34 |      0.816 |      -1.192 |  0.015 |  72.079 |
| CONSTANTINI S | ITA    |     202 |      11 |         0.436 |      0.226 |     -0.285 |           8 |           23 |   -7.313 | -0.062 |             18 |              36 |      0.543 |      -1.24  |  0.009 |  72.125 |
| AITKEN G      | SCO    |      32 |       2 |         0.375 |      0.337 |     -0.627 |           3 |            7 |   -8.857 | -0.265 |              2 |               6 |      0.194 |      -0.761 |  0.048 |  56.25  |

### Thirds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| NAKAJIMA S   | JPN    |     110 |       6 |         0.582 |      0.14  |     -0.134 |           0 |            2 |   -2.208 |  0.025 |              4 |               5 |      0.275 |      -0.323 |  0.017 |  82.045 |
| SWEETING V   | CAN    |     248 |      14 |         0.565 |      0.146 |     -0.143 |           8 |            4 |   -2.846 |  0.02  |              9 |              15 |      0.617 |      -0.517 | -0.011 |  84.173 |
| MCMANUS S    | SWE    |     266 |      14 |         0.553 |      0.131 |     -0.106 |           2 |            2 |   -2.471 |  0.025 |             13 |               9 |      0.403 |      -0.539 | -0.008 |  86.842 |
| ROERVIK M    | NOR    |     204 |      11 |         0.549 |      0.133 |     -0.126 |           2 |            2 |   -2.695 |  0.016 |              3 |               3 |      0.335 |      -0.355 |  0.001 |  81.373 |
| KIM K        | KOR    |     232 |      12 |         0.547 |      0.151 |     -0.135 |           2 |            4 |   -2.79  |  0.022 |             14 |              13 |      0.521 |      -0.51  |  0.012 |  85.129 |
| TIRINZONI S  | SUI    |     228 |      14 |         0.539 |      0.112 |     -0.135 |           0 |            3 |   -2.64  | -0.002 |              3 |              11 |      0.26  |      -0.398 | -0.003 |  87.061 |
| ANDERSON S   | USA    |     224 |      12 |         0.487 |      0.101 |     -0.117 |           1 |            1 |   -2.075 | -0.011 |              5 |               7 |      0.387 |      -0.402 | -0.007 |  78.46  |
| HALSE M      | DEN    |     224 |      12 |         0.451 |      0.119 |     -0.136 |           0 |            3 |   -3.042 | -0.021 |              7 |              12 |      0.38  |      -0.433 | -0     |  76.562 |
| POLAT O      | TUR    |     198 |      11 |         0.424 |      0.133 |     -0.141 |           2 |            2 |   -2.402 | -0.025 |              8 |               7 |      0.386 |      -0.361 |  0.006 |  77.904 |
| ABBES E      | GER    |     206 |      11 |         0.413 |      0.128 |     -0.149 |           1 |            4 |   -2.574 | -0.035 |              3 |              10 |      0.335 |      -0.371 |  0.017 |  74.515 |
| VINSOVA P    | CZE    |     218 |      12 |         0.385 |      0.113 |     -0.158 |           0 |            6 |   -3.312 | -0.053 |              8 |              14 |      0.368 |      -0.504 | -0.002 |  75.229 |
| MATSUMURA C  | JPN    |     112 |       6 |         0.366 |      0.129 |     -0.082 |           3 |            0 |   -1.589 | -0.005 |              3 |               1 |      0.371 |      -0.202 |  0.008 |  84.152 |
| LO DESERTO M | ITA    |     202 |      11 |         0.361 |      0.113 |     -0.121 |           2 |            4 |   -2.786 | -0.036 |              6 |              10 |      0.361 |      -0.394 |  0.01  |  78.094 |
| SINCLAIR S   | SCO    |      48 |       2 |         0.354 |      0.118 |     -0.106 |           1 |            2 |   -1.806 | -0.027 |              1 |               1 |      0.173 |      -0.142 |  0.017 |  80.729 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HOWALD C         | SUI    |      60 |       7 |         0.567 |      0.068 |     -0.056 |           0 |            0 |   -0.559 |  0.014 |              1 |               0 |      0.151 |      -0.09  | -0.016 |  86.667 |
| PERSINGER V      | USA    |     218 |      12 |         0.514 |      0.097 |     -0.082 |           0 |            1 |   -1.863 |  0.01  |              5 |               4 |      0.297 |      -0.329 |  0.003 |  85.55  |
| DUPONT D         | DEN    |     224 |      12 |         0.482 |      0.086 |     -0.082 |           0 |            1 |   -1.684 | -0.001 |              1 |               3 |      0.21  |      -0.256 |  0.009 |  83.482 |
| HASLEV NORDBYE M | NOR    |     196 |      11 |         0.48  |      0.076 |     -0.08  |           0 |            1 |   -1.705 | -0.005 |              1 |               1 |      0.184 |      -0.228 |  0.005 |  85.842 |
| KIM C            | KOR    |     232 |      12 |         0.478 |      0.072 |     -0.075 |           0 |            0 |   -1.4   | -0.005 |              3 |               3 |      0.257 |      -0.278 | -0.008 |  82.684 |
| SUZUKI M         | JPN    |     166 |       9 |         0.476 |      0.073 |     -0.091 |           0 |            1 |   -2.145 | -0.013 |              1 |               1 |      0.228 |      -0.207 |  0.005 |  80.723 |
| BIRCHARD S       | CAN    |     248 |      14 |         0.472 |      0.085 |     -0.079 |           0 |            1 |   -2.15  | -0.001 |              0 |               3 |      0.194 |      -0.282 | -0.007 |  84.173 |
| ROMEI A          | ITA    |     202 |      11 |         0.45  |      0.076 |     -0.085 |           0 |            1 |   -2.185 | -0.012 |              1 |               1 |      0.227 |      -0.281 |  0.01  |  81.592 |
| HOEHNE M         | GER    |     206 |      11 |         0.447 |      0.081 |     -0.097 |           0 |            3 |   -2.693 | -0.017 |              0 |               4 |      0.189 |      -0.394 |  0.005 |  74.272 |
| NEUENSCHWANDER E | SUI    |     214 |      13 |         0.439 |      0.098 |     -0.072 |           1 |            0 |   -1.484 |  0.003 |              6 |               1 |      0.374 |      -0.213 | -0.002 |  91.197 |
| KNOCHENHAUER A   | SWE    |     246 |      13 |         0.439 |      0.083 |     -0.074 |           1 |            0 |   -1.243 | -0.005 |              3 |               1 |      0.303 |      -0.188 | -0.001 |  83.709 |
| SENGUL B         | TUR    |     142 |       8 |         0.43  |      0.084 |     -0.111 |           0 |            0 |   -1.966 | -0.027 |              4 |               3 |      0.305 |      -0.249 |  0.002 |  68.662 |
| POLAT M          | TUR    |      90 |       6 |         0.4   |      0.052 |     -0.076 |           0 |            1 |   -1.318 | -0.025 |              0 |               0 |      0.095 |      -0.167 |  0.003 |  78.889 |
| BAUDYSOVA M      | CZE    |     218 |      12 |         0.358 |      0.049 |     -0.081 |           0 |            0 |   -1.364 | -0.034 |              0 |               0 |      0.135 |      -0.22  |  0.002 |  77.179 |

### Leads

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KIM S       | KOR    |     226 |      12 |         0.588 |      0.038 |     -0.044 |           0 |            0 |   -0.742 |  0.005 |              0 |               0 |      0.098 |      -0.1   | -0.004 |  86.947 |
| MEILLEUR B  | CAN    |     248 |      14 |         0.585 |      0.043 |     -0.041 |           0 |            0 |   -0.927 |  0.008 |              0 |               0 |      0.122 |      -0.109 |  0.001 |  88.71  |
| BARBEZAT M  | SUI    |     228 |      14 |         0.566 |      0.044 |     -0.042 |           0 |            0 |   -0.723 |  0.007 |              0 |               0 |      0.098 |      -0.123 |  0.002 |  87.004 |
| ROENNING M  | NOR    |     204 |      11 |         0.564 |      0.034 |     -0.033 |           0 |            0 |   -0.651 |  0.005 |              0 |               0 |      0.113 |      -0.086 | -0.001 |  88.235 |
| JENTSCH A   | GER    |     206 |      11 |         0.563 |      0.033 |     -0.05  |           0 |            0 |   -0.95  | -0.003 |              0 |               0 |      0.11  |      -0.125 | -0.004 |  81.22  |
| GOZUTOK A   | TUR    |     164 |       9 |         0.53  |      0.028 |     -0.047 |           0 |            0 |   -1.105 | -0.007 |              0 |               0 |      0.071 |      -0.153 | -0.006 |  80.64  |
| MABERGS S   | SWE    |     262 |      14 |         0.523 |      0.039 |     -0.037 |           0 |            0 |   -0.83  |  0.002 |              0 |               0 |      0.134 |      -0.119 | -0.001 |  89.559 |
| ANDERSON T  | USA    |     224 |      12 |         0.509 |      0.04  |     -0.034 |           0 |            0 |   -0.656 |  0.004 |              0 |               0 |      0.137 |      -0.098 |  0.001 |  89.062 |
| LARSEN M    | DEN    |     224 |      12 |         0.509 |      0.038 |     -0.038 |           0 |            0 |   -0.621 |  0.001 |              0 |               0 |      0.131 |      -0.098 |  0.002 |  87.5   |
| ZAPPONE V   | ITA    |     178 |      10 |         0.489 |      0.041 |     -0.043 |           0 |            0 |   -0.766 | -0.002 |              0 |               0 |      0.137 |      -0.131 |  0.005 |  83.708 |
| ISHIGOOKA H | JPN    |     152 |       8 |         0.487 |      0.036 |     -0.049 |           0 |            0 |   -0.903 | -0.008 |              0 |               0 |      0.127 |      -0.105 |  0     |  81.126 |
| JACKSON S   | SCO    |      48 |       2 |         0.458 |      0.034 |     -0.056 |           0 |            0 |   -0.731 | -0.015 |              0 |               0 |      0.07  |      -0.097 |  0.008 |  79.688 |
| SVATONOVA K | CZE    |     218 |      12 |         0.436 |      0.044 |     -0.047 |           0 |            0 |   -0.837 | -0.007 |              0 |               0 |      0.12  |      -0.142 |  0.001 |  83.486 |

