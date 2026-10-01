# World Men's Curling Championship (WMCC2022_ResultsBook)

Las Vegas, NV, USA, 2022; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SWE    |      14 | 11-3     |  28.6 |   7   |  18.6 |       1.7 |     1.3 |      70   |
| CAN    |      14 | 11-3     |  28.6 |  -3.5 |  16.4 |      15.3 |     0.3 |      62.5 |
| ITA    |      15 | 10-5     |  16.7 |  -0.8 |  22.4 |      -6.4 |     1.5 |      55.3 |
| SCO    |      13 | 7-6      |   3.8 |   4.7 |  -0.7 |       0.2 |    -0.4 |      53.5 |
| USA    |      15 | 8-7      |   3.3 |  -2.4 |   4.8 |       2.1 |    -1.1 |      49.6 |
| GER    |      12 | 6-6      |   0   |   2   |  -6.5 |       3.2 |     1.3 |      58   |
| KOR    |      12 | 6-6      |   0   |   0   |  -0.9 |       2.8 |    -1.9 |      55   |
| SUI    |      13 | 6-7      |  -3.8 |   4.7 |   3.8 |     -10.8 |    -1.5 |      48.8 |
| CZE    |      12 | 5-7      |  -8.3 |   2   |  -4.2 |      -6.7 |     0.5 |      48.5 |
| NOR    |      12 | 5-7      |  -8.3 |  -2   |  -4.7 |      -1.8 |     0.2 |      46.4 |
| FIN    |      12 | 4-8      | -16.7 |  -2   | -22.8 |       5.3 |     2.9 |      37.8 |
| NED    |      12 | 3-9      | -25   |   0   | -24.5 |       2.4 |    -2.9 |      26.3 |
| DEN    |      12 | 2-10     | -33.3 | -10.2 | -14.7 |      -8   |    -0.4 |      31.7 |

### Fourths

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| RETORNAZ J  | ITA    |     284 |      15 |         0.588 |      0.29  |     -0.282 |  0.055 |          30 |           21 |   -8.047 |             49 |              27 |      1.269 |      -1.337 |  0.003 |  81.004 |
| EDIN N      | SWE    |     253 |      14 |         0.581 |      0.28  |     -0.27  |  0.05  |          21 |           19 |   -6.84  |             35 |              28 |      1.748 |      -1.785 | -0.01  |  82.341 |
| SCHWALLER Y | SUI    |     229 |      13 |         0.572 |      0.278 |     -0.293 |  0.034 |          21 |           17 |   -6.12  |             25 |              25 |      1.213 |      -0.817 |  0.005 |  75.111 |
| GUSHUE B    | CAN    |     248 |      14 |         0.589 |      0.267 |     -0.3   |  0.034 |          22 |           19 |   -5.879 |             31 |              25 |      0.913 |      -1.054 |  0.012 |  80.996 |
| KLIMA L     | CZE    |     211 |      12 |         0.573 |      0.264 |     -0.316 |  0.017 |          18 |           16 |   -7.566 |             13 |              21 |      1.081 |      -0.811 |  0.016 |  75     |
| DROPKIN K   | USA    |     276 |      15 |         0.572 |      0.23  |     -0.304 |  0.002 |          16 |           28 |   -5.478 |             28 |              27 |      1.01  |      -0.855 | -0.003 |  75.092 |
| RAMSFJELL M | NOR    |     228 |      12 |         0.553 |      0.226 |     -0.312 | -0.015 |          17 |           21 |   -7.938 |             26 |              36 |      0.878 |      -1.248 | -0.016 |  75.661 |
| PATERSON R  | SCO    |     250 |      13 |         0.568 |      0.207 |     -0.313 | -0.018 |          11 |           21 |   -7.433 |             25 |              29 |      0.605 |      -1.349 | -0.011 |  75.201 |
| KIM SH      | KOR    |     222 |      12 |         0.541 |      0.262 |     -0.354 | -0.021 |          20 |           26 |   -8.774 |             32 |              35 |      1.068 |      -1.179 | -0.001 |  72.955 |
| KIISKINEN K | FIN    |     211 |      12 |         0.512 |      0.223 |     -0.308 | -0.036 |          13 |           24 |   -5.973 |             18 |              23 |      0.482 |      -0.831 |  0.001 |  71.875 |
| TOTZEK S    | GER    |     213 |      12 |         0.54  |      0.244 |     -0.37  | -0.038 |          18 |           26 |   -8.515 |             17 |              26 |      0.864 |      -1.152 |  0.002 |  74.405 |
| GOESGENS W  | NED    |     228 |      12 |         0.5   |      0.21  |     -0.309 | -0.049 |           9 |           27 |   -7.669 |             20 |              34 |      1     |      -1.091 |  0.004 |  71.571 |
| THUNE T     | DEN    |     204 |      12 |         0.515 |      0.234 |     -0.394 | -0.071 |          13 |           21 |   -9.977 |             25 |              27 |      0.859 |      -1.214 | -0.001 |  69.118 |

