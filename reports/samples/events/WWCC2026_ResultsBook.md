# World Women's Curling Championship (WWCC2026_ResultsBook)

Calgary, AB, Canada, 2026; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The player tables show the spread of each player's shots, not just their average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more percentage points of win probability, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SUI    |      14 | 13-1     |  42.9 |   8.1 |  31.2 |       4   |    -0.5 |      70.6 |
| CAN    |      14 | 11-3     |  28.6 |   1.6 |  36   |      -9.1 |     0.1 |      67   |
| SWE    |      15 | 10-5     |  16.7 |   0.8 |  16   |      -0.3 |     0.3 |      60.3 |
| JPN    |      15 | 10-5     |  16.7 |   3.8 |   2.2 |       9.5 |     1.2 |      58.8 |
| KOR    |      13 | 8-5      |  11.5 |  -6.1 |   0.8 |      15.3 |     1.5 |      51.9 |
| TUR    |      13 | 7-6      |   3.8 |  -0.9 |  -7.3 |      12.7 |    -0.7 |      49.3 |
| CHN    |      12 | 6-6      |   0   |  -3.8 |   7.4 |      -4.9 |     1.2 |      50.2 |
| ITA    |      12 | 5-7      |  -8.3 |   0   |   2.5 |     -12.1 |     1.3 |      40.3 |
| NOR    |      12 | 4-8      | -16.7 |   1.9 |  -6.8 |      -9   |    -2.8 |      50   |
| SCO    |      12 | 4-8      | -16.7 |  -1.9 |  -0.8 |     -16.7 |     2.7 |      48.5 |
| DEN    |      12 | 3-9      | -25   |   0   | -15.3 |      -6.8 |    -2.8 |      39.2 |
| USA    |      12 | 2-10     | -33.3 |  -3.8 | -25.3 |      -2.5 |    -1.8 |      32.2 |
| AUS    |      12 | 1-11     | -41.7 |  -1.9 | -55.7 |      16.1 |    -0.2 |      20.4 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| EINARSON K    | CAN    |     248 |      14 |         0.661 |      0.289 |     -0.24  |  0.11  |          25 |           12 |   -4.177 |             41 |              19 |      1.081 |      -0.763 |  0.017 |  81.883 |
| GIM E         | KOR    |     242 |      13 |         0.616 |      0.291 |     -0.277 |  0.073 |          29 |           17 |   -4.713 |             32 |              22 |      1.015 |      -0.93  |  0.009 |  81.715 |
| HAN Y         | CHN    |     208 |      11 |         0.577 |      0.269 |     -0.23  |  0.058 |          17 |           12 |   -4.939 |             33 |              21 |      1.138 |      -0.622 |  0.006 |  80.435 |
| FUJISAWA S    | JPN    |     265 |      15 |         0.57  |      0.294 |     -0.259 |  0.056 |          28 |           18 |   -4.953 |             30 |              26 |      1.041 |      -0.933 |  0.02  |  78.22  |
| SCHWALLER X   | SUI    |     257 |      14 |         0.611 |      0.236 |     -0.232 |  0.054 |          15 |           12 |   -6.284 |             38 |              14 |      1.287 |      -0.819 | -0.001 |  85.925 |
| WRANAA I      | SWE    |     282 |      15 |         0.571 |      0.289 |     -0.282 |  0.044 |          31 |           18 |   -6.22  |             41 |              28 |      1.02  |      -1.009 |  0.007 |  76.971 |
| CONSTANTINI S | ITA    |     219 |      12 |         0.58  |      0.315 |     -0.362 |  0.031 |          23 |           22 |   -8.82  |             29 |              31 |      1.072 |      -1.249 |  0.022 |  76.968 |
| BJOERNSTAD T  | NOR    |     231 |      12 |         0.498 |      0.287 |     -0.267 |  0.009 |          21 |           22 |   -5.881 |             30 |              28 |      1.35  |      -1.314 |  0.014 |  76.432 |
| HENDERSON F   | SCO    |     223 |      12 |         0.502 |      0.27  |     -0.288 | -0.008 |          17 |           25 |   -6.187 |             26 |              30 |      1.55  |      -1.129 |  0.024 |  74.886 |
| YILDIZ D      | TUR    |     240 |      13 |         0.538 |      0.28  |     -0.36  | -0.016 |          24 |           30 |   -8.204 |             30 |              41 |      1.038 |      -1.372 |  0.012 |  76.261 |
| DUPONT M      | DEN    |     218 |      12 |         0.509 |      0.292 |     -0.382 | -0.039 |          21 |           31 |   -8.203 |             35 |              42 |      1.556 |      -1.048 |  0.006 |  70.642 |
| STROUSE D     | USA    |     203 |      12 |         0.458 |      0.31  |     -0.369 | -0.058 |          22 |           32 |   -8.739 |             23 |              29 |      0.664 |      -1.164 |  0.01  |  68.193 |
| WILLIAMS H    | AUS    |     190 |      12 |         0.416 |      0.265 |     -0.451 | -0.153 |          11 |           35 |   -9.392 |             11 |              36 |      1.093 |      -1.417 |  0.015 |  60.505 |

