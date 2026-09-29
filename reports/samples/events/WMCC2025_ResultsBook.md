# World Men's Curling Championship (WMCC2025_ResultsBook)

Moose Jaw, SK, Canada, 2025; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Men

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| SCO    |      15 | 11-4     |               73.3 |
| CAN    |      14 | 12-2     |               65.7 |
| SUI    |      14 | 10-4     |               61.9 |
| SWE    |      13 | 8-5      |               54   |
| NOR    |      13 | 7-6      |               48.2 |
| ITA    |      12 | 5-7      |               47.5 |
| CZE    |      12 | 6-6      |               47.3 |
| CHN    |      15 | 9-6      |               45.8 |
| USA    |      12 | 4-8      |               40.4 |
| JPN    |      12 | 5-7      |               35.7 |
| GER    |      12 | 5-7      |               35.4 |
| KOR    |      12 | 1-11     |               10   |
| AUT    |      12 | 1-11     |                5.8 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| JPN    |      878 |   0.032 |    -0.03  |          0.63  |                1.926 |                   2.128 |
| GER    |      770 |   0.011 |    -0.028 |          0.638 |                2.345 |                   2.026 |
| KOR    |      782 |   0.007 |    -0.017 |          0.625 |                2.101 |                   2.035 |
| USA    |      852 |   0.006 |     0.008 |          0.608 |                1.949 |                   2.2   |
| AUT    |      738 |   0.004 |    -0.021 |          0.617 |                1.879 |                   2.085 |
| CHN    |     1050 |   0.002 |    -0.009 |          0.636 |                2.063 |                   2.238 |
| SWE    |      938 |   0.001 |     0.011 |          0.594 |                1.932 |                   2.075 |
| ITA    |      842 |  -0.005 |     0.009 |          0.6   |                1.976 |                   2.229 |
| CZE    |      872 |  -0.006 |     0.008 |          0.596 |                2.126 |                   2.034 |
| SCO    |     1052 |  -0.009 |     0.025 |          0.575 |                2.135 |                   1.991 |
| CAN    |      966 |  -0.011 |     0.025 |          0.545 |                2.116 |                   1.925 |
| NOR    |      930 |  -0.012 |    -0.003 |          0.609 |                2.251 |                   2.202 |
| SUI    |     1006 |  -0.012 |     0.007 |          0.573 |                2.356 |                   2.002 |

