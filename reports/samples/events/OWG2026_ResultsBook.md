# Milano Cortina 2026 Olympic Winter Games, Curling (OWG2026_ResultsBook)

Cortina, Italy, 2026; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SUI    |      11 | 10-1     |  40.9 |   9.8 |  20.8 |      10.7 |    -0.5 |      77   |
| CAN    |      11 | 9-2      |  31.8 |   1.1 |  15.4 |      11.4 |     3.9 |      57.8 |
| GBR    |      11 | 6-5      |   4.5 |   1.1 |  16.5 |     -10.3 |    -2.7 |      59.5 |
| NOR    |      11 | 5-6      |  -4.5 |  -5.5 |   7.1 |      -4   |    -2.1 |      39.8 |
| ITA    |       9 | 4-5      |  -5.6 |  -4   | -10.9 |       5.6 |     3.7 |      52.6 |
| USA    |       9 | 4-5      |  -5.6 |   4   | -10.9 |       0.4 |     0.9 |      48.8 |
| GER    |       9 | 4-5      |  -5.6 |  -1.3 |   8.3 |     -12.6 |     0   |      46.3 |
| CZE    |       9 | 3-6      | -16.7 |  -4   | -19.9 |       6.1 |     1.1 |      35   |
| SWE    |       9 | 2-7      | -27.8 |   4   | -24.9 |      -4.1 |    -2.7 |      38.2 |
| CHN    |       9 | 2-7      | -27.8 |  -6.7 | -14.7 |      -5   |    -1.4 |      37.5 |

### Fourths

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SCHWARZ-VAN BERKEL | SUI    |     194 |      11 |         0.655 |      0.272 |     -0.242 |  0.095 |          23 |            9 |   -4.891 |             29 |              13 |      1.097 |      -0.756 |  0.006 |  87.565 |
| JACOBS B           | CAN    |     204 |      11 |         0.642 |      0.243 |     -0.218 |  0.078 |          20 |           11 |   -4.111 |             30 |              16 |      1.149 |      -0.743 |  0.013 |  85.714 |
| MOUAT B            | GBR    |     203 |      11 |         0.65  |      0.28  |     -0.301 |  0.077 |          22 |           13 |   -6.649 |             35 |              16 |      1.151 |      -1.248 |  0.009 |  84.606 |
| RAMSFJELL M        | NOR    |     214 |      11 |         0.593 |      0.27  |     -0.29  |  0.042 |          20 |           17 |   -8.425 |             29 |              19 |      1.148 |      -1.089 |  0.027 |  79.643 |
| MUSKATEWITZ M      | GER    |     177 |       9 |         0.588 |      0.294 |     -0.321 |  0.04  |          22 |           18 |   -5.425 |             24 |              23 |      1.412 |      -1.05  |  0.016 |  75.426 |
| RETORNAZ J         | ITA    |     166 |       9 |         0.578 |      0.261 |     -0.349 |  0.004 |          14 |           18 |   -7.095 |             23 |              18 |      0.88  |      -1.336 |  0.017 |  79.242 |
| EDIN N             | SWE    |     157 |       9 |         0.567 |      0.237 |     -0.332 | -0.009 |          10 |           12 |   -6.357 |             20 |              23 |      0.597 |      -1.078 |  0.015 |  74.204 |
| KLIMA L            | CZE    |     160 |       9 |         0.506 |      0.282 |     -0.311 | -0.011 |          16 |           16 |   -6.076 |             15 |              21 |      0.912 |      -0.671 |  0.004 |  73.594 |
| XU X               | CHN    |     169 |       9 |         0.515 |      0.255 |     -0.295 | -0.012 |          11 |           18 |   -6.574 |             19 |              21 |      0.862 |      -1.065 |  0.021 |  77.53  |
| CASPER D           | USA    |     166 |       9 |         0.524 |      0.224 |     -0.361 | -0.054 |           7 |           21 |   -8.648 |             18 |              22 |      1.201 |      -1.171 |  0.012 |  75.758 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| SCHWALLER Y | SUI    |     194 |      11 |         0.577 |      0.122 |     -0.128 |  0.017 |           0 |            1 |   -2.265 |              6 |               3 |      0.339 |      -0.277 | -0.009 |  88.66  |
| HARDIE G    | GBR    |     204 |      11 |         0.554 |      0.137 |     -0.134 |  0.016 |           2 |            1 |   -2.346 |             10 |               5 |      0.48  |      -0.332 | -0.006 |  87.868 |
| VIOLETTE L  | USA    |     166 |       9 |         0.512 |      0.117 |     -0.142 | -0.01  |           0 |            5 |   -3.306 |              1 |               8 |      0.236 |      -0.424 | -0.009 |  80.12  |
| ERIKSSON O  | SWE    |     164 |       9 |         0.488 |      0.135 |     -0.151 | -0.012 |           3 |            5 |   -3.743 |              5 |               4 |      0.355 |      -0.452 | -0.002 |  81.402 |
| KENNEDY M   | CAN    |     206 |      11 |         0.461 |      0.14  |     -0.142 | -0.012 |           3 |            5 |   -3.585 |              5 |               7 |      0.401 |      -0.712 | -0.009 |  86.22  |
| CERNOVSKY M | CZE    |     164 |       9 |         0.451 |      0.133 |     -0.141 | -0.017 |           0 |            2 |   -2.603 |              5 |               3 |      0.368 |      -0.259 |  0.006 |  81.25  |
| KAPP B      | GER    |     178 |       9 |         0.472 |      0.125 |     -0.149 | -0.02  |           1 |            5 |   -2.984 |              5 |               8 |      0.491 |      -0.555 |  0.019 |  84.41  |
| FEI X       | CHN    |     170 |       9 |         0.388 |      0.125 |     -0.125 | -0.028 |           1 |            4 |   -3.084 |              8 |               9 |      0.322 |      -0.476 |  0.007 |  82.206 |
| SESAKER M   | NOR    |     216 |      11 |         0.431 |      0.128 |     -0.149 | -0.03  |           1 |            2 |   -2.656 |             11 |               7 |      0.457 |      -0.351 |  0.002 |  78.009 |
| MOSANER A   | ITA    |     166 |       9 |         0.398 |      0.104 |     -0.139 | -0.043 |           1 |            3 |   -3.68  |              3 |               6 |      0.308 |      -0.618 | -0.004 |  81.364 |

