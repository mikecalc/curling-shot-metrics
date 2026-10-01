# Olympic Winter Games (OWG2018_ResultsBook)

PyeongChang, Republic of Korea, 2018; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SWE    |      11 | 8-3      |  22.7 |   7.4 |   2.9 |      11.2 |     1.2 |      65.2 |
| USA    |      11 | 7-4      |  13.6 |  -1.1 |  12.2 |       2.1 |     0.4 |      51.2 |
| SUI    |      12 | 7-5      |   8.3 |   0   |   8.3 |       0.3 |    -0.3 |      52.9 |
| CAN    |      11 | 6-5      |   4.5 |   3.2 |  10.7 |      -7.8 |    -1.5 |      56.1 |
| GBR    |      10 | 5-5      |   0   |   0   |  -1.6 |       2.1 |    -0.5 |      50.8 |
| NOR    |       9 | 4-5      |  -5.6 |  -3.9 |  -1.4 |      -1.3 |     1   |      51.6 |
| KOR    |       9 | 4-5      |  -5.6 |  -1.3 | -10   |       4.5 |     1.2 |      45.7 |
| JPN    |       9 | 4-5      |  -5.6 |  -6.5 |  12.3 |     -10.7 |    -0.7 |      45.7 |
| ITA    |       9 | 3-6      | -16.7 |  -1.3 |  -4.9 |     -10.3 |    -0.1 |      39.6 |
| DEN    |       9 | 2-7      | -27.8 |   1.3 | -36.9 |       8.4 |    -0.6 |      35.2 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| CAN    |      835 |   0.008 |     0.003 |          0.61  |                1.958 |                   2.085 |
| GBR    |      758 |   0.007 |     0.01  |          0.591 |                1.8   |                   1.968 |
| NOR    |      647 |   0.005 |     0.031 |          0.569 |                1.957 |                   2.058 |
| KOR    |      691 |   0.004 |    -0.015 |          0.63  |                1.899 |                   1.886 |
| DEN    |      694 |   0.004 |    -0.024 |          0.608 |                1.855 |                   1.905 |
| SUI    |      912 |   0     |    -0.009 |          0.6   |                2.253 |                   1.959 |
| USA    |      800 |  -0.001 |     0.003 |          0.57  |                2.135 |                   2.058 |
| ITA    |      707 |  -0.005 |    -0.023 |          0.655 |                1.839 |                   2.089 |
| SWE    |      750 |  -0.012 |     0.017 |          0.555 |                2.253 |                   1.938 |
| JPN    |      654 |  -0.013 |     0.01  |          0.58  |                2.044 |                   2.077 |

### Fourths

| player     | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SCHWARZ B  | SUI    |     229 |      12 |         0.585 |      0.221 |     -0.264 |          18 |           14 |   -5.106 |  0.02  |             35 |              28 |      0.692 |      -1.016 |  0.005 |  81.278 |
| MOROZUMI Y | JPN    |     164 |       9 |         0.579 |      0.253 |     -0.284 |          17 |           11 |   -3.941 |  0.027 |             19 |              22 |      0.851 |      -0.659 |  0.023 |  77.454 |
| KOE K      | CAN    |     209 |      11 |         0.579 |      0.253 |     -0.261 |          19 |           17 |   -5.677 |  0.036 |             26 |              19 |      0.862 |      -1.055 |  0.007 |  83.213 |
| KIM C      | KOR    |     172 |       9 |         0.576 |      0.216 |     -0.311 |          10 |           13 |   -7.162 | -0.008 |             10 |              20 |      0.89  |      -1.133 |  0.011 |  76.744 |
| EDIN N     | SWE    |     188 |      11 |         0.574 |      0.263 |     -0.265 |          17 |           16 |   -4.193 |  0.038 |             23 |              11 |      0.607 |      -0.48  |  0.005 |  84.973 |
| MOSANER A  | ITA    |     179 |       9 |         0.564 |      0.249 |     -0.254 |          15 |           16 |   -4.361 |  0.03  |             24 |              21 |      0.778 |      -0.729 |  0.016 |  80.508 |
| ULSRUD T   | NOR    |     160 |       9 |         0.562 |      0.285 |     -0.339 |          10 |           19 |   -6.575 |  0.012 |             26 |              18 |      1.303 |      -1.367 | -0.014 |  79.874 |
| SHUSTER J  | USA    |     199 |      11 |         0.558 |      0.263 |     -0.294 |          18 |           18 |   -5.567 |  0.017 |             27 |              21 |      0.84  |      -0.75  |  0.016 |  78.518 |
| STJERNE R  | DEN    |     173 |       9 |         0.543 |      0.164 |     -0.309 |           5 |           15 |   -7.307 | -0.052 |              7 |              17 |      0.454 |      -1     |  0.017 |  75.446 |
| SMITH K    | GBR    |     189 |      10 |         0.54  |      0.21  |     -0.299 |          13 |           18 |   -6.254 | -0.024 |             22 |              30 |      0.975 |      -0.896 | -0.004 |  78.191 |

