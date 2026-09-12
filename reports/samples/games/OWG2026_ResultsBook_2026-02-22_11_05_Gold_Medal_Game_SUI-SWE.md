# Milano Cortina 2026 Olympic Winter Games, Curling: Gold Medal Game, Switzerland v Sweden (women)

2026-02-22 11:05; SUI red, SWE yellow. Final score SUI 5, SWE 6. Game key `OWG2026_ResultsBook|2026-02-22|11:05|Gold_Medal_Game|SUI-SWE`.

Every value is a difference of model outputs on the diagrammed positions (design Sections 2 and 10). `V before`, `V call` and `V after` are the hammer team's expected hammer-adjusted points before the shot, after the call (the field's usual result for this shot type from this position) and after the delivered stone. `call`, `throw` and `total` are from the thrower's view: `call` = V call - V before, `throw` = V after - V call, `total` = call + throw, signed so a gain for the thrower's team is positive. The `wp` columns are the same differences in win probability, in percentage points. Within an end the hammer team's totals minus the other team's totals sum exactly to the end's result minus `V before` on the first stone.

## Ends

`E[pts] start` is the hammer team's expected hammer-adjusted points at the start of the end and `result (adj)` the end's result in the same currency (H = 0.58: a score of k is worth k - H because the hammer passes, a steal of k is -k + H, a blank +H). The call and throw columns are each team's summed values over the end (thrower's view); the win-probability columns are SUI's, before the first stone and after the last.

|   end | hammer   | result       |   E[pts] start |   result (adj) |   SUI call |   SUI throw |   SWE call |   SWE throw |   WP SUI start |   WP SUI end |
|------:|:---------|:-------------|---------------:|---------------:|-----------:|------------:|-----------:|------------:|---------------:|-------------:|
|     1 | SWE      | SWE 2        |           0.65 |           1.42 |      -0.3  |        0.51 |       0.21 |        0.77 |           38.4 |         24.3 |
|     2 | SUI      | blank        |           0.4  |           0.58 |       0.84 |        0.02 |       0.29 |        0.4  |           24.5 |         24.5 |
|     3 | SUI      | blank        |           0.44 |           0.58 |       0.73 |       -0.01 |      -0.01 |        0.59 |           24.5 |         26   |
|     4 | SUI      | SUI 1        |           0.47 |           0.42 |       0.44 |       -0.22 |      -0.14 |        0.41 |           25.1 |         20.6 |
|     5 | SWE      | SWE 1        |           0.71 |           0.42 |       0.35 |        1.65 |       0.42 |        1.28 |           21.3 |         25.2 |
|     6 | SUI      | SUI 2        |           0.49 |           1.42 |       0.42 |        0.89 |      -0.49 |        0.88 |           22.8 |         36.9 |
|     7 | SWE      | SWE 1        |           0.63 |           0.42 |      -0.12 |        0.62 |       0.36 |       -0.07 |           36   |         40.5 |
|     8 | SUI      | SWE steals 1 |           0.56 |          -0.42 |      -0.17 |       -0.53 |      -0.31 |        0.58 |           40.1 |         12.9 |
|     9 | SUI      | SUI 2        |           0.5  |           1.42 |       0.73 |        0.85 |      -0.04 |        0.7  |           13.5 |         20.4 |
|    10 | SWE      | SWE 1        |           0.42 |           0.42 |      -0.79 |        0.07 |       0.34 |       -1.06 |           21   |          0   |

Conservation: max |sum of shot values - (result (adj) - E[pts] start)| over ends = 1.4e-16.

## Players

Sums over the game, thrower's view. `throw` is execution: the value of the delivered stone against the field's usual result for the call. `total` adds the call component. The official grade is the book's percentage.

| team   | player         |   shots |   call |   throw |   total |   throw wp |   total wp |   grade | worst throw              | best throw              |
|:-------|:---------------|--------:|-------:|--------:|--------:|-----------:|-----------:|--------:|:-------------------------|:------------------------|
| SUI    | PAETZ A        |      20 |   1.12 |    2.88 |    4    |      48.63 |      55.64 |   80    | -0.38 (end 4, stone 16)  | +1.04 (end 5, stone 15) |
| SUI    | TIRINZONI S    |      20 |   0.04 |    1.1  |    1.14 |      27.5  |      18.12 |   78.75 | -0.11 (end 7, stone 11)  | +0.53 (end 9, stone 10) |
| SUI    | HOWALD C       |      20 |   0.63 |    0.02 |    0.65 |      16.27 |      18.06 |   75    | -0.21 (end 6, stone 6)   | +0.28 (end 5, stone 7)  |
| SUI    | WITSCHONKE S   |      20 |   0.34 |   -0.14 |    0.2  |       7.18 |       4.82 |   97.5  | -0.10 (end 9, stone 2)   | +0.09 (end 1, stone 3)  |
| SWE    | HASSELBORG A   |      20 |   0.49 |    3.02 |    3.51 |      68.98 |      90.7  |   83.75 | -0.57 (end 10, stone 16) | +0.69 (end 1, stone 14) |
| SWE    | McMANUS S      |      20 |   0.26 |    0.42 |    0.68 |       1.03 |      23.46 |   80    | -0.21 (end 1, stone 12)  | +0.56 (end 5, stone 12) |
| SWE    | KNOCHENHAUER A |      20 |   0.05 |    0.69 |    0.73 |       3.21 |      15.97 |   81.25 | -0.21 (end 10, stone 8)  | +0.17 (end 9, stone 5)  |
| SWE    | SCHARBACK S    |      20 |  -0.17 |    0.36 |    0.19 |      -0.8  |       2.4  |   85    | -0.12 (end 7, stone 4)   | +0.10 (end 9, stone 3)  |

