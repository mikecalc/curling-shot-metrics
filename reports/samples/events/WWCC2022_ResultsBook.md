# World Women's Curling Championship (WWCC2022_ResultsBook)

Prince George, BC, Canada, 2022; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SUI    |      14 | 14-0     |  50   |   1.6 |  39.6 |       8.6 |     0.1 |      75.3 |
| CAN    |      14 | 10-4     |  21.4 |   0   |  18.7 |       3.4 |    -0.6 |      64.2 |
| KOR    |      12 | 8-4      |  16.7 |   3.8 |  18.8 |      -6   |     0.1 |      56   |
| SWE    |      14 | 9-5      |  14.3 |  -1.6 |  21.5 |      -5.9 |     0.3 |      59   |
| USA    |      12 | 7-5      |   8.3 |   1.9 |   1.5 |       4.5 |     0.3 |      60.1 |
| JPN    |      10 | 5-5      |   0   |  -4.6 |  -9   |      11.9 |     1.7 |      47.3 |
| DEN    |      12 | 6-6      |   0   |   0   |   1.1 |      -0.4 |    -0.7 |      43.7 |
| NOR    |      11 | 4-7      | -13.6 |   1   | -12   |       0.4 |    -3   |      50.2 |
| GER    |      11 | 4-7      | -13.6 |   1   | -15.1 |      -0.3 |     0.7 |      36.5 |
| ITA    |      11 | 3-8      | -22.7 |  -1   | -28.2 |       5.2 |     1.3 |      36.3 |
| CZE    |      12 | 2-10     | -33.3 |   0   | -26.7 |      -5.6 |    -1   |      36.2 |
| TUR    |      11 | 1-10     | -40.9 |  -3.1 | -23.4 |     -15   |     0.6 |      27.8 |
| SCO    |       2 | 0-2      | -50   |   0   | -49.2 |      -4.1 |     3.3 |      19.1 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| SCO    |      127 |   0.028 |    -0.084 |          0.756 |                2.263 |                   2.813 |
| KOR    |      918 |   0.023 |     0.005 |          0.623 |                2.048 |                   2.311 |
| DEN    |      897 |   0.012 |    -0.002 |          0.625 |                2.283 |                   2.141 |
| GER    |      823 |   0.01  |    -0.009 |          0.621 |                2.01  |                   2.171 |
| NOR    |      827 |   0.009 |    -0.015 |          0.644 |                2.147 |                   2.052 |
| USA    |      885 |   0.004 |    -0.012 |          0.611 |                1.969 |                   2.36  |
| CZE    |      871 |   0.002 |    -0.014 |          0.615 |                2.039 |                   2.032 |
| TUR    |      786 |  -0.002 |    -0.012 |          0.625 |                2.169 |                   2.041 |
| SWE    |     1053 |  -0.002 |     0.013 |          0.599 |                1.932 |                   1.979 |
| JPN    |      715 |  -0.004 |     0.006 |          0.607 |                2.179 |                   2.058 |
| ITA    |      796 |  -0.012 |    -0.008 |          0.594 |                1.948 |                   1.884 |
| CAN    |     1004 |  -0.018 |     0.019 |          0.58  |                2.328 |                   2.2   |
| SUI    |      968 |  -0.022 |     0.032 |          0.546 |                2.208 |                   1.994 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| PAETZ A       | SUI    |     240 |      14 |         0.679 |      0.275 |     -0.267 |          21 |           12 |   -5.561 |  0.101 |             40 |              18 |      1.268 |      -1.008 |  0.006 |  89.391 |
| EINARSON K    | CAN    |     249 |      14 |         0.606 |      0.295 |     -0.348 |          26 |           27 |   -6.851 |  0.042 |             35 |              30 |      1.348 |      -1.219 |  0.008 |  80.221 |
| HASSELBORG A  | SWE    |     265 |      14 |         0.604 |      0.249 |     -0.219 |          18 |           14 |   -4.853 |  0.063 |             28 |              22 |      1.225 |      -0.932 |  0.008 |  82.481 |
| KIM E         | KOR    |     231 |      12 |         0.602 |      0.249 |     -0.273 |          20 |           16 |   -7.158 |  0.041 |             37 |              26 |      1.318 |      -1.879 | -0     |  77.851 |
| CHRISTENSEN C | USA    |     224 |      12 |         0.58  |      0.244 |     -0.271 |          18 |           18 |   -5.551 |  0.028 |             27 |              23 |      1.001 |      -1.4   | -0.007 |  79.709 |
| JENTSCH D     | GER    |     207 |      11 |         0.551 |      0.275 |     -0.283 |          18 |           19 |   -5.353 |  0.024 |             23 |              24 |      0.698 |      -0.909 |  0.025 |  76.585 |
| YILDIZ D      | TUR    |     199 |      11 |         0.523 |      0.287 |     -0.397 |          17 |           23 |   -9.432 | -0.039 |             20 |              29 |      0.841 |      -0.816 | -0.006 |  69.005 |
| SKASLIEN K    | NOR    |     207 |      11 |         0.517 |      0.281 |     -0.343 |          18 |           21 |   -8.854 | -0.02  |             16 |              31 |      0.957 |      -0.954 | -0.016 |  75.735 |
| DUPONT M      | DEN    |     219 |      12 |         0.502 |      0.343 |     -0.311 |          23 |           24 |   -7.006 |  0.017 |             36 |              35 |      1.63  |      -1.006 | -0.003 |  73.832 |
| BAUDYSOVA A   | CZE    |     219 |      12 |         0.479 |      0.3   |     -0.336 |          17 |           27 |   -7.594 | -0.031 |             24 |              30 |      0.898 |      -1.221 |  0.007 |  72.106 |
| KITAZAWA I    | JPN    |     180 |      10 |         0.467 |      0.257 |     -0.295 |           9 |           19 |   -7.415 | -0.037 |             19 |              26 |      0.74  |      -1.267 |  0.011 |  75.424 |
| CONSTANTINI S | ITA    |     203 |      11 |         0.448 |      0.224 |     -0.292 |          11 |           25 |   -6.735 | -0.061 |             14 |              30 |      0.786 |      -1.262 |  0.001 |  71.766 |
| AITKEN G      | SCO    |      32 |       2 |         0.344 |      0.34  |     -0.588 |           4 |            7 |   -8.521 | -0.269 |              2 |               7 |      0.249 |      -0.791 |  0.058 |  56.25  |

