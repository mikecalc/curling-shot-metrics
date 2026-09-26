# World Men's Curling Championship (WMCC2025_ResultsBook)

Moose Jaw, SK, Canada, 2025; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Men

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| SCO    |      15 | 11-4     |               75.1 |
| CAN    |      14 | 12-2     |               67.5 |
| SUI    |      14 | 10-4     |               66.4 |
| SWE    |      13 | 8-5      |               53.9 |
| CZE    |      12 | 6-6      |               51.9 |
| ITA    |      12 | 5-7      |               49   |
| NOR    |      13 | 7-6      |               48.2 |
| CHN    |      15 | 9-6      |               44.7 |
| USA    |      12 | 4-8      |               40.9 |
| GER    |      12 | 5-7      |               35.1 |
| JPN    |      12 | 5-7      |               33.9 |
| KOR    |      12 | 1-11     |                7.9 |
| AUT    |      12 | 1-11     |                6.9 |

### Build or address

How each team played the stones, in rock potential (descriptive, not a ranking): `build` is how much a stone added to the team's own potential and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' potential together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| GER    |      770 |   0.018 |    -0.015 |          0.76  |                2.873 |                   2.64  |
| NOR    |      930 |   0.012 |    -0.009 |          0.728 |                2.815 |                   2.778 |
| CHN    |     1050 |   0.007 |    -0.013 |          0.748 |                2.463 |                   2.823 |
| AUT    |      738 |   0.007 |     0     |          0.737 |                2.638 |                   2.366 |
| KOR    |      782 |   0.006 |    -0.008 |          0.756 |                2.675 |                   2.354 |
| SWE    |      938 |   0.002 |     0     |          0.729 |                2.341 |                   2.44  |
| USA    |      852 |   0.002 |     0.002 |          0.735 |                2.54  |                   2.528 |
| JPN    |      878 |   0.001 |     0.008 |          0.723 |                2.216 |                   2.478 |
| SUI    |     1006 |  -0.001 |    -0.003 |          0.709 |                2.795 |                   2.572 |
| CZE    |      872 |  -0.002 |    -0.007 |          0.719 |                2.602 |                   2.692 |
| ITA    |      842 |  -0.004 |    -0.006 |          0.729 |                2.371 |                   2.654 |
| CAN    |      966 |  -0.012 |     0.02  |          0.696 |                2.552 |                   2.545 |
| SCO    |     1052 |  -0.027 |     0.024 |          0.665 |                2.605 |                   2.405 |

