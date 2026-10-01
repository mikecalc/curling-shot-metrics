# World Men's Curling Championship (WMCC2018_ResultsBook)

Las Vegas, NV, United States, 2018; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

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

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| NOR    |      965 |   0.027 |    -0.017 |          0.648 |                1.649 |                   2.222 |
| GER    |      864 |   0.024 |    -0.042 |          0.674 |                2.007 |                   2.092 |
| CHN    |      895 |   0.012 |    -0.019 |          0.617 |                1.758 |                   2.056 |
| NED    |      944 |   0.011 |    -0.026 |          0.629 |                1.843 |                   1.944 |
| SUI    |      922 |   0.003 |    -0.002 |          0.603 |                1.963 |                   1.966 |
| RUS    |      918 |   0.002 |     0.019 |          0.559 |                2.042 |                   1.788 |
| KOR    |     1119 |   0.001 |    -0.006 |          0.605 |                1.913 |                   1.962 |
| ITA    |      871 |   0.001 |     0.005 |          0.61  |                1.944 |                   1.953 |
| USA    |     1023 |  -0.001 |    -0.002 |          0.587 |                1.769 |                   2.067 |
| CAN    |     1055 |  -0.002 |     0.013 |          0.599 |                2.15  |                   1.863 |
| SCO    |      966 |  -0.022 |     0.043 |          0.519 |                2.088 |                   1.857 |
| JPN    |      846 |  -0.023 |    -0.012 |          0.595 |                2.014 |                   1.934 |
| SWE    |      988 |  -0.031 |     0.038 |          0.512 |                2.158 |                   1.596 |

### Fourths

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| EDIN N      | SWE    |     250 |      14 |         0.684 |      0.202 |     -0.258 |          18 |           14 |   -6.659 |  0.056 |             32 |              19 |      1.156 |      -1.233 | -0.007 |  89.415 |
| GUSHUE B    | CAN    |     264 |      15 |         0.648 |      0.225 |     -0.266 |          22 |           15 |   -7.013 |  0.052 |             34 |              20 |      1.23  |      -1.695 |  0.005 |  85.701 |
| MOUAT B     | SCO    |     244 |      14 |         0.615 |      0.259 |     -0.296 |          22 |           20 |   -5.724 |  0.045 |             37 |              33 |      1.229 |      -0.919 | -0.016 |  81.455 |
| MOSANER A   | ITA    |     219 |      12 |         0.603 |      0.236 |     -0.313 |          17 |           22 |   -6.572 |  0.018 |             29 |              24 |      0.806 |      -1.685 |  0.004 |  79.263 |
| ZOU D       | CHN    |     225 |      12 |         0.6   |      0.224 |     -0.328 |          16 |           19 |   -8.043 |  0.003 |             25 |              22 |      0.653 |      -0.923 |  0.009 |  78.139 |
| PERSINGER G | USA    |     259 |      13 |         0.568 |      0.167 |     -0.239 |           8 |           14 |   -7.15  | -0.008 |             24 |              28 |      1.053 |      -2.593 |  0.002 |  82.776 |
| KIM C       | KOR    |     284 |      15 |         0.567 |      0.271 |     -0.324 |          20 |           25 |   -8.523 |  0.013 |             42 |              39 |      1.317 |      -1.828 |  0.008 |  78.136 |
| VAN DORP J  | NED    |     235 |      12 |         0.549 |      0.194 |     -0.349 |          14 |           27 |   -7.178 | -0.051 |             33 |              43 |      0.747 |      -1.731 | -0.002 |  78.205 |
| WALSTAD S   | NOR    |     243 |      13 |         0.543 |      0.226 |     -0.283 |          14 |           18 |   -9.121 | -0.007 |             31 |              31 |      1.268 |      -1.973 | -0.012 |  81.921 |
| TIMOFEEV A  | RUS    |     230 |      12 |         0.53  |      0.229 |     -0.258 |          12 |           18 |   -6.48  |  0     |             35 |              28 |      1.148 |      -1.436 | -0.002 |  76.747 |
| PFISTER M   | SUI    |     232 |      12 |         0.513 |      0.206 |     -0.222 |           9 |           16 |   -5.187 | -0.002 |             28 |              30 |      0.807 |      -0.995 |  0.002 |  78.634 |
| BAUMANN A   | GER    |     202 |      11 |         0.5   |      0.234 |     -0.345 |          12 |           27 |   -7.887 | -0.055 |             24 |              39 |      0.644 |      -0.893 |  0.013 |  67.537 |
| AOKI G      | JPN    |     215 |      12 |         0.474 |      0.265 |     -0.276 |          17 |           20 |   -4.74  | -0.02  |             18 |              29 |      0.982 |      -1.485 | -0.012 |  71.831 |

### Thirds