### Thirds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KIM K        | KOR    |     234 |      12 |         0.594 |      0.154 |     -0.17  |           1 |            8 |   -3.907 |  0.022 |             16 |              14 |      0.701 |      -0.721 |  0.009 |  85.256 |
| ROERVIK M    | NOR    |     209 |      11 |         0.584 |      0.141 |     -0.149 |           5 |            1 |   -2.529 |  0.02  |              6 |               4 |      0.447 |      -0.282 | -0.005 |  80.383 |
| SWEETING V   | CAN    |     252 |      14 |         0.583 |      0.156 |     -0.158 |           5 |            4 |   -2.694 |  0.025 |             14 |              14 |      0.594 |      -0.423 | -0.015 |  84.028 |
| NAKAJIMA S   | JPN    |     110 |       6 |         0.564 |      0.161 |     -0.133 |           0 |            0 |   -1.823 |  0.033 |              5 |               2 |      0.383 |      -0.267 |  0.013 |  82.045 |
| TIRINZONI S  | SUI    |     230 |      14 |         0.561 |      0.13  |     -0.134 |           1 |            4 |   -2.897 |  0.014 |              6 |              12 |      0.365 |      -0.477 | -0.006 |  87.174 |
| MCMANUS S    | SWE    |     268 |      14 |         0.552 |      0.128 |     -0.117 |           3 |            2 |   -2.498 |  0.018 |              9 |               6 |      0.429 |      -0.503 | -0.006 |  86.94  |
| POLAT O      | TUR    |     200 |      11 |         0.515 |      0.151 |     -0.149 |           3 |            3 |   -2.881 |  0.006 |             12 |              10 |      0.444 |      -0.471 |  0.006 |  78.125 |
| ANDERSON S   | USA    |     224 |      12 |         0.487 |      0.099 |     -0.123 |           1 |            1 |   -2.551 | -0.015 |              1 |              10 |      0.299 |      -0.509 | -0.012 |  78.46  |
| ABBES E      | GER    |     210 |      11 |         0.443 |      0.115 |     -0.167 |           2 |            5 |   -3.266 | -0.042 |              5 |              16 |      0.356 |      -0.583 |  0.011 |  74.762 |
| LO DESERTO M | ITA    |     205 |      11 |         0.42  |      0.125 |     -0.115 |           3 |            3 |   -2.698 | -0.014 |              5 |              11 |      0.387 |      -0.464 |  0.002 |  77.927 |
| HALSE M      | DEN    |     226 |      12 |         0.412 |      0.14  |     -0.128 |           2 |            4 |   -3.053 | -0.018 |              8 |              12 |      0.429 |      -0.518 | -0.001 |  76.77  |
| SINCLAIR S   | SCO    |      48 |       2 |         0.396 |      0.118 |     -0.121 |           0 |            1 |   -1.911 | -0.027 |              0 |               0 |      0.167 |      -0.162 |  0.039 |  80.729 |
| MATSUMURA C  | JPN    |     112 |       6 |         0.393 |      0.125 |     -0.089 |           2 |            0 |   -1.529 | -0.005 |              4 |               1 |      0.372 |      -0.222 |  0.013 |  84.152 |
| VINSOVA P    | CZE    |     222 |      12 |         0.392 |      0.138 |     -0.157 |           3 |            7 |   -3.602 | -0.041 |              9 |              10 |      0.453 |      -0.545 | -0.002 |  75.225 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| BIRCHARD S       | CAN    |     252 |      14 |         0.548 |      0.077 |     -0.094 |           0 |            0 |   -1.928 | -0.001 |              2 |               2 |      0.212 |      -0.289 | -0.012 |  84.425 |
| PERSINGER V      | USA    |     218 |      12 |         0.532 |      0.096 |     -0.077 |           0 |            1 |   -1.948 |  0.015 |              7 |               2 |      0.363 |      -0.321 |  0.002 |  85.55  |
| NEUENSCHWANDER E | SUI    |     216 |      13 |         0.509 |      0.094 |     -0.072 |           1 |            0 |   -1.243 |  0.013 |              3 |               1 |      0.363 |      -0.198 | -0.001 |  91.163 |
| KIM C            | KOR    |     234 |      12 |         0.504 |      0.07  |     -0.079 |           0 |            0 |   -1.569 | -0.004 |              3 |               3 |      0.285 |      -0.26  | -0.007 |  82.833 |
| HOWALD C         | SUI    |      60 |       7 |         0.5   |      0.058 |     -0.056 |           0 |            0 |   -0.79  |  0.001 |              0 |               0 |      0.122 |      -0.073 | -0.013 |  86.667 |
| KNOCHENHAUER A   | SWE    |     248 |      13 |         0.492 |      0.075 |     -0.079 |           1 |            0 |   -1.462 | -0.004 |              4 |               1 |      0.322 |      -0.204 | -0.005 |  83.776 |
| DUPONT D         | DEN    |     226 |      12 |         0.469 |      0.097 |     -0.087 |           0 |            0 |   -1.882 | -0.001 |              4 |               3 |      0.298 |      -0.269 |  0.008 |  83.407 |
| HASLEV NORDBYE M | NOR    |     202 |      11 |         0.45  |      0.081 |     -0.086 |           0 |            0 |   -1.612 | -0.011 |              0 |               1 |      0.136 |      -0.197 |  0.007 |  85.149 |
| HOEHNE M         | GER    |     210 |      11 |         0.448 |      0.077 |     -0.089 |           0 |            1 |   -2.123 | -0.015 |              2 |               3 |      0.242 |      -0.328 |  0.002 |  74.643 |
| ROMEI A          | ITA    |     206 |      11 |         0.442 |      0.071 |     -0.074 |           0 |            0 |   -1.681 | -0.01  |              3 |               2 |      0.261 |      -0.244 |  0.009 |  81.74  |
| SUZUKI M         | JPN    |     166 |       9 |         0.422 |      0.062 |     -0.085 |           1 |            2 |   -2.401 | -0.023 |              2 |               4 |      0.247 |      -0.298 |  0.006 |  80.723 |
| BAUDYSOVA M      | CZE    |     222 |      12 |         0.401 |      0.058 |     -0.095 |           0 |            0 |   -1.903 | -0.034 |              0 |               3 |      0.154 |      -0.29  |  0     |  76.914 |
| SENGUL B         | TUR    |     144 |       8 |         0.375 |      0.082 |     -0.12  |           0 |            2 |   -2.534 | -0.044 |              2 |               4 |      0.268 |      -0.31  | -0     |  69.097 |
| POLAT M          | TUR    |      92 |       6 |         0.359 |      0.069 |     -0.081 |           0 |            0 |   -1.427 | -0.027 |              0 |               0 |      0.125 |      -0.144 |  0.005 |  78.261 |