### Thirds

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| NICHOLS M     | CAN    |     252 |      14 |         0.591 |      0.149 |     -0.153 |  0.025 |           4 |            2 |   -2.675 |             14 |              10 |      0.349 |      -0.456 |  0.007 |  82.143 |
| MUSKATEWITZ M | GER    |     214 |      12 |         0.537 |      0.153 |     -0.128 |  0.023 |           3 |            2 |   -2.432 |              7 |               6 |      0.387 |      -0.379 | -0.001 |  82.477 |
| BRUNNER M     | SUI    |     230 |      13 |         0.543 |      0.153 |     -0.134 |  0.022 |           6 |            2 |   -2.36  |             13 |              11 |      0.417 |      -0.419 | -0.005 |  78.804 |
| ERIKSSON O    | SWE    |     254 |      14 |         0.567 |      0.138 |     -0.131 |  0.021 |           3 |            0 |   -2.162 |             14 |              12 |      0.464 |      -0.452 | -0.001 |  83.202 |
| POLO J        | USA    |     280 |      15 |         0.596 |      0.129 |     -0.142 |  0.02  |           4 |            5 |   -2.829 |              6 |               7 |      0.378 |      -0.346 | -0.007 |  81.205 |
| SESAKER M     | NOR    |     232 |      12 |         0.595 |      0.124 |     -0.134 |  0.02  |           0 |            3 |   -2.693 |             12 |               7 |      0.419 |      -0.403 | -0.002 |  81.034 |
| MOSANER A     | ITA    |     285 |      15 |         0.579 |      0.132 |     -0.157 |  0.01  |           4 |            4 |   -3.04  |              9 |              18 |      0.502 |      -0.483 | -0.003 |  81.095 |
| WADDELL K     | SCO    |     252 |      13 |         0.563 |      0.113 |     -0.124 |  0.009 |           0 |            5 |   -3.008 |             13 |               5 |      0.355 |      -0.357 | -0.005 |  83.829 |
| CERNOVSKY M   | CZE    |     212 |      12 |         0.467 |      0.147 |     -0.13  | -0.001 |           3 |            1 |   -2.256 |              6 |              10 |      0.459 |      -0.319 |  0.002 |  76.179 |
| KIM CM        | KOR    |     224 |      12 |         0.549 |      0.121 |     -0.155 | -0.003 |           1 |            3 |   -2.838 |             11 |              15 |      0.499 |      -0.564 | -0.002 |  76.674 |
| VAN DORP J    | NED    |     212 |      11 |         0.5   |      0.11  |     -0.136 | -0.013 |           1 |            2 |   -2.513 |              4 |              13 |      0.405 |      -0.47  |  0.006 |  75.825 |
| WIKSTEN K     | DEN    |     202 |      12 |         0.426 |      0.125 |     -0.157 | -0.037 |           1 |            4 |   -3.199 |              8 |              10 |      0.347 |      -0.439 |  0.012 |  73.144 |
| SALO T        | FIN    |     214 |      12 |         0.425 |      0.133 |     -0.166 | -0.039 |           3 |            4 |   -2.926 |              6 |              15 |      0.357 |      -0.409 |  0.021 |  70.305 |

