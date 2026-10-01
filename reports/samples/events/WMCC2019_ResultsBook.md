# World Men's Curling Championship (WMCC2019_ResultsBook)

Lethbridge, AB, Canada, 2019; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SWE    |      14 | 13-1     |  42.9 |   6.9 |  20.8 |      15.1 |     0.1 |      74.5 |
| CAN    |      15 | 11-4     |  23.3 |   0.8 |  25.1 |      -6.1 |     3.6 |      63.4 |
| SUI    |      14 | 10-4     |  21.4 |   1.7 |  14.2 |       3.8 |     1.7 |      59.4 |
| JPN    |      15 | 10-5     |  16.7 |  -4   |  10.5 |       8.7 |     1.5 |      51.8 |
| SCO    |      13 | 8-5      |  11.5 |   8.3 |   5.9 |      -5.1 |     2.4 |      60.5 |
| USA    |      13 | 8-5      |  11.5 |  -2.8 |  14.6 |       1.3 |    -1.5 |      55.5 |
| ITA    |      12 | 7-5      |   8.3 |   0   |  -3.4 |      10.4 |     1.3 |      59.5 |
| NED    |      12 | 4-8      | -16.7 |  -8   |   1.8 |      -9.3 |    -1.2 |      39.8 |
| RUS    |      12 | 4-8      | -16.7 |  -2   |  -6   |      -8.6 |    -0   |      38.4 |
| GER    |      12 | 4-8      | -16.7 |  -2   | -13.6 |       0   |    -1.1 |      36.2 |
| CHN    |      12 | 2-10     | -33.3 |   4   | -28.4 |      -3.7 |    -5.3 |      36.1 |
| NOR    |      12 | 2-10     | -33.3 |  -4   | -26.5 |      -0.1 |    -2.8 |      22.4 |
| KOR    |      12 | 1-11     | -41.7 |   0   | -31.5 |      -9.9 |    -0.3 |      41.7 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| SCO    |      936 |   0.022 |    -0.005 |          0.634 |                2.031 |                   2.165 |
| CHN    |      875 |   0.011 |    -0.02  |          0.618 |                2.03  |                   2.071 |
| RUS    |      869 |   0.008 |     0.001 |          0.602 |                2.171 |                   1.986 |
| NED    |      925 |   0.004 |    -0.004 |          0.6   |                2.085 |                   1.951 |
| NOR    |      817 |   0.003 |     0.007 |          0.596 |                1.848 |                   2.364 |
| ITA    |      863 |   0.002 |    -0.004 |          0.621 |                2.154 |                   2.064 |
| SUI    |     1029 |  -0.001 |     0     |          0.607 |                2.081 |                   2.104 |
| USA    |      973 |  -0.003 |     0.004 |          0.582 |                2.042 |                   1.919 |
| GER    |      865 |  -0.005 |    -0     |          0.61  |                1.949 |                   1.993 |
| KOR    |      907 |  -0.006 |    -0.01  |          0.605 |                2.02  |                   2.162 |
| CAN    |     1054 |  -0.006 |     0.036 |          0.578 |                2.071 |                   2.065 |
| SWE    |      938 |  -0.011 |     0.002 |          0.597 |                2.132 |                   1.888 |
| JPN    |     1120 |  -0.013 |    -0.01  |          0.604 |                2.079 |                   2.059 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MOUAT B       | SCO    |     237 |      13 |         0.646 |      0.248 |     -0.332 |          21 |           19 |   -6.827 |  0.043 |             30 |              35 |      1.615 |      -1.26  | -0.007 |  83.617 |
| EDIN N        | SWE    |     235 |      14 |         0.643 |      0.263 |     -0.254 |          23 |           14 |   -5.699 |  0.078 |             29 |              14 |      1.015 |      -0.779 | -0.001 |  88.197 |
| SCHWARZ B     | SUI    |     258 |      14 |         0.612 |      0.231 |     -0.226 |          15 |           13 |   -5.384 |  0.054 |             35 |              23 |      1.118 |      -0.742 |  0.001 |  86.759 |
| KOE K         | CAN    |     265 |      15 |         0.611 |      0.245 |     -0.294 |          22 |           19 |   -7.969 |  0.035 |             38 |              22 |      1.135 |      -1.084 |  0.002 |  84.828 |
| RAMSFJELL M   | NOR    |     203 |      12 |         0.581 |      0.225 |     -0.347 |          13 |           23 |   -6.41  | -0.015 |              9 |              20 |      0.429 |      -0.773 |  0.019 |  72.277 |
| SHUSTER J     | USA    |     241 |      13 |         0.577 |      0.251 |     -0.202 |          19 |           13 |   -4.554 |  0.059 |             27 |              20 |      1.215 |      -0.828 | -0.001 |  83.333 |
| MUSKATEWITZ M | GER    |     215 |      12 |         0.567 |      0.233 |     -0.308 |          17 |           17 |   -6.861 | -0.001 |             20 |              23 |      0.793 |      -1.103 |  0.018 |  75.234 |
| GOESGENS W    | NED    |     233 |      12 |         0.558 |      0.229 |     -0.27  |          13 |           17 |   -6.105 |  0.008 |             27 |              29 |      1.664 |      -1.332 | -0.008 |  77.694 |
| GLUKHOV S     | RUS    |     218 |      12 |         0.537 |      0.225 |     -0.262 |          11 |           18 |   -5.28  | -0.001 |             15 |              23 |      0.617 |      -0.646 |  0.012 |  77.064 |
| ZOU Q         | CHN    |     220 |      12 |         0.536 |      0.22  |     -0.332 |           9 |           22 |   -7.798 | -0.036 |             21 |              34 |      0.725 |      -1.032 |  0     |  75.115 |
| MATSUMURA Y   | JPN    |     280 |      15 |         0.532 |      0.271 |     -0.223 |          23 |           19 |   -4.87  |  0.04  |             42 |              19 |      1.207 |      -0.612 | -0.01  |  82.727 |
| KIM S         | KOR    |     217 |      11 |         0.53  |      0.237 |     -0.339 |          20 |           21 |   -7.986 | -0.034 |             26 |              33 |      0.78  |      -1.9   |  0.008 |  73.372 |
| RETORNAZ J    | ITA    |     218 |      12 |         0.528 |      0.214 |     -0.243 |          15 |           11 |   -7.379 | -0.002 |             26 |              25 |      0.868 |      -0.989 |  0.002 |  83.142 |