### Fourths

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MUSKATEWITZ M      | GER    |     193 |      12 |         0.663 |      0.262 |     -0.351 |          17 |           17 |   -6.366 |  0.055 |             19 |              17 |      0.629 |      -0.981 |  0.019 |  83.421 |
| SCHWARZ-VAN BERKEL | SUI    |     252 |      14 |         0.655 |      0.251 |     -0.224 |          22 |            8 |   -4.703 |  0.087 |             32 |              14 |      1.215 |      -0.668 |  0.004 |  87.351 |
| JACOBS B           | CAN    |     244 |      14 |         0.639 |      0.263 |     -0.218 |          21 |           11 |   -5.705 |  0.09  |             25 |              10 |      1.052 |      -0.625 |  0.008 |  91.736 |
| RETORNAZ J         | ITA    |     211 |      12 |         0.63  |      0.289 |     -0.318 |          25 |           16 |   -7.044 |  0.065 |             34 |              16 |      1.267 |      -1.294 |  0.01  |  79.881 |
| DROPKIN K          | USA    |     215 |      12 |         0.586 |      0.266 |     -0.303 |          18 |           22 |   -5.795 |  0.031 |             33 |              25 |      1.097 |      -1.532 |  0     |  79.245 |
| RAMSFJELL M        | NOR    |     234 |      13 |         0.585 |      0.281 |     -0.293 |          22 |           20 |   -5.973 |  0.043 |             26 |              22 |      1.541 |      -0.896 |  0.007 |  85.48  |
| KLIMA L            | CZE    |     219 |      12 |         0.584 |      0.277 |     -0.26  |          18 |           11 |   -5.965 |  0.054 |             33 |              20 |      1.175 |      -0.783 |  0.002 |  79.243 |
| MOUAT B            | SCO    |     263 |      15 |         0.582 |      0.262 |     -0.264 |          24 |           19 |   -6.825 |  0.042 |             39 |              27 |      1.291 |      -0.758 |  0.022 |  86.047 |
| EDIN N             | SWE    |     236 |      13 |         0.564 |      0.242 |     -0.25  |          18 |           12 |   -7.209 |  0.027 |             29 |              26 |      0.719 |      -1.005 |  0.004 |  85.622 |
| XU X               | CHN    |     269 |      15 |         0.524 |      0.288 |     -0.259 |          23 |           18 |   -7.295 |  0.028 |             33 |              25 |      1.232 |      -0.949 |  0.02  |  80.472 |
| KIM E              | KOR    |     196 |      12 |         0.495 |      0.177 |     -0.242 |           4 |           11 |   -7.452 | -0.035 |             10 |               5 |      0.509 |      -0.535 |  0.01  |  75.644 |
| YANAGISAWA R       | JPN    |     221 |      12 |         0.493 |      0.216 |     -0.293 |           8 |           20 |   -7.165 | -0.042 |             23 |              25 |      0.849 |      -0.694 |  0.02  |  80.465 |
| GENNER M           | AUT    |     186 |      12 |         0.457 |      0.229 |     -0.377 |           8 |           24 |   -9.976 | -0.1   |              8 |              27 |      0.492 |      -0.853 |  0.039 |  68.478 |
| KIM H              | KOR    |     198 |      12 |         0.455 |      0.156 |     -0.263 |           7 |           11 |   -7.448 | -0.072 |              5 |              18 |      0.385 |      -0.832 |  0.021 |  74.112 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SCHWALLER Y | SUI    |     252 |      14 |         0.607 |      0.131 |     -0.119 |           3 |            3 |   -2.539 |  0.033 |             11 |               8 |      0.416 |      -0.384 | -0.009 |  87.004 |
| HARDIE G    | SCO    |     264 |      15 |         0.568 |      0.137 |     -0.135 |           5 |            5 |   -2.803 |  0.019 |             12 |               9 |      0.701 |      -0.525 | -0.003 |  89.11  |
| CERNOVSKY M | CZE    |     220 |      12 |         0.555 |      0.131 |     -0.156 |           2 |            5 |   -3.368 |  0.003 |             12 |              13 |      0.476 |      -0.584 | -0.002 |  84.205 |
| HOWELL T    | USA    |     216 |      12 |         0.542 |      0.122 |     -0.137 |           1 |            1 |   -2.148 |  0.003 |              6 |               7 |      0.461 |      -0.321 | -0     |  82.674 |
| KENNEDY M   | CAN    |     244 |      14 |         0.537 |      0.14  |     -0.122 |           2 |            4 |   -3.546 |  0.019 |             10 |               4 |      0.438 |      -0.63  | -0.009 |  90.779 |
| ERIKSSON O  | SWE    |     236 |      13 |         0.53  |      0.126 |     -0.118 |           3 |            2 |   -2.482 |  0.011 |              8 |               5 |      0.413 |      -0.407 | -0.01  |  87.606 |
| KAPP B      | GER    |     194 |      12 |         0.521 |      0.149 |     -0.134 |           2 |            1 |   -2.304 |  0.014 |              3 |               4 |      0.264 |      -0.327 |  0.009 |  84.794 |
| SESAKER M   | NOR    |     234 |      13 |         0.504 |      0.117 |     -0.143 |           1 |            5 |   -3.345 | -0.012 |              4 |              11 |      0.287 |      -0.394 | -0.007 |  85.15  |
| MOSANER A   | ITA    |     212 |      12 |         0.486 |      0.141 |     -0.161 |           5 |            7 |   -3.087 | -0.014 |              3 |              11 |      0.454 |      -0.58  | -0.005 |  84.788 |
| FEI X       | CHN    |     270 |      15 |         0.43  |      0.142 |     -0.13  |           3 |            2 |   -2.469 | -0.013 |             12 |               7 |      0.508 |      -0.398 |  0.001 |  84.259 |
| YAMAGUCHI T | JPN    |     222 |      12 |         0.428 |      0.129 |     -0.145 |           1 |            2 |   -2.771 | -0.028 |              7 |               7 |      0.406 |      -0.375 |  0.016 |  80.405 |
| BACKOFEN J  | AUT    |     186 |      12 |         0.398 |      0.122 |     -0.136 |           2 |            2 |   -2.563 | -0.033 |              3 |               3 |      0.264 |      -0.339 |  0.017 |  74.462 |

