# World Women's Curling Championship (WWCC2019_ResultsBook)

Silkeborg, Denmark, 2019; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| SWE    |      14 | 12-2     |  35.7 |   6.5 |  16.6 |      12.5 |     0.1 |      67.6 |
| SUI    |      15 | 11-4     |  23.3 |  -2.3 |  19.8 |       4.4 |     1.5 |      52.9 |
| KOR    |      14 | 10-4     |  21.4 |  -1.6 |  25.9 |      -4.2 |     1.3 |      53.4 |
| RUS    |      13 | 9-4      |  19.2 |   4.4 |  12.7 |       4.1 |    -2   |      59.2 |
| CHN    |      13 | 7-6      |   3.8 |  -2.6 |  16.4 |      -9.1 |    -0.8 |      56.6 |
| CAN    |      12 | 6-6      |   0   |   0   |   5.3 |      -2.2 |    -3   |      55.5 |
| USA    |      12 | 6-6      |   0   |  -1.9 | -20.5 |      17.8 |     4.6 |      45.5 |
| JPN    |      15 | 7-8      |  -3.3 |   2.3 |   0.1 |      -7   |     1.2 |      52.3 |
| GER    |      12 | 5-7      |  -8.3 |  -3.8 |   7.9 |     -13.6 |     1.2 |      44.5 |
| SCO    |      12 | 4-8      | -16.7 |   5.7 | -15.8 |      -2   |    -4.6 |      43.4 |
| FIN    |      12 | 3-9      | -25   |  -1.9 | -41   |      16.8 |     1.1 |      38.9 |
| DEN    |      12 | 3-9      | -25   |  -3.8 | -13.5 |      -6.3 |    -1.4 |      35.8 |
| LAT    |      12 | 1-11     | -41.7 |  -1.9 | -28.3 |     -11.5 |     0   |      38.1 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| JPN    |     1065 |   0.014 |    -0.016 |          0.649 |                1.945 |                   2.196 |
| SUI    |     1128 |   0.011 |     0.002 |          0.601 |                2.094 |                   1.923 |
| CAN    |      912 |   0.009 |    -0.01  |          0.64  |                1.973 |                   2.065 |
| LAT    |      910 |   0.008 |    -0.01  |          0.605 |                1.934 |                   2.253 |
| SCO    |      893 |   0.006 |    -0.013 |          0.625 |                1.78  |                   2.151 |
| CHN    |      969 |   0.005 |     0.006 |          0.595 |                2.133 |                   1.911 |
| RUS    |      980 |  -0.001 |     0.009 |          0.602 |                2.174 |                   1.812 |
| SWE    |     1022 |  -0.007 |     0.017 |          0.577 |                2.088 |                   1.865 |
| KOR    |     1072 |  -0.008 |     0.026 |          0.549 |                2.066 |                   1.876 |
| FIN    |      860 |  -0.008 |    -0.02  |          0.626 |                2.069 |                   2.317 |
| GER    |      881 |  -0.01  |     0.004 |          0.589 |                2.105 |                   2.07  |
| USA    |      916 |  -0.011 |    -0.005 |          0.585 |                1.99  |                   2.031 |
| DEN    |      879 |  -0.013 |     0.002 |          0.592 |                2.063 |                   2.044 |

### Fourths

