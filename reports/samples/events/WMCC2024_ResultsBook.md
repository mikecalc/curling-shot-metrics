# World Men's Curling Championship (WMCC2024_ResultsBook)

Schaffhausen, Switzerland, 2024; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

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

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| JPN    |      867 |   0.021 |    -0.024 |          0.645 |                1.974 |                   2.384 |
| NED    |      884 |   0.015 |    -0.015 |          0.612 |                1.924 |                   2.053 |
| SUI    |      898 |   0.014 |    -0.006 |          0.604 |                2.329 |                   1.929 |
| NZL    |      809 |   0.009 |    -0.032 |          0.613 |                1.861 |                   2.331 |
| NOR    |      896 |   0.006 |    -0.004 |          0.616 |                2.159 |                   2.132 |
| KOR    |      902 |   0.004 |    -0.033 |          0.645 |                2.065 |                   2.166 |
| CZE    |      940 |   0     |     0.016 |          0.583 |                2.084 |                   1.935 |
| GER    |      964 |  -0.003 |    -0.003 |          0.606 |                2.049 |                   2.089 |
| USA    |      888 |  -0.006 |    -0.004 |          0.604 |                2.013 |                   2.133 |
| ITA    |     1136 |  -0.006 |     0.015 |          0.591 |                2.094 |                   2.055 |
| SWE    |     1087 |  -0.01  |    -0.002 |          0.592 |                2.046 |                   1.925 |
| SCO    |     1094 |  -0.016 |     0.048 |          0.548 |                2.215 |                   2.079 |
| CAN    |     1004 |  -0.018 |     0.021 |          0.573 |                2.138 |                   1.917 |

