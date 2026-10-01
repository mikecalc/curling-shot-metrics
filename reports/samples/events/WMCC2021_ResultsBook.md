# World Men's Curling Championship (WMCC2021_ResultsBook)

Calgary, AB, Canada, 2021; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SWE    |      15 | 13-2     |  36.7 |   5.6 |  23   |       4.9 |     3.2 |      66.4 |
| RCF    |      15 | 11-4     |  23.3 |   2.4 |   8.9 |      10.8 |     1.2 |      58.9 |
| USA    |      14 | 10-4     |  21.4 |   1.7 |  18   |       0.1 |     1.5 |      56.8 |
| SCO    |      16 | 11-5     |  18.8 |  -1.5 |  21.9 |      -3.1 |     1.4 |      59.5 |
| CAN    |      14 | 9-5      |  14.3 |   5.1 |  20.8 |     -13.4 |     1.8 |      65.2 |
| SUI    |      16 | 10-6     |  12.5 |   1.5 |  15.1 |      -2.2 |    -1.9 |      60.9 |
| ITA    |      13 | 7-6      |   3.8 |   0.9 |  -3   |       7   |    -1.2 |      55.9 |
| NOR    |      13 | 7-6      |   3.8 |   2.8 | -11.1 |      13.8 |    -1.6 |      55.3 |
| JPN    |      13 | 6-7      |  -3.8 |  -6.5 |  -7.3 |       7.8 |     2.1 |      43.2 |
| GER    |      13 | 4-9      | -19.2 |  -4.6 | -23.4 |      10.2 |    -1.5 |      39.9 |
| DEN    |      13 | 3-10     | -26.9 |  -4.6 | -23   |      -0.3 |     1   |      29.7 |
| CHN    |      13 | 2-11     | -34.6 |  -0.9 |  -9.8 |     -23.1 |    -0.8 |      32.8 |
| NED    |      13 | 2-11     | -34.6 |  -2.8 | -17.8 |      -9.3 |    -4.7 |      32.8 |
| KOR    |      13 | 2-11     | -34.6 |  -0.9 | -28.8 |      -3.5 |    -1.4 |      32.6 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| NED    |      919 |   0.015 |    -0.004 |          0.617 |                2.091 |                   1.984 |
| GER    |      962 |   0.014 |    -0.005 |          0.616 |                2.158 |                   2.103 |
| USA    |     1010 |   0.012 |     0.001 |          0.62  |                2.138 |                   2.186 |
| CHN    |      957 |   0.009 |     0     |          0.626 |                1.999 |                   2.044 |
| JPN    |      912 |   0.003 |     0.001 |          0.605 |                2.171 |                   2.141 |
| ITA    |      920 |   0.003 |    -0.012 |          0.626 |                2.107 |                   2.149 |
| NOR    |      972 |   0.002 |    -0.025 |          0.632 |                2.044 |                   2.226 |
| CAN    |     1079 |  -0.002 |     0.009 |          0.614 |                2.096 |                   2.135 |
| SCO    |     1159 |  -0.002 |     0.027 |          0.592 |                2.148 |                   1.898 |
| DEN    |      895 |  -0.005 |    -0.028 |          0.63  |                2.233 |                   2.229 |
| SWE    |     1085 |  -0.005 |     0.007 |          0.62  |                2.157 |                   1.962 |
| RCF    |     1099 |  -0.009 |     0.01  |          0.57  |                2.041 |                   2.255 |
| KOR    |      889 |  -0.009 |    -0.007 |          0.583 |                2.113 |                   2.302 |
| SUI    |     1185 |  -0.017 |     0.01  |          0.602 |                2.259 |                   2.231 |

