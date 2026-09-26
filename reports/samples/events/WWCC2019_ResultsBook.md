# World Women's Curling Championship (WWCC2019_ResultsBook)

Silkeborg, Denmark, 2019; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and what its stones did to its chance of winning, so it carries no execution columns.

## Women

### Teams

The team-level view, in win probability: the record, and the summed effect of the team's own stones on its chance of winning, per game, in percentage points (calls and throws together).

| team   |   games | record   |   WP gained / game |
|:-------|--------:|:---------|-------------------:|
| KOR    |      14 | 10-4     |               63.4 |
| SUI    |      15 | 11-4     |               55.2 |
| SWE    |      14 | 12-2     |               49.3 |
| CHN    |      13 | 7-6      |               45.2 |
| RUS    |      13 | 9-4      |               43.8 |
| CAN    |      12 | 6-6      |               36.5 |
| GER    |      12 | 5-7      |               33.8 |
| JPN    |      15 | 7-8      |               26.4 |
| SCO    |      12 | 4-8      |               22.2 |
| DEN    |      12 | 3-9      |               16.8 |
| USA    |      12 | 6-6      |               15.6 |
| LAT    |      12 | 1-11     |                8.9 |
| FIN    |      12 | 3-9      |               -1.8 |

### Build or address

How each team played the stones, in rock potential (descriptive, not a ranking): `build` is how much a stone added to the team's own potential and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' potential together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| LAT    |      903 |   0.019 |    -0.032 |          0.751 |                2.369 |                   2.789 |
| DEN    |      872 |   0.009 |    -0.012 |          0.737 |                2.797 |                   2.514 |
| CAN    |      884 |   0.008 |    -0.01  |          0.726 |                2.356 |                   2.75  |
| JPN    |     1051 |   0.007 |    -0.013 |          0.747 |                2.382 |                   2.797 |
| SUI    |     1128 |   0.005 |    -0.002 |          0.738 |                2.578 |                   2.447 |
| GER    |      875 |   0.005 |    -0.005 |          0.727 |                2.766 |                   2.558 |
| CHN    |      946 |   0.001 |     0.009 |          0.728 |                2.593 |                   2.337 |
| SCO    |      879 |  -0.003 |    -0.003 |          0.724 |                2.06  |                   2.775 |
| FIN    |      853 |  -0.005 |    -0.01  |          0.727 |                2.615 |                   2.781 |
| SWE    |      993 |  -0.007 |     0.021 |          0.69  |                2.399 |                   2.221 |
| USA    |      909 |  -0.01  |    -0.001 |          0.723 |                2.71  |                   2.416 |
| RUS    |      966 |  -0.011 |     0.024 |          0.698 |                2.587 |                   2.07  |
| KOR    |     1072 |  -0.015 |     0.024 |          0.701 |                2.531 |                   2.311 |

### Fourths

