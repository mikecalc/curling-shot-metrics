# World Men's Curling Championship (WMCC2023_ResultsBook)

Ottawa, ON, Canada, 2023; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Men

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| SCO    |      14 | 12-2     |               76.1 |
| SUI    |      14 | 12-2     |               74.9 |
| CAN    |      15 | 11-4     |               61.2 |
| NOR    |      13 | 10-3     |               56.1 |
| SWE    |      13 | 9-4      |               53.8 |
| ITA    |      15 | 9-6      |               48.1 |
| USA    |      12 | 5-7      |               45.5 |
| CZE    |      12 | 3-9      |               26.6 |
| JPN    |      12 | 5-7      |               25.8 |
| GER    |      12 | 4-8      |               24.3 |
| TUR    |      12 | 2-10     |               10   |
| KOR    |      12 | 1-11     |                1.9 |
| NZL    |      12 | 1-11     |               -7.1 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| USA    |      837 |   0.018 |    -0.001 |          0.616 |                2.301 |                   2.347 |
| KOR    |      771 |   0.012 |    -0.034 |          0.638 |                1.91  |                   2.336 |
| NZL    |      775 |   0.009 |    -0.043 |          0.637 |                1.88  |                   2.193 |
| GER    |      821 |   0.008 |     0.002 |          0.615 |                2.195 |                   2.102 |
| CZE    |      812 |   0.006 |    -0.013 |          0.635 |                2.027 |                   2.269 |
| CAN    |     1020 |   0.006 |     0.019 |          0.586 |                2.052 |                   2.069 |
| SCO    |      955 |   0.001 |     0.04  |          0.547 |                2.036 |                   2.053 |
| SUI    |      986 |  -0.003 |     0.009 |          0.586 |                2.164 |                   1.939 |
| NOR    |      941 |  -0.004 |     0.009 |          0.598 |                2.04  |                   1.955 |
| ITA    |     1030 |  -0.008 |    -0.006 |          0.599 |                2.286 |                   1.976 |
| JPN    |      816 |  -0.013 |    -0.002 |          0.594 |                2.167 |                   1.988 |
| TUR    |      807 |  -0.014 |    -0.001 |          0.607 |                1.947 |                   1.946 |
| SWE    |      872 |  -0.017 |     0.005 |          0.586 |                2.16  |                   2.108 |

