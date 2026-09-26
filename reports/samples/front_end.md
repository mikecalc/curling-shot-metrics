# Front end: what early-end execution values measure

596,002 shots with a post-shot position. Execution is `pg_throw` relative to the event's field for the same shot type and hammer state. Grades appear only as a check; they are never a model input.

## Measurement by position

`repeatability`: Spearman between a player's mean execution in their odd and even games at an event (40+ shots in each half). `grade_agreement_player`: Spearman between a player-event's mean execution and mean grade (80+ shots). `grade_agreement_shot`: Spearman between a shot's execution and its grade. `opponent_same_game`: Spearman between the two teams' mean execution at the position in the same game, and the same for grades.

| position   |   shots |   player_events |   repeatability |   repeatability_wp |   grade_repeatability |   grade_agreement_player |   grade_agreement_shot |   opponent_same_game |   opponent_same_game_grade |
|:-----------|--------:|----------------:|----------------:|-------------------:|----------------------:|-------------------------:|-----------------------:|---------------------:|---------------------------:|
| Lead       |  148584 |             718 |           0.684 |              0.649 |                 0.617 |                   -0.1   |                  0.207 |                0.153 |                      0.212 |
| Second     |  149167 |             731 |           0.527 |              0.465 |                 0.68  |                    0.155 |                  0.348 |                0.208 |                      0.053 |
| Third      |  149031 |             740 |           0.323 |              0.304 |                 0.643 |                    0.466 |                  0.413 |                0.148 |                      0.001 |
| Fourth     |  149220 |             750 |           0.474 |              0.456 |                 0.641 |                    0.814 |                  0.578 |                0.069 |                     -0.19  |

Team-event correlation of mean execution between positions (a shared component that is not the player's):

|        |   Lead |   Second |   Third |   Fourth |
|:-------|-------:|---------:|--------:|---------:|
| Lead   |   1    |     0.59 |    0.31 |    -0.01 |
| Second |   0.59 |     1    |    0.34 |    -0.03 |
| Third  |   0.31 |     0.34 |    1    |     0.24 |
| Fourth |  -0.01 |    -0.03 |    0.24 |     1    |

Spread of execution per stone (points, and percentage points of win probability), agreement with the grade, and `next_stone`, the correlation with the next stone's execution in the same end (negative: the see-saw of a mispriced position):

|   shot |    sd |   sd_wp_pp |   mean_abs |   grade_agreement |   next_stone |
|-------:|------:|-----------:|-----------:|------------------:|-------------:|
|      1 | 0.021 |      0.374 |      0.018 |             0.167 |       -0.089 |
|      2 | 0.031 |      0.514 |      0.024 |             0.11  |       -0.069 |
|      3 | 0.052 |      0.783 |      0.039 |             0.257 |        0.097 |
|      4 | 0.06  |      0.893 |      0.045 |             0.302 |       -0.043 |
|      5 | 0.081 |      1.265 |      0.06  |             0.375 |        0.163 |
|      6 | 0.092 |      1.359 |      0.068 |             0.328 |        0.109 |
|      7 | 0.103 |      1.586 |      0.074 |             0.312 |        0.071 |
|      8 | 0.118 |      1.777 |      0.087 |             0.391 |       -0.005 |
|      9 | 0.149 |      2.241 |      0.11  |             0.394 |        0.15  |
|     10 | 0.175 |      2.62  |      0.128 |             0.414 |        0.148 |
|     11 | 0.192 |      2.906 |      0.145 |             0.392 |        0.144 |
|     12 | 0.211 |      3.148 |      0.155 |             0.459 |        0.043 |
|     13 | 0.269 |      4.085 |      0.201 |             0.47  |        0.131 |
|     14 | 0.305 |      4.659 |      0.225 |             0.52  |        0.099 |
|     15 | 0.378 |      6.05  |      0.276 |             0.505 |        0.003 |
|     16 | 0.645 |     10.706 |      0.451 |             0.723 |      nan     |

## Style check (leads and seconds)

Team-event mean execution regressed on the team's mix of calls and pre-shot configurations at that position.

- r2_lead: 0.369
- team_events_lead: 749
- r2_second: 0.379
- team_events_second: 750
- lead_second_raw: 0.667
- lead_second_residual: 0.380

## Configuration calibration

For each configuration before the shot and band of rocks remaining: the model's value of the position (`model_v`, hammer-adjusted points, hammer team's view) against the realised value of the end (`real_v`), and the same in win probability (percent). A configuration the field converts better than the model expects has a positive gap.