### Thirds

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| GAFNER S          | SUI    |     264 |      14 |         0.53  |      0.139 |     -0.129 |  0.013 |           2 |            4 |   -2.65  |             10 |               9 |      0.369 |      -0.432 | -0.011 |  88.783 |
| DE VAL A          | SWE    |     286 |      15 |         0.538 |      0.144 |     -0.152 |  0.008 |           3 |            8 |   -4.54  |             13 |              10 |      0.677 |      -0.673 | -0.01  |  82.692 |
| SWEETING V        | CAN    |     250 |      14 |         0.488 |      0.135 |     -0.114 |  0.008 |           2 |            2 |   -2.651 |              7 |               7 |      0.431 |      -0.364 | -0.003 |  83.434 |
| ZARDINI LACEDELLI | ITA    |     222 |      12 |         0.509 |      0.157 |     -0.154 |  0.004 |           4 |            3 |   -2.683 |             13 |              12 |      0.482 |      -0.365 |  0.017 |  79.955 |
| KIM M             | KOR    |     244 |      13 |         0.516 |      0.148 |     -0.152 |  0.003 |           6 |            7 |   -3.369 |             10 |              13 |      0.478 |      -0.522 | -0.003 |  81.967 |
| POLAT O           | TUR    |     242 |      13 |         0.475 |      0.151 |     -0.133 |  0.002 |           1 |            4 |   -2.703 |             15 |              11 |      0.492 |      -0.445 |  0.018 |  79.029 |
| YOSHIDA C         | JPN    |     172 |      10 |         0.5   |      0.13  |     -0.145 | -0.008 |           0 |            2 |   -2.638 |              4 |               6 |      0.28  |      -0.34  | -0.01  |  80.814 |
| HALSE M           | DEN    |     260 |      12 |         0.481 |      0.138 |     -0.149 | -0.011 |           4 |            4 |   -3.092 |             15 |              18 |      0.562 |      -0.75  |  0.013 |  76.346 |
| O'HARA A          | USA    |     206 |      12 |         0.49  |      0.16  |     -0.177 | -0.012 |           5 |            7 |   -3.328 |             11 |              10 |      0.5   |      -0.498 |  0.021 |  77.549 |
| WANG R            | CHN    |     222 |      12 |         0.477 |      0.123 |     -0.136 | -0.012 |           2 |            3 |   -2.781 |              7 |               8 |      0.358 |      -0.403 | -0     |  78.491 |
| WATT L            | SCO    |     118 |       6 |         0.466 |      0.145 |     -0.152 | -0.014 |           1 |            2 |   -2.58  |              6 |               9 |      0.458 |      -0.454 |  0.012 |  76.059 |
| DAVIE L           | SCO    |     110 |       6 |         0.509 |      0.143 |     -0.177 | -0.014 |           0 |            5 |   -3.064 |              3 |               7 |      0.271 |      -0.448 |  0     |  85.092 |
| KOANA T           | JPN    |      96 |       5 |         0.458 |      0.167 |     -0.168 | -0.015 |           3 |            4 |   -3.35  |              6 |               5 |      0.335 |      -0.364 |  0.003 |  76.302 |
| OESTGAARD N       | NOR    |     214 |      11 |         0.444 |      0.145 |     -0.158 | -0.023 |           2 |            7 |   -3.736 |              9 |              17 |      0.686 |      -0.528 |  0.008 |  76.285 |
| WESTMAN S         | AUS    |     162 |      10 |         0.407 |      0.119 |     -0.174 | -0.054 |           1 |            6 |   -3.375 |              4 |              11 |      0.364 |      -0.504 |  0.021 |  75.154 |

