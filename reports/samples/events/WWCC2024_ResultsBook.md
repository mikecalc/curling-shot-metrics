# World Women's Curling Championship (WWCC2024_ResultsBook)

Sydney, NS, Canada, 2024; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Women

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| CAN    |      14 | 13-1     |               81.9 |
| SUI    |      14 | 11-3     |               62.9 |
| ITA    |      15 | 11-4     |               58.2 |
| KOR    |      15 | 12-3     |               56.7 |
| SWE    |      13 | 7-6      |               48.2 |
| TUR    |      12 | 3-9      |               30.8 |
| DEN    |      13 | 6-7      |               28.6 |
| USA    |      12 | 6-6      |               25.9 |
| SCO    |      12 | 5-7      |               19.2 |
| JPN    |      12 | 3-9      |               11.8 |
| NOR    |      12 | 4-8      |               10.8 |
| EST    |      12 | 2-10     |               -4.8 |
| NZL    |      12 | 1-11     |              -15.1 |

### Build or address

How each team played the stones, in rock potential (descriptive, not a ranking): `build` is how much a stone added to the team's own potential and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' potential together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| JPN    |      889 |   0.014 |    -0.012 |          0.76  |                2.416 |                   2.719 |
| EST    |      847 |   0.013 |    -0.042 |          0.78  |                2.306 |                   3.223 |
| ITA    |     1079 |   0.013 |    -0.002 |          0.74  |                2.703 |                   2.72  |
| USA    |      814 |   0.009 |    -0.006 |          0.725 |                3.115 |                   2.384 |
| DEN    |      910 |   0.008 |    -0.003 |          0.737 |                2.934 |                   2.179 |
| NZL    |      759 |   0.001 |    -0.007 |          0.735 |                2.834 |                   2.317 |
| NOR    |      835 |  -0.001 |    -0.003 |          0.725 |                2.211 |                   2.671 |
| TUR    |      911 |  -0.002 |    -0.004 |          0.723 |                2.707 |                   2.422 |
| SCO    |      845 |  -0.005 |     0.004 |          0.701 |                2.415 |                   2.376 |
| SUI    |      930 |  -0.006 |     0.024 |          0.695 |                2.579 |                   2.338 |
| KOR    |     1110 |  -0.01  |     0.017 |          0.686 |                2.383 |                   2.397 |
| CAN    |      982 |  -0.013 |     0.03  |          0.697 |                2.253 |                   2.412 |
| SWE    |      960 |  -0.018 |    -0.005 |          0.697 |                2.074 |                   2.715 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HOMAN R       | CAN    |     247 |      14 |         0.7   |      0.283 |     -0.213 |          32 |            8 |   -3.959 |  0.135 |             45 |              11 |      1.611 |      -0.876 |  0.003 |  88.525 |
| PAETZ A       | SUI    |     234 |      14 |         0.654 |      0.247 |     -0.223 |          18 |           12 |   -4.14  |  0.084 |             24 |              15 |      1.235 |      -0.891 |  0.007 |  89.286 |
| CONSTANTINI S | ITA    |     273 |      15 |         0.645 |      0.288 |     -0.227 |          29 |           13 |   -4.437 |  0.105 |             42 |              23 |      1.559 |      -0.724 |  0.005 |  84.815 |
| HASSELBORG A  | SWE    |     241 |      13 |         0.585 |      0.268 |     -0.212 |          24 |           10 |   -4.78  |  0.069 |             34 |              16 |      0.997 |      -0.757 |  0.012 |  84.362 |
| YILDIZ D      | TUR    |     231 |      12 |         0.567 |      0.278 |     -0.32  |          16 |           23 |   -6.139 |  0.019 |             30 |              31 |      1.101 |      -0.906 |  0.008 |  75.433 |
| GIM E         | KOR    |     280 |      15 |         0.561 |      0.305 |     -0.251 |          28 |           18 |   -4.679 |  0.061 |             42 |              30 |      1.69  |      -0.85  | -0.003 |  80.306 |
| PETERSON TAB  | USA    |     205 |      12 |         0.532 |      0.267 |     -0.337 |          17 |           15 |   -8.641 | -0.016 |             21 |              20 |      0.898 |      -0.715 |  0.007 |  76.617 |
| SKASLIEN K    | NOR    |     207 |      12 |         0.531 |      0.235 |     -0.3   |          13 |           23 |   -5.606 | -0.016 |             18 |              28 |      0.85  |      -0.894 | -0.038 |  75.485 |
| DUPONT M      | DEN    |     230 |      13 |         0.526 |      0.291 |     -0.28  |          17 |           14 |   -7.713 |  0.02  |             24 |              26 |      1.305 |      -0.868 |  0.003 |  73.362 |
| TUVIKE E      | EST    |     216 |      12 |         0.509 |      0.306 |     -0.446 |          15 |           36 |   -9.509 | -0.063 |             25 |              44 |      1.671 |      -1.568 |  0.018 |  66.315 |
| UENO M        | JPN    |     224 |      12 |         0.504 |      0.272 |     -0.324 |          18 |           25 |   -8.206 | -0.023 |             31 |              28 |      0.849 |      -1.196 |  0.009 |  67.568 |
| MORRISON R    | SCO    |     212 |      12 |         0.476 |      0.247 |     -0.349 |          12 |           25 |   -9.346 | -0.065 |             24 |              28 |      0.738 |      -1.197 |  0.014 |  74.517 |
| SMITH J       | NZL    |     178 |      11 |         0.393 |      0.343 |     -0.442 |          19 |           34 |   -9.556 | -0.133 |             19 |              32 |      1.423 |      -1.222 |  0.016 |  63.21  |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| FLEURY T    | CAN    |     248 |      14 |         0.589 |      0.115 |     -0.139 |           2 |            4 |   -3.18  |  0.01  |              9 |              10 |      0.381 |      -0.504 | -0.009 |  85.786 |
| TIRINZONI S | SUI    |     230 |      14 |         0.561 |      0.136 |     -0.131 |           2 |            2 |   -2.256 |  0.019 |             11 |               5 |      0.451 |      -0.375 | -0.011 |  87.118 |
| ROERVIK M   | NOR    |     210 |      12 |         0.543 |      0.122 |     -0.126 |           0 |            2 |   -2.594 |  0.008 |              3 |               5 |      0.262 |      -0.359 | -0.002 |  83.333 |
| KIM M       | KOR    |     280 |      15 |         0.504 |      0.126 |     -0.119 |           3 |            3 |   -2.587 |  0.005 |             11 |               7 |      0.49  |      -0.448 | -0.012 |  82.411 |
| DODDS J     | SCO    |     212 |      12 |         0.495 |      0.123 |     -0.146 |           0 |            5 |   -3.404 | -0.013 |              5 |               9 |      0.393 |      -0.501 |  0.018 |  81.014 |
| THIESSE C   | USA    |     206 |      12 |         0.481 |      0.12  |     -0.139 |           1 |            2 |   -3.049 | -0.014 |              5 |               6 |      0.371 |      -0.445 |  0.002 |  83.617 |
| MCMANUS S   | SWE    |     242 |      13 |         0.479 |      0.124 |     -0.123 |           2 |            1 |   -2.741 | -0.005 |              6 |               9 |      0.42  |      -0.403 | -0.006 |  88.017 |
| MATHIS E    | ITA    |     272 |      15 |         0.471 |      0.125 |     -0.142 |           2 |            6 |   -3.099 | -0.016 |             11 |              19 |      0.539 |      -0.468 | -0.009 |  80.607 |
| HALSE M     | DEN    |     230 |      13 |         0.457 |      0.124 |     -0.117 |           2 |            0 |   -1.964 | -0.007 |              6 |              10 |      0.338 |      -0.453 |  0.008 |  80.217 |
| POLAT O     | TUR    |     232 |      12 |         0.448 |      0.123 |     -0.139 |           1 |            4 |   -2.735 | -0.022 |             10 |               8 |      0.393 |      -0.388 |  0.011 |  77.371 |
| KANAI A     | JPN    |     226 |      12 |         0.434 |      0.122 |     -0.122 |           0 |            1 |   -2.218 | -0.016 |              8 |               8 |      0.399 |      -0.348 | -0     |  75.996 |
| SMITH C     | NZL    |     190 |      12 |         0.426 |      0.12  |     -0.2   |           0 |            7 |   -3.417 | -0.063 |              6 |              12 |      0.368 |      -0.607 |  0.023 |  65.741 |
| LAIDSALU K  | EST    |     216 |      12 |         0.403 |      0.101 |     -0.15  |           1 |            5 |   -3.158 | -0.049 |              3 |              13 |      0.257 |      -0.536 |  0.005 |  77.431 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| THURLOW N        | NZL    |      40 |       3 |         0.525 |      0.074 |     -0.126 |           0 |            0 |   -1.432 | -0.021 |              0 |               1 |      0.064 |      -0.145 |  0.011 |  76.25  |
| KNOCHENHAUER A   | SWE    |     242 |      13 |         0.525 |      0.064 |     -0.091 |           0 |            0 |   -1.894 | -0.01  |              3 |               2 |      0.266 |      -0.272 | -0.015 |  84.917 |
| WITSCHONKE S     | SUI    |     230 |      14 |         0.522 |      0.071 |     -0.081 |           0 |            0 |   -1.674 | -0.002 |              3 |               2 |      0.264 |      -0.239 | -0.008 |  86.848 |
| HASLEV NORDBYE M | NOR    |     210 |      12 |         0.505 |      0.062 |     -0.087 |           0 |            0 |   -1.729 | -0.012 |              1 |               3 |      0.197 |      -0.268 |  0.003 |  86.429 |
| KARAMAN I        | TUR    |      34 |       3 |         0.5   |      0.088 |     -0.153 |           0 |            0 |   -1.495 | -0.032 |              0 |               2 |      0.117 |      -0.246 |  0.013 |  69.853 |
| ROMEI A          | ITA    |     272 |      15 |         0.478 |      0.073 |     -0.077 |           0 |            0 |   -1.466 | -0.006 |              5 |               3 |      0.298 |      -0.249 | -0.003 |  85.24  |
| DUPONT D         | DEN    |     144 |       8 |         0.472 |      0.053 |     -0.076 |           0 |            0 |   -1.57  | -0.015 |              0 |               0 |      0.108 |      -0.188 | -0     |  78.819 |
| KIM S            | KOR    |     264 |      14 |         0.458 |      0.072 |     -0.077 |           0 |            0 |   -1.678 | -0.009 |              0 |               1 |      0.196 |      -0.199 | -0.008 |  84.186 |
| MISKEW E         | CAN    |     248 |      14 |         0.456 |      0.089 |     -0.076 |           0 |            0 |   -1.91  | -0.001 |              3 |               3 |      0.293 |      -0.259 | -0.006 |  87.955 |
| LANDER J         | DEN    |     142 |       8 |         0.451 |      0.08  |     -0.084 |           0 |            0 |   -1.396 | -0.01  |              0 |               1 |      0.149 |      -0.23  |  0.007 |  81.338 |
| PETERSON TAR     | USA    |     206 |      12 |         0.442 |      0.065 |     -0.072 |           0 |            0 |   -1.259 | -0.012 |              1 |               0 |      0.198 |      -0.185 | -0.005 |  86.044 |
| CALIKUSU IS      | TUR    |     198 |      11 |         0.434 |      0.072 |     -0.096 |           0 |            0 |   -2.009 | -0.023 |              1 |               4 |      0.22  |      -0.382 |  0.003 |  74.746 |
| NISHIMURO J      | JPN    |     208 |      11 |         0.423 |      0.068 |     -0.097 |           0 |            1 |   -1.829 | -0.028 |              1 |               3 |      0.163 |      -0.258 | -0.008 |  76.442 |
| TURMANN L        | EST    |     216 |      12 |         0.421 |      0.06  |     -0.095 |           0 |            1 |   -1.899 | -0.03  |              0 |               1 |      0.143 |      -0.24  |  0.005 |  75.463 |
| SINCLAIR S       | SCO    |     212 |      12 |         0.42  |      0.06  |     -0.084 |           0 |            0 |   -1.575 | -0.024 |              1 |               5 |      0.195 |      -0.325 | -0.001 |  80.896 |
| BECKER B         | NZL    |     176 |      11 |         0.409 |      0.082 |     -0.115 |           1 |            2 |   -2.364 | -0.034 |              1 |               3 |      0.171 |      -0.262 |  0.003 |  64.915 |