| configuration         | rocks_left   |     n |   model_v |   real_v |    gap |   model_wp |   real_wp |   gap_wp_pp |
|:----------------------|:-------------|------:|----------:|---------:|-------:|-----------:|----------:|------------:|
| empty                 | 16-13        | 37619 |     0.587 |    0.582 | -0.006 |     47.204 |    47.26  |       0.057 |
| guards_only           | 16-13        | 29832 |     0.632 |    0.612 | -0.02  |     60.93  |    60.778 |      -0.151 |
| guards_only           | 12-9         |  7227 |     0.571 |    0.575 |  0.004 |     56.311 |    57.017 |       0.706 |
| guards_only           | 8-5          |  6099 |     0.552 |    0.56  |  0.008 |     55.356 |    55.713 |       0.357 |
| guards_only           | 4-1          |  4450 |     0.503 |    0.519 |  0.016 |     53.959 |    54.396 |       0.437 |
| own_centre_guard      | 16-13        |  2980 |     0.513 |    0.482 | -0.031 |     45.47  |    45.132 |      -0.338 |
| own_centre_guard      | 12-9         | 18122 |     0.491 |    0.479 | -0.011 |     44.41  |    44.025 |      -0.385 |
| own_centre_guard      | 8-5          | 26709 |     0.464 |    0.46  | -0.004 |     45.378 |    45.265 |      -0.114 |
| own_centre_guard      | 4-1          | 29367 |     0.408 |    0.403 | -0.006 |     44.919 |    44.835 |      -0.084 |
| opp_centre_guard      | 16-13        | 60218 |     0.647 |    0.628 | -0.019 |     60.74  |    60.537 |      -0.203 |
| opp_centre_guard      | 12-9         | 88082 |     0.624 |    0.605 | -0.019 |     55.195 |    55.1   |      -0.094 |
| opp_centre_guard      | 8-5          | 63574 |     0.602 |    0.583 | -0.018 |     52.448 |    52.345 |      -0.104 |
| opp_centre_guard      | 4-1          | 56484 |     0.568 |    0.568 | -0     |     49.57  |    49.658 |       0.088 |
| own_corner_guard      | 16-13        | 37623 |     0.503 |    0.541 |  0.038 |     31.386 |    32.137 |       0.751 |
| own_corner_guard      | 12-9         | 80117 |     0.514 |    0.542 |  0.027 |     35.211 |    35.725 |       0.514 |
| own_corner_guard      | 8-5          | 77395 |     0.528 |    0.531 |  0.003 |     40.838 |    40.974 |       0.137 |
| own_corner_guard      | 4-1          | 78389 |     0.516 |    0.509 | -0.007 |     43.096 |    43.112 |       0.015 |
| opp_corner_guard      | 16-13        |  2422 |     0.678 |    0.654 | -0.024 |     72.425 |    72.864 |       0.439 |
| opp_corner_guard      | 12-9         | 16294 |     0.647 |    0.653 |  0.006 |     56.095 |    56.493 |       0.398 |
| opp_corner_guard      | 8-5          | 32199 |     0.648 |    0.653 |  0.005 |     49.281 |    49.455 |       0.174 |
| opp_corner_guard      | 4-1          | 40617 |     0.656 |    0.652 | -0.004 |     48.086 |    48.13  |       0.043 |
| open_house            | 16-13        | 63603 |     0.562 |    0.559 | -0.003 |     42.453 |    42.623 |       0.17  |
| open_house            | 12-9         | 14159 |     0.592 |    0.546 | -0.046 |     48.16  |    47.788 |      -0.373 |
| open_house            | 8-5          | 23770 |     0.598 |    0.588 | -0.01  |     48.026 |    48.049 |       0.023 |
| open_house            | 4-1          | 27173 |     0.625 |    0.618 | -0.008 |     47.762 |    47.802 |       0.04  |
| own_shot              | 16-13        | 22150 |     0.737 |    0.705 | -0.032 |     69.63  |    69.106 |      -0.524 |
| own_shot              | 12-9         | 52435 |     0.757 |    0.732 | -0.025 |     63.419 |    63.179 |      -0.24  |
| own_shot              | 8-5          | 56790 |     0.82  |    0.812 | -0.008 |     57.108 |    57.054 |      -0.054 |
| own_shot              | 4-1          | 64861 |     0.937 |    0.96  |  0.023 |     54.209 |    54.526 |       0.318 |
| opp_shot              | 16-13        | 58983 |     0.5   |    0.519 |  0.019 |     31.621 |    32.128 |       0.507 |
| opp_shot              | 12-9         | 89501 |     0.488 |    0.494 |  0.007 |     36.855 |    37.024 |       0.169 |
| opp_shot              | 8-5          | 86142 |     0.431 |    0.432 |  0.001 |     40.004 |    40.1   |       0.096 |
| opp_shot              | 4-1          | 79908 |     0.3   |    0.278 | -0.022 |     41     |    40.837 |      -0.163 |
| own_two_plus          | 12-9         | 14234 |     0.92  |    0.881 | -0.038 |     74.502 |    73.941 |      -0.561 |
| own_two_plus          | 8-5          | 17622 |     1.061 |    1.054 | -0.007 |     63.921 |    63.795 |      -0.126 |
| own_two_plus          | 4-1          | 22152 |     1.337 |    1.382 |  0.045 |     62.012 |    62.674 |       0.662 |
| opp_two_plus          | 16-13        |  8165 |     0.436 |    0.468 |  0.032 |     18.656 |    19.43  |       0.774 |
| opp_two_plus          | 12-9         | 34368 |     0.386 |    0.394 |  0.008 |     24.496 |    24.724 |       0.228 |
| opp_two_plus          | 8-5          | 35242 |     0.266 |    0.262 | -0.004 |     31.202 |    31.307 |       0.105 |
| opp_two_plus          | 4-1          | 33685 |    -0.002 |   -0.045 | -0.043 |     32.715 |    32.452 |      -0.262 |
| split_house           | 12-9         |  4922 |     0.911 |    0.888 | -0.023 |     73.592 |    73.099 |      -0.493 |
| split_house           | 8-5          |  5612 |     1.042 |    1.052 |  0.01  |     61.586 |    61.562 |      -0.024 |
| split_house           | 4-1          |  6234 |     1.299 |    1.362 |  0.062 |     62.264 |    63.112 |       0.848 |
| split_flat            | 12-9         |   641 |     0.919 |    0.895 | -0.024 |     69.777 |    69.541 |      -0.235 |
| split_flat            | 8-5          |  1041 |     1.031 |    1.036 |  0.005 |     59.744 |    60.322 |       0.578 |
| split_flat            | 4-1          |  1272 |     1.249 |    1.322 |  0.073 |     59.034 |    60.198 |       1.164 |
| split_staggered       | 12-9         |  4281 |     0.91  |    0.888 | -0.023 |     74.164 |    73.632 |      -0.532 |
| split_staggered       | 8-5          |  4571 |     1.045 |    1.056 |  0.011 |     62.005 |    61.845 |      -0.161 |
| split_staggered       | 4-1          |  4962 |     1.312 |    1.372 |  0.059 |     63.092 |    63.86  |       0.767 |
| own_shot_covered      | 16-13        | 14549 |     0.757 |    0.725 | -0.032 |     70.493 |    69.956 |      -0.537 |
| own_shot_covered      | 12-9         | 35732 |     0.776 |    0.745 | -0.031 |     65.474 |    65.186 |      -0.289 |
| own_shot_covered      | 8-5          | 33077 |     0.843 |    0.833 | -0.01  |     58.81  |    58.704 |      -0.106 |
| own_shot_covered      | 4-1          | 35430 |     0.984 |    1.019 |  0.035 |     55.192 |    55.666 |       0.474 |
| deuce_loose           | 8-5          |  8894 |     0.951 |    0.934 | -0.017 |     55.264 |    55.216 |      -0.048 |
| deuce_loose           | 4-1          | 12073 |     1.149 |    1.18  |  0.031 |     53.883 |    54.378 |       0.495 |
| steal_setup           | 16-13        |  4750 |     0.727 |    0.671 | -0.056 |     76.957 |    76.316 |      -0.641 |
| steal_setup           | 12-9         | 18370 |     0.698 |    0.65  | -0.048 |     67.849 |    67.443 |      -0.406 |
| steal_setup           | 8-5          | 10149 |     0.613 |    0.578 | -0.034 |     53.984 |    53.423 |      -0.561 |
| steal_setup           | 4-1          | 10771 |     0.545 |    0.524 | -0.021 |     47.449 |    47.144 |      -0.305 |
| steal_on              | 16-13        | 17073 |     0.487 |    0.516 |  0.029 |     34.763 |    35.376 |       0.613 |
| steal_on              | 12-9         | 55495 |     0.46  |    0.464 |  0.004 |     36.556 |    36.707 |       0.152 |
| steal_on              | 8-5          | 46561 |     0.365 |    0.36  | -0.005 |     40.034 |    40.094 |       0.06  |
| steal_on              | 4-1          | 42009 |     0.147 |    0.118 | -0.029 |     39.208 |    38.958 |      -0.249 |
| opp_exposed           | 16-13        | 48193 |     0.501 |    0.517 |  0.016 |     29.694 |    30.196 |       0.502 |
| opp_exposed           | 12-9         | 65536 |     0.538 |    0.543 |  0.005 |     37.867 |    38.028 |       0.161 |
| opp_exposed           | 8-5          | 83706 |     0.543 |    0.543 |  0     |     42.293 |    42.362 |       0.068 |
| opp_exposed           | 4-1          | 88725 |     0.527 |    0.524 | -0.003 |     43.606 |    43.668 |       0.061 |
| open_shot_own         | 16-13        |  3043 |     0.633 |    0.646 |  0.013 |     58.07  |    58.597 |       0.527 |
| open_shot_own         | 12-9         |  5347 |     0.695 |    0.658 | -0.037 |     58.677 |    58.362 |      -0.315 |
| open_shot_own         | 8-5          |  9818 |     0.756 |    0.737 | -0.019 |     57.782 |    57.808 |       0.026 |
| open_shot_own         | 4-1          | 12098 |     0.841 |    0.852 |  0.011 |     52.864 |    53.144 |       0.281 |
| open_shot_opp         | 16-13        | 22725 |     0.509 |    0.51  |  0.001 |     32.384 |    32.701 |       0.317 |
| open_shot_opp         | 12-9         |  8480 |     0.526 |    0.473 | -0.052 |     41.255 |    40.837 |      -0.418 |
| open_shot_opp         | 8-5          | 13373 |     0.484 |    0.48  | -0.004 |     40.674 |    40.705 |       0.03  |
| open_shot_opp         | 4-1          | 14273 |     0.447 |    0.423 | -0.024 |     43.261 |    43.087 |      -0.175 |
| shot_runback_straight | 16-13        | 29820 |     0.619 |    0.624 |  0.005 |     52.564 |    52.666 |       0.102 |
| shot_runback_straight | 12-9         | 89071 |     0.593 |    0.586 | -0.007 |     49.17  |    49.176 |       0.006 |
| shot_runback_straight | 8-5          | 78019 |     0.57  |    0.564 | -0.007 |     48.244 |    48.21  |      -0.034 |
| shot_runback_straight | 4-1          | 77859 |     0.541 |    0.539 | -0.002 |     46.649 |    46.653 |       0.004 |
| shot_runback_angled   | 16-13        | 19701 |     0.525 |    0.534 |  0.009 |     32.43  |    32.792 |       0.362 |
| shot_runback_angled   | 12-9         | 35462 |     0.567 |    0.577 |  0.01  |     39.042 |    39.154 |       0.112 |
| shot_runback_angled   | 8-5          | 39855 |     0.602 |    0.612 |  0.01  |     43.177 |    43.32  |       0.143 |
| shot_runback_angled   | 4-1          | 36596 |     0.632 |    0.635 |  0.003 |     45.929 |    46.09  |       0.162 |
| lonely_steal          | 12-9         |  5843 |     0.709 |    0.701 | -0.008 |     62.767 |    62.794 |       0.027 |
| lonely_steal          | 8-5          |  8920 |     0.721 |    0.758 |  0.037 |     52.676 |    53.052 |       0.376 |
| lonely_steal          | 4-1          |  9645 |     0.751 |    0.774 |  0.022 |     52.383 |    52.61  |       0.226 |
| lonely_steal_exposed  | 12-9         |  5558 |     0.705 |    0.695 | -0.01  |     62.677 |    62.743 |       0.065 |
| lonely_steal_exposed  | 8-5          |  8066 |     0.711 |    0.749 |  0.038 |     52.611 |    52.974 |       0.363 |
| lonely_steal_exposed  | 4-1          |  8781 |     0.728 |    0.745 |  0.017 |     52.006 |    52.226 |       0.22  |
| busy_house            | 12-9         | 15237 |     0.644 |    0.633 | -0.011 |     49.549 |    49.283 |      -0.266 |
| busy_house            | 8-5          | 40003 |     0.599 |    0.598 | -0.001 |     44.276 |    44.241 |      -0.034 |
| busy_house            | 4-1          | 58436 |     0.575 |    0.569 | -0.007 |     43.936 |    43.863 |      -0.073 |
| near_tie              | 16-13        |   356 |     0.684 |    0.681 | -0.003 |     61.656 |    61.588 |      -0.068 |
| near_tie              | 12-9         |  5419 |     0.639 |    0.626 | -0.013 |     51.907 |    51.742 |      -0.164 |
| near_tie              | 8-5          |  8036 |     0.622 |    0.62  | -0.002 |     47.821 |    47.874 |       0.053 |
| near_tie              | 4-1          | 10620 |     0.595 |    0.603 |  0.008 |     45.551 |    45.773 |       0.223 |

