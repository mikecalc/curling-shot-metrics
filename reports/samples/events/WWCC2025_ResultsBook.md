# World Women's Curling Championship (WWCC2025_ResultsBook)

Uijeongbu, Korea, 2025; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Women

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| KOR    |      14 | 10-4     |               84.9 |
| SUI    |      14 | 12-2     |               74.7 |
| CAN    |      15 | 13-2     |               68.6 |
| SWE    |      13 | 9-4      |               67.8 |
| SCO    |      13 | 7-6      |               66.1 |
| CHN    |      15 | 9-6      |               57   |
| USA    |      12 | 3-9      |               50.9 |
| DEN    |      12 | 5-7      |               45.5 |
| NOR    |      12 | 5-7      |               45.1 |
| JPN    |      12 | 4-8      |               42.7 |
| ITA    |      12 | 4-8      |               35.1 |
| TUR    |      12 | 3-9      |               34.3 |
| LTU    |      12 | 0-12     |              -13.8 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| DEN    |      841 |   0.026 |    -0.013 |          0.639 |                2.415 |                   2.099 |
| KOR    |     1095 |   0.017 |     0.016 |          0.585 |                2.049 |                   2.023 |
| ITA    |      857 |   0.01  |    -0.02  |          0.618 |                2.332 |                   2.067 |
| JPN    |      864 |   0.01  |    -0.007 |          0.631 |                2.041 |                   1.851 |
| CHN    |     1103 |   0.005 |     0     |          0.61  |                1.717 |                   2.159 |
| TUR    |      837 |  -0     |    -0.022 |          0.611 |                1.907 |                   2.008 |
| NOR    |      869 |  -0.004 |     0.004 |          0.58  |                1.908 |                   1.921 |
| SCO    |      953 |  -0.006 |     0.003 |          0.588 |                1.827 |                   2.074 |
| CAN    |     1070 |  -0.008 |     0.022 |          0.573 |                2.145 |                   2.104 |
| USA    |      904 |  -0.01  |     0.004 |          0.587 |                2.105 |                   2.17  |
| SUI    |     1065 |  -0.012 |     0.034 |          0.543 |                2.138 |                   1.799 |
| LTU    |      720 |  -0.013 |    -0.044 |          0.614 |                1.99  |                   2.219 |
| SWE    |      985 |  -0.015 |    -0.004 |          0.596 |                2.075 |                   2.103 |

### Fourths

| player         | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:---------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HOMAN R        | CAN    |     268 |      15 |         0.627 |      0.304 |     -0.228 |          27 |           10 |   -5.241 |  0.105 |             37 |              18 |      1.36  |      -1.153 | -0.011 |  87.643 |
| GIM E          | KOR    |     277 |      14 |         0.625 |      0.256 |     -0.28  |          26 |           21 |   -6.768 |  0.055 |             48 |              23 |      1.26  |      -1.085 |  0.02  |  85.31  |
| HASSELBORG A   | SWE    |     228 |      12 |         0.61  |      0.272 |     -0.25  |          24 |           11 |   -6.243 |  0.068 |             37 |              18 |      1.052 |      -0.883 |  0.013 |  87.058 |
| DUPONT M       | DEN    |     212 |      12 |         0.604 |      0.243 |     -0.342 |          12 |           20 |   -7.432 |  0.011 |             27 |              28 |      0.994 |      -0.97  |  0.02  |  80.687 |
| YOSHIMURA S    | JPN    |     218 |      12 |         0.596 |      0.277 |     -0.389 |          21 |           24 |   -9.9   |  0.008 |             28 |              23 |      0.837 |      -1.251 |  0.008 |  78.111 |
| WANG R         | CHN    |     276 |      15 |         0.569 |      0.232 |     -0.212 |          18 |           13 |   -5.536 |  0.041 |             26 |              17 |      2.254 |      -1.126 |  0.007 |  84.455 |
| PAETZ A        | SUI    |     270 |      14 |         0.559 |      0.226 |     -0.234 |          18 |           18 |   -6.232 |  0.024 |             34 |              28 |      1.776 |      -1.201 |  0.014 |  85.502 |
| CONSTANTINI S  | ITA    |     216 |      12 |         0.519 |      0.297 |     -0.289 |          22 |           21 |   -7.438 |  0.015 |             24 |              21 |      0.886 |      -1.503 |  0.021 |  78.037 |
| PETERSON TAB   | USA    |     227 |      12 |         0.511 |      0.29  |     -0.263 |          19 |           20 |   -5.415 |  0.02  |             30 |              31 |      1.059 |      -1.01  |  0.009 |  78.111 |
| MORRISON R     | SCO    |     242 |      13 |         0.508 |      0.292 |     -0.242 |          17 |           19 |   -6.368 |  0.03  |             38 |              24 |      1.406 |      -0.961 |  0.004 |  83.996 |
| SKASLIEN K     | NOR    |     222 |      12 |         0.495 |      0.251 |     -0.299 |          12 |           16 |   -8.608 | -0.026 |             28 |              32 |      1.554 |      -1.444 |  0.011 |  76.239 |
| YILDIZ D       | TUR    |     212 |      12 |         0.462 |      0.29  |     -0.29  |          18 |           20 |   -7.203 | -0.022 |             24 |              27 |      0.847 |      -0.874 |  0.013 |  75.478 |
| PAULAUSKAITE V | LTU    |     182 |      12 |         0.396 |      0.298 |     -0.396 |          17 |           31 |   -8.608 | -0.122 |             13 |              26 |      0.85  |      -0.78  |  0.043 |  65     |

