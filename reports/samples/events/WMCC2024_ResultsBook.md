# World Men's Curling Championship (WMCC2024_ResultsBook)

Schaffhausen, Switzerland, 2024; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SWE    |      14 | 13-1     |  42.9 |   8.5 |  23.8 |      11.3 |    -0.8 |      67.2 |
| CAN    |      14 | 11-3     |  28.6 |   3.4 |  17.8 |       6.8 |     0.5 |      66.5 |
| SCO    |      15 | 11-4     |  23.3 |  -0.8 |  38.5 |     -16.7 |     2.3 |      66.3 |
| ITA    |      15 | 10-5     |  16.7 |  -2.4 |  18.4 |       1.2 |    -0.6 |      54.7 |
| GER    |      13 | 8-5      |  11.5 |   0.9 |  -4.8 |      13.2 |     2.2 |      50.5 |
| USA    |      13 | 7-6      |   3.8 |  -2.8 |  -4.7 |      10.7 |     0.6 |      55.6 |
| SUI    |      12 | 6-6      |   0   |   2   |   8.8 |      -8.9 |    -2   |      54.7 |
| NED    |      12 | 5-7      |  -8.3 |  -2   | -19.1 |      12.6 |     0.1 |      36.8 |
| CZE    |      12 | 4-8      | -16.7 |  -2   | -16.5 |       1.8 |     0   |      43.1 |
| NOR    |      12 | 4-8      | -16.7 |  -4   |  -3   |      -9.1 |    -0.6 |      40.6 |
| JPN    |      12 | 3-9      | -25   |  -2   |  -5.2 |     -16.8 |    -1.1 |      41.6 |
| KOR    |      12 | 2-10     | -33.3 |   2   | -27.4 |      -7.6 |    -0.3 |      40.2 |
| NZL    |      12 | 0-12     | -50   |  -2   | -47.1 |       0.3 |    -1.2 |      20.8 |

