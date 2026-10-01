# World Women's Curling Championship (WWCC2024_ResultsBook)

Sydney, NS, Canada, 2024; tier 1.0.

Execution (PGAA, points gained above average) relative to this event's field for the same shot type and hammer state, in hammer-adjusted points per shot. The block reads the player's distribution rather than its average: `reliability` is the share of shots at or above the field's expectation; `avg_make` how good the shot was when it was above, `avg_miss` how bad when below; `big_makes` / `big_misses` count shots beyond half a point either way; `worst5` sums the five costliest shots. `net` is the mean, kept as the single number that folds these together. The `_wp` columns are the effect on win probability, for reference: shots that gained or cost five or more points, and the five best and five worst stones summed, in percentage points. `call` is the call component (secondary). Players are grouped by throwing position and sorted by reliability, then by average miss. The team table above them is a different kind of table: a team's standing is its record and where its chance of winning came from, so it carries no execution columns.

## Women

### Teams

Each team's games in win probability, in percentage points per game. `net` is the record (a win is +50, a loss -50: every game runs from an even start to the end) and is the sort; it adds up from `dsc`, the start a team had from first-end hammer (won in the draw shot challenge; seeding in playoffs), `own`, what the team's stones did against what this field's stones did at the same point of the end, `allowed`, what the other team's stones did the same way, from this team's side (positive: they got less out of their stones than the field does), and `other`, what no stone accounts for (concessions between ends, ends missing from the book's shot-by-shot pages). A lead flattens both stone columns: in a decided game neither team's stones move much, which reads as low `own` and high `allowed`; read the two together as the team's stones and the split as style. `control` is the team's mean chance of winning at the start of each end (ends after the game was decided count as decided), the second sort: a team that leads early and keeps the game quiet holds it high.

| team   |   games | record   |   net |   dsc |   own |   allowed |   other |   control |
|:-------|--------:|:---------|------:|------:|------:|----------:|--------:|----------:|
| CAN    |      14 | 13-1     |  42.9 |   4.9 |  43.8 |      -5.4 |    -0.3 |      71   |
| KOR    |      15 | 12-3     |  30   |   3.8 |  19.6 |       2.7 |     3.8 |      63.4 |
| SUI    |      14 | 11-3     |  28.6 |   0   |  33.4 |      -7.5 |     2.6 |      69.3 |
| ITA    |      15 | 11-4     |  23.3 |   8.3 |  27.3 |     -10.1 |    -2.3 |      64.8 |
| SWE    |      13 | 7-6      |   3.8 |  -4.4 |  17.9 |      -8.3 |    -1.4 |      55.3 |
| USA    |      12 | 6-6      |   0   |  -1.9 |  -0.8 |       4.8 |    -2   |      49.6 |
| DEN    |      13 | 6-7      |  -3.8 |  -2.6 |  -5.3 |       3.1 |     0.9 |      44.9 |
| SCO    |      12 | 5-7      |  -8.3 |   0   | -14.8 |       6.1 |     0.4 |      38.2 |
| NOR    |      12 | 4-8      | -16.7 |  -1.9 | -25.6 |      10.6 |     0.3 |      40.8 |
| JPN    |      12 | 3-9      | -25   |  -1.9 | -19.7 |      -3.7 |     0.3 |      42   |
| TUR    |      12 | 3-9      | -25   |  -3.8 | -12.5 |      -6.6 |    -2.1 |      36.6 |
| EST    |      12 | 2-10     | -33.3 |   3.8 | -42.1 |       6.2 |    -1.3 |      38   |
| NZL    |      12 | 1-11     | -41.7 |  -7.6 | -46.9 |      12.5 |     0.4 |      22.2 |

### Build or address

How each team played the stones, in rock grades (descriptive, not a ranking): `build` is how much a stone added to the grade of the team's own rocks and `address` how much it took from the other team's, per stone, relative to this field at the same stage of the end; `builds_share` the share of its stones that built more than they addressed; `temperature` the mean peak of both teams' grades together in its ends with and without hammer (high: aggressive ends, low: conservative ones).