### Fourths

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MOUAT B     | SCO    |     290 |      16 |         0.672 |      0.249 |     -0.275 |          27 |           17 |   -6.361 |  0.077 |             54 |              25 |      1.006 |      -0.995 |  0.01  |  85.801 |
| BOTTCHER B  | CAN    |     271 |      14 |         0.616 |      0.245 |     -0.315 |          23 |           25 |   -6.047 |  0.03  |             45 |              30 |      0.864 |      -1.179 |  0.014 |  85.463 |
| SHUSTER J   | USA    |     253 |      14 |         0.601 |      0.247 |     -0.267 |          20 |           16 |   -6.315 |  0.042 |             29 |              25 |      1.491 |      -0.714 |  0.005 |  80.5   |
| EDIN N      | SWE    |     273 |      15 |         0.59  |      0.275 |     -0.269 |          28 |           20 |   -7.069 |  0.052 |             40 |              27 |      1.894 |      -1.597 | -0.001 |  84.907 |
| GLUKHOV S   | RCF    |     275 |      15 |         0.589 |      0.265 |     -0.264 |          18 |           21 |   -4.951 |  0.048 |             45 |              33 |      0.925 |      -1.071 |  0.003 |  80.909 |
| SCHWARZ B   | SUI    |     296 |      16 |         0.588 |      0.275 |     -0.298 |          25 |           21 |   -8.196 |  0.039 |             51 |              32 |      1.205 |      -1.18  | -0.008 |  79.561 |
| RETORNAZ J  | ITA    |     230 |      13 |         0.57  |      0.241 |     -0.315 |          21 |           20 |   -7.078 |  0.002 |             26 |              28 |      0.8   |      -1.171 |  0.007 |  77.632 |
| MATSUMURA Y | JPN    |     226 |      13 |         0.566 |      0.25  |     -0.277 |          14 |           17 |   -6.608 |  0.022 |             22 |              16 |      1.081 |      -1.062 |  0     |  78.125 |
| KRAUSE M    | DEN    |     226 |      13 |         0.531 |      0.298 |     -0.34  |          20 |           25 |   -7.991 | -0.002 |             26 |              37 |      1.329 |      -1.062 |  0.001 |  71.652 |
| TOTZEK S    | GER    |     243 |      13 |         0.523 |      0.272 |     -0.351 |          21 |           28 |   -9.114 | -0.026 |             24 |              38 |      1.048 |      -1.667 | -0     |  75.625 |
| WALSTAD S   | NOR    |     244 |      13 |         0.52  |      0.219 |     -0.264 |          16 |           19 |   -7.292 | -0.012 |             27 |              33 |      0.74  |      -1.855 |  0.014 |  79.959 |
| ZOU Q       | CHN    |     239 |      13 |         0.506 |      0.227 |     -0.317 |          12 |           26 |   -8.798 | -0.042 |             24 |              34 |      0.897 |      -1.098 |  0.001 |  72.059 |
| JEONG YS    | KOR    |     222 |      13 |         0.495 |      0.258 |     -0.388 |          16 |           27 |   -9.444 | -0.068 |             19 |              30 |      0.906 |      -1.684 | -0.002 |  71.171 |
| GOESGENS W  | NED    |     228 |      13 |         0.491 |      0.252 |     -0.31  |          14 |           20 |   -7.978 | -0.034 |             23 |              29 |      0.589 |      -1.075 |  0.012 |  75     |

### Thirds

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| ERIKSSON O    | SWE    |     274 |      15 |         0.588 |      0.133 |     -0.121 |           3 |            2 |   -2.317 |  0.028 |             17 |              10 |      0.434 |      -0.5   |  0.003 |  89.325 |
| TIAN J        | CHN    |     224 |      12 |         0.571 |      0.122 |     -0.13  |           1 |            1 |   -2.501 |  0.014 |              3 |               7 |      0.442 |      -0.41  |  0.007 |  80.357 |
| MOULDING D    | CAN    |     274 |      14 |         0.566 |      0.138 |     -0.148 |           5 |            4 |   -3.556 |  0.014 |             16 |              11 |      0.546 |      -0.575 | -0.004 |  83.12  |
| HARDIE G      | SCO    |     292 |      16 |         0.562 |      0.136 |     -0.147 |           1 |            9 |   -3.774 |  0.012 |             12 |              12 |      0.35  |      -0.553 |  0.001 |  87.5   |
| PLYS C        | USA    |     254 |      14 |         0.559 |      0.121 |     -0.143 |           3 |            3 |   -2.518 |  0.005 |              8 |               9 |      0.429 |      -0.464 |  0.016 |  83.234 |
| MUSKATEWITZ M | GER    |     234 |      13 |         0.543 |      0.147 |     -0.159 |           4 |            4 |   -3.136 |  0.007 |              7 |              10 |      0.446 |      -0.476 |  0.01  |  78.953 |
| MICHEL S      | SUI    |     298 |      16 |         0.537 |      0.115 |     -0.156 |           3 |            6 |   -3.698 | -0.011 |              7 |              11 |      0.398 |      -0.62  | -0.001 |  83.054 |
| SHIMIZU T     | JPN    |     232 |      13 |         0.534 |      0.117 |     -0.165 |           2 |            4 |   -3.029 | -0.014 |              3 |               8 |      0.33  |      -0.422 |  0.001 |  81.573 |
| MOSANER A     | ITA    |     234 |      13 |         0.53  |      0.132 |     -0.12  |           4 |            2 |   -2.52  |  0.014 |             12 |               5 |      0.45  |      -0.371 | -0.009 |  84.722 |
| KLIMOV E      | RCF    |     278 |      15 |         0.518 |      0.135 |     -0.137 |           4 |            2 |   -2.648 |  0.004 |             16 |              13 |      0.496 |      -0.48  | -0.001 |  79.317 |
| VAN DORP J    | NED    |     232 |      13 |         0.5   |      0.113 |     -0.132 |           2 |            1 |   -2.406 | -0.01  |              4 |               8 |      0.313 |      -0.403 | -0.002 |  80.603 |
| NERGAARD T    | NOR    |     246 |      13 |         0.492 |      0.134 |     -0.136 |           5 |            3 |   -3.062 | -0.003 |              8 |              11 |      0.567 |      -0.53  |  0.001 |  77.134 |
| THUNE T       | DEN    |     220 |      13 |         0.473 |      0.116 |     -0.167 |           1 |            9 |   -3.333 | -0.033 |              5 |              11 |      0.35  |      -0.567 |  0.003 |  77.386 |
| KIM JM        | KOR    |     224 |      13 |         0.406 |      0.114 |     -0.137 |           1 |            4 |   -3.486 | -0.035 |              3 |               8 |      0.34  |      -0.531 |  0.003 |  77.902 |