### Fourths

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| JACOBS B           | CAN    |     244 |      14 |         0.668 |      0.282 |     -0.233 |          22 |           12 |   -5.734 |  0.111 |             35 |              12 |      1.119 |      -0.691 |  0.017 |  91.736 |
| RETORNAZ J         | ITA    |     211 |      12 |         0.664 |      0.293 |     -0.349 |          24 |           18 |   -6.72  |  0.077 |             35 |              19 |      1.285 |      -1.286 |  0.018 |  79.881 |
| SCHWARZ-VAN BERKEL | SUI    |     252 |      14 |         0.655 |      0.277 |     -0.225 |          29 |           10 |   -4.311 |  0.104 |             34 |              14 |      1.267 |      -0.672 |  0.011 |  87.351 |
| MUSKATEWITZ M      | GER    |     193 |      12 |         0.648 |      0.281 |     -0.324 |          24 |           15 |   -6.539 |  0.068 |             21 |              16 |      0.638 |      -1.026 |  0.023 |  83.421 |
| RAMSFJELL M        | NOR    |     234 |      13 |         0.615 |      0.278 |     -0.302 |          20 |           20 |   -6.187 |  0.055 |             29 |              20 |      1.461 |      -0.995 |  0.019 |  85.48  |
| KLIMA L            | CZE    |     219 |      12 |         0.598 |      0.295 |     -0.286 |          24 |           16 |   -6.002 |  0.061 |             38 |              24 |      1.207 |      -0.798 |  0.003 |  79.243 |
| MOUAT B            | SCO    |     263 |      15 |         0.597 |      0.276 |     -0.268 |          30 |           18 |   -6.391 |  0.056 |             44 |              25 |      1.266 |      -0.739 |  0.032 |  86.047 |
| DROPKIN K          | USA    |     215 |      12 |         0.591 |      0.276 |     -0.309 |          19 |           18 |   -5.813 |  0.037 |             31 |              27 |      1.079 |      -1.51  |  0.013 |  79.245 |
| EDIN N             | SWE    |     236 |      13 |         0.585 |      0.249 |     -0.26  |          18 |           13 |   -7.311 |  0.038 |             31 |              22 |      0.816 |      -1.024 |  0.012 |  85.622 |
| XU X               | CHN    |     269 |      15 |         0.558 |      0.282 |     -0.269 |          24 |           19 |   -7.549 |  0.038 |             38 |              20 |      1.221 |      -1.035 |  0.018 |  80.472 |
| YANAGISAWA R       | JPN    |     221 |      12 |         0.516 |      0.208 |     -0.289 |           8 |           21 |   -6.889 | -0.033 |             20 |              26 |      0.882 |      -0.708 |  0.015 |  80.465 |
| KIM E              | KOR    |     196 |      12 |         0.459 |      0.173 |     -0.215 |           5 |           10 |   -6.856 | -0.037 |              9 |               4 |      0.508 |      -0.501 |  0.012 |  75.644 |
| GENNER M           | AUT    |     186 |      12 |         0.452 |      0.236 |     -0.387 |          10 |           27 |  -10.232 | -0.106 |             14 |              30 |      0.482 |      -0.841 |  0.054 |  68.478 |
| KIM H              | KOR    |     198 |      12 |         0.399 |      0.166 |     -0.226 |           6 |           14 |   -7.492 | -0.069 |              6 |              17 |      0.37  |      -0.865 |  0.024 |  74.112 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SCHWALLER Y | SUI    |     252 |      14 |         0.575 |      0.119 |     -0.11  |           6 |            2 |   -2.396 |  0.022 |              6 |               4 |      0.465 |      -0.326 | -0.002 |  87.004 |
| CERNOVSKY M | CZE    |     220 |      12 |         0.568 |      0.129 |     -0.146 |           2 |            4 |   -3.31  |  0.01  |             15 |              12 |      0.543 |      -0.583 |  0.003 |  84.205 |
| KENNEDY M   | CAN    |     244 |      14 |         0.557 |      0.115 |     -0.122 |           3 |            4 |   -3.374 |  0.01  |              8 |               6 |      0.348 |      -0.631 | -0     |  90.779 |
| HARDIE G    | SCO    |     264 |      15 |         0.553 |      0.124 |     -0.121 |           4 |            5 |   -2.759 |  0.014 |             14 |               8 |      0.636 |      -0.488 | -0.001 |  89.11  |
| ERIKSSON O  | SWE    |     236 |      13 |         0.513 |      0.106 |     -0.115 |           0 |            2 |   -2.634 | -0.002 |              8 |               6 |      0.377 |      -0.414 | -0.005 |  87.606 |
| KAPP B      | GER    |     194 |      12 |         0.495 |      0.13  |     -0.129 |           1 |            2 |   -2.262 | -0.001 |              3 |               4 |      0.286 |      -0.353 |  0.009 |  84.794 |
| HOWELL T    | USA    |     216 |      12 |         0.491 |      0.118 |     -0.137 |           3 |            2 |   -2.325 | -0.012 |              8 |               9 |      0.394 |      -0.327 |  0.004 |  82.674 |
| SESAKER M   | NOR    |     234 |      13 |         0.483 |      0.103 |     -0.132 |           0 |            5 |   -2.941 | -0.019 |              3 |               6 |      0.264 |      -0.382 | -0.007 |  85.15  |
| MOSANER A   | ITA    |     212 |      12 |         0.481 |      0.114 |     -0.16  |           3 |            5 |   -3.045 | -0.028 |              2 |              13 |      0.52  |      -0.499 | -0.001 |  84.788 |
| YAMAGUCHI T | JPN    |     222 |      12 |         0.464 |      0.103 |     -0.144 |           0 |            3 |   -3.369 | -0.03  |              9 |               7 |      0.398 |      -0.413 |  0.012 |  80.405 |
| FEI X       | CHN    |     270 |      15 |         0.452 |      0.117 |     -0.126 |           0 |            2 |   -2.697 | -0.016 |              6 |               6 |      0.319 |      -0.337 |  0.004 |  84.259 |
| BACKOFEN J  | AUT    |     186 |      12 |         0.409 |      0.109 |     -0.141 |           1 |            2 |   -2.839 | -0.039 |              1 |               6 |      0.244 |      -0.384 |  0.017 |  74.462 |