## Largest swings

The ten shots that moved win probability most, either way.

|   end |   shot | team   | player       | type            | turn   |   grade |   call |   throw |   total |   throw wp |   total wp |
|------:|-------:|:-------|:-------------|:----------------|:-------|--------:|-------:|--------:|--------:|-----------:|-----------:|
|     5 |     15 | SUI    | PAETZ A      | Double Take-out | cw     |     100 |   0.21 |    1.04 |    1.26 |      15.3  |      17.2  |
|     1 |     14 | SWE    | HASSELBORG A | Double Take-out | cw     |     100 |   0.01 |    0.69 |    0.7  |      12.15 |      12.27 |
|    10 |     16 | SWE    | HASSELBORG A | Take-out        | ccw    |     100 |   0.21 |   -0.57 |   -0.36 |       5.05 |      10.68 |
|     5 |     12 | SWE    | McMANUS S    | Take-out        | cw     |     100 |   0.2  |    0.56 |    0.76 |       7.49 |      10.04 |
|    10 |     10 | SWE    | McMANUS S    | Clearing        | ccw    |     100 |   0.06 |   -0.04 |    0.02 |      -1.47 |       9.88 |
|     8 |     16 | SUI    | PAETZ A      | Double Take-out | ccw    |      25 |   0.08 |   -0.32 |   -0.24 |     -12.15 |      -9.85 |
|     1 |     16 | SWE    | HASSELBORG A | Take-out        | ccw    |     100 |   0.13 |    0.35 |    0.48 |       6.43 |       8.82 |
|     6 |     16 | SUI    | PAETZ A      | Draw            | ccw    |     100 |  -0.01 |    0.54 |    0.53 |       8.73 |       8.58 |
|     7 |     15 | SUI    | PAETZ A      | Take-out        | ccw    |     100 |   0.16 |    0.21 |    0.37 |       5.16 |       8.46 |
|     9 |     16 | SUI    | PAETZ A      | Raise           | ccw    |     100 |   0.26 |    0.52 |    0.78 |       5.51 |       8.46 |

## Shots

### End 1: SWE hammer, tied, 10 ends left; result SWE 2

|   shot | team   | player         | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SUI    | WITSCHONKE S   | Front           | ccw    |     100 |       0.65 |     0.66 |      0.63 |  -0.01 |    0.04 |    0.03 |       0.73 |       0.71 |
|      2 | SWE    | SCHARBACK S    | Draw            | cw     |     100 |       0.63 |     0.63 |      0.68 |   0    |    0.05 |    0.06 |       0.82 |       0.91 |
|      3 | SUI    | WITSCHONKE S   | Draw            | ccw    |     100 |       0.68 |     0.69 |      0.6  |  -0    |    0.09 |    0.08 |       1.33 |       1.27 |
|      4 | SWE    | SCHARBACK S    | Draw            | cw     |     100 |       0.6  |     0.65 |      0.6  |   0.04 |   -0.05 |   -0    |      -0.87 |      -0.24 |
|      5 | SUI    | HOWALD C       | Draw            | ccw    |      50 |       0.6  |     0.58 |      0.65 |   0.02 |   -0.07 |   -0.05 |      -1.03 |      -0.73 |
|      6 | SWE    | KNOCHENHAUER A | Draw            | cw     |       0 |       0.65 |     0.64 |      0.5  |  -0.02 |   -0.14 |   -0.15 |      -2.27 |      -2.5  |
|      7 | SUI    | HOWALD C       | Draw            | cw     |     100 |       0.5  |     0.54 |      0.59 |  -0.04 |   -0.06 |   -0.09 |      -0.84 |      -1.44 |
|      8 | SWE    | KNOCHENHAUER A | Clearing        | ccw    |      50 |       0.59 |     0.56 |      0.69 |  -0.04 |    0.13 |    0.1  |       2.15 |       1.75 |
|      9 | SUI    | TIRINZONI S    | Double Take-out | ccw    |      50 |       0.69 |     0.76 |      0.73 |  -0.07 |    0.03 |   -0.04 |       0.59 |      -0.71 |
|     10 | SWE    | McMANUS S      | Draw            | cw     |     100 |       0.73 |     0.69 |      0.63 |  -0.05 |   -0.06 |   -0.11 |      -1.15 |      -1.9  |
|     11 | SUI    | TIRINZONI S    | Double Take-out | cw     |     100 |       0.63 |     0.71 |      0.62 |  -0.09 |    0.1  |    0.01 |       1.52 |      -0.04 |
|     12 | SWE    | McMANUS S      | Take-out        | ccw    |      75 |       0.62 |     0.73 |      0.52 |   0.11 |   -0.21 |   -0.09 |      -3.82 |      -1.77 |
|     13 | SUI    | PAETZ A        | Take-out        | cw     |     100 |       0.52 |     0.65 |      0.39 |  -0.13 |    0.26 |    0.13 |       4.02 |       1.87 |
|     14 | SWE    | HASSELBORG A   | Double Take-out | cw     |     100 |       0.39 |     0.41 |      1.1  |   0.01 |    0.69 |    0.7  |      12.15 |      12.27 |
|     15 | SUI    | PAETZ A        | Double Take-out | cw     |      50 |       1.1  |     1.07 |      0.94 |   0.02 |    0.14 |    0.16 |       1.96 |       2.33 |
|     16 | SWE    | HASSELBORG A   | Take-out        | ccw    |     100 |       0.94 |     1.07 |      1.42 |   0.13 |    0.35 |    0.48 |       6.43 |       8.82 |