### Fourths

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| EDIN N       | SWE    |     218 |      13 |         0.656 |      0.271 |     -0.351 |          19 |           14 |   -8.807 |  0.057 |             34 |              13 |      1.001 |      -1.464 | -0.01  |  83.83  |
| SCHWARZ B    | SUI    |     249 |      14 |         0.643 |      0.24  |     -0.246 |          13 |           11 |   -5.983 |  0.066 |             38 |              17 |      1.229 |      -0.941 |  0.004 |  85.553 |
| MOUAT B      | SCO    |     242 |      14 |         0.636 |      0.263 |     -0.235 |          25 |           16 |   -4.331 |  0.082 |             37 |              20 |      0.909 |      -0.675 |  0.011 |  84.959 |
| SHUSTER J    | USA    |     210 |      12 |         0.629 |      0.301 |     -0.331 |          25 |           17 |   -7.474 |  0.066 |             29 |              19 |      0.907 |      -1.382 |  0.001 |  78.708 |
| GUSHUE B     | CAN    |     255 |      15 |         0.62  |      0.267 |     -0.262 |          25 |           15 |   -5.767 |  0.066 |             25 |              19 |      0.91  |      -0.997 |  0.013 |  87.698 |
| RETORNAZ J   | ITA    |     260 |      15 |         0.604 |      0.249 |     -0.34  |          23 |           21 |  -10.39  |  0.015 |             34 |              23 |      1.088 |      -1.377 |  0.005 |  82.239 |
| RAMSFJELL M  | NOR    |     238 |      13 |         0.597 |      0.266 |     -0.296 |          26 |           21 |   -6.181 |  0.039 |             34 |              25 |      1.41  |      -0.83  |  0.015 |  82.097 |
| YANAGISAWA R | JPN    |     206 |      12 |         0.592 |      0.234 |     -0.29  |          13 |           13 |   -6.063 |  0.021 |             18 |              14 |      0.739 |      -1.276 | -0.004 |  79.634 |
| KLIMA L      | CZE    |     203 |      12 |         0.567 |      0.244 |     -0.352 |          12 |           20 |   -7.187 | -0.014 |             25 |              26 |      0.657 |      -0.854 |  0.005 |  72.512 |
| TOTZEK S     | GER    |     205 |      12 |         0.527 |      0.271 |     -0.309 |          14 |           22 |   -7.078 | -0.004 |             17 |              21 |      0.715 |      -0.9   |  0.019 |  75.854 |
| JEONG B      | KOR    |     194 |      12 |         0.521 |      0.17  |     -0.443 |           5 |           30 |   -8.34  | -0.124 |              5 |              31 |      0.412 |      -0.849 |  0.015 |  69.56  |
| KARAGOZ U    | TUR    |     204 |      12 |         0.451 |      0.278 |     -0.379 |          13 |           27 |   -8.672 | -0.083 |             20 |              29 |      1.212 |      -2.068 |  0.021 |  67.822 |
| HOOD A       | NZL    |     196 |      12 |         0.423 |      0.267 |     -0.412 |          12 |           35 |  -10.79  | -0.124 |             15 |              30 |      1.027 |      -1.345 |  0.022 |  66.839 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HARDIE G    | SCO    |     242 |      14 |         0.653 |      0.16  |     -0.126 |           4 |            1 |   -2.133 |  0.061 |             11 |               6 |      0.442 |      -0.309 | -0.002 |  87.552 |
| NICHOLS M   | CAN    |     256 |      15 |         0.609 |      0.154 |     -0.122 |           6 |            1 |   -2.378 |  0.046 |             11 |               5 |      0.465 |      -0.324 | -0.003 |  85.645 |
| MOSANER A   | ITA    |     260 |      15 |         0.573 |      0.141 |     -0.144 |           3 |            5 |   -2.938 |  0.019 |              8 |               6 |      0.427 |      -0.318 | -0     |  86.442 |
| SCHWALLER Y | SUI    |     250 |      14 |         0.568 |      0.145 |     -0.104 |           2 |            1 |   -2.346 |  0.038 |             15 |               5 |      0.519 |      -0.391 | -0.003 |  90.5   |
| ERIKSSON O  | SWE    |     218 |      13 |         0.532 |      0.146 |     -0.134 |           3 |            2 |   -2.629 |  0.015 |              9 |               6 |      0.529 |      -0.519 | -0.018 |  83.065 |
| YAMAGUCHI T | JPN    |     206 |      12 |         0.505 |      0.132 |     -0.127 |           3 |            0 |   -2.023 |  0.004 |              5 |               5 |      0.333 |      -0.36  |  0.003 |  83.01  |
| SESAKER M   | NOR    |     238 |      13 |         0.496 |      0.128 |     -0.151 |           1 |            3 |   -2.963 | -0.012 |              9 |              13 |      0.348 |      -0.51  | -0.001 |  81.933 |
| DEMIREL MH  | TUR    |     205 |      12 |         0.478 |      0.147 |     -0.142 |           4 |            4 |   -2.761 | -0.004 |             12 |               9 |      0.688 |      -0.49  |  0.012 |  79.024 |
| CERNOVSKY M | CZE    |     204 |      12 |         0.475 |      0.167 |     -0.142 |           3 |            5 |   -3.572 |  0.005 |              9 |               5 |      0.506 |      -0.519 |  0.018 |  79.534 |
| HARSCH K    | GER    |     206 |      12 |         0.461 |      0.134 |     -0.155 |           4 |            7 |   -2.925 | -0.021 |              4 |               8 |      0.329 |      -0.442 |  0.019 |  78.034 |
| PLYS C      | USA    |     210 |      12 |         0.438 |      0.157 |     -0.149 |           2 |            4 |   -2.752 | -0.015 |              8 |               6 |      0.511 |      -0.4   |  0.013 |  78.469 |
| SMITH B     | NZL    |     196 |      12 |         0.398 |      0.11  |     -0.194 |           0 |           10 |   -3.633 | -0.073 |              1 |              10 |      0.231 |      -0.398 |  0.019 |  68.24  |
| LEE J       | KOR    |     194 |      12 |         0.392 |      0.131 |     -0.165 |           1 |            5 |   -3.164 | -0.049 |              2 |               5 |      0.251 |      -0.413 |  0.014 |  73.582 |