### Seconds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WRANAA R     | SWE    |     236 |      13 |         0.538 |      0.056 |     -0.077 |           0 |            0 |   -1.388 | -0.005 |              1 |               1 |      0.196 |      -0.201 | -0.003 |  90.36  |
| ARMAN S      | ITA    |     212 |      12 |         0.505 |      0.055 |     -0.087 |           0 |            1 |   -1.742 | -0.015 |              1 |               1 |      0.199 |      -0.315 | -0.002 |  86.137 |
| GALLANT B    | CAN    |     244 |      14 |         0.467 |      0.06  |     -0.065 |           0 |            1 |   -1.899 | -0.006 |              3 |               2 |      0.238 |      -0.275 | -0.007 |  91.598 |
| RAMSFJELL B  | NOR    |     234 |      13 |         0.423 |      0.052 |     -0.087 |           0 |            1 |   -1.649 | -0.028 |              1 |               1 |      0.209 |      -0.242 |  0.002 |  86.966 |
| MESSENZEHL F | GER    |     194 |      12 |         0.412 |      0.059 |     -0.087 |           0 |            0 |   -1.597 | -0.027 |              1 |               0 |      0.175 |      -0.176 |  0.003 |  80.959 |
| LAMMIE B     | SCO    |     264 |      15 |         0.409 |      0.06  |     -0.078 |           0 |            0 |   -1.592 | -0.022 |              1 |               1 |      0.227 |      -0.24  | -0.005 |  87.689 |
| JURIK M      | CZE    |     218 |      12 |         0.408 |      0.044 |     -0.088 |           0 |            0 |   -1.552 | -0.034 |              0 |               3 |      0.177 |      -0.285 | -0.005 |  78.67  |
| MICHEL S     | SUI    |     252 |      14 |         0.405 |      0.056 |     -0.068 |           0 |            0 |   -1.39  | -0.018 |              1 |               1 |      0.192 |      -0.185 | -0.008 |  89     |
| KIM C        | KOR    |     134 |       9 |         0.403 |      0.087 |     -0.113 |           0 |            1 |   -2.311 | -0.032 |              0 |               4 |      0.146 |      -0.38  |  0.015 |  80.97  |
| HOFER M      | AUT    |     118 |       8 |         0.398 |      0.07  |     -0.079 |           0 |            0 |   -1.364 | -0.02  |              0 |               0 |      0.137 |      -0.155 |  0.007 |  78.39  |
| STOPERA A    | USA    |     216 |      12 |         0.366 |      0.074 |     -0.08  |           0 |            0 |   -1.383 | -0.024 |              1 |               1 |      0.259 |      -0.209 | -0.002 |  82.06  |
| WANG Z       | CHN    |     270 |      15 |         0.363 |      0.048 |     -0.078 |           0 |            0 |   -1.493 | -0.032 |              1 |               2 |      0.197 |      -0.271 | -0.002 |  83.55  |
| USUI S       | JPN    |     222 |      12 |         0.333 |      0.053 |     -0.085 |           0 |            0 |   -1.471 | -0.039 |              2 |               1 |      0.201 |      -0.245 | -0.002 |  80.293 |