| team   |   stones |   build |   address |   builds_share |   temperature_hammer |   temperature_no_hammer |
|:-------|---------:|--------:|----------:|---------------:|---------------------:|------------------------:|
| EST    |      847 |   0.018 |    -0.069 |          0.718 |                1.957 |                   2.445 |
| ITA    |     1086 |   0.014 |    -0.008 |          0.625 |                2.152 |                   2.117 |
| JPN    |      889 |   0.011 |    -0.008 |          0.632 |                2.1   |                   2.234 |
| CAN    |      997 |   0.008 |     0.024 |          0.58  |                2.062 |                   2.003 |
| NOR    |      854 |   0.004 |    -0.016 |          0.643 |                1.914 |                   2.193 |
| SCO    |      853 |   0.003 |    -0.009 |          0.62  |                1.969 |                   2.015 |
| DEN    |      931 |  -0.004 |     0.008 |          0.582 |                2.256 |                   1.834 |
| NZL    |      759 |  -0.006 |    -0.029 |          0.596 |                2.143 |                   2.13  |
| SWE    |      967 |  -0.007 |    -0.002 |          0.57  |                1.835 |                   2.112 |
| SUI    |      959 |  -0.008 |     0.04  |          0.542 |                2.237 |                   1.825 |
| KOR    |     1122 |  -0.01  |     0.027 |          0.558 |                1.992 |                   2.027 |
| TUR    |      911 |  -0.01  |     0.016 |          0.58  |                2.047 |                   2.128 |
| USA    |      821 |  -0.011 |     0.005 |          0.571 |                2.335 |                   2.018 |

### Fourths

| player        | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:--------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| CONSTANTINI S | ITA    |     274 |      15 |         0.661 |      0.283 |     -0.243 |          29 |           16 |   -4.325 |  0.104 |             43 |              24 |      1.67  |      -0.678 | -0.003 |  84.871 |
| HOMAN R       | CAN    |     250 |      14 |         0.624 |      0.291 |     -0.172 |          27 |            8 |   -4.11  |  0.117 |             45 |              12 |      1.712 |      -0.966 |  0     |  88.563 |
| PAETZ A       | SUI    |     239 |      14 |         0.623 |      0.25  |     -0.2   |          17 |            9 |   -4.36  |  0.081 |             26 |              16 |      1.29  |      -0.981 |  0.004 |  89.089 |
| HASSELBORG A  | SWE    |     242 |      13 |         0.574 |      0.256 |     -0.211 |          22 |           11 |   -5.192 |  0.057 |             31 |              16 |      0.889 |      -0.711 |  0.011 |  84.428 |
| GIM E         | KOR    |     280 |      15 |         0.561 |      0.3   |     -0.251 |          29 |           14 |   -4.754 |  0.058 |             40 |              32 |      1.822 |      -0.845 | -0.005 |  80.306 |
| YILDIZ D      | TUR    |     231 |      12 |         0.541 |      0.291 |     -0.326 |          21 |           25 |   -6.256 |  0.008 |             31 |              32 |      1.037 |      -0.987 | -0.002 |  75.433 |
| DUPONT M      | DEN    |     233 |      13 |         0.515 |      0.296 |     -0.266 |          17 |           18 |   -6.916 |  0.023 |             27 |              26 |      1.384 |      -0.908 |  0.006 |  73.276 |
| SKASLIEN K    | NOR    |     208 |      12 |         0.505 |      0.235 |     -0.303 |          17 |           26 |   -5.65  | -0.031 |             17 |              26 |      0.808 |      -0.894 | -0.025 |  75.362 |
| TUVIKE E      | EST    |     216 |      12 |         0.5   |      0.295 |     -0.436 |          14 |           36 |   -9.582 | -0.071 |             25 |              44 |      1.582 |      -1.517 |  0.015 |  66.315 |
| PETERSON TAB  | USA    |     206 |      12 |         0.495 |      0.298 |     -0.321 |          19 |           17 |   -8.765 | -0.014 |             20 |              19 |      0.905 |      -0.7   |  0.022 |  76.733 |
| MORRISON R    | SCO    |     214 |      12 |         0.477 |      0.236 |     -0.349 |          11 |           23 |   -8.733 | -0.07  |             21 |              37 |      0.673 |      -1.072 |  0.016 |  74.761 |
| UENO M        | JPN    |     224 |      12 |         0.469 |      0.269 |     -0.298 |          16 |           23 |   -7.757 | -0.032 |             26 |              31 |      0.866 |      -1.132 |  0.006 |  67.568 |
| SMITH J       | NZL    |     178 |      11 |         0.393 |      0.328 |     -0.459 |          15 |           38 |   -9.188 | -0.15  |             15 |              35 |      1.46  |      -1.293 |  0.017 |  63.21  |