### Thirds

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| FLEURY T          | CAN    |     270 |      15 |         0.567 |      0.163 |     -0.118 |           8 |            2 |   -2.366 |  0.041 |             19 |               5 |      0.411 |      -0.312 | -0.016 |  88.981 |
| ONODERA K         | JPN    |     218 |      12 |         0.537 |      0.141 |     -0.121 |           3 |            3 |   -2.694 |  0.02  |             14 |               4 |      0.485 |      -0.402 | -0.006 |  83.945 |
| TIRINZONI S       | SUI    |     270 |      14 |         0.519 |      0.144 |     -0.143 |           3 |            5 |   -2.802 |  0.006 |             17 |              19 |      0.641 |      -0.522 |  0.003 |  86.481 |
| HALSE M           | DEN    |     212 |      12 |         0.505 |      0.137 |     -0.14  |           5 |            4 |   -3.324 |  0     |             10 |               7 |      0.443 |      -0.439 |  0.008 |  81.368 |
| MCMANUS S         | SWE    |     247 |      13 |         0.502 |      0.141 |     -0.138 |           2 |            5 |   -3.895 |  0.002 |              8 |              11 |      0.334 |      -0.529 | -0.007 |  87.146 |
| ZARDINI LACEDELLI | ITA    |     216 |      12 |         0.5   |      0.152 |     -0.152 |           3 |            2 |   -3.162 |  0     |              9 |               9 |      0.441 |      -0.521 |  0.003 |  79.63  |
| POLAT O           | TUR    |     212 |      12 |         0.495 |      0.131 |     -0.126 |           4 |            1 |   -2.308 |  0.001 |              8 |               8 |      0.486 |      -0.307 |  0.009 |  81.132 |
| ROERVIK M         | NOR    |     222 |      12 |         0.491 |      0.13  |     -0.125 |           2 |            3 |   -2.739 |  0     |              6 |              11 |      0.496 |      -0.454 | -0.001 |  84.685 |
| THIESSE C         | USA    |     228 |      12 |         0.487 |      0.115 |     -0.127 |           1 |            6 |   -3.263 | -0.009 |              8 |              10 |      0.384 |      -0.442 |  0.016 |  81.14  |
| DODDS J           | SCO    |     242 |      13 |         0.483 |      0.13  |     -0.13  |           4 |            5 |   -3.376 | -0.004 |             13 |              11 |      0.442 |      -0.546 |  0     |  84.607 |
| KIM M             | KOR    |     278 |      14 |         0.482 |      0.149 |     -0.126 |           6 |            4 |   -2.751 |  0.006 |             14 |              12 |      0.542 |      -0.481 | -0.002 |  85.162 |
| HAN Y             | CHN    |     282 |      15 |         0.436 |      0.127 |     -0.112 |           3 |            1 |   -2.625 | -0.008 |              6 |               4 |      0.346 |      -0.329 |  0.002 |  85.106 |
| DVOJEGLAZOVA O    | LTU    |     182 |      12 |         0.308 |      0.156 |     -0.199 |           4 |            8 |   -3.571 | -0.09  |              5 |              15 |      0.331 |      -0.489 |  0.019 |  62.017 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KARAMAN I        | TUR    |      42 |       3 |         0.643 |      0.07  |     -0.06  |           0 |            0 |   -0.585 |  0.024 |              0 |               0 |      0.063 |      -0.064 | -0.006 |  77.976 |
| KNOCHENHAUER A   | SWE    |     248 |      13 |         0.54  |      0.085 |     -0.094 |           2 |            0 |   -2.103 |  0.002 |              2 |               5 |      0.313 |      -0.369 | -0.005 |  85.081 |
| KIM S            | KOR    |     244 |      12 |         0.529 |      0.087 |     -0.093 |           0 |            1 |   -2.02  |  0.002 |              6 |               5 |      0.357 |      -0.358 | -0.002 |  84.529 |
| SINCLAIR S       | SCO    |     228 |      12 |         0.504 |      0.07  |     -0.076 |           0 |            0 |   -1.894 | -0.002 |              2 |               2 |      0.278 |      -0.262 | -0.002 |  87.39  |
| MISKEW E         | CAN    |     270 |      15 |         0.496 |      0.086 |     -0.087 |           0 |            0 |   -1.59  | -0.001 |              3 |               1 |      0.291 |      -0.238 | -0.011 |  87.22  |
| KOTANI Y         | JPN    |     198 |      11 |         0.46  |      0.078 |     -0.081 |           0 |            0 |   -1.538 | -0.008 |              3 |               1 |      0.28  |      -0.206 | -0.004 |  86.111 |
| DONG Z           | CHN    |     272 |      15 |         0.46  |      0.079 |     -0.076 |           0 |            0 |   -1.644 | -0.004 |              3 |               2 |      0.257 |      -0.241 | -0.005 |  85.662 |
| MATHIS E         | ITA    |     216 |      12 |         0.458 |      0.073 |     -0.079 |           0 |            0 |   -1.289 | -0.009 |              2 |               2 |      0.256 |      -0.216 |  0     |  84.144 |
| HASLEV NORDBYE M | NOR    |     202 |      11 |         0.455 |      0.077 |     -0.085 |           0 |            0 |   -1.666 | -0.011 |              1 |               2 |      0.272 |      -0.246 |  0.006 |  85     |
| PETERSON TAR     | USA    |     194 |      10 |         0.438 |      0.087 |     -0.119 |           0 |            2 |   -2.41  | -0.029 |              5 |               6 |      0.333 |      -0.437 |  0.001 |  78.737 |
| HOLTERMANN J     | DEN    |     144 |       8 |         0.438 |      0.097 |     -0.091 |           1 |            0 |   -1.61  | -0.009 |              3 |               1 |      0.264 |      -0.249 |  0.003 |  81.076 |
| HOWALD C         | SUI    |     262 |      14 |         0.424 |      0.077 |     -0.094 |           0 |            1 |   -2.146 | -0.021 |              4 |               3 |      0.37  |      -0.339 | -0.003 |  86.442 |
| PERSINGER V      | USA    |      34 |       2 |         0.412 |      0.078 |     -0.094 |           0 |            0 |   -1.004 | -0.023 |              0 |               0 |      0.072 |      -0.152 |  0.02  |  75     |
| CALIKUSU IS      | TUR    |     170 |      10 |         0.347 |      0.08  |     -0.1   |           0 |            2 |   -2.066 | -0.038 |              0 |               2 |      0.152 |      -0.299 |  0.006 |  70.882 |
| KIUDYTE M        | LTU    |     182 |      12 |         0.302 |      0.084 |     -0.118 |           0 |            1 |   -1.931 | -0.057 |              0 |               2 |      0.136 |      -0.286 |  0.016 |  67.445 |

