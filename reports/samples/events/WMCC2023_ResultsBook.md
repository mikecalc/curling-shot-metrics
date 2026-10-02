# World Men's Curling Championship (WMCC2023_ResultsBook)

Ottawa, ON, Canada, 2023; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The player tables show the spread of each player's shots, not just their average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more percentage points of win probability, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SCO    |      14 | 12-2     |  35.7 |   3.4 |  33.2 |      -2.8 |     1.8 |      70.4 |
| SUI    |      14 | 12-2     |  35.7 |   6.9 |  33.9 |      -1.3 |    -3.7 |      68.5 |
| NOR    |      13 | 10-3     |  26.9 |   2.8 |  16.3 |       9.5 |    -1.7 |      54   |
| CAN    |      15 | 11-4     |  23.3 |   2.4 |  20   |      -2.1 |     3   |      66.2 |
| SWE    |      13 | 9-4      |  19.2 |   2.8 |  15.4 |       3.8 |    -2.7 |      69.3 |
| ITA    |      15 | 9-6      |  10   |  -2.4 |   8.2 |      -1.4 |     5.6 |      57.2 |
| USA    |      12 | 5-7      |  -8.3 |  -2   |   5.5 |     -15.4 |     3.5 |      48.4 |
| JPN    |      12 | 5-7      |  -8.3 |  -2   | -14.6 |      10.3 |    -2   |      42.3 |
| GER    |      12 | 4-8      | -16.7 |  -6   | -16.2 |       8.1 |    -2.6 |      33.7 |
| CZE    |      12 | 3-9      | -25   |  -2   | -13.7 |     -10.5 |     1.2 |      34.7 |
| TUR    |      12 | 2-10     | -33.3 |  -4   | -29.9 |      -1.3 |     1.8 |      39.4 |
| KOR    |      12 | 1-11     | -41.7 |   2   | -35.1 |      -4.8 |    -3.8 |      26.6 |
| NZL    |      12 | 1-11     | -41.7 |  -4   | -43.9 |       8.1 |    -1.8 |      24.9 |