## What each configuration leaves the opponent

Before a stone (not the last), by who throws it: how often the configuration survives the stone, and the end's realised value (hammer-adjusted points, hammer team's view) when it survived and when it was wrecked. `model_gap` is the model's gap between the positions left; where `real_gap` is larger, the model under-credits keeping the configuration and under-charges losing it. The `_wp_pp` columns are the same gaps in percentage points of win probability.

| configuration         | thrower    |      n |   survives |   real_kept |   real_wrecked |   real_gap |   model_gap |   real_gap_wp_pp |   model_gap_wp_pp |
|:----------------------|:-----------|-------:|-----------:|------------:|---------------:|-----------:|------------:|-----------------:|------------------:|
| guards_only           | non-hammer |  17198 |      0.393 |       0.586 |          0.5   |      0.086 |       0.09  |           10.62  |            10.264 |
| guards_only           | hammer     |  29355 |      0.381 |       0.531 |          0.682 |     -0.151 |      -0.145 |           -7.632 |            -8.064 |
| own_centre_guard      | non-hammer |  40047 |      0.92  |       0.433 |          0.691 |     -0.258 |      -0.264 |           14.098 |            14.001 |
| own_centre_guard      | hammer     |  29738 |      0.853 |       0.464 |          0.335 |      0.129 |       0.094 |           -6.512 |            -6.891 |
| opp_centre_guard      | non-hammer | 111952 |      0.971 |       0.608 |          0.898 |     -0.289 |      -0.311 |            3.392 |             2.932 |
| opp_centre_guard      | hammer     | 141875 |      0.784 |       0.617 |          0.485 |      0.132 |       0.141 |           -7.259 |            -7.094 |
| own_corner_guard      | non-hammer | 141251 |      0.931 |       0.525 |          0.616 |     -0.091 |      -0.087 |           13.4   |            13.286 |
| own_corner_guard      | hammer     | 112690 |      0.989 |       0.532 |          0.42  |      0.112 |       0.066 |          -14.507 |           -14.489 |
| opp_corner_guard      | non-hammer |  41729 |      0.976 |       0.644 |          0.801 |     -0.158 |      -0.126 |           13.253 |            13.793 |
| opp_corner_guard      | hammer     |  38868 |      0.963 |       0.662 |          0.535 |      0.127 |       0.16  |          -15.125 |           -14.808 |
| open_house            | non-hammer |  73233 |      0.661 |       0.559 |          0.622 |     -0.063 |      -0.093 |          -23.582 |           -24.067 |
| open_house            | hammer     |  48606 |      0.593 |       0.579 |          0.531 |      0.049 |       0.125 |           19.162 |            20     |
| own_shot              | non-hammer | 132579 |      0.458 |       0.964 |          0.6   |      0.365 |       0.396 |           14.238 |            14.678 |
| own_shot              | hammer     |  54809 |      0.952 |       0.896 |          0.544 |      0.353 |       0.388 |            3.046 |             3.678 |
| opp_shot              | non-hammer | 111201 |      0.98  |       0.36  |          0.758 |     -0.398 |      -0.412 |           -4.378 |            -4.528 |
| opp_shot              | hammer     | 175929 |      0.607 |       0.362 |          0.667 |     -0.305 |      -0.31  |          -16.468 |           -16.458 |
| own_two_plus          | non-hammer |  42437 |      0.257 |       1.396 |          0.97  |      0.427 |       0.499 |           15.681 |            16.666 |
| own_two_plus          | hammer     |   9675 |      0.944 |       1.247 |          0.753 |      0.495 |       0.558 |           -3.065 |            -2.371 |
| opp_two_plus          | non-hammer |  29284 |      0.969 |       0.106 |          0.541 |     -0.435 |      -0.44  |            5.124 |             5.315 |
| opp_two_plus          | hammer     |  69214 |      0.392 |       0.112 |          0.464 |     -0.352 |      -0.359 |          -14.035 |           -14.126 |
| split_house           | non-hammer |  14562 |      0.118 |       1.452 |          1.018 |      0.434 |       0.487 |           11.914 |            12.66  |
| split_house           | hammer     |   1891 |      0.734 |       1.316 |          1.304 |      0.012 |      -0.055 |            2.709 |             2.211 |
| split_flat            | non-hammer |   2643 |      0.061 |       1.348 |          1.063 |      0.285 |       0.442 |           13.667 |            14.746 |
| split_flat            | hammer     |    260 |      0.346 |       1.107 |          1.504 |     -0.397 |      -0.344 |           14.625 |            13.517 |
| split_staggered       | non-hammer |  11919 |      0.122 |       1.44  |          1.015 |      0.426 |       0.469 |           11.876 |            12.575 |
| split_staggered       | hammer     |   1631 |      0.73  |       1.308 |          1.293 |      0.016 |      -0.064 |            2.241 |             1.666 |
| own_shot_covered      | non-hammer |  74646 |      0.534 |       0.922 |          0.661 |      0.261 |       0.304 |           15.864 |            16.431 |
| own_shot_covered      | hammer     |  38063 |      0.847 |       0.873 |          0.804 |      0.069 |       0.128 |           -3.059 |            -2.186 |
| deuce_loose           | non-hammer |  15884 |      0.25  |       1.341 |          0.875 |      0.466 |       0.464 |            7.76  |             7.889 |
| deuce_loose           | hammer     |   3640 |      0.83  |       1.24  |          1.042 |      0.198 |       0.243 |           -8.573 |            -8.042 |
| steal_setup           | non-hammer |  14246 |      0.944 |       0.634 |          1.048 |     -0.414 |      -0.381 |           -1.709 |            -1.131 |
| steal_setup           | hammer     |  26477 |      0.535 |       0.657 |          0.526 |      0.131 |       0.16  |           -6.643 |            -6.081 |
| steal_on              | non-hammer |  53575 |      0.883 |       0.262 |          0.519 |     -0.257 |      -0.227 |            5.395 |             5.604 |
| steal_on              | hammer     |  93406 |      0.512 |       0.28  |          0.569 |     -0.289 |      -0.289 |          -15.373 |           -15.451 |
| opp_exposed           | non-hammer | 119599 |      0.836 |       0.502 |          0.458 |      0.044 |       0.008 |           -9.866 |           -10.324 |
| opp_exposed           | hammer     | 140610 |      0.679 |       0.501 |          0.685 |     -0.184 |      -0.174 |          -18.139 |           -18.075 |
| open_shot_own         | non-hammer |  22617 |      0.202 |       1.083 |          0.596 |      0.487 |       0.439 |            7.57  |             6.851 |
| open_shot_own         | hammer     |   6417 |      0.783 |       0.907 |          0.749 |      0.158 |       0.263 |           11.027 |            12.298 |
| open_shot_opp         | non-hammer |  12691 |      0.717 |       0.362 |          0.452 |     -0.09  |      -0.14  |          -25.92  |           -26.318 |
| open_shot_opp         | hammer     |  40782 |      0.182 |       0.318 |          0.549 |     -0.231 |      -0.149 |           -9.332 |            -8.386 |
| shot_runback_straight | non-hammer | 125182 |      0.847 |       0.571 |          0.722 |     -0.151 |      -0.12  |            6.098 |             6.522 |
| shot_runback_straight | hammer     | 129122 |      0.749 |       0.563 |          0.546 |      0.017 |       0.018 |           -6.747 |            -6.69  |
| shot_runback_angled   | non-hammer |  73777 |      0.506 |       0.605 |          0.531 |      0.074 |       0.077 |           -3.137 |            -3.162 |
| shot_runback_angled   | hammer     |  49756 |      0.64  |       0.597 |          0.67  |     -0.073 |      -0.065 |           -9.182 |            -8.969 |
| lonely_steal          | non-hammer |  13783 |      0.341 |       0.745 |          0.547 |      0.198 |       0.297 |           21.39  |            22.318 |
| lonely_steal          | hammer     |   8215 |      0.501 |       0.626 |          1.123 |     -0.497 |      -0.469 |           -3.27  |            -2.877 |
| lonely_steal_exposed  | non-hammer |  12415 |      0.342 |       0.722 |          0.538 |      0.184 |       0.291 |           20.336 |            21.338 |
| lonely_steal_exposed  | hammer     |   7741 |      0.47  |       0.594 |          1.085 |     -0.491 |      -0.436 |           -6.126 |            -5.515 |
| busy_house            | non-hammer |  53215 |      0.866 |       0.584 |          0.703 |     -0.119 |      -0.084 |            9.9   |            10.171 |
| busy_house            | hammer     |  44093 |      0.872 |       0.595 |          0.586 |      0.009 |       0.014 |           -9.77  |            -9.624 |
| near_tie              | non-hammer |  11955 |      0.49  |       0.577 |          0.566 |      0.011 |       0.046 |            7.597 |             8.215 |
| near_tie              | hammer     |   9607 |      0.482 |       0.595 |          0.728 |     -0.133 |      -0.146 |           -0.781 |            -0.846 |