| player          | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KIM M           | KOR    |     269 |      14 |         0.606 |      0.239 |     -0.318 |          14 |           21 |   -6.889 |  0.019 |             37 |              40 |      1.458 |      -1.067 | -0.003 |  75.749 |
| KOVALEVA A      | RUS    |     245 |      13 |         0.604 |      0.239 |     -0.333 |          18 |           20 |   -6.872 |  0.013 |             38 |              34 |      1.077 |      -1.17  |  0.012 |  77.169 |
| WANG R          | CHN    |     247 |      13 |         0.595 |      0.267 |     -0.3   |          20 |           19 |   -7.375 |  0.037 |             34 |              23 |      1.287 |      -1.507 |  0.009 |  75     |
| HASSELBORG A    | SWE    |     254 |      14 |         0.571 |      0.204 |     -0.265 |          14 |           18 |   -6.044 |  0.003 |             23 |              26 |      1.093 |      -1.093 |  0.006 |  80.6   |
| PAETZ A         | SUI    |     285 |      15 |         0.558 |      0.224 |     -0.254 |          15 |           17 |   -5.063 |  0.013 |             42 |              40 |      1.597 |      -0.829 |  0.003 |  77.419 |
| JENTSCH D       | GER    |     221 |      12 |         0.552 |      0.304 |     -0.223 |          21 |           12 |   -5.599 |  0.068 |             33 |              18 |      1.284 |      -0.67  |  0.015 |  77.283 |
| KITAZAWA I      | JPN    |     266 |      15 |         0.549 |      0.293 |     -0.33  |          25 |           27 |   -7.384 |  0.012 |             28 |              39 |      1.041 |      -1.355 | -0.003 |  75     |
| CAREY C         | CAN    |     231 |      12 |         0.545 |      0.226 |     -0.253 |          14 |           19 |   -5.016 |  0.008 |             27 |              24 |      0.944 |      -0.857 | -0.002 |  74.78  |
| GRAY L          | SCO    |      74 |       4 |         0.541 |      0.233 |     -0.311 |           8 |            7 |   -4.629 | -0.017 |             10 |              12 |      0.908 |      -0.699 | -0.004 |  77.397 |
| STASA-SARSUNE I | LAT    |     192 |      10 |         0.516 |      0.241 |     -0.29  |          12 |           17 |   -5.961 | -0.016 |             30 |              33 |      0.806 |      -1.109 | -0.006 |  72.632 |
| DUPONT M        | DEN    |     220 |      12 |         0.509 |      0.266 |     -0.301 |          14 |           21 |   -5.668 | -0.012 |             26 |              34 |      1.013 |      -1.389 |  0.013 |  72.12  |
| KAUSTE O        | FIN    |     217 |      12 |         0.498 |      0.275 |     -0.361 |          17 |           31 |   -7.268 | -0.044 |             23 |              36 |      0.901 |      -1.175 |  0.001 |  69.484 |
| SINCLAIR J      | USA    |     211 |      11 |         0.474 |      0.334 |     -0.327 |          19 |           25 |   -9.087 | -0.014 |             27 |              35 |      1.182 |      -1.292 |  0.009 |  72.262 |
| JACKSON S       | SCO    |     153 |       9 |         0.464 |      0.243 |     -0.324 |           9 |           19 |   -8.474 | -0.061 |             22 |              28 |      0.856 |      -1.081 |  0.01  |  70.167 |

### Thirds

