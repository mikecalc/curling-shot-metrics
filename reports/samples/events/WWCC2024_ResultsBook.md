# World Women's Curling Championship (WWCC2024_ResultsBook)

Sydney, NS, Canada, 2024; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Women

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| CAN    |      14 | 13-1     |               76.6 |
| SUI    |      14 | 11-3     |               62.6 |
| ITA    |      15 | 11-4     |               60.8 |
| KOR    |      15 | 12-3     |               55   |
| SWE    |      13 | 7-6      |               52.1 |
| USA    |      12 | 6-6      |               28.1 |
| DEN    |      13 | 6-7      |               27.3 |
| TUR    |      12 | 3-9      |               23   |
| SCO    |      12 | 5-7      |               15.4 |
| JPN    |      12 | 3-9      |               15   |
| NOR    |      12 | 4-8      |                7.5 |
| EST    |      12 | 2-10     |              -12.7 |
| NZL    |      12 | 1-11     |              -16.3 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| EST    |      847 |   0.016 |    -0.069 |          0.718 |                1.945 |                   2.419 |
| ITA    |     1079 |   0.015 |    -0.008 |          0.63  |                2.171 |                   2.111 |
| JPN    |      889 |   0.011 |    -0.008 |          0.623 |                2.088 |                   2.217 |
| CAN    |      982 |   0.01  |     0.025 |          0.579 |                2.049 |                   2.009 |
| SCO    |      845 |   0.004 |    -0.01  |          0.622 |                1.961 |                   2.02  |
| NOR    |      835 |   0.003 |    -0.014 |          0.635 |                1.911 |                   2.216 |
| DEN    |      910 |  -0.005 |     0.011 |          0.571 |                2.264 |                   1.842 |
| NZL    |      759 |  -0.006 |    -0.03  |          0.588 |                2.116 |                   2.116 |
| SUI    |      930 |  -0.007 |     0.038 |          0.543 |                2.233 |                   1.822 |
| SWE    |      960 |  -0.009 |    -0.002 |          0.566 |                1.832 |                   2.108 |
| KOR    |     1110 |  -0.01  |     0.028 |          0.558 |                2.024 |                   2.019 |
| USA    |      814 |  -0.011 |     0.004 |          0.566 |                2.312 |                   2.012 |
| TUR    |      911 |  -0.011 |     0.016 |          0.578 |                2.046 |                   2.118 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| CONSTANTINI S | ITA    |     273 |      15 |         0.652 |      0.292 |     -0.235 |          29 |           15 |   -4.305 |  0.108 |             42 |              25 |      1.657 |      -0.637 | -0     |  84.815 |
| HOMAN R       | CAN    |     247 |      14 |         0.644 |      0.293 |     -0.185 |          29 |            8 |   -4.115 |  0.123 |             46 |              12 |      1.694 |      -0.981 | -0.001 |  88.525 |
| PAETZ A       | SUI    |     234 |      14 |         0.62  |      0.25  |     -0.194 |          17 |           12 |   -4.072 |  0.081 |             23 |              16 |      1.299 |      -0.972 |  0.002 |  89.286 |
| GIM E         | KOR    |     280 |      15 |         0.554 |      0.302 |     -0.251 |          28 |           19 |   -4.806 |  0.055 |             40 |              32 |      1.822 |      -0.874 | -0.003 |  80.306 |
| HASSELBORG A  | SWE    |     241 |      13 |         0.552 |      0.272 |     -0.204 |          25 |           10 |   -5.12  |  0.059 |             31 |              16 |      0.961 |      -0.705 |  0.008 |  84.362 |
| YILDIZ D      | TUR    |     231 |      12 |         0.541 |      0.289 |     -0.316 |          22 |           24 |   -6.169 |  0.012 |             32 |              33 |      1.084 |      -1.001 | -0.004 |  75.433 |
| DUPONT M      | DEN    |     230 |      13 |         0.535 |      0.272 |     -0.285 |          17 |           20 |   -7.039 |  0.013 |             27 |              25 |      1.376 |      -0.857 |  0.011 |  73.362 |
| SKASLIEN K    | NOR    |     207 |      12 |         0.517 |      0.231 |     -0.312 |          16 |           23 |   -5.713 | -0.031 |             16 |              25 |      0.795 |      -0.911 | -0.027 |  75.485 |
| TUVIKE E      | EST    |     216 |      12 |         0.491 |      0.309 |     -0.432 |          18 |           35 |   -9.709 | -0.069 |             27 |              51 |      1.537 |      -1.603 |  0.015 |  66.315 |
| PETERSON TAB  | USA    |     205 |      12 |         0.478 |      0.298 |     -0.322 |          18 |           18 |   -8.688 | -0.026 |             20 |              20 |      0.928 |      -0.704 |  0.014 |  76.617 |
| UENO M        | JPN    |     224 |      12 |         0.478 |      0.258 |     -0.302 |          16 |           25 |   -7.677 | -0.034 |             25 |              32 |      0.875 |      -1.184 |  0.008 |  67.568 |
| MORRISON R    | SCO    |     212 |      12 |         0.453 |      0.248 |     -0.341 |          14 |           23 |   -8.71  | -0.074 |             21 |              40 |      0.689 |      -1.082 |  0.014 |  74.517 |
| SMITH J       | NZL    |     178 |      11 |         0.41  |      0.316 |     -0.465 |          14 |           37 |   -9.176 | -0.145 |             16 |              36 |      1.39  |      -1.335 |  0.022 |  63.21  |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| FLEURY T    | CAN    |     248 |      14 |         0.565 |      0.143 |     -0.137 |           5 |            4 |   -3.667 |  0.021 |             10 |               9 |      0.486 |      -0.57  | -0.015 |  85.786 |
| TIRINZONI S | SUI    |     230 |      14 |         0.552 |      0.164 |     -0.117 |           3 |            0 |   -1.919 |  0.038 |             10 |               3 |      0.44  |      -0.276 | -0.012 |  87.118 |
| HALSE M     | DEN    |     230 |      13 |         0.526 |      0.128 |     -0.147 |           2 |            1 |   -2.417 | -0.002 |              3 |              12 |      0.344 |      -0.4   |  0.002 |  80.217 |
| ROERVIK M   | NOR    |     210 |      12 |         0.519 |      0.137 |     -0.131 |           3 |            5 |   -3.04  |  0.008 |              3 |               6 |      0.33  |      -0.443 | -0.006 |  83.333 |
| MCMANUS S   | SWE    |     242 |      13 |         0.512 |      0.144 |     -0.139 |           3 |            3 |   -2.764 |  0.006 |             12 |              11 |      0.474 |      -0.36  | -0.005 |  88.017 |
| KIM M       | KOR    |     280 |      15 |         0.496 |      0.131 |     -0.13  |           4 |            4 |   -2.826 | -0     |              9 |               9 |      0.45  |      -0.553 | -0.013 |  82.411 |
| DODDS J     | SCO    |     212 |      12 |         0.495 |      0.133 |     -0.153 |           0 |            4 |   -3.217 | -0.011 |              4 |              13 |      0.351 |      -0.482 |  0.015 |  81.014 |
| KANAI A     | JPN    |     226 |      12 |         0.491 |      0.135 |     -0.15  |           4 |            3 |   -2.694 | -0.01  |             10 |              11 |      0.418 |      -0.443 |  0.006 |  75.996 |
| POLAT O     | TUR    |     232 |      12 |         0.478 |      0.125 |     -0.145 |           2 |            3 |   -3.079 | -0.016 |             11 |               8 |      0.418 |      -0.462 |  0.007 |  77.371 |
| THIESSE C   | USA    |     206 |      12 |         0.476 |      0.134 |     -0.128 |           1 |            3 |   -3.32  | -0.003 |              4 |               5 |      0.319 |      -0.5   |  0.007 |  83.617 |
| MATHIS E    | ITA    |     272 |      15 |         0.471 |      0.146 |     -0.143 |           5 |            6 |   -3.691 | -0.007 |             11 |              20 |      0.691 |      -0.511 | -0.005 |  80.607 |
| LAIDSALU K  | EST    |     216 |      12 |         0.417 |      0.118 |     -0.167 |           1 |            7 |   -3.01  | -0.048 |              3 |              15 |      0.33  |      -0.545 |  0.009 |  77.431 |
| SMITH C     | NZL    |     190 |      12 |         0.4   |      0.134 |     -0.186 |           0 |            8 |   -3.208 | -0.058 |              3 |              12 |      0.408 |      -0.585 |  0.028 |  65.741 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HASLEV NORDBYE M | NOR    |     210 |      12 |         0.543 |      0.09  |     -0.092 |           0 |            1 |   -2.197 |  0.007 |              1 |               3 |      0.215 |      -0.294 |  0.004 |  86.429 |
| WITSCHONKE S     | SUI    |     230 |      14 |         0.535 |      0.089 |     -0.086 |           0 |            0 |   -1.955 |  0.008 |              2 |               1 |      0.248 |      -0.24  | -0.007 |  86.848 |
| KNOCHENHAUER A   | SWE    |     242 |      13 |         0.521 |      0.092 |     -0.094 |           0 |            0 |   -1.763 |  0.003 |              6 |               3 |      0.428 |      -0.254 | -0.009 |  84.917 |
| MISKEW E         | CAN    |     248 |      14 |         0.52  |      0.089 |     -0.073 |           0 |            0 |   -1.463 |  0.011 |              4 |               1 |      0.354 |      -0.215 | -0.006 |  87.955 |
| ROMEI A          | ITA    |     272 |      15 |         0.504 |      0.079 |     -0.072 |           1 |            0 |   -1.449 |  0.004 |              8 |               2 |      0.392 |      -0.227 |  0.002 |  85.24  |
| THURLOW N        | NZL    |      40 |       3 |         0.5   |      0.102 |     -0.16  |           0 |            1 |   -1.869 | -0.029 |              0 |               1 |      0.074 |      -0.146 |  0.02  |  76.25  |
| LANDER J         | DEN    |     142 |       8 |         0.472 |      0.085 |     -0.096 |           0 |            0 |   -1.742 | -0.01  |              1 |               3 |      0.218 |      -0.269 |  0.008 |  81.338 |
| KIM S            | KOR    |     264 |      14 |         0.47  |      0.081 |     -0.072 |           0 |            0 |   -1.497 |  0     |              1 |               1 |      0.227 |      -0.19  | -0.005 |  84.186 |
| NISHIMURO J      | JPN    |     208 |      11 |         0.462 |      0.073 |     -0.092 |           0 |            0 |   -1.959 | -0.016 |              1 |               6 |      0.225 |      -0.381 |  0     |  76.442 |
| PETERSON TAR     | USA    |     206 |      12 |         0.451 |      0.085 |     -0.081 |           0 |            0 |   -1.422 | -0.006 |              0 |               0 |      0.184 |      -0.197 | -0.002 |  86.044 |
| SINCLAIR S       | SCO    |     212 |      12 |         0.425 |      0.07  |     -0.092 |           0 |            1 |   -1.76  | -0.023 |              1 |               5 |      0.219 |      -0.312 |  0.002 |  80.896 |
| BECKER B         | NZL    |     176 |      11 |         0.42  |      0.104 |     -0.134 |           1 |            3 |   -2.632 | -0.034 |              1 |               4 |      0.232 |      -0.327 |  0.01  |  64.915 |
| TURMANN L        | EST    |     216 |      12 |         0.417 |      0.068 |     -0.113 |           0 |            4 |   -2.839 | -0.037 |              0 |               2 |      0.166 |      -0.253 |  0.01  |  75.463 |
| KARAMAN I        | TUR    |      34 |       3 |         0.412 |      0.111 |     -0.125 |           0 |            1 |   -1.676 | -0.028 |              1 |               2 |      0.134 |      -0.249 |  0.003 |  69.853 |
| DUPONT D         | DEN    |     144 |       8 |         0.403 |      0.061 |     -0.075 |           0 |            1 |   -1.887 | -0.02  |              0 |               1 |      0.124 |      -0.191 |  0.001 |  78.819 |
| CALIKUSU IS      | TUR    |     198 |      11 |         0.343 |      0.09  |     -0.093 |           0 |            0 |   -1.908 | -0.03  |              1 |               4 |      0.23  |      -0.354 |  0.003 |  74.746 |

