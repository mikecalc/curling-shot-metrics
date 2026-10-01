# World Women's Curling Championship (WWCC2025_ResultsBook)

Uijeongbu, Korea, 2025; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| CAN    |      15 | 13-2     |  36.7 |   3.8 |  17.4 |      13.8 |     1.7 |      69.6 |
| SUI    |      14 | 12-2     |  35.7 |   3.3 |  22   |       8.6 |     1.8 |      64.2 |
| KOR    |      14 | 10-4     |  21.4 |   6.5 |  27.6 |     -11.2 |    -1.6 |      66   |
| SWE    |      13 | 9-4      |  19.2 |   2.6 |  14.6 |       4.1 |    -2.1 |      63.7 |
| CHN    |      15 | 9-6      |  10   |  -0.8 |   3.9 |       7   |    -0.1 |      52.3 |
| SCO    |      13 | 7-6      |   3.8 |  -6.1 |  11.2 |      -1.2 |     0   |      49   |
| NOR    |      12 | 5-7      |  -8.3 |   1.9 |  -7.6 |      -0.6 |    -2   |      44.4 |
| DEN    |      12 | 5-7      |  -8.3 |  -3.8 |  -4.2 |       0.6 |    -0.9 |      40.8 |
| JPN    |      12 | 4-8      | -16.7 |   0   | -10.4 |      -8.2 |     1.9 |      48.6 |
| ITA    |      12 | 4-8      | -16.7 |   0   | -15.9 |       1.1 |    -1.8 |      45.1 |
| USA    |      12 | 3-9      | -25   |  -3.8 |  -3.6 |     -18.5 |     0.9 |      41.7 |
| TUR    |      12 | 3-9      | -25   |   0   | -16.2 |     -11.8 |     2.9 |      36.3 |
| LTU    |      12 | 0-12     | -50   |  -5.7 | -54.4 |      11.1 |    -1   |      16.8 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| DEN    |      841 |   0.025 |    -0.012 |          0.641 |                2.428 |                   2.114 |
| KOR    |     1109 |   0.014 |     0.017 |          0.579 |                2.058 |                   2.036 |
| ITA    |      869 |   0.014 |    -0.022 |          0.633 |                2.349 |                   2.074 |
| JPN    |      878 |   0.006 |    -0.006 |          0.637 |                2.053 |                   1.864 |
| CHN    |     1110 |   0.005 |    -0.001 |          0.615 |                1.732 |                   2.171 |
| TUR    |      837 |   0.001 |    -0.021 |          0.616 |                1.918 |                   2.013 |
| NOR    |      892 |  -0.006 |     0.002 |          0.589 |                1.894 |                   1.947 |
| SCO    |      960 |  -0.006 |     0.003 |          0.594 |                1.834 |                   2.077 |
| CAN    |     1077 |  -0.007 |     0.022 |          0.576 |                2.156 |                   2.104 |
| USA    |      911 |  -0.009 |     0.005 |          0.592 |                2.13  |                   2.178 |
| SUI    |     1065 |  -0.011 |     0.035 |          0.547 |                2.151 |                   1.799 |
| LTU    |      720 |  -0.011 |    -0.043 |          0.622 |                1.994 |                   2.234 |
| SWE    |      992 |  -0.015 |    -0.004 |          0.592 |                2.083 |                   2.133 |

### Fourths