### End 2: SUI hammer, down 2, 9 ends left; result blank

|   shot | team   | player         | type         | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:-------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SWE    | SCHARBACK S    | Front        | ccw    |     100 |       0.4  |     0.47 |      0.46 |  -0.07 |    0.02 |   -0.05 |       0.17 |      -0.62 |
|      2 | SUI    | WITSCHONKE S   | Front        | ccw    |     100 |       0.46 |     0.5  |      0.45 |   0.04 |   -0.05 |   -0.01 |      -0.45 |       0.06 |
|      3 | SWE    | SCHARBACK S    | Draw         | ccw    |      75 |       0.45 |     0.5  |      0.44 |  -0.05 |    0.06 |    0.01 |       0.85 |       0.3  |
|      4 | SUI    | WITSCHONKE S   | Take-out     | ccw    |     100 |       0.44 |     0.56 |      0.54 |   0.12 |   -0.03 |    0.1  |      -0.36 |       1.08 |
|      5 | SWE    | KNOCHENHAUER A | Hit and Roll | ccw    |      75 |       0.54 |     0.55 |      0.5  |  -0.02 |    0.05 |    0.03 |       0.46 |       0.4  |
|      6 | SUI    | HOWALD C       | Hit and Roll | ccw    |      50 |       0.5  |     0.63 |      0.43 |   0.13 |   -0.2  |   -0.07 |      -2.9  |      -1.25 |
|      7 | SWE    | KNOCHENHAUER A | Draw         | ccw    |      75 |       0.43 |     0.48 |      0.42 |  -0.05 |    0.06 |    0.01 |       0.88 |       0.03 |
|      8 | SUI    | HOWALD C       | Hit and Roll | cw     |      75 |       0.42 |     0.55 |      0.63 |   0.13 |    0.08 |    0.21 |       1.36 |       3.04 |
|      9 | SWE    | McMANUS S      | Hit and Roll | cw     |      75 |       0.63 |     0.56 |      0.4  |   0.07 |    0.17 |    0.24 |       2.16 |       3.51 |
|     10 | SUI    | TIRINZONI S    | Hit and Roll | cw     |      75 |       0.4  |     0.51 |      0.45 |   0.11 |   -0.06 |    0.06 |      -0.73 |       0.69 |
|     11 | SWE    | McMANUS S      | Take-out     | cw     |      50 |       0.45 |     0.5  |      0.56 |  -0.05 |   -0.06 |   -0.11 |      -0.68 |      -1.03 |
|     12 | SUI    | TIRINZONI S    | Draw         | ccw    |      75 |       0.56 |     0.62 |      0.66 |   0.05 |    0.04 |    0.09 |       0.75 |       1.83 |
|     13 | SWE    | HASSELBORG A   | Take-out     | ccw    |     100 |       0.66 |     0.49 |      0.41 |   0.16 |    0.09 |    0.25 |       1.28 |       4.23 |
|     14 | SUI    | PAETZ A        | Hit and Roll | cw     |      75 |       0.41 |     0.51 |      0.68 |   0.11 |    0.17 |    0.27 |       2.8  |       4.23 |
|     15 | SWE    | HASSELBORG A   | Hit and Roll | cw     |      75 |       0.68 |     0.38 |      0.37 |   0.3  |    0.01 |    0.31 |       0.9  |       5.65 |
|     16 | SUI    | PAETZ A        | Clearing     | cw     |     100 |       0.37 |     0.51 |      0.58 |   0.14 |    0.07 |    0.21 |       0.86 |       2.73 |

### End 3: SUI hammer, down 2, 8 ends left; result blank

