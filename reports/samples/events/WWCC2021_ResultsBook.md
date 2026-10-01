# World Women's Curling Championship (WWCC2021_ResultsBook)

Calgary, AB, Canada, 2021; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SUI    |      15 | 14-1     |  43.3 |   8.3 |  23.9 |      10.2 |     0.9 |      74   |
| RCF    |      15 | 12-3     |  30   |   3.8 |  35.3 |      -8.8 |    -0.3 |      60.6 |
| SWE    |      16 | 11-5     |  18.8 |   1.4 |   5.8 |      12.3 |    -0.7 |      57.2 |
| DEN    |      14 | 8-6      |   7.1 |   1.6 |  -0.7 |       9.8 |    -3.6 |      50.6 |
| USA    |      16 | 9-7      |   6.2 |  -4.2 |  11.6 |      -3.7 |     2.6 |      53.3 |
| KOR    |      13 | 7-6      |   3.8 |   0.9 |   1.9 |       1.1 |    -0   |      58.1 |
| CAN    |      14 | 7-7      |   0   |  -3.2 |   2.8 |      -1.6 |     2.1 |      54.7 |
| SCO    |      13 | 6-7      |  -3.8 |   0.9 |  16   |     -21.8 |     1.1 |      52.5 |
| GER    |      13 | 6-7      |  -3.8 |   0.9 | -10.6 |       8.6 |    -2.6 |      44.5 |
| CHN    |      13 | 6-7      |  -3.8 |  -4.3 |  -5.6 |       4.7 |     1.4 |      43.5 |
| JPN    |      13 | 5-8      | -11.5 |  -2.6 |  13   |     -21.7 |    -0.2 |      49.9 |
| CZE    |      13 | 3-10     | -26.9 |  -4.3 | -19.6 |      -2.4 |    -0.5 |      29.8 |
| ITA    |      13 | 2-11     | -34.6 |  -0.9 | -40.2 |       5.4 |     1.1 |      30.6 |
| EST    |      13 | 1-12     | -42.3 |   0.9 | -46.7 |       5   |    -1.5 |      32.4 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| SCO    |     1018 |   0.016 |    -0.003 |          0.598 |                2.031 |                   2.074 |
| EST    |     1005 |   0.011 |    -0.017 |          0.614 |                1.835 |                   2.086 |
| SUI    |     1030 |   0.008 |     0.026 |          0.563 |                2.095 |                   1.898 |
| GER    |      990 |   0.007 |     0.001 |          0.577 |                1.896 |                   2.015 |
| CZE    |      911 |   0.004 |    -0.011 |          0.613 |                1.932 |                   1.822 |
| USA    |     1215 |   0.003 |     0.011 |          0.577 |                1.947 |                   1.904 |
| DEN    |     1029 |   0.001 |    -0.009 |          0.641 |                2.077 |                   2.184 |
| ITA    |      954 |  -0.001 |    -0.026 |          0.613 |                1.874 |                   2.06  |
| JPN    |     1004 |  -0.001 |    -0.004 |          0.593 |                2.033 |                   1.873 |
| CHN    |      949 |  -0.004 |     0.002 |          0.579 |                2.125 |                   1.903 |
| KOR    |      988 |  -0.006 |    -0.01  |          0.615 |                2.031 |                   2.235 |
| RCF    |     1155 |  -0.007 |     0.013 |          0.584 |                2.091 |                   1.994 |
| CAN    |     1047 |  -0.01  |     0.018 |          0.585 |                1.911 |                   2.053 |
| SWE    |     1178 |  -0.017 |     0.002 |          0.58  |                2.124 |                   1.913 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| PAETZ A       | SUI    |     258 |      15 |         0.62  |      0.264 |     -0.23  |          26 |           15 |   -4.486 |  0.077 |             33 |              21 |      0.995 |      -0.605 |  0.018 |  84.941 |
| KOVALEVA A    | RCF    |     288 |      15 |         0.615 |      0.251 |     -0.308 |          28 |           23 |   -7.757 |  0.036 |             43 |              31 |      2.346 |      -1.355 |  0.005 |  80.035 |
| MUIRHEAD E    | SCO    |     255 |      13 |         0.592 |      0.26  |     -0.272 |          23 |           18 |   -6.23  |  0.043 |             37 |              24 |      1.097 |      -1.289 |  0.007 |  79.249 |
| HASSELBORG A  | SWE    |     295 |      16 |         0.586 |      0.264 |     -0.27  |          26 |           22 |   -5.562 |  0.043 |             22 |              32 |      1.28  |      -0.981 |  0.004 |  80.593 |
| PETERSON TAB  | USA    |     305 |      16 |         0.58  |      0.234 |     -0.275 |          16 |           22 |   -5.941 |  0.02  |             38 |              27 |      1.079 |      -1.49  |  0.016 |  76.974 |
| JENTSCH D     | GER    |     249 |      13 |         0.574 |      0.254 |     -0.334 |          19 |           28 |   -6.4   |  0.003 |             28 |              34 |      1.174 |      -1.717 |  0.013 |  74.297 |
| YOSHIMURA S   | JPN    |     253 |      13 |         0.53  |      0.248 |     -0.244 |          15 |           17 |   -5.533 |  0.016 |             32 |              24 |      1.103 |      -0.879 |  0.01  |  76.885 |
| KIM E         | KOR    |     250 |      13 |         0.528 |      0.292 |     -0.354 |          21 |           30 |   -9.226 | -0.013 |             42 |              37 |      1.509 |      -1.287 |  0.011 |  71.774 |
| EINARSON K    | CAN    |     262 |      14 |         0.523 |      0.227 |     -0.302 |          15 |           27 |   -6.539 | -0.025 |             27 |              34 |      1.001 |      -1.489 |  0.014 |  76.255 |
| HAN Y         | CHN    |     236 |      13 |         0.517 |      0.246 |     -0.274 |          14 |           17 |   -6.083 | -0.005 |             14 |              21 |      0.822 |      -0.739 |  0.024 |  77.34  |
| TURMANN M     | EST    |     250 |      13 |         0.516 |      0.236 |     -0.38  |          16 |           37 |   -9.539 | -0.062 |             28 |              45 |      0.89  |      -1.721 |  0.016 |  68.927 |
| CONSTANTINI S | ITA    |     237 |      13 |         0.506 |      0.229 |     -0.329 |          12 |           26 |   -8.284 | -0.046 |             16 |              35 |      0.751 |      -0.847 |  0.005 |  69.255 |
| DUPONT M      | DEN    |     260 |      14 |         0.504 |      0.296 |     -0.262 |          23 |           21 |   -4.913 |  0.019 |             36 |              37 |      1.52  |      -1.006 |  0.006 |  72.008 |
| KUBESKOVA A   | CZE    |     228 |      13 |         0.5   |      0.283 |     -0.379 |          19 |           32 |   -9.886 | -0.048 |             23 |              37 |      0.886 |      -1.356 |  0.03  |  70.796 |

