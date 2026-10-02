# World Men's Curling Championship (WMCC2025_ResultsBook)

Moose Jaw, SK, Canada, 2025; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The player tables show the spread of each player's shots, not just their average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more percentage points of win probability, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| CAN    |      14 | 12-2     |  35.7 |   3.5 |  21.7 |      11.4 |    -0.8 |      74.5 |
| SCO    |      15 | 11-4     |  23.3 |   0.8 |  26.1 |      -3.3 |    -0.3 |      56.5 |
| SUI    |      14 | 10-4     |  21.4 |   3.5 |  14.6 |       3.7 |    -0.3 |      66   |
| SWE    |      13 | 8-5      |  11.5 |   6.5 |   8.7 |      -4.1 |     0.4 |      63.1 |
| CHN    |      15 | 9-6      |  10   |  -0.8 |   1   |       6.2 |     3.6 |      49.2 |
| NOR    |      13 | 7-6      |   3.8 |  -4.7 |   1.6 |       4.2 |     2.7 |      51.1 |
| CZE    |      12 | 6-6      |   0   |  -4   |   0.7 |       1.6 |     1.7 |      49.6 |
| GER    |      12 | 5-7      |  -8.3 |   4   |  -5.6 |      -2.4 |    -4.4 |      49.9 |
| ITA    |      12 | 5-7      |  -8.3 |  -6.1 |   3.7 |      -5.2 |    -0.8 |      47.4 |
| JPN    |      12 | 5-7      |  -8.3 |   8.1 | -11.5 |      -5.5 |     0.7 |      44.4 |
| USA    |      12 | 4-8      | -16.7 |   4   |  -7.3 |     -10.3 |    -3   |      47.8 |
| AUT    |      12 | 1-11     | -41.7 |  -6.1 | -32.9 |      -2.2 |    -0.5 |      23.6 |
| KOR    |      12 | 1-11     | -41.7 | -10.1 | -34.5 |       2.8 |     0.1 |      17.4 |