| player          | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| HASSELBORG A    | SWE    |     249 |      14 |         0.627 |      0.205 |     -0.3   |          11 |           15 |   -5.755 |  0.016 |             28 |              28 |      1.146 |      -1.038 |  0.007 |  80.408 |
| JENTSCH D       | GER    |     220 |      12 |         0.605 |      0.296 |     -0.27  |          24 |           13 |   -6.395 |  0.073 |             31 |              21 |      1.299 |      -0.742 |  0.012 |  77.294 |
| WANG R          | CHN    |     242 |      13 |         0.603 |      0.265 |     -0.295 |          20 |           17 |   -7.355 |  0.043 |             36 |              26 |      1.18  |      -1.389 |  0.01  |  75.314 |
| KIM M           | KOR    |     269 |      14 |         0.602 |      0.248 |     -0.325 |          15 |           23 |   -7.307 |  0.02  |             42 |              41 |      1.561 |      -1.172 |  0.006 |  75.749 |
| KOVALEVA A      | RUS    |     243 |      13 |         0.584 |      0.248 |     -0.323 |          20 |           22 |   -7.79  |  0.011 |             36 |              30 |      0.946 |      -1.144 |  0.009 |  77.083 |
| KITAZAWA I      | JPN    |     264 |      15 |         0.568 |      0.284 |     -0.349 |          22 |           24 |   -7.478 |  0.011 |             27 |              38 |      1.164 |      -1.35  | -0.002 |  74.81  |
| PAETZ A         | SUI    |     285 |      15 |         0.561 |      0.239 |     -0.242 |          19 |           16 |   -5.08  |  0.028 |             47 |              40 |      1.616 |      -0.941 |  0.001 |  77.419 |
| STASA-SARSUNE I | LAT    |     192 |      10 |         0.542 |      0.236 |     -0.322 |          11 |           15 |   -5.842 | -0.02  |             30 |              34 |      0.772 |      -1.103 |  0.008 |  72.632 |
| DUPONT M        | DEN    |     219 |      12 |         0.534 |      0.257 |     -0.3   |          14 |           18 |   -5.807 | -0.002 |             31 |              30 |      0.831 |      -1.371 |  0.006 |  72.454 |
| GRAY L          | SCO    |      72 |       4 |         0.528 |      0.22  |     -0.298 |           4 |            7 |   -5.087 | -0.025 |              9 |              10 |      1.03  |      -0.674 |  0.005 |  77.113 |
| SINCLAIR J      | USA    |     209 |      11 |         0.522 |      0.333 |     -0.366 |          25 |           23 |   -8.861 | -0.001 |             27 |              33 |      1.21  |      -1.236 |  0.016 |  71.995 |
| CAREY C         | CAN    |     226 |      12 |         0.513 |      0.233 |     -0.236 |          11 |           17 |   -4.838 |  0.005 |             27 |              24 |      0.931 |      -1.044 |  0.001 |  74.437 |
| JACKSON S       | SCO    |     152 |       9 |         0.5   |      0.214 |     -0.334 |           8 |           16 |   -8.462 | -0.06  |             20 |              26 |      0.77  |      -1.075 |  0.011 |  70.638 |
| KAUSTE O        | FIN    |     216 |      12 |         0.495 |      0.279 |     -0.346 |          16 |           27 |   -6.859 | -0.036 |             22 |              35 |      0.838 |      -1.01  | -0.004 |  69.575 |