### Thirds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| TIRINZONI S  | SUI    |     238 |      14 |         0.58  |      0.139 |     -0.128 |           2 |            3 |   -2.791 |  0.027 |              7 |               6 |      0.277 |      -0.486 |  0.003 |  85.819 |
| WRIGHT V     | SCO    |     256 |      13 |         0.555 |      0.143 |     -0.151 |           2 |            4 |   -2.801 |  0.012 |             14 |              12 |      0.436 |      -0.585 |  0.009 |  81.738 |
| SWEETING V   | CAN    |     264 |      14 |         0.542 |      0.148 |     -0.123 |           4 |            2 |   -2.745 |  0.024 |             14 |              10 |      0.466 |      -0.451 |  0.005 |  81.345 |
| PORTUNOVA J  | RCF    |     292 |      15 |         0.541 |      0.143 |     -0.137 |           2 |            4 |   -3.154 |  0.015 |             14 |               8 |      0.57  |      -0.389 |  0.004 |  82.277 |
| ONODERA K    | JPN    |     254 |      13 |         0.539 |      0.123 |     -0.139 |           2 |            4 |   -3.08  |  0.002 |              9 |              11 |      0.57  |      -0.54  |  0.01  |  83.661 |
| MCMANUS S    | SWE    |     298 |      16 |         0.537 |      0.132 |     -0.147 |           4 |            3 |   -2.969 |  0.002 |             10 |              13 |      0.408 |      -0.399 |  0     |  81.711 |
| ROTH N       | USA    |     306 |      16 |         0.523 |      0.127 |     -0.14  |           2 |            4 |   -3.39  | -0.001 |             13 |              12 |      0.497 |      -0.521 |  0.014 |  79.739 |
| KIM K        | KOR    |     252 |      13 |         0.52  |      0.139 |     -0.132 |           1 |            2 |   -2.597 |  0.009 |             10 |              10 |      0.438 |      -0.578 | -0.004 |  78.77  |
| DONG Z       | CHN    |     240 |      13 |         0.512 |      0.12  |     -0.128 |           2 |            2 |   -2.388 | -0.001 |              4 |               6 |      0.302 |      -0.337 |  0.002 |  77.083 |
| HOEHNE M     | GER    |     377 |      13 |         0.507 |      0.117 |     -0.133 |           2 |            5 |   -3.234 | -0.006 |             19 |              16 |      0.415 |      -0.579 |  0.003 |  74.801 |
| HALSE M      | DEN    |     262 |      14 |         0.496 |      0.136 |     -0.171 |           4 |            6 |   -2.889 | -0.018 |             12 |              19 |      0.46  |      -0.511 |  0.006 |  71.469 |
| LO DESERTO M | ITA    |     244 |      13 |         0.459 |      0.109 |     -0.142 |           2 |            5 |   -2.791 | -0.027 |              5 |              10 |      0.335 |      -0.373 |  0.008 |  73.258 |
| TURMANN L    | EST    |     234 |      12 |         0.423 |      0.126 |     -0.153 |           2 |            6 |   -2.994 | -0.035 |              6 |              14 |      0.382 |      -0.577 |  0.01  |  69.551 |
| BAUDYSOVA A  | CZE    |     230 |      13 |         0.409 |      0.128 |     -0.143 |           1 |            2 |   -2.605 | -0.032 |              6 |               7 |      0.399 |      -0.371 |  0.018 |  70.652 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| NEUENSCHWANDER E | SUI    |     258 |      15 |         0.57  |      0.087 |     -0.088 |           1 |            0 |   -1.473 |  0.012 |              2 |               1 |      0.285 |      -0.203 | -0     |  86.089 |
| KIM C            | KOR    |     252 |      13 |         0.536 |      0.089 |     -0.093 |           2 |            1 |   -2.095 |  0.004 |              4 |               4 |      0.289 |      -0.333 |  0.002 |  78.175 |
| ARSENKINA G      | RCF    |     292 |      15 |         0.531 |      0.082 |     -0.076 |           1 |            0 |   -1.289 |  0.008 |              4 |               1 |      0.346 |      -0.216 |  0.007 |  85.959 |
| DUPONT D         | DEN    |     262 |      14 |         0.519 |      0.074 |     -0.086 |           0 |            1 |   -1.59  | -0.003 |              4 |               1 |      0.333 |      -0.24  |  0.007 |  79.485 |
| KNOCHENHAUER A   | SWE    |     278 |      15 |         0.518 |      0.085 |     -0.086 |           0 |            0 |   -1.826 |  0.003 |              3 |               1 |      0.252 |      -0.226 |  0.001 |  84.173 |
| BIRCHARD S       | CAN    |     264 |      14 |         0.515 |      0.087 |     -0.082 |           1 |            0 |   -1.708 |  0.005 |              6 |               2 |      0.329 |      -0.262 |  0.003 |  84.506 |
| HAMILTON B       | USA    |     306 |      16 |         0.484 |      0.076 |     -0.108 |           0 |            2 |   -2.645 | -0.019 |              1 |               6 |      0.222 |      -0.37  |  0.006 |  80.392 |
| DODDS J          | SCO    |     236 |      12 |         0.479 |      0.09  |     -0.078 |           1 |            0 |   -1.483 |  0.003 |              5 |               2 |      0.476 |      -0.275 | -0.006 |  77.754 |
| VINSOVA P        | CZE    |     156 |       9 |         0.468 |      0.067 |     -0.084 |           0 |            0 |   -1.469 | -0.013 |              3 |               0 |      0.238 |      -0.119 |  0.006 |  77.097 |
| BAUDYSOVA M      | CZE    |     126 |       7 |         0.452 |      0.079 |     -0.102 |           0 |            0 |   -1.407 | -0.02  |              2 |               1 |      0.204 |      -0.241 |  0.004 |  71.429 |
| OHMIYA A         | JPN    |     254 |      13 |         0.437 |      0.076 |     -0.086 |           0 |            1 |   -2.008 | -0.015 |              1 |               3 |      0.211 |      -0.303 |  0.002 |  78.458 |
| ZHANG L          | CHN    |     240 |      13 |         0.433 |      0.074 |     -0.095 |           0 |            0 |   -1.844 | -0.022 |              3 |               2 |      0.289 |      -0.279 |  0.003 |  78.958 |
| ROMEI A          | ITA    |     204 |      11 |         0.407 |      0.069 |     -0.089 |           0 |            0 |   -1.597 | -0.024 |              0 |               1 |      0.138 |      -0.193 |  0.005 |  71.691 |
| GROSSMANN H      | EST    |     118 |       6 |         0.398 |      0.075 |     -0.135 |           0 |            2 |   -2.413 | -0.051 |              0 |               6 |      0.146 |      -0.429 |  0.001 |  65.678 |
| LAIDSALU K       | EST    |     156 |       8 |         0.385 |      0.089 |     -0.097 |           0 |            0 |   -1.823 | -0.026 |              1 |               6 |      0.203 |      -0.291 |  0.012 |  68.91  |