### Leads

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HOWALD C          | SUI    |     232 |      14 |         0.677 |      0.037 |     -0.038 |           0 |            0 |   -0.762 |  0.013 |              0 |               0 |      0.117 |      -0.132 |  0     |  93.506 |
| SEOL Y            | KOR    |     296 |      15 |         0.662 |      0.036 |     -0.04  |           0 |            0 |   -0.928 |  0.01  |              0 |               0 |      0.125 |      -0.14  | -0.001 |  88.514 |
| LARSEN M          | DEN    |     174 |      10 |         0.632 |      0.032 |     -0.042 |           0 |            0 |   -0.674 |  0.005 |              0 |               0 |      0.079 |      -0.108 | -0.002 |  81.178 |
| ROENNING M        | NOR    |     210 |      12 |         0.624 |      0.034 |     -0.032 |           0 |            0 |   -0.658 |  0.009 |              0 |               0 |      0.087 |      -0.076 |  0.004 |  90.952 |
| ZARDINI LACEDELLI | ITA    |     274 |      15 |         0.617 |      0.039 |     -0.036 |           0 |            0 |   -0.882 |  0.011 |              0 |               0 |      0.097 |      -0.147 |  0.001 |  92.399 |
| MABERGS S         | SWE    |     242 |      13 |         0.616 |      0.036 |     -0.043 |           0 |            0 |   -0.736 |  0.006 |              0 |               0 |      0.131 |      -0.117 | -0.002 |  90.083 |
| HAMILTON B        | USA    |     132 |       8 |         0.606 |      0.035 |     -0.04  |           0 |            0 |   -0.728 |  0.005 |              0 |               0 |      0.067 |      -0.114 |  0.002 |  85.227 |
| GROSSMANN H       | EST    |     216 |      12 |         0.602 |      0.036 |     -0.049 |           0 |            0 |   -1.091 |  0.002 |              0 |               0 |      0.126 |      -0.135 |  0.002 |  83.449 |
| JACKSON S         | SCO    |     212 |      12 |         0.599 |      0.035 |     -0.038 |           0 |            0 |   -0.509 |  0.006 |              1 |               0 |      0.144 |      -0.084 | -0     |  88.561 |
| WILKES S          | CAN    |     246 |      14 |         0.593 |      0.029 |     -0.029 |           0 |            0 |   -0.635 |  0.005 |              0 |               0 |      0.099 |      -0.116 | -0     |  91.667 |
| UENO Y            | JPN    |     226 |      12 |         0.593 |      0.043 |     -0.044 |           0 |            0 |   -0.864 |  0.008 |              0 |               0 |      0.116 |      -0.118 |  0.001 |  88.385 |
| SENGUL B          | TUR    |     232 |      12 |         0.586 |      0.032 |     -0.039 |           0 |            0 |   -0.747 |  0.003 |              0 |               0 |      0.124 |      -0.12  |  0.001 |  84.914 |
| THOMPSON H        | NZL    |     176 |      11 |         0.523 |      0.031 |     -0.049 |           0 |            0 |   -1.081 | -0.007 |              1 |               0 |      0.15  |      -0.169 | -0.005 |  77.983 |
| PERSINGER V       | USA    |      74 |       4 |         0.514 |      0.03  |     -0.048 |           0 |            0 |   -0.766 | -0.008 |              0 |               0 |      0.057 |      -0.098 |  0.002 |  87.162 |