| player       | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| KIM H        | KOR    |     270 |      14 |         0.63  |      0.135 |     -0.129 |           6 |            4 |   -2.971 |  0.037 |             20 |              16 |      0.546 |      -0.752 |  0.009 |  79.259 |
| TIRINZONI S  | SUI    |     266 |      14 |         0.602 |      0.129 |     -0.107 |           4 |            1 |   -2.294 |  0.035 |             16 |               9 |      0.581 |      -0.413 |  0.004 |  79.623 |
| MCMANUS S    | SWE    |     258 |      14 |         0.597 |      0.124 |     -0.143 |           2 |            5 |   -2.962 |  0.017 |              7 |              10 |      0.575 |      -0.511 | -0.001 |  86.24  |
| MEI J        | CHN    |     248 |      13 |         0.585 |      0.139 |     -0.135 |           6 |            4 |   -2.92  |  0.025 |             10 |               8 |      0.468 |      -0.448 |  0.004 |  82.359 |
| MATSUMURA C  | JPN    |     268 |      15 |         0.575 |      0.141 |     -0.15  |           4 |            5 |   -3.281 |  0.017 |             14 |               8 |      0.645 |      -0.436 |  0.006 |  81.716 |
| BRYZGALOVA A | RUS    |     248 |      13 |         0.573 |      0.119 |     -0.148 |           2 |            4 |   -2.847 |  0.005 |              7 |              12 |      0.404 |      -0.439 | -0.012 |  81.653 |
| WILKES S     | CAN    |     234 |      12 |         0.543 |      0.145 |     -0.146 |           4 |            4 |   -3.111 |  0.012 |             13 |              11 |      0.529 |      -0.434 | -0.005 |  82.692 |
| DUPONT D     | DEN    |     222 |      12 |         0.523 |      0.144 |     -0.13  |           1 |            2 |   -2.745 |  0.013 |             12 |               7 |      0.381 |      -0.499 |  0.004 |  75.226 |
| JUHASZ E     | FIN    |     218 |      12 |         0.495 |      0.126 |     -0.162 |           2 |            4 |   -2.892 | -0.019 |              6 |              12 |      0.399 |      -0.512 | -0.004 |  72.706 |
| ANDERSON S   | USA    |     232 |      12 |         0.491 |      0.131 |     -0.164 |           2 |            3 |   -2.725 | -0.019 |              9 |              13 |      0.376 |      -0.351 |  0.002 |  71.552 |
| ABBES E      | GER    |     222 |      12 |         0.491 |      0.16  |     -0.198 |           4 |           10 |   -3.321 | -0.022 |              9 |              19 |      0.487 |      -0.614 |  0.011 |  72.072 |
| BLUMBERGA S  | LAT    |     229 |      12 |         0.485 |      0.148 |     -0.199 |           5 |            9 |   -5.103 | -0.03  |             12 |              22 |      0.746 |      -0.677 | -0.009 |  67.841 |
| BROWN N      | SCO    |     227 |      12 |         0.441 |      0.125 |     -0.172 |           2 |            7 |   -4.232 | -0.041 |             11 |              20 |      0.567 |      -0.515 |  0.008 |  78.194 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| ARSENKINA G      | RUS    |     248 |      13 |         0.573 |      0.08  |     -0.069 |           0 |            1 |   -1.564 |  0.016 |              3 |               0 |      0.301 |      -0.208 | -0     |  85.931 |
| KNOCHENHAUER A   | SWE    |     258 |      14 |         0.55  |      0.074 |     -0.075 |           0 |            1 |   -1.658 |  0.007 |              2 |               1 |      0.27  |      -0.221 | -0.004 |  87.012 |
| YAO M            | CHN    |     248 |      13 |         0.532 |      0.086 |     -0.079 |           0 |            1 |   -1.529 |  0.009 |              2 |               1 |      0.253 |      -0.208 |  0.001 |  78.125 |
| NEUENSCHWANDER E | SUI    |     286 |      15 |         0.517 |      0.08  |     -0.084 |           1 |            0 |   -1.801 |  0.001 |              2 |               4 |      0.318 |      -0.324 |  0.001 |  81.579 |
| NAKAJIMA S       | JPN    |     268 |      15 |         0.515 |      0.085 |     -0.075 |           0 |            0 |   -1.375 |  0.007 |              2 |               1 |      0.306 |      -0.237 |  0.005 |  80.431 |
| YANG T           | KOR    |     270 |      14 |         0.5   |      0.08  |     -0.083 |           0 |            1 |   -1.702 | -0.001 |              1 |               7 |      0.25  |      -0.371 |  0.008 |  75.833 |
| ANDERSON T       | USA    |     232 |      12 |         0.487 |      0.06  |     -0.088 |           0 |            1 |   -2.103 | -0.016 |              2 |               3 |      0.24  |      -0.315 |  0.001 |  76.724 |
| FOMM KH          | GER    |     182 |      10 |         0.462 |      0.082 |     -0.105 |           0 |            0 |   -2.044 | -0.018 |              3 |               2 |      0.236 |      -0.256 |  0.004 |  71.016 |
| FERGUSON D       | CAN    |     226 |      12 |         0.456 |      0.094 |     -0.072 |           0 |            0 |   -1.943 |  0.004 |              6 |               3 |      0.325 |      -0.282 | -0.007 |  82.444 |
| KRUSTA I         | LAT    |     230 |      12 |         0.448 |      0.082 |     -0.082 |           0 |            1 |   -1.797 | -0.008 |              3 |               2 |      0.264 |      -0.257 |  0.007 |  74.672 |
| SMITH M          | SCO    |     228 |      12 |         0.447 |      0.075 |     -0.09  |           0 |            1 |   -1.827 | -0.016 |              1 |               3 |      0.234 |      -0.247 |  0.004 |  78.728 |
| HOEGH J          | DEN    |     222 |      12 |         0.446 |      0.065 |     -0.087 |           0 |            0 |   -1.754 | -0.019 |              0 |               2 |      0.164 |      -0.225 | -0.001 |  75.225 |
| SALMIOVIRTA M    | FIN    |     218 |      12 |         0.399 |      0.082 |     -0.107 |           1 |            2 |   -2.247 | -0.032 |              1 |               3 |      0.181 |      -0.347 |  0     |  68.922 |
| HOEHNE M         | GER    |      50 |       3 |         0.34  |      0.073 |     -0.123 |           0 |            0 |   -1.424 | -0.057 |              0 |               0 |      0.12  |      -0.187 |  0.011 |  61     |