### Seconds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| DE CRUZ P   | SUI    |     298 |      16 |         0.604 |      0.06  |     -0.07  |           0 |            0 |   -1.382 |  0.009 |              2 |               1 |      0.27  |      -0.228 | -0.003 |  85.319 |
| ARMAN S     | ITA    |     234 |      13 |         0.487 |      0.074 |     -0.084 |           0 |            1 |   -2.032 | -0.007 |              2 |               3 |      0.24  |      -0.379 |  0.001 |  85.363 |
| PARK SW     | KOR    |     224 |      13 |         0.482 |      0.085 |     -0.114 |           2 |            1 |   -2.353 | -0.018 |              3 |               3 |      0.292 |      -0.312 |  0.002 |  76.674 |
| HAMILTON M  | USA    |     252 |      14 |         0.476 |      0.074 |     -0.069 |           0 |            0 |   -1.502 | -0.001 |              2 |               1 |      0.286 |      -0.2   |  0.005 |  83.036 |
| WRANAA R    | SWE    |     274 |      15 |         0.474 |      0.079 |     -0.078 |           0 |            0 |   -1.568 | -0.004 |              2 |               4 |      0.246 |      -0.281 |  0     |  88.777 |
| SUTOR J     | GER    |     244 |      13 |         0.467 |      0.065 |     -0.098 |           0 |            1 |   -2.335 | -0.022 |              1 |               6 |      0.216 |      -0.329 | -0.002 |  77.254 |
| TANIDA Y    | JPN    |     232 |      13 |         0.461 |      0.064 |     -0.077 |           0 |            0 |   -1.561 | -0.012 |              0 |               2 |      0.168 |      -0.211 | -0.009 |  83.082 |
| MIRONOV D   | RCF    |     278 |      15 |         0.457 |      0.074 |     -0.066 |           0 |            1 |   -1.858 | -0.002 |              4 |               1 |      0.364 |      -0.212 | -0.003 |  84.432 |
| WANG Z      | CHN    |     240 |      13 |         0.454 |      0.087 |     -0.097 |           1 |            2 |   -2.547 | -0.013 |              4 |               5 |      0.308 |      -0.386 | -0.001 |  78.229 |
| THIESSEN B  | CAN    |     274 |      14 |         0.449 |      0.063 |     -0.089 |           0 |            1 |   -2.044 | -0.02  |              1 |               3 |      0.209 |      -0.258 |  0.003 |  85.858 |
| LAMMIE B    | SCO    |     292 |      16 |         0.445 |      0.077 |     -0.081 |           0 |            1 |   -2.067 | -0.011 |              2 |               3 |      0.263 |      -0.286 | -0.001 |  85.616 |
| HOEIBERG M  | NOR    |     246 |      13 |         0.443 |      0.064 |     -0.074 |           0 |            0 |   -1.37  | -0.013 |              1 |               2 |      0.228 |      -0.218 | -0.003 |  83.673 |
| NOERGAARD M | DEN    |     226 |      13 |         0.416 |      0.056 |     -0.098 |           0 |            2 |   -2.406 | -0.034 |              1 |               2 |      0.187 |      -0.243 |  0.003 |  72.898 |
| HOEKMAN L   | NED    |     232 |      13 |         0.388 |      0.071 |     -0.078 |           0 |            1 |   -1.73  | -0.02  |              1 |               1 |      0.187 |      -0.22  |  0.003 |  78.448 |