### Seconds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MICHEL S     | SUI    |     194 |      11 |         0.562 |      0.076 |     -0.064 |  0.014 |           0 |            0 |   -1.34  |              3 |               0 |      0.27  |      -0.15  | -0.019 |  86.34  |
| ARMAN S      | ITA    |     166 |       9 |         0.518 |      0.068 |     -0.086 | -0.006 |           0 |            0 |   -1.63  |              1 |               3 |      0.199 |      -0.305 | -0.001 |  85.542 |
| GALLANT B    | CAN    |     206 |      11 |         0.5   |      0.069 |     -0.084 | -0.007 |           0 |            0 |   -1.722 |              2 |               2 |      0.197 |      -0.207 | -0.004 |  83.617 |
| MESSENZEHL F | GER    |     178 |       9 |         0.455 |      0.089 |     -0.102 | -0.015 |           0 |            0 |   -1.757 |              5 |               2 |      0.333 |      -0.235 |  0.002 |  87.36  |
| LI Z         | CHN    |     170 |       9 |         0.459 |      0.058 |     -0.079 | -0.016 |           0 |            0 |   -1.46  |              1 |               3 |      0.236 |      -0.248 | -0.004 |  78.235 |
| LAMMIE B     | GBR    |     204 |      11 |         0.461 |      0.07  |     -0.092 | -0.017 |           0 |            1 |   -2.144 |              3 |               4 |      0.273 |      -0.265 | -0.01  |  79.167 |
| RICHARDSON B | USA    |     166 |       9 |         0.446 |      0.071 |     -0.094 | -0.02  |           0 |            0 |   -1.501 |              0 |               1 |      0.212 |      -0.219 | -0.009 |  78.464 |
| RAMSFJELL B  | NOR    |     216 |      11 |         0.407 |      0.062 |     -0.082 | -0.023 |           0 |            0 |   -1.903 |              2 |               2 |      0.22  |      -0.249 | -0.004 |  77.778 |
| WRANAA R     | SWE    |     160 |       9 |         0.45  |      0.072 |     -0.11  | -0.028 |           0 |            0 |   -1.598 |              0 |               1 |      0.145 |      -0.223 | -0     |  84.375 |
| JURIK M      | CZE    |     164 |       9 |         0.384 |      0.065 |     -0.097 | -0.035 |           0 |            0 |   -1.751 |              1 |               2 |      0.134 |      -0.216 | -0.002 |  75.457 |

### Leads

