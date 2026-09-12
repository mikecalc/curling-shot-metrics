# Milano Cortina 2026 Olympic Winter Games, Curling: Gold Medal Game, Great Britain v Canada (men)

2026-02-21 19:05; GBR red, CAN yellow. Final score GBR 6, CAN 9. Game key `OWG2026_ResultsBook|2026-02-21|19:05|Gold_Medal_Game|CAN-GBR`.

Every value is a difference of model outputs on the diagrammed positions (design Sections 2 and 10). `V before`, `V call` and `V after` are the hammer team's expected hammer-adjusted points before the shot, after the call (the field's usual result for this shot type from this position) and after the delivered stone. `call`, `throw` and `total` are from the thrower's view: `call` = V call - V before, `throw` = V after - V call, `total` = call + throw, signed so a gain for the thrower's team is positive. The `wp` columns are the same differences in win probability, in percentage points. Within an end the hammer team's totals minus the other team's totals sum exactly to the end's result minus `V before` on the first stone.

## Ends

`E[pts] start` is the hammer team's expected hammer-adjusted points at the start of the end and `result (adj)` the end's result in the same currency (H = 0.58: a score of k is worth k - H because the hammer passes, a steal of k is -k + H, a blank +H). The call and throw columns are each team's summed values over the end (thrower's view); the win-probability columns are GBR's, before the first stone and after the last.

|   end | hammer   | result       |   E[pts] start |   result (adj) |   GBR call |   GBR throw |   CAN call |   CAN throw |   WP GBR start |   WP GBR end |
|------:|:---------|:-------------|---------------:|---------------:|-----------:|------------:|-----------:|------------:|---------------:|-------------:|
|     1 | CAN      | CAN 1        |           0.69 |           0.42 |      -0.24 |        1.42 |       0.6  |        0.3  |           37.7 |         42.9 |
|     2 | GBR      | GBR 2        |           0.59 |           1.42 |       0.2  |        0.31 |      -0.25 |       -0.06 |           43.1 |         58.8 |
|     3 | CAN      | CAN 2        |           0.61 |           1.42 |      -0.06 |        1.48 |       1.04 |        1.19 |           57.6 |         44.5 |
|     4 | GBR      | GBR 1        |           0.6  |           0.42 |       0.37 |       -0.41 |      -0.33 |        0.46 |           43.5 |         40.1 |
|     5 | CAN      | CAN 1        |           0.68 |           0.42 |       0.27 |        0.64 |       0.18 |        0.47 |           38   |         43.9 |
|     6 | GBR      | GBR 2        |           0.61 |           1.42 |       0.6  |        0.6  |      -0.13 |        0.51 |           42.3 |         60.3 |
|     7 | CAN      | CAN 1        |           0.61 |           0.42 |       0.12 |        0.67 |      -0.02 |        0.62 |           59.4 |         67.3 |
|     8 | GBR      | GBR 1        |           0.67 |           0.42 |       0.02 |       -0.1  |      -0.04 |        0.2  |           66.8 |         63.4 |
|     9 | CAN      | CAN 3        |           0.6  |           2.42 |      -0.27 |       -0.48 |       0.26 |        0.82 |           64.7 |         16.6 |
|    10 | GBR      | CAN steals 1 |           0.47 |          -0.42 |       0.54 |       -0.97 |      -0.84 |        1.29 |           16.5 |          0   |

Conservation: max |sum of shot values - (result (adj) - E[pts] start)| over ends = 2.2e-16.

## Players

Sums over the game, thrower's view. `throw` is execution: the value of the delivered stone against the field's usual result for the call. `total` adds the call component. The official grade is the book's percentage.

| team   | player     |   shots |   call |   throw |   total |   throw wp |   total wp |   grade | worst throw              | best throw               |
|:-------|:-----------|--------:|-------:|--------:|--------:|-----------:|-----------:|--------:|:-------------------------|:-------------------------|
| GBR    | MOUAT B    |      20 |   2.19 |    3.24 |    5.44 |      62.4  |     104.27 |   80    | -0.70 (end 10, stone 16) | +0.70 (end 10, stone 14) |
| GBR    | HARDIE G   |      20 |   0.12 |   -0.04 |    0.08 |       4.69 |       8.19 |   86.25 | -0.24 (end 6, stone 12)  | +0.34 (end 1, stone 9)   |
| GBR    | LAMMIE B   |      20 |  -0.63 |    0.34 |   -0.3  |       4.98 |      -5.98 |   75    | -0.20 (end 10, stone 8)  | +0.28 (end 3, stone 7)   |
| GBR    | McMILLAN H |      20 |  -0.14 |   -0.39 |   -0.52 |      -2.4  |      -5.42 |   98.75 | -0.22 (end 10, stone 2)  | +0.07 (end 6, stone 4)   |
| CAN    | JACOBS B   |      20 |   0.14 |    5.05 |    5.2  |     102.14 |     103.33 |   83.75 | -0.57 (end 1, stone 14)  | +1.16 (end 10, stone 15) |
| CAN    | KENNEDY M  |      20 |  -0.08 |    0.75 |    0.67 |      15.91 |      15.99 |   92.5  | -0.17 (end 2, stone 11)  | +0.37 (end 3, stone 12)  |
| CAN    | GALLANT B  |      20 |   0.41 |    0.12 |    0.52 |       2.22 |      13.98 |   77.5  | -0.24 (end 3, stone 6)   | +0.25 (end 3, stone 8)   |
| CAN    | HEBERT B   |      20 |   0.02 |   -0.11 |   -0.1  |      -2.56 |      -0.45 |   97.5  | -0.08 (end 9, stone 4)   | +0.08 (end 10, stone 1)  |

