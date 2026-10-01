# World Men's Curling Championship (WMCC2022_ResultsBook)

Las Vegas, NV, USA, 2022; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

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

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| NOR    |      905 |   0.015 |    -0.005 |          0.617 |                2.097 |                   1.958 |
| CZE    |      833 |   0.012 |    -0     |          0.618 |                1.979 |                   1.995 |
| SUI    |      911 |   0.01  |    -0.001 |          0.625 |                2.077 |                   2.271 |
| NED    |      909 |   0.008 |    -0.009 |          0.623 |                2.028 |                   2.055 |
| FIN    |      846 |   0.006 |    -0.006 |          0.645 |                2.165 |                   2.164 |
| SWE    |     1005 |   0.004 |     0.004 |          0.598 |                2.198 |                   2.102 |
| CAN    |     1003 |   0.004 |     0     |          0.608 |                2.439 |                   2.207 |
| GER    |      843 |  -0.003 |    -0.001 |          0.617 |                2.184 |                   2.177 |
| KOR    |      883 |  -0.007 |    -0.01  |          0.598 |                2.148 |                   2.21  |
| USA    |     1100 |  -0.007 |    -0.002 |          0.596 |                1.991 |                   2.189 |
| SCO    |     1002 |  -0.011 |     0.012 |          0.587 |                2.045 |                   2.03  |
| ITA    |     1122 |  -0.011 |     0.011 |          0.596 |                2.38  |                   2.198 |
| DEN    |      810 |  -0.017 |     0.001 |          0.588 |                2.023 |                   2.2   |

### Fourths

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| GUSHUE B    | CAN    |     248 |      14 |         0.589 |      0.267 |     -0.3   |          22 |           19 |   -5.879 |  0.034 |             31 |              25 |      0.913 |      -1.054 |  0.012 |  80.996 |
| RETORNAZ J  | ITA    |     284 |      15 |         0.588 |      0.29  |     -0.282 |          30 |           21 |   -8.047 |  0.055 |             49 |              27 |      1.269 |      -1.337 |  0.003 |  81.004 |
| EDIN N      | SWE    |     253 |      14 |         0.581 |      0.28  |     -0.27  |          21 |           19 |   -6.84  |  0.05  |             35 |              28 |      1.748 |      -1.785 | -0.01  |  82.341 |
| KLIMA L     | CZE    |     211 |      12 |         0.573 |      0.264 |     -0.316 |          18 |           16 |   -7.566 |  0.017 |             13 |              21 |      1.081 |      -0.811 |  0.016 |  75     |
| DROPKIN K   | USA    |     276 |      15 |         0.572 |      0.23  |     -0.304 |          16 |           28 |   -5.478 |  0.002 |             28 |              27 |      1.01  |      -0.855 | -0.003 |  75.092 |
| SCHWALLER Y | SUI    |     229 |      13 |         0.572 |      0.278 |     -0.293 |          21 |           17 |   -6.12  |  0.034 |             25 |              25 |      1.213 |      -0.817 |  0.005 |  75.111 |
| PATERSON R  | SCO    |     250 |      13 |         0.568 |      0.207 |     -0.313 |          11 |           21 |   -7.433 | -0.018 |             25 |              29 |      0.605 |      -1.349 | -0.011 |  75.201 |
| RAMSFJELL M | NOR    |     228 |      12 |         0.553 |      0.226 |     -0.312 |          17 |           21 |   -7.938 | -0.015 |             26 |              36 |      0.878 |      -1.248 | -0.016 |  75.661 |
| KIM SH      | KOR    |     222 |      12 |         0.541 |      0.262 |     -0.354 |          20 |           26 |   -8.774 | -0.021 |             32 |              35 |      1.068 |      -1.179 | -0.001 |  72.955 |
| TOTZEK S    | GER    |     213 |      12 |         0.54  |      0.244 |     -0.37  |          18 |           26 |   -8.515 | -0.038 |             17 |              26 |      0.864 |      -1.152 |  0.002 |  74.405 |
| THUNE T     | DEN    |     204 |      12 |         0.515 |      0.234 |     -0.394 |          13 |           21 |   -9.977 | -0.071 |             25 |              27 |      0.859 |      -1.214 | -0.001 |  69.118 |
| KIISKINEN K | FIN    |     211 |      12 |         0.512 |      0.223 |     -0.308 |          13 |           24 |   -5.973 | -0.036 |             18 |              23 |      0.482 |      -0.831 |  0.001 |  71.875 |
| GOESGENS W  | NED    |     228 |      12 |         0.5   |      0.21  |     -0.309 |           9 |           27 |   -7.669 | -0.049 |             20 |              34 |      1     |      -1.091 |  0.004 |  71.571 |

