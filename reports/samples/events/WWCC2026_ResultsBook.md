# World Women's Curling Championship (WWCC2026_ResultsBook)

Calgary, AB, Canada, 2026; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

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

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| DEN    |      866 |   0.023 |    -0.02  |          0.64  |                2.295 |                   2.03  |
| USA    |      810 |   0.017 |    -0.043 |          0.659 |                2.101 |                   2.089 |
| ITA    |      874 |   0.016 |    -0.004 |          0.624 |                2.135 |                   2.084 |
| SCO    |      900 |   0.011 |     0.011 |          0.604 |                1.99  |                   1.958 |
| AUS    |      751 |   0.004 |    -0.04  |          0.622 |                1.986 |                   2.571 |
| CAN    |      990 |   0.001 |     0.015 |          0.604 |                2.185 |                   2.161 |
| TUR    |      951 |  -0     |    -0.007 |          0.637 |                2.082 |                   2.278 |
| SUI    |     1040 |  -0.003 |     0.006 |          0.588 |                2.057 |                   1.946 |
| KOR    |      974 |  -0.003 |     0.007 |          0.593 |                2.28  |                   2.076 |
| JPN    |     1054 |  -0.012 |     0.013 |          0.576 |                2.01  |                   2.234 |
| NOR    |      922 |  -0.013 |    -0.008 |          0.612 |                1.938 |                   1.902 |
| CHN    |      877 |  -0.015 |     0.028 |          0.566 |                2.053 |                   1.959 |
| SWE    |     1133 |  -0.016 |     0.02  |          0.566 |                2.207 |                   2.103 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| EINARSON K    | CAN    |     248 |      14 |         0.661 |      0.289 |     -0.24  |          25 |           12 |   -4.177 |  0.11  |             41 |              19 |      1.081 |      -0.763 |  0.017 |  81.883 |
| GIM E         | KOR    |     242 |      13 |         0.616 |      0.291 |     -0.277 |          29 |           17 |   -4.713 |  0.073 |             32 |              22 |      1.015 |      -0.93  |  0.009 |  81.715 |
| SCHWALLER X   | SUI    |     257 |      14 |         0.611 |      0.236 |     -0.232 |          15 |           12 |   -6.284 |  0.054 |             38 |              14 |      1.287 |      -0.819 | -0.001 |  85.925 |
| CONSTANTINI S | ITA    |     219 |      12 |         0.58  |      0.315 |     -0.362 |          23 |           22 |   -8.82  |  0.031 |             29 |              31 |      1.072 |      -1.249 |  0.022 |  76.968 |
| HAN Y         | CHN    |     208 |      11 |         0.577 |      0.269 |     -0.23  |          17 |           12 |   -4.939 |  0.058 |             33 |              21 |      1.138 |      -0.622 |  0.006 |  80.435 |
| WRANAA I      | SWE    |     282 |      15 |         0.571 |      0.289 |     -0.282 |          31 |           18 |   -6.22  |  0.044 |             41 |              28 |      1.02  |      -1.009 |  0.007 |  76.971 |
| FUJISAWA S    | JPN    |     265 |      15 |         0.57  |      0.294 |     -0.259 |          28 |           18 |   -4.953 |  0.056 |             30 |              26 |      1.041 |      -0.933 |  0.02  |  78.22  |
| YILDIZ D      | TUR    |     240 |      13 |         0.538 |      0.28  |     -0.36  |          24 |           30 |   -8.204 | -0.016 |             30 |              41 |      1.038 |      -1.372 |  0.012 |  76.261 |
| DUPONT M      | DEN    |     218 |      12 |         0.509 |      0.292 |     -0.382 |          21 |           31 |   -8.203 | -0.039 |             35 |              42 |      1.556 |      -1.048 |  0.006 |  70.642 |
| HENDERSON F   | SCO    |     223 |      12 |         0.502 |      0.27  |     -0.288 |          17 |           25 |   -6.187 | -0.008 |             26 |              30 |      1.55  |      -1.129 |  0.024 |  74.886 |
| BJOERNSTAD T  | NOR    |     231 |      12 |         0.498 |      0.287 |     -0.267 |          21 |           22 |   -5.881 |  0.009 |             30 |              28 |      1.35  |      -1.314 |  0.014 |  76.432 |
| STROUSE D     | USA    |     203 |      12 |         0.458 |      0.31  |     -0.369 |          22 |           32 |   -8.739 | -0.058 |             23 |              29 |      0.664 |      -1.164 |  0.01  |  68.193 |
| WILLIAMS H    | AUS    |     190 |      12 |         0.416 |      0.265 |     -0.451 |          11 |           35 |   -9.392 | -0.153 |             11 |              36 |      1.093 |      -1.417 |  0.015 |  60.505 |

