# World Women's Curling Championship (WWCC2025_ResultsBook)

Uijeongbu, Korea, 2025; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The player tables show the spread of each player's shots, not just their average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more percentage points of win probability, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

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

### Fourths

| player         | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:---------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HOMAN R        | CAN    |     269 |      15 |         0.632 |      0.303 |     -0.232 |  0.106 |          28 |           12 |   -5.004 |             37 |              17 |      1.326 |      -1.115 | -0.01  |  87.689 |
| HASSELBORG A   | SWE    |     229 |      12 |         0.598 |      0.275 |     -0.237 |  0.069 |          22 |           11 |   -6.28  |             37 |              18 |      1.017 |      -0.912 |  0.009 |  87.115 |
| GIM E          | KOR    |     279 |      14 |         0.62  |      0.259 |     -0.277 |  0.055 |          29 |           17 |   -6.507 |             48 |              23 |      1.182 |      -1.086 |  0.021 |  85.236 |
| WANG R         | CHN    |     277 |      15 |         0.552 |      0.235 |     -0.205 |  0.038 |          19 |           12 |   -5.326 |             24 |              19 |      2.208 |      -1.061 |  0.008 |  84.42  |
| MORRISON R     | SCO    |     243 |      13 |         0.523 |      0.282 |     -0.247 |  0.03  |          17 |           18 |   -6.508 |             40 |              25 |      1.454 |      -0.946 | -0     |  83.854 |
| PAETZ A        | SUI    |     270 |      14 |         0.567 |      0.224 |     -0.242 |  0.022 |          20 |           19 |   -6.227 |             32 |              28 |      1.807 |      -1.176 |  0.015 |  85.502 |
| PETERSON TAB   | USA    |     228 |      12 |         0.504 |      0.299 |     -0.265 |  0.019 |          19 |           22 |   -5.296 |             28 |              28 |      1.099 |      -1.038 |  0.004 |  77.987 |
| CONSTANTINI S  | ITA    |     216 |      12 |         0.532 |      0.277 |     -0.3   |  0.007 |          21 |           19 |   -7.481 |             25 |              21 |      0.843 |      -1.513 |  0.027 |  78.037 |
| DUPONT M       | DEN    |     212 |      12 |         0.58  |      0.25  |     -0.331 |  0.006 |          11 |           21 |   -7.403 |             25 |              27 |      1.007 |      -0.936 |  0.017 |  80.687 |
| YOSHIMURA S    | JPN    |     220 |      12 |         0.586 |      0.279 |     -0.384 |  0.005 |          21 |           23 |  -10.009 |             24 |              24 |      0.77  |      -1.283 |  0.009 |  78.311 |
| YILDIZ D       | TUR    |     212 |      12 |         0.491 |      0.273 |     -0.303 | -0.021 |          16 |           20 |   -7.365 |             24 |              25 |      0.868 |      -0.927 |  0.012 |  75.478 |
| SKASLIEN K     | NOR    |     227 |      12 |         0.48  |      0.251 |     -0.301 | -0.036 |          11 |           20 |   -8.626 |             28 |              34 |      1.562 |      -1.474 |  0.013 |  75.551 |
| PAULAUSKAITE V | LTU    |     182 |      12 |         0.368 |      0.309 |     -0.376 | -0.124 |          15 |           30 |   -8.788 |             12 |              25 |      0.935 |      -0.758 |  0.049 |  65     |