### Thirds

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| PAETZ C       | SUI    |     230 |      12 |         0.6   |      0.101 |     -0.101 |           1 |            0 |   -1.676 |  0.02  |              7 |               3 |      0.31  |      -0.335 | -0.005 |  84.891 |
| KENNEDY M     | CAN    |     214 |      11 |         0.579 |      0.115 |     -0.128 |           2 |            4 |   -3.411 |  0.012 |              9 |               8 |      0.396 |      -0.657 | -0.011 |  87.15  |
| ERIKSSON O    | SWE    |     190 |      11 |         0.532 |      0.139 |     -0.102 |           2 |            0 |   -1.855 |  0.026 |              7 |               4 |      0.373 |      -0.272 | -0.021 |  87.895 |
| GEORGE T      | USA    |     202 |      11 |         0.515 |      0.114 |     -0.131 |           0 |            2 |   -2.356 | -0.005 |             11 |               7 |      0.329 |      -0.382 | -0     |  80.198 |
| NERGAARD T    | NOR    |     164 |       9 |         0.512 |      0.111 |     -0.121 |           0 |            1 |   -2.092 | -0.002 |              3 |               6 |      0.293 |      -0.354 |  0.003 |  83.129 |
| MUIRHEAD T    | GBR    |     192 |      10 |         0.495 |      0.106 |     -0.125 |           0 |            2 |   -2.429 | -0.011 |              6 |               8 |      0.448 |      -0.41  | -0.002 |  81.641 |
| FREDERIKSEN J | DEN    |     174 |       9 |         0.489 |      0.082 |     -0.15  |           0 |            5 |   -2.824 | -0.037 |              1 |               9 |      0.202 |      -0.49  |  0.002 |  81.322 |
| SHIMIZU T     | JPN    |     164 |       9 |         0.482 |      0.118 |     -0.131 |           2 |            3 |   -2.681 | -0.011 |              5 |               1 |      0.305 |      -0.266 | -0.004 |  79.116 |
| SEONG S       | KOR    |     174 |       9 |         0.443 |      0.115 |     -0.105 |           2 |            1 |   -2.275 | -0.007 |              3 |               5 |      0.377 |      -0.357 | -0.005 |  82.902 |
| RETORNAZ J    | ITA    |     180 |       9 |         0.361 |      0.123 |     -0.14  |           2 |            4 |   -2.775 | -0.045 |              5 |              10 |      0.44  |      -0.381 | -0.007 |  78.333 |