## Largest swings

The ten shots that moved win probability most, either way.

|   end |   shot | team   | player   | type            | turn   |   grade |   call |   throw |   total |   throw wp |   total wp |
|------:|-------:|:-------|:---------|:----------------|:-------|--------:|-------:|--------:|--------:|-----------:|-----------:|
|    10 |     15 | CAN    | JACOBS B | Double Take-out | cw     |     100 |  -0.03 |    1.16 |    1.13 |      26.87 |      26.34 |
|     6 |     16 | GBR    | MOUAT B  | Double Take-out | cw     |     100 |   0.37 |    0.67 |    1.04 |      14.89 |      22.61 |
|     9 |     16 | CAN    | JACOBS B | Clearing        | cw     |     100 |  -0.21 |    0.81 |    0.6  |      22.68 |      16.98 |
|    10 |     14 | GBR    | MOUAT B  | Double Take-out | cw     |     100 |   0.09 |    0.7  |    0.79 |      13.47 |      15.84 |
|     4 |     16 | GBR    | MOUAT B  | Take-out        | cw     |     100 |   0.61 |    0.49 |    1.1  |       7.53 |      15.63 |
|     3 |     16 | CAN    | JACOBS B | Take-out        | ccw    |     100 |   0.41 |    0.41 |    0.81 |       6.97 |      13.85 |
|     1 |     16 | CAN    | JACOBS B | Draw            | ccw    |     100 |   0.06 |    0.73 |    0.79 |      11.94 |      12.79 |
|     3 |     15 | GBR    | MOUAT B  | Hit and Roll    | cw     |      75 |   0.11 |    0.58 |    0.69 |      10    |      12.1  |
|     3 |     14 | CAN    | JACOBS B | Take-out        | cw     |     100 |   0.24 |    0.43 |    0.67 |       7.45 |      11.36 |
|     5 |     14 | CAN    | JACOBS B | Double Take-out | ccw    |     100 |   0.19 |    0.36 |    0.55 |       6.34 |       9.59 |

## Shots

### End 1: CAN hammer, tied, 10 ends left; result CAN 1

|   shot | team   | player     | type               | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:-------------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | GBR    | McMILLAN H | Front              | cw     |     100 |       0.69 |     0.72 |      0.69 |  -0.03 |    0.03 |    0.01 |       0.65 |       0.36 |
|      2 | CAN    | HEBERT B   | Draw               | ccw    |     100 |       0.69 |     0.69 |      0.7  |   0    |    0.01 |    0.01 |       0.16 |       0.2  |
|      3 | GBR    | McMILLAN H | Draw               | cw     |     100 |       0.7  |     0.75 |      0.75 |  -0.05 |   -0    |   -0.05 |      -0.02 |      -0.82 |
|      4 | CAN    | HEBERT B   | Draw               | ccw    |     100 |       0.75 |     0.79 |      0.74 |   0.04 |   -0.05 |   -0.01 |      -0.81 |      -0.26 |
|      5 | GBR    | LAMMIE B   | Promotion Take-out | cw     |      75 |       0.74 |     0.82 |      0.71 |  -0.08 |    0.11 |    0.03 |       1.81 |       0.33 |
|      6 | CAN    | GALLANT B  | Take-out           | cw     |       0 |       0.71 |     0.79 |      0.7  |   0.08 |   -0.09 |   -0.01 |      -1.58 |      -0.25 |
|      7 | GBR    | LAMMIE B   | Take-out           | cw     |     100 |       0.7  |     0.61 |      0.45 |   0.09 |    0.16 |    0.26 |       2.64 |       3.98 |
|      8 | CAN    | GALLANT B  | Hit and Roll       | cw     |      75 |       0.45 |     0.5  |      0.63 |   0.06 |    0.13 |    0.18 |       2.14 |       2.95 |
|      9 | GBR    | HARDIE G   | Hit and Roll       | ccw    |     100 |       0.63 |     0.62 |      0.28 |   0.02 |    0.34 |    0.36 |       5.79 |       6.04 |
|     10 | CAN    | KENNEDY M  | Raise              | cw     |      75 |       0.28 |     0.36 |      0.5  |   0.09 |    0.14 |    0.22 |       2.15 |       3.47 |
|     11 | GBR    | HARDIE G   | Raise              | ccw    |      75 |       0.5  |     0.54 |      0.6  |  -0.05 |   -0.06 |   -0.11 |      -0.99 |      -1.68 |
|     12 | CAN    | KENNEDY M  | Raise              | cw     |     100 |       0.6  |     0.71 |      0.72 |   0.11 |    0    |    0.11 |       0.06 |       1.82 |
|     13 | GBR    | MOUAT B    | Promotion Take-out | ccw    |     100 |       0.72 |     0.75 |      0.29 |  -0.03 |    0.46 |    0.43 |       7.97 |       7.27 |
|     14 | CAN    | JACOBS B   | Raise              | cw     |       0 |       0.29 |     0.46 |     -0.12 |   0.17 |   -0.57 |   -0.4  |      -9.73 |      -6.79 |
|     15 | GBR    | MOUAT B    | Hit and Roll       | cw     |      75 |      -0.12 |     0    |     -0.37 |  -0.12 |    0.37 |    0.25 |       5.56 |       3.65 |
|     16 | CAN    | JACOBS B   | Draw               | ccw    |     100 |      -0.37 |    -0.31 |      0.42 |   0.06 |    0.73 |    0.79 |      11.94 |      12.79 |