### Thirds

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| DE VAL A          | SWE    |     286 |      15 |         0.538 |      0.144 |     -0.152 |           3 |            8 |   -4.54  |  0.008 |             13 |              10 |      0.677 |      -0.673 | -0.01  |  82.692 |
| GAFNER S          | SUI    |     264 |      14 |         0.53  |      0.139 |     -0.129 |           2 |            4 |   -2.65  |  0.013 |             10 |               9 |      0.369 |      -0.432 | -0.011 |  88.783 |
| KIM M             | KOR    |     244 |      13 |         0.516 |      0.148 |     -0.152 |           6 |            7 |   -3.369 |  0.003 |             10 |              13 |      0.478 |      -0.522 | -0.003 |  81.967 |
| DAVIE L           | SCO    |     110 |       6 |         0.509 |      0.143 |     -0.177 |           0 |            5 |   -3.064 | -0.014 |              3 |               7 |      0.271 |      -0.448 |  0     |  85.092 |
| ZARDINI LACEDELLI | ITA    |     222 |      12 |         0.509 |      0.157 |     -0.154 |           4 |            3 |   -2.683 |  0.004 |             13 |              12 |      0.482 |      -0.365 |  0.017 |  79.955 |
| YOSHIDA C         | JPN    |     172 |      10 |         0.5   |      0.13  |     -0.145 |           0 |            2 |   -2.638 | -0.008 |              4 |               6 |      0.28  |      -0.34  | -0.01  |  80.814 |
| O'HARA A          | USA    |     206 |      12 |         0.49  |      0.16  |     -0.177 |           5 |            7 |   -3.328 | -0.012 |             11 |              10 |      0.5   |      -0.498 |  0.021 |  77.549 |
| SWEETING V        | CAN    |     250 |      14 |         0.488 |      0.135 |     -0.114 |           2 |            2 |   -2.651 |  0.008 |              7 |               7 |      0.431 |      -0.364 | -0.003 |  83.434 |
| HALSE M           | DEN    |     260 |      12 |         0.481 |      0.138 |     -0.149 |           4 |            4 |   -3.092 | -0.011 |             15 |              18 |      0.562 |      -0.75  |  0.013 |  76.346 |
| WANG R            | CHN    |     222 |      12 |         0.477 |      0.123 |     -0.136 |           2 |            3 |   -2.781 | -0.012 |              7 |               8 |      0.358 |      -0.403 | -0     |  78.491 |
| POLAT O           | TUR    |     242 |      13 |         0.475 |      0.151 |     -0.133 |           1 |            4 |   -2.703 |  0.002 |             15 |              11 |      0.492 |      -0.445 |  0.018 |  79.029 |
| WATT L            | SCO    |     118 |       6 |         0.466 |      0.145 |     -0.152 |           1 |            2 |   -2.58  | -0.014 |              6 |               9 |      0.458 |      -0.454 |  0.012 |  76.059 |
| KOANA T           | JPN    |      96 |       5 |         0.458 |      0.167 |     -0.168 |           3 |            4 |   -3.35  | -0.015 |              6 |               5 |      0.335 |      -0.364 |  0.003 |  76.302 |
| OESTGAARD N       | NOR    |     214 |      11 |         0.444 |      0.145 |     -0.158 |           2 |            7 |   -3.736 | -0.023 |              9 |              17 |      0.686 |      -0.528 |  0.008 |  76.285 |
| WESTMAN S         | AUS    |     162 |      10 |         0.407 |      0.119 |     -0.174 |           1 |            6 |   -3.375 | -0.054 |              4 |              11 |      0.364 |      -0.504 |  0.021 |  75.154 |

### Seconds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| RIEDER F     | SUI    |     264 |      14 |         0.557 |      0.084 |     -0.098 |           0 |            2 |   -2.147 |  0.004 |              1 |               2 |      0.256 |      -0.325 | -0.007 |  89.504 |
| BIRCHARD S   | CAN    |     250 |      14 |         0.552 |      0.088 |     -0.072 |           0 |            0 |   -1.36  |  0.016 |              5 |               2 |      0.346 |      -0.221 | -0.003 |  88.1   |
| SU T         | CHN    |      88 |       5 |         0.545 |      0.08  |     -0.075 |           0 |            0 |   -1.152 |  0.01  |              2 |               0 |      0.243 |      -0.146 | -0.011 |  84.375 |
| LARSSON M    | SWE    |     284 |      15 |         0.528 |      0.093 |     -0.096 |           0 |            2 |   -2.72  |  0.004 |              2 |               5 |      0.244 |      -0.499 | -0.003 |  82.218 |
| SUZUKI Y     | JPN    |     268 |      15 |         0.489 |      0.083 |     -0.096 |           0 |            0 |   -2.032 | -0.009 |              3 |               3 |      0.264 |      -0.274 |  0.007 |  80.357 |
| KARAMAN I    | TUR    |     242 |      13 |         0.475 |      0.077 |     -0.099 |           0 |            0 |   -1.83  | -0.015 |              5 |               4 |      0.298 |      -0.326 |  0.008 |  73.347 |
| KIM S        | KOR    |     228 |      12 |         0.465 |      0.079 |     -0.091 |           0 |            1 |   -2.141 | -0.012 |              2 |               4 |      0.251 |      -0.282 | -0.001 |  82.346 |
| FORBREGD I   | NOR    |     232 |      12 |         0.444 |      0.08  |     -0.094 |           1 |            3 |   -2.69  | -0.016 |              6 |               5 |      0.562 |      -0.304 |  0.008 |  80.28  |
| MATHIS E     | ITA    |     222 |      12 |         0.441 |      0.072 |     -0.101 |           0 |            0 |   -1.865 | -0.025 |              1 |               0 |      0.223 |      -0.199 |  0.008 |  80.068 |
| DUFF H       | SCO    |     228 |      12 |         0.439 |      0.088 |     -0.09  |           1 |            0 |   -1.736 | -0.012 |              3 |               2 |      0.368 |      -0.246 |  0.006 |  79.496 |
| DONG Z       | CHN    |     146 |       9 |         0.418 |      0.075 |     -0.097 |           0 |            1 |   -1.904 | -0.025 |              0 |               5 |      0.15  |      -0.294 |  0.004 |  81.164 |
| SCHMIDT K    | DEN    |     188 |      10 |         0.41  |      0.069 |     -0.086 |           0 |            0 |   -1.888 | -0.023 |              1 |               4 |      0.214 |      -0.275 |  0.016 |  77.793 |
| MULLANEY S   | USA    |     206 |      12 |         0.359 |      0.09  |     -0.105 |           0 |            1 |   -2.069 | -0.035 |              6 |               2 |      0.416 |      -0.252 |  0.003 |  76.341 |
| TSOURLENES K | AUS    |     166 |      10 |         0.313 |      0.071 |     -0.125 |           0 |            2 |   -2.177 | -0.064 |              2 |               1 |      0.338 |      -0.25  |  0.005 |  60.693 |