### Seconds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WRANAA R    | SWE    |     218 |      13 |         0.537 |      0.077 |     -0.068 |           0 |            0 |   -1.125 |  0.01  |              2 |               0 |      0.276 |      -0.135 | -0.008 |  89.335 |
| HARNDEN E   | CAN    |     256 |      15 |         0.523 |      0.082 |     -0.084 |           0 |            1 |   -1.638 |  0.003 |              2 |               0 |      0.257 |      -0.177 | -0.006 |  82.157 |
| ARMAN S     | ITA    |     260 |      15 |         0.519 |      0.081 |     -0.087 |           0 |            2 |   -2.258 |  0     |              3 |               2 |      0.265 |      -0.288 |  0.001 |  84.436 |
| MICHEL S    | SUI    |     250 |      14 |         0.496 |      0.078 |     -0.093 |           1 |            0 |   -1.962 | -0.008 |              5 |               7 |      0.283 |      -0.355 |  0.002 |  85.2   |
| RAMSFJELL B | NOR    |     238 |      13 |         0.487 |      0.071 |     -0.078 |           0 |            1 |   -1.865 | -0.005 |              1 |               2 |      0.217 |      -0.248 | -0     |  83.613 |
| LAMMIE B    | SCO    |     242 |      14 |         0.483 |      0.079 |     -0.086 |           0 |            0 |   -1.435 | -0.006 |              2 |               1 |      0.304 |      -0.183 | -0.007 |  80.394 |
| YAMAMOTO T  | JPN    |     206 |      12 |         0.442 |      0.074 |     -0.089 |           0 |            1 |   -1.787 | -0.017 |              2 |               1 |      0.22  |      -0.205 | -0.003 |  80.882 |
| HAMILTON M  | USA    |     190 |      11 |         0.437 |      0.094 |     -0.095 |           1 |            3 |   -2.829 | -0.012 |              1 |               1 |      0.18  |      -0.209 |  0.006 |  79.474 |
| BOHAC R     | CZE    |     166 |      11 |         0.434 |      0.069 |     -0.094 |           0 |            1 |   -2.072 | -0.023 |              0 |               1 |      0.133 |      -0.214 |  0.002 |  76.054 |
| SUTOR M     | GER    |     204 |      12 |         0.422 |      0.089 |     -0.094 |           0 |            0 |   -1.374 | -0.017 |              1 |               1 |      0.253 |      -0.222 |  0.004 |  73.775 |
| KAVAZ F     | TUR    |      44 |       4 |         0.409 |      0.055 |     -0.137 |           0 |            1 |   -1.854 | -0.059 |              0 |               0 |      0.12  |      -0.165 |  0.005 |  63.068 |
| KIM M       | KOR    |     194 |      12 |         0.392 |      0.081 |     -0.105 |           0 |            1 |   -2.118 | -0.032 |              1 |               3 |      0.165 |      -0.255 |  0.012 |  74.613 |
| UCAN MZ     | TUR    |     167 |      10 |         0.383 |      0.076 |     -0.097 |           0 |            2 |   -2.477 | -0.031 |              0 |               4 |      0.183 |      -0.552 |  0.011 |  78.443 |
| SARGON B    | NZL    |     196 |      12 |         0.383 |      0.063 |     -0.105 |           0 |            0 |   -1.908 | -0.041 |              0 |               2 |      0.148 |      -0.251 |  0.004 |  70.408 |