### End 2: GBR hammer, down 1, 9 ends left; result GBR 2

|   shot | team   | player     | type               | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:-------------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | CAN    | HEBERT B   | Front              | ccw    |     100 |       0.59 |     0.62 |      0.59 |  -0.02 |    0.03 |    0    |       0.36 |      -0.03 |
|      2 | GBR    | McMILLAN H | Front              | cw     |     100 |       0.59 |     0.58 |      0.58 |  -0.01 |    0    |   -0.01 |       0.19 |       0.02 |
|      3 | CAN    | HEBERT B   | Draw               | cw     |     100 |       0.58 |     0.59 |      0.6  |  -0    |   -0.01 |   -0.02 |      -0.29 |      -0.27 |
|      4 | GBR    | McMILLAN H | Draw               | cw     |     100 |       0.6  |     0.64 |      0.6  |   0.04 |   -0.04 |   -0.01 |      -0.74 |      -0.06 |
|      5 | CAN    | GALLANT B  | Raise              | cw     |       0 |       0.6  |     0.69 |      0.66 |  -0.09 |    0.03 |   -0.06 |       0.41 |      -1.19 |
|      6 | GBR    | LAMMIE B   | Double Take-out    | cw     |     100 |       0.66 |     0.6  |      0.6  |  -0.06 |   -0    |   -0.06 |       0.03 |      -1.19 |
|      7 | CAN    | GALLANT B  | Hit and Roll       | ccw    |      75 |       0.6  |     0.64 |      0.54 |  -0.04 |    0.1  |    0.06 |       1.68 |       1.14 |
|      8 | GBR    | LAMMIE B   | Hit and Roll       | ccw    |      75 |       0.54 |     0.57 |      0.59 |   0.03 |    0.02 |    0.05 |       0.46 |       0.92 |
|      9 | CAN    | KENNEDY M  | Take-out           | cw     |     100 |       0.59 |     0.53 |      0.47 |   0.06 |    0.07 |    0.12 |       1    |       2.17 |
|     10 | GBR    | HARDIE G   | Hit and Roll       | cw     |     100 |       0.47 |     0.55 |      0.76 |   0.09 |    0.21 |    0.3  |       3.71 |       5.05 |
|     11 | CAN    | KENNEDY M  | Double Take-out    | ccw    |      50 |       0.76 |     0.87 |      1.03 |  -0.1  |   -0.17 |   -0.27 |      -3.25 |      -5.07 |
|     12 | GBR    | HARDIE G   | Draw               | ccw    |     100 |       1.03 |     1.07 |      1.05 |   0.04 |   -0.02 |    0.02 |      -0.36 |       0.41 |
|     13 | CAN    | JACOBS B   | Promotion Take-out | ccw    |      50 |       1.05 |     1.15 |      1.05 |  -0.1  |    0.1  |    0    |       1.72 |      -0.03 |
|     14 | GBR    | MOUAT B    | Draw               | cw     |     100 |       1.05 |     1.12 |      1.18 |   0.06 |    0.07 |    0.13 |       1.07 |       2.4  |
|     15 | CAN    | JACOBS B   | Clearing           | cw     |     100 |       1.18 |     1.13 |      1.34 |   0.05 |   -0.21 |   -0.15 |      -4.24 |      -3.26 |
|     16 | GBR    | MOUAT B    | Draw               | cw     |     100 |       1.34 |     1.35 |      1.42 |   0.01 |    0.07 |    0.08 |       1.41 |       1.61 |

### End 3: CAN hammer, down 1, 8 ends left; result CAN 2