### Thirds

| player      | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| FLEURY T    | CAN    |     252 |      14 |         0.587 |      0.14  |     -0.143 |           5 |            5 |   -3.756 |  0.024 |             11 |              13 |      0.506 |      -0.574 | -0.019 |  85.417 |
| TIRINZONI S | SUI    |     238 |      14 |         0.576 |      0.151 |     -0.128 |           4 |            0 |   -1.919 |  0.033 |             12 |               4 |      0.436 |      -0.31  | -0.012 |  87.131 |
| ROERVIK M   | NOR    |     216 |      12 |         0.537 |      0.124 |     -0.139 |           2 |            3 |   -2.903 |  0.002 |              3 |               8 |      0.295 |      -0.43  | -0.002 |  82.907 |
| HALSE M     | DEN    |     236 |      13 |         0.525 |      0.126 |     -0.14  |           3 |            1 |   -2.257 | -0     |              4 |               9 |      0.324 |      -0.377 | -0.001 |  80.403 |
| MCMANUS S   | SWE    |     244 |      13 |         0.525 |      0.132 |     -0.145 |           2 |            3 |   -2.815 |  0     |             11 |              11 |      0.466 |      -0.359 | -0.003 |  87.807 |
| THIESSE C   | USA    |     208 |      12 |         0.49  |      0.125 |     -0.135 |           1 |            3 |   -3.136 | -0.008 |              3 |               5 |      0.294 |      -0.452 |  0.004 |  83.293 |
| KANAI A     | JPN    |     226 |      12 |         0.478 |      0.135 |     -0.149 |           1 |            4 |   -2.792 | -0.014 |              8 |              11 |      0.346 |      -0.443 |  0.007 |  75.996 |
| DODDS J     | SCO    |     214 |      12 |         0.477 |      0.138 |     -0.141 |           0 |            4 |   -3.255 | -0.008 |              4 |              10 |      0.364 |      -0.448 |  0.013 |  81.192 |
| KIM M       | KOR    |     284 |      15 |         0.475 |      0.136 |     -0.128 |           4 |            4 |   -2.908 | -0.003 |             11 |              10 |      0.486 |      -0.563 | -0.016 |  82.218 |
| POLAT O     | TUR    |     232 |      12 |         0.461 |      0.123 |     -0.144 |           2 |            4 |   -2.994 | -0.021 |             12 |               9 |      0.409 |      -0.467 |  0.007 |  77.371 |
| MATHIS E    | ITA    |     274 |      15 |         0.46  |      0.144 |     -0.144 |           5 |            5 |   -3.389 | -0.012 |             10 |              22 |      0.589 |      -0.499 | -0.006 |  80.748 |
| SMITH C     | NZL    |     190 |      12 |         0.437 |      0.128 |     -0.21  |           0 |            9 |   -3.267 | -0.063 |              3 |              13 |      0.383 |      -0.607 |  0.022 |  65.741 |
| LAIDSALU K  | EST    |     216 |      12 |         0.421 |      0.119 |     -0.157 |           2 |            5 |   -3.044 | -0.04  |              4 |              11 |      0.36  |      -0.541 |  0.004 |  77.431 |

