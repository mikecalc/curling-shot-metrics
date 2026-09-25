# World Men's Curling Championship (WMCC2023_ResultsBook)

Ottawa, ON, Canada, 2023; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Men

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| SUI    |      14 | 12-2     |               77.2 |
| SCO    |      14 | 12-2     |               67.3 |
| CAN    |      15 | 11-4     |               59.2 |
| NOR    |      13 | 10-3     |               49   |
| SWE    |      13 | 9-4      |               46.6 |
| ITA    |      15 | 9-6      |               44.8 |
| USA    |      12 | 5-7      |               44.1 |
| CZE    |      12 | 3-9      |               27.1 |
| GER    |      12 | 4-8      |               27   |
| JPN    |      12 | 5-7      |               23.3 |
| TUR    |      12 | 2-10     |                8.1 |
| KOR    |      12 | 1-11     |                2.2 |
| NZL    |      12 | 1-11     |               -6.8 |

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
| EDIN N       | SWE    |     218 |      13 |         0.679 |      0.265 |     -0.356 |          23 |           14 |   -8.579 |  0.065 |             34 |              16 |      0.954 |      -1.401 | -0.016 |  83.83  |
| MOUAT B      | SCO    |     242 |      14 |         0.649 |      0.264 |     -0.224 |          21 |           12 |   -4.296 |  0.092 |             40 |              16 |      0.951 |      -0.696 |  0.011 |  84.959 |
| RETORNAZ J   | ITA    |     260 |      15 |         0.646 |      0.244 |     -0.356 |          21 |           21 |  -10.291 |  0.032 |             32 |              22 |      0.947 |      -1.373 |  0.002 |  82.239 |
| SCHWARZ B    | SUI    |     249 |      14 |         0.639 |      0.259 |     -0.234 |          19 |            8 |   -5.428 |  0.081 |             44 |              17 |      1.425 |      -0.836 |  0.008 |  85.553 |
| GUSHUE B     | CAN    |     255 |      15 |         0.627 |      0.268 |     -0.258 |          19 |           13 |   -5.887 |  0.072 |             28 |              13 |      0.913 |      -1.008 |  0.024 |  87.698 |
| SHUSTER J    | USA    |     210 |      12 |         0.619 |      0.313 |     -0.295 |          24 |           11 |   -7.219 |  0.081 |             30 |              16 |      1.188 |      -1.371 | -0.001 |  78.708 |
| YANAGISAWA R | JPN    |     206 |      12 |         0.578 |      0.25  |     -0.264 |          13 |           12 |   -6.2   |  0.033 |             18 |              18 |      0.826 |      -1.355 | -0.002 |  79.634 |
| KLIMA L      | CZE    |     203 |      12 |         0.571 |      0.257 |     -0.361 |          17 |           20 |   -7.982 | -0.008 |             23 |              24 |      0.786 |      -0.9   |  0.009 |  72.512 |
| RAMSFJELL M  | NOR    |     238 |      13 |         0.563 |      0.284 |     -0.276 |          26 |           20 |   -6.148 |  0.039 |             36 |              25 |      1.267 |      -0.854 |  0.014 |  82.097 |
| TOTZEK S     | GER    |     205 |      12 |         0.532 |      0.296 |     -0.313 |          16 |           20 |   -6.945 |  0.011 |             17 |              20 |      0.697 |      -0.796 |  0.029 |  75.854 |
| JEONG B      | KOR    |     194 |      12 |         0.49  |      0.188 |     -0.4   |           5 |           29 |   -8.213 | -0.112 |              7 |              28 |      0.404 |      -0.796 |  0.007 |  69.56  |
| KARAGOZ U    | TUR    |     204 |      12 |         0.451 |      0.302 |     -0.375 |          16 |           27 |   -8.457 | -0.069 |             20 |              26 |      1.293 |      -2.017 |  0.019 |  67.822 |
| HOOD A       | NZL    |     196 |      12 |         0.429 |      0.284 |     -0.414 |          12 |           30 |  -10.553 | -0.115 |             17 |              29 |      1.072 |      -1.454 |  0.026 |  66.839 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HARDIE G    | SCO    |     242 |      14 |         0.665 |      0.122 |     -0.125 |           1 |            1 |   -2.031 |  0.04  |              5 |               5 |      0.354 |      -0.335 | -0.003 |  87.552 |
| NICHOLS M   | CAN    |     256 |      15 |         0.641 |      0.142 |     -0.122 |           5 |            1 |   -2.215 |  0.047 |              9 |               4 |      0.494 |      -0.322 | -0     |  85.645 |
| SCHWALLER Y | SUI    |     250 |      14 |         0.584 |      0.122 |     -0.101 |           0 |            2 |   -2.19  |  0.029 |             14 |               5 |      0.371 |      -0.359 |  0.004 |  90.5   |
| ERIKSSON O  | SWE    |     218 |      13 |         0.578 |      0.12  |     -0.133 |           2 |            1 |   -2.329 |  0.013 |              3 |               4 |      0.427 |      -0.335 | -0.027 |  83.065 |
| MOSANER A   | ITA    |     260 |      15 |         0.542 |      0.135 |     -0.134 |           3 |            4 |   -2.73  |  0.012 |              8 |               6 |      0.452 |      -0.356 |  0.003 |  86.442 |
| DEMIREL MH  | TUR    |     205 |      12 |         0.532 |      0.125 |     -0.155 |           3 |            1 |   -2.629 | -0.006 |             10 |              10 |      0.563 |      -0.533 |  0.02  |  79.024 |
| CERNOVSKY M | CZE    |     204 |      12 |         0.5   |      0.145 |     -0.141 |           3 |            4 |   -2.945 |  0.002 |             10 |               6 |      0.45  |      -0.439 |  0.015 |  79.534 |
| SESAKER M   | NOR    |     238 |      13 |         0.475 |      0.116 |     -0.131 |           0 |            1 |   -2.27  | -0.014 |              8 |               6 |      0.364 |      -0.569 |  0.001 |  81.933 |
| HARSCH K    | GER    |     206 |      12 |         0.471 |      0.124 |     -0.17  |           2 |            5 |   -3.054 | -0.032 |              3 |               5 |      0.275 |      -0.377 |  0.022 |  78.034 |
| LEE J       | KOR    |     194 |      12 |         0.454 |      0.114 |     -0.16  |           0 |            2 |   -2.7   | -0.036 |              2 |               7 |      0.284 |      -0.42  |  0.012 |  73.582 |
| PLYS C      | USA    |     210 |      12 |         0.443 |      0.139 |     -0.146 |           1 |            2 |   -2.485 | -0.02  |              5 |               8 |      0.393 |      -0.317 |  0.013 |  78.469 |
| YAMAGUCHI T | JPN    |     206 |      12 |         0.437 |      0.123 |     -0.118 |           1 |            2 |   -2.302 | -0.013 |              2 |               7 |      0.317 |      -0.32  |  0.005 |  83.01  |
| SMITH B     | NZL    |     196 |      12 |         0.357 |      0.114 |     -0.173 |           0 |           11 |   -3.417 | -0.07  |              2 |               9 |      0.253 |      -0.389 |  0.021 |  68.24  |