|   shot | team   | player     | type         | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:-------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | GBR    | McMILLAN H | Front        | cw     |     100 |       0.61 |     0.65 |      0.61 |  -0.04 |    0.04 |   -0    |       0.5  |      -0.01 |
|      2 | CAN    | HEBERT B   | Front        | ccw    |     100 |       0.61 |     0.62 |      0.58 |   0.01 |   -0.04 |   -0.03 |      -0.62 |      -0.6  |
|      3 | GBR    | McMILLAN H | Draw         | ccw    |     100 |       0.58 |     0.6  |      0.59 |  -0.02 |    0.01 |   -0.02 |       0.09 |      -0.27 |
|      4 | CAN    | HEBERT B   | Draw         | ccw    |     100 |       0.59 |     0.65 |      0.59 |   0.06 |   -0.06 |   -0    |      -0.84 |      -0.05 |
|      5 | GBR    | LAMMIE B   | Draw         | cw     |       0 |       0.59 |     0.61 |      0.55 |  -0.02 |    0.06 |    0.04 |       0.73 |       0.58 |
|      6 | CAN    | GALLANT B  | Draw         | ccw    |       0 |       0.55 |     0.6  |      0.36 |   0.05 |   -0.24 |   -0.19 |      -3.71 |      -3.09 |
|      7 | GBR    | LAMMIE B   | Draw         | ccw    |     100 |       0.36 |     0.46 |      0.18 |  -0.1  |    0.28 |    0.18 |       4.27 |       2.78 |
|      8 | CAN    | GALLANT B  | Clearing     | ccw    |     100 |       0.18 |     0.23 |      0.48 |   0.04 |    0.25 |    0.3  |       4.07 |       4.56 |
|      9 | GBR    | HARDIE G   | Guard        | ccw    |     100 |       0.48 |     0.45 |      0.49 |   0.03 |   -0.04 |   -0.01 |      -0.62 |      -0.03 |
|     10 | CAN    | KENNEDY M  | Take-out     | cw     |     100 |       0.49 |     0.54 |      0.6  |   0.05 |    0.06 |    0.11 |       1    |       1.79 |
|     11 | GBR    | HARDIE G   | Hit and Roll | cw     |       0 |       0.6  |     0.66 |      0.59 |  -0.06 |    0.06 |    0    |       0.97 |       0.02 |
|     12 | CAN    | KENNEDY M  | Take-out     | cw     |     100 |       0.59 |     0.79 |      1.16 |   0.2  |    0.37 |    0.57 |       6.24 |       9.54 |
|     13 | GBR    | MOUAT B    | Take-out     | cw     |     100 |       1.16 |     1.12 |      0.63 |   0.04 |    0.5  |    0.54 |       8.33 |       9.09 |
|     14 | CAN    | JACOBS B   | Take-out     | cw     |     100 |       0.63 |     0.87 |      1.3  |   0.24 |    0.43 |    0.67 |       7.45 |      11.36 |
|     15 | GBR    | MOUAT B    | Hit and Roll | cw     |      75 |       1.3  |     1.18 |      0.6  |   0.11 |    0.58 |    0.69 |      10    |      12.1  |
|     16 | CAN    | JACOBS B   | Take-out     | ccw    |     100 |       0.6  |     1.01 |      1.42 |   0.41 |    0.41 |    0.81 |       6.97 |      13.85 |

### End 4: GBR hammer, down 1, 7 ends left; result GBR 1

|   shot | team   | player     | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | CAN    | HEBERT B   | Front           | cw     |     100 |       0.6  |     0.63 |      0.61 |  -0.03 |    0.02 |   -0.02 |       0.28 |      -0.32 |
|      2 | GBR    | McMILLAN H | Front           | cw     |     100 |       0.61 |     0.62 |      0.59 |   0    |   -0.03 |   -0.03 |      -0.48 |      -0.4  |
|      3 | CAN    | HEBERT B   | Front           | ccw    |     100 |       0.59 |     0.61 |      0.6  |  -0.03 |    0.01 |   -0.01 |       0.21 |      -0.18 |
|      4 | GBR    | McMILLAN H | Front           | ccw    |     100 |       0.6  |     0.62 |      0.51 |   0.02 |   -0.11 |   -0.1  |      -1.92 |      -1.61 |
|      5 | CAN    | GALLANT B  | Draw            | ccw    |     100 |       0.51 |     0.55 |      0.52 |  -0.04 |    0.02 |   -0.02 |       0.37 |      -0.31 |
|      6 | GBR    | LAMMIE B   | Clearing        | ccw    |     100 |       0.52 |     0.47 |      0.47 |  -0.05 |    0    |   -0.05 |       0.23 |      -0.92 |
|      7 | CAN    | GALLANT B  | Guard           | ccw    |     100 |       0.47 |     0.5  |      0.49 |  -0.02 |    0    |   -0.02 |       0.06 |      -0.3  |
|      8 | GBR    | LAMMIE B   | Clearing        | ccw    |     100 |       0.49 |     0.44 |      0.41 |  -0.05 |   -0.03 |   -0.08 |      -0.28 |      -1.44 |
|      9 | CAN    | KENNEDY M  | Guard           | ccw    |     100 |       0.41 |     0.42 |      0.43 |  -0.01 |   -0.02 |   -0.02 |      -0.3  |      -0.35 |
|     10 | GBR    | HARDIE G   | Clearing        | cw     |     100 |       0.43 |     0.38 |      0.31 |  -0.05 |   -0.07 |   -0.12 |      -1.02 |      -2.14 |
|     11 | CAN    | KENNEDY M  | Guard           | ccw    |     100 |       0.31 |     0.34 |      0.37 |  -0.03 |   -0.03 |   -0.06 |      -0.52 |      -0.87 |
|     12 | GBR    | HARDIE G   | Double Take-out | cw     |     100 |       0.37 |     0.35 |      0.22 |  -0.02 |   -0.13 |   -0.15 |      -1.87 |      -2.4  |
|     13 | CAN    | JACOBS B   | Raise           | cw     |     100 |       0.22 |     0.34 |      0.17 |  -0.12 |    0.17 |    0.05 |       2.69 |       0.65 |
|     14 | GBR    | MOUAT B    | Raise           | cw     |       0 |       0.17 |     0.08 |     -0.45 |  -0.08 |   -0.53 |   -0.62 |      -7.72 |      -8.94 |
|     15 | CAN    | JACOBS B   | Draw            | ccw    |      50 |      -0.45 |    -0.4  |     -0.68 |  -0.05 |    0.28 |    0.23 |       3.71 |       2.88 |
|     16 | GBR    | MOUAT B    | Take-out        | cw     |     100 |      -0.68 |    -0.07 |      0.42 |   0.61 |    0.49 |    1.1  |       7.53 |      15.63 |