### Seconds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| YAMAGUCHI T | JPN    |     164 |       9 |         0.549 |      0.075 |     -0.072 |           0 |            0 |   -1.088 |  0.009 |              4 |               0 |      0.342 |      -0.175 | -0.004 |  85.213 |
| DE CRUZ P   | SUI    |     230 |      12 |         0.526 |      0.069 |     -0.078 |           0 |            0 |   -1.918 | -0.001 |              1 |               4 |      0.233 |      -0.286 | -0.014 |  82.283 |
| HAMILTON M  | USA    |     202 |      11 |         0.52  |      0.061 |     -0.071 |           0 |            0 |   -1.188 | -0.002 |              1 |               2 |      0.207 |      -0.221 | -0.012 |  81.683 |
| POULSEN M   | DEN    |     174 |       9 |         0.517 |      0.071 |     -0.086 |           0 |            0 |   -1.512 | -0.005 |              1 |               2 |      0.194 |      -0.27  | -0.011 |  85.489 |
| LAING B     | CAN    |     214 |      11 |         0.509 |      0.068 |     -0.066 |           0 |            0 |   -1.584 |  0.002 |              2 |               2 |      0.274 |      -0.258 | -0.009 |  83.879 |
| WADDELL K   | GBR    |     192 |      10 |         0.505 |      0.079 |     -0.08  |           0 |            0 |   -1.714 |  0     |              6 |               5 |      0.332 |      -0.308 | -0.011 |  81.771 |
| WRANAA R    | SWE    |     190 |      11 |         0.495 |      0.075 |     -0.066 |           0 |            0 |   -1.372 |  0.003 |              1 |               2 |      0.209 |      -0.192 | -0.022 |  87.895 |
| GONIN S     | ITA    |     180 |       9 |         0.478 |      0.061 |     -0.061 |           0 |            0 |   -1.315 | -0.003 |              1 |               1 |      0.184 |      -0.208 | -0.005 |  80     |
| SVAE C      | NOR    |     164 |       9 |         0.47  |      0.075 |     -0.085 |           0 |            0 |   -1.656 | -0.01  |              3 |               3 |      0.325 |      -0.329 | -0     |  81.098 |
| OH E        | KOR    |     136 |       7 |         0.434 |      0.066 |     -0.079 |           0 |            1 |   -1.708 | -0.016 |              0 |               1 |      0.184 |      -0.206 | -0.001 |  83.824 |
| KIM M       | KOR    |      38 |       2 |         0.395 |      0.043 |     -0.077 |           0 |            0 |   -0.976 | -0.03  |              0 |               0 |      0.047 |      -0.119 | -0.014 |  78.947 |

### Leads

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| PILZER A      | ITA    |      58 |       3 |         0.603 |      0.033 |     -0.053 |           0 |            0 |   -0.606 | -0.001 |              0 |               0 |      0.044 |      -0.073 | -0.006 |  85.268 |
| SMITH C       | GBR    |     192 |      10 |         0.542 |      0.032 |     -0.031 |           0 |            0 |   -0.673 |  0.003 |              0 |               0 |      0.094 |      -0.111 | -0.001 |  87.042 |
| FERRAZZA D    | ITA    |     122 |       6 |         0.525 |      0.03  |     -0.041 |           0 |            0 |   -0.556 | -0.004 |              0 |               0 |      0.123 |      -0.078 |  0.002 |  83.264 |
| TANNER V      | SUI    |     230 |      12 |         0.517 |      0.035 |     -0.036 |           0 |            0 |   -0.754 |  0.001 |              1 |               0 |      0.178 |      -0.143 |  0.001 |  86.294 |
| MOROZUMI K    | JPN    |     164 |       9 |         0.5   |      0.027 |     -0.043 |           0 |            0 |   -0.762 | -0.008 |              0 |               0 |      0.133 |      -0.102 | -0.001 |  83.079 |
| DUPONT O      | DEN    |     174 |       9 |         0.483 |      0.029 |     -0.039 |           0 |            0 |   -0.653 | -0.006 |              0 |               0 |      0.077 |      -0.106 |  0     |  89.244 |
| HEBERT B      | CAN    |     210 |      11 |         0.481 |      0.032 |     -0.032 |           0 |            0 |   -0.618 | -0.001 |              0 |               0 |      0.078 |      -0.077 | -0.001 |  87.439 |
| SUNDGREN C    | SWE    |     184 |      11 |         0.478 |      0.035 |     -0.036 |           0 |            0 |   -0.589 | -0.002 |              0 |               0 |      0.059 |      -0.075 |  0.004 |  88     |
| LEE K         | KOR    |     174 |       9 |         0.437 |      0.036 |     -0.036 |           0 |            0 |   -0.604 | -0.005 |              0 |               0 |      0.126 |      -0.101 |  0.001 |  87.283 |
| PETERSSON HV  | NOR    |     164 |       9 |         0.433 |      0.038 |     -0.034 |           0 |            0 |   -0.555 | -0.003 |              0 |               0 |      0.078 |      -0.107 | -0.001 |  82.515 |
| LANDSTEINER J | USA    |     202 |      11 |         0.416 |      0.032 |     -0.041 |           0 |            0 |   -0.756 | -0.011 |              0 |               1 |      0.101 |      -0.136 |  0.001 |  82.702 |

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| KOR    |      11 | 9-2      |  31.8 |   3.1 |  12.4 |      14.3 |     2.1 |      68.3 |
| SWE    |      11 | 9-2      |  31.8 |  -1   |  17.4 |      14.8 |     0.6 |      64.1 |
| GBR    |      11 | 6-5      |   4.5 |   7.1 |   6.5 |      -9.2 |     0.1 |      52.5 |
| JPN    |      11 | 6-5      |   4.5 |  -3.1 |  -1.2 |      10.2 |    -1.4 |      46.8 |
| SUI    |       9 | 4-5      |  -5.6 |   3.7 |  -3.8 |      -5.3 |    -0.1 |      58.4 |
| CAN    |       9 | 4-5      |  -5.6 |  -3.7 |  -2.3 |      -2.9 |     3.4 |      50   |
| CHN    |       9 | 4-5      |  -5.6 |  -6.2 |  -1.4 |      -0.3 |     2.5 |      43.4 |
| USA    |       9 | 4-5      |  -5.6 |   3.7 |   2.2 |     -10.9 |    -0.6 |      42.1 |
| OAR    |       9 | 2-7      | -27.8 |   3.7 | -12   |     -17.7 |    -1.9 |      38.7 |
| DEN    |       9 | 1-8      | -38.9 |  -8.7 | -25.6 |       0.5 |    -5.1 |      28.8 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| DEN    |      664 |   0.024 |    -0.021 |          0.636 |                1.947 |                   2.044 |
| USA    |      674 |   0.012 |    -0.018 |          0.636 |                2.159 |                   1.938 |
| CHN    |      691 |   0.012 |    -0.011 |          0.63  |                1.878 |                   2.079 |
| JPN    |      832 |   0.011 |    -0.016 |          0.62  |                1.925 |                   2.148 |
| GBR    |      854 |   0.009 |     0.012 |          0.58  |                1.98  |                   1.942 |
| CAN    |      682 |   0.008 |    -0.006 |          0.626 |                2.169 |                   2.222 |
| OAR    |      643 |  -0.003 |    -0.023 |          0.639 |                2.085 |                   2.114 |
| SWE    |      866 |  -0.021 |     0.034 |          0.539 |                1.729 |                   1.821 |
| SUI    |      665 |  -0.022 |     0.016 |          0.552 |                2.139 |                   1.852 |
| KOR    |      804 |  -0.024 |     0.019 |          0.551 |                2.21  |                   2.057 |