The double on a split: how often the non-hammer team's hit removes both hammer stones (hammer two in the house, the opponent none; percent), by the separation of the pair and its stagger from level:

| sep    |   <10° |   10-20° |   20-35° |   35-55° |   55-90° |
|:-------|-------:|---------:|---------:|---------:|---------:|
| 2-3 ft |     25 |       26 |       21 |        8 |       22 |
| 3-4 ft |      9 |       14 |       20 |        8 |       17 |
| 4-6 ft |      2 |        8 |       14 |        6 |       13 |
| 6 ft+  |      0 |        2 |        7 |        5 |        9 |

Counts:

| sep    |   <10° |   10-20° |   20-35° |   35-55° |   55-90° |
|:-------|-------:|---------:|---------:|---------:|---------:|
| 2-3 ft |    122 |       81 |      154 |      199 |      355 |
| 3-4 ft |    186 |      159 |      209 |      242 |      366 |
| 4-6 ft |    558 |      454 |      519 |      583 |      745 |
| 6 ft+  |    989 |      764 |      941 |     1097 |     1196 |

The runback on the shot rock: how often a Promotion Take-out on the opponent's shot rock leaves the thrower's team lying shot (percent), by the angle of the stone in front off the line of delivery and its distance in front:

| distance   |   <5° |   5-10° |   10-20° |   20-35° |
|:-----------|------:|--------:|---------:|---------:|
| <4 ft      |    46 |      58 |       62 |       71 |
| 4-8 ft     |    37 |      37 |       44 |       39 |
| 8-12 ft    |    28 |      31 |       38 |       39 |
| 12-15 ft   |    31 |      39 |       52 |       27 |