### Leads

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HELDIN J         | SWE    |      36 |       2 |         0.611 |      0.028 |     -0.059 |           0 |            0 |   -0.502 | -0.006 |              0 |               0 |      0.053 |      -0.064 |  0.003 |  81.25  |
| WILKES S         | CAN    |     270 |      15 |         0.604 |      0.037 |     -0.042 |           0 |            0 |   -0.871 |  0.006 |              1 |               0 |      0.138 |      -0.156 | -0.001 |  92.193 |
| MABERGS S        | SWE    |     232 |      12 |         0.569 |      0.031 |     -0.047 |           0 |            0 |   -1.214 | -0.002 |              0 |               2 |      0.122 |      -0.201 | -0.002 |  90.217 |
| SEOL Y           | KOR    |     312 |      14 |         0.542 |      0.036 |     -0.052 |           0 |            0 |   -1.234 | -0.004 |              1 |               1 |      0.168 |      -0.2   | -0.001 |  87.379 |
| LARSEN M         | DEN    |      84 |       5 |         0.536 |      0.032 |     -0.048 |           0 |            0 |   -0.603 | -0.005 |              0 |               0 |      0.08  |      -0.093 |  0.005 |  80.655 |
| OHMIYA A         | JPN    |     218 |      12 |         0.532 |      0.033 |     -0.041 |           0 |            0 |   -0.667 | -0.001 |              0 |               0 |      0.122 |      -0.118 |  0.002 |  91.514 |
| ANDERSON-HEIDE T | USA    |     228 |      12 |         0.531 |      0.028 |     -0.051 |           0 |            0 |   -1.048 | -0.009 |              0 |               0 |      0.118 |      -0.137 |  0.001 |  86.513 |
| JACKSON S        | SCO    |     242 |      13 |         0.5   |      0.029 |     -0.047 |           0 |            0 |   -0.72  | -0.009 |              0 |               0 |      0.124 |      -0.133 |  0.006 |  89.375 |
| SENGUL B         | TUR    |     212 |      12 |         0.5   |      0.036 |     -0.05  |           0 |            0 |   -0.736 | -0.007 |              0 |               0 |      0.116 |      -0.114 |  0.004 |  85.167 |
| BLAZIENE R       | LTU    |     182 |      12 |         0.5   |      0.025 |     -0.066 |           0 |            0 |   -1.08  | -0.02  |              0 |               0 |      0.065 |      -0.132 |  0.005 |  72.527 |
| ROMEI A          | ITA    |     202 |      11 |         0.495 |      0.03  |     -0.051 |           0 |            0 |   -0.787 | -0.011 |              0 |               0 |      0.13  |      -0.129 | -0     |  84.53  |
| DUPONT D         | DEN    |     196 |      11 |         0.49  |      0.042 |     -0.059 |           0 |            0 |   -1.025 | -0.009 |              1 |               1 |      0.156 |      -0.19  |  0.003 |  87.436 |
| FORBREGD I       | NOR    |      78 |       4 |         0.436 |      0.044 |     -0.065 |           0 |            0 |   -0.984 | -0.018 |              0 |               0 |      0.101 |      -0.132 |  0.001 |  85.256 |
| WITSCHONKE S     | SUI    |     258 |      14 |         0.434 |      0.032 |     -0.043 |           0 |            0 |   -0.768 | -0.011 |              0 |               0 |      0.108 |      -0.125 |  0.003 |  88.281 |
| KJAERLAND E      | NOR    |     164 |       9 |         0.415 |      0.026 |     -0.04  |           0 |            0 |   -0.785 | -0.012 |              0 |               0 |      0.117 |      -0.152 |  0     |  88.872 |
| JIANG J          | CHN    |     282 |      15 |         0.401 |      0.032 |     -0.042 |           0 |            0 |   -0.634 | -0.012 |              0 |               0 |      0.088 |      -0.11  |  0.007 |  92.086 |