### Thirds

| player     | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| ERIKSSON O | SWE    |     236 |      14 |         0.581 |      0.133 |     -0.12  |           2 |            3 |   -3.124 |  0.027 |             10 |               8 |      0.376 |      -0.446 | -0.015 |  89.149 |
| ALI A      | RUS    |      88 |       5 |         0.58  |      0.106 |     -0.141 |           0 |            1 |   -1.862 |  0.002 |              2 |               4 |      0.285 |      -0.305 |  0.009 |  77.273 |
| NEUFELD BJ | CAN    |     266 |      15 |         0.564 |      0.147 |     -0.123 |           9 |            3 |   -2.704 |  0.029 |             14 |               7 |      0.578 |      -0.499 | -0.006 |  86.226 |
| HARDIE G   | SCO    |     238 |      13 |         0.555 |      0.131 |     -0.136 |           6 |            3 |   -2.877 |  0.012 |             13 |               7 |      0.452 |      -0.535 |  0.003 |  86.87  |
| VAN DORP J | NED    |     234 |      12 |         0.534 |      0.12  |     -0.114 |           3 |            2 |   -2.477 |  0.011 |              8 |               4 |      0.56  |      -0.402 |  0.002 |  81.517 |
| BA D       | CHN    |     176 |      10 |         0.523 |      0.096 |     -0.128 |           0 |            3 |   -2.52  | -0.011 |              2 |               7 |      0.26  |      -0.619 |  0.008 |  80.824 |
| WANG Z     | CHN    |     222 |      12 |         0.523 |      0.089 |     -0.121 |           0 |            3 |   -2.903 | -0.011 |              2 |               6 |      0.244 |      -0.381 |  0.004 |  81.222 |
| PLYS C     | USA    |     246 |      13 |         0.516 |      0.133 |     -0.118 |           3 |            2 |   -2.937 |  0.011 |              9 |              11 |      0.466 |      -0.572 |  0.01  |  85.874 |
| KLIMOV E   | RUS    |     130 |       7 |         0.515 |      0.117 |     -0.157 |           1 |            2 |   -2.529 | -0.016 |              1 |               5 |      0.202 |      -0.38  |  0.007 |  74.612 |
| MICHEL S   | SUI    |     256 |      14 |         0.504 |      0.122 |     -0.111 |           3 |            2 |   -2.402 |  0.006 |              5 |               9 |      0.312 |      -0.405 |  0.004 |  85.938 |
| WALSTAD S  | NOR    |     146 |       8 |         0.5   |      0.127 |     -0.151 |           0 |            2 |   -2.58  | -0.012 |              1 |               5 |      0.224 |      -0.379 |  0.018 |  73.63  |
| SHERRARD R | GER    |     218 |      12 |         0.482 |      0.113 |     -0.126 |           4 |            2 |   -2.37  | -0.011 |              6 |               4 |      0.376 |      -0.28  |  0.001 |  76.147 |
| MOSANER A  | ITA    |     218 |      12 |         0.482 |      0.127 |     -0.148 |           0 |            7 |   -3.504 | -0.016 |              8 |              11 |      0.351 |      -0.651 | -0.005 |  81.078 |
| LEE J      | KOR    |     230 |      12 |         0.426 |      0.126 |     -0.157 |           5 |            7 |   -4.412 | -0.036 |              8 |              13 |      0.453 |      -0.604 | -0.005 |  78.152 |
| SHIMIZU T  | JPN    |     282 |      15 |         0.418 |      0.114 |     -0.112 |           1 |            4 |   -2.82  | -0.018 |              5 |               5 |      0.359 |      -0.362 | -0.005 |  83.511 |