### Seconds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| BIRCHARD S   | CAN    |     250 |      14 |         0.552 |      0.088 |     -0.072 |  0.016 |           0 |            0 |   -1.36  |              5 |               2 |      0.346 |      -0.221 | -0.003 |  88.1   |
| SU T         | CHN    |      88 |       5 |         0.545 |      0.08  |     -0.075 |  0.01  |           0 |            0 |   -1.152 |              2 |               0 |      0.243 |      -0.146 | -0.011 |  84.375 |
| RIEDER F     | SUI    |     264 |      14 |         0.557 |      0.084 |     -0.098 |  0.004 |           0 |            2 |   -2.147 |              1 |               2 |      0.256 |      -0.325 | -0.007 |  89.504 |
| LARSSON M    | SWE    |     284 |      15 |         0.528 |      0.093 |     -0.096 |  0.004 |           0 |            2 |   -2.72  |              2 |               5 |      0.244 |      -0.499 | -0.003 |  82.218 |
| SUZUKI Y     | JPN    |     268 |      15 |         0.489 |      0.083 |     -0.096 | -0.009 |           0 |            0 |   -2.032 |              3 |               3 |      0.264 |      -0.274 |  0.007 |  80.357 |
| DUFF H       | SCO    |     228 |      12 |         0.439 |      0.088 |     -0.09  | -0.012 |           1 |            0 |   -1.736 |              3 |               2 |      0.368 |      -0.246 |  0.006 |  79.496 |
| KIM S        | KOR    |     228 |      12 |         0.465 |      0.079 |     -0.091 | -0.012 |           0 |            1 |   -2.141 |              2 |               4 |      0.251 |      -0.282 | -0.001 |  82.346 |
| KARAMAN I    | TUR    |     242 |      13 |         0.475 |      0.077 |     -0.099 | -0.015 |           0 |            0 |   -1.83  |              5 |               4 |      0.298 |      -0.326 |  0.008 |  73.347 |
| FORBREGD I   | NOR    |     232 |      12 |         0.444 |      0.08  |     -0.094 | -0.016 |           1 |            3 |   -2.69  |              6 |               5 |      0.562 |      -0.304 |  0.008 |  80.28  |
| SCHMIDT K    | DEN    |     188 |      10 |         0.41  |      0.069 |     -0.086 | -0.023 |           0 |            0 |   -1.888 |              1 |               4 |      0.214 |      -0.275 |  0.016 |  77.793 |
| MATHIS E     | ITA    |     222 |      12 |         0.441 |      0.072 |     -0.101 | -0.025 |           0 |            0 |   -1.865 |              1 |               0 |      0.223 |      -0.199 |  0.008 |  80.068 |
| DONG Z       | CHN    |     146 |       9 |         0.418 |      0.075 |     -0.097 | -0.025 |           0 |            1 |   -1.904 |              0 |               5 |      0.15  |      -0.294 |  0.004 |  81.164 |
| MULLANEY S   | USA    |     206 |      12 |         0.359 |      0.09  |     -0.105 | -0.035 |           0 |            1 |   -2.069 |              6 |               2 |      0.416 |      -0.252 |  0.003 |  76.341 |
| TSOURLENES K | AUS    |     166 |      10 |         0.313 |      0.071 |     -0.125 | -0.064 |           0 |            2 |   -2.177 |              2 |               1 |      0.338 |      -0.25  |  0.005 |  60.693 |