|   shot | team   | player         | type         | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:-------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SWE    | SCHARBACK S    | Front        | cw     |     100 |       0.44 |     0.51 |      0.48 |  -0.07 |    0.03 |   -0.03 |       0.34 |      -0.33 |
|      2 | SUI    | WITSCHONKE S   | Front        | ccw    |     100 |       0.48 |     0.52 |      0.46 |   0.05 |   -0.07 |   -0.02 |      -0.67 |      -0.18 |
|      3 | SWE    | SCHARBACK S    | Draw         | cw     |     100 |       0.46 |     0.51 |      0.42 |  -0.05 |    0.09 |    0.04 |       1.13 |       0.64 |
|      4 | SUI    | WITSCHONKE S   | Draw         | ccw    |      75 |       0.42 |     0.47 |      0.43 |   0.06 |   -0.04 |    0.01 |      -0.55 |       0.14 |
|      5 | SWE    | KNOCHENHAUER A | Take-out     | cw     |     100 |       0.43 |     0.46 |      0.32 |  -0.03 |    0.13 |    0.11 |       1.53 |       1.37 |
|      6 | SUI    | HOWALD C       | Hit and Roll | cw     |      50 |       0.32 |     0.43 |      0.42 |   0.11 |   -0.02 |    0.1  |      -0.3  |       1.02 |
|      7 | SWE    | KNOCHENHAUER A | Draw         | cw     |      75 |       0.42 |     0.47 |      0.4  |  -0.05 |    0.07 |    0.01 |       0.88 |       0.2  |
|      8 | SUI    | HOWALD C       | Take-out     | ccw    |     100 |       0.4  |     0.54 |      0.51 |   0.14 |   -0.03 |    0.11 |      -0.32 |       1.37 |
|      9 | SWE    | McMANUS S      | Take-out     | ccw    |     100 |       0.51 |     0.52 |      0.48 |  -0.01 |    0.04 |    0.03 |       0.49 |       0.52 |
|     10 | SUI    | TIRINZONI S    | Draw         | ccw    |     100 |       0.48 |     0.55 |      0.57 |   0.07 |    0.02 |    0.09 |       0.51 |       1.32 |
|     11 | SWE    | McMANUS S      | Take-out     | ccw    |      50 |       0.57 |     0.48 |      0.44 |   0.09 |    0.04 |    0.13 |       0.63 |       2.12 |
|     12 | SUI    | TIRINZONI S    | Take-out     | cw     |     100 |       0.44 |     0.54 |      0.54 |   0.1  |   -0    |    0.1  |       0.06 |       1.29 |
|     13 | SWE    | HASSELBORG A   | Take-out     | ccw    |     100 |       0.54 |     0.48 |      0.37 |   0.05 |    0.11 |    0.16 |       1.68 |       2.47 |
|     14 | SUI    | PAETZ A        | Take-out     | cw     |     100 |       0.37 |     0.44 |      0.44 |   0.07 |   -0.01 |    0.06 |      -0.17 |       0.84 |
|     15 | SWE    | HASSELBORG A   | Take-out     | ccw    |     100 |       0.44 |     0.38 |      0.31 |   0.05 |    0.08 |    0.13 |       1.33 |       1.95 |
|     16 | SUI    | PAETZ A        | Clearing     | ccw    |     100 |       0.31 |     0.46 |      0.58 |   0.15 |    0.12 |    0.27 |       2.1  |       4.64 |

### End 4: SUI hammer, down 2, 7 ends left; result SUI 1

|   shot | team   | player         | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SWE    | SCHARBACK S    | Front           | ccw    |     100 |       0.47 |     0.5  |      0.5  |  -0.03 |   -0    |   -0.03 |      -0.12 |      -0.52 |
|      2 | SUI    | WITSCHONKE S   | Front           | cw     |     100 |       0.5  |     0.52 |      0.5  |   0.02 |   -0.02 |   -0    |      -0.16 |       0.06 |
|      3 | SWE    | SCHARBACK S    | Draw            | ccw    |     100 |       0.5  |     0.5  |      0.44 |  -0    |    0.06 |    0.06 |       0.89 |       0.96 |
|      4 | SUI    | WITSCHONKE S   | Draw            | ccw    |     100 |       0.44 |     0.48 |      0.44 |   0.04 |   -0.05 |   -0    |      -0.68 |      -0    |
|      5 | SWE    | KNOCHENHAUER A | Draw            | ccw    |      75 |       0.44 |     0.43 |      0.44 |   0.01 |   -0.01 |   -0    |      -0.1  |      -0.05 |
|      6 | SUI    | HOWALD C       | Double Take-out | ccw    |     100 |       0.44 |     0.54 |      0.65 |   0.1  |    0.11 |    0.21 |       1.39 |       2.91 |
|      7 | SWE    | KNOCHENHAUER A | Draw            | ccw    |     100 |       0.65 |     0.68 |      0.7  |  -0.03 |   -0.02 |   -0.05 |      -0.3  |      -0.83 |
|      8 | SUI    | HOWALD C       | Draw            | cw     |     100 |       0.7  |     0.75 |      0.66 |   0.05 |   -0.09 |   -0.04 |      -1.53 |      -0.59 |
|      9 | SWE    | McMANUS S      | Draw            | cw     |     100 |       0.66 |     0.66 |      0.73 |  -0    |   -0.07 |   -0.08 |      -1.27 |      -1.35 |
|     10 | SUI    | TIRINZONI S    | Raise           | ccw    |     100 |       0.73 |     0.76 |      0.73 |   0.03 |   -0.03 |   -0.01 |      -0.47 |      -0.02 |
|     11 | SWE    | McMANUS S      | Double Take-out | ccw    |      50 |       0.73 |     0.74 |      0.71 |  -0.01 |    0.03 |    0.01 |       0.36 |       0.42 |
|     12 | SUI    | TIRINZONI S    | Take-out        | cw     |     100 |       0.71 |     0.79 |      0.81 |   0.08 |    0.03 |    0.1  |       0.11 |       1.53 |
|     13 | SWE    | HASSELBORG A   | Draw            | ccw    |     100 |       0.81 |     0.82 |      0.85 |  -0.01 |   -0.02 |   -0.03 |      -0.29 |      -0.52 |
|     14 | SUI    | PAETZ A        | Draw            | ccw    |     100 |       0.85 |     0.93 |      1.14 |   0.09 |    0.21 |    0.29 |       3.72 |       5.07 |
|     15 | SWE    | HASSELBORG A   | Raise           | cw     |      50 |       1.14 |     1.2  |      0.75 |  -0.07 |    0.45 |    0.38 |       8.75 |       7.47 |
|     16 | SUI    | PAETZ A        | Draw            | ccw    |       0 |       0.75 |     0.8  |      0.42 |   0.04 |   -0.38 |   -0.34 |      -8.26 |      -7.91 |

