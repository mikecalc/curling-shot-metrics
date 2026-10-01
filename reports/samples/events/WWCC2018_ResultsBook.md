# World Women's Curling Championship (WWCC2018_ResultsBook)

North Bay, ON, Canada, 2018; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| CAN    |      13 | 13-0     |  50   |   6.1 |  47.3 |      -3.1 |    -0.2 |      72.5 |
| SWE    |      13 | 10-3     |  26.9 |   2.6 |  18.3 |       6.7 |    -0.7 |      60.3 |
| KOR    |      13 | 8-5      |  11.5 |   2.6 |  -7.1 |      15.6 |     0.4 |      57   |
| CZE    |      11 | 6-5      |   4.5 |  -1   |  -0.1 |       3.9 |     1.8 |      47.3 |
| RUS    |      13 | 7-6      |   3.8 |  -0.9 |   9.5 |      -1   |    -3.9 |      62.3 |
| SCO    |      10 | 5-5      |   0   |  -4.5 | -13   |      19.3 |    -1.8 |      51.4 |
| SUI    |      11 | 5-6      |  -4.5 |  -1   |  -6.7 |       4.3 |    -1.1 |      45.1 |
| CHN    |      11 | 5-6      |  -4.5 |  -5.1 |  -3.2 |      -2   |     5.7 |      38.8 |
| USA    |      14 | 6-8      |  -7.1 |   0   |   6.9 |     -13.8 |    -0.2 |      48.5 |
| JPN    |      12 | 5-7      |  -8.3 |   3.7 |   7.2 |     -20.1 |     0.8 |      43.4 |
| GER    |      11 | 3-8      | -22.7 |  -1   |  -4.9 |     -15.3 |    -1.5 |      41.7 |
| DEN    |      12 | 3-9      | -25   |  -3.7 | -43.6 |      21.4 |     1   |      41.5 |
| ITA    |      12 | 2-10     | -33.3 |   0   | -20.9 |     -12.5 |     0   |      34   |