### Seconds

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| DE CRUZ P     | SUI    |     258 |      14 |         0.539 |      0.06  |     -0.085 |           0 |            1 |   -1.864 | -0.007 |              2 |               2 |      0.254 |      -0.237 |  0.001 |  88.424 |
| MAGNUSSON D   | SWE    |      30 |       3 |         0.5   |      0.064 |     -0.05  |           0 |            0 |   -0.446 |  0.007 |              0 |               0 |      0.089 |      -0.09  | -0.003 |  86.667 |
| TANIDA Y      | JPN    |     282 |      15 |         0.479 |      0.062 |     -0.073 |           0 |            1 |   -1.852 | -0.008 |              1 |               2 |      0.214 |      -0.237 |  0.001 |  87.766 |
| HOEKMAN L     | NED    |     234 |      12 |         0.479 |      0.076 |     -0.088 |           0 |            0 |   -1.857 | -0.01  |              4 |               3 |      0.301 |      -0.287 |  0.002 |  81.624 |
| WRANAA R      | SWE    |     216 |      13 |         0.477 |      0.067 |     -0.073 |           0 |            0 |   -1.391 | -0.006 |              1 |               0 |      0.207 |      -0.17  | -0.005 |  87.5   |
| LAMMIE B      | SCO    |     238 |      13 |         0.475 |      0.081 |     -0.07  |           0 |            0 |   -1.402 |  0.002 |              2 |               4 |      0.237 |      -0.262 | -0.002 |  87.395 |
| MYRAN J       | NOR    |      98 |       6 |         0.459 |      0.063 |     -0.071 |           0 |            0 |   -1.084 | -0.009 |              0 |               0 |      0.114 |      -0.131 | -0.003 |  76.531 |
| MIRONOV D     | RUS    |     218 |      12 |         0.45  |      0.057 |     -0.078 |           0 |            0 |   -1.197 | -0.017 |              1 |               0 |      0.198 |      -0.147 |  0.006 |  81.422 |
| HWANG H       | KOR    |     230 |      12 |         0.448 |      0.055 |     -0.07  |           0 |            0 |   -1.618 | -0.014 |              1 |               3 |      0.279 |      -0.259 | -0.001 |  81.739 |
| FLASCH C      | CAN    |     264 |      15 |         0.439 |      0.066 |     -0.078 |           0 |            0 |   -1.234 | -0.015 |              1 |               0 |      0.218 |      -0.21  | -0.001 |  82.89  |
| HAMILTON M    | USA    |     246 |      13 |         0.415 |      0.079 |     -0.074 |           0 |            0 |   -1.935 | -0.01  |              5 |               4 |      0.268 |      -0.278 |  0.003 |  86.382 |
| ARMAN S       | ITA    |     218 |      12 |         0.399 |      0.088 |     -0.087 |           1 |            0 |   -1.537 | -0.017 |              3 |               1 |      0.296 |      -0.245 |  0.005 |  79.724 |
| NEUNER D      | GER    |     218 |      12 |         0.394 |      0.082 |     -0.118 |           0 |            4 |   -2.907 | -0.04  |              2 |               6 |      0.217 |      -0.337 | -0     |  72.477 |
| MELLEMSETER M | NOR    |     188 |      11 |         0.335 |      0.117 |     -0.11  |           1 |            0 |   -1.798 | -0.034 |              1 |               1 |      0.213 |      -0.206 |  0.001 |  71.941 |