### Seconds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WRANAA R    | SWE    |     252 |      14 |         0.516 |      0.089 |     -0.067 |  0.013 |           1 |            0 |   -1.457 |              7 |               2 |      0.405 |      -0.252 | -0.003 |  84.821 |
| GALLANT B   | CAN    |     248 |      14 |         0.548 |      0.086 |     -0.089 |  0.007 |           1 |            2 |   -2.153 |              3 |               2 |      0.282 |      -0.305 | -0.007 |  84.98  |
| MEIER R     | SUI    |     230 |      13 |         0.548 |      0.078 |     -0.082 |  0.006 |           0 |            0 |   -1.831 |              2 |               2 |      0.253 |      -0.263 | -0.005 |  81.413 |
| SEONG SH    | KOR    |     224 |      12 |         0.5   |      0.097 |     -0.087 |  0.005 |           1 |            0 |   -1.61  |              6 |               4 |      0.345 |      -0.28  |  0.005 |  77.79  |
| ARMAN S     | ITA    |     285 |      15 |         0.516 |      0.083 |     -0.082 |  0.003 |           0 |            0 |   -1.597 |              3 |               3 |      0.295 |      -0.263 |  0.001 |  84.894 |
| SUTOR J     | GER    |     214 |      12 |         0.533 |      0.075 |     -0.082 |  0.002 |           0 |            1 |   -1.953 |              1 |               1 |      0.211 |      -0.189 | -0.005 |  80.869 |
| HOEKMAN L   | NED    |     210 |      11 |         0.49  |      0.087 |     -0.085 | -0     |           1 |            0 |   -2.069 |              3 |               3 |      0.306 |      -0.281 |  0     |  77.381 |
| MENZIES D   | SCO    |     252 |      13 |         0.504 |      0.069 |     -0.073 | -0.001 |           0 |            0 |   -1.658 |              1 |               1 |      0.233 |      -0.262 | -0.002 |  83.829 |
| RAMSFJELL B | NOR    |     232 |      12 |         0.483 |      0.067 |     -0.07  | -0.004 |           0 |            0 |   -1.289 |              1 |               2 |      0.214 |      -0.209 |  0.003 |  82.651 |
| FENNER M    | USA    |     280 |      15 |         0.5   |      0.082 |     -0.092 | -0.005 |           0 |            0 |   -1.808 |              4 |               2 |      0.29  |      -0.244 | -0.006 |  78.339 |
| BOHAC R     | CZE    |     212 |      12 |         0.443 |      0.079 |     -0.075 | -0.007 |           0 |            0 |   -1.441 |              2 |               0 |      0.25  |      -0.189 | -0.001 |  80.071 |
| KRAUSE M    | DEN    |     194 |      12 |         0.423 |      0.09  |     -0.081 | -0.008 |           0 |            0 |   -1.577 |              2 |               2 |      0.246 |      -0.215 |  0.004 |  80.57  |
| OUNI L      | FIN    |     104 |       6 |         0.394 |      0.09  |     -0.108 | -0.03  |           0 |            2 |   -2.197 |              1 |               0 |      0.17  |      -0.177 |  0.007 |  76.442 |

### Leads

