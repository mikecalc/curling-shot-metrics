# World Men's Curling Championship (WMCC2023_ResultsBook)

Ottawa, ON, Canada, 2023; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Men

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| SUI    |      14 | 12-2     |               74.5 |
| SCO    |      14 | 12-2     |               66.2 |
| CAN    |      15 | 11-4     |               57.7 |
| NOR    |      13 | 10-3     |               48.4 |
| SWE    |      13 | 9-4      |               45.6 |
| ITA    |      15 | 9-6      |               42.8 |
| USA    |      12 | 5-7      |               42.8 |
| GER    |      12 | 4-8      |               26   |
| CZE    |      12 | 3-9      |               23.5 |
| JPN    |      12 | 5-7      |               21.7 |
| TUR    |      12 | 2-10     |                7.9 |
| KOR    |      12 | 1-11     |                1.4 |
| NZL    |      12 | 1-11     |               -6.2 |

### Build or address

How each team played the stones, in rock potential (descriptive, not a ranking): `build` is how much a stone added to the team's own potential and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' potential together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| USA    |      837 |   0.022 |    -0.017 |          0.773 |                2.883 |                   2.76  |
| GER    |      821 |   0.014 |     0     |          0.766 |                2.786 |                   2.34  |
| NZL    |      775 |   0.009 |    -0.012 |          0.746 |                2.445 |                   2.643 |
| JPN    |      816 |   0.006 |    -0.018 |          0.765 |                2.604 |                   2.443 |
| ITA    |     1030 |   0.006 |    -0.012 |          0.726 |                2.672 |                   2.544 |
| KOR    |      771 |   0.004 |    -0.009 |          0.732 |                2.448 |                   2.708 |
| SWE    |      872 |  -0.001 |    -0.001 |          0.729 |                2.507 |                   2.674 |
| CZE    |      812 |  -0.003 |    -0.007 |          0.73  |                2.511 |                   2.836 |
| SUI    |      986 |  -0.007 |     0.021 |          0.699 |                2.619 |                   2.405 |
| NOR    |      941 |  -0.008 |     0.008 |          0.717 |                2.416 |                   2.19  |
| CAN    |     1020 |  -0.008 |     0.005 |          0.704 |                2.333 |                   2.678 |
| SCO    |      955 |  -0.013 |     0.019 |          0.685 |                2.338 |                   2.562 |
| TUR    |      807 |  -0.017 |     0.015 |          0.71  |                2.409 |                   2.167 |