### Thirds

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| FLEURY T          | CAN    |     272 |      15 |         0.559 |      0.162 |     -0.109 |  0.043 |           6 |            2 |   -2.277 |             20 |               6 |      0.406 |      -0.305 | -0.015 |  89.062 |
| ONODERA K         | JPN    |     222 |      12 |         0.518 |      0.14  |     -0.118 |  0.015 |           4 |            2 |   -2.731 |             11 |               5 |      0.472 |      -0.386 | -0.004 |  84.234 |
| MCMANUS S         | SWE    |     249 |      13 |         0.522 |      0.139 |     -0.139 |  0.006 |           1 |            5 |   -3.676 |             11 |              10 |      0.333 |      -0.471 | -0.011 |  87.249 |
| TIRINZONI S       | SUI    |     270 |      14 |         0.493 |      0.146 |     -0.131 |  0.005 |           4 |            4 |   -2.888 |             15 |              19 |      0.607 |      -0.525 |  0.007 |  86.481 |
| KIM M             | KOR    |     282 |      14 |         0.493 |      0.145 |     -0.135 |  0.003 |           5 |            3 |   -2.631 |             15 |              13 |      0.569 |      -0.453 | -0.002 |  85.195 |
| ZARDINI LACEDELLI | ITA    |     220 |      12 |         0.464 |      0.167 |     -0.139 |  0.003 |           3 |            2 |   -3.267 |             10 |               9 |      0.444 |      -0.533 | -0.001 |  80     |
| POLAT O           | TUR    |     212 |      12 |         0.481 |      0.138 |     -0.123 |  0.002 |           4 |            2 |   -2.325 |             10 |               7 |      0.488 |      -0.319 |  0.01  |  81.132 |
| HALSE M           | DEN    |     212 |      12 |         0.519 |      0.135 |     -0.14  |  0.002 |           4 |            3 |   -3.229 |             10 |               8 |      0.463 |      -0.446 |  0.009 |  81.368 |
| DODDS J           | SCO    |     244 |      13 |         0.492 |      0.136 |     -0.13  |  0.001 |           4 |            4 |   -3.383 |             11 |              11 |      0.416 |      -0.551 | -0     |  84.734 |
| THIESSE C         | USA    |     230 |      12 |         0.504 |      0.116 |     -0.125 | -0.003 |           0 |            6 |   -3.093 |             10 |              10 |      0.404 |      -0.432 |  0.012 |  81.196 |
| ROERVIK M         | NOR    |     228 |      12 |         0.474 |      0.13  |     -0.126 | -0.005 |           3 |            2 |   -2.598 |              6 |              10 |      0.48  |      -0.45  | -0.001 |  84.759 |
| HAN Y             | CHN    |     284 |      15 |         0.43  |      0.126 |     -0.11  | -0.009 |           4 |            1 |   -2.548 |              6 |               4 |      0.378 |      -0.325 |  0     |  85.211 |
| DVOJEGLAZOVA O    | LTU    |     182 |      12 |         0.302 |      0.168 |     -0.194 | -0.084 |           4 |            9 |   -3.412 |              6 |              16 |      0.346 |      -0.474 |  0.02  |  62.017 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KARAMAN I        | TUR    |      42 |       3 |         0.667 |      0.064 |     -0.052 |  0.026 |           0 |            0 |   -0.522 |              0 |               0 |      0.052 |      -0.059 | -0.012 |  77.976 |
| KNOCHENHAUER A   | SWE    |     250 |      13 |         0.52  |      0.093 |     -0.085 |  0.008 |           2 |            0 |   -1.926 |              2 |               4 |      0.337 |      -0.321 | -0.006 |  85.2   |
| KIM S            | KOR    |     248 |      12 |         0.492 |      0.093 |     -0.082 |  0.004 |           0 |            0 |   -1.853 |              4 |               4 |      0.336 |      -0.308 | -0.005 |  84.778 |
| SINCLAIR S       | SCO    |     230 |      12 |         0.483 |      0.076 |     -0.072 | -0.001 |           1 |            0 |   -1.775 |              2 |               2 |      0.276 |      -0.237 | -0.003 |  87.283 |
| KOTANI Y         | JPN    |     202 |      11 |         0.48  |      0.079 |     -0.076 | -0.001 |           0 |            0 |   -1.471 |              2 |               1 |      0.259 |      -0.218 | -0.007 |  85.272 |
| DONG Z           | CHN    |     272 |      15 |         0.452 |      0.082 |     -0.074 | -0.003 |           1 |            0 |   -1.626 |              3 |               2 |      0.264 |      -0.231 | -0.005 |  85.662 |
| MISKEW E         | CAN    |     272 |      15 |         0.5   |      0.083 |     -0.092 | -0.005 |           0 |            0 |   -1.744 |              2 |               1 |      0.27  |      -0.246 | -0.011 |  87.315 |
| MATHIS E         | ITA    |     220 |      12 |         0.477 |      0.075 |     -0.079 | -0.005 |           0 |            0 |   -1.285 |              2 |               2 |      0.259 |      -0.226 | -0.001 |  84.432 |
| HOLTERMANN J     | DEN    |     144 |       8 |         0.417 |      0.098 |     -0.084 | -0.008 |           1 |            0 |   -1.491 |              2 |               1 |      0.257 |      -0.232 |  0.003 |  81.076 |
| HASLEV NORDBYE M | NOR    |     208 |      11 |         0.457 |      0.077 |     -0.09  | -0.014 |           0 |            1 |   -1.755 |              2 |               3 |      0.302 |      -0.266 |  0.006 |  84.951 |
| HOWALD C         | SUI    |     262 |      14 |         0.397 |      0.083 |     -0.086 | -0.019 |           0 |            1 |   -1.972 |              4 |               3 |      0.376 |      -0.326 | -0.004 |  86.442 |
| PETERSON TAR     | USA    |     194 |      10 |         0.418 |      0.094 |     -0.111 | -0.025 |           0 |            1 |   -2.331 |              5 |               6 |      0.304 |      -0.425 |  0.001 |  78.737 |
| PERSINGER V      | USA    |      36 |       2 |         0.417 |      0.084 |     -0.111 | -0.03  |           0 |            0 |   -1.093 |              0 |               1 |      0.077 |      -0.147 |  0.02  |  75     |
| CALIKUSU IS      | TUR    |     170 |      10 |         0.318 |      0.081 |     -0.099 | -0.042 |           0 |            1 |   -2.043 |              0 |               2 |      0.16  |      -0.293 |  0.006 |  70.882 |
| KIUDYTE M        | LTU    |     182 |      12 |         0.319 |      0.08  |     -0.119 | -0.056 |           1 |            0 |   -1.879 |              0 |               1 |      0.125 |      -0.246 |  0.015 |  67.445 |