### Thirds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KIM H        | KOR    |     270 |      14 |         0.585 |      0.134 |     -0.123 |           4 |            4 |   -2.905 |  0.027 |             12 |              17 |      0.516 |      -0.714 |  0.015 |  79.259 |
| MCMANUS S    | SWE    |     250 |      14 |         0.568 |      0.117 |     -0.113 |           1 |            1 |   -2.326 |  0.018 |             10 |               9 |      0.491 |      -0.37  | -0.001 |  86.7   |
| WILKES S     | CAN    |     226 |      12 |         0.562 |      0.137 |     -0.141 |           2 |            3 |   -3.116 |  0.015 |              8 |               8 |      0.493 |      -0.377 | -0.01  |  83.075 |
| BRYZGALOVA A | RUS    |     244 |      13 |         0.553 |      0.118 |     -0.141 |           1 |            3 |   -3.058 |  0.002 |              4 |              13 |      0.303 |      -0.448 | -0.008 |  81.762 |
| TIRINZONI S  | SUI    |     266 |      14 |         0.545 |      0.118 |     -0.105 |           0 |            0 |   -2.025 |  0.017 |             12 |               7 |      0.429 |      -0.323 |  0.01  |  79.623 |
| DUPONT D     | DEN    |     220 |      12 |         0.536 |      0.147 |     -0.132 |           2 |            1 |   -2.237 |  0.018 |             12 |               5 |      0.396 |      -0.556 | -0.003 |  75.114 |
| MEI J        | CHN    |     242 |      13 |         0.525 |      0.112 |     -0.123 |           1 |            3 |   -2.93  |  0     |              7 |              11 |      0.396 |      -0.431 |  0.01  |  82.128 |
| MATSUMURA C  | JPN    |     264 |      15 |         0.519 |      0.114 |     -0.132 |           1 |            2 |   -2.644 | -0.004 |              8 |               6 |      0.48  |      -0.374 |  0.01  |  81.534 |
| JUHASZ E     | FIN    |     216 |      12 |         0.514 |      0.111 |     -0.164 |           0 |            2 |   -2.945 | -0.023 |              6 |               9 |      0.324 |      -0.403 | -0     |  73.032 |
| BLUMBERGA S  | LAT    |     228 |      12 |         0.487 |      0.134 |     -0.194 |           3 |           10 |   -4.277 | -0.035 |              9 |              19 |      0.72  |      -0.605 | -0.005 |  68.142 |
| BROWN N      | SCO    |     224 |      12 |         0.46  |      0.114 |     -0.167 |           1 |            5 |   -4.177 | -0.038 |              7 |              16 |      0.494 |      -0.453 |  0.01  |  78.348 |
| ABBES E      | GER    |     220 |      12 |         0.45  |      0.14  |     -0.185 |           3 |            8 |   -3.297 | -0.039 |              7 |              20 |      0.424 |      -0.574 |  0.013 |  72.045 |
| ANDERSON S   | USA    |     230 |      12 |         0.439 |      0.135 |     -0.155 |           1 |            5 |   -3.3   | -0.028 |              9 |              14 |      0.356 |      -0.399 | -0.002 |  71.304 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| ARSENKINA G      | RUS    |     244 |      13 |         0.582 |      0.061 |     -0.065 |           0 |            0 |   -1.098 |  0.008 |              1 |               0 |      0.194 |      -0.182 |  0.007 |  86.214 |
| NAKAJIMA S       | JPN    |     264 |      15 |         0.545 |      0.069 |     -0.084 |           0 |            0 |   -1.726 | -0.001 |              2 |               2 |      0.225 |      -0.25  |  0.006 |  80.133 |
| KNOCHENHAUER A   | SWE    |     250 |      14 |         0.544 |      0.067 |     -0.063 |           0 |            0 |   -1.334 |  0.007 |              1 |               3 |      0.2   |      -0.238 | -0.004 |  87.048 |
| FERGUSON D       | CAN    |     220 |      12 |         0.532 |      0.074 |     -0.073 |           0 |            0 |   -1.443 |  0.005 |              1 |               1 |      0.267 |      -0.175 | -0.004 |  82.078 |
| YAO M            | CHN    |     242 |      13 |         0.529 |      0.069 |     -0.071 |           0 |            0 |   -1.494 |  0.003 |              0 |               2 |      0.17  |      -0.284 |  0.006 |  78.306 |
| NEUENSCHWANDER E | SUI    |     286 |      15 |         0.524 |      0.071 |     -0.081 |           1 |            0 |   -1.622 | -0.001 |              1 |               3 |      0.232 |      -0.316 |  0.002 |  81.579 |
| YANG T           | KOR    |     270 |      14 |         0.522 |      0.067 |     -0.081 |           0 |            0 |   -1.515 | -0.004 |              2 |               3 |      0.237 |      -0.251 |  0.01  |  75.833 |
| SMITH M          | SCO    |     224 |      12 |         0.5   |      0.076 |     -0.087 |           0 |            0 |   -1.612 | -0.005 |              1 |               2 |      0.232 |      -0.244 |  0.003 |  78.906 |
| ANDERSON T       | USA    |     230 |      12 |         0.5   |      0.054 |     -0.087 |           0 |            1 |   -2.125 | -0.017 |              1 |               3 |      0.189 |      -0.274 |  0.001 |  76.522 |
| FOMM KH          | GER    |     180 |      10 |         0.472 |      0.068 |     -0.109 |           0 |            0 |   -1.789 | -0.026 |              0 |               2 |      0.163 |      -0.236 |  0.004 |  70.833 |
| KRUSTA I         | LAT    |     228 |      12 |         0.465 |      0.072 |     -0.088 |           0 |            0 |   -1.872 | -0.014 |              2 |               3 |      0.239 |      -0.284 |  0.008 |  74.67  |
| HOEGH J          | DEN    |     220 |      12 |         0.45  |      0.058 |     -0.083 |           0 |            0 |   -1.559 | -0.019 |              1 |               0 |      0.198 |      -0.195 | -0.005 |  75.227 |
| SALMIOVIRTA M    | FIN    |     216 |      12 |         0.44  |      0.069 |     -0.092 |           1 |            0 |   -1.619 | -0.021 |              1 |               1 |      0.19  |      -0.243 | -0     |  69.097 |
| HOEHNE M         | GER    |      50 |       3 |         0.4   |      0.074 |     -0.134 |           0 |            0 |   -1.565 | -0.051 |              0 |               0 |      0.117 |      -0.18  |  0.006 |  61     |