### End 5: SWE hammer, up 1, 6 ends left; result SWE 1

|   shot | team   | player         | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SUI    | WITSCHONKE S   | Front           | ccw    |     100 |       0.71 |     0.71 |      0.72 |  -0    |   -0.01 |   -0.01 |       0    |       0.1  |
|      2 | SWE    | SCHARBACK S    | Draw            | ccw    |      75 |       0.72 |     0.72 |      0.75 |  -0    |    0.04 |    0.03 |       0.43 |       0.36 |
|      3 | SUI    | WITSCHONKE S   | Draw            | cw     |      75 |       0.75 |     0.78 |      0.72 |  -0.02 |    0.06 |    0.04 |       0.78 |       0.53 |
|      4 | SWE    | SCHARBACK S    | Draw            | ccw    |     100 |       0.72 |     0.73 |      0.7  |   0.01 |   -0.02 |   -0.02 |      -0.16 |      -0.27 |
|      5 | SUI    | HOWALD C       | Draw            | ccw    |     100 |       0.7  |     0.69 |      0.56 |   0.02 |    0.13 |    0.14 |       1.82 |       2.13 |
|      6 | SWE    | KNOCHENHAUER A | Double Take-out | ccw    |      50 |       0.56 |     0.8  |      0.76 |   0.24 |   -0.04 |    0.2  |      -0.2  |       2.89 |
|      7 | SUI    | HOWALD C       | Draw            | cw     |     100 |       0.76 |     0.73 |      0.45 |   0.03 |    0.28 |    0.31 |       4.03 |       4.64 |
|      8 | SWE    | KNOCHENHAUER A | Clearing        | ccw    |     100 |       0.45 |     0.41 |      0.44 |  -0.04 |    0.03 |   -0.01 |       0.59 |       0.22 |
|      9 | SUI    | TIRINZONI S    | Guard           | ccw    |     100 |       0.44 |     0.39 |      0.41 |   0.05 |   -0.01 |    0.04 |       0.06 |       0.93 |
|     10 | SWE    | McMANUS S      | Raise           | cw     |      50 |       0.41 |     0.38 |      0.37 |  -0.03 |   -0.01 |   -0.04 |      -0.44 |      -1.11 |
|     11 | SUI    | TIRINZONI S    | Hit and Roll    | ccw    |      75 |       0.37 |     0.43 |      0.35 |  -0.07 |    0.08 |    0.02 |       0.78 |      -0.22 |
|     12 | SWE    | McMANUS S      | Take-out        | cw     |     100 |       0.35 |     0.55 |      1.11 |   0.2  |    0.56 |    0.76 |       7.49 |      10.04 |
|     13 | SUI    | PAETZ A        | Hit and Roll    | cw     |      75 |       1.11 |     0.98 |      0.9  |   0.13 |    0.07 |    0.2  |       0.7  |       1.87 |
|     14 | SWE    | HASSELBORG A   | Draw            | cw     |      75 |       0.9  |     0.93 |      1.19 |   0.03 |    0.26 |    0.29 |       2.6  |       3.06 |
|     15 | SUI    | PAETZ A        | Double Take-out | cw     |     100 |       1.19 |     0.98 |     -0.06 |   0.21 |    1.04 |    1.26 |      15.3  |      17.2  |
|     16 | SWE    | HASSELBORG A   | Draw            | cw     |     100 |      -0.06 |    -0.05 |      0.42 |   0.02 |    0.47 |    0.48 |       7.73 |       8.06 |

### End 6: SUI hammer, down 2, 5 ends left; result SUI 2