Counts:

| distance   |   <5° |   5-10° |   10-20° |   20-35° |
|:-----------|------:|--------:|---------:|---------:|
| <4 ft      |  1537 |     611 |      472 |      143 |
| 4-8 ft     |  5300 |    1141 |      303 |      100 |
| 8-12 ft    |  3639 |     485 |      164 |       77 |
| 12-15 ft   |   878 |      93 |       61 |       15 |

Runbacks by player (40 or more across the corpus): `angled` and `busy` are the shares of their runbacks at 10 degrees or more and from a house with four or more stones; `lies_shot` how often their team lay shot after; `execution` the mean relative to the event's field for the same call and hammer state (points); `wp_pp` the effect on win probability per runback; `big_makes` runbacks worth half a point or more above the field. The top and bottom fifteen per discipline:

### M

| discipline   | player_key    |   runbacks | teams   |   angled |   busy |   lies_shot |   execution |   wp_pp |   big_makes |   grade |
|:-------------|:--------------|-----------:|:--------|---------:|-------:|------------:|------------:|--------:|------------:|--------:|
| M            | JACOBS B      |         40 | CAN     |    0.125 |  0.625 |       0.725 |       0.22  |   4.167 |          14 |  81.875 |
| M            | DROPKIN K     |         56 | USA     |    0.107 |  0.661 |       0.482 |       0.177 |   3.428 |          18 |  60.714 |
| M            | MOROZUMI Y    |         56 | JPN     |    0.054 |  0.554 |       0.571 |       0.147 |   3.558 |          16 |  68.304 |
| M            | MUSKATEWITZ M |        108 | GER     |    0.083 |  0.556 |       0.509 |       0.138 |   2.673 |          26 |  69.907 |
| M            | GUSHUE B      |         62 | CAN     |    0.129 |  0.597 |       0.565 |       0.135 |   2.937 |          15 |  72.951 |
| M            | SCHWARZ B     |        114 | SUI     |    0.079 |  0.491 |       0.518 |       0.133 |   2.571 |          26 |  64.254 |
| M            | MOUAT B       |        186 | GBR/SCO |    0.108 |  0.554 |       0.602 |       0.133 |   3.999 |          48 |  70.968 |
| M            | HOOD A        |         50 | NZL     |    0.16  |  0.56  |       0.46  |       0.102 |   1.741 |           8 |  61     |
| M            | SHUSTER J     |        126 | USA     |    0.087 |  0.635 |       0.46  |       0.064 |   2.432 |          27 |  61.706 |
| M            | HARDIE G      |        201 | GBR/SCO |    0.07  |  0.338 |       0.468 |       0.059 |   2.423 |           8 |  73.01  |
| M            | NICHOLS M     |         85 | CAN     |    0.118 |  0.471 |       0.424 |       0.056 |   1.743 |           6 |  68.529 |
| M            | ERIKSSON O    |        265 | SWE     |    0.147 |  0.423 |       0.472 |       0.056 |   2.014 |          16 |  72.075 |
| M            | SCHWALLER Y   |        109 | SUI     |    0.083 |  0.44  |       0.422 |       0.053 |   1.963 |          11 |  66.435 |
| M            | RETORNAZ J    |        242 | ITA     |    0.107 |  0.463 |       0.442 |       0.045 |   1.911 |          47 |  58.574 |
| M            | KRAUSE M      |         58 | DEN     |    0.069 |  0.552 |       0.328 |       0.043 |   2.106 |           9 |  53.879 |
| M            | PLYS C        |         74 | USA     |    0.216 |  0.446 |       0.392 |      -0.025 |   0.711 |           3 |  64.527 |
| M            | MESSENZEHL F  |         46 | GER     |    0.087 |  0.152 |       0.478 |      -0.027 |   1.28  |           0 |  70.109 |
| M            | MOSANER A     |        218 | ITA     |    0.087 |  0.381 |       0.344 |      -0.03  |   0.661 |          14 |  61.927 |
| M            | RAMSFJELL B   |         41 | NOR     |    0.024 |  0.195 |       0.39  |      -0.034 |   0.847 |           0 |  70.122 |
| M            | BAUMANN A     |         54 | GER     |    0.093 |  0.37  |       0.426 |      -0.034 |   0.314 |           8 |  55.093 |
| M            | HOEIBERG M    |         43 | NOR     |    0.093 |  0.209 |       0.256 |      -0.038 |   0.432 |           1 |  60.465 |
| M            | VAN DORP J    |         86 | NED     |    0.07  |  0.233 |       0.163 |      -0.052 |   0.074 |           2 |  54.651 |
| M            | JURIK M       |         40 | CZE     |    0.025 |  0.25  |       0.225 |      -0.053 |   0.264 |           0 |  59.375 |
| M            | YANAGISAWA R  |         43 | JPN     |    0.07  |  0.558 |       0.349 |      -0.06  |  -0.467 |           5 |  55.233 |
| M            | PATERSON R    |         40 | SCO     |    0.05  |  0.475 |       0.35  |      -0.079 |  -0.879 |           3 |  61.25  |
| M            | WALSTAD S     |         69 | NOR     |    0.101 |  0.565 |       0.333 |      -0.081 |  -1.042 |           9 |  51.087 |
| M            | SMITH B       |         40 | NZL     |    0.075 |  0.375 |       0.15  |      -0.084 |  -0.622 |           1 |  47.5   |
| M            | TIMOFEEV A    |         42 | RUS     |    0.143 |  0.476 |       0.429 |      -0.12  |  -1.794 |           6 |  50     |
| M            | KIISKINEN K   |         41 | FIN     |    0.073 |  0.683 |       0.293 |      -0.148 |  -1.309 |           3 |  43.902 |
| M            | ZOU Q         |         43 | CHN     |    0.047 |  0.605 |       0.326 |      -0.171 |   0.083 |           3 |  51.744 |