### End 5: CAN hammer, tied, 6 ends left; result CAN 1

|   shot | team   | player     | type               | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:-------------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | GBR    | McMILLAN H | Front              | cw     |     100 |       0.68 |     0.71 |      0.71 |  -0.03 |   -0    |   -0.03 |       0.03 |      -0.42 |
|      2 | CAN    | HEBERT B   | Draw               | ccw    |     100 |       0.71 |     0.73 |      0.73 |   0.02 |   -0.01 |    0.02 |      -0.06 |       0.32 |
|      3 | GBR    | McMILLAN H | Draw               | cw     |      75 |       0.73 |     0.78 |      0.79 |  -0.06 |   -0.01 |   -0.07 |      -0.16 |      -1.12 |
|      4 | CAN    | HEBERT B   | Draw               | ccw    |     100 |       0.79 |     0.83 |      0.78 |   0.04 |   -0.05 |   -0.01 |      -0.85 |      -0.3  |
|      5 | GBR    | LAMMIE B   | Promotion Take-out | cw     |      75 |       0.78 |     0.81 |      0.83 |  -0.03 |   -0.01 |   -0.04 |      -0.05 |      -0.75 |
|      6 | CAN    | GALLANT B  | Raise              | ccw    |      50 |       0.83 |     0.87 |      0.93 |   0.04 |    0.06 |    0.1  |       0.94 |       1.5  |
|      7 | GBR    | LAMMIE B   | Take-out           | ccw    |     100 |       0.93 |     0.89 |      0.75 |   0.04 |    0.14 |    0.18 |       2.46 |       3.08 |
|      8 | CAN    | GALLANT B  | Raise              | ccw    |      50 |       0.75 |     0.84 |      0.67 |   0.1  |   -0.17 |   -0.08 |      -2.92 |      -1.41 |
|      9 | GBR    | HARDIE G   | Hit and Roll       | cw     |     100 |       0.67 |     0.68 |      0.53 |  -0.01 |    0.15 |    0.14 |       2.57 |       2.43 |
|     10 | CAN    | KENNEDY M  | Clearing           | cw     |     100 |       0.53 |     0.39 |      0.35 |  -0.15 |   -0.03 |   -0.18 |      -0.33 |      -2.83 |
|     11 | GBR    | HARDIE G   | Guard              | ccw    |     100 |       0.35 |     0.35 |      0.49 |   0.01 |   -0.14 |   -0.13 |      -2.3  |      -2.12 |
|     12 | CAN    | KENNEDY M  | Double Take-out    | ccw    |     100 |       0.49 |     0.35 |      0.6  |  -0.14 |    0.25 |    0.11 |       4.19 |       1.9  |
|     13 | GBR    | MOUAT B    | Hit and Roll       | cw     |     100 |       0.6  |     0.43 |      0.05 |   0.17 |    0.38 |    0.55 |       6.51 |       9.46 |
|     14 | CAN    | JACOBS B   | Double Take-out    | ccw    |     100 |       0.05 |     0.24 |      0.6  |   0.19 |    0.36 |    0.55 |       6.34 |       9.59 |
|     15 | GBR    | MOUAT B    | Take-out           | ccw    |     100 |       0.6  |     0.42 |      0.28 |   0.18 |    0.14 |    0.32 |       2.85 |       6.17 |
|     16 | CAN    | JACOBS B   | Clearing           | ccw    |      50 |       0.28 |     0.35 |      0.42 |   0.08 |    0.06 |    0.14 |      -1.07 |       2.03 |

### End 6: GBR hammer, down 1, 5 ends left; result GBR 2