### Seconds

| player           | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:-----------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| WITSCHONKE S     | SUI    |     238 |      14 |         0.555 |      0.087 |     -0.091 |           1 |            0 |   -1.843 |  0.008 |              1 |               1 |      0.238 |      -0.232 | -0.007 |  86.765 |
| KNOCHENHAUER A   | SWE    |     244 |      13 |         0.541 |      0.091 |     -0.094 |           0 |            0 |   -1.795 |  0.006 |              7 |               3 |      0.446 |      -0.243 | -0.011 |  85.041 |
| MISKEW E         | CAN    |     252 |      14 |         0.54  |      0.085 |     -0.079 |           0 |            1 |   -1.573 |  0.01  |              5 |               1 |      0.368 |      -0.22  | -0.005 |  88.147 |
| HASLEV NORDBYE M | NOR    |     216 |      12 |         0.528 |      0.091 |     -0.093 |           0 |            0 |   -2.055 |  0.004 |              2 |               3 |      0.223 |      -0.279 |  0.006 |  85.88  |
| THURLOW N        | NZL    |      40 |       3 |         0.525 |      0.1   |     -0.158 |           0 |            1 |   -1.792 | -0.022 |              0 |               1 |      0.078 |      -0.144 |  0.017 |  76.25  |
| KARAMAN I        | TUR    |      34 |       3 |         0.5   |      0.107 |     -0.133 |           0 |            1 |   -1.555 | -0.013 |              0 |               2 |      0.133 |      -0.237 | -0.001 |  69.853 |
| ROMEI A          | ITA    |     274 |      15 |         0.485 |      0.084 |     -0.069 |           2 |            0 |   -1.384 |  0.005 |              7 |               2 |      0.385 |      -0.228 |  0.002 |  85.348 |
| KIM S            | KOR    |     268 |      14 |         0.474 |      0.086 |     -0.075 |           0 |            0 |   -1.487 |  0.001 |              1 |               1 |      0.231 |      -0.182 | -0.004 |  84.422 |
| PETERSON TAR     | USA    |     208 |      12 |         0.466 |      0.079 |     -0.083 |           0 |            0 |   -1.423 | -0.007 |              0 |               0 |      0.176 |      -0.197 | -0.003 |  86.058 |
| NISHIMURO J      | JPN    |     208 |      11 |         0.466 |      0.075 |     -0.097 |           0 |            0 |   -1.996 | -0.017 |              2 |               4 |      0.266 |      -0.329 | -0     |  76.442 |
| SINCLAIR S       | SCO    |     214 |      12 |         0.458 |      0.069 |     -0.093 |           0 |            1 |   -1.74  | -0.019 |              1 |               4 |      0.223 |      -0.32  |  0.002 |  81.075 |
| LANDER J         | DEN    |     144 |       8 |         0.451 |      0.09  |     -0.093 |           0 |            0 |   -1.753 | -0.01  |              2 |               3 |      0.219 |      -0.292 |  0.006 |  81.597 |
| DUPONT D         | DEN    |     150 |       8 |         0.44  |      0.059 |     -0.08  |           0 |            1 |   -1.869 | -0.019 |              0 |               1 |      0.125 |      -0.211 | -0.002 |  79.027 |
| TURMANN L        | EST    |     216 |      12 |         0.435 |      0.069 |     -0.112 |           0 |            3 |   -2.539 | -0.034 |              0 |               3 |      0.167 |      -0.262 |  0.01  |  75.463 |
| BECKER B         | NZL    |     176 |      11 |         0.403 |      0.111 |     -0.131 |           1 |            3 |   -2.609 | -0.033 |              1 |               4 |      0.229 |      -0.332 |  0.012 |  64.915 |
| CALIKUSU IS      | TUR    |     198 |      11 |         0.374 |      0.085 |     -0.095 |           0 |            0 |   -1.767 | -0.028 |              1 |               4 |      0.223 |      -0.333 |  0.004 |  74.746 |