### Seconds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| GALLANT B    | CAN    |     244 |      14 |         0.566 |      0.064 |     -0.086 |           0 |            1 |   -2.291 | -0.001 |              3 |               3 |      0.324 |      -0.345 | -0.01  |  91.598 |
| WRANAA R     | SWE    |     236 |      13 |         0.525 |      0.068 |     -0.076 |           0 |            1 |   -1.607 | -0     |              0 |               1 |      0.222 |      -0.222 | -0.001 |  90.36  |
| ARMAN S      | ITA    |     212 |      12 |         0.495 |      0.08  |     -0.078 |           0 |            1 |   -1.713 | -0     |              3 |               2 |      0.282 |      -0.282 | -0.004 |  86.137 |
| MICHEL S     | SUI    |     252 |      14 |         0.448 |      0.07  |     -0.073 |           0 |            0 |   -1.469 | -0.009 |              1 |               1 |      0.251 |      -0.217 | -0.011 |  89     |
| KIM C        | KOR    |     134 |       9 |         0.44  |      0.12  |     -0.149 |           1 |            4 |   -2.954 | -0.031 |              1 |               6 |      0.212 |      -0.479 |  0.022 |  80.97  |
| MESSENZEHL F | GER    |     194 |      12 |         0.438 |      0.074 |     -0.101 |           0 |            0 |   -1.773 | -0.025 |              1 |               1 |      0.228 |      -0.197 |  0.003 |  80.959 |
| STOPERA A    | USA    |     216 |      12 |         0.431 |      0.083 |     -0.099 |           0 |            1 |   -2.104 | -0.021 |              1 |               2 |      0.238 |      -0.248 |  0.002 |  82.06  |
| RAMSFJELL B  | NOR    |     234 |      13 |         0.423 |      0.07  |     -0.088 |           0 |            1 |   -1.813 | -0.021 |              2 |               1 |      0.264 |      -0.246 |  0.004 |  86.966 |
| WANG Z       | CHN    |     270 |      15 |         0.415 |      0.063 |     -0.084 |           0 |            0 |   -1.709 | -0.023 |              1 |               2 |      0.206 |      -0.267 | -0.001 |  83.55  |
| LAMMIE B     | SCO    |     264 |      15 |         0.409 |      0.071 |     -0.084 |           0 |            1 |   -1.893 | -0.021 |              1 |               3 |      0.222 |      -0.301 | -0.005 |  87.689 |
| USUI S       | JPN    |     222 |      12 |         0.374 |      0.071 |     -0.097 |           0 |            0 |   -1.36  | -0.034 |              1 |               1 |      0.225 |      -0.239 |  0.001 |  80.293 |
| JURIK M      | CZE    |     218 |      12 |         0.372 |      0.068 |     -0.088 |           0 |            1 |   -2.098 | -0.03  |              2 |               4 |      0.249 |      -0.381 | -0.001 |  78.67  |
| HOFER M      | AUT    |     118 |       8 |         0.339 |      0.064 |     -0.092 |           0 |            0 |   -1.753 | -0.039 |              0 |               1 |      0.088 |      -0.175 |  0.013 |  78.39  |