| player             | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| LACHAT-COUCHEPIN P | SUI    |     192 |      11 |         0.536 |      0.044 |     -0.039 |  0.006 |           0 |            0 |   -0.635 |              0 |               0 |      0.103 |      -0.145 |  0.005 |  91.099 |
| OLDENBURG A        | USA    |     164 |       9 |         0.585 |      0.039 |     -0.045 |  0.004 |           0 |            0 |   -0.569 |              0 |               0 |      0.101 |      -0.082 |  0.003 |  92.53  |
| XU J               | CHN    |     170 |       9 |         0.588 |      0.037 |     -0.044 |  0.004 |           0 |            0 |   -0.686 |              0 |               0 |      0.107 |      -0.123 |  0.004 |  87.647 |
| KLIPA L            | CZE    |     160 |       9 |         0.556 |      0.039 |     -0.051 | -0.001 |           0 |            0 |   -0.597 |              0 |               0 |      0.077 |      -0.071 | -0     |  89.151 |
| GIOVANELLA M       | ITA    |     166 |       9 |         0.584 |      0.035 |     -0.053 | -0.002 |           0 |            0 |   -0.746 |              1 |               0 |      0.16  |      -0.109 |  0.003 |  85.909 |
| NEPSTAD G          | NOR    |     216 |      11 |         0.519 |      0.04  |     -0.046 | -0.002 |           0 |            0 |   -0.655 |              0 |               0 |      0.104 |      -0.118 |  0.001 |  86.806 |
| MCMILLAN H         | GBR    |     204 |      11 |         0.529 |      0.034 |     -0.043 | -0.002 |           0 |            0 |   -0.563 |              0 |               0 |      0.086 |      -0.126 | -0.001 |  91.789 |
| SUNDGREN C         | SWE    |     164 |       9 |         0.573 |      0.038 |     -0.057 | -0.003 |           0 |            0 |   -0.894 |              0 |               0 |      0.069 |      -0.131 | -0.003 |  90.244 |
| HEBERT B           | CAN    |     182 |      10 |         0.522 |      0.034 |     -0.044 | -0.003 |           0 |            0 |   -0.64  |              0 |               0 |      0.096 |      -0.094 |  0.002 |  92.033 |
| SCHEUERL J         | GER    |     176 |       9 |         0.54  |      0.034 |     -0.048 | -0.004 |           0 |            0 |   -0.679 |              0 |               0 |      0.094 |      -0.107 |  0     |  90.909 |

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SWE    |      11 | 9-2      |  31.8 |   3.1 |  12.6 |      15.6 |     0.6 |      61.8 |
| CAN    |      11 | 7-4      |  13.6 |   1   |   8.6 |       6.8 |    -2.8 |      59.5 |
| SUI    |      11 | 7-4      |  13.6 |  -5.1 |  33.5 |     -18.2 |     3.5 |      51.5 |
| KOR    |       9 | 5-4      |   5.6 |   6.3 | -15   |      15.3 |    -1   |      59.3 |
| GBR    |       9 | 5-4      |   5.6 |   3.8 |  -4.2 |       7.2 |    -1.3 |      55.6 |
| USA    |      11 | 6-5      |   4.5 |   1   |   5.3 |      -4.3 |     2.5 |      48.8 |
| DEN    |       9 | 4-5      |  -5.6 |  -3.8 |  -3.1 |       0.8 |     0.5 |      49.2 |
| CHN    |       9 | 2-7      | -27.8 |  -1.3 | -18.1 |      -6.6 |    -1.8 |      39.1 |
| ITA    |       9 | 2-7      | -27.8 |  -1.3 | -24.8 |      -0.6 |    -1.1 |      37.9 |
| JPN    |       9 | 2-7      | -27.8 |  -3.8 |  -8.2 |     -15.9 |     0.1 |      32.5 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| PAETZ A       | SUI    |     218 |      11 |         0.569 |      0.291 |     -0.236 |  0.064 |          22 |           14 |   -4.476 |             40 |              30 |      1.5   |      -0.854 |  0.015 |  82.407 |
| HASSELBORG A  | SWE    |     207 |      11 |         0.585 |      0.306 |     -0.282 |  0.062 |          24 |           14 |   -6.1   |             35 |              19 |      1.355 |      -0.691 | -0.004 |  80.825 |
| HOMAN R       | CAN    |     214 |      11 |         0.57  |      0.285 |     -0.26  |  0.051 |          20 |           17 |   -4.602 |             28 |              23 |      1.29  |      -0.792 |  0.007 |  77.817 |
| MORRISON R    | GBR    |     166 |       9 |         0.554 |      0.319 |     -0.295 |  0.046 |          21 |           12 |   -5.784 |             26 |              19 |      1.108 |      -0.821 |  0.007 |  81.627 |
| DUPONT M      | DEN    |     163 |       9 |         0.491 |      0.31  |     -0.284 |  0.007 |          16 |           10 |   -7.329 |             21 |              20 |      1.154 |      -1.29  |  0.014 |  75.932 |
| PETERSON T    | USA    |     214 |      11 |         0.491 |      0.293 |     -0.268 |  0.007 |          18 |           16 |   -7.454 |             27 |              27 |      1.385 |      -1.452 |  0.033 |  79.695 |
| YOSHIMURA S   | JPN    |     174 |       9 |         0.546 |      0.278 |     -0.336 | -0.001 |          16 |           13 |   -7.937 |             27 |              23 |      0.87  |      -1.231 |  0.016 |  73.132 |
| CONSTANTINI S | ITA    |     167 |       9 |         0.443 |      0.323 |     -0.279 | -0.012 |          19 |           14 |   -5.633 |             19 |              24 |      1.27  |      -1.256 |  0.013 |  72.59  |
| GIM E         | KOR    |     163 |       9 |         0.54  |      0.273 |     -0.353 | -0.015 |          11 |           18 |   -8.166 |             24 |              21 |      0.862 |      -1.414 |  0.02  |  77.16  |
| WANG R        | CHN    |     173 |       9 |         0.468 |      0.271 |     -0.3   | -0.033 |          14 |           19 |   -5.82  |             23 |              33 |      0.689 |      -1.095 |  0.015 |  74.273 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HAN Y       | CHN    |     174 |       9 |         0.483 |      0.163 |     -0.106 |  0.024 |           3 |            1 |   -1.86  |             13 |               4 |      0.427 |      -0.33  |  0.008 |  83.477 |
| TIRINZONI S | SUI    |     220 |      11 |         0.523 |      0.142 |     -0.127 |  0.014 |           2 |            3 |   -2.576 |             13 |               6 |      0.506 |      -0.291 |  0.009 |  83.977 |
| ONODERA K   | JPN    |     174 |       9 |         0.494 |      0.157 |     -0.129 |  0.012 |           2 |            4 |   -2.918 |             11 |               6 |      0.456 |      -0.457 |  0.003 |  77.874 |
| FLEURY T    | CAN    |     216 |      11 |         0.546 |      0.152 |     -0.171 |  0.005 |           2 |            7 |   -3.23  |             14 |              13 |      0.492 |      -0.527 | -0.003 |  79.302 |
| HALSE M     | DEN    |     164 |       9 |         0.482 |      0.152 |     -0.137 |  0.002 |           2 |            4 |   -2.652 |              7 |               8 |      0.369 |      -0.43  |  0.008 |  75.457 |
| THIESSE C   | USA    |     214 |      11 |         0.463 |      0.148 |     -0.128 | -0     |           2 |            3 |   -3.08  |             11 |              10 |      0.48  |      -0.485 |  0.013 |  81.075 |
| MCMANUS S   | SWE    |     208 |      11 |         0.466 |      0.17  |     -0.15  | -0.001 |           2 |            4 |   -2.651 |             16 |              14 |      0.363 |      -0.454 |  0.002 |  78.486 |
| KIM M       | KOR    |     164 |       9 |         0.427 |      0.16  |     -0.123 | -0.002 |           4 |            3 |   -2.747 |              7 |               5 |      0.482 |      -0.46  | -0.001 |  82.927 |
| DODDS J     | GBR    |     166 |       9 |         0.434 |      0.136 |     -0.142 | -0.022 |           1 |            3 |   -2.672 |              2 |               7 |      0.256 |      -0.465 |  0.003 |  81.627 |
| MATHIS E    | ITA    |     168 |       9 |         0.411 |      0.125 |     -0.153 | -0.039 |           1 |            0 |   -2.248 |              4 |              13 |      0.436 |      -0.467 |  0.001 |  77.695 |