### Leads

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| BURGESS K    | CAN    |     246 |      14 |         0.699 |      0.043 |     -0.048 |  0.016 |           0 |            0 |   -0.908 |              0 |               0 |      0.148 |      -0.12  |  0.002 |  94.207 |
| SEOL YEJ     | KOR    |      36 |       2 |         0.694 |      0.047 |     -0.059 |  0.015 |           0 |            0 |   -0.445 |              0 |               0 |      0.099 |      -0.061 | -0.015 |  87.5   |
| RYCHIGER S   | SUI    |     264 |      14 |         0.659 |      0.047 |     -0.048 |  0.015 |           0 |            0 |   -0.823 |              0 |               0 |      0.133 |      -0.136 |  0.004 |  91.858 |
| STENLUND L   | SWE    |     286 |      15 |         0.65  |      0.045 |     -0.044 |  0.014 |           0 |            0 |   -0.687 |              1 |               0 |      0.156 |      -0.153 |  0.006 |  90.702 |
| SENGUL B     | TUR    |     242 |      13 |         0.583 |      0.044 |     -0.048 |  0.006 |           0 |            0 |   -0.76  |              0 |               1 |      0.157 |      -0.168 |  0.004 |  85.64  |
| SEOL YEE     | KOR    |     224 |      12 |         0.594 |      0.041 |     -0.046 |  0.006 |           0 |            0 |   -0.732 |              0 |               0 |      0.1   |      -0.124 |  0     |  90.29  |
| BEAR M       | USA    |     206 |      12 |         0.568 |      0.043 |     -0.044 |  0.005 |           0 |            0 |   -0.703 |              0 |               0 |      0.104 |      -0.099 |  0     |  85.801 |
| YOSHIDA Y    | JPN    |     268 |      15 |         0.534 |      0.041 |     -0.042 |  0.002 |           0 |            0 |   -0.647 |              0 |               0 |      0.089 |      -0.089 |  0.004 |  85.168 |
| MESLOE E     | NOR    |     232 |      12 |         0.487 |      0.052 |     -0.047 |  0.001 |           0 |            0 |   -0.739 |              0 |               0 |      0.132 |      -0.148 |  0.004 |  86.746 |
| JIANG J      | CHN    |     222 |      12 |         0.55  |      0.038 |     -0.045 |  0.001 |           0 |            0 |   -0.691 |              0 |               0 |      0.117 |      -0.103 |  0.003 |  90.271 |
| MCMILLAN K   | SCO    |     228 |      12 |         0.561 |      0.041 |     -0.053 | -0     |           0 |            0 |   -0.888 |              1 |               0 |      0.166 |      -0.13  |  0.001 |  88.326 |
| LO DESERTO M | ITA    |     222 |      12 |         0.518 |      0.044 |     -0.051 | -0.002 |           0 |            0 |   -0.851 |              0 |               0 |      0.106 |      -0.176 |  0.001 |  87.162 |
| ARMSTRONG M  | AUS    |      82 |       6 |         0.549 |      0.049 |     -0.077 | -0.008 |           0 |            0 |   -0.765 |              0 |               0 |      0.055 |      -0.092 |  0.001 |  80.488 |
| LARSEN M     | DEN    |     206 |      10 |         0.51  |      0.042 |     -0.061 | -0.008 |           0 |            0 |   -1.236 |              0 |               0 |      0.13  |      -0.149 |  0.001 |  82.16  |
| TITHERIDGE K | AUS    |     160 |      10 |         0.525 |      0.043 |     -0.139 | -0.044 |           0 |            4 |   -3.018 |              0 |               4 |      0.097 |      -0.346 |  0.018 |  75.781 |

