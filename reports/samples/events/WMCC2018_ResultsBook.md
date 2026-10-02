# World Men's Curling Championship (WMCC2018_ResultsBook)

Las Vegas, NV, United States, 2018; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The player tables show the spread of each player's shots, not just their average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more percentage points of win probability, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SWE    |      14 | 13-1     |  42.9 |   5.2 |  24.2 |      12.4 |     1.1 |      73.5 |
| SCO    |      14 | 12-2     |  35.7 |   5.2 |  12   |      18.2 |     0.4 |      67.5 |
| CAN    |      15 | 11-4     |  23.3 |  -0.8 |  23.2 |       0.7 |     0.3 |      65.2 |
| NOR    |      13 | 7-6      |   3.8 |  -0.9 |  -1.9 |       8   |    -1.3 |      50.5 |
| KOR    |      15 | 8-7      |   3.3 |   0.8 |   4.1 |      -3.5 |     1.9 |      50   |
| SUI    |      12 | 6-6      |   0   |  -4   |  -4.3 |      13.6 |    -5.4 |      44.6 |
| USA    |      13 | 6-7      |  -3.8 |   2.8 |  -2.6 |      -6.6 |     2.6 |      53.7 |
| ITA    |      12 | 5-7      |  -8.3 |  -2   |   1   |      -7   |    -0.4 |      47.7 |
| RUS    |      12 | 5-7      |  -8.3 |  -6   |  -3.4 |      -1.5 |     2.6 |      39.7 |
| NED    |      12 | 4-8      | -16.7 |   8   | -15   |      -8.3 |    -1.3 |      48.3 |
| CHN    |      12 | 3-9      | -25   |  -2   |  -2.4 |     -17.4 |    -3.2 |      36   |
| JPN    |      12 | 3-9      | -25   |  -6   | -24   |       6   |    -0.9 |      34.6 |
| GER    |      12 | 1-11     | -41.7 |  -2   | -23.4 |     -18.9 |     2.6 |      27.8 |

### Fourths

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| EDIN N      | SWE    |     250 |      14 |         0.684 |      0.202 |     -0.258 |  0.056 |          18 |           14 |   -6.659 |             32 |              19 |      1.156 |      -1.233 | -0.007 |  89.415 |
| GUSHUE B    | CAN    |     264 |      15 |         0.648 |      0.225 |     -0.266 |  0.052 |          22 |           15 |   -7.013 |             34 |              20 |      1.23  |      -1.695 |  0.005 |  85.701 |
| MOUAT B     | SCO    |     244 |      14 |         0.615 |      0.259 |     -0.296 |  0.045 |          22 |           20 |   -5.724 |             37 |              33 |      1.229 |      -0.919 | -0.016 |  81.455 |
| MOSANER A   | ITA    |     219 |      12 |         0.603 |      0.236 |     -0.313 |  0.018 |          17 |           22 |   -6.572 |             29 |              24 |      0.806 |      -1.685 |  0.004 |  79.263 |
| KIM C       | KOR    |     284 |      15 |         0.567 |      0.271 |     -0.324 |  0.013 |          20 |           25 |   -8.523 |             42 |              39 |      1.317 |      -1.828 |  0.008 |  78.136 |
| ZOU D       | CHN    |     225 |      12 |         0.6   |      0.224 |     -0.328 |  0.003 |          16 |           19 |   -8.043 |             25 |              22 |      0.653 |      -0.923 |  0.009 |  78.139 |
| TIMOFEEV A  | RUS    |     230 |      12 |         0.53  |      0.229 |     -0.258 |  0     |          12 |           18 |   -6.48  |             35 |              28 |      1.148 |      -1.436 | -0.002 |  76.747 |
| PFISTER M   | SUI    |     232 |      12 |         0.513 |      0.206 |     -0.222 | -0.002 |           9 |           16 |   -5.187 |             28 |              30 |      0.807 |      -0.995 |  0.002 |  78.634 |
| WALSTAD S   | NOR    |     243 |      13 |         0.543 |      0.226 |     -0.283 | -0.007 |          14 |           18 |   -9.121 |             31 |              31 |      1.268 |      -1.973 | -0.012 |  81.921 |
| PERSINGER G | USA    |     259 |      13 |         0.568 |      0.167 |     -0.239 | -0.008 |           8 |           14 |   -7.15  |             24 |              28 |      1.053 |      -2.593 |  0.002 |  82.776 |
| AOKI G      | JPN    |     215 |      12 |         0.474 |      0.265 |     -0.276 | -0.02  |          17 |           20 |   -4.74  |             18 |              29 |      0.982 |      -1.485 | -0.012 |  71.831 |
| VAN DORP J  | NED    |     235 |      12 |         0.549 |      0.194 |     -0.349 | -0.051 |          14 |           27 |   -7.178 |             33 |              43 |      0.747 |      -1.731 | -0.002 |  78.205 |
| BAUMANN A   | GER    |     202 |      11 |         0.5   |      0.234 |     -0.345 | -0.055 |          12 |           27 |   -7.887 |             24 |              39 |      0.644 |      -0.893 |  0.013 |  67.537 |