### Fourths

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MOUAT B      | SCO    |     242 |      14 |         0.682 |      0.264 |     -0.251 |          25 |           13 |   -4.336 |  0.1   |             42 |              16 |      0.982 |      -0.72  |  0.009 |  84.959 |
| SHUSTER J    | USA    |     210 |      12 |         0.671 |      0.298 |     -0.339 |          25 |           12 |   -7.481 |  0.089 |             29 |              19 |      1.241 |      -1.381 | -0.001 |  78.708 |
| EDIN N       | SWE    |     218 |      13 |         0.656 |      0.285 |     -0.335 |          20 |           16 |   -8.892 |  0.072 |             36 |              15 |      0.958 |      -1.485 | -0.014 |  83.83  |
| SCHWARZ B    | SUI    |     249 |      14 |         0.647 |      0.257 |     -0.233 |          14 |            8 |   -5.245 |  0.084 |             47 |              17 |      1.388 |      -0.801 |  0.009 |  85.553 |
| RETORNAZ J   | ITA    |     260 |      15 |         0.642 |      0.256 |     -0.359 |          25 |           22 |  -10.508 |  0.036 |             36 |              24 |      0.968 |      -1.418 |  0     |  82.239 |
| GUSHUE B     | CAN    |     255 |      15 |         0.635 |      0.276 |     -0.258 |          25 |           14 |   -5.916 |  0.081 |             31 |              15 |      0.93  |      -0.993 |  0.018 |  87.698 |
| YANAGISAWA R | JPN    |     206 |      12 |         0.592 |      0.246 |     -0.268 |          13 |           12 |   -6.238 |  0.036 |             19 |              16 |      0.745 |      -1.305 | -0.006 |  79.634 |
| RAMSFJELL M  | NOR    |     238 |      13 |         0.584 |      0.281 |     -0.293 |          26 |           20 |   -6.147 |  0.042 |             38 |              27 |      1.289 |      -0.893 |  0.013 |  82.097 |
| KLIMA L      | CZE    |     203 |      12 |         0.581 |      0.263 |     -0.37  |          17 |           20 |   -8.011 | -0.002 |             28 |              25 |      0.79  |      -0.89  |  0.007 |  72.512 |
| TOTZEK S     | GER    |     205 |      12 |         0.527 |      0.299 |     -0.307 |          17 |           20 |   -6.934 |  0.012 |             17 |              18 |      0.785 |      -0.778 |  0.027 |  75.854 |
| JEONG B      | KOR    |     194 |      12 |         0.515 |      0.186 |     -0.413 |           5 |           30 |   -8.228 | -0.104 |              6 |              27 |      0.436 |      -0.794 |  0.009 |  69.56  |
| KARAGOZ U    | TUR    |     204 |      12 |         0.461 |      0.296 |     -0.383 |          16 |           29 |   -8.611 | -0.07  |             21 |              28 |      1.277 |      -2.096 |  0.021 |  67.822 |
| HOOD A       | NZL    |     196 |      12 |         0.459 |      0.275 |     -0.432 |          13 |           30 |  -10.8   | -0.107 |             18 |              27 |      1.12  |      -1.416 |  0.029 |  66.839 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HARDIE G    | SCO    |     242 |      14 |         0.649 |      0.121 |     -0.123 |           3 |            1 |   -2.209 |  0.035 |              4 |               7 |      0.342 |      -0.385 | -0.001 |  87.552 |
| NICHOLS M   | CAN    |     256 |      15 |         0.609 |      0.143 |     -0.123 |           3 |            1 |   -2.242 |  0.039 |             12 |               6 |      0.493 |      -0.342 |  0.003 |  85.645 |
| SCHWALLER Y | SUI    |     250 |      14 |         0.596 |      0.116 |     -0.112 |           2 |            1 |   -2.238 |  0.024 |             11 |               5 |      0.389 |      -0.374 |  0.007 |  90.5   |
| ERIKSSON O  | SWE    |     218 |      13 |         0.55  |      0.121 |     -0.134 |           3 |            1 |   -2.221 |  0.006 |              4 |               4 |      0.406 |      -0.334 | -0.018 |  83.065 |
| MOSANER A   | ITA    |     260 |      15 |         0.542 |      0.127 |     -0.134 |           3 |            5 |   -2.67  |  0.008 |              8 |               6 |      0.428 |      -0.347 |  0.002 |  86.442 |
| DEMIREL MH  | TUR    |     205 |      12 |         0.537 |      0.126 |     -0.159 |           4 |            3 |   -2.722 | -0.006 |             10 |              10 |      0.59  |      -0.565 |  0.013 |  79.024 |
| CERNOVSKY M | CZE    |     204 |      12 |         0.525 |      0.139 |     -0.156 |           2 |            1 |   -2.783 | -0.001 |             11 |               6 |      0.451 |      -0.421 |  0.012 |  79.534 |
| SESAKER M   | NOR    |     238 |      13 |         0.508 |      0.106 |     -0.146 |           0 |            1 |   -2.353 | -0.018 |              4 |              10 |      0.331 |      -0.552 |  0.004 |  81.933 |
| HARSCH K    | GER    |     206 |      12 |         0.476 |      0.12  |     -0.163 |           0 |            4 |   -3.124 | -0.029 |              3 |               7 |      0.284 |      -0.393 |  0.021 |  78.034 |
| LEE J       | KOR    |     194 |      12 |         0.469 |      0.113 |     -0.167 |           0 |            5 |   -3.009 | -0.035 |              3 |               8 |      0.283 |      -0.456 |  0.009 |  73.582 |
| YAMAGUCHI T | JPN    |     206 |      12 |         0.451 |      0.115 |     -0.121 |           1 |            1 |   -2.106 | -0.015 |              1 |               3 |      0.31  |      -0.274 |  0.003 |  83.01  |
| PLYS C      | USA    |     210 |      12 |         0.443 |      0.127 |     -0.146 |           1 |            1 |   -2.413 | -0.025 |              3 |               9 |      0.37  |      -0.313 |  0.014 |  78.469 |
| SMITH B     | NZL    |     196 |      12 |         0.378 |      0.101 |     -0.181 |           0 |            9 |   -4.105 | -0.075 |              3 |               9 |      0.274 |      -0.41  |  0.017 |  68.24  |