### Fourths

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MOUAT B      | SCO    |     246 |      14 |         0.634 |      0.262 |     -0.244 |  0.077 |          25 |           16 |   -4.505 |             41 |              21 |      0.92  |      -0.697 |  0.014 |  84.388 |
| SCHWARZ B    | SUI    |     252 |      14 |         0.647 |      0.244 |     -0.245 |  0.071 |          18 |           10 |   -6.04  |             41 |              20 |      1.206 |      -0.938 |  0.003 |  85.729 |
| GUSHUE B     | CAN    |     257 |      15 |         0.63  |      0.263 |     -0.257 |  0.071 |          23 |           14 |   -5.503 |             26 |              18 |      0.922 |      -0.927 |  0.009 |  87.795 |
| SHUSTER J    | USA    |     210 |      12 |         0.648 |      0.288 |     -0.343 |  0.066 |          24 |           16 |   -7.722 |             29 |              18 |      0.885 |      -1.394 |  0.001 |  78.708 |
| EDIN N       | SWE    |     219 |      13 |         0.639 |      0.276 |     -0.352 |  0.049 |          20 |           16 |   -8.915 |             35 |              16 |      1.002 |      -1.485 | -0.007 |  83.904 |
| RAMSFJELL M  | NOR    |     241 |      13 |         0.589 |      0.271 |     -0.283 |  0.043 |          29 |           23 |   -6.105 |             34 |              25 |      1.411 |      -0.798 |  0.014 |  82.322 |
| YANAGISAWA R | JPN    |     206 |      12 |         0.583 |      0.234 |     -0.28  |  0.019 |          12 |           13 |   -6.174 |             17 |              14 |      0.692 |      -1.277 | -0.003 |  79.634 |
| RETORNAZ J   | ITA    |     260 |      15 |         0.6   |      0.25  |     -0.333 |  0.017 |          24 |           25 |  -10.288 |             28 |              23 |      1.143 |      -1.365 |  0     |  82.239 |
| TOTZEK S     | GER    |     207 |      12 |         0.512 |      0.278 |     -0.306 | -0.007 |          14 |           21 |   -7.146 |             17 |              19 |      0.719 |      -0.894 |  0.015 |  75.725 |
| KLIMA L      | CZE    |     204 |      12 |         0.539 |      0.256 |     -0.331 | -0.014 |          16 |           22 |   -7.382 |             25 |              24 |      0.653 |      -0.876 |  0.003 |  72.401 |
| KARAGOZ U    | TUR    |     206 |      12 |         0.456 |      0.281 |     -0.382 | -0.079 |          15 |           27 |   -8.975 |             22 |              30 |      1.242 |      -2.132 |  0.015 |  68.137 |
| JEONG B      | KOR    |     195 |      12 |         0.513 |      0.166 |     -0.433 | -0.126 |           2 |           32 |   -8.398 |              6 |              29 |      0.394 |      -0.824 |  0.014 |  69.201 |
| HOOD A       | NZL    |     197 |      12 |         0.416 |      0.271 |     -0.416 | -0.13  |          13 |           36 |  -10.954 |             18 |              26 |      0.97  |      -1.354 |  0.021 |  66.495 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HARDIE G    | SCO    |     248 |      14 |         0.629 |      0.157 |     -0.129 |  0.051 |           5 |            1 |   -2.547 |              9 |               7 |      0.472 |      -0.355 | -0.004 |  87.652 |
| NICHOLS M   | CAN    |     260 |      15 |         0.588 |      0.157 |     -0.116 |  0.045 |           7 |            1 |   -2.498 |             10 |               6 |      0.47  |      -0.34  | -0.003 |  85.769 |
| SCHWALLER Y | SUI    |     254 |      14 |         0.575 |      0.139 |     -0.108 |  0.034 |           2 |            1 |   -2.402 |             16 |               5 |      0.491 |      -0.414 |  0.001 |  90.65  |
| ERIKSSON O  | SWE    |     220 |      13 |         0.536 |      0.147 |     -0.139 |  0.014 |           4 |            4 |   -2.743 |              9 |               6 |      0.548 |      -0.496 | -0.017 |  83.219 |
| MOSANER A   | ITA    |     260 |      15 |         0.569 |      0.137 |     -0.149 |  0.014 |           2 |            5 |   -3.246 |              8 |               4 |      0.446 |      -0.325 |  0.004 |  86.442 |
| CERNOVSKY M | CZE    |     208 |      12 |         0.495 |      0.16  |     -0.134 |  0.012 |           3 |            5 |   -3.3   |             12 |               5 |      0.486 |      -0.507 |  0.013 |  79.688 |
| YAMAGUCHI T | JPN    |     208 |      12 |         0.5   |      0.133 |     -0.127 |  0.003 |           2 |            0 |   -2.139 |              6 |               4 |      0.333 |      -0.354 |  0.005 |  83.053 |
| DEMIREL MH  | TUR    |     207 |      12 |         0.527 |      0.138 |     -0.154 | -0     |           4 |            4 |   -2.878 |             13 |              12 |      0.653 |      -0.483 |  0.01  |  79.227 |
| SESAKER M   | NOR    |     242 |      13 |         0.496 |      0.125 |     -0.148 | -0.013 |           1 |            3 |   -2.873 |              5 |              12 |      0.338 |      -0.549 |  0.002 |  82.231 |
| PLYS C      | USA    |     210 |      12 |         0.443 |      0.162 |     -0.152 | -0.013 |           2 |            2 |   -2.725 |              8 |               8 |      0.516 |      -0.355 |  0.013 |  78.469 |
| HARSCH K    | GER    |     210 |      12 |         0.41  |      0.156 |     -0.144 | -0.021 |           4 |            5 |   -2.825 |              2 |               7 |      0.304 |      -0.341 |  0.016 |  78.214 |
| LEE J       | KOR    |     196 |      12 |         0.429 |      0.121 |     -0.175 | -0.048 |           1 |            3 |   -3.066 |              3 |               7 |      0.265 |      -0.414 |  0.014 |  73.597 |
| SMITH B     | NZL    |     198 |      12 |         0.384 |      0.118 |     -0.187 | -0.07  |           0 |           11 |   -4.017 |              1 |              12 |      0.242 |      -0.41  |  0.017 |  67.929 |

### Seconds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WRANAA R    | SWE    |     220 |      13 |         0.559 |      0.077 |     -0.067 |  0.013 |           0 |            0 |   -1.121 |              2 |               0 |      0.286 |      -0.139 | -0.01  |  88.977 |
| HARNDEN E   | CAN    |     260 |      15 |         0.542 |      0.078 |     -0.089 |  0.002 |           0 |            1 |   -1.715 |              2 |               0 |      0.239 |      -0.191 | -0.007 |  82.432 |
| ARMAN S     | ITA    |     260 |      15 |         0.531 |      0.076 |     -0.094 | -0.004 |           0 |            2 |   -2.472 |              1 |               2 |      0.256 |      -0.291 |  0.002 |  84.436 |
| RAMSFJELL B | NOR    |     242 |      13 |         0.467 |      0.076 |     -0.075 | -0.004 |           0 |            1 |   -1.936 |              3 |               2 |      0.247 |      -0.231 | -0.001 |  83.884 |
| LAMMIE B    | SCO    |     248 |      14 |         0.484 |      0.078 |     -0.086 | -0.006 |           0 |            0 |   -1.498 |              4 |               1 |      0.342 |      -0.21  | -0.012 |  80.466 |
| MICHEL S    | SUI    |     254 |      14 |         0.484 |      0.078 |     -0.091 | -0.009 |           1 |            0 |   -1.958 |              4 |               6 |      0.282 |      -0.336 |  0.002 |  85.375 |
| HAMILTON M  | USA    |     190 |      11 |         0.432 |      0.103 |     -0.096 | -0.01  |           1 |            4 |   -3.09  |              1 |               1 |      0.196 |      -0.22  |  0.007 |  79.474 |
| YAMAMOTO T  | JPN    |     208 |      12 |         0.418 |      0.077 |     -0.088 | -0.019 |           0 |            0 |   -1.814 |              2 |               0 |      0.23  |      -0.224 | -0.004 |  81.068 |
| SUTOR M     | GER    |     208 |      12 |         0.409 |      0.086 |     -0.093 | -0.02  |           0 |            0 |   -1.43  |              3 |               1 |      0.264 |      -0.198 |  0.005 |  74.038 |
| BOHAC R     | CZE    |     170 |      11 |         0.447 |      0.067 |     -0.103 | -0.027 |           0 |            1 |   -2.054 |              0 |               1 |      0.128 |      -0.223 |  0.002 |  76.324 |
| UCAN MZ     | TUR    |     169 |      10 |         0.385 |      0.075 |     -0.096 | -0.031 |           0 |            2 |   -2.46  |              1 |               3 |      0.184 |      -0.51  |  0.009 |  78.698 |
| KIM M       | KOR    |     196 |      12 |         0.378 |      0.085 |     -0.106 | -0.034 |           0 |            2 |   -2.324 |              1 |               2 |      0.157 |      -0.256 |  0.012 |  74.745 |
| SARGON B    | NZL    |     198 |      12 |         0.404 |      0.059 |     -0.11  | -0.042 |           0 |            0 |   -1.943 |              0 |               2 |      0.147 |      -0.253 |  0.006 |  70.581 |
| KAVAZ F     | TUR    |      44 |       4 |         0.364 |      0.055 |     -0.118 | -0.055 |           0 |            1 |   -1.736 |              1 |               0 |      0.119 |      -0.156 |  0.004 |  63.068 |