### Thirds

| player     | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| NICHOLS M  | CAN    |     262 |      15 |         0.573 |      0.11  |     -0.102 |  0.019 |           1 |            2 |   -2.568 |              6 |               4 |      0.386 |      -0.406 | -0.002 |  87.069 |
| ERIKSSON O | SWE    |     250 |      14 |         0.576 |      0.096 |     -0.111 |  0.008 |           0 |            3 |   -2.636 |              7 |               8 |      0.361 |      -0.582 | -0.015 |  87.249 |
| RUOHONEN R | USA    |     260 |      13 |         0.527 |      0.121 |     -0.118 |  0.008 |           2 |            2 |   -2.377 |             18 |              15 |      0.567 |      -0.478 | -0     |  85.769 |
| HARDIE G   | SCO    |     244 |      14 |         0.541 |      0.123 |     -0.139 |  0.003 |           3 |            4 |   -3.225 |             10 |              13 |      0.712 |      -0.501 | -0.017 |  84.711 |
| RETORNAZ J | ITA    |     220 |      12 |         0.477 |      0.129 |     -0.114 |  0.002 |           4 |            0 |   -2.088 |              8 |               7 |      0.414 |      -0.328 | -0.002 |  80.227 |
| HOEIBERG M | NOR    |     244 |      13 |         0.561 |      0.088 |     -0.112 |  0     |           1 |            2 |   -2.29  |              6 |               7 |      0.398 |      -0.409 | -0.002 |  83.607 |
| GOESGENS W | NED    |     240 |      12 |         0.488 |      0.11  |     -0.11  | -0.003 |           3 |            1 |   -2.103 |              6 |               7 |      0.534 |      -0.408 |  0     |  81.042 |
| SEONG S    | KOR    |     284 |      15 |         0.479 |      0.115 |     -0.116 | -0.006 |           3 |            3 |   -2.791 |             10 |               8 |      0.512 |      -0.422 | -0.005 |  78.887 |
| GLUKHOV S  | RUS    |     212 |      12 |         0.514 |      0.103 |     -0.128 | -0.009 |           1 |            2 |   -2.479 |              4 |              12 |      0.382 |      -0.536 | -0.003 |  74.764 |
| PFISTER E  | SUI    |     234 |      12 |         0.487 |      0.106 |     -0.123 | -0.011 |           1 |            4 |   -3.293 |              7 |              10 |      0.337 |      -0.577 | -0.004 |  80.769 |
| ZOU Q      | CHN    |     226 |      12 |         0.496 |      0.111 |     -0.144 | -0.018 |           1 |            3 |   -2.965 |              5 |              10 |      0.353 |      -0.572 | -0.001 |  81.195 |
| WALTER M   | GER    |     200 |      11 |         0.475 |      0.105 |     -0.136 | -0.022 |           1 |            0 |   -2.139 |              5 |              14 |      0.326 |      -0.41  | -0.004 |  73.995 |
| IWAI M     | JPN    |     216 |      12 |         0.389 |      0.094 |     -0.134 | -0.045 |           0 |            4 |   -2.925 |              4 |               8 |      0.404 |      -0.451 | -0.013 |  75.347 |