|   shot | team   | player     | type                | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:--------------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | CAN    | HEBERT B   | Front               | ccw    |      75 |       0.61 |     0.63 |      0.63 |  -0.02 |   -0.01 |   -0.03 |      -0.15 |      -0.54 |
|      2 | GBR    | McMILLAN H | Front               | ccw    |     100 |       0.63 |     0.62 |      0.62 |  -0.01 |   -0    |   -0.02 |      -0.03 |      -0.19 |
|      3 | CAN    | HEBERT B   | Front               | ccw    |      75 |       0.62 |     0.63 |      0.63 |  -0.01 |   -0    |   -0.01 |      -0.01 |      -0.15 |
|      4 | GBR    | McMILLAN H | Wick / Soft Peeling | cw     |     100 |       0.63 |     0.59 |      0.66 |  -0.04 |    0.07 |    0.03 |       1.66 |       0.64 |
|      5 | CAN    | GALLANT B  | Hit and Roll        | ccw    |     100 |       0.66 |     0.6  |      0.61 |   0.06 |   -0.01 |    0.05 |      -0.33 |       1.03 |
|      6 | GBR    | LAMMIE B   | Wick / Soft Peeling | cw     |     100 |       0.61 |     0.61 |      0.61 |  -0    |    0    |    0    |       0.05 |      -0.04 |
|      7 | CAN    | GALLANT B  | Take-out            | ccw    |     100 |       0.61 |     0.59 |      0.51 |   0.02 |    0.08 |    0.1  |       1.59 |       1.92 |
|      8 | GBR    | LAMMIE B   | Draw                | cw     |     100 |       0.51 |     0.5  |      0.56 |  -0.01 |    0.06 |    0.05 |       1.09 |       1.05 |
|      9 | CAN    | KENNEDY M  | Clearing            | cw     |     100 |       0.56 |     0.56 |      0.47 |  -0    |    0.09 |    0.09 |       1.65 |       1.76 |
|     10 | GBR    | HARDIE G   | Draw                | cw     |     100 |       0.47 |     0.44 |      0.51 |  -0.03 |    0.07 |    0.04 |       1.16 |       0.66 |
|     11 | CAN    | KENNEDY M  | Draw                | cw     |     100 |       0.51 |     0.54 |      0.64 |  -0.03 |   -0.1  |   -0.14 |      -2.12 |      -2.85 |
|     12 | GBR    | HARDIE G   | Wick / Soft Peeling | cw     |      75 |       0.64 |     0.73 |      0.48 |   0.08 |   -0.24 |   -0.16 |      -4.74 |      -3.11 |
|     13 | CAN    | JACOBS B   | Draw                | cw     |      75 |       0.48 |     0.51 |      0.38 |  -0.03 |    0.13 |    0.11 |       1.96 |       1.5  |
|     14 | GBR    | MOUAT B    | Double Take-out     | cw     |     100 |       0.38 |     0.62 |      0.6  |   0.25 |   -0.03 |    0.22 |      -0.92 |       3.44 |
|     15 | CAN    | JACOBS B   | Take-out            | ccw    |     100 |       0.6  |     0.71 |      0.38 |  -0.11 |    0.33 |    0.22 |       6.75 |       4.36 |
|     16 | GBR    | MOUAT B    | Double Take-out     | cw     |     100 |       0.38 |     0.75 |      1.42 |   0.37 |    0.67 |    1.04 |      14.89 |      22.61 |

### End 7: CAN hammer, down 1, 4 ends left; result CAN 1

|   shot | team   | player     | type               | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:-------------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | GBR    | McMILLAN H | Front              | cw     |     100 |       0.61 |     0.63 |      0.62 |  -0.03 |    0.02 |   -0.01 |       0.38 |      -0.11 |
|      2 | CAN    | HEBERT B   | Front              | ccw    |     100 |       0.62 |     0.6  |      0.6  |  -0.01 |   -0.01 |   -0.02 |      -0.08 |      -0.32 |
|      3 | GBR    | McMILLAN H | Draw               | ccw    |     100 |       0.6  |     0.59 |      0.59 |   0.01 |    0    |    0.01 |       0.06 |       0.17 |
|      4 | CAN    | HEBERT B   | Draw               | ccw    |     100 |       0.59 |     0.6  |      0.59 |   0.02 |   -0.02 |   -0    |      -0.36 |      -0.07 |
|      5 | GBR    | LAMMIE B   | Draw               | cw     |     100 |       0.59 |     0.59 |      0.62 |  -0.01 |   -0.02 |   -0.03 |      -0.52 |      -0.58 |
|      6 | CAN    | GALLANT B  | Draw               | ccw    |     100 |       0.62 |     0.62 |      0.56 |   0    |   -0.06 |   -0.06 |      -1.27 |      -1.16 |
|      7 | GBR    | LAMMIE B   | Double Take-out    | cw     |     100 |       0.56 |     0.69 |      0.47 |  -0.13 |    0.22 |    0.09 |       4.58 |       1.82 |
|      8 | CAN    | GALLANT B  | Double Take-out    | cw     |     100 |       0.47 |     0.5  |      0.65 |   0.03 |    0.15 |    0.18 |       3.14 |       3.74 |
|      9 | GBR    | HARDIE G   | Take-out           | cw     |     100 |       0.65 |     0.58 |      0.56 |   0.07 |    0.02 |    0.09 |       0.49 |       2.16 |
|     10 | CAN    | KENNEDY M  | Take-out           | cw     |     100 |       0.56 |     0.59 |      0.49 |   0.04 |   -0.1  |   -0.06 |      -2.12 |      -1.46 |
|     11 | GBR    | HARDIE G   | Draw               | ccw    |     100 |       0.49 |     0.49 |      0.43 |   0    |    0.06 |    0.06 |       1.11 |       1.25 |
|     12 | CAN    | KENNEDY M  | Double Take-out    | ccw    |      50 |       0.43 |     0.41 |      0.37 |  -0.02 |   -0.04 |   -0.06 |      -1.11 |      -1.71 |
|     13 | GBR    | MOUAT B    | Draw               | ccw    |     100 |       0.37 |     0.36 |      0.18 |   0.01 |    0.18 |    0.19 |       3.38 |       3.52 |
|     14 | CAN    | JACOBS B   | Promotion Take-out | cw     |     100 |       0.18 |     0.09 |      0.61 |  -0.09 |    0.51 |    0.42 |       9.98 |       8.1  |
|     15 | GBR    | MOUAT B    | Take-out           | cw     |     100 |       0.61 |     0.42 |      0.22 |   0.19 |    0.2  |    0.39 |       4.69 |       9.28 |
|     16 | CAN    | JACOBS B   | Draw               | ccw    |     100 |       0.22 |     0.24 |      0.42 |   0.02 |    0.18 |    0.2  |       2.19 |       2.47 |