### Fourths

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| JONES J      | CAN    |     236 |      13 |         0.648 |      0.27  |     -0.274 |  0.079 |          19 |           14 |   -5.514 |             33 |              21 |      1.386 |      -0.752 |  0.008 |  79.487 |
| SINCLAIR J   | USA    |     265 |      14 |         0.596 |      0.218 |     -0.222 |  0.04  |          16 |           14 |   -4.603 |             34 |              20 |      0.999 |      -1.84  | -0.007 |  81.679 |
| HASSELBORG A | SWE    |     240 |      13 |         0.638 |      0.233 |     -0.299 |  0.04  |          18 |           15 |   -6.735 |             27 |              19 |      0.978 |      -1.065 | -0.004 |  84.574 |
| MOISEEVA V   | RUS    |     255 |      13 |         0.584 |      0.195 |     -0.243 |  0.013 |          13 |           17 |   -4.903 |             26 |              28 |      0.992 |      -1.737 | -0.007 |  80.357 |
| KUBESKOVA A  | CZE    |     193 |      10 |         0.585 |      0.22  |     -0.355 | -0.018 |          11 |           15 |   -8.569 |             20 |              25 |      1.022 |      -1.89  | -0.009 |  77.88  |
| KOANA T      | JPN    |     218 |      12 |         0.56  |      0.26  |     -0.39  | -0.027 |          20 |           27 |   -8.199 |             23 |              31 |      1.883 |      -1.072 |  0.003 |  73.38  |
| KIM E        | KOR    |     248 |      13 |         0.536 |      0.235 |     -0.342 | -0.033 |          14 |           24 |   -9.55  |             30 |              30 |      0.797 |      -1.873 | -0.01  |  76.633 |
| FELTSCHER B  | SUI    |     209 |      11 |         0.522 |      0.238 |     -0.346 | -0.041 |          12 |           27 |   -6.948 |             28 |              38 |      1.027 |      -1.252 |  0.012 |  71.481 |
| JENTSCH D    | GER    |     205 |      11 |         0.507 |      0.184 |     -0.275 | -0.042 |           8 |           18 |   -7.311 |             15 |              31 |      0.689 |      -1.176 |  0.003 |  75     |
| JIANG Y      | CHN    |     198 |      11 |         0.51  |      0.271 |     -0.379 | -0.048 |          13 |           22 |   -9.243 |             25 |              28 |      1.063 |      -1.444 |  0.002 |  70.581 |
| FLEMING H    | SCO    |     188 |      10 |         0.527 |      0.227 |     -0.391 | -0.065 |          10 |           25 |   -8.66  |             25 |              32 |      1.085 |      -1.546 | -0.01  |  72.838 |
| JENSEN A     | DEN    |     219 |      12 |         0.479 |      0.256 |     -0.375 | -0.073 |          10 |           28 |   -7.613 |             23 |              48 |      1.618 |      -1.898 | -0.021 |  68.548 |
| GASPARI D    | ITA    |     231 |      12 |         0.502 |      0.219 |     -0.407 | -0.093 |          11 |           36 |   -8.892 |             24 |              48 |      0.938 |      -1.375 | -0.015 |  70.306 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| LAWES K     | CAN    |     240 |      13 |         0.65  |      0.157 |     -0.129 |  0.057 |           7 |            3 |   -2.705 |             11 |               6 |      0.536 |      -0.376 | -0.006 |  85.417 |
| BAUDYSOVA A | CZE    |     218 |      11 |         0.628 |      0.121 |     -0.131 |  0.027 |           1 |            1 |   -2.446 |              9 |               7 |      0.541 |      -0.385 |  0.004 |  78.226 |
| PORTUNOVA J | RUS    |     262 |      13 |         0.565 |      0.123 |     -0.12  |  0.017 |           1 |            2 |   -2.932 |              9 |              10 |      0.47  |      -0.539 | -0.005 |  82.92  |
| WANG R      | CHN    |     198 |      11 |         0.52  |      0.127 |     -0.126 |  0.006 |           2 |            3 |   -2.758 |              5 |               5 |      0.448 |      -0.461 |  0.009 |  80.177 |
| CARLSON A   | USA    |     268 |      14 |         0.549 |      0.1   |     -0.111 |  0.005 |           1 |            1 |   -2.415 |              9 |               4 |      0.427 |      -0.381 | -0.006 |  81.343 |
| MCMANUS S   | SWE    |     242 |      13 |         0.558 |      0.112 |     -0.132 |  0.004 |           0 |            3 |   -2.735 |              7 |               7 |      0.392 |      -0.427 | -0.012 |  86.467 |
| KIM K       | KOR    |     228 |      12 |         0.548 |      0.113 |     -0.131 |  0.003 |           0 |            1 |   -2.325 |              8 |               7 |      0.344 |      -0.438 | -0.008 |  81.36  |
| KOTANI Y    | JPN    |     126 |       7 |         0.54  |      0.099 |     -0.118 | -0.001 |           0 |            1 |   -2.377 |              1 |               2 |      0.19  |      -0.334 | -0.002 |  81.349 |
| ONODERA K   | JPN    |     148 |       8 |         0.52  |      0.142 |     -0.159 | -0.002 |           3 |            3 |   -2.677 |              6 |               6 |      0.52  |      -0.402 |  0.002 |  79.223 |
| DODDS J     | SCO    |     190 |      10 |         0.489 |      0.13  |     -0.138 | -0.007 |           1 |            2 |   -2.453 |              9 |              11 |      0.401 |      -0.407 | -0.003 |  78.175 |
| ABBES E     | GER    |     209 |      11 |         0.493 |      0.116 |     -0.128 | -0.008 |           1 |            2 |   -2.591 |              8 |               9 |      0.401 |      -0.463 |  0.004 |  73.684 |
| SCHORI I    | SUI    |     212 |      11 |         0.552 |      0.106 |     -0.154 | -0.011 |           0 |            3 |   -2.607 |              4 |              13 |      0.33  |      -0.418 |  0.001 |  75.59  |
| ZAPPONE V   | ITA    |     232 |      12 |         0.5   |      0.09  |     -0.133 | -0.022 |           1 |            4 |   -2.917 |             10 |               9 |      0.561 |      -0.502 | -0.001 |  77.802 |
| GROENBECH C | DEN    |     220 |      12 |         0.473 |      0.091 |     -0.138 | -0.03  |           1 |            5 |   -3.028 |              3 |               9 |      0.341 |      -0.567 | -0.005 |  72.727 |