### Seconds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MICHEL S    | SUI    |     250 |      14 |         0.556 |      0.066 |     -0.103 |           0 |            1 |   -2.164 | -0.009 |              2 |               6 |      0.236 |      -0.369 |  0.004 |  85.2   |
| WRANAA R    | SWE    |     218 |      13 |         0.532 |      0.071 |     -0.072 |           0 |            0 |   -1.132 |  0.004 |              0 |               0 |      0.2   |      -0.154 | -0.007 |  89.335 |
| ARMAN S     | ITA    |     260 |      15 |         0.512 |      0.066 |     -0.089 |           0 |            0 |   -1.827 | -0.01  |              0 |               1 |      0.205 |      -0.244 |  0.002 |  84.436 |
| HARNDEN E   | CAN    |     256 |      15 |         0.504 |      0.077 |     -0.082 |           0 |            0 |   -1.841 | -0.002 |              1 |               2 |      0.229 |      -0.233 | -0.007 |  82.157 |
| LAMMIE B    | SCO    |     242 |      14 |         0.475 |      0.066 |     -0.094 |           0 |            0 |   -1.584 | -0.018 |              2 |               1 |      0.266 |      -0.221 | -0.008 |  80.394 |
| HAMILTON M  | USA    |     190 |      11 |         0.453 |      0.078 |     -0.081 |           0 |            0 |   -1.558 | -0.009 |              1 |               0 |      0.181 |      -0.149 |  0.007 |  79.474 |
| RAMSFJELL B | NOR    |     238 |      13 |         0.429 |      0.065 |     -0.071 |           0 |            1 |   -1.846 | -0.012 |              1 |               0 |      0.217 |      -0.219 |  0.002 |  83.613 |
| UCAN MZ     | TUR    |     167 |      10 |         0.425 |      0.074 |     -0.105 |           0 |            2 |   -2.673 | -0.029 |              1 |               4 |      0.181 |      -0.535 |  0.009 |  78.443 |
| YAMAMOTO T  | JPN    |     206 |      12 |         0.408 |      0.067 |     -0.081 |           0 |            0 |   -1.47  | -0.02  |              1 |               0 |      0.207 |      -0.18  | -0.001 |  80.882 |
| SUTOR M     | GER    |     204 |      12 |         0.407 |      0.086 |     -0.096 |           0 |            0 |   -1.21  | -0.022 |              2 |               0 |      0.252 |      -0.178 | -0     |  73.775 |
| BOHAC R     | CZE    |     166 |      11 |         0.398 |      0.057 |     -0.087 |           0 |            0 |   -1.375 | -0.029 |              1 |               0 |      0.138 |      -0.173 |  0.009 |  76.054 |
| KIM M       | KOR    |     194 |      12 |         0.397 |      0.071 |     -0.097 |           0 |            1 |   -1.764 | -0.03  |              1 |               1 |      0.176 |      -0.254 |  0.013 |  74.613 |
| KAVAZ F     | TUR    |      44 |       4 |         0.364 |      0.044 |     -0.098 |           0 |            1 |   -1.516 | -0.047 |              0 |               0 |      0.077 |      -0.131 |  0.007 |  63.068 |
| SARGON B    | NZL    |     196 |      12 |         0.342 |      0.052 |     -0.094 |           0 |            0 |   -1.581 | -0.044 |              0 |               2 |      0.128 |      -0.239 |  0.008 |  70.408 |