### Thirds

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| POLO J        | USA    |     280 |      15 |         0.596 |      0.129 |     -0.142 |           4 |            5 |   -2.829 |  0.02  |              6 |               7 |      0.378 |      -0.346 | -0.007 |  81.205 |
| SESAKER M     | NOR    |     232 |      12 |         0.595 |      0.124 |     -0.134 |           0 |            3 |   -2.693 |  0.02  |             12 |               7 |      0.419 |      -0.403 | -0.002 |  81.034 |
| NICHOLS M     | CAN    |     252 |      14 |         0.591 |      0.149 |     -0.153 |           4 |            2 |   -2.675 |  0.025 |             14 |              10 |      0.349 |      -0.456 |  0.007 |  82.143 |
| MOSANER A     | ITA    |     285 |      15 |         0.579 |      0.132 |     -0.157 |           4 |            4 |   -3.04  |  0.01  |              9 |              18 |      0.502 |      -0.483 | -0.003 |  81.095 |
| ERIKSSON O    | SWE    |     254 |      14 |         0.567 |      0.138 |     -0.131 |           3 |            0 |   -2.162 |  0.021 |             14 |              12 |      0.464 |      -0.452 | -0.001 |  83.202 |
| WADDELL K     | SCO    |     252 |      13 |         0.563 |      0.113 |     -0.124 |           0 |            5 |   -3.008 |  0.009 |             13 |               5 |      0.355 |      -0.357 | -0.005 |  83.829 |
| KIM CM        | KOR    |     224 |      12 |         0.549 |      0.121 |     -0.155 |           1 |            3 |   -2.838 | -0.003 |             11 |              15 |      0.499 |      -0.564 | -0.002 |  76.674 |
| BRUNNER M     | SUI    |     230 |      13 |         0.543 |      0.153 |     -0.134 |           6 |            2 |   -2.36  |  0.022 |             13 |              11 |      0.417 |      -0.419 | -0.005 |  78.804 |
| MUSKATEWITZ M | GER    |     214 |      12 |         0.537 |      0.153 |     -0.128 |           3 |            2 |   -2.432 |  0.023 |              7 |               6 |      0.387 |      -0.379 | -0.001 |  82.477 |
| VAN DORP J    | NED    |     212 |      11 |         0.5   |      0.11  |     -0.136 |           1 |            2 |   -2.513 | -0.013 |              4 |              13 |      0.405 |      -0.47  |  0.006 |  75.825 |
| CERNOVSKY M   | CZE    |     212 |      12 |         0.467 |      0.147 |     -0.13  |           3 |            1 |   -2.256 | -0.001 |              6 |              10 |      0.459 |      -0.319 |  0.002 |  76.179 |
| WIKSTEN K     | DEN    |     202 |      12 |         0.426 |      0.125 |     -0.157 |           1 |            4 |   -3.199 | -0.037 |              8 |              10 |      0.347 |      -0.439 |  0.012 |  73.144 |
| SALO T        | FIN    |     214 |      12 |         0.425 |      0.133 |     -0.166 |           3 |            4 |   -2.926 | -0.039 |              6 |              15 |      0.357 |      -0.409 |  0.021 |  70.305 |