### Leads

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KUZMINA E   | RUS    |     204 |      11 |         0.657 |      0.032 |     -0.042 |           0 |            0 |   -0.801 |  0.007 |              0 |               0 |      0.082 |      -0.167 |  0.003 |  83.911 |
| ISHIGOOKA H | JPN    |     264 |      15 |         0.61  |      0.03  |     -0.037 |           0 |            0 |   -0.883 |  0.004 |              0 |               0 |      0.129 |      -0.134 |  0.003 |  81.534 |
| MABERGS S   | SWE    |     250 |      14 |         0.608 |      0.037 |     -0.032 |           0 |            0 |   -0.679 |  0.01  |              0 |               0 |      0.118 |      -0.1   |  0     |  86.8   |
| KIM S       | KOR    |     270 |      14 |         0.607 |      0.031 |     -0.031 |           0 |            0 |   -0.584 |  0.007 |              0 |               0 |      0.118 |      -0.098 | -0.002 |  81.296 |
| VASILEVA U  | RUS    |      40 |       2 |         0.6   |      0.029 |     -0.038 |           0 |            0 |   -0.392 |  0.002 |              0 |               0 |      0.058 |      -0.058 |  0.009 |  86.25  |
| JENTSCH A   | GER    |     210 |      12 |         0.6   |      0.033 |     -0.051 |           0 |            0 |   -0.809 | -0.001 |              0 |               0 |      0.105 |      -0.112 | -0.001 |  75.957 |
| SINCLAIR S  | SCO    |     224 |      12 |         0.594 |      0.035 |     -0.034 |           0 |            0 |   -0.653 |  0.007 |              0 |               0 |      0.122 |      -0.088 | -0.004 |  85.268 |
| KNUDSEN L   | DEN    |     220 |      12 |         0.582 |      0.036 |     -0.034 |           0 |            0 |   -0.672 |  0.007 |              0 |               0 |      0.124 |      -0.102 | -0.002 |  83.182 |
| WALKER M    | USA    |     230 |      12 |         0.565 |      0.028 |     -0.044 |           0 |            0 |   -0.835 | -0.003 |              0 |               0 |      0.124 |      -0.122 | -0.004 |  84.348 |
| BARBEZAT M  | SUI    |     286 |      15 |         0.563 |      0.03  |     -0.036 |           0 |            0 |   -1.134 |  0.001 |              0 |               1 |      0.113 |      -0.189 |  0.001 |  86.14  |
| BARONE E    | LAT    |     228 |      12 |         0.561 |      0.031 |     -0.049 |           0 |            0 |   -0.99  | -0.004 |              0 |               1 |      0.116 |      -0.199 |  0     |  78.399 |
| BROWN R     | CAN    |     226 |      12 |         0.54  |      0.033 |     -0.037 |           0 |            0 |   -0.862 |  0.001 |              0 |               0 |      0.123 |      -0.143 | -0.004 |  83     |
| MA J        | CHN    |     242 |      13 |         0.521 |      0.027 |     -0.033 |           0 |            0 |   -0.719 | -0.002 |              0 |               0 |      0.084 |      -0.112 | -0.002 |  85.021 |
| IMMONEN L   | FIN    |     216 |      12 |         0.514 |      0.033 |     -0.04  |           0 |            0 |   -0.853 | -0.003 |              0 |               0 |      0.111 |      -0.105 | -0.004 |  80.465 |
| SILINA T    | LAT    |      36 |       2 |         0.444 |      0.038 |     -0.052 |           0 |            0 |   -0.647 | -0.012 |              0 |               0 |      0.051 |      -0.079 | -0.002 |  65.278 |