| player         | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:---------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HOMAN R        | CAN    |     269 |      15 |         0.632 |      0.303 |     -0.232 |          28 |           12 |   -5.004 |  0.106 |             37 |              17 |      1.326 |      -1.115 | -0.01  |  87.689 |
| GIM E          | KOR    |     279 |      14 |         0.62  |      0.259 |     -0.277 |          29 |           17 |   -6.507 |  0.055 |             48 |              23 |      1.182 |      -1.086 |  0.021 |  85.236 |
| HASSELBORG A   | SWE    |     229 |      12 |         0.598 |      0.275 |     -0.237 |          22 |           11 |   -6.28  |  0.069 |             37 |              18 |      1.017 |      -0.912 |  0.009 |  87.115 |
| YOSHIMURA S    | JPN    |     220 |      12 |         0.586 |      0.279 |     -0.384 |          21 |           23 |  -10.009 |  0.005 |             24 |              24 |      0.77  |      -1.283 |  0.009 |  78.311 |
| DUPONT M       | DEN    |     212 |      12 |         0.58  |      0.25  |     -0.331 |          11 |           21 |   -7.403 |  0.006 |             25 |              27 |      1.007 |      -0.936 |  0.017 |  80.687 |
| PAETZ A        | SUI    |     270 |      14 |         0.567 |      0.224 |     -0.242 |          20 |           19 |   -6.227 |  0.022 |             32 |              28 |      1.807 |      -1.176 |  0.015 |  85.502 |
| WANG R         | CHN    |     277 |      15 |         0.552 |      0.235 |     -0.205 |          19 |           12 |   -5.326 |  0.038 |             24 |              19 |      2.208 |      -1.061 |  0.008 |  84.42  |
| CONSTANTINI S  | ITA    |     216 |      12 |         0.532 |      0.277 |     -0.3   |          21 |           19 |   -7.481 |  0.007 |             25 |              21 |      0.843 |      -1.513 |  0.027 |  78.037 |
| MORRISON R     | SCO    |     243 |      13 |         0.523 |      0.282 |     -0.247 |          17 |           18 |   -6.508 |  0.03  |             40 |              25 |      1.454 |      -0.946 | -0     |  83.854 |
| PETERSON TAB   | USA    |     228 |      12 |         0.504 |      0.299 |     -0.265 |          19 |           22 |   -5.296 |  0.019 |             28 |              28 |      1.099 |      -1.038 |  0.004 |  77.987 |
| YILDIZ D       | TUR    |     212 |      12 |         0.491 |      0.273 |     -0.303 |          16 |           20 |   -7.365 | -0.021 |             24 |              25 |      0.868 |      -0.927 |  0.012 |  75.478 |
| SKASLIEN K     | NOR    |     227 |      12 |         0.48  |      0.251 |     -0.301 |          11 |           20 |   -8.626 | -0.036 |             28 |              34 |      1.562 |      -1.474 |  0.013 |  75.551 |
| PAULAUSKAITE V | LTU    |     182 |      12 |         0.368 |      0.309 |     -0.376 |          15 |           30 |   -8.788 | -0.124 |             12 |              25 |      0.935 |      -0.758 |  0.049 |  65     |