### Seconds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MICHEL S    | SUI    |     250 |      14 |         0.508 |      0.067 |     -0.097 |           0 |            1 |   -2.162 | -0.014 |              0 |               5 |      0.209 |      -0.367 |  0.001 |  85.2   |
| HARNDEN E   | CAN    |     256 |      15 |         0.504 |      0.072 |     -0.083 |           0 |            0 |   -1.726 | -0.005 |              1 |               1 |      0.213 |      -0.214 | -0.008 |  82.157 |
| WRANAA R    | SWE    |     218 |      13 |         0.495 |      0.062 |     -0.071 |           0 |            0 |   -1.096 | -0.005 |              1 |               0 |      0.194 |      -0.154 | -0.005 |  89.335 |
| ARMAN S     | ITA    |     260 |      15 |         0.485 |      0.059 |     -0.087 |           0 |            0 |   -1.864 | -0.016 |              0 |               1 |      0.186 |      -0.216 |  0.002 |  84.436 |
| KAVAZ F     | TUR    |      44 |       4 |         0.455 |      0.035 |     -0.109 |           0 |            0 |   -1.557 | -0.044 |              0 |               0 |      0.078 |      -0.133 |  0.004 |  63.068 |
| LAMMIE B    | SCO    |     242 |      14 |         0.45  |      0.059 |     -0.091 |           0 |            0 |   -1.501 | -0.023 |              2 |               0 |      0.235 |      -0.207 | -0.01  |  80.394 |
| HAMILTON M  | USA    |     190 |      11 |         0.442 |      0.068 |     -0.079 |           0 |            0 |   -1.569 | -0.014 |              0 |               0 |      0.164 |      -0.166 |  0.007 |  79.474 |
| KIM M       | KOR    |     194 |      12 |         0.433 |      0.058 |     -0.102 |           0 |            1 |   -1.802 | -0.033 |              1 |               1 |      0.176 |      -0.258 |  0.011 |  74.613 |
| YAMAMOTO T  | JPN    |     206 |      12 |         0.417 |      0.062 |     -0.079 |           0 |            0 |   -1.39  | -0.02  |              1 |               0 |      0.217 |      -0.17  | -0.005 |  80.882 |
| UCAN MZ     | TUR    |     167 |      10 |         0.413 |      0.068 |     -0.1   |           0 |            2 |   -2.513 | -0.03  |              0 |               3 |      0.145 |      -0.527 |  0.009 |  78.443 |
| RAMSFJELL B | NOR    |     238 |      13 |         0.412 |      0.059 |     -0.067 |           0 |            1 |   -1.86  | -0.015 |              1 |               2 |      0.189 |      -0.243 |  0.002 |  83.613 |
| SUTOR M     | GER    |     204 |      12 |         0.407 |      0.077 |     -0.093 |           0 |            0 |   -1.2   | -0.024 |              2 |               0 |      0.229 |      -0.167 | -0.001 |  73.775 |
| BOHAC R     | CZE    |     166 |      11 |         0.392 |      0.051 |     -0.082 |           0 |            0 |   -1.376 | -0.03  |              0 |               0 |      0.11  |      -0.158 |  0.005 |  76.054 |
| SARGON B    | NZL    |     196 |      12 |         0.372 |      0.054 |     -0.097 |           0 |            0 |   -1.664 | -0.041 |              1 |               2 |      0.177 |      -0.256 |  0.005 |  70.408 |