### Fourths

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MOUAT B            | SCO    |     274 |      15 |         0.664 |      0.271 |     -0.289 |  0.083 |          31 |           13 |   -7.415 |             48 |              23 |      1.586 |      -1.494 |  0.011 |  86.447 |
| GUSHUE B           | CAN    |     250 |      14 |         0.636 |      0.235 |     -0.22  |  0.069 |          21 |           11 |   -4.168 |             29 |              14 |      1.117 |      -0.57  | -0.005 |  88.2   |
| RETORNAZ J         | ITA    |     284 |      15 |         0.599 |      0.294 |     -0.285 |  0.062 |          29 |           16 |   -7.284 |             46 |              28 |      1.232 |      -1.294 |  0.014 |  83.569 |
| EDIN N             | SWE    |     252 |      13 |         0.607 |      0.229 |     -0.25  |  0.041 |          17 |           15 |   -5.056 |             35 |              22 |      1.693 |      -0.851 |  0.007 |  87.004 |
| SCHWARZ-VAN BERKEL | SUI    |     225 |      12 |         0.582 |      0.259 |     -0.28  |  0.034 |          17 |           17 |   -5.811 |             35 |              28 |      1.365 |      -2.025 | -0.009 |  84.305 |
| SHUSTER J          | USA    |     223 |      13 |         0.605 |      0.24  |     -0.314 |  0.021 |          17 |           16 |   -7.82  |             24 |              18 |      0.938 |      -2.074 |  0.008 |  81.448 |
| MUSKATEWITZ M      | GER    |     241 |      13 |         0.531 |      0.273 |     -0.291 |  0.009 |          25 |           18 |   -8.642 |             29 |              25 |      1.099 |      -0.984 | -0.006 |  79.393 |
| RAMSFJELL M        | NOR    |     221 |      12 |         0.566 |      0.249 |     -0.308 |  0.007 |          14 |           14 |   -7.79  |             32 |              24 |      1.231 |      -1.299 |  0.012 |  80.137 |
| SHIMIZU T          | JPN    |     217 |      12 |         0.585 |      0.277 |     -0.394 | -0.001 |          21 |           28 |   -7.222 |             31 |              29 |      1.26  |      -1.178 |  0.023 |  76.887 |
| GOESGENS W         | NED    |     219 |      12 |         0.539 |      0.211 |     -0.283 | -0.017 |           7 |           15 |   -7.86  |             20 |              24 |      1.001 |      -0.966 |  0.019 |  78.784 |
| KLIMA L            | CZE    |     234 |      12 |         0.551 |      0.241 |     -0.345 | -0.022 |          15 |           27 |   -7.395 |             36 |              35 |      0.918 |      -1.083 |  0.008 |  75.322 |
| PARK J             | KOR    |     225 |      12 |         0.48  |      0.221 |     -0.3   | -0.05  |          12 |           26 |   -6.03  |             18 |              30 |      0.988 |      -1.043 | -0.004 |  71.171 |
| HOOD A             | NZL    |     201 |      12 |         0.493 |      0.206 |     -0.408 | -0.105 |           7 |           26 |   -9.427 |             13 |              31 |      0.479 |      -1.136 |  0.019 |  68.561 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| NICHOLS M   | CAN    |     252 |      14 |         0.591 |      0.151 |     -0.124 |  0.038 |           3 |            3 |   -3.115 |             12 |               6 |      0.381 |      -0.409 | -0.008 |  90.476 |
| HARDIE G    | SCO    |     274 |      15 |         0.595 |      0.152 |     -0.15  |  0.03  |           5 |            5 |   -2.988 |             14 |              15 |      0.526 |      -0.493 | -0.01  |  84.854 |
| SCHWALLER Y | SUI    |     226 |      12 |         0.584 |      0.133 |     -0.116 |  0.03  |           2 |            0 |   -2.083 |             13 |               4 |      0.411 |      -0.288 |  0.005 |  87.667 |
| ERIKSSON O  | SWE    |     274 |      14 |         0.511 |      0.15  |     -0.129 |  0.013 |           4 |            5 |   -3.505 |             14 |               7 |      0.47  |      -0.554 | -0.018 |  87.5   |
| MOSANER A   | ITA    |     284 |      15 |         0.553 |      0.13  |     -0.142 |  0.008 |           3 |            6 |   -3.391 |             13 |               9 |      0.407 |      -0.517 | -0.007 |  88.251 |
| PLYS C      | USA    |     224 |      13 |         0.531 |      0.121 |     -0.138 | -0.001 |           4 |            1 |   -2.294 |              5 |               9 |      0.345 |      -0.335 |  0.002 |  85.491 |
| JEONG Y     | KOR    |     228 |      12 |         0.518 |      0.123 |     -0.145 | -0.006 |           3 |            5 |   -3.167 |              5 |               9 |      0.405 |      -0.537 | -0.009 |  81.469 |
| CERNOVSKY M | CZE    |     216 |      11 |         0.486 |      0.13  |     -0.137 | -0.007 |           2 |            3 |   -2.786 |              8 |               8 |      0.405 |      -0.506 |  0.003 |  80.903 |
| KAPP B      | GER    |     242 |      13 |         0.459 |      0.144 |     -0.148 | -0.014 |           5 |            3 |   -2.945 |             10 |              10 |      0.61  |      -0.522 |  0.003 |  79.132 |
| SESAKER M   | NOR    |     226 |      12 |         0.46  |      0.147 |     -0.152 | -0.014 |           6 |            2 |   -2.601 |             10 |              15 |      0.558 |      -0.687 |  0.003 |  79.425 |
| ABE S       | JPN    |     218 |      12 |         0.463 |      0.12  |     -0.15  | -0.025 |           2 |            2 |   -2.553 |              6 |               7 |      0.378 |      -0.403 |  0.009 |  77.064 |
| HOEKMAN L   | NED    |     224 |      12 |         0.429 |      0.127 |     -0.141 | -0.026 |           3 |            3 |   -2.88  |              5 |              15 |      0.6   |      -0.448 |  0     |  76.786 |
| SMITH B     | NZL    |     204 |      12 |         0.368 |      0.111 |     -0.155 | -0.057 |           1 |            5 |   -2.949 |              2 |              16 |      0.257 |      -0.486 |  0.015 |  71.814 |