### Thirds

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| FLEURY T          | CAN    |     272 |      15 |         0.559 |      0.162 |     -0.109 |           6 |            2 |   -2.277 |  0.043 |             20 |               6 |      0.406 |      -0.305 | -0.015 |  89.062 |
| MCMANUS S         | SWE    |     249 |      13 |         0.522 |      0.139 |     -0.139 |           1 |            5 |   -3.676 |  0.006 |             11 |              10 |      0.333 |      -0.471 | -0.011 |  87.249 |
| HALSE M           | DEN    |     212 |      12 |         0.519 |      0.135 |     -0.14  |           4 |            3 |   -3.229 |  0.002 |             10 |               8 |      0.463 |      -0.446 |  0.009 |  81.368 |
| ONODERA K         | JPN    |     222 |      12 |         0.518 |      0.14  |     -0.118 |           4 |            2 |   -2.731 |  0.015 |             11 |               5 |      0.472 |      -0.386 | -0.004 |  84.234 |
| THIESSE C         | USA    |     230 |      12 |         0.504 |      0.116 |     -0.125 |           0 |            6 |   -3.093 | -0.003 |             10 |              10 |      0.404 |      -0.432 |  0.012 |  81.196 |
| KIM M             | KOR    |     282 |      14 |         0.493 |      0.145 |     -0.135 |           5 |            3 |   -2.631 |  0.003 |             15 |              13 |      0.569 |      -0.453 | -0.002 |  85.195 |
| TIRINZONI S       | SUI    |     270 |      14 |         0.493 |      0.146 |     -0.131 |           4 |            4 |   -2.888 |  0.005 |             15 |              19 |      0.607 |      -0.525 |  0.007 |  86.481 |
| DODDS J           | SCO    |     244 |      13 |         0.492 |      0.136 |     -0.13  |           4 |            4 |   -3.383 |  0.001 |             11 |              11 |      0.416 |      -0.551 | -0     |  84.734 |
| POLAT O           | TUR    |     212 |      12 |         0.481 |      0.138 |     -0.123 |           4 |            2 |   -2.325 |  0.002 |             10 |               7 |      0.488 |      -0.319 |  0.01  |  81.132 |
| ROERVIK M         | NOR    |     228 |      12 |         0.474 |      0.13  |     -0.126 |           3 |            2 |   -2.598 | -0.005 |              6 |              10 |      0.48  |      -0.45  | -0.001 |  84.759 |
| ZARDINI LACEDELLI | ITA    |     220 |      12 |         0.464 |      0.167 |     -0.139 |           3 |            2 |   -3.267 |  0.003 |             10 |               9 |      0.444 |      -0.533 | -0.001 |  80     |
| HAN Y             | CHN    |     284 |      15 |         0.43  |      0.126 |     -0.11  |           4 |            1 |   -2.548 | -0.009 |              6 |               4 |      0.378 |      -0.325 |  0     |  85.211 |
| DVOJEGLAZOVA O    | LTU    |     182 |      12 |         0.302 |      0.168 |     -0.194 |           4 |            9 |   -3.412 | -0.084 |              6 |              16 |      0.346 |      -0.474 |  0.02  |  62.017 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KARAMAN I        | TUR    |      42 |       3 |         0.667 |      0.064 |     -0.052 |           0 |            0 |   -0.522 |  0.026 |              0 |               0 |      0.052 |      -0.059 | -0.012 |  77.976 |
| KNOCHENHAUER A   | SWE    |     250 |      13 |         0.52  |      0.093 |     -0.085 |           2 |            0 |   -1.926 |  0.008 |              2 |               4 |      0.337 |      -0.321 | -0.006 |  85.2   |
| MISKEW E         | CAN    |     272 |      15 |         0.5   |      0.083 |     -0.092 |           0 |            0 |   -1.744 | -0.005 |              2 |               1 |      0.27  |      -0.246 | -0.011 |  87.315 |
| KIM S            | KOR    |     248 |      12 |         0.492 |      0.093 |     -0.082 |           0 |            0 |   -1.853 |  0.004 |              4 |               4 |      0.336 |      -0.308 | -0.005 |  84.778 |
| SINCLAIR S       | SCO    |     230 |      12 |         0.483 |      0.076 |     -0.072 |           1 |            0 |   -1.775 | -0.001 |              2 |               2 |      0.276 |      -0.237 | -0.003 |  87.283 |
| KOTANI Y         | JPN    |     202 |      11 |         0.48  |      0.079 |     -0.076 |           0 |            0 |   -1.471 | -0.001 |              2 |               1 |      0.259 |      -0.218 | -0.007 |  85.272 |
| MATHIS E         | ITA    |     220 |      12 |         0.477 |      0.075 |     -0.079 |           0 |            0 |   -1.285 | -0.005 |              2 |               2 |      0.259 |      -0.226 | -0.001 |  84.432 |
| HASLEV NORDBYE M | NOR    |     208 |      11 |         0.457 |      0.077 |     -0.09  |           0 |            1 |   -1.755 | -0.014 |              2 |               3 |      0.302 |      -0.266 |  0.006 |  84.951 |
| DONG Z           | CHN    |     272 |      15 |         0.452 |      0.082 |     -0.074 |           1 |            0 |   -1.626 | -0.003 |              3 |               2 |      0.264 |      -0.231 | -0.005 |  85.662 |
| PETERSON TAR     | USA    |     194 |      10 |         0.418 |      0.094 |     -0.111 |           0 |            1 |   -2.331 | -0.025 |              5 |               6 |      0.304 |      -0.425 |  0.001 |  78.737 |
| HOLTERMANN J     | DEN    |     144 |       8 |         0.417 |      0.098 |     -0.084 |           1 |            0 |   -1.491 | -0.008 |              2 |               1 |      0.257 |      -0.232 |  0.003 |  81.076 |
| PERSINGER V      | USA    |      36 |       2 |         0.417 |      0.084 |     -0.111 |           0 |            0 |   -1.093 | -0.03  |              0 |               1 |      0.077 |      -0.147 |  0.02  |  75     |
| HOWALD C         | SUI    |     262 |      14 |         0.397 |      0.083 |     -0.086 |           0 |            1 |   -1.972 | -0.019 |              4 |               3 |      0.376 |      -0.326 | -0.004 |  86.442 |
| KIUDYTE M        | LTU    |     182 |      12 |         0.319 |      0.08  |     -0.119 |           1 |            0 |   -1.879 | -0.056 |              0 |               1 |      0.125 |      -0.246 |  0.015 |  67.445 |
| CALIKUSU IS      | TUR    |     170 |      10 |         0.318 |      0.081 |     -0.099 |           0 |            1 |   -2.043 | -0.042 |              0 |               2 |      0.16  |      -0.293 |  0.006 |  70.882 |