### Seconds

| player         | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:---------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| LO DESERTO M   | ITA    |     126 |       7 |         0.548 |      0.097 |     -0.083 |  0.016 |           0 |            0 |   -1.145 |              3 |               0 |      0.275 |      -0.165 |  0.009 |  80.357 |
| DONG Z         | CHN    |     174 |       9 |         0.466 |      0.076 |     -0.078 | -0.006 |           0 |            1 |   -1.702 |              3 |               2 |      0.256 |      -0.256 |  0.003 |  81.034 |
| KIM S          | KOR    |     144 |       8 |         0.41  |      0.104 |     -0.083 | -0.006 |           1 |            0 |   -1.43  |              3 |               2 |      0.3   |      -0.23  | -0.006 |  81.076 |
| KNOCHENHAUER A | SWE    |     208 |      11 |         0.442 |      0.074 |     -0.083 | -0.013 |           0 |            0 |   -1.403 |              5 |               1 |      0.34  |      -0.291 |  0.001 |  82.85  |
| HOWALD C       | SUI    |     220 |      11 |         0.468 |      0.073 |     -0.097 | -0.017 |           0 |            3 |   -2.441 |              4 |               6 |      0.306 |      -0.407 |  0.003 |  84.659 |
| MISKEW E       | CAN    |     216 |      11 |         0.472 |      0.074 |     -0.103 | -0.02  |           0 |            0 |   -1.652 |              3 |               2 |      0.296 |      -0.277 |  0.008 |  78.819 |
| PETERSON TS    | USA    |     214 |      11 |         0.449 |      0.067 |     -0.091 | -0.02  |           0 |            1 |   -2.049 |              1 |               4 |      0.267 |      -0.359 | -0.002 |  80.634 |
| SINCLAIR S     | GBR    |     166 |       9 |         0.44  |      0.075 |     -0.098 | -0.022 |           0 |            0 |   -1.803 |              2 |               1 |      0.213 |      -0.246 | -0.01  |  79.848 |
| HOLTERMANN J   | DEN    |     164 |       9 |         0.451 |      0.066 |     -0.096 | -0.023 |           0 |            0 |   -1.762 |              0 |               3 |      0.206 |      -0.306 |  0.003 |  76.677 |
| KOTANI Y       | JPN    |     154 |       8 |         0.409 |      0.073 |     -0.101 | -0.03  |           0 |            2 |   -2.277 |              0 |               2 |      0.184 |      -0.33  |  0.003 |  78.247 |

