# World Men's Curling Championship (WMCC2026_ResultsBook)

Ogden, UT, USA, 2026; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SWE    |      14 | 12-2     |  35.7 |   5.2 |  11.6 |      22.8 |    -3.9 |      66.9 |
| CAN    |      15 | 12-3     |  30   |  -2.4 |  20.2 |       9.9 |     2.4 |      58.9 |
| SCO    |      14 | 11-3     |  28.6 |   3.5 |  17.9 |       6.9 |     0.3 |      74   |
| SUI    |      13 | 9-4      |  19.2 |  -0.9 |  14.7 |       3.9 |     1.6 |      60.8 |
| ITA    |      13 | 8-5      |  11.5 |   2.8 |   4.1 |       4.4 |     0.2 |      54.7 |
| USA    |      15 | 9-6      |  10   |  -2.4 |  20.3 |      -8.5 |     0.7 |      53.2 |
| CHN    |      12 | 6-6      |   0   |   6.1 |  -3.9 |      -1.8 |    -0.4 |      47.4 |
| JPN    |      12 | 5-7      |  -8.3 |  -4.1 |   9.6 |     -12.2 |    -1.6 |      51.8 |
| GER    |      12 | 4-8      | -16.7 |   0   | -12.3 |      -4.9 |     0.6 |      33   |
| KOR    |      12 | 3-9      | -25   |   0   |  -8.6 |     -15.9 |    -0.5 |      36.3 |
| CZE    |      12 | 3-9      | -25   |  -4.1 | -12.8 |     -11.1 |     3   |      33.9 |
| POL    |      12 | 2-10     | -33.3 |  -6.1 | -34.3 |       8.5 |    -1.4 |      34.9 |
| NOR    |      12 | 0-12     | -50   |   2   | -43   |      -7.9 |    -1.1 |      33.1 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| DUNSTONE M    | CAN    |     251 |      15 |         0.641 |      0.284 |     -0.208 |  0.108 |          27 |           13 |   -4.246 |             32 |              17 |      1.753 |      -0.685 |  0.018 |  86.032 |
| WHYTE R       | SCO    |     235 |      14 |         0.643 |      0.287 |     -0.225 |  0.104 |          21 |            9 |   -4.966 |             40 |              16 |      1.19  |      -0.745 | -0.002 |  86.695 |
| EDIN N        | SWE    |     232 |      14 |         0.655 |      0.252 |     -0.24  |  0.083 |          20 |           13 |   -4.916 |             34 |              19 |      1.065 |      -0.794 |  0.008 |  86.58  |
| HOESLI P      | SUI    |     236 |      13 |         0.631 |      0.253 |     -0.254 |  0.066 |          23 |           12 |   -7.082 |             37 |              20 |      1.21  |      -1.677 |  0.016 |  84.428 |
| YANAGISAWA R  | JPN    |     206 |      12 |         0.607 |      0.261 |     -0.237 |  0.065 |          22 |           10 |   -5.753 |             28 |              17 |      0.926 |      -0.993 |  0.01  |  86.887 |
| SPILLER S     | ITA    |     227 |      13 |         0.626 |      0.245 |     -0.309 |  0.038 |          18 |           17 |   -9.049 |             30 |              21 |      0.998 |      -1.19  |  0.008 |  82.111 |
| SHUSTER J     | USA    |     284 |      15 |         0.56  |      0.259 |     -0.267 |  0.028 |          21 |           26 |   -6.188 |             41 |              30 |      1.65  |      -1.015 |  0.028 |  81.028 |
| FEI X         | CHN    |     217 |      12 |         0.562 |      0.256 |     -0.275 |  0.024 |          15 |           21 |   -4.697 |             36 |              24 |      1.224 |      -0.847 |  0.018 |  79.051 |
| KIM C         | KOR    |     210 |      12 |         0.586 |      0.266 |     -0.323 |  0.022 |          18 |           16 |   -7.7   |             33 |              22 |      1.071 |      -1.111 |  0.007 |  76.683 |
| KLIMA L       | CZE    |     228 |      12 |         0.583 |      0.268 |     -0.356 |  0.008 |          20 |           24 |   -8.817 |             35 |              31 |      1.446 |      -1.904 |  0.001 |  76.101 |
| MUSKATEWITZ M | GER    |     206 |      12 |         0.5   |      0.289 |     -0.327 | -0.019 |          16 |           16 |   -9.562 |             34 |              30 |      1.009 |      -0.82  |  0.013 |  76.578 |
| RAMSFJELL M   | NOR    |     138 |       7 |         0.478 |      0.2   |     -0.265 | -0.042 |           5 |           11 |   -4.538 |              7 |              19 |      0.43  |      -1.023 |  0.019 |  73.188 |
| HAARSTAD A    | NOR    |     191 |      10 |         0.476 |      0.163 |     -0.238 | -0.047 |           4 |           12 |   -5.744 |              9 |              22 |      0.442 |      -1.41  |  0.006 |  78.141 |
| STYCH K       | POL    |     207 |      12 |         0.522 |      0.331 |     -0.467 | -0.05  |          27 |           31 |   -9.595 |             24 |              29 |      0.91  |      -1.088 |  0.034 |  72.573 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HOESLI M    | SUI    |     238 |      13 |         0.584 |      0.138 |     -0.109 |  0.035 |           3 |            0 |   -2.029 |             12 |               8 |      0.421 |      -0.366 | -0.004 |  86.92  |
| ERIKSSON O  | SWE    |     238 |      14 |         0.534 |      0.129 |     -0.11  |  0.018 |           2 |            0 |   -2.111 |             11 |               8 |      0.501 |      -0.397 | -0.006 |  87.29  |
| MOSANER A   | ITA    |     228 |      13 |         0.544 |      0.133 |     -0.128 |  0.014 |           3 |            3 |   -3.373 |             12 |               5 |      0.453 |      -0.356 |  0     |  89.364 |
| YAMAGUCHI T | JPN    |     216 |      12 |         0.532 |      0.136 |     -0.126 |  0.014 |           2 |            3 |   -2.881 |             11 |               7 |      0.453 |      -0.487 | -0.003 |  83.912 |
| BRYDONE R   | SCO    |     236 |      14 |         0.538 |      0.132 |     -0.13  |  0.011 |           1 |            2 |   -2.577 |             11 |               7 |      0.509 |      -0.351 | -0.008 |  88.983 |
| LOTT C      | CAN    |     252 |      15 |         0.556 |      0.121 |     -0.129 |  0.01  |           1 |            4 |   -3.094 |              7 |               6 |      0.456 |      -0.372 | -0.007 |  87.5   |
| PLYS C      | USA    |     286 |      15 |         0.524 |      0.139 |     -0.14  |  0.007 |           4 |            5 |   -2.923 |             10 |              14 |      0.418 |      -0.517 |  0.017 |  85.664 |
| KAPP B      | GER    |     206 |      12 |         0.466 |      0.147 |     -0.13  | -0.001 |           5 |            3 |   -2.594 |             11 |              11 |      0.384 |      -0.441 |  0.001 |  80.34  |
| CERNOVSKY M | CZE    |     218 |      11 |         0.491 |      0.122 |     -0.142 | -0.012 |           1 |            2 |   -2.949 |              9 |              11 |      0.46  |      -0.65  |  0.01  |  81.193 |
| LI Z        | CHN    |     218 |      12 |         0.495 |      0.089 |     -0.135 | -0.024 |           0 |            4 |   -3.147 |              6 |               9 |      0.363 |      -0.49  |  0     |  83.142 |
| YOO M       | KOR    |     318 |      12 |         0.409 |      0.114 |     -0.119 | -0.024 |           1 |            1 |   -2.397 |              7 |               7 |      0.404 |      -0.341 |  0.001 |  77.28  |
| XU X        | CHN    |      42 |       3 |         0.476 |      0.122 |     -0.166 | -0.029 |           0 |            2 |   -2.407 |              0 |               2 |      0.06  |      -0.218 | -0.009 |  81.548 |
| NAESS W     | NOR    |     194 |      10 |         0.418 |      0.1   |     -0.147 | -0.044 |           0 |            1 |   -2.295 |              6 |              11 |      0.325 |      -0.421 |  0.018 |  79.253 |
| DOMIN K     | POL    |     208 |      12 |         0.389 |      0.132 |     -0.177 | -0.057 |           2 |            9 |   -3.118 |              7 |              11 |      0.353 |      -0.412 |  0.012 |  71.635 |