### Seconds

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| GALLANT B     | CAN    |     266 |      15 |         0.556 |      0.08  |     -0.066 |  0.015 |           0 |            0 |   -1.312 |              1 |               2 |      0.256 |      -0.261 | -0.011 |  85.338 |
| NEDREGOTTEN M | NOR    |     244 |      13 |         0.611 |      0.063 |     -0.064 |  0.014 |           0 |            0 |   -1.218 |              0 |               1 |      0.227 |      -0.223 | -0.008 |  87.14  |
| LAMMIE B      | SCO    |     244 |      14 |         0.525 |      0.075 |     -0.069 |  0.007 |           0 |            0 |   -1.595 |              5 |               1 |      0.403 |      -0.269 | -0.018 |  87.86  |
| WRANAA R      | SWE    |     252 |      14 |         0.476 |      0.082 |     -0.063 |  0.006 |           0 |            0 |   -1.49  |              3 |               2 |      0.327 |      -0.238 | -0.016 |  87.1   |
| PILZER A      | ITA    |     220 |      12 |         0.559 |      0.074 |     -0.082 |  0.005 |           0 |            0 |   -1.504 |              5 |               1 |      0.301 |      -0.271 | -0.008 |  79.224 |
| OH E          | KOR    |     192 |      10 |         0.562 |      0.065 |     -0.078 |  0.002 |           0 |            0 |   -1.582 |              4 |               2 |      0.28  |      -0.226 | -0.001 |  84.424 |
| MAERKI R      | SUI    |     214 |      11 |         0.481 |      0.071 |     -0.07  | -0.002 |           0 |            0 |   -1.336 |              2 |               1 |      0.336 |      -0.223 | -0.003 |  80.14  |
| HUFMAN C      | USA    |     260 |      13 |         0.519 |      0.059 |     -0.075 | -0.005 |           0 |            0 |   -1.576 |              2 |               5 |      0.269 |      -0.306 | -0.003 |  82.308 |
| KIM M         | KOR    |      92 |       5 |         0.543 |      0.056 |     -0.079 | -0.006 |           0 |            0 |   -1.134 |              0 |               0 |      0.106 |      -0.148 | -0.009 |  85.598 |
| HOEKMAN L     | NED    |     240 |      12 |         0.5   |      0.064 |     -0.076 | -0.006 |           0 |            0 |   -1.537 |              1 |               1 |      0.211 |      -0.243 | -0.004 |  80.104 |
| RAZHABOV A    | RUS    |     232 |      12 |         0.509 |      0.059 |     -0.078 | -0.008 |           0 |            0 |   -1.423 |              0 |               4 |      0.201 |      -0.363 | -0.002 |  81.25  |
| SHUKUYA R     | JPN    |     176 |      10 |         0.472 |      0.066 |     -0.075 | -0.008 |           0 |            0 |   -1.416 |              2 |               1 |      0.281 |      -0.199 | -0.009 |  81.818 |
| XU J          | CHN    |     226 |      12 |         0.46  |      0.066 |     -0.072 | -0.009 |           0 |            0 |   -1.337 |              1 |               0 |      0.274 |      -0.215 | -0.009 |  76.881 |
| HERBERG D     | GER    |     176 |      10 |         0.426 |      0.064 |     -0.081 | -0.019 |           0 |            0 |   -1.185 |              3 |               0 |      0.257 |      -0.166 |  0.005 |  85.227 |