### Seconds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WRANAA R     | SWE    |     274 |      14 |         0.522 |      0.083 |     -0.085 |  0.003 |           0 |            1 |   -1.75  |              3 |               3 |      0.262 |      -0.287 | -0.007 |  87.5   |
| HARNDEN EJ   | CAN    |      80 |       5 |         0.462 |      0.109 |     -0.09  |  0.002 |           0 |            0 |   -1.461 |              0 |               1 |      0.138 |      -0.184 | -0.016 |  81.013 |
| OUCHI H      | JPN    |     164 |       9 |         0.494 |      0.081 |     -0.082 | -0.001 |           1 |            0 |   -1.586 |              2 |               0 |      0.247 |      -0.192 | -0.001 |  84.451 |
| MESSENZEHL F | GER    |     242 |      13 |         0.488 |      0.079 |     -0.078 | -0.002 |           0 |            0 |   -1.545 |              1 |               2 |      0.219 |      -0.224 | -0.005 |  85.227 |
| HARNDEN E    | CAN    |     170 |       9 |         0.5   |      0.075 |     -0.085 | -0.005 |           0 |            1 |   -1.895 |              1 |               3 |      0.205 |      -0.272 | -0.009 |  86.391 |
| RAMSFJELL B  | NOR    |     182 |      10 |         0.489 |      0.069 |     -0.077 | -0.005 |           0 |            0 |   -1.242 |              1 |               1 |      0.206 |      -0.217 | -0.004 |  83.516 |
| MICHEL S     | SUI    |     226 |      12 |         0.558 |      0.067 |     -0.097 | -0.006 |           0 |            1 |   -1.997 |              0 |               5 |      0.18  |      -0.364 |  0.001 |  85.509 |
| LAMMIE B     | SCO    |     274 |      15 |         0.46  |      0.083 |     -0.088 | -0.01  |           0 |            1 |   -2.02  |              2 |               4 |      0.242 |      -0.374 | -0.01  |  84.763 |
| HUFMAN C     | USA    |     224 |      13 |         0.496 |      0.078 |     -0.096 | -0.01  |           0 |            1 |   -2.084 |              4 |               4 |      0.321 |      -0.359 | -0.001 |  83.705 |
| ARMAN S      | ITA    |     284 |      15 |         0.489 |      0.074 |     -0.103 | -0.016 |           0 |            3 |   -2.742 |              3 |               5 |      0.283 |      -0.411 | -0.005 |  83.363 |
| VAN DORP J   | NED    |     224 |      12 |         0.464 |      0.076 |     -0.097 | -0.017 |           0 |            2 |   -2.612 |              1 |               4 |      0.225 |      -0.417 |  0.004 |  81.054 |
| NAESS W      | NOR    |      46 |       4 |         0.457 |      0.073 |     -0.093 | -0.017 |           0 |            0 |   -1.371 |              1 |               2 |      0.172 |      -0.178 |  0.004 |  89.13  |
| OH S         | KOR    |     170 |       9 |         0.429 |      0.086 |     -0.096 | -0.018 |           0 |            0 |   -1.329 |              1 |               1 |      0.236 |      -0.211 |  0.006 |  76.775 |
| SARGON B     | NZL    |     204 |      12 |         0.426 |      0.079 |     -0.102 | -0.025 |           0 |            1 |   -2.034 |              1 |               5 |      0.152 |      -0.325 |  0.001 |  72.672 |
| JURIK M      | CZE    |     236 |      12 |         0.436 |      0.066 |     -0.097 | -0.026 |           0 |            0 |   -1.685 |              1 |               2 |      0.24  |      -0.226 | -0.006 |  78.191 |