### Fourths

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MOUAT B            | SCO    |     274 |      15 |         0.664 |      0.271 |     -0.289 |          31 |           13 |   -7.415 |  0.083 |             48 |              23 |      1.586 |      -1.494 |  0.011 |  86.447 |
| GUSHUE B           | CAN    |     250 |      14 |         0.636 |      0.235 |     -0.22  |          21 |           11 |   -4.168 |  0.069 |             29 |              14 |      1.117 |      -0.57  | -0.005 |  88.2   |
| EDIN N             | SWE    |     252 |      13 |         0.607 |      0.229 |     -0.25  |          17 |           15 |   -5.056 |  0.041 |             35 |              22 |      1.693 |      -0.851 |  0.007 |  87.004 |
| SHUSTER J          | USA    |     223 |      13 |         0.605 |      0.24  |     -0.314 |          17 |           16 |   -7.82  |  0.021 |             24 |              18 |      0.938 |      -2.074 |  0.008 |  81.448 |
| RETORNAZ J         | ITA    |     284 |      15 |         0.599 |      0.294 |     -0.285 |          29 |           16 |   -7.284 |  0.062 |             46 |              28 |      1.232 |      -1.294 |  0.014 |  83.569 |
| SHIMIZU T          | JPN    |     217 |      12 |         0.585 |      0.277 |     -0.394 |          21 |           28 |   -7.222 | -0.001 |             31 |              29 |      1.26  |      -1.178 |  0.023 |  76.887 |
| SCHWARZ-VAN BERKEL | SUI    |     225 |      12 |         0.582 |      0.259 |     -0.28  |          17 |           17 |   -5.811 |  0.034 |             35 |              28 |      1.365 |      -2.025 | -0.009 |  84.305 |
| RAMSFJELL M        | NOR    |     221 |      12 |         0.566 |      0.249 |     -0.308 |          14 |           14 |   -7.79  |  0.007 |             32 |              24 |      1.231 |      -1.299 |  0.012 |  80.137 |
| KLIMA L            | CZE    |     234 |      12 |         0.551 |      0.241 |     -0.345 |          15 |           27 |   -7.395 | -0.022 |             36 |              35 |      0.918 |      -1.083 |  0.008 |  75.322 |
| GOESGENS W         | NED    |     219 |      12 |         0.539 |      0.211 |     -0.283 |           7 |           15 |   -7.86  | -0.017 |             20 |              24 |      1.001 |      -0.966 |  0.019 |  78.784 |
| MUSKATEWITZ M      | GER    |     241 |      13 |         0.531 |      0.273 |     -0.291 |          25 |           18 |   -8.642 |  0.009 |             29 |              25 |      1.099 |      -0.984 | -0.006 |  79.393 |
| HOOD A             | NZL    |     201 |      12 |         0.493 |      0.206 |     -0.408 |           7 |           26 |   -9.427 | -0.105 |             13 |              31 |      0.479 |      -1.136 |  0.019 |  68.561 |
| PARK J             | KOR    |     225 |      12 |         0.48  |      0.221 |     -0.3   |          12 |           26 |   -6.03  | -0.05  |             18 |              30 |      0.988 |      -1.043 | -0.004 |  71.171 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HARDIE G    | SCO    |     274 |      15 |         0.595 |      0.152 |     -0.15  |           5 |            5 |   -2.988 |  0.03  |             14 |              15 |      0.526 |      -0.493 | -0.01  |  84.854 |
| NICHOLS M   | CAN    |     252 |      14 |         0.591 |      0.151 |     -0.124 |           3 |            3 |   -3.115 |  0.038 |             12 |               6 |      0.381 |      -0.409 | -0.008 |  90.476 |
| SCHWALLER Y | SUI    |     226 |      12 |         0.584 |      0.133 |     -0.116 |           2 |            0 |   -2.083 |  0.03  |             13 |               4 |      0.411 |      -0.288 |  0.005 |  87.667 |
| MOSANER A   | ITA    |     284 |      15 |         0.553 |      0.13  |     -0.142 |           3 |            6 |   -3.391 |  0.008 |             13 |               9 |      0.407 |      -0.517 | -0.007 |  88.251 |
| PLYS C      | USA    |     224 |      13 |         0.531 |      0.121 |     -0.138 |           4 |            1 |   -2.294 | -0.001 |              5 |               9 |      0.345 |      -0.335 |  0.002 |  85.491 |
| JEONG Y     | KOR    |     228 |      12 |         0.518 |      0.123 |     -0.145 |           3 |            5 |   -3.167 | -0.006 |              5 |               9 |      0.405 |      -0.537 | -0.009 |  81.469 |
| ERIKSSON O  | SWE    |     274 |      14 |         0.511 |      0.15  |     -0.129 |           4 |            5 |   -3.505 |  0.013 |             14 |               7 |      0.47  |      -0.554 | -0.018 |  87.5   |
| CERNOVSKY M | CZE    |     216 |      11 |         0.486 |      0.13  |     -0.137 |           2 |            3 |   -2.786 | -0.007 |              8 |               8 |      0.405 |      -0.506 |  0.003 |  80.903 |
| ABE S       | JPN    |     218 |      12 |         0.463 |      0.12  |     -0.15  |           2 |            2 |   -2.553 | -0.025 |              6 |               7 |      0.378 |      -0.403 |  0.009 |  77.064 |
| SESAKER M   | NOR    |     226 |      12 |         0.46  |      0.147 |     -0.152 |           6 |            2 |   -2.601 | -0.014 |             10 |              15 |      0.558 |      -0.687 |  0.003 |  79.425 |
| KAPP B      | GER    |     242 |      13 |         0.459 |      0.144 |     -0.148 |           5 |            3 |   -2.945 | -0.014 |             10 |              10 |      0.61  |      -0.522 |  0.003 |  79.132 |
| HOEKMAN L   | NED    |     224 |      12 |         0.429 |      0.127 |     -0.141 |           3 |            3 |   -2.88  | -0.026 |              5 |              15 |      0.6   |      -0.448 |  0     |  76.786 |
| SMITH B     | NZL    |     204 |      12 |         0.368 |      0.111 |     -0.155 |           1 |            5 |   -2.949 | -0.057 |              2 |              16 |      0.257 |      -0.486 |  0.015 |  71.814 |