|   shot | team   | player         | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SWE    | SCHARBACK S    | Front           | ccw    |       0 |       0.49 |     0.52 |      0.51 |  -0.03 |    0.01 |   -0.02 |       0.3  |      -0.11 |
|      2 | SUI    | WITSCHONKE S   | Front           | cw     |     100 |       0.51 |     0.53 |      0.5  |   0.02 |   -0.03 |   -0.01 |      -0.34 |      -0.07 |
|      3 | SWE    | SCHARBACK S    | Guard           | ccw    |     100 |       0.5  |     0.52 |      0.52 |  -0.02 |    0    |   -0.02 |      -0.44 |      -0.6  |
|      4 | SUI    | WITSCHONKE S   | Draw            | cw     |     100 |       0.52 |     0.55 |      0.58 |   0.04 |    0.02 |    0.06 |       0.42 |       0.94 |
|      5 | SWE    | KNOCHENHAUER A | Draw            | cw     |     100 |       0.58 |     0.61 |      0.51 |  -0.04 |    0.1  |    0.06 |       1.52 |       0.84 |
|      6 | SUI    | HOWALD C       | Take-out        | cw     |       0 |       0.51 |     0.67 |      0.46 |   0.16 |   -0.21 |   -0.05 |      -3.37 |      -0.76 |
|      7 | SWE    | KNOCHENHAUER A | Draw            | cw     |     100 |       0.46 |     0.46 |      0.32 |   0.01 |    0.13 |    0.14 |       1.73 |       1.69 |
|      8 | SUI    | HOWALD C       | Double Take-out | ccw    |      50 |       0.32 |     0.31 |      0.26 |  -0.01 |   -0.05 |   -0.07 |      -0.28 |      -0.48 |
|      9 | SWE    | McMANUS S      | Draw            | ccw    |      75 |       0.26 |     0.25 |      0.24 |   0.01 |    0.02 |    0.02 |       0.3  |       0.16 |
|     10 | SUI    | TIRINZONI S    | Draw            | ccw    |      75 |       0.24 |     0.28 |      0.53 |   0.04 |    0.25 |    0.3  |       3.25 |       3.82 |
|     11 | SWE    | McMANUS S      | Draw            | ccw    |     100 |       0.53 |     0.61 |      0.37 |  -0.08 |    0.24 |    0.16 |       3.52 |       2.36 |
|     12 | SUI    | TIRINZONI S    | Draw            | ccw    |     100 |       0.37 |     0.43 |      0.64 |   0.05 |    0.21 |    0.26 |       2.32 |       3.21 |
|     13 | SWE    | HASSELBORG A   | Draw            | ccw    |     100 |       0.64 |     0.77 |      0.65 |  -0.14 |    0.12 |   -0.01 |       3.3  |       0.51 |
|     14 | SUI    | PAETZ A        | Draw            | cw     |     100 |       0.65 |     0.77 |      0.94 |   0.12 |    0.17 |    0.29 |       3.63 |       5.84 |
|     15 | SWE    | HASSELBORG A   | Double Take-out | cw     |      50 |       0.94 |     1.15 |      0.89 |  -0.21 |    0.26 |    0.05 |       5.95 |       2.17 |
|     16 | SUI    | PAETZ A        | Draw            | ccw    |     100 |       0.89 |     0.88 |      1.42 |  -0.01 |    0.54 |    0.53 |       8.73 |       8.58 |

### End 7: SWE hammer, tied, 4 ends left; result SWE 1

|   shot | team   | player         | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SUI    | WITSCHONKE S   | Front           | ccw    |     100 |       0.63 |     0.66 |      0.6  |  -0.02 |    0.05 |    0.03 |       1.04 |       0.75 |
|      2 | SWE    | SCHARBACK S    | Draw            | cw     |     100 |       0.6  |     0.64 |      0.65 |   0.04 |    0.01 |    0.04 |       0.16 |       0.75 |
|      3 | SUI    | WITSCHONKE S   | Draw            | ccw    |     100 |       0.65 |     0.68 |      0.67 |  -0.03 |    0.01 |   -0.02 |       0.1  |      -0.49 |
|      4 | SWE    | SCHARBACK S    | Draw            | cw     |      75 |       0.67 |     0.73 |      0.6  |   0.06 |   -0.12 |   -0.06 |      -2.41 |      -1.55 |
|      5 | SUI    | HOWALD C       | Hit and Roll    | cw     |      75 |       0.6  |     0.67 |      0.55 |  -0.07 |    0.11 |    0.05 |       2.44 |       0.89 |
|      6 | SWE    | KNOCHENHAUER A | Hit and Roll    | cw     |      75 |       0.55 |     0.68 |      0.6  |   0.13 |   -0.08 |    0.05 |      -1.53 |       0.89 |
|      7 | SUI    | HOWALD C       | Hit and Roll    | cw     |      75 |       0.6  |     0.67 |      0.55 |  -0.07 |    0.12 |    0.05 |       2.48 |       0.91 |
|      8 | SWE    | KNOCHENHAUER A | Double Take-out | ccw    |     100 |       0.55 |     0.57 |      0.6  |   0.02 |    0.03 |    0.04 |       1.01 |       1.87 |
|      9 | SUI    | TIRINZONI S    | Guard           | ccw    |     100 |       0.6  |     0.62 |      0.66 |  -0.02 |   -0.04 |   -0.06 |      -0.5  |      -0.29 |
|     10 | SWE    | McMANUS S      | Clearing        | ccw    |     100 |       0.66 |     0.6  |      0.58 |  -0.06 |   -0.02 |   -0.08 |       0.03 |      -0.64 |
|     11 | SUI    | TIRINZONI S    | Guard           | ccw    |       0 |       0.58 |     0.61 |      0.72 |  -0.03 |   -0.11 |   -0.14 |      -2.19 |      -2.11 |
|     12 | SWE    | McMANUS S      | Double Take-out | ccw    |      50 |       0.72 |     0.7  |      0.51 |  -0.01 |   -0.19 |   -0.21 |      -3.43 |      -3.36 |
|     13 | SUI    | PAETZ A        | Take-out        | ccw    |     100 |       0.51 |     0.55 |      0.29 |  -0.04 |    0.26 |    0.22 |       6.04 |       4.75 |
|     14 | SWE    | HASSELBORG A   | Hit and Roll    | cw     |      75 |       0.29 |     0.38 |      0.6  |   0.09 |    0.22 |    0.31 |       4.32 |       6.42 |
|     15 | SUI    | PAETZ A        | Take-out        | ccw    |     100 |       0.6  |     0.43 |      0.23 |   0.16 |    0.21 |    0.37 |       5.16 |       8.46 |
|     16 | SWE    | HASSELBORG A   | Take-out        | cw     |     100 |       0.23 |     0.33 |      0.42 |   0.1  |    0.09 |    0.19 |       1.97 |       4.02 |