### Seconds

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| USUI S        | JPN    |      98 |       6 |         0.459 |      0.079 |     -0.076 | -0.005 |           1 |            0 |   -0.99  |              2 |               0 |      0.217 |      -0.16  | -0.01  |  81.633 |
| WADDELL C     | SCO    |     230 |      14 |         0.491 |      0.079 |     -0.091 | -0.007 |           0 |            1 |   -1.885 |              2 |               1 |      0.31  |      -0.274 | -0.017 |  86.196 |
| ARMAN S       | ITA    |     228 |      13 |         0.417 |      0.093 |     -0.086 | -0.011 |           0 |            0 |   -1.529 |              3 |               2 |      0.277 |      -0.239 | -0.006 |  84.211 |
| WRANAA R      | SWE    |     228 |      13 |         0.434 |      0.071 |     -0.084 | -0.017 |           0 |            1 |   -2.058 |              1 |               3 |      0.22  |      -0.305 | -0.017 |  85.778 |
| HARNDEN E     | CAN    |     250 |      15 |         0.444 |      0.071 |     -0.089 | -0.018 |           0 |            1 |   -2.243 |              1 |               1 |      0.209 |      -0.209 | -0.001 |  85.1   |
| GLOOR S       | SUI    |     238 |      13 |         0.42  |      0.067 |     -0.083 | -0.02  |           0 |            0 |   -1.315 |              2 |               1 |      0.255 |      -0.2   |  0.001 |  87.131 |
| CHABICOVSKY V | CZE    |      32 |       2 |         0.438 |      0.069 |     -0.094 | -0.022 |           0 |            0 |   -1.027 |              0 |               0 |      0.108 |      -0.123 | -0.009 |  73.438 |
| MESSENZEHL F  | GER    |     206 |      12 |         0.422 |      0.074 |     -0.098 | -0.025 |           0 |            0 |   -1.793 |              2 |               3 |      0.246 |      -0.3   |  0.005 |  82.524 |
| HUFMAN C      | USA    |     268 |      14 |         0.422 |      0.07  |     -0.101 | -0.029 |           0 |            0 |   -1.959 |              1 |               5 |      0.241 |      -0.426 |  0.004 |  81.25  |
| YAMAMOTO T    | JPN    |      90 |       5 |         0.411 |      0.063 |     -0.099 | -0.033 |           0 |            0 |   -1.482 |              1 |               0 |      0.155 |      -0.164 | -0.011 |  77.841 |
| JURIK M       | CZE    |     210 |      11 |         0.4   |      0.076 |     -0.105 | -0.033 |           1 |            0 |   -1.955 |              4 |               4 |      0.299 |      -0.283 | -0.005 |  77.632 |
| YU S          | CHN    |     176 |      10 |         0.403 |      0.043 |     -0.085 | -0.033 |           0 |            1 |   -1.951 |              1 |               3 |      0.198 |      -0.299 |  0.001 |  81.392 |
| CIEMINSKI M   | POL    |     156 |       9 |         0.397 |      0.054 |     -0.104 | -0.042 |           0 |            0 |   -1.681 |              0 |               2 |      0.106 |      -0.263 | -0.006 |  76.282 |
| MELLEMSETER M | NOR    |     198 |      10 |         0.364 |      0.056 |     -0.102 | -0.044 |           0 |            0 |   -1.722 |              0 |               4 |      0.131 |      -0.333 |  0.004 |  78.914 |
| GRZELKA M     | POL    |      78 |       5 |         0.231 |      0.095 |     -0.104 | -0.058 |           1 |            1 |   -1.801 |              1 |               2 |      0.17  |      -0.253 |  0.002 |  76.923 |