### Leads

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WILKES S          | CAN    |     216 |      11 |         0.616 |      0.038 |     -0.057 |  0.001 |           0 |            0 |   -0.79  |              0 |               0 |      0.125 |      -0.144 |  0.002 |  85.995 |
| OHMIYA A          | JPN    |     174 |       9 |         0.575 |      0.033 |     -0.046 | -0.001 |           0 |            0 |   -0.54  |              0 |               0 |      0.171 |      -0.084 | -0.003 |  85.345 |
| JIANG J           | CHN    |     174 |       9 |         0.523 |      0.037 |     -0.042 | -0.001 |           0 |            0 |   -0.597 |              0 |               0 |      0.104 |      -0.074 | -0.002 |  91.954 |
| WITSCHONKE S      | SUI    |     220 |      11 |         0.564 |      0.034 |     -0.047 | -0.001 |           0 |            0 |   -0.801 |              0 |               0 |      0.112 |      -0.118 |  0.002 |  88.864 |
| JACKSON S         | GBR    |     166 |       9 |         0.53  |      0.039 |     -0.047 | -0.001 |           0 |            0 |   -0.718 |              0 |               0 |      0.1   |      -0.085 |  0     |  90.586 |
| SCHARBACK S       | SWE    |     200 |      11 |         0.565 |      0.031 |     -0.054 | -0.006 |           0 |            0 |   -0.839 |              0 |               0 |      0.086 |      -0.128 |  0.002 |  86.25  |
| MARIANI R         | ITA    |      42 |       2 |         0.476 |      0.045 |     -0.054 | -0.007 |           0 |            0 |   -0.533 |              0 |               0 |      0.096 |      -0.073 | -0.008 |  79.762 |
| DUPONT D          | DEN    |     164 |       9 |         0.488 |      0.035 |     -0.048 | -0.008 |           0 |            0 |   -0.692 |              0 |               0 |      0.109 |      -0.118 |  0.002 |  79.726 |
| ANDERSON-HEIDE T  | USA    |     214 |      11 |         0.486 |      0.033 |     -0.051 | -0.01  |           0 |            0 |   -0.808 |              0 |               0 |      0.085 |      -0.142 |  0.003 |  85.514 |
| ZARDINI LACEDELLI | ITA    |     168 |       9 |         0.464 |      0.05  |     -0.067 | -0.013 |           0 |            0 |   -1.3   |              1 |               1 |      0.157 |      -0.193 |  0.005 |  84.524 |
| SEOL YEE          | KOR    |     164 |       9 |         0.457 |      0.033 |     -0.053 | -0.014 |           0 |            0 |   -0.765 |              0 |               0 |      0.069 |      -0.113 | -0.003 |  84.909 |