### Seconds

| player         | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:---------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| ARSENKINA G    | RUS    |     262 |      13 |         0.592 |      0.079 |     -0.069 |  0.018 |           0 |            0 |   -1.761 |              5 |               2 |      0.362 |      -0.272 | -0.009 |  88.697 |
| KNOCHENHAUER A | SWE    |     242 |      13 |         0.612 |      0.07  |     -0.062 |  0.018 |           0 |            0 |   -1.099 |              1 |               0 |      0.219 |      -0.167 | -0.01  |  89.773 |
| PERSINGER V    | USA    |     268 |      14 |         0.593 |      0.07  |     -0.067 |  0.014 |           0 |            0 |   -1.544 |              1 |               1 |      0.238 |      -0.217 | -0.01  |  86.007 |
| KAUFMANN F     | SUI    |     212 |      11 |         0.571 |      0.081 |     -0.088 |  0.008 |           0 |            1 |   -1.881 |              2 |               1 |      0.279 |      -0.333 | -0.002 |  81.368 |
| OFFICER J      | CAN    |     214 |      12 |         0.593 |      0.081 |     -0.104 |  0.006 |           1 |            2 |   -2.767 |              1 |               4 |      0.249 |      -0.404 | -0.009 |  83.685 |
| SPENCE A       | SCO    |     190 |      10 |         0.579 |      0.067 |     -0.08  |  0.005 |           0 |            0 |   -1.262 |              2 |               3 |      0.251 |      -0.256 | -0.008 |  77.116 |
| ISHIGAKI M     | JPN    |     178 |       9 |         0.506 |      0.08  |     -0.073 |  0.005 |           0 |            0 |   -1.131 |              0 |               1 |      0.171 |      -0.207 |  0.002 |  79.635 |
| KIM S          | KOR    |     250 |      13 |         0.516 |      0.087 |     -0.085 |  0.004 |           0 |            0 |   -1.549 |              2 |               2 |      0.27  |      -0.244 | -0.013 |  83.4   |
| CONSTANTINI S  | ITA    |     232 |      12 |         0.466 |      0.08  |     -0.071 | -0.001 |           0 |            1 |   -1.909 |              3 |               6 |      0.28  |      -0.394 | -0     |  78.233 |
| JIANG X        | CHN    |     198 |      11 |         0.505 |      0.076 |     -0.08  | -0.001 |           0 |            0 |   -1.547 |              5 |               4 |      0.301 |      -0.276 | -0     |  77.652 |
| PLISKOVA T     | CZE    |     218 |      11 |         0.477 |      0.069 |     -0.075 | -0.006 |           0 |            1 |   -1.917 |              2 |               4 |      0.266 |      -0.393 | -0.009 |  75.691 |
| JENTSCH A      | GER    |     210 |      11 |         0.5   |      0.075 |     -0.088 | -0.007 |           0 |            0 |   -1.747 |              0 |               5 |      0.216 |      -0.28  |  0.001 |  76.555 |
| JENSEN C       | DEN    |     220 |      12 |         0.473 |      0.094 |     -0.132 | -0.025 |           2 |            2 |   -2.455 |              4 |              16 |      0.389 |      -0.606 | -0.009 |  77.045 |

### Leads