### Leads

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HOWALD C          | SUI    |     232 |      14 |         0.616 |      0.04  |     -0.035 |           0 |            0 |   -0.802 |  0.011 |              0 |               0 |      0.116 |      -0.111 |  0.001 |  93.506 |
| ZARDINI LACEDELLI | ITA    |     274 |      15 |         0.588 |      0.038 |     -0.037 |           0 |            0 |   -0.842 |  0.007 |              0 |               0 |      0.145 |      -0.137 |  0.002 |  92.399 |
| THOMPSON H        | NZL    |     176 |      11 |         0.585 |      0.031 |     -0.056 |           0 |            0 |   -0.974 | -0.005 |              1 |               0 |      0.15  |      -0.134 | -0.002 |  77.983 |
| SEOL Y            | KOR    |     296 |      15 |         0.561 |      0.038 |     -0.036 |           0 |            0 |   -0.816 |  0.005 |              0 |               0 |      0.115 |      -0.136 | -0     |  88.514 |
| JACKSON S         | SCO    |     212 |      12 |         0.557 |      0.038 |     -0.045 |           0 |            0 |   -0.731 |  0.001 |              1 |               0 |      0.173 |      -0.117 |  0.001 |  88.561 |
| PERSINGER V       | USA    |      74 |       4 |         0.554 |      0.034 |     -0.04  |           0 |            0 |   -0.651 |  0.001 |              0 |               0 |      0.05  |      -0.091 |  0.001 |  87.162 |
| WILKES S          | CAN    |     246 |      14 |         0.545 |      0.034 |     -0.035 |           0 |            0 |   -0.692 |  0.003 |              1 |               0 |      0.148 |      -0.118 | -0.001 |  91.667 |
| GROSSMANN H       | EST    |     216 |      12 |         0.542 |      0.037 |     -0.045 |           0 |            0 |   -1.004 | -0.001 |              0 |               0 |      0.137 |      -0.106 |  0.002 |  83.449 |
| ROENNING M        | NOR    |     210 |      12 |         0.533 |      0.04  |     -0.035 |           0 |            0 |   -0.829 |  0.005 |              0 |               0 |      0.075 |      -0.107 |  0.001 |  90.952 |
| UENO Y            | JPN    |     226 |      12 |         0.522 |      0.045 |     -0.044 |           1 |            0 |   -1.092 |  0.002 |              0 |               0 |      0.09  |      -0.106 |  0.003 |  88.385 |
| MABERGS S         | SWE    |     242 |      13 |         0.521 |      0.041 |     -0.04  |           0 |            0 |   -0.738 |  0.002 |              0 |               0 |      0.102 |      -0.132 | -0     |  90.083 |
| LARSEN M          | DEN    |     174 |      10 |         0.517 |      0.033 |     -0.049 |           0 |            0 |   -0.712 | -0.006 |              0 |               0 |      0.085 |      -0.116 | -0.002 |  81.178 |
| HAMILTON B        | USA    |     132 |       8 |         0.515 |      0.036 |     -0.044 |           0 |            0 |   -0.786 | -0.003 |              0 |               0 |      0.064 |      -0.099 |  0.002 |  85.227 |
| SENGUL B          | TUR    |     232 |      12 |         0.44  |      0.038 |     -0.038 |           0 |            0 |   -0.757 | -0.005 |              0 |               0 |      0.13  |      -0.126 |  0.001 |  84.914 |