### Fourths

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| JACOBS B           | CAN    |     246 |      14 |         0.634 |      0.266 |     -0.213 |  0.091 |          24 |           12 |   -5.798 |             26 |               9 |      1.094 |      -0.645 |  0.009 |  91.803 |
| SCHWARZ-VAN BERKEL | SUI    |     253 |      14 |         0.652 |      0.246 |     -0.227 |  0.081 |          24 |           10 |   -4.936 |             29 |              14 |      1.173 |      -0.678 |  0.004 |  87.401 |
| RETORNAZ J         | ITA    |     212 |      12 |         0.623 |      0.3   |     -0.311 |  0.069 |          25 |           17 |   -6.784 |             29 |              14 |      1.291 |      -1.247 |  0.006 |  79.739 |
| KLIMA L            | CZE    |     219 |      12 |         0.557 |      0.293 |     -0.244 |  0.055 |          17 |           12 |   -5.836 |             33 |              20 |      1.19  |      -0.758 |  0.001 |  79.243 |
| MUSKATEWITZ M      | GER    |     193 |      12 |         0.632 |      0.265 |     -0.321 |  0.05  |          17 |           17 |   -6.407 |             19 |              17 |      0.614 |      -0.981 |  0.022 |  83.421 |
| RAMSFJELL M        | NOR    |     237 |      13 |         0.591 |      0.279 |     -0.294 |  0.044 |          19 |           20 |   -6.006 |             26 |              22 |      1.501 |      -0.925 |  0.008 |  84.806 |
| MOUAT B            | SCO    |     264 |      15 |         0.602 |      0.254 |     -0.279 |  0.042 |          23 |           18 |   -6.877 |             41 |              25 |      1.262 |      -0.767 |  0.021 |  85.907 |
| XU X               | CHN    |     269 |      15 |         0.532 |      0.288 |     -0.255 |  0.034 |          25 |           20 |   -7.131 |             34 |              21 |      1.226 |      -0.937 |  0.014 |  80.472 |
| EDIN N             | SWE    |     239 |      13 |         0.582 |      0.241 |     -0.255 |  0.034 |          17 |           13 |   -7.18  |             26 |              24 |      0.748 |      -1.006 |  0.003 |  85.805 |
| DROPKIN K          | USA    |     215 |      12 |         0.605 |      0.259 |     -0.323 |  0.029 |          18 |           22 |   -5.868 |             31 |              28 |      1.051 |      -1.556 | -0.004 |  79.245 |
| KIM E              | KOR    |     198 |      12 |         0.475 |      0.176 |     -0.238 | -0.041 |           4 |           10 |   -7.522 |              8 |               8 |      0.445 |      -0.537 |  0.007 |  75.893 |
| YANAGISAWA R       | JPN    |     223 |      12 |         0.507 |      0.21  |     -0.31  | -0.046 |           8 |           21 |   -7.042 |             24 |              27 |      0.878 |      -0.703 |  0.015 |  80.184 |
| KIM H              | KOR    |     202 |      12 |         0.46  |      0.149 |     -0.268 | -0.076 |           7 |           12 |   -7.325 |              5 |              19 |      0.397 |      -0.818 |  0.023 |  74.005 |
| GENNER M           | AUT    |     186 |      12 |         0.462 |      0.231 |     -0.38  | -0.098 |           9 |           26 |  -10.117 |             10 |              29 |      0.447 |      -0.791 |  0.038 |  68.478 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SCHWALLER Y | SUI    |     256 |      14 |         0.586 |      0.132 |     -0.121 |  0.027 |           4 |            3 |   -2.652 |             10 |               5 |      0.465 |      -0.377 | -0.007 |  87.207 |
| KENNEDY M   | CAN    |     246 |      14 |         0.565 |      0.128 |     -0.132 |  0.015 |           1 |            4 |   -3.513 |              7 |               4 |      0.427 |      -0.598 | -0.008 |  90.549 |
| KAPP B      | GER    |     194 |      12 |         0.521 |      0.151 |     -0.135 |  0.014 |           2 |            2 |   -2.265 |              2 |               5 |      0.278 |      -0.322 |  0.007 |  84.794 |
| ERIKSSON O  | SWE    |     240 |      13 |         0.521 |      0.128 |     -0.115 |  0.012 |           2 |            2 |   -2.498 |              9 |               5 |      0.421 |      -0.408 | -0.009 |  87.812 |
| HARDIE G    | SCO    |     266 |      15 |         0.534 |      0.133 |     -0.13  |  0.01  |           6 |            6 |   -2.883 |             12 |               9 |      0.73  |      -0.528 | -0.002 |  89.192 |
| CERNOVSKY M | CZE    |     220 |      12 |         0.541 |      0.133 |     -0.146 |  0.005 |           1 |            5 |   -3.195 |             14 |              12 |      0.488 |      -0.615 |  0.001 |  84.205 |
| HOWELL T    | USA    |     216 |      12 |         0.537 |      0.12  |     -0.141 | -0.001 |           1 |            1 |   -2.152 |              7 |               6 |      0.415 |      -0.295 |  0.002 |  82.674 |
| FEI X       | CHN    |     270 |      15 |         0.441 |      0.141 |     -0.123 | -0.006 |           3 |            2 |   -2.488 |              9 |               6 |      0.522 |      -0.394 |  0.001 |  84.259 |
| SESAKER M   | NOR    |     238 |      13 |         0.5   |      0.114 |     -0.141 | -0.013 |           1 |            5 |   -3.321 |              4 |               9 |      0.267 |      -0.425 | -0.006 |  85.294 |
| MOSANER A   | ITA    |     214 |      12 |         0.458 |      0.144 |     -0.152 | -0.016 |           6 |            7 |   -3.118 |              3 |              11 |      0.441 |      -0.581 |  0.001 |  84.813 |
| YAMAGUCHI T | JPN    |     226 |      12 |         0.425 |      0.132 |     -0.143 | -0.027 |           2 |            3 |   -2.915 |              5 |               7 |      0.433 |      -0.388 |  0.013 |  80.752 |
| BACKOFEN J  | AUT    |     186 |      12 |         0.414 |      0.117 |     -0.14  | -0.033 |           1 |            2 |   -2.649 |              1 |               3 |      0.237 |      -0.349 |  0.02  |  74.462 |

### Seconds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WRANAA R     | SWE    |     240 |      13 |         0.517 |      0.076 |     -0.078 |  0.002 |           0 |            1 |   -1.69  |              1 |               1 |      0.23  |      -0.226 | -0.002 |  90.521 |
| GALLANT B    | CAN    |     246 |      14 |         0.549 |      0.067 |     -0.082 | -0     |           0 |            1 |   -2.016 |              2 |               2 |      0.309 |      -0.304 | -0.015 |  91.26  |
| ARMAN S      | ITA    |     214 |      12 |         0.5   |      0.076 |     -0.077 | -0.001 |           0 |            0 |   -1.594 |              2 |               2 |      0.273 |      -0.265 | -0.005 |  86.268 |
| MICHEL S     | SUI    |     256 |      14 |         0.453 |      0.069 |     -0.071 | -0.007 |           0 |            0 |   -1.531 |              2 |               1 |      0.26  |      -0.229 | -0.013 |  88.78  |
| RAMSFJELL B  | NOR    |     238 |      13 |         0.42  |      0.073 |     -0.084 | -0.018 |           0 |            1 |   -1.778 |              3 |               1 |      0.298 |      -0.229 |  0.001 |  86.555 |
| STOPERA A    | USA    |     216 |      12 |         0.426 |      0.084 |     -0.098 | -0.02  |           0 |            1 |   -2.01  |              2 |               3 |      0.251 |      -0.248 |  0.001 |  82.06  |
| WANG Z       | CHN    |     270 |      15 |         0.456 |      0.058 |     -0.086 | -0.02  |           0 |            1 |   -1.853 |              1 |               3 |      0.251 |      -0.286 | -0.002 |  83.55  |
| LAMMIE B     | SCO    |     266 |      15 |         0.406 |      0.068 |     -0.088 | -0.025 |           0 |            1 |   -1.901 |              1 |               4 |      0.219 |      -0.285 | -0.007 |  87.782 |
| MESSENZEHL F | GER    |     194 |      12 |         0.479 |      0.068 |     -0.112 | -0.026 |           0 |            1 |   -1.762 |              1 |               1 |      0.235 |      -0.208 |  0.003 |  80.959 |
| JURIK M      | CZE    |     218 |      12 |         0.413 |      0.065 |     -0.092 | -0.027 |           0 |            1 |   -2.125 |              2 |               6 |      0.251 |      -0.378 | -0.004 |  78.67  |
| KIM C        | KOR    |     140 |       9 |         0.393 |      0.134 |     -0.135 | -0.029 |           2 |            2 |   -2.966 |              1 |               6 |      0.215 |      -0.499 |  0.016 |  81.071 |
| USUI S       | JPN    |     226 |      12 |         0.394 |      0.07  |     -0.098 | -0.032 |           0 |            0 |   -1.355 |              2 |               1 |      0.228 |      -0.226 | -0.001 |  80.199 |
| HOFER M      | AUT    |     118 |       8 |         0.39  |      0.063 |     -0.095 | -0.033 |           0 |            0 |   -1.802 |              0 |               1 |      0.101 |      -0.178 |  0.011 |  78.39  |