### Leads

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KLIPA L       | CZE    |      56 |       3 |         0.625 |      0.022 |     -0.035 |           0 |            0 |   -0.432 |  0     |              0 |               1 |      0.051 |      -0.162 | -0.003 |  75.893 |
| SUNDGREN C    | SWE    |     214 |      13 |         0.584 |      0.027 |     -0.029 |           0 |            0 |   -0.726 |  0.004 |              0 |               0 |      0.075 |      -0.116 | -0     |  90.421 |
| HUFMAN C      | USA    |      84 |       5 |         0.571 |      0.042 |     -0.061 |           0 |            0 |   -1.05  | -0.002 |              0 |               1 |      0.134 |      -0.161 |  0.004 |  89.583 |
| GREINDL D     | GER    |     206 |      12 |         0.568 |      0.025 |     -0.029 |           0 |            0 |   -0.722 |  0.001 |              0 |               0 |      0.064 |      -0.123 | -0.003 |  85.437 |
| KIM T         | KOR    |     194 |      12 |         0.557 |      0.027 |     -0.033 |           0 |            0 |   -0.715 |  0     |              0 |               0 |      0.084 |      -0.094 | -0.002 |  86.788 |
| LANDSTEINER J | USA    |     146 |       9 |         0.555 |      0.029 |     -0.034 |           0 |            0 |   -0.731 |  0.001 |              0 |               0 |      0.063 |      -0.087 | -0     |  86.473 |
| NEPSTAD G     | NOR    |     238 |      13 |         0.55  |      0.026 |     -0.036 |           0 |            0 |   -0.89  | -0.002 |              0 |               1 |      0.084 |      -0.148 |  0.002 |  88.291 |
| WALKER G      | CAN    |     252 |      15 |         0.536 |      0.021 |     -0.03  |           0 |            0 |   -0.609 | -0.002 |              0 |               0 |      0.072 |      -0.075 | -0.002 |  92.659 |
| GIOVANELLA M  | ITA    |     260 |      15 |         0.535 |      0.027 |     -0.033 |           0 |            0 |   -0.701 | -0.001 |              0 |               0 |      0.091 |      -0.104 | -0     |  88.803 |
| LACHAT P      | SUI    |     250 |      14 |         0.528 |      0.027 |     -0.042 |           0 |            0 |   -0.758 | -0.005 |              0 |               1 |      0.101 |      -0.117 |  0.001 |  86.1   |
| MCMILLAN H    | SCO    |     240 |      14 |         0.517 |      0.023 |     -0.029 |           0 |            0 |   -0.628 | -0.002 |              0 |               0 |      0.066 |      -0.092 |  0.004 |  90.521 |
| JURIK M       | CZE    |     186 |      11 |         0.511 |      0.029 |     -0.043 |           0 |            0 |   -1.006 | -0.006 |              0 |               1 |      0.11  |      -0.186 |  0     |  79.032 |
| WALKER H      | NZL    |     188 |      12 |         0.5   |      0.025 |     -0.033 |           0 |            0 |   -0.596 | -0.004 |              0 |               0 |      0.085 |      -0.081 |  0     |  86.436 |
| KOIZUMI S     | JPN    |     206 |      12 |         0.466 |      0.024 |     -0.03  |           0 |            0 |   -0.522 | -0.004 |              0 |               0 |      0.084 |      -0.1   | -0.001 |  85.437 |
| YUCE O        | TUR    |     196 |      12 |         0.418 |      0.027 |     -0.034 |           0 |            0 |   -0.835 | -0.009 |              0 |               1 |      0.065 |      -0.194 |  0.001 |  79.847 |