| player         | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:---------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KIM C          | KOR    |      64 |       3 |         0.719 |      0.053 |     -0.053 |  0.023 |           0 |            0 |   -0.737 |              1 |               1 |      0.17  |      -0.129 |  0.003 |  84.677 |
| SCHOELL PL     | GER    |     172 |       9 |         0.628 |      0.045 |     -0.034 |  0.016 |           0 |            0 |   -0.662 |              0 |               0 |      0.124 |      -0.141 |  0.002 |  83.626 |
| MCEWEN D       | CAN    |     240 |      13 |         0.617 |      0.046 |     -0.034 |  0.015 |           0 |            0 |   -0.646 |              1 |               0 |      0.13  |      -0.094 |  0     |  86.146 |
| KOLCHEVSKAIA E | CZE    |     162 |       8 |         0.679 |      0.043 |     -0.046 |  0.015 |           0 |            0 |   -0.959 |              1 |               0 |      0.186 |      -0.157 | -0.001 |  84.259 |
| SVATONOVA K    | CZE    |      76 |       4 |         0.632 |      0.038 |     -0.03  |  0.013 |           0 |            0 |   -0.414 |              0 |               0 |      0.081 |      -0.076 |  0.002 |  85.526 |
| OLIVIERI C     | ITA    |      44 |       3 |         0.568 |      0.049 |     -0.035 |  0.013 |           0 |            0 |   -0.332 |              0 |               0 |      0.09  |      -0.042 | -0.006 |  82.955 |
| ROMEI A        | ITA    |     188 |      10 |         0.606 |      0.039 |     -0.029 |  0.012 |           0 |            0 |   -0.581 |              0 |               0 |      0.154 |      -0.088 | -0.004 |  75.798 |
| HOWALD C       | SUI    |     212 |      11 |         0.594 |      0.037 |     -0.026 |  0.012 |           0 |            0 |   -0.508 |              0 |               0 |      0.116 |      -0.101 |  0.002 |  83.608 |
| GUZIEVA J      | RUS    |     242 |      12 |         0.64  |      0.04  |     -0.038 |  0.012 |           0 |            0 |   -0.909 |              0 |               0 |      0.102 |      -0.128 |  0.003 |  87.021 |
| KIM Y          | KOR    |     208 |      11 |         0.615 |      0.038 |     -0.035 |  0.01  |           0 |            0 |   -0.59  |              1 |               0 |      0.16  |      -0.093 | -0.01  |  85.922 |
| WALKER M       | USA    |     268 |      14 |         0.631 |      0.034 |     -0.032 |  0.01  |           0 |            0 |   -0.702 |              0 |               0 |      0.102 |      -0.13  | -0.003 |  88.483 |
| MABERGS S      | SWE    |     238 |      13 |         0.609 |      0.033 |     -0.03  |  0.009 |           0 |            0 |   -0.767 |              0 |               0 |      0.097 |      -0.096 | -0.001 |  90.665 |
| KNUDSEN L      | DEN    |     220 |      12 |         0.532 |      0.045 |     -0.035 |  0.007 |           0 |            0 |   -0.69  |              0 |               0 |      0.109 |      -0.126 | -0     |  80.903 |
| OBERMANN J     | GER    |      38 |       2 |         0.658 |      0.033 |     -0.045 |  0.007 |           0 |            0 |   -0.392 |              0 |               0 |      0.095 |      -0.049 |  0.002 |  71.622 |
| KOTANI A       | JPN    |     226 |      12 |         0.602 |      0.037 |     -0.04  |  0.006 |           0 |            0 |   -0.707 |              0 |               0 |      0.11  |      -0.102 | -0.005 |  82.222 |
| YAN H          | CHN    |     198 |      11 |         0.5   |      0.034 |     -0.033 |  0     |           0 |            0 |   -0.578 |              0 |               0 |      0.107 |      -0.098 | -0.003 |  80.964 |
| WRIGHT V       | SCO    |     190 |      10 |         0.468 |      0.034 |     -0.031 | -0.001 |           0 |            0 |   -0.502 |              0 |               0 |      0.08  |      -0.14  | -0.001 |  79.435 |