### Leads

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SUNDGREN C         | SWE    |     236 |      13 |         0.623 |      0.027 |     -0.045 |           0 |            0 |   -0.635 |  0     |              0 |               0 |      0.085 |      -0.11  | -0.001 |  93.803 |
| HEBERT B           | CAN    |     236 |      14 |         0.606 |      0.026 |     -0.042 |           0 |            0 |   -0.697 | -0.001 |              0 |               0 |      0.09  |      -0.082 |  0.001 |  95.233 |
| GIOVANELLA M       | ITA    |     212 |      12 |         0.59  |      0.029 |     -0.048 |           0 |            0 |   -0.703 | -0.003 |              1 |               0 |      0.178 |      -0.142 | -0.001 |  89.387 |
| SCHEUERL J         | GER    |     194 |      12 |         0.588 |      0.031 |     -0.048 |           0 |            0 |   -0.684 | -0.002 |              0 |               0 |      0.093 |      -0.101 | -0     |  89.896 |
| MCMILLAN H         | SCO    |     264 |      15 |         0.572 |      0.029 |     -0.043 |           0 |            0 |   -0.687 | -0.002 |              1 |               0 |      0.141 |      -0.131 | -0     |  90.152 |
| MAVEC F            | AUT    |     112 |       7 |         0.536 |      0.035 |     -0.046 |           0 |            0 |   -0.515 | -0.002 |              0 |               0 |      0.072 |      -0.079 | -0.001 |  83.259 |
| NEPSTAD G          | NOR    |     234 |      13 |         0.53  |      0.032 |     -0.044 |           0 |            0 |   -0.76  | -0.004 |              0 |               0 |      0.109 |      -0.115 |  0.003 |  91.631 |
| LACHAT-COUCHEPIN P | SUI    |     250 |      14 |         0.516 |      0.029 |     -0.047 |           0 |            0 |   -0.7   | -0.008 |              0 |               0 |      0.087 |      -0.104 |  0     |  90.423 |
| KOIZUMI S          | JPN    |     222 |      12 |         0.514 |      0.03  |     -0.05  |           0 |            0 |   -0.662 | -0.009 |              0 |               0 |      0.076 |      -0.174 |  0.003 |  87.67  |
| KIM J              | KOR    |      82 |       9 |         0.512 |      0.034 |     -0.049 |           0 |            0 |   -0.697 | -0.007 |              0 |               0 |      0.05  |      -0.109 |  0.001 |  77.439 |
| FENNER M           | USA    |     216 |      12 |         0.505 |      0.023 |     -0.052 |           0 |            0 |   -0.805 | -0.014 |              0 |               0 |      0.083 |      -0.132 |  0     |  89.12  |
| KLIPA L            | CZE    |     220 |      12 |         0.495 |      0.026 |     -0.046 |           0 |            0 |   -0.872 | -0.01  |              0 |               1 |      0.065 |      -0.179 |  0.002 |  90.909 |
| PYO J              | KOR    |     182 |      12 |         0.478 |      0.041 |     -0.078 |           0 |            1 |   -1.672 | -0.021 |              0 |               0 |      0.133 |      -0.188 |  0.004 |  80.22  |
| LI Z               | CHN    |     270 |      15 |         0.478 |      0.029 |     -0.049 |           0 |            0 |   -0.909 | -0.012 |              0 |               0 |      0.071 |      -0.139 |  0.004 |  88.889 |
| REICHEL M          | AUT    |     142 |       9 |         0.437 |      0.04  |     -0.09  |           0 |            0 |   -1.458 | -0.033 |              0 |               2 |      0.093 |      -0.249 |  0.004 |  82.57  |