### Seconds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| GALLANT B   | CAN    |     248 |      14 |         0.548 |      0.086 |     -0.089 |           1 |            2 |   -2.153 |  0.007 |              3 |               2 |      0.282 |      -0.305 | -0.007 |  84.98  |
| MEIER R     | SUI    |     230 |      13 |         0.548 |      0.078 |     -0.082 |           0 |            0 |   -1.831 |  0.006 |              2 |               2 |      0.253 |      -0.263 | -0.005 |  81.413 |
| SUTOR J     | GER    |     214 |      12 |         0.533 |      0.075 |     -0.082 |           0 |            1 |   -1.953 |  0.002 |              1 |               1 |      0.211 |      -0.189 | -0.005 |  80.869 |
| WRANAA R    | SWE    |     252 |      14 |         0.516 |      0.089 |     -0.067 |           1 |            0 |   -1.457 |  0.013 |              7 |               2 |      0.405 |      -0.252 | -0.003 |  84.821 |
| ARMAN S     | ITA    |     285 |      15 |         0.516 |      0.083 |     -0.082 |           0 |            0 |   -1.597 |  0.003 |              3 |               3 |      0.295 |      -0.263 |  0.001 |  84.894 |
| MENZIES D   | SCO    |     252 |      13 |         0.504 |      0.069 |     -0.073 |           0 |            0 |   -1.658 | -0.001 |              1 |               1 |      0.233 |      -0.262 | -0.002 |  83.829 |
| SEONG SH    | KOR    |     224 |      12 |         0.5   |      0.097 |     -0.087 |           1 |            0 |   -1.61  |  0.005 |              6 |               4 |      0.345 |      -0.28  |  0.005 |  77.79  |
| FENNER M    | USA    |     280 |      15 |         0.5   |      0.082 |     -0.092 |           0 |            0 |   -1.808 | -0.005 |              4 |               2 |      0.29  |      -0.244 | -0.006 |  78.339 |
| HOEKMAN L   | NED    |     210 |      11 |         0.49  |      0.087 |     -0.085 |           1 |            0 |   -2.069 | -0     |              3 |               3 |      0.306 |      -0.281 |  0     |  77.381 |
| RAMSFJELL B | NOR    |     232 |      12 |         0.483 |      0.067 |     -0.07  |           0 |            0 |   -1.289 | -0.004 |              1 |               2 |      0.214 |      -0.209 |  0.003 |  82.651 |
| BOHAC R     | CZE    |     212 |      12 |         0.443 |      0.079 |     -0.075 |           0 |            0 |   -1.441 | -0.007 |              2 |               0 |      0.25  |      -0.189 | -0.001 |  80.071 |
| KRAUSE M    | DEN    |     194 |      12 |         0.423 |      0.09  |     -0.081 |           0 |            0 |   -1.577 | -0.008 |              2 |               2 |      0.246 |      -0.215 |  0.004 |  80.57  |
| OUNI L      | FIN    |     104 |       6 |         0.394 |      0.09  |     -0.108 |           0 |            2 |   -2.197 | -0.03  |              1 |               0 |      0.17  |      -0.177 |  0.007 |  76.442 |

### Leads