| player     | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| ERIKSSON O | SWE    |     250 |      14 |         0.576 |      0.096 |     -0.111 |           0 |            3 |   -2.636 |  0.008 |              7 |               8 |      0.361 |      -0.582 | -0.015 |  87.249 |
| NICHOLS M  | CAN    |     262 |      15 |         0.573 |      0.11  |     -0.102 |           1 |            2 |   -2.568 |  0.019 |              6 |               4 |      0.386 |      -0.406 | -0.002 |  87.069 |
| HOEIBERG M | NOR    |     244 |      13 |         0.561 |      0.088 |     -0.112 |           1 |            2 |   -2.29  |  0     |              6 |               7 |      0.398 |      -0.409 | -0.002 |  83.607 |
| HARDIE G   | SCO    |     244 |      14 |         0.541 |      0.123 |     -0.139 |           3 |            4 |   -3.225 |  0.003 |             10 |              13 |      0.712 |      -0.501 | -0.017 |  84.711 |
| RUOHONEN R | USA    |     260 |      13 |         0.527 |      0.121 |     -0.118 |           2 |            2 |   -2.377 |  0.008 |             18 |              15 |      0.567 |      -0.478 | -0     |  85.769 |
| GLUKHOV S  | RUS    |     212 |      12 |         0.514 |      0.103 |     -0.128 |           1 |            2 |   -2.479 | -0.009 |              4 |              12 |      0.382 |      -0.536 | -0.003 |  74.764 |
| ZOU Q      | CHN    |     226 |      12 |         0.496 |      0.111 |     -0.144 |           1 |            3 |   -2.965 | -0.018 |              5 |              10 |      0.353 |      -0.572 | -0.001 |  81.195 |
| GOESGENS W | NED    |     240 |      12 |         0.488 |      0.11  |     -0.11  |           3 |            1 |   -2.103 | -0.003 |              6 |               7 |      0.534 |      -0.408 |  0     |  81.042 |
| PFISTER E  | SUI    |     234 |      12 |         0.487 |      0.106 |     -0.123 |           1 |            4 |   -3.293 | -0.011 |              7 |              10 |      0.337 |      -0.577 | -0.004 |  80.769 |
| SEONG S    | KOR    |     284 |      15 |         0.479 |      0.115 |     -0.116 |           3 |            3 |   -2.791 | -0.006 |             10 |               8 |      0.512 |      -0.422 | -0.005 |  78.887 |
| RETORNAZ J | ITA    |     220 |      12 |         0.477 |      0.129 |     -0.114 |           4 |            0 |   -2.088 |  0.002 |              8 |               7 |      0.414 |      -0.328 | -0.002 |  80.227 |
| WALTER M   | GER    |     200 |      11 |         0.475 |      0.105 |     -0.136 |           1 |            0 |   -2.139 | -0.022 |              5 |              14 |      0.326 |      -0.41  | -0.004 |  73.995 |
| IWAI M     | JPN    |     216 |      12 |         0.389 |      0.094 |     -0.134 |           0 |            4 |   -2.925 | -0.045 |              4 |               8 |      0.404 |      -0.451 | -0.013 |  75.347 |

### Seconds

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| NEDREGOTTEN M | NOR    |     244 |      13 |         0.611 |      0.063 |     -0.064 |           0 |            0 |   -1.218 |  0.014 |              0 |               1 |      0.227 |      -0.223 | -0.008 |  87.14  |
| OH E          | KOR    |     192 |      10 |         0.562 |      0.065 |     -0.078 |           0 |            0 |   -1.582 |  0.002 |              4 |               2 |      0.28  |      -0.226 | -0.001 |  84.424 |
| PILZER A      | ITA    |     220 |      12 |         0.559 |      0.074 |     -0.082 |           0 |            0 |   -1.504 |  0.005 |              5 |               1 |      0.301 |      -0.271 | -0.008 |  79.224 |
| GALLANT B     | CAN    |     266 |      15 |         0.556 |      0.08  |     -0.066 |           0 |            0 |   -1.312 |  0.015 |              1 |               2 |      0.256 |      -0.261 | -0.011 |  85.338 |
| KIM M         | KOR    |      92 |       5 |         0.543 |      0.056 |     -0.079 |           0 |            0 |   -1.134 | -0.006 |              0 |               0 |      0.106 |      -0.148 | -0.009 |  85.598 |
| LAMMIE B      | SCO    |     244 |      14 |         0.525 |      0.075 |     -0.069 |           0 |            0 |   -1.595 |  0.007 |              5 |               1 |      0.403 |      -0.269 | -0.018 |  87.86  |
| HUFMAN C      | USA    |     260 |      13 |         0.519 |      0.059 |     -0.075 |           0 |            0 |   -1.576 | -0.005 |              2 |               5 |      0.269 |      -0.306 | -0.003 |  82.308 |
| RAZHABOV A    | RUS    |     232 |      12 |         0.509 |      0.059 |     -0.078 |           0 |            0 |   -1.423 | -0.008 |              0 |               4 |      0.201 |      -0.363 | -0.002 |  81.25  |
| HOEKMAN L     | NED    |     240 |      12 |         0.5   |      0.064 |     -0.076 |           0 |            0 |   -1.537 | -0.006 |              1 |               1 |      0.211 |      -0.243 | -0.004 |  80.104 |
| MAERKI R      | SUI    |     214 |      11 |         0.481 |      0.071 |     -0.07  |           0 |            0 |   -1.336 | -0.002 |              2 |               1 |      0.336 |      -0.223 | -0.003 |  80.14  |
| WRANAA R      | SWE    |     252 |      14 |         0.476 |      0.082 |     -0.063 |           0 |            0 |   -1.49  |  0.006 |              3 |               2 |      0.327 |      -0.238 | -0.016 |  87.1   |
| SHUKUYA R     | JPN    |     176 |      10 |         0.472 |      0.066 |     -0.075 |           0 |            0 |   -1.416 | -0.008 |              2 |               1 |      0.281 |      -0.199 | -0.009 |  81.818 |
| XU J          | CHN    |     226 |      12 |         0.46  |      0.066 |     -0.072 |           0 |            0 |   -1.337 | -0.009 |              1 |               0 |      0.274 |      -0.215 | -0.009 |  76.881 |
| HERBERG D     | GER    |     176 |      10 |         0.426 |      0.064 |     -0.081 |           0 |            0 |   -1.185 | -0.019 |              3 |               0 |      0.257 |      -0.166 |  0.005 |  85.227 |