### Leads

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WILKES S         | CAN    |     272 |      15 |         0.555 |      0.04  |     -0.037 |  0.006 |           0 |            0 |   -0.803 |              1 |               0 |      0.139 |      -0.151 | -0     |  92.159 |
| OHMIYA A         | JPN    |     222 |      12 |         0.536 |      0.033 |     -0.039 | -0     |           0 |            0 |   -0.652 |              0 |               0 |      0.107 |      -0.139 |  0     |  91.667 |
| MABERGS S        | SWE    |     234 |      12 |         0.538 |      0.029 |     -0.044 | -0.004 |           0 |            0 |   -1.083 |              0 |               0 |      0.127 |      -0.184 |  0     |  90.302 |
| SEOL Y           | KOR    |     316 |      14 |         0.472 |      0.041 |     -0.046 | -0.005 |           0 |            0 |   -1.166 |              1 |               1 |      0.167 |      -0.203 |  0.001 |  87.222 |
| LARSEN M         | DEN    |      84 |       5 |         0.5   |      0.032 |     -0.045 | -0.006 |           0 |            0 |   -0.596 |              0 |               0 |      0.067 |      -0.092 |  0.004 |  80.655 |
| SENGUL B         | TUR    |     212 |      12 |         0.495 |      0.035 |     -0.047 | -0.007 |           0 |            0 |   -0.719 |              0 |               0 |      0.108 |      -0.115 |  0.002 |  85.167 |
| HELDIN J         | SWE    |      36 |       2 |         0.556 |      0.031 |     -0.053 | -0.007 |           0 |            0 |   -0.529 |              0 |               0 |      0.053 |      -0.066 |  0.003 |  81.25  |
| DUPONT D         | DEN    |     196 |      11 |         0.505 |      0.043 |     -0.061 | -0.008 |           0 |            0 |   -1.038 |              1 |               1 |      0.154 |      -0.19  |  0.002 |  87.436 |
| JACKSON S        | SCO    |     244 |      13 |         0.467 |      0.03  |     -0.043 | -0.009 |           0 |            0 |   -0.719 |              0 |               0 |      0.118 |      -0.132 |  0.005 |  89.463 |
| ANDERSON-HEIDE T | USA    |     230 |      12 |         0.513 |      0.029 |     -0.05  | -0.009 |           0 |            0 |   -1.011 |              0 |               0 |      0.107 |      -0.137 | -0.001 |  86.63  |
| WITSCHONKE S     | SUI    |     258 |      14 |         0.407 |      0.032 |     -0.04  | -0.011 |           0 |            0 |   -0.744 |              0 |               0 |      0.088 |      -0.133 |  0.004 |  88.281 |
| ROMEI A          | ITA    |     206 |      11 |         0.481 |      0.032 |     -0.051 | -0.011 |           0 |            0 |   -0.807 |              0 |               0 |      0.114 |      -0.13  | -0.001 |  84.345 |
| JIANG J          | CHN    |     284 |      15 |         0.387 |      0.032 |     -0.038 | -0.011 |           0 |            0 |   -0.629 |              0 |               0 |      0.083 |      -0.099 |  0.006 |  92.143 |
| KJAERLAND E      | NOR    |     170 |       9 |         0.441 |      0.027 |     -0.043 | -0.012 |           0 |            0 |   -0.834 |              0 |               0 |      0.113 |      -0.152 | -0.002 |  89.118 |
| FORBREGD I       | NOR    |      78 |       4 |         0.423 |      0.037 |     -0.06  | -0.019 |           0 |            0 |   -0.897 |              0 |               0 |      0.104 |      -0.135 |  0     |  85.256 |
| BLAZIENE R       | LTU    |     182 |      12 |         0.462 |      0.028 |     -0.06  | -0.02  |           0 |            0 |   -1.091 |              0 |               0 |      0.062 |      -0.131 |  0.003 |  72.527 |