### Leads

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KOIZUMI S     | JPN    |     206 |      12 |         0.607 |      0.033 |     -0.049 |           0 |            0 |   -0.679 |  0.001 |              0 |               0 |      0.106 |      -0.127 |  0.002 |  85.437 |
| LANDSTEINER J | USA    |     146 |       9 |         0.596 |      0.038 |     -0.049 |           0 |            0 |   -0.718 |  0.003 |              0 |               0 |      0.071 |      -0.098 |  0.002 |  86.473 |
| SUNDGREN C    | SWE    |     214 |      13 |         0.593 |      0.042 |     -0.036 |           0 |            0 |   -0.734 |  0.01  |              0 |               0 |      0.094 |      -0.113 |  0.004 |  90.421 |
| KLIPA L       | CZE    |      56 |       3 |         0.571 |      0.022 |     -0.055 |           0 |            0 |   -0.614 | -0.011 |              0 |               1 |      0.059 |      -0.147 | -0     |  75.893 |
| HUFMAN C      | USA    |      84 |       5 |         0.571 |      0.047 |     -0.059 |           0 |            0 |   -0.854 |  0.002 |              0 |               1 |      0.126 |      -0.14  |  0.006 |  89.583 |
| MCMILLAN H    | SCO    |     240 |      14 |         0.571 |      0.034 |     -0.036 |           0 |            0 |   -0.612 |  0.004 |              0 |               0 |      0.089 |      -0.09  |  0.006 |  90.521 |
| KIM T         | KOR    |     194 |      12 |         0.562 |      0.039 |     -0.05  |           0 |            0 |   -0.708 | -0     |              0 |               0 |      0.094 |      -0.097 |  0.002 |  86.788 |
| GREINDL D     | GER    |     206 |      12 |         0.553 |      0.038 |     -0.042 |           0 |            0 |   -0.685 |  0.002 |              0 |               0 |      0.087 |      -0.115 |  0.001 |  85.437 |
| WALKER G      | CAN    |     252 |      15 |         0.544 |      0.035 |     -0.037 |           0 |            0 |   -0.58  |  0.002 |              0 |               0 |      0.094 |      -0.076 |  0.001 |  92.659 |
| WALKER H      | NZL    |     188 |      12 |         0.537 |      0.036 |     -0.044 |           0 |            0 |   -0.646 | -0.001 |              0 |               0 |      0.094 |      -0.095 |  0.003 |  86.436 |
| GIOVANELLA M  | ITA    |     260 |      15 |         0.535 |      0.039 |     -0.044 |           0 |            0 |   -0.692 |  0     |              0 |               0 |      0.107 |      -0.1   |  0.003 |  88.803 |
| LACHAT P      | SUI    |     250 |      14 |         0.524 |      0.041 |     -0.045 |           0 |            0 |   -0.748 |  0     |              0 |               1 |      0.096 |      -0.147 |  0.004 |  86.1   |
| NEPSTAD G     | NOR    |     238 |      13 |         0.492 |      0.036 |     -0.038 |           0 |            0 |   -0.799 | -0.002 |              0 |               0 |      0.084 |      -0.129 |  0.003 |  88.291 |
| YUCE O        | TUR    |     196 |      12 |         0.454 |      0.037 |     -0.054 |           0 |            0 |   -0.879 | -0.013 |              0 |               1 |      0.081 |      -0.201 |  0.005 |  79.847 |
| JURIK M       | CZE    |     186 |      11 |         0.441 |      0.04  |     -0.059 |           0 |            0 |   -1.356 | -0.015 |              0 |               1 |      0.099 |      -0.191 |  0.001 |  79.032 |