### Leads

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| ABE S         | JPN    |     282 |      15 |         0.504 |      0.026 |     -0.03  |           0 |            0 |   -0.658 | -0.002 |              0 |               0 |      0.163 |      -0.095 |  0.003 |  91.135 |
| TANNER V      | SUI    |     258 |      14 |         0.5   |      0.03  |     -0.028 |           0 |            0 |   -0.642 |  0.001 |              0 |               0 |      0.139 |      -0.108 | -0.002 |  93.066 |
| MCMILLAN H    | SCO    |     234 |      13 |         0.496 |      0.026 |     -0.026 |           0 |            0 |   -0.587 | -0     |              0 |               0 |      0.115 |      -0.083 | -0.002 |  92.949 |
| XU J          | CHN    |     126 |       7 |         0.492 |      0.029 |     -0.046 |           0 |            0 |   -0.611 | -0.009 |              0 |               0 |      0.069 |      -0.091 | -0.002 |  85.317 |
| SUNDGREN C    | SWE    |     226 |      14 |         0.487 |      0.03  |     -0.025 |           0 |            0 |   -0.581 |  0.002 |              0 |               0 |      0.071 |      -0.059 |  0.005 |  93.695 |
| KALALB A      | RUS    |     218 |      12 |         0.477 |      0.028 |     -0.036 |           0 |            0 |   -0.684 | -0.005 |              0 |               0 |      0.071 |      -0.1   |  0.003 |  90.138 |
| LEE D         | KOR    |      36 |       3 |         0.472 |      0.028 |     -0.064 |           0 |            0 |   -0.736 | -0.02  |              0 |               1 |      0.053 |      -0.114 | -0.002 |  70.833 |
| HEBERT B      | CAN    |     262 |      15 |         0.469 |      0.031 |     -0.031 |           0 |            0 |   -0.657 | -0.002 |              0 |               1 |      0.124 |      -0.146 |  0.001 |  93.798 |
| HAARSTAD A    | NOR    |     186 |      11 |         0.457 |      0.027 |     -0.039 |           0 |            0 |   -0.721 | -0.009 |              0 |               0 |      0.052 |      -0.111 |  0.003 |  86.425 |
| GLASBERGEN C  | NED    |     234 |      12 |         0.449 |      0.031 |     -0.034 |           0 |            0 |   -0.69  | -0.005 |              0 |               0 |      0.133 |      -0.105 | -0.001 |  89.637 |
| GREINDL D     | GER    |     128 |       7 |         0.445 |      0.028 |     -0.036 |           0 |            0 |   -0.57  | -0.007 |              0 |               0 |      0.036 |      -0.079 | -0.002 |  78.125 |
| SHAO Z        | CHN    |     142 |       8 |         0.444 |      0.035 |     -0.046 |           0 |            0 |   -1.211 | -0.01  |              0 |               1 |      0.086 |      -0.179 | -0.007 |  85.387 |
| JEONG B       | KOR    |     206 |      11 |         0.417 |      0.047 |     -0.06  |           0 |            0 |   -1.27  | -0.016 |              0 |               1 |      0.174 |      -0.2   | -0.002 |  81.917 |
| GONIN S       | ITA    |     218 |      12 |         0.404 |      0.028 |     -0.031 |           0 |            0 |   -0.615 | -0.007 |              0 |               1 |      0.129 |      -0.143 |  0.005 |  89.335 |
| LANDSTEINER J | USA    |     222 |      12 |         0.401 |      0.028 |     -0.026 |           0 |            0 |   -0.657 | -0.004 |              0 |               0 |      0.09  |      -0.092 | -0.001 |  90.878 |
| KAPP B        | GER    |      90 |       5 |         0.367 |      0.023 |     -0.036 |           0 |            0 |   -0.603 | -0.014 |              0 |               0 |      0.052 |      -0.082 | -0.002 |  85.278 |