### Fourths

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WANG B       | CHN    |     173 |       9 |         0.601 |      0.239 |     -0.296 |          12 |           12 |   -5.39  |  0.026 |             24 |              20 |      1.109 |      -1.394 |  0.01  |  72.929 |
| KIM E        | KOR    |     202 |      11 |         0.589 |      0.314 |     -0.307 |          19 |           14 |   -5.408 |  0.059 |             30 |              21 |      1.218 |      -1.294 |  0.005 |  77.97  |
| ROTH N       | USA    |     169 |       9 |         0.574 |      0.273 |     -0.356 |          14 |           15 |   -9.147 |  0.005 |             19 |              20 |      1.031 |      -1.194 |  0.015 |  74.554 |
| HOMAN R      | CAN    |     171 |       9 |         0.567 |      0.292 |     -0.275 |          16 |           11 |   -6.392 |  0.047 |             25 |              26 |      1.15  |      -1.336 | -0.005 |  77.059 |
| FUJISAWA S   | JPN    |     209 |      11 |         0.55  |      0.261 |     -0.279 |          17 |           16 |   -6.616 |  0.018 |             27 |              27 |      0.761 |      -0.934 | -0     |  75     |
| HASSELBORG A | SWE    |     216 |      11 |         0.532 |      0.23  |     -0.239 |          12 |           17 |   -5.191 |  0.011 |             27 |              23 |      1.272 |      -1.516 |  0.001 |  82.791 |
| MUIRHEAD E   | GBR    |     215 |      11 |         0.53  |      0.226 |     -0.299 |          15 |           23 |   -6.984 | -0.021 |             26 |              28 |      0.996 |      -1.461 |  0.017 |  76.402 |
| DUPONT M     | DEN    |     168 |       9 |         0.506 |      0.268 |     -0.361 |          13 |           26 |   -6.449 | -0.043 |             22 |              35 |      0.842 |      -1.053 |  0.027 |  67.665 |
| TIRINZONI S  | SUI    |     167 |       9 |         0.503 |      0.268 |     -0.326 |          10 |           13 |   -7.86  | -0.027 |             19 |              24 |      1.037 |      -1.293 |  0.022 |  73.03  |
| MOISEEVA V   | OAR    |     163 |       9 |         0.497 |      0.25  |     -0.366 |          11 |           17 |   -8.927 | -0.06  |             21 |              22 |      0.674 |      -1.013 |  0.008 |  70.092 |