### End 8: GBR hammer, tied, 3 ends left; result GBR 1

|   shot | team   | player     | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | CAN    | HEBERT B   | Front           | ccw    |     100 |       0.67 |     0.69 |      0.69 |  -0.02 |   -0    |   -0.02 |       0.03 |      -0.44 |
|      2 | GBR    | McMILLAN H | Front           | ccw    |     100 |       0.69 |     0.7  |      0.67 |   0    |   -0.03 |   -0.02 |      -0.8  |      -0.65 |
|      3 | CAN    | HEBERT B   | Front           | ccw    |     100 |       0.67 |     0.69 |      0.67 |  -0.02 |    0.03 |    0    |       0.69 |       0.08 |
|      4 | GBR    | McMILLAN H | Draw            | ccw    |     100 |       0.67 |     0.7  |      0.69 |   0.03 |   -0.01 |    0.02 |      -0.29 |       0.26 |
|      5 | CAN    | GALLANT B  | Take-out        | ccw    |     100 |       0.69 |     0.57 |      0.58 |   0.12 |   -0.02 |    0.1  |       0.01 |       2.25 |
|      6 | GBR    | LAMMIE B   | Clearing        | cw     |      25 |       0.58 |     0.53 |      0.51 |  -0.06 |   -0.02 |   -0.07 |      -0.71 |      -1.56 |
|      7 | CAN    | GALLANT B  | Front           | ccw    |     100 |       0.51 |     0.51 |      0.57 |  -0    |   -0.05 |   -0.05 |      -1    |      -1.22 |
|      8 | GBR    | LAMMIE B   | Raise           | cw     |      25 |       0.57 |     0.5  |      0.41 |  -0.07 |   -0.09 |   -0.16 |      -2.09 |      -3.53 |
|      9 | CAN    | KENNEDY M  | Guard           | ccw    |     100 |       0.41 |     0.39 |      0.38 |   0.02 |    0.01 |    0.03 |       0.62 |       0.96 |
|     10 | GBR    | HARDIE G   | Double Take-out | cw     |     100 |       0.38 |     0.31 |      0.48 |  -0.06 |    0.16 |    0.1  |       4.84 |       3.49 |
|     11 | CAN    | KENNEDY M  | Front           | cw     |     100 |       0.48 |     0.46 |      0.5  |   0.01 |   -0.04 |   -0.02 |      -0.66 |      -0.27 |
|     12 | GBR    | HARDIE G   | Hit and Roll    | cw     |      50 |       0.5  |     0.48 |      0.37 |  -0.02 |   -0.12 |   -0.13 |      -2.3  |      -2.68 |
|     13 | CAN    | JACOBS B   | Draw            | ccw    |      75 |       0.37 |     0.4  |      0.35 |  -0.03 |    0.05 |    0.02 |       0.88 |      -0    |
|     14 | GBR    | MOUAT B    | Hit and Roll    | ccw    |      75 |       0.35 |     0.45 |      0.36 |   0.09 |   -0.08 |    0.01 |      -2.36 |      -0.15 |
|     15 | CAN    | JACOBS B   | Take-out        | ccw    |     100 |       0.36 |     0.48 |      0.25 |  -0.11 |    0.23 |    0.11 |       5.37 |       2.14 |
|     16 | GBR    | MOUAT B    | Take-out        | cw     |     100 |       0.25 |     0.34 |      0.42 |   0.09 |    0.07 |    0.17 |       2.35 |       4.92 |

### End 9: CAN hammer, down 1, 2 ends left; result CAN 3

|   shot | team   | player     | type               | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:-------------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | GBR    | McMILLAN H | Front              | cw     |     100 |       0.6  |     0.64 |      0.61 |  -0.04 |    0.03 |   -0.01 |       0.73 |      -0.19 |
|      2 | CAN    | HEBERT B   | Draw               | ccw    |     100 |       0.61 |     0.64 |      0.65 |   0.03 |    0.01 |    0.04 |       0.25 |       1.08 |
|      3 | GBR    | McMILLAN H | Draw               | cw     |     100 |       0.65 |     0.69 |      0.68 |  -0.04 |    0.01 |   -0.03 |       0.17 |      -0.75 |
|      4 | CAN    | HEBERT B   | Draw               | ccw    |     100 |       0.68 |     0.74 |      0.67 |   0.06 |   -0.08 |   -0.02 |      -1.74 |      -0.22 |
|      5 | GBR    | LAMMIE B   | Raise              | cw     |       0 |       0.67 |     0.79 |      0.91 |  -0.12 |   -0.12 |   -0.24 |      -2.75 |      -5.31 |
|      6 | CAN    | GALLANT B  | Take-out           | ccw    |     100 |       0.91 |     0.99 |      0.83 |   0.08 |   -0.16 |   -0.08 |      -4.08 |      -1.77 |
|      7 | GBR    | LAMMIE B   | Double Take-out    | cw     |      50 |       0.83 |     0.9  |      0.97 |  -0.07 |   -0.08 |   -0.15 |      -1.75 |      -3.82 |
|      8 | CAN    | GALLANT B  | Promotion Take-out | ccw    |     100 |       0.97 |     1.11 |      1.15 |   0.13 |    0.04 |    0.18 |       1.11 |       5.07 |
|      9 | GBR    | HARDIE G   | Hit and Roll       | ccw    |     100 |       1.15 |     1.17 |      1.06 |  -0.02 |    0.11 |    0.09 |       3.55 |       2.98 |
|     10 | CAN    | KENNEDY M  | Hit and Roll       | ccw    |     100 |       1.06 |     1.23 |      1.24 |   0.17 |    0.01 |    0.18 |       0.6  |       5.36 |
|     11 | GBR    | HARDIE G   | Double Take-out    | cw     |      50 |       1.24 |     1.15 |      1.28 |   0.1  |   -0.13 |   -0.03 |      -2.81 |      -0.48 |
|     12 | CAN    | KENNEDY M  | Hit and Roll       | cw     |     100 |       1.28 |     1.23 |      1.42 |  -0.05 |    0.19 |    0.14 |       5.4  |       4.09 |
|     13 | GBR    | MOUAT B    | Double Take-out    | ccw    |      50 |       1.42 |     1.37 |      1.61 |   0.05 |   -0.24 |   -0.19 |      -6.55 |      -5.06 |
|     14 | CAN    | JACOBS B   | Draw               | ccw    |      75 |       1.61 |     1.66 |      1.64 |   0.05 |   -0.02 |    0.03 |      -0.45 |       0.44 |
|     15 | GBR    | MOUAT B    | Freeze             | ccw    |      25 |       1.64 |     1.77 |      1.82 |  -0.13 |   -0.05 |   -0.18 |      -1.24 |      -4.46 |
|     16 | CAN    | JACOBS B   | Clearing           | cw     |     100 |       1.82 |     1.6  |      2.42 |  -0.21 |    0.81 |    0.6  |      22.68 |      16.98 |