### W

| discipline   | player_key     |   runbacks | teams       |   angled |   busy |   lies_shot |   execution |   wp_pp |   big_makes |   grade |
|:-------------|:---------------|-----------:|:------------|---------:|-------:|------------:|------------:|--------:|------------:|--------:|
| W            | PAETZ A        |        114 | SUI         |    0.096 |  0.588 |       0.57  |       0.151 |   3.559 |          28 |  63.816 |
| W            | HOMAN R        |         49 | CAN         |    0.102 |  0.694 |       0.612 |       0.149 |   4.5   |          15 |  70.408 |
| W            | KUBESKOVA A    |         48 | CZE         |    0.062 |  0.562 |       0.438 |       0.148 |   0.339 |          13 |  54.167 |
| W            | SKASLIEN K     |         75 | NOR         |    0.093 |  0.547 |       0.52  |       0.129 |   2.218 |          19 |  59.667 |
| W            | HASSELBORG A   |        135 | SWE         |    0.074 |  0.652 |       0.533 |       0.117 |   3.039 |          34 |  63.519 |
| W            | DUPONT M       |        126 | DEN         |    0.071 |  0.667 |       0.468 |       0.099 |   3.254 |          30 |  54.563 |
| W            | FUJISAWA S     |         58 | JPN         |    0.103 |  0.621 |       0.431 |       0.095 |  -0.045 |          18 |  56.034 |
| W            | GIM E          |         61 | KOR         |    0.148 |  0.672 |       0.541 |       0.093 |   2.996 |          14 |  70.082 |
| W            | KIM M          |         74 | KOR         |    0.041 |  0.473 |       0.419 |       0.08  |   2.608 |          12 |  64.527 |
| W            | LAWES K        |         46 | CAN         |    0.065 |  0.435 |       0.37  |       0.057 |   1.345 |           2 |  68.478 |
| W            | JENTSCH D      |         90 | GER         |    0.033 |  0.567 |       0.411 |       0.055 |   1.169 |          24 |  53.056 |
| W            | SWEETING V     |         55 | CAN         |    0.091 |  0.455 |       0.473 |       0.051 |   1.83  |           4 |  67.273 |
| W            | TIRINZONI S    |        112 | SUI         |    0.098 |  0.536 |       0.464 |       0.049 |   1.582 |           7 |  70.312 |
| W            | BAUDYSOVA A    |         60 | CZE         |    0.1   |  0.383 |       0.283 |       0.048 |   0.347 |           7 |  49.583 |
| W            | EINARSON K     |         60 | CAN         |    0.15  |  0.65  |       0.533 |       0.047 |   1.771 |          12 |  62.083 |
| W            | KIM K          |         59 | KOR         |    0.153 |  0.492 |       0.254 |      -0.005 |   0.644 |           1 |  64.831 |
| W            | KIM S          |         44 | KOR         |    0.114 |  0.227 |       0.318 |      -0.008 |   1.125 |           0 |  67.614 |
| W            | YILDIZ D       |        119 | TUR         |    0.076 |  0.622 |       0.395 |      -0.009 |   0.953 |          23 |  56.78  |
| W            | MUIRHEAD E     |         78 | GBR/SCO     |    0.064 |  0.615 |       0.5   |      -0.017 |  -0.178 |          17 |  54.167 |
| W            | KNOCHENHAUER A |         79 | SWE         |    0.089 |  0.304 |       0.278 |      -0.018 |   0.731 |           0 |  64.241 |
| W            | ABBES E        |         77 | GER         |    0.104 |  0.312 |       0.325 |      -0.023 |   0.212 |           3 |  59.091 |
| W            | SLOAN A        |         48 | GBR/SCO     |    0.104 |  0.312 |       0.333 |      -0.028 |   0.276 |           2 |  57.812 |
| W            | DONG Z         |         40 | CHN         |    0.05  |  0.4   |       0.3   |      -0.038 |   0.259 |           1 |  63.75  |
| W            | DUPONT D       |         58 | DEN         |    0.121 |  0.431 |       0.241 |      -0.051 |   0.258 |           0 |  53.448 |
| W            | HALSE M        |         82 | DEN         |    0.085 |  0.476 |       0.317 |      -0.059 |  -0.163 |           3 |  57.927 |
| W            | HAN Y          |         42 | CHN         |    0.143 |  0.762 |       0.262 |      -0.069 |  -0.819 |           6 |  60.119 |
| W            | DODDS J        |         80 | GBR/SCO     |    0.088 |  0.275 |       0.238 |      -0.075 |   0.157 |           1 |  55.938 |
| W            | KOVALEVA A     |         48 | RCF/ROC/RUS |    0.125 |  0.625 |       0.396 |      -0.096 |  -0.225 |           8 |  50.532 |
| W            | MORRISON R     |         55 | GBR/SCO     |    0.073 |  0.582 |       0.418 |      -0.107 |   0.45  |          12 |  51.364 |
| W            | KIM E          |         61 | KOR         |    0.082 |  0.689 |       0.377 |      -0.118 |  -1.375 |           8 |  45.492 |