### Leads

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| OLDENBURG A | USA    |      38 |       2 |         0.526 |      0.036 |     -0.031 |  0.004 |           0 |            0 |   -0.365 |              0 |               0 |      0.022 |      -0.043 |  0.003 |  96.711 |
| SUNDGREN C  | SWE    |     192 |      11 |         0.51  |      0.037 |     -0.034 |  0.003 |           0 |            0 |   -0.58  |              0 |               0 |      0.109 |      -0.089 |  0.003 |  95.681 |
| BRAENDEN M  | NOR    |     214 |      11 |         0.556 |      0.035 |     -0.044 | -0     |           0 |            0 |   -0.767 |              0 |               0 |      0.095 |      -0.113 | -0.001 |  89.252 |
| KYLE E      | SCO    |     230 |      14 |         0.517 |      0.028 |     -0.034 | -0.002 |           0 |            0 |   -0.553 |              0 |               0 |      0.084 |      -0.086 |  0.002 |  91.63  |
| HAUSHERR J  | SUI    |     236 |      13 |         0.496 |      0.032 |     -0.036 | -0.002 |           0 |            0 |   -0.61  |              0 |               0 |      0.083 |      -0.1   | -0.005 |  94.206 |
| HAMILTON M  | USA    |     266 |      14 |         0.571 |      0.03  |     -0.046 | -0.002 |           0 |            0 |   -0.674 |              0 |               0 |      0.147 |      -0.134 | -0.006 |  91.635 |
| KLIPA L     | CZE    |     230 |      12 |         0.509 |      0.031 |     -0.04  | -0.004 |           0 |            0 |   -0.616 |              0 |               0 |      0.107 |      -0.141 | -0.006 |  87.283 |
| KOIZUMI S   | JPN    |     218 |      12 |         0.528 |      0.028 |     -0.04  | -0.004 |           0 |            0 |   -0.849 |              1 |               0 |      0.13  |      -0.131 | -0     |  91.17  |
| HARNDEN R   | CAN    |     230 |      14 |         0.517 |      0.03  |     -0.042 | -0.004 |           0 |            0 |   -0.748 |              0 |               0 |      0.075 |      -0.113 | -0.005 |  92.935 |
| PIMPINI A   | ITA    |     228 |      13 |         0.43  |      0.033 |     -0.042 | -0.01  |           0 |            0 |   -0.698 |              0 |               0 |      0.071 |      -0.115 | -0     |  90.419 |
| LOBAZA B    | POL    |     182 |      10 |         0.456 |      0.031 |     -0.046 | -0.011 |           0 |            0 |   -0.781 |              0 |               0 |      0.069 |      -0.147 |  0     |  89.286 |
| SCHEUERL J  | GER    |     200 |      12 |         0.47  |      0.027 |     -0.048 | -0.013 |           0 |            0 |   -0.953 |              0 |               1 |      0.077 |      -0.182 | -0.003 |  83.625 |
| WANG Z      | CHN    |     218 |      12 |         0.445 |      0.047 |     -0.062 | -0.013 |           0 |            0 |   -1.633 |              1 |               3 |      0.187 |      -0.276 |  0.003 |  87.156 |
| JEON JI     | KOR    |     318 |      12 |         0.475 |      0.033 |     -0.061 | -0.017 |           0 |            0 |   -1.222 |              0 |               1 |      0.166 |      -0.224 | -0.005 |  86.83  |
| OLOFSSON S  | SWE    |      60 |       5 |         0.383 |      0.028 |     -0.048 | -0.019 |           0 |            0 |   -0.682 |              0 |               0 |      0.035 |      -0.105 | -0.004 |  91.667 |