### End 10: GBR hammer, down 2, 1 ends left; result CAN steals 1

|   shot | team   | player     | type            | turn   |   grade |   V before |   V call |   V after |   call |   throw |   total |   throw wp |   total wp |
|-------:|:-------|:-----------|:----------------|:-------|--------:|-----------:|---------:|----------:|-------:|--------:|--------:|-----------:|-----------:|
|      1 | CAN    | HEBERT B   | Draw            | ccw    |     100 |       0.47 |     0.52 |      0.44 |  -0.06 |    0.08 |    0.03 |       1    |       0.83 |
|      2 | GBR    | McMILLAN H | Front           | cw     |     100 |       0.44 |     0.52 |      0.3  |   0.08 |   -0.22 |   -0.14 |      -1.51 |      -0.79 |
|      3 | CAN    | HEBERT B   | Draw            | ccw    |     100 |       0.3  |     0.32 |      0.29 |  -0.02 |    0.03 |    0    |       0.28 |       0.78 |
|      4 | GBR    | McMILLAN H | Front           | cw     |     100 |       0.29 |     0.38 |      0.25 |   0.08 |   -0.13 |   -0.05 |      -0.89 |       0.52 |
|      5 | CAN    | GALLANT B  | Draw            | ccw    |     100 |       0.25 |     0.25 |      0.27 |   0    |   -0.02 |   -0.02 |       1.39 |       1.92 |
|      6 | GBR    | LAMMIE B   | Raise           | cw     |     100 |       0.27 |     0.26 |      0.11 |  -0    |   -0.15 |   -0.15 |      -2.25 |      -0.64 |
|      7 | CAN    | GALLANT B  | Clearing        | cw     |     100 |       0.11 |     0.32 |      0.27 |  -0.21 |    0.06 |   -0.15 |       0.21 |      -1.44 |
|      8 | GBR    | LAMMIE B   | Draw            | ccw    |      75 |       0.27 |     0.32 |      0.13 |   0.06 |   -0.2  |   -0.14 |      -2.96 |      -0.77 |
|      9 | CAN    | KENNEDY M  | Clearing        | cw     |     100 |       0.13 |     0.35 |      0.37 |  -0.22 |   -0.01 |   -0.24 |       1.01 |      -1.84 |
|     10 | GBR    | HARDIE G   | Draw            | ccw    |     100 |       0.37 |     0.38 |      0.18 |   0.01 |   -0.2  |   -0.18 |      -2.68 |      -3.07 |
|     11 | CAN    | KENNEDY M  | Raise           | cw     |      75 |       0.18 |     0.25 |      0.15 |  -0.07 |    0.1  |    0.03 |       2.4  |       0.36 |
|     12 | GBR    | HARDIE G   | Raise           | ccw    |      75 |       0.15 |     0.15 |      0.07 |  -0    |   -0.08 |   -0.08 |       0.19 |       1.41 |
|     13 | CAN    | JACOBS B   | Double Take-out | ccw    |     100 |       0.07 |     0.3  |      0.39 |  -0.23 |   -0.1  |   -0.33 |       0.12 |      -2.06 |
|     14 | GBR    | MOUAT B    | Double Take-out | cw     |     100 |       0.39 |     0.48 |      1.18 |   0.09 |    0.7  |    0.79 |      13.47 |      15.84 |
|     15 | CAN    | JACOBS B   | Double Take-out | cw     |     100 |       1.18 |     1.21 |      0.05 |  -0.03 |    1.16 |    1.13 |      26.87 |      26.34 |
|     16 | GBR    | MOUAT B    | Double Take-out | cw     |       0 |       0.05 |     0.28 |     -0.42 |   0.22 |   -0.7  |   -0.47 |      -8.8  |      -4.1  |