## Scenario probes

One call family from one kind of position, split by what the shot left. `model_v_after` and `model_wp_after` are the model's value of the position the shot left; `real_v` and `real_wp` what the ends from those positions were actually worth; `pg_throw` and `pg_throw_wp_pp` the execution credited. Where the model's gap between two states is smaller than the realised gap, it under-credits the make and under-charges the miss.

### Split house restored, and the walk

Hammer team's hit, stones 6-14, one stone each in the house and no guards. The make restores the split; whether it restores a flat split (the double nearly off) or a staggered one (the walked split, double on) is what the opponent is left.

| state                     |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| opponent still in         |  73 |           0.522 |    0.524 |     -0.203 |           43.888 |    43.675 |           -2.857 |           0.135 |          0.164 |         0.194 |        0.219 |  18.403 |
| other                     |   2 |           0.535 |    0.582 |     -0.347 |           86.148 |    87.866 |           -1.723 |           0.048 |          0     |         0.033 |        0     |  50     |
| rolled out (one in)       | 207 |           0.59  |    0.599 |     -0.207 |           54.899 |    54.83  |           -2.688 |           0.056 |          0.063 |         0.105 |        0.126 |  57.367 |
| split restored, flat      | 196 |           1.054 |    1.082 |      0.235 |           55.954 |    56.657 |            3.227 |           0.041 |          0.02  |         0.589 |        0.602 |  99.872 |
| split restored, staggered | 668 |           0.97  |    0.972 |      0.169 |           55.078 |    55.255 |            2.07  |           0.052 |          0.045 |         0.492 |        0.491 |  98.129 |
| two in, not split         | 103 |           0.898 |    0.658 |      0.094 |           52.251 |    49.605 |            1.009 |           0.056 |          0.029 |         0.413 |        0.184 |  90.049 |

### Peel with hammer, last end, tied

Hammer team's peel, double or take-out, stones 5-8, last end tied with hammer, two or more guards up. The peel gives up points expectation to take the steal away; the question is whether the second is credited for that in win probability, and charged for the miss.

| state               |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| all guards gone     |  69 |           0.433 |    0.449 |     -0.028 |           79.916 |    81.159 |            3.1   |           0.199 |          0.188 |         0.193 |        0.174 |  98.551 |
| none removed        | 276 |           0.413 |    0.255 |     -0.025 |           77.187 |    69.479 |            0.385 |           0.226 |          0.304 |         0.194 |        0.138 |  64.455 |
| one or more removed | 899 |           0.438 |    0.398 |     -0.015 |           79.239 |    78.955 |            1.059 |           0.206 |          0.209 |         0.195 |        0.161 |  96.051 |