### Leads

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SHAO Z       | CHN    |     226 |      12 |         0.558 |      0.032 |     -0.037 |           0 |            0 |   -0.598 |  0.002 |              0 |               0 |      0.125 |      -0.112 | -0.002 |  88.496 |
| RIBOTTA F    | ITA    |      36 |       2 |         0.556 |      0.033 |     -0.023 |           0 |            0 |   -0.283 |  0.008 |              0 |               0 |      0.108 |      -0.051 | -0.005 |  95.139 |
| SUNDGREN C   | SWE    |     244 |      14 |         0.553 |      0.039 |     -0.031 |           0 |            0 |   -0.5   |  0.008 |              0 |               0 |      0.111 |      -0.096 |  0.001 |  88.924 |
| FERRAZZA D   | ITA    |     184 |      10 |         0.549 |      0.032 |     -0.038 |           0 |            0 |   -0.793 |  0     |              0 |               0 |      0.087 |      -0.149 |  0.001 |  82.88  |
| VAAGBERG M   | NOR    |     244 |      13 |         0.545 |      0.031 |     -0.031 |           0 |            0 |   -0.785 |  0.003 |              0 |               0 |      0.09  |      -0.125 | -0.002 |  88.946 |
| GEMPELER S   | SUI    |     234 |      12 |         0.538 |      0.035 |     -0.038 |           0 |            0 |   -0.787 |  0.001 |              0 |               0 |      0.145 |      -0.125 | -0     |  87.073 |
| AOYAMA Y     | JPN    |     156 |       8 |         0.526 |      0.032 |     -0.038 |           0 |            0 |   -0.604 | -0.001 |              0 |               0 |      0.127 |      -0.105 | -0.002 |  86.859 |
| GLASBERGEN C | NED    |     240 |      12 |         0.525 |      0.038 |     -0.036 |           0 |            0 |   -0.653 |  0.003 |              0 |               0 |      0.139 |      -0.11  |  0.002 |  86.354 |
| LEE K        | KOR    |     284 |      15 |         0.525 |      0.035 |     -0.042 |           0 |            0 |   -0.875 | -0.002 |              0 |               0 |      0.137 |      -0.176 |  0.002 |  89.134 |
| SCHWEIZER S  | GER    |     146 |       8 |         0.521 |      0.032 |     -0.034 |           0 |            0 |   -0.753 |  0     |              0 |               0 |      0.083 |      -0.099 | -0.004 |  88.87  |
| SHERRARD R   | GER    |     148 |       8 |         0.507 |      0.07  |     -0.079 |           1 |            1 |   -2.469 | -0.003 |              0 |               1 |      0.2   |      -0.188 | -0.006 |  81.081 |
| MCMILLAN H   | SCO    |     242 |      14 |         0.492 |      0.041 |     -0.031 |           0 |            0 |   -0.747 |  0.004 |              0 |               0 |      0.138 |      -0.109 | -0.002 |  90.064 |
| TILKER P     | USA    |     260 |      13 |         0.481 |      0.037 |     -0.037 |           0 |            0 |   -0.707 | -0.001 |              0 |               0 |      0.123 |      -0.146 |  0.003 |  85.7   |
| KLIMOV E     | RUS    |     232 |      12 |         0.474 |      0.033 |     -0.038 |           0 |            0 |   -0.815 | -0.004 |              0 |               0 |      0.147 |      -0.144 |  0     |  86.245 |
| WALKER G     | CAN    |     258 |      15 |         0.469 |      0.036 |     -0.032 |           0 |            0 |   -0.804 | -0     |              0 |               0 |      0.101 |      -0.103 | -0.001 |  89.782 |
| NISATO K     | JPN    |     100 |       6 |         0.42  |      0.049 |     -0.063 |           0 |            0 |   -1.167 | -0.016 |              1 |               0 |      0.171 |      -0.154 | -0.005 |  79.948 |