### Leads

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SUNDGREN C    | SWE    |     214 |      13 |         0.654 |      0.025 |     -0.033 |           0 |            0 |   -0.769 |  0.005 |              0 |               0 |      0.075 |      -0.114 | -0     |  90.421 |
| KLIPA L       | CZE    |      56 |       3 |         0.589 |      0.021 |     -0.027 |           0 |            0 |   -0.372 |  0.001 |              0 |               1 |      0.049 |      -0.125 | -0.002 |  75.893 |
| GREINDL D     | GER    |     206 |      12 |         0.578 |      0.025 |     -0.03  |           0 |            0 |   -0.729 |  0.002 |              0 |               0 |      0.056 |      -0.117 | -0.002 |  85.437 |
| HUFMAN C      | USA    |      84 |       5 |         0.571 |      0.038 |     -0.052 |           0 |            0 |   -0.936 | -0     |              0 |               1 |      0.091 |      -0.148 |  0.002 |  89.583 |
| WALKER G      | CAN    |     252 |      15 |         0.563 |      0.021 |     -0.03  |           0 |            0 |   -0.596 | -0.001 |              0 |               0 |      0.062 |      -0.075 | -0.002 |  92.659 |
| NEPSTAD G     | NOR    |     238 |      13 |         0.563 |      0.027 |     -0.032 |           0 |            0 |   -0.781 |  0.001 |              0 |               0 |      0.085 |      -0.134 |  0.001 |  88.291 |
| KIM T         | KOR    |     194 |      12 |         0.552 |      0.028 |     -0.029 |           0 |            0 |   -0.608 |  0.003 |              0 |               0 |      0.077 |      -0.082 | -0.001 |  86.788 |
| LANDSTEINER J | USA    |     146 |       9 |         0.548 |      0.028 |     -0.033 |           0 |            0 |   -0.724 |  0     |              0 |               0 |      0.063 |      -0.089 |  0.001 |  86.473 |
| WALKER H      | NZL    |     188 |      12 |         0.537 |      0.026 |     -0.03  |           0 |            0 |   -0.571 | -0     |              0 |               0 |      0.083 |      -0.068 | -0.002 |  86.436 |
| LACHAT P      | SUI    |     250 |      14 |         0.532 |      0.027 |     -0.038 |           0 |            0 |   -0.658 | -0.003 |              0 |               0 |      0.091 |      -0.11  |  0     |  86.1   |
| MCMILLAN H    | SCO    |     240 |      14 |         0.525 |      0.025 |     -0.028 |           0 |            0 |   -0.578 | -0     |              0 |               0 |      0.071 |      -0.078 |  0.005 |  90.521 |
| GIOVANELLA M  | ITA    |     260 |      15 |         0.519 |      0.028 |     -0.032 |           0 |            0 |   -0.741 | -0.001 |              0 |               0 |      0.085 |      -0.104 |  0.002 |  88.803 |
| JURIK M       | CZE    |     186 |      11 |         0.505 |      0.027 |     -0.042 |           0 |            0 |   -1.12  | -0.007 |              0 |               1 |      0.083 |      -0.176 |  0     |  79.032 |
| KOIZUMI S     | JPN    |     206 |      12 |         0.505 |      0.023 |     -0.029 |           0 |            0 |   -0.574 | -0.003 |              0 |               0 |      0.077 |      -0.092 | -0.001 |  85.437 |
| YUCE O        | TUR    |     196 |      12 |         0.429 |      0.026 |     -0.034 |           0 |            0 |   -0.844 | -0.008 |              0 |               1 |      0.062 |      -0.192 |  0.002 |  79.847 |