| player         | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:---------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| GLOOR S        | SUI    |      56 |       3 |         0.643 |      0.029 |     -0.045 |           0 |            0 |   -0.446 |  0.002 |              0 |               0 |      0.048 |      -0.035 | -0.007 |  91.964 |
| WADDELL C      | SCO    |     252 |      13 |         0.587 |      0.031 |     -0.033 |           0 |            0 |   -0.57  |  0.005 |              0 |               0 |      0.14  |      -0.104 | -0.002 |  89.087 |
| GLASBERGEN C   | NED    |     190 |      10 |         0.579 |      0.032 |     -0.039 |           0 |            0 |   -0.695 |  0.002 |              0 |               0 |      0.072 |      -0.116 | -0.005 |  85.526 |
| HOWELL T       | USA    |     280 |      15 |         0.579 |      0.026 |     -0.042 |           0 |            0 |   -0.634 | -0.003 |              0 |               0 |      0.065 |      -0.104 | -0.003 |  83.123 |
| SUNDGREN C     | SWE    |     160 |       9 |         0.569 |      0.03  |     -0.032 |           0 |            0 |   -0.74  |  0.003 |              0 |               0 |      0.068 |      -0.117 | -0     |  92.247 |
| NEPSTAD G      | NOR    |     232 |      12 |         0.534 |      0.028 |     -0.041 |           0 |            0 |   -0.74  | -0.004 |              0 |               0 |      0.095 |      -0.115 |  0.002 |  80.568 |
| MAGNUSSON D    | SWE    |      96 |       6 |         0.531 |      0.034 |     -0.042 |           0 |            0 |   -0.773 | -0.002 |              0 |               0 |      0.065 |      -0.097 |  0.001 |  85     |
| POULSEN D      | DEN    |      64 |       4 |         0.531 |      0.039 |     -0.046 |           0 |            0 |   -0.551 | -0     |              1 |               0 |      0.104 |      -0.053 | -0.005 |  82.422 |
| GREINDL D      | GER    |     212 |      12 |         0.528 |      0.031 |     -0.038 |           0 |            0 |   -0.581 | -0.001 |              1 |               0 |      0.128 |      -0.103 |  0     |  88.325 |
| VAN DEN HURK T | NED    |      72 |       4 |         0.528 |      0.049 |     -0.089 |           0 |            0 |   -1.473 | -0.016 |              0 |               0 |      0.051 |      -0.124 | -0.002 |  77.778 |
| WALKER G       | CAN    |     250 |      14 |         0.524 |      0.029 |     -0.033 |           0 |            0 |   -0.713 | -0     |              0 |               0 |      0.128 |      -0.115 | -0.003 |  89.257 |
| KIM HK         | KOR    |     224 |      12 |         0.518 |      0.031 |     -0.037 |           0 |            0 |   -0.574 | -0.002 |              0 |               0 |      0.091 |      -0.111 | -0.003 |  82.812 |
| KAEUFELER M    | SUI    |     174 |      10 |         0.511 |      0.033 |     -0.047 |           0 |            0 |   -0.784 | -0.006 |              0 |               0 |      0.092 |      -0.126 | -0.002 |  83.333 |
| POLLANEN J     | FIN    |     112 |       7 |         0.509 |      0.04  |     -0.057 |           0 |            0 |   -0.864 | -0.008 |              0 |               0 |      0.119 |      -0.112 |  0.002 |  80.357 |
| SOEE OR        | DEN    |     152 |       9 |         0.5   |      0.032 |     -0.049 |           0 |            0 |   -1.074 | -0.008 |              0 |               0 |      0.091 |      -0.111 |  0     |  79.934 |
| KLIPA L        | CZE    |     112 |       7 |         0.482 |      0.026 |     -0.044 |           0 |            0 |   -0.672 | -0.01  |              0 |               0 |      0.055 |      -0.069 | -0.003 |  81.532 |
| GONIN S        | ITA    |     282 |      15 |         0.479 |      0.027 |     -0.04  |           0 |            0 |   -0.652 | -0.008 |              0 |               0 |      0.086 |      -0.096 | -0     |  89.388 |
| CANDRA J       | CZE    |     100 |       6 |         0.46  |      0.028 |     -0.037 |           0 |            0 |   -0.537 | -0.007 |              0 |               0 |      0.051 |      -0.063 | -0.001 |  82     |
| KUOSMANEN P    | FIN    |     212 |      12 |         0.425 |      0.046 |     -0.063 |           1 |            0 |   -1.441 | -0.017 |              1 |               0 |      0.231 |      -0.159 |  0.005 |  81.84  |