### Leads

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| RIBOTTA F    | ITA    |      36 |       2 |         0.556 |      0.033 |     -0.023 |  0.008 |           0 |            0 |   -0.283 |              0 |               0 |      0.108 |      -0.051 | -0.005 |  95.139 |
| SUNDGREN C   | SWE    |     244 |      14 |         0.553 |      0.039 |     -0.031 |  0.008 |           0 |            0 |   -0.5   |              0 |               0 |      0.111 |      -0.096 |  0.001 |  88.924 |
| MCMILLAN H   | SCO    |     242 |      14 |         0.492 |      0.041 |     -0.031 |  0.004 |           0 |            0 |   -0.747 |              0 |               0 |      0.138 |      -0.109 | -0.002 |  90.064 |
| GLASBERGEN C | NED    |     240 |      12 |         0.525 |      0.038 |     -0.036 |  0.003 |           0 |            0 |   -0.653 |              0 |               0 |      0.139 |      -0.11  |  0.002 |  86.354 |
| VAAGBERG M   | NOR    |     244 |      13 |         0.545 |      0.031 |     -0.031 |  0.003 |           0 |            0 |   -0.785 |              0 |               0 |      0.09  |      -0.125 | -0.002 |  88.946 |
| SHAO Z       | CHN    |     226 |      12 |         0.558 |      0.032 |     -0.037 |  0.002 |           0 |            0 |   -0.598 |              0 |               0 |      0.125 |      -0.112 | -0.002 |  88.496 |
| GEMPELER S   | SUI    |     234 |      12 |         0.538 |      0.035 |     -0.038 |  0.001 |           0 |            0 |   -0.787 |              0 |               0 |      0.145 |      -0.125 | -0     |  87.073 |
| FERRAZZA D   | ITA    |     184 |      10 |         0.549 |      0.032 |     -0.038 |  0     |           0 |            0 |   -0.793 |              0 |               0 |      0.087 |      -0.149 |  0.001 |  82.88  |
| SCHWEIZER S  | GER    |     146 |       8 |         0.521 |      0.032 |     -0.034 |  0     |           0 |            0 |   -0.753 |              0 |               0 |      0.083 |      -0.099 | -0.004 |  88.87  |
| WALKER G     | CAN    |     258 |      15 |         0.469 |      0.036 |     -0.032 | -0     |           0 |            0 |   -0.804 |              0 |               0 |      0.101 |      -0.103 | -0.001 |  89.782 |
| TILKER P     | USA    |     260 |      13 |         0.481 |      0.037 |     -0.037 | -0.001 |           0 |            0 |   -0.707 |              0 |               0 |      0.123 |      -0.146 |  0.003 |  85.7   |
| AOYAMA Y     | JPN    |     156 |       8 |         0.526 |      0.032 |     -0.038 | -0.001 |           0 |            0 |   -0.604 |              0 |               0 |      0.127 |      -0.105 | -0.002 |  86.859 |
| LEE K        | KOR    |     284 |      15 |         0.525 |      0.035 |     -0.042 | -0.002 |           0 |            0 |   -0.875 |              0 |               0 |      0.137 |      -0.176 |  0.002 |  89.134 |
| SHERRARD R   | GER    |     148 |       8 |         0.507 |      0.07  |     -0.079 | -0.003 |           1 |            1 |   -2.469 |              0 |               1 |      0.2   |      -0.188 | -0.006 |  81.081 |
| KLIMOV E     | RUS    |     232 |      12 |         0.474 |      0.033 |     -0.038 | -0.004 |           0 |            0 |   -0.815 |              0 |               0 |      0.147 |      -0.144 |  0     |  86.245 |
| NISATO K     | JPN    |     100 |       6 |         0.42  |      0.049 |     -0.063 | -0.016 |           0 |            0 |   -1.167 |              1 |               0 |      0.171 |      -0.154 | -0.005 |  79.948 |