### Leads

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MEILLEUR B  | CAN    |     252 |      14 |         0.631 |      0.041 |     -0.041 |           0 |            0 |   -0.753 |  0.011 |              0 |               0 |      0.137 |      -0.115 |  0.001 |  88.889 |
| ANDERSON T  | USA    |     224 |      12 |         0.594 |      0.032 |     -0.042 |           0 |            0 |   -0.663 |  0.002 |              0 |               0 |      0.152 |      -0.096 |  0.002 |  89.062 |
| KIM S       | KOR    |     228 |      12 |         0.575 |      0.038 |     -0.034 |           0 |            0 |   -0.622 |  0.008 |              1 |               0 |      0.144 |      -0.143 | -0.006 |  87.061 |
| GOZUTOK A   | TUR    |     164 |       9 |         0.567 |      0.027 |     -0.053 |           0 |            0 |   -0.901 | -0.008 |              0 |               0 |      0.084 |      -0.123 | -0.006 |  80.64  |
| JENTSCH A   | GER    |     210 |      11 |         0.552 |      0.03  |     -0.046 |           0 |            0 |   -0.808 | -0.004 |              0 |               0 |      0.107 |      -0.123 | -0.005 |  80.861 |
| MABERGS S   | SWE    |     264 |      14 |         0.534 |      0.038 |     -0.04  |           0 |            0 |   -0.74  |  0.002 |              1 |               0 |      0.146 |      -0.099 | -0.001 |  89.599 |
| ZAPPONE V   | ITA    |     182 |      10 |         0.533 |      0.032 |     -0.046 |           0 |            0 |   -0.754 | -0.005 |              0 |               0 |      0.1   |      -0.134 |  0.006 |  83.75  |
| BARBEZAT M  | SUI    |     230 |      14 |         0.522 |      0.036 |     -0.035 |           0 |            0 |   -0.673 |  0.002 |              0 |               0 |      0.072 |      -0.072 |  0.002 |  87.118 |
| LARSEN M    | DEN    |     226 |      12 |         0.504 |      0.035 |     -0.041 |           0 |            0 |   -0.711 | -0.003 |              0 |               0 |      0.096 |      -0.106 |  0.004 |  87.611 |
| SVATONOVA K | CZE    |     222 |      12 |         0.495 |      0.038 |     -0.053 |           0 |            0 |   -0.674 | -0.008 |              0 |               1 |      0.125 |      -0.155 |  0.002 |  83.559 |
| ROENNING M  | NOR    |     210 |      11 |         0.495 |      0.031 |     -0.036 |           0 |            0 |   -0.601 | -0.003 |              0 |               0 |      0.124 |      -0.086 |  0     |  88.571 |
| ISHIGOOKA H | JPN    |     152 |       8 |         0.461 |      0.028 |     -0.059 |           0 |            1 |   -1.43  | -0.019 |              0 |               0 |      0.099 |      -0.107 |  0.002 |  81.126 |
| JACKSON S   | SCO    |      48 |       2 |         0.396 |      0.05  |     -0.045 |           0 |            0 |   -0.633 | -0.007 |              0 |               0 |      0.047 |      -0.081 |  0.005 |  79.688 |