### End 8: SUI hammer, down 1, 3 ends left; result SWE steals 1

|   shot | team   | player         | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SWE    | SCHARBACK S    | Front           | ccw    |     100 |       0.56 |     0.57 |      0.56 |  -0.02 |    0.01 |   -0    |       0.35 |      -0.04 |
|      2 | SUI    | WITSCHONKE S   | Front           | cw     |     100 |       0.56 |     0.56 |      0.55 |  -0    |   -0    |   -0.01 |       0.13 |       0.09 |
|      3 | SWE    | SCHARBACK S    | Draw            | ccw    |     100 |       0.55 |     0.54 |      0.5  |   0.01 |    0.04 |    0.05 |       0.84 |       1.15 |
|      4 | SUI    | WITSCHONKE S   | Draw            | cw     |     100 |       0.5  |     0.51 |      0.46 |   0    |   -0.05 |   -0.04 |      -1.1  |      -0.91 |
|      5 | SWE    | KNOCHENHAUER A | Guard           | ccw    |      50 |       0.46 |     0.47 |      0.48 |  -0.01 |   -0    |   -0.02 |       0.12 |      -0.23 |
|      6 | SUI    | HOWALD C       | Double Take-out | ccw    |      50 |       0.48 |     0.42 |      0.44 |  -0.05 |    0.02 |   -0.03 |       0.51 |      -0.69 |
|      7 | SWE    | KNOCHENHAUER A | Guard           | ccw    |     100 |       0.44 |     0.5  |      0.36 |  -0.06 |    0.14 |    0.08 |       2.97 |       1.61 |
|      8 | SUI    | HOWALD C       | Double Take-out | ccw    |      50 |       0.36 |     0.38 |      0.4  |   0.02 |    0.02 |    0.04 |       0.24 |       0.65 |
|      9 | SWE    | McMANUS S      | Guard           | ccw    |     100 |       0.4  |     0.46 |      0.41 |  -0.06 |    0.05 |   -0    |       0.97 |      -0.13 |
|     10 | SUI    | TIRINZONI S    | Double Take-out | ccw    |      50 |       0.41 |     0.32 |      0.35 |  -0.09 |    0.03 |   -0.06 |       0.58 |      -1.54 |
|     11 | SWE    | McMANUS S      | Guard           | ccw    |     100 |       0.35 |     0.41 |      0.36 |  -0.06 |    0.05 |   -0.01 |       0.97 |      -0.27 |
|     12 | SUI    | TIRINZONI S    | Double Take-out | ccw    |      50 |       0.36 |     0.27 |      0.22 |  -0.09 |   -0.05 |   -0.14 |      -1.31 |      -3.54 |
|     13 | SWE    | HASSELBORG A   | Guard           | ccw    |     100 |       0.22 |     0.3  |      0.27 |  -0.07 |    0.03 |   -0.04 |       0.43 |      -0.81 |
|     14 | SUI    | PAETZ A        | Double Take-out | ccw    |      50 |       0.27 |     0.22 |      0.04 |  -0.04 |   -0.19 |   -0.23 |      -4.08 |      -5.7  |
|     15 | SWE    | HASSELBORG A   | Guard           | ccw    |      25 |       0.04 |     0.07 |     -0.18 |  -0.03 |    0.25 |    0.22 |       4.4  |       4.47 |
|     16 | SUI    | PAETZ A        | Double Take-out | ccw    |      25 |      -0.18 |    -0.1  |     -0.42 |   0.08 |   -0.32 |   -0.24 |     -12.15 |      -9.85 |

### End 9: SUI hammer, down 2, 2 ends left; result SUI 2