### Leads

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| BURGESS K    | CAN    |     246 |      14 |         0.699 |      0.043 |     -0.048 |           0 |            0 |   -0.908 |  0.016 |              0 |               0 |      0.148 |      -0.12  |  0.002 |  94.207 |
| SEOL YEJ     | KOR    |      36 |       2 |         0.694 |      0.047 |     -0.059 |           0 |            0 |   -0.445 |  0.015 |              0 |               0 |      0.099 |      -0.061 | -0.015 |  87.5   |
| RYCHIGER S   | SUI    |     264 |      14 |         0.659 |      0.047 |     -0.048 |           0 |            0 |   -0.823 |  0.015 |              0 |               0 |      0.133 |      -0.136 |  0.004 |  91.858 |
| STENLUND L   | SWE    |     286 |      15 |         0.65  |      0.045 |     -0.044 |           0 |            0 |   -0.687 |  0.014 |              1 |               0 |      0.156 |      -0.153 |  0.006 |  90.702 |
| SEOL YEE     | KOR    |     224 |      12 |         0.594 |      0.041 |     -0.046 |           0 |            0 |   -0.732 |  0.006 |              0 |               0 |      0.1   |      -0.124 |  0     |  90.29  |
| SENGUL B     | TUR    |     242 |      13 |         0.583 |      0.044 |     -0.048 |           0 |            0 |   -0.76  |  0.006 |              0 |               1 |      0.157 |      -0.168 |  0.004 |  85.64  |
| BEAR M       | USA    |     206 |      12 |         0.568 |      0.043 |     -0.044 |           0 |            0 |   -0.703 |  0.005 |              0 |               0 |      0.104 |      -0.099 |  0     |  85.801 |
| MCMILLAN K   | SCO    |     228 |      12 |         0.561 |      0.041 |     -0.053 |           0 |            0 |   -0.888 | -0     |              1 |               0 |      0.166 |      -0.13  |  0.001 |  88.326 |
| JIANG J      | CHN    |     222 |      12 |         0.55  |      0.038 |     -0.045 |           0 |            0 |   -0.691 |  0.001 |              0 |               0 |      0.117 |      -0.103 |  0.003 |  90.271 |
| ARMSTRONG M  | AUS    |      82 |       6 |         0.549 |      0.049 |     -0.077 |           0 |            0 |   -0.765 | -0.008 |              0 |               0 |      0.055 |      -0.092 |  0.001 |  80.488 |
| YOSHIDA Y    | JPN    |     268 |      15 |         0.534 |      0.041 |     -0.042 |           0 |            0 |   -0.647 |  0.002 |              0 |               0 |      0.089 |      -0.089 |  0.004 |  85.168 |
| TITHERIDGE K | AUS    |     160 |      10 |         0.525 |      0.043 |     -0.139 |           0 |            4 |   -3.018 | -0.044 |              0 |               4 |      0.097 |      -0.346 |  0.018 |  75.781 |
| LO DESERTO M | ITA    |     222 |      12 |         0.518 |      0.044 |     -0.051 |           0 |            0 |   -0.851 | -0.002 |              0 |               0 |      0.106 |      -0.176 |  0.001 |  87.162 |
| LARSEN M     | DEN    |     206 |      10 |         0.51  |      0.042 |     -0.061 |           0 |            0 |   -1.236 | -0.008 |              0 |               0 |      0.13  |      -0.149 |  0.001 |  82.16  |
| MESLOE E     | NOR    |     232 |      12 |         0.487 |      0.052 |     -0.047 |           0 |            0 |   -0.739 |  0.001 |              0 |               0 |      0.132 |      -0.148 |  0.004 |  86.746 |