### Leads

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SUNDGREN C         | SWE    |     240 |      13 |         0.621 |      0.028 |     -0.043 |  0.001 |           0 |            0 |   -0.594 |              0 |               0 |      0.087 |      -0.112 | -0.002 |  93.908 |
| HEBERT B           | CAN    |     238 |      14 |         0.605 |      0.027 |     -0.038 |  0.001 |           0 |            0 |   -0.607 |              0 |               0 |      0.091 |      -0.084 | -0     |  95.273 |
| SCHEUERL J         | GER    |     194 |      12 |         0.608 |      0.03  |     -0.049 | -0.001 |           0 |            0 |   -0.705 |              0 |               0 |      0.091 |      -0.102 | -0.001 |  89.896 |
| MCMILLAN H         | SCO    |     266 |      15 |         0.568 |      0.029 |     -0.042 | -0.001 |           0 |            0 |   -0.746 |              1 |               0 |      0.141 |      -0.132 | -0.001 |  90.152 |
| NEPSTAD G          | NOR    |     238 |      13 |         0.525 |      0.034 |     -0.043 | -0.002 |           0 |            0 |   -0.757 |              0 |               0 |      0.112 |      -0.115 |  0.001 |  91.772 |
| GIOVANELLA M       | ITA    |     214 |      12 |         0.565 |      0.031 |     -0.047 | -0.003 |           0 |            0 |   -0.742 |              1 |               0 |      0.185 |      -0.131 |  0     |  89.019 |
| MAVEC F            | AUT    |     112 |       7 |         0.527 |      0.034 |     -0.047 | -0.005 |           0 |            0 |   -0.546 |              0 |               0 |      0.071 |      -0.083 |  0.002 |  83.259 |
| LACHAT-COUCHEPIN P | SUI    |     254 |      14 |         0.531 |      0.03  |     -0.046 | -0.005 |           0 |            0 |   -0.671 |              0 |               0 |      0.098 |      -0.094 | -0.002 |  90.139 |
| KIM J              | KOR    |      84 |       9 |         0.524 |      0.03  |     -0.049 | -0.008 |           0 |            0 |   -0.641 |              0 |               0 |      0.048 |      -0.109 |  0.002 |  77.976 |
| KLIPA L            | CZE    |     220 |      12 |         0.518 |      0.027 |     -0.047 | -0.009 |           0 |            0 |   -0.846 |              0 |               1 |      0.072 |      -0.179 |  0.001 |  90.909 |
| KOIZUMI S          | JPN    |     226 |      12 |         0.5   |      0.03  |     -0.052 | -0.011 |           0 |            0 |   -0.656 |              0 |               0 |      0.077 |      -0.155 |  0.004 |  87.333 |
| LI Z               | CHN    |     270 |      15 |         0.478 |      0.029 |     -0.049 | -0.012 |           0 |            0 |   -0.886 |              0 |               0 |      0.065 |      -0.137 |  0.003 |  88.889 |
| FENNER M           | USA    |     216 |      12 |         0.495 |      0.024 |     -0.051 | -0.014 |           0 |            0 |   -0.791 |              0 |               0 |      0.089 |      -0.135 | -0     |  89.12  |
| PYO J              | KOR    |     186 |      12 |         0.478 |      0.041 |     -0.077 | -0.021 |           0 |            0 |   -1.676 |              0 |               1 |      0.139 |      -0.192 |  0.003 |  80.108 |
| REICHEL M          | AUT    |     142 |       9 |         0.472 |      0.041 |     -0.096 | -0.031 |           0 |            0 |   -1.482 |              0 |               2 |      0.115 |      -0.256 |  0.002 |  82.57  |