### Thirds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| NEUENSCHWANDER E | SUI    |     168 |       9 |         0.56  |      0.114 |     -0.128 |           0 |            1 |   -2.643 |  0.007 |              3 |               4 |      0.317 |      -0.393 |  0.001 |  80.357 |
| PETERSON T       | USA    |     170 |       9 |         0.547 |      0.135 |     -0.149 |           4 |            0 |   -2.11  |  0.006 |              6 |               5 |      0.627 |      -0.336 | -0.006 |  77.206 |
| MISKEW E         | CAN    |     172 |       9 |         0.547 |      0.141 |     -0.128 |           2 |            2 |   -2.474 |  0.019 |             10 |               7 |      0.457 |      -0.369 | -0.007 |  81.831 |
| YOSHIDA C        | JPN    |     210 |      11 |         0.543 |      0.139 |     -0.141 |           2 |            1 |   -2.405 |  0.011 |             13 |              11 |      0.518 |      -0.38  | -0.005 |  77.857 |
| MCMANUS S        | SWE    |     218 |      11 |         0.528 |      0.138 |     -0.108 |           3 |            1 |   -2.405 |  0.022 |             13 |               3 |      0.393 |      -0.361 | -0.006 |  84.174 |
| SLOAN A          | GBR    |     216 |      11 |         0.519 |      0.127 |     -0.122 |           3 |            3 |   -2.421 |  0.007 |             15 |               9 |      0.683 |      -0.36  | -0.004 |  76.157 |
| ZHOU Y           | CHN    |     174 |       9 |         0.506 |      0.11  |     -0.132 |           0 |            2 |   -2.384 | -0.01  |              5 |               8 |      0.323 |      -0.41  | -0.004 |  76.149 |
| KIM K            | KOR    |     202 |      11 |         0.5   |      0.171 |     -0.156 |           4 |            5 |   -3.515 |  0.008 |             12 |               9 |      0.628 |      -0.528 | -0.003 |  77.475 |
| DUPONT D         | DEN    |     170 |       9 |         0.488 |      0.106 |     -0.151 |           2 |            5 |   -3.349 | -0.026 |              6 |              10 |      0.528 |      -0.421 |  0.003 |  74.556 |
| PORTUNOVA J      | OAR    |      52 |       3 |         0.462 |      0.095 |     -0.221 |           0 |            4 |   -3.117 | -0.075 |              2 |               3 |      0.236 |      -0.392 |  0.006 |  70.192 |
| VASILEVA U       | OAR    |     112 |       6 |         0.455 |      0.143 |     -0.145 |           3 |            1 |   -2.118 | -0.014 |              6 |               4 |      0.543 |      -0.42  |  0.003 |  69.82  |

### Seconds