### Seconds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MICHEL S     | SUI    |     226 |      12 |         0.558 |      0.067 |     -0.097 |           0 |            1 |   -1.997 | -0.006 |              0 |               5 |      0.18  |      -0.364 |  0.001 |  85.509 |
| WRANAA R     | SWE    |     274 |      14 |         0.522 |      0.083 |     -0.085 |           0 |            1 |   -1.75  |  0.003 |              3 |               3 |      0.262 |      -0.287 | -0.007 |  87.5   |
| HARNDEN E    | CAN    |     170 |       9 |         0.5   |      0.075 |     -0.085 |           0 |            1 |   -1.895 | -0.005 |              1 |               3 |      0.205 |      -0.272 | -0.009 |  86.391 |
| HUFMAN C     | USA    |     224 |      13 |         0.496 |      0.078 |     -0.096 |           0 |            1 |   -2.084 | -0.01  |              4 |               4 |      0.321 |      -0.359 | -0.001 |  83.705 |
| OUCHI H      | JPN    |     164 |       9 |         0.494 |      0.081 |     -0.082 |           1 |            0 |   -1.586 | -0.001 |              2 |               0 |      0.247 |      -0.192 | -0.001 |  84.451 |
| ARMAN S      | ITA    |     284 |      15 |         0.489 |      0.074 |     -0.103 |           0 |            3 |   -2.742 | -0.016 |              3 |               5 |      0.283 |      -0.411 | -0.005 |  83.363 |
| RAMSFJELL B  | NOR    |     182 |      10 |         0.489 |      0.069 |     -0.077 |           0 |            0 |   -1.242 | -0.005 |              1 |               1 |      0.206 |      -0.217 | -0.004 |  83.516 |
| MESSENZEHL F | GER    |     242 |      13 |         0.488 |      0.079 |     -0.078 |           0 |            0 |   -1.545 | -0.002 |              1 |               2 |      0.219 |      -0.224 | -0.005 |  85.227 |
| VAN DORP J   | NED    |     224 |      12 |         0.464 |      0.076 |     -0.097 |           0 |            2 |   -2.612 | -0.017 |              1 |               4 |      0.225 |      -0.417 |  0.004 |  81.054 |
| HARNDEN EJ   | CAN    |      80 |       5 |         0.462 |      0.109 |     -0.09  |           0 |            0 |   -1.461 |  0.002 |              0 |               1 |      0.138 |      -0.184 | -0.016 |  81.013 |
| LAMMIE B     | SCO    |     274 |      15 |         0.46  |      0.083 |     -0.088 |           0 |            1 |   -2.02  | -0.01  |              2 |               4 |      0.242 |      -0.374 | -0.01  |  84.763 |
| NAESS W      | NOR    |      46 |       4 |         0.457 |      0.073 |     -0.093 |           0 |            0 |   -1.371 | -0.017 |              1 |               2 |      0.172 |      -0.178 |  0.004 |  89.13  |
| JURIK M      | CZE    |     236 |      12 |         0.436 |      0.066 |     -0.097 |           0 |            0 |   -1.685 | -0.026 |              1 |               2 |      0.24  |      -0.226 | -0.006 |  78.191 |
| OH S         | KOR    |     170 |       9 |         0.429 |      0.086 |     -0.096 |           0 |            0 |   -1.329 | -0.018 |              1 |               1 |      0.236 |      -0.211 |  0.006 |  76.775 |
| SARGON B     | NZL    |     204 |      12 |         0.426 |      0.079 |     -0.102 |           0 |            1 |   -2.034 | -0.025 |              1 |               5 |      0.152 |      -0.325 |  0.001 |  72.672 |