### Leads

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SOEE OR       | DEN    |      52 |       4 |         0.654 |      0.026 |     -0.042 |           0 |            0 |   -0.503 |  0.003 |              0 |               0 |      0.027 |      -0.053 |  0     |  81.25  |
| TANNER V      | SUI    |     296 |      16 |         0.591 |      0.033 |     -0.029 |           0 |            0 |   -0.798 |  0.007 |              0 |               0 |      0.134 |      -0.147 | -0.001 |  92.821 |
| MCMILLAN H    | SCO    |     288 |      16 |         0.556 |      0.029 |     -0.029 |           0 |            0 |   -0.623 |  0.003 |              0 |               0 |      0.102 |      -0.122 | -0.002 |  90.941 |
| XU J          | CHN    |     240 |      13 |         0.533 |      0.028 |     -0.033 |           0 |            0 |   -0.686 | -0.001 |              0 |               0 |      0.115 |      -0.093 |  0.001 |  89.375 |
| GLASBERGEN C  | NED    |     232 |      13 |         0.53  |      0.033 |     -0.033 |           0 |            0 |   -0.639 |  0.002 |              0 |               0 |      0.07  |      -0.103 |  0.001 |  89.009 |
| MARTIN K      | CAN    |     274 |      14 |         0.518 |      0.03  |     -0.03  |           0 |            0 |   -0.566 |  0.001 |              0 |               0 |      0.079 |      -0.085 |  0.006 |  90.693 |
| SUNDGREN C    | SWE    |     272 |      15 |         0.5   |      0.031 |     -0.025 |           0 |            0 |   -0.601 |  0.003 |              0 |               0 |      0.111 |      -0.114 |  0.001 |  91.085 |
| KALALB A      | RCF    |     260 |      14 |         0.5   |      0.027 |     -0.027 |           0 |            0 |   -0.606 | -0     |              0 |               0 |      0.09  |      -0.101 | -0.001 |  85.156 |
| SEO MG        | KOR    |      32 |       2 |         0.5   |      0.03  |     -0.03  |           0 |            0 |   -0.362 | -0     |              0 |               0 |      0.037 |      -0.038 |  0.003 |  89.062 |
| VAAGBERG M    | NOR    |     246 |      13 |         0.496 |      0.033 |     -0.031 |           0 |            0 |   -0.839 |  0.001 |              0 |               0 |      0.121 |      -0.14  |  0.002 |  86.28  |
| LEE JH        | KOR    |     192 |      11 |         0.495 |      0.023 |     -0.035 |           0 |            0 |   -0.683 | -0.006 |              0 |               0 |      0.049 |      -0.107 |  0     |  87.37  |
| GREINDL D     | GER    |     244 |      13 |         0.488 |      0.035 |     -0.027 |           0 |            0 |   -0.609 |  0.003 |              0 |               0 |      0.103 |      -0.106 |  0.001 |  87.346 |
| GIOVANELLA M  | ITA    |     234 |      13 |         0.483 |      0.033 |     -0.037 |           0 |            0 |   -0.763 | -0.003 |              0 |               0 |      0.085 |      -0.106 |  0.001 |  87.931 |
| LANDSTEINER J | USA    |     232 |      13 |         0.466 |      0.031 |     -0.031 |           0 |            0 |   -0.722 | -0.002 |              0 |               0 |      0.087 |      -0.116 | -0.002 |  87.013 |
| WIKSTEN K     | DEN    |     180 |      10 |         0.456 |      0.037 |     -0.053 |           0 |            0 |   -1.434 | -0.012 |              0 |               3 |      0.101 |      -0.286 |  0.004 |  84.722 |
| ABE S         | JPN    |     232 |      13 |         0.453 |      0.03  |     -0.03  |           0 |            0 |   -0.619 | -0.003 |              0 |               0 |      0.091 |      -0.082 |  0.002 |  87.823 |