|   shot | team   | player         | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SWE    | SCHARBACK S    | Front           | cw     |     100 |       0.5  |     0.56 |      0.51 |  -0.06 |    0.05 |   -0.01 |       0.52 |      -0.36 |
|      2 | SUI    | WITSCHONKE S   | Front           | ccw    |     100 |       0.51 |     0.58 |      0.48 |   0.07 |   -0.1  |   -0.03 |      -1.59 |      -0.5  |
|      3 | SWE    | SCHARBACK S    | Draw            | cw     |      75 |       0.48 |     0.53 |      0.43 |  -0.05 |    0.1  |    0.05 |       1.42 |       0.78 |
|      4 | SUI    | WITSCHONKE S   | Draw            | ccw    |     100 |       0.43 |     0.49 |      0.42 |   0.06 |   -0.07 |   -0.01 |      -0.83 |       0.03 |
|      5 | SWE    | KNOCHENHAUER A | Take-out        | ccw    |     100 |       0.42 |     0.42 |      0.25 |  -0.01 |    0.17 |    0.16 |       1.17 |       1.38 |
|      6 | SUI    | HOWALD C       | Draw            | ccw    |     100 |       0.25 |     0.32 |      0.25 |   0.07 |   -0.07 |   -0    |      -0.66 |       0.37 |
|      7 | SWE    | KNOCHENHAUER A | Take-out        | ccw    |     100 |       0.25 |     0.27 |      0.22 |  -0.02 |    0.04 |    0.03 |       1.4  |       1.3  |
|      8 | SUI    | HOWALD C       | Draw            | ccw    |     100 |       0.22 |     0.18 |      0.04 |  -0.04 |   -0.14 |   -0.19 |      -0.66 |      -0.54 |
|      9 | SWE    | McMANUS S      | Draw            | cw     |      75 |       0.04 |    -0.01 |     -0.01 |   0.05 |    0    |    0.05 |       0.5  |       0.38 |
|     10 | SUI    | TIRINZONI S    | Double Take-out | ccw    |      50 |      -0.01 |     0.04 |      0.57 |   0.05 |    0.53 |    0.58 |       3.98 |       4.44 |
|     11 | SWE    | McMANUS S      | Double Take-out | cw     |      50 |       0.57 |     0.49 |      0.46 |   0.08 |    0.03 |    0.11 |      -0.01 |       1.18 |
|     12 | SUI    | TIRINZONI S    | Hit and Roll    | ccw    |      75 |       0.46 |     0.62 |      0.57 |   0.16 |   -0.05 |    0.11 |      -0.59 |       1.35 |
|     13 | SWE    | HASSELBORG A   | Double Take-out | ccw    |      50 |       0.57 |     0.63 |      0.71 |  -0.06 |   -0.08 |   -0.14 |      -0.72 |      -0.4  |
|     14 | SUI    | PAETZ A        | Take-out        | cw     |     100 |       0.71 |     0.8  |      1.04 |   0.1  |    0.24 |    0.33 |       3.25 |       4.25 |
|     15 | SWE    | HASSELBORG A   | Hit and Roll    | cw     |      75 |       1.04 |     1.01 |      0.63 |   0.03 |    0.38 |    0.41 |       5.2  |       6.65 |
|     16 | SUI    | PAETZ A        | Raise           | ccw    |     100 |       0.63 |     0.9  |      1.42 |   0.26 |    0.52 |    0.78 |       5.51 |       8.46 |

### End 10: SWE hammer, tied, 1 ends left; result SWE 1

|   shot | team   | player         | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:---------------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | SUI    | WITSCHONKE S   | Front           | ccw    |     100 |       0.42 |     0.46 |      0.41 |  -0.04 |    0.05 |    0.01 |       4.7  |       1.33 |
|      2 | SWE    | SCHARBACK S    | Draw            | ccw    |       0 |       0.41 |     0.47 |      0.38 |   0.06 |   -0.09 |   -0.03 |      -5.56 |      -2.61 |
|      3 | SUI    | WITSCHONKE S   | Front           | ccw    |     100 |       0.38 |     0.42 |      0.37 |  -0.04 |    0.05 |    0.01 |       4.67 |      -0.13 |
|      4 | SWE    | SCHARBACK S    | Draw            | cw     |     100 |       0.37 |     0.43 |      0.5  |   0.06 |    0.06 |    0.12 |       0.55 |       3.82 |
|      5 | SUI    | HOWALD C       | Raise           | cw     |     100 |       0.5  |     0.44 |      0.37 |   0.05 |    0.07 |    0.12 |       8.01 |       6.5  |
|      6 | SWE    | KNOCHENHAUER A | Double Take-out | ccw    |     100 |       0.37 |     0.41 |      0.49 |   0.04 |    0.08 |    0.12 |       2.25 |       6.82 |
|      7 | SUI    | HOWALD C       | Front           | cw     |      75 |       0.49 |     0.61 |      0.59 |  -0.12 |    0.02 |   -0.1  |       5.87 |       0.11 |
|      8 | SWE    | KNOCHENHAUER A | Clearing        | cw     |     100 |       0.59 |     0.61 |      0.4  |   0.02 |   -0.21 |   -0.19 |     -11.05 |      -3.68 |
|      9 | SUI    | TIRINZONI S    | Front           | cw     |     100 |       0.4  |     0.6  |      0.47 |  -0.2  |    0.13 |   -0.07 |      11.02 |       1.92 |
|     10 | SWE    | McMANUS S      | Clearing        | ccw    |     100 |       0.47 |     0.53 |      0.49 |   0.06 |   -0.04 |    0.02 |      -1.47 |       9.88 |
|     11 | SUI    | TIRINZONI S    | Front           | ccw    |     100 |       0.49 |     0.59 |      0.59 |  -0.1  |   -0    |   -0.1  |       7.78 |       4.25 |
|     12 | SWE    | McMANUS S      | Clearing        | ccw    |     100 |       0.59 |     0.6  |      0.46 |   0.01 |   -0.14 |   -0.13 |      -4.13 |       4.47 |
|     13 | SUI    | PAETZ A        | Front           | ccw    |     100 |       0.46 |     0.6  |      0.67 |  -0.14 |   -0.07 |   -0.21 |       7.67 |       2.11 |
|     14 | SWE    | HASSELBORG A   | Clearing        | ccw    |     100 |       0.67 |     0.56 |      0.4  |  -0.11 |   -0.16 |   -0.27 |      -3.48 |       3.52 |
|     15 | SUI    | PAETZ A        | Freeze          | ccw    |      25 |       0.4  |     0.61 |      0.78 |  -0.21 |   -0.17 |   -0.38 |       1.85 |      -4.14 |
|     16 | SWE    | HASSELBORG A   | Take-out        | ccw    |     100 |       0.78 |     0.99 |      0.42 |   0.21 |   -0.57 |   -0.36 |       5.05 |      10.68 |