### Leads

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| GIOVANELLA M       | ITA    |     284 |      15 |         0.567 |      0.026 |     -0.035 |           0 |            0 |   -0.722 | -0.001 |              1 |               0 |      0.124 |      -0.11  | -0.002 |  92.606 |
| LEE K              | KOR    |     120 |       6 |         0.55  |      0.072 |     -0.056 |           0 |            0 |   -1.17  |  0.015 |              0 |               1 |      0.167 |      -0.183 | -0.006 |  88.559 |
| MCMILLAN H         | SCO    |     274 |      15 |         0.544 |      0.031 |     -0.029 |           0 |            0 |   -0.779 |  0.004 |              0 |               0 |      0.084 |      -0.126 |  0.005 |  92.518 |
| VAN DEN HURK T     | NED    |     188 |      10 |         0.537 |      0.029 |     -0.038 |           0 |            0 |   -0.776 | -0.002 |              0 |               0 |      0.073 |      -0.127 | -0.001 |  89.096 |
| HAMILTON M         | USA    |      84 |       5 |         0.536 |      0.029 |     -0.039 |           0 |            0 |   -0.542 | -0.003 |              0 |               0 |      0.081 |      -0.082 | -0.001 |  89.583 |
| MAGAN A            | NED    |      36 |       2 |         0.528 |      0.029 |     -0.045 |           0 |            0 |   -0.596 | -0.006 |              0 |               0 |      0.021 |      -0.064 | -0.003 |  84.722 |
| SUNDGREN C         | SWE    |     274 |      14 |         0.515 |      0.031 |     -0.029 |           0 |            0 |   -0.751 |  0.002 |              0 |               0 |      0.089 |      -0.134 |  0.002 |  93.704 |
| NAKAHARA A         | JPN    |     150 |       8 |         0.5   |      0.057 |     -0.056 |           0 |            0 |   -1.257 |  0     |              0 |               0 |      0.132 |      -0.096 |  0.002 |  86.167 |
| SEONG J            | KOR    |     166 |       9 |         0.494 |      0.03  |     -0.038 |           0 |            0 |   -0.647 | -0.005 |              0 |               0 |      0.051 |      -0.075 | -0.003 |  88.855 |
| WALKER G           | CAN    |     250 |      14 |         0.492 |      0.03  |     -0.033 |           0 |            0 |   -0.756 | -0.002 |              0 |               0 |      0.123 |      -0.118 |  0.001 |  91.7   |
| TSURUGA S          | JPN    |     122 |       7 |         0.492 |      0.034 |     -0.047 |           0 |            0 |   -0.66  | -0.007 |              0 |               0 |      0.093 |      -0.098 | -0.003 |  85.246 |
| WALKER H           | NZL    |     204 |      12 |         0.49  |      0.028 |     -0.046 |           0 |            0 |   -0.812 | -0.01  |              0 |               0 |      0.062 |      -0.113 |  0.001 |  84.191 |
| SCHEUERL J         | GER    |     242 |      13 |         0.471 |      0.03  |     -0.035 |           0 |            0 |   -0.707 | -0.004 |              0 |               0 |      0.081 |      -0.114 |  0.001 |  89.834 |
| LACHAT-COUCHEPIN P | SUI    |     222 |      12 |         0.468 |      0.031 |     -0.034 |           0 |            0 |   -0.713 | -0.003 |              1 |               0 |      0.123 |      -0.091 | -0.001 |  91.216 |
| NEPSTAD G          | NOR    |     224 |      12 |         0.433 |      0.03  |     -0.036 |           0 |            0 |   -0.8   | -0.007 |              0 |               0 |      0.079 |      -0.127 |  0.001 |  87.05  |
| KLIPA L            | CZE    |     236 |      12 |         0.424 |      0.027 |     -0.045 |           0 |            0 |   -0.777 | -0.014 |              0 |               0 |      0.079 |      -0.132 | -0.001 |  83.404 |
| LANDSTEINER J      | USA    |     140 |       8 |         0.421 |      0.028 |     -0.028 |           0 |            0 |   -0.643 | -0.004 |              0 |               0 |      0.071 |      -0.088 |  0.002 |  90     |