### Leads

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HELDIN J         | SWE    |      36 |       2 |         0.556 |      0.031 |     -0.053 |           0 |            0 |   -0.529 | -0.007 |              0 |               0 |      0.053 |      -0.066 |  0.003 |  81.25  |
| WILKES S         | CAN    |     272 |      15 |         0.555 |      0.04  |     -0.037 |           0 |            0 |   -0.803 |  0.006 |              1 |               0 |      0.139 |      -0.151 | -0     |  92.159 |
| MABERGS S        | SWE    |     234 |      12 |         0.538 |      0.029 |     -0.044 |           0 |            0 |   -1.083 | -0.004 |              0 |               0 |      0.127 |      -0.184 |  0     |  90.302 |
| OHMIYA A         | JPN    |     222 |      12 |         0.536 |      0.033 |     -0.039 |           0 |            0 |   -0.652 | -0     |              0 |               0 |      0.107 |      -0.139 |  0     |  91.667 |
| ANDERSON-HEIDE T | USA    |     230 |      12 |         0.513 |      0.029 |     -0.05  |           0 |            0 |   -1.011 | -0.009 |              0 |               0 |      0.107 |      -0.137 | -0.001 |  86.63  |
| DUPONT D         | DEN    |     196 |      11 |         0.505 |      0.043 |     -0.061 |           0 |            0 |   -1.038 | -0.008 |              1 |               1 |      0.154 |      -0.19  |  0.002 |  87.436 |
| LARSEN M         | DEN    |      84 |       5 |         0.5   |      0.032 |     -0.045 |           0 |            0 |   -0.596 | -0.006 |              0 |               0 |      0.067 |      -0.092 |  0.004 |  80.655 |
| SENGUL B         | TUR    |     212 |      12 |         0.495 |      0.035 |     -0.047 |           0 |            0 |   -0.719 | -0.007 |              0 |               0 |      0.108 |      -0.115 |  0.002 |  85.167 |
| ROMEI A          | ITA    |     206 |      11 |         0.481 |      0.032 |     -0.051 |           0 |            0 |   -0.807 | -0.011 |              0 |               0 |      0.114 |      -0.13  | -0.001 |  84.345 |
| SEOL Y           | KOR    |     316 |      14 |         0.472 |      0.041 |     -0.046 |           0 |            0 |   -1.166 | -0.005 |              1 |               1 |      0.167 |      -0.203 |  0.001 |  87.222 |
| JACKSON S        | SCO    |     244 |      13 |         0.467 |      0.03  |     -0.043 |           0 |            0 |   -0.719 | -0.009 |              0 |               0 |      0.118 |      -0.132 |  0.005 |  89.463 |
| BLAZIENE R       | LTU    |     182 |      12 |         0.462 |      0.028 |     -0.06  |           0 |            0 |   -1.091 | -0.02  |              0 |               0 |      0.062 |      -0.131 |  0.003 |  72.527 |
| KJAERLAND E      | NOR    |     170 |       9 |         0.441 |      0.027 |     -0.043 |           0 |            0 |   -0.834 | -0.012 |              0 |               0 |      0.113 |      -0.152 | -0.002 |  89.118 |
| FORBREGD I       | NOR    |      78 |       4 |         0.423 |      0.037 |     -0.06  |           0 |            0 |   -0.897 | -0.019 |              0 |               0 |      0.104 |      -0.135 |  0     |  85.256 |
| WITSCHONKE S     | SUI    |     258 |      14 |         0.407 |      0.032 |     -0.04  |           0 |            0 |   -0.744 | -0.011 |              0 |               0 |      0.088 |      -0.133 |  0.004 |  88.281 |
| JIANG J          | CHN    |     284 |      15 |         0.387 |      0.032 |     -0.038 |           0 |            0 |   -0.629 | -0.011 |              0 |               0 |      0.083 |      -0.099 |  0.006 |  92.143 |