| player         | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:---------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KNOCHENHAUER A | SWE    |     218 |      11 |         0.587 |      0.065 |     -0.075 |           0 |            0 |   -1.541 |  0.008 |              1 |               2 |      0.331 |      -0.232 | -0.009 |  83.945 |
| GEVING A       | USA    |     170 |       9 |         0.559 |      0.063 |     -0.083 |           0 |            0 |   -1.453 | -0.001 |              3 |               1 |      0.24  |      -0.243 | -0.002 |  76.912 |
| ARSENKINA G    | OAR    |     164 |       9 |         0.555 |      0.087 |     -0.085 |           0 |            0 |   -1.221 |  0.01  |              6 |               2 |      0.382 |      -0.252 |  0.003 |  81.902 |
| COURTNEY J     | CAN    |     172 |       9 |         0.541 |      0.092 |     -0.083 |           1 |            0 |   -1.229 |  0.011 |              7 |               2 |      0.347 |      -0.258 | -0.008 |  79.506 |
| LIU J          | CHN    |     174 |       9 |         0.506 |      0.075 |     -0.094 |           0 |            0 |   -1.57  | -0.008 |              2 |               3 |      0.288 |      -0.324 |  0.006 |  76.437 |
| ADAMS V        | GBR    |     216 |      11 |         0.481 |      0.084 |     -0.083 |           0 |            0 |   -1.637 | -0.003 |              2 |               4 |      0.297 |      -0.289 |  0.002 |  78.472 |
| HOGH J         | DEN    |     136 |       7 |         0.478 |      0.082 |     -0.092 |           0 |            0 |   -1.452 | -0.009 |              1 |               3 |      0.204 |      -0.255 | -0.004 |  73.897 |
| KIM S          | KOR    |     202 |      11 |         0.475 |      0.083 |     -0.09  |           1 |            1 |   -1.954 | -0.007 |              1 |               3 |      0.251 |      -0.324 | -0.016 |  79.95  |
| SUZUKI Y       | JPN    |     210 |      11 |         0.467 |      0.078 |     -0.088 |           0 |            1 |   -2.463 | -0.01  |              3 |               5 |      0.28  |      -0.385 | -0.005 |  72.857 |
| SIEGRIST M     | SUI    |     168 |       9 |         0.464 |      0.072 |     -0.074 |           0 |            0 |   -1.665 | -0.006 |              0 |               3 |      0.164 |      -0.327 |  0.002 |  77.976 |

### Leads

| player     | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KIM C      | KOR    |      50 |       3 |         0.7   |      0.042 |     -0.042 |           0 |            0 |   -0.505 |  0.017 |              0 |               0 |      0.053 |      -0.056 |  0.007 |  85.714 |
| YOSHIDA Y  | JPN    |     210 |      11 |         0.576 |      0.032 |     -0.04  |           0 |            0 |   -0.741 |  0.002 |              0 |               0 |      0.124 |      -0.117 | -0.003 |  79.928 |
| HAMILTON B | USA    |     170 |       9 |         0.547 |      0.033 |     -0.036 |           0 |            0 |   -0.669 |  0.002 |              0 |               0 |      0.095 |      -0.104 |  0.002 |  84.789 |
| GUZIEVA J  | OAR    |     164 |       9 |         0.506 |      0.042 |     -0.04  |           0 |            0 |   -0.735 |  0.002 |              0 |               0 |      0.129 |      -0.1   |  0.005 |  82.927 |
| WEAGLE L   | CAN    |     172 |       9 |         0.5   |      0.028 |     -0.034 |           0 |            0 |   -0.754 | -0.003 |              0 |               0 |      0.13  |      -0.115 |  0.001 |  85.901 |
| KIM Y      | KOR    |     152 |       8 |         0.487 |      0.037 |     -0.035 |           0 |            0 |   -0.645 | -0     |              0 |               0 |      0.073 |      -0.111 |  0     |  83.333 |
| MA J       | CHN    |     174 |       9 |         0.483 |      0.027 |     -0.041 |           0 |            0 |   -0.637 | -0.008 |              1 |               0 |      0.142 |      -0.09  | -0.003 |  84.483 |
| KNUDSEN LA | DEN    |      34 |       2 |         0.471 |      0.031 |     -0.043 |           0 |            0 |   -0.452 | -0.008 |              0 |               0 |      0.044 |      -0.061 |  0.007 |  87.5   |
| HALSE M    | DEN    |     170 |       9 |         0.471 |      0.042 |     -0.058 |           0 |            0 |   -1.072 | -0.011 |              1 |               0 |      0.156 |      -0.179 |  0.002 |  74.412 |
| GRAY L     | GBR    |     216 |      11 |         0.468 |      0.029 |     -0.039 |           0 |            0 |   -0.927 | -0.007 |              0 |               0 |      0.134 |      -0.136 |  0     |  82.477 |
| MABERGS S  | SWE    |     218 |      11 |         0.454 |      0.031 |     -0.032 |           0 |            0 |   -0.547 | -0.003 |              0 |               1 |      0.114 |      -0.166 |  0.002 |  85.833 |
| ALBRECHT M | SUI    |     168 |       9 |         0.452 |      0.027 |     -0.046 |           0 |            0 |   -0.738 | -0.013 |              0 |               0 |      0.063 |      -0.128 | -0     |  79.613 |