### Leads

| player            | team   |   shots |   games |   reliability |   avg_make |   avg_miss |   big_makes |   big_misses |   worst5 |    net |   big_makes_wp |   big_misses_wp |   best5_wp |   worst5_wp |   call |   grade |
|:------------------|:-------|--------:|--------:|--------------:|-----------:|-----------:|------------:|-------------:|---------:|-------:|---------------:|----------------:|-----------:|------------:|-------:|--------:|
| ZARDINI LACEDELLI | ITA    |     276 |      15 |         0.591 |      0.04  |     -0.039 |           0 |            0 |   -0.816 |  0.008 |              0 |               0 |      0.143 |      -0.13  |  0.003 |  92.399 |
| HOWALD C          | SUI    |     240 |      14 |         0.583 |      0.042 |     -0.036 |           0 |            0 |   -0.82  |  0.01  |              0 |               0 |      0.112 |      -0.133 |  0.002 |  93.41  |
| JACKSON S         | SCO    |     214 |      12 |         0.575 |      0.037 |     -0.046 |           0 |            0 |   -0.709 |  0.002 |              1 |               0 |      0.164 |      -0.108 |  0.001 |  88.668 |
| THOMPSON H        | NZL    |     176 |      11 |         0.568 |      0.031 |     -0.058 |           0 |            0 |   -0.964 | -0.008 |              1 |               0 |      0.152 |      -0.143 | -0.002 |  77.983 |
| WILKES S          | CAN    |     250 |      14 |         0.564 |      0.036 |     -0.034 |           0 |            0 |   -0.67  |  0.005 |              0 |               0 |      0.143 |      -0.113 |  0     |  91.8   |
| SEOL Y            | KOR    |     300 |      15 |         0.563 |      0.037 |     -0.038 |           0 |            0 |   -0.841 |  0.004 |              0 |               0 |      0.11  |      -0.136 |  0     |  87.833 |
| ROENNING M        | NOR    |     216 |      12 |         0.56  |      0.037 |     -0.039 |           0 |            0 |   -0.814 |  0.004 |              0 |               0 |      0.081 |      -0.096 |  0.002 |  91.088 |
| PERSINGER V       | USA    |      74 |       4 |         0.554 |      0.036 |     -0.04  |           0 |            0 |   -0.632 |  0.002 |              0 |               0 |      0.063 |      -0.082 |  0.002 |  87.162 |
| MABERGS S         | SWE    |     244 |      13 |         0.553 |      0.039 |     -0.044 |           0 |            0 |   -0.75  |  0.002 |              0 |               0 |      0.11  |      -0.131 |  0     |  90.164 |
| UENO Y            | JPN    |     226 |      12 |         0.527 |      0.044 |     -0.045 |           1 |            0 |   -0.995 |  0.002 |              0 |               0 |      0.085 |      -0.115 |  0.004 |  88.385 |
| GROSSMANN H       | EST    |     216 |      12 |         0.514 |      0.041 |     -0.044 |           0 |            0 |   -0.932 | -0.001 |              0 |               0 |      0.137 |      -0.102 |  0.004 |  83.449 |
| LARSEN M          | DEN    |     178 |      10 |         0.511 |      0.036 |     -0.045 |           0 |            0 |   -0.638 | -0.004 |              0 |               0 |      0.09  |      -0.105 | -0.002 |  81.32  |
| HAMILTON B        | USA    |     134 |       8 |         0.507 |      0.038 |     -0.043 |           0 |            0 |   -0.776 | -0.002 |              0 |               0 |      0.061 |      -0.1   |  0.003 |  85.448 |
| SENGUL B          | TUR    |     232 |      12 |         0.487 |      0.037 |     -0.044 |           0 |            0 |   -0.775 | -0.005 |              0 |               0 |      0.115 |      -0.121 |  0.001 |  84.914 |