| player         | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:---------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WADDELL C      | SCO    |     252 |      13 |         0.587 |      0.031 |     -0.033 |  0.005 |           0 |            0 |   -0.57  |              0 |               0 |      0.14  |      -0.104 | -0.002 |  89.087 |
| SUNDGREN C     | SWE    |     160 |       9 |         0.569 |      0.03  |     -0.032 |  0.003 |           0 |            0 |   -0.74  |              0 |               0 |      0.068 |      -0.117 | -0     |  92.247 |
| GLOOR S        | SUI    |      56 |       3 |         0.643 |      0.029 |     -0.045 |  0.002 |           0 |            0 |   -0.446 |              0 |               0 |      0.048 |      -0.035 | -0.007 |  91.964 |
| GLASBERGEN C   | NED    |     190 |      10 |         0.579 |      0.032 |     -0.039 |  0.002 |           0 |            0 |   -0.695 |              0 |               0 |      0.072 |      -0.116 | -0.005 |  85.526 |
| WALKER G       | CAN    |     250 |      14 |         0.524 |      0.029 |     -0.033 | -0     |           0 |            0 |   -0.713 |              0 |               0 |      0.128 |      -0.115 | -0.003 |  89.257 |
| POULSEN D      | DEN    |      64 |       4 |         0.531 |      0.039 |     -0.046 | -0     |           0 |            0 |   -0.551 |              1 |               0 |      0.104 |      -0.053 | -0.005 |  82.422 |
| GREINDL D      | GER    |     212 |      12 |         0.528 |      0.031 |     -0.038 | -0.001 |           0 |            0 |   -0.581 |              1 |               0 |      0.128 |      -0.103 |  0     |  88.325 |
| MAGNUSSON D    | SWE    |      96 |       6 |         0.531 |      0.034 |     -0.042 | -0.002 |           0 |            0 |   -0.773 |              0 |               0 |      0.065 |      -0.097 |  0.001 |  85     |
| KIM HK         | KOR    |     224 |      12 |         0.518 |      0.031 |     -0.037 | -0.002 |           0 |            0 |   -0.574 |              0 |               0 |      0.091 |      -0.111 | -0.003 |  82.812 |
| HOWELL T       | USA    |     280 |      15 |         0.579 |      0.026 |     -0.042 | -0.003 |           0 |            0 |   -0.634 |              0 |               0 |      0.065 |      -0.104 | -0.003 |  83.123 |
| NEPSTAD G      | NOR    |     232 |      12 |         0.534 |      0.028 |     -0.041 | -0.004 |           0 |            0 |   -0.74  |              0 |               0 |      0.095 |      -0.115 |  0.002 |  80.568 |
| KAEUFELER M    | SUI    |     174 |      10 |         0.511 |      0.033 |     -0.047 | -0.006 |           0 |            0 |   -0.784 |              0 |               0 |      0.092 |      -0.126 | -0.002 |  83.333 |
| CANDRA J       | CZE    |     100 |       6 |         0.46  |      0.028 |     -0.037 | -0.007 |           0 |            0 |   -0.537 |              0 |               0 |      0.051 |      -0.063 | -0.001 |  82     |
| POLLANEN J     | FIN    |     112 |       7 |         0.509 |      0.04  |     -0.057 | -0.008 |           0 |            0 |   -0.864 |              0 |               0 |      0.119 |      -0.112 |  0.002 |  80.357 |
| GONIN S        | ITA    |     282 |      15 |         0.479 |      0.027 |     -0.04  | -0.008 |           0 |            0 |   -0.652 |              0 |               0 |      0.086 |      -0.096 | -0     |  89.388 |
| SOEE OR        | DEN    |     152 |       9 |         0.5   |      0.032 |     -0.049 | -0.008 |           0 |            0 |   -1.074 |              0 |               0 |      0.091 |      -0.111 |  0     |  79.934 |
| KLIPA L        | CZE    |     112 |       7 |         0.482 |      0.026 |     -0.044 | -0.01  |           0 |            0 |   -0.672 |              0 |               0 |      0.055 |      -0.069 | -0.003 |  81.532 |
| VAN DEN HURK T | NED    |      72 |       4 |         0.528 |      0.049 |     -0.089 | -0.016 |           0 |            0 |   -1.473 |              0 |               0 |      0.051 |      -0.124 | -0.002 |  77.778 |
| KUOSMANEN P    | FIN    |     212 |      12 |         0.425 |      0.046 |     -0.063 | -0.017 |           1 |            0 |   -1.441 |              1 |               0 |      0.231 |      -0.159 |  0.005 |  81.84  |

