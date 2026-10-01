# Olympic Winter Games (OWG2022_ResultsBook)

Beijing, China, 2022; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `net` is the mean over every shot, which folds the three together (reliability times the average make plus the rest times the average miss). The big shots follow: `big_makes` / `big_misses` count shots beyond half a point either way, `worst5` sums the five costliest shots, and the `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by net, then by reliability. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Men

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| GBR    |      11 | 9-2      |  31.8 |   3.3 |  17.9 |      10.1 |     0.6 |      67.2 |
| SWE    |      11 | 9-2      |  31.8 |   7.6 |  12.5 |      11.5 |     0.2 |      65   |
| CAN    |      11 | 6-5      |   4.5 |  -5.5 |   9   |       0.8 |     0.1 |      52.5 |
| USA    |      11 | 5-6      |  -4.5 |  -5.5 |  -4   |       6   |    -1.2 |      45.5 |
| SUI    |       9 | 4-5      |  -5.6 |   6.7 |  -1.3 |     -11.2 |     0.3 |      53.4 |
| NOR    |       9 | 4-5      |  -5.6 |  -6.7 |  -4   |       4.7 |     0.4 |      48.3 |
| CHN    |       9 | 4-5      |  -5.6 |   6.7 |   5.4 |     -15.6 |    -2   |      48   |
| ROC    |       9 | 4-5      |  -5.6 |  -4   |  -0.7 |      -2.7 |     1.8 |      42.4 |
| ITA    |       9 | 3-6      | -16.7 |  -1.3 | -10.4 |      -4.9 |    -0.1 |      44.7 |
| DEN    |       9 | 1-8      | -38.9 |  -1.3 | -32.5 |      -5   |    -0.1 |      26.3 |

### Fourths

| player     | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MOUAT B    | GBR    |     209 |      11 |         0.627 |      0.211 |     -0.223 |  0.049 |          12 |            8 |   -5.149 |             22 |              13 |      0.723 |      -0.696 |  0.004 |  88.702 |
| EDIN N     | SWE    |     214 |      11 |         0.607 |      0.214 |     -0.24  |  0.036 |          13 |           13 |   -4.128 |             32 |              22 |      0.943 |      -0.753 | -0.002 |  83.929 |
| GUSHUE B   | CAN    |     209 |      11 |         0.593 |      0.201 |     -0.243 |  0.021 |           9 |            6 |   -5.582 |             25 |              29 |      0.854 |      -1.178 |  0.008 |  81.585 |
| WALSTAD S  | NOR    |     172 |       9 |         0.605 |      0.204 |     -0.263 |  0.019 |          12 |            8 |   -5.743 |             16 |              20 |      0.835 |      -1.534 |  0.008 |  82.267 |
| RETORNAZ J | ITA    |     160 |       9 |         0.506 |      0.296 |     -0.265 |  0.019 |          14 |           14 |   -5.32  |             17 |              22 |      0.873 |      -0.803 | -0.003 |  79.062 |
| MA X       | CHN    |     178 |       9 |         0.545 |      0.222 |     -0.246 |  0.009 |           8 |           12 |   -4.97  |             21 |              20 |      0.742 |      -0.848 |  0.009 |  81.039 |
| GLUKHOV S  | ROC    |     171 |       9 |         0.591 |      0.232 |     -0.326 |  0.004 |          14 |           13 |   -8.024 |             23 |              17 |      1.407 |      -0.985 | -0.001 |  80.147 |
| SCHWARZ B  | SUI    |     175 |       9 |         0.549 |      0.216 |     -0.255 |  0.003 |          10 |           13 |   -5.585 |             16 |              26 |      1.316 |      -1.017 | -0.014 |  82.749 |
| SHUSTER J  | USA    |     211 |      11 |         0.526 |      0.246 |     -0.333 | -0.028 |          15 |           21 |   -8.494 |             24 |              31 |      1.099 |      -0.985 | -0.004 |  80.288 |
| KRAUSE M   | DEN    |     157 |       9 |         0.503 |      0.23  |     -0.353 | -0.06  |          11 |           19 |   -8.129 |             15 |              22 |      0.758 |      -1.395 |  0.01  |  73.726 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HARDIE G    | GBR    |     210 |      11 |         0.552 |      0.136 |     -0.118 |  0.023 |           2 |            1 |   -2.542 |              9 |               5 |      0.459 |      -0.432 | -0.008 |  87.381 |
| NERGAARD T  | NOR    |     172 |       9 |         0.552 |      0.12  |     -0.103 |  0.02  |           1 |            0 |   -1.976 |              6 |               0 |      0.425 |      -0.222 |  0.003 |  84.157 |
| ZOU Q       | CHN    |     180 |       9 |         0.472 |      0.133 |     -0.097 |  0.012 |           3 |            0 |   -1.627 |              7 |               4 |      0.399 |      -0.296 |  0.002 |  85.972 |
| ERIKSSON O  | SWE    |     216 |      11 |         0.523 |      0.125 |     -0.122 |  0.007 |           3 |            3 |   -2.811 |              9 |               5 |      0.476 |      -0.391 | -0.01  |  87.269 |
| NICHOLS M   | CAN    |     212 |      11 |         0.552 |      0.118 |     -0.13  |  0.007 |           2 |            2 |   -2.607 |              8 |              12 |      0.444 |      -0.459 | -0.001 |  80.778 |
| MOSANER A   | ITA    |     162 |       9 |         0.512 |      0.117 |     -0.127 | -0.002 |           1 |            2 |   -2.604 |              3 |               5 |      0.301 |      -0.436 |  0.003 |  81.327 |
| MICHEL S    | SUI    |     170 |       9 |         0.553 |      0.109 |     -0.14  | -0.002 |           1 |            3 |   -2.717 |              7 |               7 |      0.412 |      -0.476 | -0.002 |  80.621 |
| PLYS C      | USA    |     216 |      11 |         0.5   |      0.125 |     -0.138 | -0.007 |           1 |            3 |   -2.547 |              7 |              13 |      0.37  |      -0.459 |  0.004 |  79.398 |
| KLIMOV E    | ROC    |     174 |       9 |         0.489 |      0.113 |     -0.138 | -0.015 |           2 |            3 |   -2.797 |              6 |              10 |      0.415 |      -0.559 |  0.001 |  78.736 |
| NOERGAARD M | DEN    |     158 |       9 |         0.411 |      0.085 |     -0.135 | -0.044 |           0 |            3 |   -2.836 |              2 |               6 |      0.25  |      -0.389 |  0.016 |  74.842 |

### Seconds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| DE CRUZ P    | SUI    |     180 |       9 |         0.556 |      0.085 |     -0.074 |  0.014 |           0 |            0 |   -1.311 |              4 |               0 |      0.27  |      -0.167 |  0.002 |  85.139 |
| HAMILTON M   | USA    |     216 |      11 |         0.514 |      0.074 |     -0.07  |  0.004 |           0 |            0 |   -1.278 |              0 |               0 |      0.188 |      -0.169 |  0.009 |  84.375 |
| WANG Z       | CHN    |     180 |       9 |         0.506 |      0.058 |     -0.06  | -0     |           0 |            0 |   -1.167 |              3 |               1 |      0.28  |      -0.178 |  0.002 |  87.849 |
| LAMMIE B     | GBR    |     210 |      11 |         0.505 |      0.069 |     -0.074 | -0.002 |           0 |            0 |   -1.334 |              4 |               1 |      0.308 |      -0.204 |  0     |  85.119 |
| HOEIBERG M   | NOR    |     172 |       9 |         0.424 |      0.07  |     -0.06  | -0.005 |           0 |            0 |   -1.151 |              1 |               2 |      0.207 |      -0.257 | -0.004 |  79.438 |
| GALLANT B    | CAN    |     204 |      11 |         0.471 |      0.088 |     -0.088 | -0.005 |           0 |            0 |   -1.726 |              4 |               3 |      0.3   |      -0.285 |  0     |  81.005 |
| WRANAA R     | SWE    |     216 |      11 |         0.523 |      0.071 |     -0.09  | -0.006 |           0 |            2 |   -2.151 |              1 |               4 |      0.242 |      -0.328 | -0.001 |  85.814 |
| ARMAN S      | ITA    |     162 |       9 |         0.444 |      0.075 |     -0.086 | -0.014 |           0 |            0 |   -1.633 |              1 |               2 |      0.23  |      -0.244 | -0.004 |  80.745 |
| MIRONOV D    | ROC    |     174 |       9 |         0.425 |      0.064 |     -0.073 | -0.015 |           0 |            0 |   -1.472 |              1 |               1 |      0.195 |      -0.194 | -0.003 |  77.746 |
| HOLTERMANN H | DEN    |     158 |       9 |         0.424 |      0.067 |     -0.09  | -0.024 |           0 |            0 |   -1.786 |              0 |               2 |      0.159 |      -0.261 |  0.008 |  76.582 |

### Leads

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| GONIN S       | ITA    |      94 |       5 |         0.489 |      0.032 |     -0.032 | -0.001 |           0 |            0 |   -0.54  |              0 |               0 |      0.054 |      -0.077 | -0.001 |  85.638 |
| WIKSTEN K     | DEN    |     140 |       8 |         0.514 |      0.032 |     -0.036 | -0.001 |           0 |            0 |   -0.741 |              0 |               0 |      0.057 |      -0.116 | -0     |  87.5   |
| SUNDGREN C    | SWE    |     216 |      11 |         0.486 |      0.029 |     -0.032 | -0.002 |           0 |            0 |   -0.564 |              0 |               0 |      0.101 |      -0.101 |  0.001 |  90.162 |
| KALALB A      | ROC    |     174 |       9 |         0.506 |      0.029 |     -0.035 | -0.003 |           0 |            0 |   -0.656 |              0 |               0 |      0.087 |      -0.102 | -0.001 |  88.075 |
| WALKER G      | CAN    |     212 |      11 |         0.425 |      0.033 |     -0.03  | -0.003 |           0 |            0 |   -0.57  |              1 |               0 |      0.146 |      -0.093 | -0.001 |  90.33  |
| MCMILLAN H    | GBR    |     210 |      11 |         0.424 |      0.028 |     -0.027 | -0.003 |           0 |            0 |   -0.695 |              0 |               1 |      0.098 |      -0.143 |  0     |  92.476 |
| VAAGBERG M    | NOR    |     172 |       9 |         0.419 |      0.031 |     -0.029 | -0.004 |           0 |            0 |   -0.576 |              0 |               0 |      0.088 |      -0.127 |  0.001 |  91.57  |
| LANDSTEINER J | USA    |     208 |      11 |         0.423 |      0.031 |     -0.031 | -0.004 |           0 |            0 |   -0.605 |              0 |               0 |      0.089 |      -0.101 | -0     |  85.938 |
| TANNER V      | SUI    |     180 |       9 |         0.461 |      0.034 |     -0.038 | -0.005 |           0 |            0 |   -0.841 |              1 |               0 |      0.183 |      -0.154 | -0.005 |  89.167 |
| XU J          | CHN    |     180 |       9 |         0.383 |      0.028 |     -0.038 | -0.012 |           0 |            0 |   -0.806 |              0 |               0 |      0.065 |      -0.114 |  0.003 |  86.872 |
| GIOVANELLA M  | ITA    |      68 |       4 |         0.353 |      0.03  |     -0.04  | -0.016 |           0 |            0 |   -0.601 |              0 |               0 |      0.038 |      -0.106 |  0.004 |  85.821 |

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SUI    |      11 | 8-3      |  22.7 |   7.3 |   2.1 |      11.9 |     1.5 |      54.9 |
| SWE    |      11 | 8-3      |  22.7 |   1   |   8.1 |      14.1 |    -0.6 |      54.3 |
| GBR    |      11 | 7-4      |  13.6 |   3.1 |   3.7 |       6.7 |     0.1 |      63.5 |
| CAN    |       9 | 5-4      |   5.6 |  -3.8 |   7.4 |      -1.5 |     3.5 |      57.7 |
| JPN    |      11 | 6-5      |   4.5 |  -5.2 |   0.8 |       9   |    -0.1 |      44.5 |
| KOR    |       9 | 4-5      |  -5.6 |  -1.3 |  11.7 |     -14.7 |    -1.3 |      54.6 |
| USA    |       9 | 4-5      |  -5.6 |  -3.8 |  -4.4 |       3.8 |    -1.1 |      48.6 |
| CHN    |       9 | 4-5      |  -5.6 |   1.3 |  11.5 |     -12.6 |    -5.8 |      40.2 |
| DEN    |       9 | 2-7      | -27.8 |   3.8 | -18.5 |     -14.3 |     1.2 |      43.5 |
| ROC    |       9 | 1-8      | -38.9 |  -3.8 | -25.7 |     -11.7 |     2.4 |      34.2 |

### Fourths

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HASSELBORG A | SWE    |     207 |      11 |         0.599 |      0.283 |     -0.28  |  0.057 |          19 |           13 |   -6.213 |             28 |              21 |      1.041 |      -1.054 | -0.002 |  77.439 |
| JONES J      | CAN    |     173 |       9 |         0.549 |      0.346 |     -0.318 |  0.047 |          19 |           16 |   -5.515 |             32 |              23 |      1.098 |      -1.316 |  0.002 |  74.419 |
| MUIRHEAD E   | GBR    |     204 |      11 |         0.593 |      0.258 |     -0.291 |  0.035 |          18 |           16 |   -4.95  |             23 |              23 |      1.034 |      -1.249 | -0.001 |  77.941 |
| PETERSON TAB | USA    |     166 |       9 |         0.59  |      0.277 |     -0.345 |  0.022 |          17 |           15 |   -7.689 |             19 |              20 |      0.566 |      -0.827 |  0.014 |  79.268 |
| FUJISAWA S   | JPN    |     202 |      11 |         0.554 |      0.253 |     -0.314 |  0     |          16 |           18 |   -8.321 |             19 |              19 |      1.343 |      -1.139 |  0.009 |  79.975 |
| PAETZ A      | SUI    |     222 |      11 |         0.554 |      0.228 |     -0.283 |  0     |          15 |           20 |   -5.205 |             25 |              36 |      0.876 |      -1.269 |  0.005 |  76.239 |
| WANG R       | CHN    |     176 |       9 |         0.574 |      0.224 |     -0.322 | -0.009 |          12 |           17 |   -5.272 |             26 |              22 |      1.491 |      -0.814 |  0.023 |  76.847 |
| KIM E        | KOR    |     180 |       9 |         0.556 |      0.276 |     -0.371 | -0.012 |          15 |           19 |   -8.331 |             27 |              25 |      1.364 |      -1.385 |  0.024 |  79.749 |
| DUPONT M     | DEN    |     168 |       9 |         0.536 |      0.271 |     -0.339 | -0.012 |          13 |           16 |   -8.187 |             17 |              25 |      1.214 |      -1.013 | -0     |  75     |
| KOVALEVA A   | ROC    |     165 |       9 |         0.552 |      0.217 |     -0.421 | -0.069 |           9 |           23 |   -8.198 |             12 |              27 |      0.422 |      -1.125 |  0.001 |  73.018 |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| PORTUNOVA J | ROC    |     166 |       9 |         0.578 |      0.138 |     -0.149 |  0.017 |           3 |            3 |   -2.427 |              6 |               5 |      0.3   |      -0.348 |  0.012 |  77.108 |
| TIRINZONI S | SUI    |     216 |      11 |         0.556 |      0.108 |     -0.114 |  0.009 |           1 |            1 |   -2.463 |              5 |               7 |      0.354 |      -0.448 |  0.012 |  79.398 |
| WRIGHT V    | GBR    |     206 |      11 |         0.578 |      0.109 |     -0.127 |  0.009 |           1 |            1 |   -2.399 |              6 |               3 |      0.339 |      -0.39  | -0.009 |  82.646 |
| KIM K       | KOR    |     180 |       9 |         0.572 |      0.131 |     -0.158 |  0.007 |           2 |            3 |   -3.239 |              8 |               8 |      0.45  |      -0.582 | -0.001 |  79.306 |
| MCMANUS S   | SWE    |     210 |      11 |         0.538 |      0.119 |     -0.136 |  0.001 |           2 |            3 |   -2.999 |              7 |               9 |      0.517 |      -0.392 |  0.001 |  79.524 |
| LAWES K     | CAN    |     176 |       9 |         0.54  |      0.129 |     -0.158 | -0.003 |           1 |            3 |   -2.579 |              8 |               8 |      0.458 |      -0.379 | -0.018 |  79.741 |
| ROTH N      | USA    |     170 |       9 |         0.547 |      0.129 |     -0.164 | -0.004 |           2 |            3 |   -3.082 |              7 |               8 |      0.426 |      -0.426 | -0.003 |  80.735 |
| YOSHIDA C   | JPN    |     208 |      11 |         0.514 |      0.115 |     -0.145 | -0.011 |           2 |            5 |   -3.248 |              7 |               8 |      0.303 |      -0.471 | -0.006 |  77.644 |
| HAN Y       | CHN    |     116 |       6 |         0.534 |      0.186 |     -0.261 | -0.022 |           3 |            7 |   -5.324 |              9 |              14 |      0.5   |      -0.798 |  0.004 |  73.491 |
| HALSE M     | DEN    |     168 |       9 |         0.452 |      0.104 |     -0.167 | -0.045 |           0 |            5 |   -3.531 |              4 |              12 |      0.331 |      -0.697 |  0.005 |  74.256 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| DODDS J          | GBR    |     206 |      11 |         0.534 |      0.073 |     -0.073 |  0.005 |           0 |            0 |   -1.456 |              2 |               2 |      0.222 |      -0.208 | -0.002 |  81.917 |
| PETERMAN J       | CAN    |     176 |       9 |         0.472 |      0.095 |     -0.077 |  0.004 |           1 |            0 |   -1.513 |              6 |               2 |      0.316 |      -0.228 | -0.001 |  78.125 |
| DUPONT D         | DEN    |     168 |       9 |         0.5   |      0.075 |     -0.076 | -0     |           0 |            0 |   -1.451 |              0 |               0 |      0.204 |      -0.196 |  0.008 |  76.935 |
| KIM C            | KOR    |     140 |       7 |         0.557 |      0.082 |     -0.11  | -0.003 |           0 |            1 |   -2.073 |              1 |               2 |      0.219 |      -0.248 | -0.001 |  81.429 |
| NEUENSCHWANDER E | SUI    |     224 |      11 |         0.513 |      0.076 |     -0.086 | -0.003 |           0 |            1 |   -2.003 |              4 |               2 |      0.379 |      -0.312 |  0.004 |  83.484 |
| SUZUKI Y         | JPN    |     208 |      11 |         0.51  |      0.072 |     -0.082 | -0.003 |           0 |            0 |   -1.83  |              1 |               3 |      0.216 |      -0.286 | -0.003 |  81.37  |
| KNOCHENHAUER A   | SWE    |     210 |      11 |         0.471 |      0.075 |     -0.077 | -0.006 |           1 |            0 |   -1.384 |              1 |               2 |      0.221 |      -0.293 | -0.005 |  82.976 |
| ARSENKINA G      | ROC    |     166 |       9 |         0.476 |      0.076 |     -0.089 | -0.01  |           0 |            0 |   -1.764 |              2 |               3 |      0.214 |      -0.278 |  0.017 |  78.916 |
| HAMILTON B       | USA    |     170 |       9 |         0.482 |      0.067 |     -0.082 | -0.01  |           0 |            0 |   -1.443 |              0 |               1 |      0.154 |      -0.2   | -0.002 |  71.746 |
| DONG Z           | CHN    |     176 |       9 |         0.511 |      0.091 |     -0.135 | -0.019 |           1 |            2 |   -2.684 |              8 |               8 |      0.575 |      -0.382 |  0.001 |  77.429 |
| KIM Y            | KOR    |      40 |       2 |         0.35  |      0.065 |     -0.096 | -0.039 |           0 |            0 |   -1.065 |              1 |               0 |      0.176 |      -0.157 |  0.01  |  77.564 |

### Leads

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |    net |   big_makes |   big_misses |   worst5 |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|-------:|------------:|-------------:|---------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| LARSEN M     | DEN    |     162 |       9 |         0.543 |      0.041 |     -0.032 |  0.008 |           0 |            0 |   -0.512 |              0 |               0 |      0.129 |      -0.076 |  0.001 |  82.562 |
| KUZMINA E    | ROC    |     166 |       9 |         0.572 |      0.041 |     -0.038 |  0.007 |           0 |            0 |   -0.825 |              0 |               0 |      0.102 |      -0.121 | -0.001 |  86.596 |
| MCEWEN D     | CAN    |     176 |       9 |         0.562 |      0.037 |     -0.035 |  0.005 |           0 |            0 |   -0.628 |              0 |               0 |      0.1   |      -0.126 |  0.004 |  89.347 |
| JIANG X      | CHN    |      58 |       3 |         0.517 |      0.042 |     -0.034 |  0.005 |           0 |            0 |   -0.43  |              0 |               0 |      0.12  |      -0.072 |  0.005 |  85.776 |
| PETERSON TAR | USA    |     170 |       9 |         0.529 |      0.033 |     -0.032 |  0.002 |           0 |            0 |   -0.666 |              0 |               0 |      0.083 |      -0.117 | -0.001 |  86.029 |
| MABERGS S    | SWE    |     210 |      11 |         0.481 |      0.033 |     -0.028 |  0.002 |           0 |            0 |   -0.444 |              0 |               0 |      0.1   |      -0.087 | -0.001 |  89.423 |
| KIM S        | KOR    |     180 |       9 |         0.483 |      0.034 |     -0.033 | -0.001 |           0 |            0 |   -0.682 |              0 |               0 |      0.132 |      -0.103 | -0     |  83.659 |
| ZHANG L      | CHN    |     176 |       9 |         0.494 |      0.048 |     -0.05  | -0.002 |           0 |            0 |   -1.141 |              0 |               1 |      0.174 |      -0.186 | -0.002 |  86.506 |
| DUFF H       | GBR    |     206 |      11 |         0.466 |      0.04  |     -0.04  | -0.002 |           0 |            0 |   -0.746 |              0 |               0 |      0.128 |      -0.113 |  0.001 |  83.859 |
| BARBEZAT M   | SUI    |     224 |      11 |         0.496 |      0.031 |     -0.038 | -0.004 |           0 |            0 |   -0.761 |              0 |               0 |      0.103 |      -0.12  |  0.003 |  84.375 |
| YOSHIDA Y    | JPN    |     208 |      11 |         0.5   |      0.027 |     -0.035 | -0.004 |           0 |            0 |   -0.751 |              0 |               0 |      0.078 |      -0.123 | -0.002 |  91.106 |