### Peel with hammer, last end, down one

Hammer team's peel, double or take-out, stones 5-8, last end down one with hammer, two or more guards up. The peel gives up points expectation to take the steal away; the question is whether the second is credited for that in win probability, and charged for the miss.

| state               |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| all guards gone     |   2 |           0.533 |    0.418 |      0.072 |           44.441 |    23.812 |            3.279 |           0.246 |          0     |         0.35  |        0     | 100     |
| none removed        | 200 |           0.462 |    0.497 |      0.01  |           41.846 |    41.81  |            0.37  |           0.311 |          0.295 |         0.336 |        0.33  |  73.625 |
| one or more removed | 104 |           0.407 |    0.693 |      0.026 |           40.051 |    50.276 |            1.373 |           0.322 |          0.202 |         0.316 |        0.413 |  88.702 |

### Come-around behind a corner guard

Hammer team's draw or freeze, stones 4-8, with its own corner guard up and not lying shot.

| state              |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:-------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| not shot rock      | 13186 |           0.436 |    0.489 |     -0.025 |           24.604 |    25.264 |           -0.24  |           0.263 |          0.247 |         0.295 |        0.316 |  67.779 |
| shot rock, covered |  4037 |           0.647 |    0.656 |      0.074 |           42.895 |    43.239 |            1.056 |           0.204 |          0.221 |         0.362 |        0.385 |  90.891 |
| shot rock, open    |   776 |           0.566 |    0.638 |      0.012 |           37.612 |    39.177 |            0.056 |           0.198 |          0.198 |         0.304 |        0.353 |  76.675 |

### Centre guard without hammer

Non-hammer team's guard or front, stones 1 and 3.

| state                       |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| centre guard placed         | 29128 |           0.638 |    0.625 |      0.004 |           61.906 |    61.845 |            0.111 |           0.208 |          0.213 |         0.343 |        0.337 |  93.212 |
| in the house                |  2285 |           0.579 |    0.613 |      0.018 |           49.322 |    50.11  |            0.192 |           0.19  |          0.182 |         0.298 |        0.311 |  28.743 |
| neither (through or corner) |   453 |           0.733 |    0.803 |     -0.064 |           73.633 |    75.051 |           -0.784 |           0.168 |          0.199 |         0.374 |        0.411 |  52.865 |

### Guard the steal or take the house: the hammer team counts one behind

Non-hammer team to throw, stones 9-14, lying one in the open with the hammer team counts one behind. Guard it and keep the steal (a tight guard, under 8 ft in front, leaves the easier runback), or remove a hammer stone and settle for holding the hammer team to less.

| state                                   |    n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------------------|-----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| guarded long                            | 1124 |           0.427 |    0.477 |      0.073 |           58.455 |    59.05  |            1.158 |           0.29  |          0.268 |         0.279 |        0.296 |  87.478 |
| guarded tight (runback from under 8 ft) | 1136 |           0.379 |    0.455 |      0.112 |           49.74  |    50.633 |            1.654 |           0.294 |          0.262 |         0.257 |        0.266 |  88.138 |
| hammer now lies shot                    |  137 |           0.895 |    0.812 |     -0.357 |           36.274 |    33.761 |           -4.463 |           0.113 |          0.117 |         0.498 |        0.438 |  32.482 |
| hammer stone removed                    | 3244 |           0.37  |    0.364 |      0.128 |           29.027 |    29.153 |            1.627 |           0.201 |          0.195 |         0.178 |        0.174 |  91.014 |
| other                                   | 2244 |           0.696 |    0.652 |     -0.173 |           36.782 |    36.404 |           -1.909 |           0.173 |          0.189 |         0.408 |        0.387 |  64.966 |

### Guard the steal or take the house: the hammer team counts two or more behind (a lonely steal)

Non-hammer team to throw, stones 9-14, lying one in the open with the hammer team counts two or more behind (a lonely steal). Guard it and keep the steal (a tight guard, under 8 ft in front, leaves the easier runback), or remove a hammer stone and settle for holding the hammer team to less.

| state                                   |    n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------------------|-----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| guarded long                            |  424 |           0.62  |    0.608 |      0.093 |           65.275 |    65.199 |            1.783 |           0.28  |          0.264 |         0.363 |        0.342 |  86.144 |
| guarded tight (runback from under 8 ft) |  403 |           0.58  |    0.688 |      0.147 |           58.902 |    60.426 |            2.269 |           0.277 |          0.201 |         0.349 |        0.362 |  87.779 |
| hammer now lies shot                    |   83 |           1.02  |    0.952 |     -0.319 |           37.931 |    37.703 |           -3.079 |           0.125 |          0.169 |         0.552 |        0.518 |  46.951 |
| hammer stone removed                    | 1499 |           0.635 |    0.702 |      0.065 |           33.001 |    33.783 |            0.785 |           0.183 |          0.153 |         0.376 |        0.392 |  86.391 |
| other                                   |  521 |           0.953 |    0.932 |     -0.238 |           51.484 |    50.861 |           -2.73  |           0.17  |          0.175 |         0.511 |        0.501 |  60.721 |

### The steal is on

Hammer team to throw, stones 10-14, the opponent lying shot behind cover. Any call.

| state                    |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:-------------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| hammer lies shot         | 15481 |           0.744 |    0.714 |      0.264 |           50.145 |    49.709 |            3.655 |           0.173 |          0.177 |         0.404 |        0.386 |  90.164 |
| opponent shot, open      |  9071 |           0.339 |    0.279 |      0.046 |           50.68  |    49.768 |            0.811 |           0.264 |          0.299 |         0.195 |        0.181 |  66.881 |
| steal still on (covered) | 18734 |           0.127 |    0.064 |     -0.094 |           35.149 |    34.438 |           -1.209 |           0.406 |          0.426 |         0.199 |        0.182 |  57.267 |