### Leads

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| PETERSON TAR      | USA    |     306 |      16 |         0.67  |      0.039 |     -0.046 |           0 |            0 |   -0.958 |  0.011 |              0 |               0 |      0.135 |      -0.138 | -0     |  85.703 |
| KUZMINA E         | RCF    |     292 |      15 |         0.668 |      0.042 |     -0.051 |           0 |            0 |   -0.741 |  0.011 |              0 |               0 |      0.146 |      -0.13  |  0.001 |  83.677 |
| BARBEZAT M        | SUI    |     256 |      15 |         0.645 |      0.048 |     -0.041 |           0 |            0 |   -0.71  |  0.016 |              0 |               0 |      0.121 |      -0.102 |  0.004 |  90.686 |
| MEILLEUR B        | CAN    |     264 |      14 |         0.633 |      0.041 |     -0.049 |           0 |            0 |   -0.855 |  0.008 |              1 |               0 |      0.188 |      -0.123 |  0.002 |  86.269 |
| MABERGS S         | SWE    |     294 |      16 |         0.612 |      0.05  |     -0.045 |           0 |            0 |   -0.654 |  0.014 |              0 |               0 |      0.113 |      -0.088 |  0.004 |  86.48  |
| KOLCEVSKAJA E     | CZE    |     178 |      10 |         0.601 |      0.042 |     -0.061 |           0 |            0 |   -0.928 |  0.001 |              0 |               0 |      0.116 |      -0.147 |  0.005 |  84.129 |
| FUNAYAMA Y        | JPN    |     254 |      13 |         0.587 |      0.044 |     -0.059 |           0 |            0 |   -1.04  |  0.001 |              0 |               0 |      0.154 |      -0.135 |  0.002 |  84.055 |
| TUVIKE E          | EST    |     254 |      13 |         0.579 |      0.036 |     -0.053 |           0 |            0 |   -0.714 | -0.001 |              0 |               1 |      0.11  |      -0.142 |  0.001 |  77.067 |
| JIANG X           | CHN    |     240 |      13 |         0.575 |      0.042 |     -0.058 |           0 |            0 |   -0.855 | -0.001 |              0 |               0 |      0.122 |      -0.107 |  0.002 |  82.636 |
| KIM S             | KOR    |     252 |      13 |         0.567 |      0.048 |     -0.05  |           0 |            0 |   -1.054 |  0.006 |              0 |               0 |      0.16  |      -0.153 |  0.005 |  81.647 |
| GRAY L            | SCO    |     256 |      13 |         0.562 |      0.042 |     -0.055 |           0 |            0 |   -0.977 | -0     |              0 |               0 |      0.115 |      -0.183 | -0     |  83.691 |
| DAMI E            | ITA    |      78 |       4 |         0.526 |      0.046 |     -0.061 |           0 |            0 |   -0.764 | -0.005 |              0 |               0 |      0.062 |      -0.099 | -0.003 |  80.592 |
| LARSEN M          | DEN    |     176 |       9 |         0.5   |      0.04  |     -0.052 |           0 |            0 |   -0.763 | -0.006 |              0 |               0 |      0.118 |      -0.116 |  0.004 |  83.807 |
| JENTSCH A         | GER    |     378 |      13 |         0.492 |      0.041 |     -0.062 |           0 |            1 |   -1.663 | -0.011 |              2 |               4 |      0.197 |      -0.288 |  0.001 |  79.775 |
| ZARDINI LACEDELLI | ITA    |     206 |      11 |         0.485 |      0.053 |     -0.064 |           0 |            0 |   -0.984 | -0.007 |              0 |               1 |      0.141 |      -0.176 |  0     |  79.634 |
| KNUDSEN L         | DEN    |      86 |       5 |         0.477 |      0.029 |     -0.039 |           0 |            0 |   -0.572 | -0.007 |              0 |               0 |      0.075 |      -0.07  |  0.005 |  83.721 |