### Leads

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SUNDGREN C         | SWE    |     236 |      13 |         0.606 |      0.024 |     -0.032 |           0 |            0 |   -0.568 |  0.002 |              0 |               0 |      0.073 |      -0.09  | -0.002 |  93.803 |
| MCMILLAN H         | SCO    |     264 |      15 |         0.602 |      0.023 |     -0.037 |           0 |            0 |   -0.612 | -0.001 |              0 |               0 |      0.09  |      -0.106 | -0.001 |  90.152 |
| HEBERT B           | CAN    |     236 |      14 |         0.597 |      0.019 |     -0.037 |           0 |            0 |   -0.623 | -0.004 |              0 |               0 |      0.065 |      -0.079 | -0.001 |  95.233 |
| SCHEUERL J         | GER    |     194 |      12 |         0.593 |      0.023 |     -0.039 |           0 |            0 |   -0.687 | -0.002 |              0 |               0 |      0.067 |      -0.096 | -0.002 |  89.896 |
| GIOVANELLA M       | ITA    |     212 |      12 |         0.552 |      0.021 |     -0.037 |           0 |            0 |   -0.65  | -0.005 |              1 |               0 |      0.102 |      -0.111 | -0.002 |  89.387 |
| KLIPA L            | CZE    |     220 |      12 |         0.55  |      0.024 |     -0.039 |           0 |            0 |   -0.756 | -0.004 |              0 |               0 |      0.052 |      -0.139 | -0     |  90.909 |
| KIM J              | KOR    |      82 |       9 |         0.524 |      0.02  |     -0.04  |           0 |            0 |   -0.521 | -0.009 |              0 |               0 |      0.04  |      -0.093 |  0.001 |  77.439 |
| NEPSTAD G          | NOR    |     234 |      13 |         0.517 |      0.027 |     -0.033 |           0 |            0 |   -0.75  | -0.002 |              0 |               0 |      0.09  |      -0.118 |  0     |  91.631 |
| LACHAT-COUCHEPIN P | SUI    |     250 |      14 |         0.512 |      0.023 |     -0.038 |           0 |            0 |   -0.791 | -0.007 |              0 |               0 |      0.057 |      -0.097 | -0.002 |  90.423 |
| KOIZUMI S          | JPN    |     222 |      12 |         0.509 |      0.025 |     -0.04  |           0 |            0 |   -0.601 | -0.007 |              0 |               0 |      0.062 |      -0.156 |  0.004 |  87.67  |
| MAVEC F            | AUT    |     112 |       7 |         0.5   |      0.027 |     -0.031 |           0 |            0 |   -0.551 | -0.002 |              0 |               0 |      0.057 |      -0.08  | -0     |  83.259 |
| FENNER M           | USA    |     216 |      12 |         0.491 |      0.022 |     -0.042 |           0 |            0 |   -0.664 | -0.011 |              0 |               0 |      0.06  |      -0.116 | -0.001 |  89.12  |
| LI Z               | CHN    |     270 |      15 |         0.452 |      0.024 |     -0.038 |           0 |            0 |   -0.861 | -0.01  |              0 |               0 |      0.057 |      -0.133 |  0.003 |  88.889 |
| PYO J              | KOR    |     182 |      12 |         0.434 |      0.034 |     -0.065 |           0 |            1 |   -1.555 | -0.022 |              0 |               0 |      0.141 |      -0.202 |  0.001 |  80.22  |
| REICHEL M          | AUT    |     142 |       9 |         0.415 |      0.038 |     -0.075 |           0 |            0 |   -1.541 | -0.028 |              0 |               2 |      0.077 |      -0.231 |  0.001 |  82.57  |