### Leads

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SUNDGREN C    | SWE    |     216 |      13 |         0.644 |      0.039 |     -0.041 |  0.01  |           0 |            0 |   -0.749 |              0 |               0 |      0.096 |      -0.115 |  0.005 |  89.931 |
| MCMILLAN H    | SCO    |     246 |      14 |         0.598 |      0.034 |     -0.036 |  0.006 |           0 |            0 |   -0.629 |              0 |               0 |      0.085 |      -0.087 |  0.005 |  90.346 |
| HUFMAN C      | USA    |      84 |       5 |         0.595 |      0.049 |     -0.06  |  0.005 |           0 |            0 |   -0.88  |              0 |               1 |      0.121 |      -0.133 |  0.005 |  89.583 |
| KOIZUMI S     | JPN    |     208 |      12 |         0.62  |      0.038 |     -0.05  |  0.005 |           0 |            0 |   -0.631 |              0 |               0 |      0.109 |      -0.103 |  0     |  85.577 |
| GREINDL D     | GER    |     210 |      12 |         0.571 |      0.041 |     -0.046 |  0.004 |           0 |            0 |   -0.725 |              0 |               0 |      0.093 |      -0.106 |  0.001 |  85.119 |
| LANDSTEINER J | USA    |     146 |       9 |         0.582 |      0.04  |     -0.047 |  0.004 |           0 |            0 |   -0.726 |              0 |               0 |      0.073 |      -0.096 |  0.002 |  86.473 |
| KIM T         | KOR    |     196 |      12 |         0.577 |      0.04  |     -0.05  |  0.002 |           0 |            0 |   -0.694 |              0 |               0 |      0.091 |      -0.096 |  0     |  86.923 |
| WALKER G      | CAN    |     256 |      15 |         0.527 |      0.036 |     -0.036 |  0.002 |           0 |            0 |   -0.618 |              0 |               0 |      0.091 |      -0.077 |  0.002 |  92.676 |
| GIOVANELLA M  | ITA    |     260 |      15 |         0.546 |      0.038 |     -0.043 |  0.002 |           0 |            0 |   -0.65  |              0 |               0 |      0.144 |      -0.094 |  0.002 |  88.803 |
| NEPSTAD G     | NOR    |     242 |      13 |         0.566 |      0.037 |     -0.044 |  0.001 |           0 |            0 |   -0.878 |              0 |               0 |      0.093 |      -0.134 |  0.003 |  88.071 |
| LACHAT P      | SUI    |     254 |      14 |         0.563 |      0.038 |     -0.047 |  0.001 |           0 |            0 |   -0.721 |              0 |               1 |      0.103 |      -0.138 |  0.005 |  86.122 |
| WALKER H      | NZL    |     190 |      12 |         0.563 |      0.037 |     -0.049 | -0.001 |           0 |            0 |   -0.651 |              0 |               0 |      0.094 |      -0.092 |  0.002 |  86.579 |
| KLIPA L       | CZE    |      58 |       3 |         0.5   |      0.034 |     -0.05  | -0.008 |           0 |            0 |   -0.596 |              0 |               0 |      0.08  |      -0.134 | -0.002 |  75     |
| YUCE O        | TUR    |     198 |      12 |         0.465 |      0.038 |     -0.057 | -0.013 |           0 |            0 |   -0.881 |              0 |               1 |      0.091 |      -0.182 |  0.005 |  80.051 |
| JURIK M       | CZE    |     188 |      11 |         0.495 |      0.041 |     -0.067 | -0.014 |           0 |            0 |   -1.494 |              0 |               2 |      0.087 |      -0.236 |  0.001 |  79.122 |