### Leads

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| MABERGS S   | SWE    |     258 |      14 |         0.55  |      0.035 |     -0.03  |           0 |            0 |   -0.611 |  0.006 |              0 |               0 |      0.088 |      -0.085 |  0.003 |  87.112 |
| KUZMINA E   | RUS    |     208 |      11 |         0.524 |      0.041 |     -0.035 |           0 |            0 |   -0.796 |  0.005 |              0 |               1 |      0.122 |      -0.149 |  0.003 |  84.223 |
| KIM S       | KOR    |     270 |      14 |         0.504 |      0.029 |     -0.032 |           0 |            0 |   -0.667 | -0.001 |              0 |               0 |      0.106 |      -0.115 | -0.001 |  81.296 |
| JENTSCH A   | GER    |     212 |      12 |         0.495 |      0.027 |     -0.043 |           0 |            0 |   -0.775 | -0.008 |              0 |               0 |      0.082 |      -0.097 |  0     |  75.711 |
| ISHIGOOKA H | JPN    |     268 |      15 |         0.493 |      0.035 |     -0.037 |           0 |            0 |   -0.904 | -0.001 |              0 |               0 |      0.116 |      -0.151 |  0.004 |  81.437 |
| KNUDSEN L   | DEN    |     222 |      12 |         0.491 |      0.035 |     -0.035 |           0 |            0 |   -0.678 | -0.001 |              0 |               0 |      0.129 |      -0.129 | -0.003 |  83.221 |
| BARONE E    | LAT    |     230 |      12 |         0.483 |      0.034 |     -0.045 |           0 |            0 |   -1.051 | -0.007 |              0 |               0 |      0.104 |      -0.146 |  0.001 |  78.587 |
| IMMONEN L   | FIN    |     218 |      12 |         0.482 |      0.036 |     -0.041 |           0 |            0 |   -0.823 | -0.004 |              0 |               0 |      0.142 |      -0.107 | -0.004 |  80.645 |
| VASILEVA U  | RUS    |      40 |       2 |         0.475 |      0.034 |     -0.034 |           0 |            0 |   -0.423 | -0.002 |              0 |               0 |      0.048 |      -0.06  |  0.008 |  86.25  |
| SILINA T    | LAT    |      38 |       2 |         0.474 |      0.028 |     -0.054 |           0 |            0 |   -0.54  | -0.015 |              0 |               0 |      0.032 |      -0.072 | -0     |  67.105 |
| MA J        | CHN    |     248 |      13 |         0.468 |      0.031 |     -0.036 |           0 |            0 |   -0.684 | -0.004 |              0 |               0 |      0.095 |      -0.12  | -0.003 |  84.577 |
| BARBEZAT M  | SUI    |     286 |      15 |         0.465 |      0.029 |     -0.036 |           0 |            0 |   -0.876 | -0.006 |              0 |               1 |      0.097 |      -0.18  |  0.001 |  86.14  |
| BROWN R     | CAN    |     234 |      12 |         0.457 |      0.035 |     -0.039 |           0 |            0 |   -0.902 | -0.005 |              0 |               0 |      0.116 |      -0.162 | -0.002 |  83.442 |
| WALKER M    | USA    |     232 |      12 |         0.453 |      0.031 |     -0.037 |           0 |            0 |   -0.884 | -0.006 |              0 |               0 |      0.127 |      -0.142 | -0.003 |  83.944 |
| SINCLAIR S  | SCO    |     228 |      12 |         0.439 |      0.037 |     -0.031 |           0 |            0 |   -0.635 | -0.001 |              0 |               0 |      0.085 |      -0.097 | -0.002 |  85.526 |