### Leads

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| LEE K              | KOR    |     120 |       6 |         0.55  |      0.072 |     -0.056 |  0.015 |           0 |            0 |   -1.17  |              0 |               1 |      0.167 |      -0.183 | -0.006 |  88.559 |
| MCMILLAN H         | SCO    |     274 |      15 |         0.544 |      0.031 |     -0.029 |  0.004 |           0 |            0 |   -0.779 |              0 |               0 |      0.084 |      -0.126 |  0.005 |  92.518 |
| SUNDGREN C         | SWE    |     274 |      14 |         0.515 |      0.031 |     -0.029 |  0.002 |           0 |            0 |   -0.751 |              0 |               0 |      0.089 |      -0.134 |  0.002 |  93.704 |
| NAKAHARA A         | JPN    |     150 |       8 |         0.5   |      0.057 |     -0.056 |  0     |           0 |            0 |   -1.257 |              0 |               0 |      0.132 |      -0.096 |  0.002 |  86.167 |
| GIOVANELLA M       | ITA    |     284 |      15 |         0.567 |      0.026 |     -0.035 | -0.001 |           0 |            0 |   -0.722 |              1 |               0 |      0.124 |      -0.11  | -0.002 |  92.606 |
| WALKER G           | CAN    |     250 |      14 |         0.492 |      0.03  |     -0.033 | -0.002 |           0 |            0 |   -0.756 |              0 |               0 |      0.123 |      -0.118 |  0.001 |  91.7   |
| VAN DEN HURK T     | NED    |     188 |      10 |         0.537 |      0.029 |     -0.038 | -0.002 |           0 |            0 |   -0.776 |              0 |               0 |      0.073 |      -0.127 | -0.001 |  89.096 |
| HAMILTON M         | USA    |      84 |       5 |         0.536 |      0.029 |     -0.039 | -0.003 |           0 |            0 |   -0.542 |              0 |               0 |      0.081 |      -0.082 | -0.001 |  89.583 |
| LACHAT-COUCHEPIN P | SUI    |     222 |      12 |         0.468 |      0.031 |     -0.034 | -0.003 |           0 |            0 |   -0.713 |              1 |               0 |      0.123 |      -0.091 | -0.001 |  91.216 |
| SCHEUERL J         | GER    |     242 |      13 |         0.471 |      0.03  |     -0.035 | -0.004 |           0 |            0 |   -0.707 |              0 |               0 |      0.081 |      -0.114 |  0.001 |  89.834 |
| LANDSTEINER J      | USA    |     140 |       8 |         0.421 |      0.028 |     -0.028 | -0.004 |           0 |            0 |   -0.643 |              0 |               0 |      0.071 |      -0.088 |  0.002 |  90     |
| SEONG J            | KOR    |     166 |       9 |         0.494 |      0.03  |     -0.038 | -0.005 |           0 |            0 |   -0.647 |              0 |               0 |      0.051 |      -0.075 | -0.003 |  88.855 |
| MAGAN A            | NED    |      36 |       2 |         0.528 |      0.029 |     -0.045 | -0.006 |           0 |            0 |   -0.596 |              0 |               0 |      0.021 |      -0.064 | -0.003 |  84.722 |
| NEPSTAD G          | NOR    |     224 |      12 |         0.433 |      0.03  |     -0.036 | -0.007 |           0 |            0 |   -0.8   |              0 |               0 |      0.079 |      -0.127 |  0.001 |  87.05  |
| TSURUGA S          | JPN    |     122 |       7 |         0.492 |      0.034 |     -0.047 | -0.007 |           0 |            0 |   -0.66  |              0 |               0 |      0.093 |      -0.098 | -0.003 |  85.246 |
| WALKER H           | NZL    |     204 |      12 |         0.49  |      0.028 |     -0.046 | -0.01  |           0 |            0 |   -0.812 |              0 |               0 |      0.062 |      -0.113 |  0.001 |  84.191 |
| KLIPA L            | CZE    |     236 |      12 |         0.424 |      0.027 |     -0.045 | -0.014 |           0 |            0 |   -0.777 |              0 |               0 |      0.079 |      -0.132 | -0.001 |  83.404 |

