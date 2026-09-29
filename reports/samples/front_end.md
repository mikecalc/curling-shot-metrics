# Front end: what early-end execution values measure

596,002 shots with a post-shot position. Execution is `pg_throw` relative to the event's field for the same shot type and hammer state. Grades appear only as a check; they are never a model input.

## Measurement by position

`repeatability`: Spearman between a player's mean execution in their odd and even games at an event (40+ shots in each half). `grade_agreement_player`: Spearman between a player-event's mean execution and mean grade (80+ shots). `grade_agreement_shot`: Spearman between a shot's execution and its grade. `opponent_same_game`: Spearman between the two teams' mean execution at the position in the same game, and the same for grades.

| position   |   shots |   player_events |   repeatability |   repeatability_wp |   grade_repeatability |   grade_agreement_player |   grade_agreement_shot |   opponent_same_game |   opponent_same_game_grade |
|:-----------|--------:|----------------:|----------------:|-------------------:|----------------------:|-------------------------:|-----------------------:|---------------------:|---------------------------:|
| Lead       |  148584 |             718 |           0.656 |              0.663 |                 0.617 |                   -0.077 |                  0.264 |                0.232 |                      0.212 |
| Second     |  149167 |             731 |           0.513 |              0.467 |                 0.68  |                    0.297 |                  0.374 |                0.178 |                      0.053 |
| Third      |  149031 |             740 |           0.303 |              0.291 |                 0.643 |                    0.505 |                  0.418 |                0.105 |                      0.001 |
| Fourth     |  149220 |             750 |           0.451 |              0.418 |                 0.641 |                    0.812 |                  0.579 |                0.075 |                     -0.19  |

Team-event correlation of mean execution between positions (a shared component that is not the player's):

|        |   Lead |   Second |   Third |   Fourth |
|:-------|-------:|---------:|--------:|---------:|
| Lead   |   1    |     0.54 |    0.25 |    -0.05 |
| Second |   0.54 |     1    |    0.34 |     0.12 |
| Third  |   0.25 |     0.34 |    1    |     0.28 |
| Fourth |  -0.05 |     0.12 |    0.28 |     1    |

Spread of execution per stone (points, and percentage points of win probability), agreement with the grade, and `next_stone`, the correlation with the next stone's execution in the same end (negative: the see-saw of a mispriced position):

|   shot |    sd |   sd_wp_pp |   mean_abs |   grade_agreement |   next_stone |
|-------:|------:|-----------:|-----------:|------------------:|-------------:|
|      1 | 0.025 |      0.42  |      0.018 |             0.129 |        0.146 |
|      2 | 0.035 |      0.567 |      0.029 |             0.13  |        0.052 |
|      3 | 0.051 |      0.781 |      0.037 |             0.324 |        0.094 |
|      4 | 0.073 |      1.047 |      0.058 |             0.339 |        0.093 |
|      5 | 0.084 |      1.307 |      0.061 |             0.377 |        0.111 |
|      6 | 0.115 |      1.636 |      0.083 |             0.403 |        0.084 |
|      7 | 0.121 |      1.845 |      0.087 |             0.324 |        0.151 |
|      8 | 0.132 |      1.986 |      0.099 |             0.402 |        0.11  |
|      9 | 0.144 |      2.2   |      0.105 |             0.358 |        0.144 |
|     10 | 0.154 |      2.322 |      0.113 |             0.428 |       -0.032 |
|     11 | 0.225 |      3.327 |      0.168 |             0.44  |        0.177 |
|     12 | 0.241 |      3.558 |      0.18  |             0.456 |        0.145 |
|     13 | 0.266 |      4.021 |      0.197 |             0.449 |        0.121 |
|     14 | 0.3   |      4.574 |      0.222 |             0.539 |        0.092 |
|     15 | 0.376 |      6.079 |      0.273 |             0.516 |        0.011 |
|     16 | 0.646 |     10.706 |      0.45  |             0.715 |      nan     |

## Style check (leads and seconds)

Team-event mean execution regressed on the team's mix of calls and pre-shot configurations at that position.

- r2_lead: 0.355
- team_events_lead: 749
- r2_second: 0.379
- team_events_second: 750
- lead_second_raw: 0.612
- lead_second_residual: 0.349

## Configuration calibration

For each configuration before the shot and band of rocks remaining: the model's value of the position (`model_v`, hammer-adjusted points, hammer team's view) against the realised value of the end (`real_v`), and the same in win probability (percent). A configuration the field converts better than the model expects has a positive gap.

| configuration         | rocks_left   |     n |   model_v |   real_v |    gap |   model_wp |   real_wp |   gap_wp_pp |
|:----------------------|:-------------|------:|----------:|---------:|-------:|-----------:|----------:|------------:|
| empty                 | 16-13        | 37619 |     0.586 |    0.582 | -0.004 |     47.196 |    47.26  |       0.064 |
| guards_only           | 16-13        | 29832 |     0.626 |    0.612 | -0.014 |     60.863 |    60.778 |      -0.084 |
| guards_only           | 12-9         |  7227 |     0.571 |    0.575 |  0.003 |     56.317 |    57.017 |       0.7   |
| guards_only           | 8-5          |  6099 |     0.555 |    0.56  |  0.004 |     55.415 |    55.713 |       0.298 |
| guards_only           | 4-1          |  4450 |     0.495 |    0.519 |  0.023 |     53.821 |    54.396 |       0.575 |
| own_centre_guard      | 16-13        |  2980 |     0.545 |    0.482 | -0.063 |     45.791 |    45.132 |      -0.659 |
| own_centre_guard      | 12-9         | 18122 |     0.483 |    0.479 | -0.004 |     44.257 |    44.025 |      -0.232 |
| own_centre_guard      | 8-5          | 26709 |     0.478 |    0.46  | -0.018 |     45.542 |    45.265 |      -0.277 |
| own_centre_guard      | 4-1          | 29367 |     0.424 |    0.403 | -0.022 |     45.11  |    44.835 |      -0.275 |
| opp_centre_guard      | 16-13        | 60218 |     0.647 |    0.628 | -0.018 |     60.737 |    60.537 |      -0.2   |
| opp_centre_guard      | 12-9         | 88082 |     0.616 |    0.605 | -0.01  |     55.07  |    55.1   |       0.03  |
| opp_centre_guard      | 8-5          | 63574 |     0.589 |    0.583 | -0.005 |     52.271 |    52.345 |       0.074 |
| opp_centre_guard      | 4-1          | 56484 |     0.565 |    0.568 |  0.002 |     49.527 |    49.658 |       0.131 |
| own_corner_guard      | 16-13        | 37623 |     0.526 |    0.541 |  0.015 |     31.709 |    32.137 |       0.428 |
| own_corner_guard      | 12-9         | 80117 |     0.511 |    0.542 |  0.031 |     35.191 |    35.725 |       0.534 |
| own_corner_guard      | 8-5          | 77395 |     0.524 |    0.531 |  0.007 |     40.784 |    40.974 |       0.191 |
| own_corner_guard      | 4-1          | 78389 |     0.517 |    0.509 | -0.009 |     43.118 |    43.112 |      -0.006 |
| opp_corner_guard      | 16-13        |  2422 |     0.686 |    0.654 | -0.032 |     72.426 |    72.864 |       0.438 |
| opp_corner_guard      | 12-9         | 16294 |     0.65  |    0.653 |  0.003 |     56.095 |    56.493 |       0.398 |
| opp_corner_guard      | 8-5          | 32199 |     0.646 |    0.653 |  0.007 |     49.234 |    49.455 |       0.221 |
| opp_corner_guard      | 4-1          | 40617 |     0.658 |    0.652 | -0.007 |     48.117 |    48.13  |       0.012 |
| open_house            | 16-13        | 63603 |     0.567 |    0.559 | -0.007 |     42.52  |    42.623 |       0.103 |
| open_house            | 12-9         | 14159 |     0.594 |    0.546 | -0.048 |     48.154 |    47.788 |      -0.367 |
| open_house            | 8-5          | 23770 |     0.601 |    0.588 | -0.013 |     48.059 |    48.049 |      -0.01  |
| open_house            | 4-1          | 27173 |     0.631 |    0.618 | -0.013 |     47.821 |    47.802 |      -0.018 |
| own_shot              | 16-13        | 22150 |     0.727 |    0.705 | -0.022 |     69.463 |    69.106 |      -0.357 |
| own_shot              | 12-9         | 52435 |     0.746 |    0.732 | -0.015 |     63.249 |    63.179 |      -0.07  |
| own_shot              | 8-5          | 56790 |     0.809 |    0.812 |  0.002 |     56.958 |    57.054 |       0.096 |
| own_shot              | 4-1          | 64861 |     0.945 |    0.96  |  0.014 |     54.306 |    54.526 |       0.221 |
| opp_shot              | 16-13        | 58983 |     0.518 |    0.519 |  0.001 |     31.865 |    32.128 |       0.263 |
| opp_shot              | 12-9         | 89501 |     0.481 |    0.494 |  0.014 |     36.788 |    37.024 |       0.236 |
| opp_shot              | 8-5          | 86142 |     0.43  |    0.432 |  0.002 |     39.996 |    40.1   |       0.104 |
| opp_shot              | 4-1          | 79908 |     0.3   |    0.278 | -0.022 |     41.012 |    40.837 |      -0.175 |
| own_two_plus          | 12-9         | 14234 |     0.914 |    0.881 | -0.033 |     74.429 |    73.941 |      -0.487 |
| own_two_plus          | 8-5          | 17622 |     1.046 |    1.054 |  0.008 |     63.702 |    63.795 |       0.094 |
| own_two_plus          | 4-1          | 22152 |     1.356 |    1.382 |  0.026 |     62.283 |    62.674 |       0.391 |
| opp_two_plus          | 16-13        |  8165 |     0.464 |    0.468 |  0.003 |     19.001 |    19.43  |       0.429 |
| opp_two_plus          | 12-9         | 34368 |     0.371 |    0.394 |  0.024 |     24.373 |    24.724 |       0.351 |
| opp_two_plus          | 8-5          | 35242 |     0.26  |    0.262 |  0.002 |     31.148 |    31.307 |       0.159 |
| opp_two_plus          | 4-1          | 33685 |    -0.002 |   -0.045 | -0.043 |     32.734 |    32.452 |      -0.282 |
| split_house           | 12-9         |  4922 |     0.904 |    0.888 | -0.016 |     73.506 |    73.099 |      -0.406 |
| split_house           | 8-5          |  5612 |     1.024 |    1.052 |  0.028 |     61.306 |    61.562 |       0.256 |
| split_house           | 4-1          |  6234 |     1.308 |    1.362 |  0.053 |     62.399 |    63.112 |       0.714 |
| split_flat            | 12-9         |   641 |     0.902 |    0.895 | -0.007 |     69.532 |    69.541 |       0.01  |
| split_flat            | 8-5          |  1041 |     0.969 |    1.036 |  0.067 |     58.787 |    60.322 |       1.535 |
| split_flat            | 4-1          |  1272 |     1.216 |    1.322 |  0.106 |     58.561 |    60.198 |       1.637 |
| split_staggered       | 12-9         |  4281 |     0.905 |    0.888 | -0.017 |     74.101 |    73.632 |      -0.468 |
| split_staggered       | 8-5          |  4571 |     1.037 |    1.056 |  0.019 |     61.88  |    61.845 |      -0.035 |
| split_staggered       | 4-1          |  4962 |     1.332 |    1.372 |  0.04  |     63.382 |    63.86  |       0.477 |
| own_shot_covered      | 16-13        | 14549 |     0.737 |    0.725 | -0.012 |     70.153 |    69.956 |      -0.197 |
| own_shot_covered      | 12-9         | 35732 |     0.762 |    0.745 | -0.017 |     65.242 |    65.186 |      -0.056 |
| own_shot_covered      | 8-5          | 33077 |     0.829 |    0.833 |  0.004 |     58.618 |    58.704 |       0.086 |
| own_shot_covered      | 4-1          | 35430 |     0.985 |    1.019 |  0.035 |     55.19  |    55.666 |       0.477 |
| deuce_loose           | 8-5          |  8894 |     0.919 |    0.934 |  0.014 |     54.848 |    55.216 |       0.368 |
| deuce_loose           | 4-1          | 12073 |     1.151 |    1.18  |  0.028 |     53.907 |    54.378 |       0.471 |
| steal_setup           | 16-13        |  4750 |     0.721 |    0.671 | -0.049 |     76.967 |    76.316 |      -0.651 |
| steal_setup           | 12-9         | 18370 |     0.688 |    0.65  | -0.038 |     67.758 |    67.443 |      -0.315 |
| steal_setup           | 8-5          | 10149 |     0.6   |    0.578 | -0.021 |     53.841 |    53.423 |      -0.418 |
| steal_setup           | 4-1          | 10771 |     0.536 |    0.524 | -0.012 |     47.332 |    47.144 |      -0.188 |
| steal_on              | 16-13        | 17073 |     0.52  |    0.516 | -0.004 |     35.229 |    35.376 |       0.147 |
| steal_on              | 12-9         | 55495 |     0.453 |    0.464 |  0.011 |     36.499 |    36.707 |       0.208 |
| steal_on              | 8-5          | 46561 |     0.368 |    0.36  | -0.007 |     40.073 |    40.094 |       0.02  |
| steal_on              | 4-1          | 42009 |     0.165 |    0.118 | -0.046 |     39.441 |    38.958 |      -0.483 |
| opp_exposed           | 16-13        | 48193 |     0.515 |    0.517 |  0.003 |     29.86  |    30.196 |       0.336 |
| opp_exposed           | 12-9         | 65536 |     0.527 |    0.543 |  0.016 |     37.742 |    38.028 |       0.286 |
| opp_exposed           | 8-5          | 83706 |     0.539 |    0.543 |  0.005 |     42.25  |    42.362 |       0.111 |
| opp_exposed           | 4-1          | 88725 |     0.532 |    0.524 | -0.007 |     43.678 |    43.668 |      -0.011 |
| open_shot_own         | 16-13        |  3043 |     0.667 |    0.646 | -0.021 |     58.573 |    58.597 |       0.024 |
| open_shot_own         | 12-9         |  5347 |     0.694 |    0.658 | -0.036 |     58.643 |    58.362 |      -0.281 |
| open_shot_own         | 8-5          |  9818 |     0.749 |    0.737 | -0.012 |     57.687 |    57.808 |       0.122 |
| open_shot_own         | 4-1          | 12098 |     0.857 |    0.852 | -0.005 |     53.02  |    53.144 |       0.125 |
| open_shot_opp         | 16-13        | 22725 |     0.521 |    0.51  | -0.011 |     32.519 |    32.701 |       0.182 |
| open_shot_opp         | 12-9         |  8480 |     0.53  |    0.473 | -0.056 |     41.269 |    40.837 |      -0.432 |
| open_shot_opp         | 8-5          | 13373 |     0.493 |    0.48  | -0.013 |     40.795 |    40.705 |      -0.091 |
| open_shot_opp         | 4-1          | 14273 |     0.444 |    0.423 | -0.021 |     43.242 |    43.087 |      -0.155 |
| shot_runback_straight | 16-13        | 29820 |     0.628 |    0.624 | -0.005 |     52.675 |    52.666 |      -0.009 |
| shot_runback_straight | 12-9         | 89071 |     0.584 |    0.586 |  0.002 |     49.058 |    49.176 |       0.118 |
| shot_runback_straight | 8-5          | 78019 |     0.567 |    0.564 | -0.003 |     48.201 |    48.21  |       0.009 |
| shot_runback_straight | 4-1          | 77859 |     0.551 |    0.539 | -0.012 |     46.777 |    46.653 |      -0.124 |
| shot_runback_angled   | 16-13        | 19701 |     0.537 |    0.534 | -0.003 |     32.567 |    32.792 |       0.225 |
| shot_runback_angled   | 12-9         | 35462 |     0.556 |    0.577 |  0.021 |     38.919 |    39.154 |       0.236 |
| shot_runback_angled   | 8-5          | 39855 |     0.592 |    0.612 |  0.021 |     43.04  |    43.32  |       0.28  |
| shot_runback_angled   | 4-1          | 36596 |     0.627 |    0.635 |  0.008 |     45.868 |    46.09  |       0.223 |
| lonely_steal          | 12-9         |  5843 |     0.71  |    0.701 | -0.009 |     62.798 |    62.794 |      -0.004 |
| lonely_steal          | 8-5          |  8920 |     0.745 |    0.758 |  0.013 |     53.038 |    53.052 |       0.014 |
| lonely_steal          | 4-1          |  9645 |     0.767 |    0.774 |  0.006 |     52.633 |    52.61  |      -0.023 |
| lonely_steal_exposed  | 12-9         |  5558 |     0.707 |    0.695 | -0.012 |     62.728 |    62.743 |       0.015 |
| lonely_steal_exposed  | 8-5          |  8066 |     0.739 |    0.749 |  0.011 |     53.026 |    52.974 |      -0.052 |
| lonely_steal_exposed  | 4-1          |  8781 |     0.751 |    0.745 | -0.006 |     52.324 |    52.226 |      -0.098 |
| busy_house            | 12-9         | 15237 |     0.61  |    0.633 |  0.023 |     49.128 |    49.283 |       0.155 |
| busy_house            | 8-5          | 40003 |     0.594 |    0.598 |  0.005 |     44.243 |    44.241 |      -0.002 |
| busy_house            | 4-1          | 58436 |     0.579 |    0.569 | -0.011 |     43.997 |    43.863 |      -0.133 |
| near_tie              | 16-13        |   356 |     0.663 |    0.681 |  0.018 |     61.298 |    61.588 |       0.29  |
| near_tie              | 12-9         |  5419 |     0.623 |    0.626 |  0.003 |     51.68  |    51.742 |       0.062 |
| near_tie              | 8-5          |  8036 |     0.617 |    0.62  |  0.003 |     47.751 |    47.874 |       0.123 |
| near_tie              | 4-1          | 10620 |     0.599 |    0.603 |  0.004 |     45.616 |    45.773 |       0.157 |

## What each configuration leaves the opponent

Before a stone (not the last), by who throws it: how often the configuration survives the stone, and the end's realised value (hammer-adjusted points, hammer team's view) when it survived and when it was wrecked. `model_gap` is the model's gap between the positions left; where `real_gap` is larger, the model under-credits keeping the configuration and under-charges losing it. The `_wp_pp` columns are the same gaps in percentage points of win probability.

| configuration         | thrower    |      n |   survives |   real_kept |   real_wrecked |   real_gap |   model_gap |   real_gap_wp_pp |   model_gap_wp_pp |
|:----------------------|:-----------|-------:|-----------:|------------:|---------------:|-----------:|------------:|-----------------:|------------------:|
| guards_only           | non-hammer |  17198 |      0.393 |       0.586 |          0.5   |      0.086 |       0.081 |           10.62  |            10.168 |
| guards_only           | hammer     |  29355 |      0.381 |       0.531 |          0.682 |     -0.151 |      -0.137 |           -7.632 |            -7.946 |
| own_centre_guard      | non-hammer |  40047 |      0.92  |       0.433 |          0.691 |     -0.258 |      -0.255 |           14.098 |            14.091 |
| own_centre_guard      | hammer     |  29738 |      0.853 |       0.464 |          0.335 |      0.129 |       0.136 |           -6.512 |            -6.32  |
| opp_centre_guard      | non-hammer | 111952 |      0.971 |       0.608 |          0.898 |     -0.289 |      -0.327 |            3.392 |             2.733 |
| opp_centre_guard      | hammer     | 141875 |      0.784 |       0.617 |          0.485 |      0.132 |       0.142 |           -7.259 |            -7.063 |
| own_corner_guard      | non-hammer | 141251 |      0.931 |       0.525 |          0.616 |     -0.091 |      -0.086 |           13.4   |            13.335 |
| own_corner_guard      | hammer     | 112690 |      0.989 |       0.532 |          0.42  |      0.112 |       0.074 |          -14.507 |           -14.323 |
| opp_corner_guard      | non-hammer |  41729 |      0.976 |       0.644 |          0.801 |     -0.158 |      -0.139 |           13.253 |            13.609 |
| opp_corner_guard      | hammer     |  38868 |      0.963 |       0.662 |          0.535 |      0.127 |       0.166 |          -15.125 |           -14.702 |
| open_house            | non-hammer |  73233 |      0.661 |       0.559 |          0.622 |     -0.063 |      -0.07  |          -23.582 |           -23.775 |
| open_house            | hammer     |  48606 |      0.593 |       0.579 |          0.531 |      0.049 |       0.127 |           19.162 |            20.054 |
| own_shot              | non-hammer | 132579 |      0.458 |       0.964 |          0.6   |      0.365 |       0.385 |           14.238 |            14.5   |
| own_shot              | hammer     |  54809 |      0.952 |       0.896 |          0.544 |      0.353 |       0.39  |            3.046 |             3.658 |
| opp_shot              | non-hammer | 111201 |      0.98  |       0.36  |          0.758 |     -0.398 |      -0.403 |           -4.378 |            -4.421 |
| opp_shot              | hammer     | 175929 |      0.607 |       0.362 |          0.667 |     -0.305 |      -0.316 |          -16.468 |           -16.497 |
| own_two_plus          | non-hammer |  42437 |      0.257 |       1.396 |          0.97  |      0.427 |       0.498 |           15.681 |            16.739 |
| own_two_plus          | hammer     |   9675 |      0.944 |       1.247 |          0.753 |      0.495 |       0.557 |           -3.065 |            -2.4   |
| opp_two_plus          | non-hammer |  29284 |      0.969 |       0.106 |          0.541 |     -0.435 |      -0.441 |            5.124 |             5.234 |
| opp_two_plus          | hammer     |  69214 |      0.392 |       0.112 |          0.464 |     -0.352 |      -0.38  |          -14.035 |           -14.246 |
| split_house           | non-hammer |  14562 |      0.118 |       1.452 |          1.018 |      0.434 |       0.5   |           11.914 |            12.979 |
| split_house           | hammer     |   1891 |      0.734 |       1.316 |          1.304 |      0.012 |      -0.064 |            2.709 |             2.077 |
| split_flat            | non-hammer |   2643 |      0.061 |       1.348 |          1.063 |      0.285 |       0.45  |           13.667 |            15.018 |
| split_flat            | hammer     |    260 |      0.346 |       1.107 |          1.504 |     -0.397 |      -0.385 |           14.625 |            12.998 |
| split_staggered       | non-hammer |  11919 |      0.122 |       1.44  |          1.015 |      0.426 |       0.485 |           11.876 |            12.945 |
| split_staggered       | hammer     |   1631 |      0.73  |       1.308 |          1.293 |      0.016 |      -0.067 |            2.241 |             1.627 |
| own_shot_covered      | non-hammer |  74646 |      0.534 |       0.922 |          0.661 |      0.261 |       0.287 |           15.864 |            16.18  |
| own_shot_covered      | hammer     |  38063 |      0.847 |       0.873 |          0.804 |      0.069 |       0.115 |           -3.059 |            -2.401 |
| deuce_loose           | non-hammer |  15884 |      0.25  |       1.341 |          0.875 |      0.466 |       0.45  |            7.76  |             7.678 |
| deuce_loose           | hammer     |   3640 |      0.83  |       1.24  |          1.042 |      0.198 |       0.227 |           -8.573 |            -8.23  |
| steal_setup           | non-hammer |  14246 |      0.944 |       0.634 |          1.048 |     -0.414 |      -0.418 |           -1.709 |            -1.602 |
| steal_setup           | hammer     |  26477 |      0.535 |       0.657 |          0.526 |      0.131 |       0.16  |           -6.643 |            -6.042 |
| steal_on              | non-hammer |  53575 |      0.883 |       0.262 |          0.519 |     -0.257 |      -0.22  |            5.395 |             5.674 |
| steal_on              | hammer     |  93406 |      0.512 |       0.28  |          0.569 |     -0.289 |      -0.279 |          -15.373 |           -15.228 |
| opp_exposed           | non-hammer | 119599 |      0.836 |       0.502 |          0.458 |      0.044 |       0.018 |           -9.866 |           -10.195 |
| opp_exposed           | hammer     | 140610 |      0.679 |       0.501 |          0.685 |     -0.184 |      -0.18  |          -18.139 |           -18.136 |
| open_shot_own         | non-hammer |  22617 |      0.202 |       1.083 |          0.596 |      0.487 |       0.439 |            7.57  |             6.778 |
| open_shot_own         | hammer     |   6417 |      0.783 |       0.907 |          0.749 |      0.158 |       0.257 |           11.027 |            12.21  |
| open_shot_opp         | non-hammer |  12691 |      0.717 |       0.362 |          0.452 |     -0.09  |      -0.111 |          -25.92  |           -25.971 |
| open_shot_opp         | hammer     |  40782 |      0.182 |       0.318 |          0.549 |     -0.231 |      -0.164 |           -9.332 |            -8.534 |
| shot_runback_straight | non-hammer | 125182 |      0.847 |       0.571 |          0.722 |     -0.151 |      -0.118 |            6.098 |             6.55  |
| shot_runback_straight | hammer     | 129122 |      0.749 |       0.563 |          0.546 |      0.017 |       0.03  |           -6.747 |            -6.5   |
| shot_runback_angled   | non-hammer |  73777 |      0.506 |       0.605 |          0.531 |      0.074 |       0.065 |           -3.137 |            -3.325 |
| shot_runback_angled   | hammer     |  49756 |      0.64  |       0.597 |          0.67  |     -0.073 |      -0.072 |           -9.182 |            -9.031 |
| lonely_steal          | non-hammer |  13783 |      0.341 |       0.745 |          0.547 |      0.198 |       0.298 |           21.39  |            22.359 |
| lonely_steal          | hammer     |   8215 |      0.501 |       0.626 |          1.123 |     -0.497 |      -0.473 |           -3.27  |            -2.893 |
| lonely_steal_exposed  | non-hammer |  12415 |      0.342 |       0.722 |          0.538 |      0.184 |       0.293 |           20.336 |            21.381 |
| lonely_steal_exposed  | hammer     |   7741 |      0.47  |       0.594 |          1.085 |     -0.491 |      -0.436 |           -6.126 |            -5.458 |
| busy_house            | non-hammer |  53215 |      0.866 |       0.584 |          0.703 |     -0.119 |      -0.087 |            9.9   |            10.151 |
| busy_house            | hammer     |  44093 |      0.872 |       0.595 |          0.586 |      0.009 |       0.003 |           -9.77  |            -9.716 |
| near_tie              | non-hammer |  11955 |      0.49  |       0.577 |          0.566 |      0.011 |       0.037 |            7.597 |             8.051 |
| near_tie              | hammer     |   9607 |      0.482 |       0.595 |          0.728 |     -0.133 |      -0.155 |           -0.781 |            -1.005 |

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
| M            | JACOBS B      |         40 | CAN     |    0.125 |  0.625 |       0.725 |       0.234 |   4.143 |          11 |  81.875 |
| M            | DROPKIN K     |         56 | USA     |    0.107 |  0.661 |       0.482 |       0.167 |   3.352 |          18 |  60.714 |
| M            | SCHWARZ B     |        114 | SUI     |    0.079 |  0.491 |       0.518 |       0.147 |   2.59  |          24 |  64.254 |
| M            | MOROZUMI Y    |         56 | JPN     |    0.054 |  0.554 |       0.571 |       0.145 |   3.318 |          15 |  68.304 |
| M            | MOUAT B       |        186 | GBR/SCO |    0.108 |  0.554 |       0.602 |       0.133 |   3.792 |          42 |  70.968 |
| M            | MUSKATEWITZ M |        108 | GER     |    0.083 |  0.556 |       0.509 |       0.125 |   2.576 |          27 |  69.907 |
| M            | HOOD A        |         50 | NZL     |    0.16  |  0.56  |       0.46  |       0.11  |   1.974 |          10 |  61     |
| M            | GUSHUE B      |         62 | CAN     |    0.129 |  0.597 |       0.565 |       0.109 |   2.723 |          13 |  72.951 |
| M            | SHUSTER J     |        126 | USA     |    0.087 |  0.635 |       0.46  |       0.089 |   2.646 |          24 |  61.706 |
| M            | DE CRUZ P     |         67 | SUI     |    0.134 |  0.194 |       0.343 |       0.073 |   2.1   |           2 |  73.507 |
| M            | KRAUSE M      |         58 | DEN     |    0.069 |  0.552 |       0.328 |       0.052 |   2.1   |           8 |  53.879 |
| M            | RETORNAZ J    |        242 | ITA     |    0.107 |  0.463 |       0.442 |       0.05  |   1.876 |          46 |  58.574 |
| M            | SCHWALLER Y   |        109 | SUI     |    0.083 |  0.44  |       0.422 |       0.048 |   2.12  |          11 |  66.435 |
| M            | WANG Z        |         48 | CHN     |    0.062 |  0.229 |       0.312 |       0.047 |   1.485 |           2 |  69.792 |
| M            | HARDIE G      |        201 | GBR/SCO |    0.07  |  0.338 |       0.468 |       0.046 |   2.145 |          18 |  73.01  |
| M            | RAMSFJELL B   |         41 | NOR     |    0.024 |  0.195 |       0.39  |      -0.024 |   0.961 |           0 |  70.122 |
| M            | PAETZ C       |         52 | SUI     |    0.154 |  0.365 |       0.269 |      -0.026 |   0.582 |           0 |  58.173 |
| M            | NERGAARD T    |         78 | NOR     |    0.09  |  0.321 |       0.41  |      -0.026 |   0.639 |           3 |  68.269 |
| M            | BAUMANN A     |         54 | GER     |    0.093 |  0.37  |       0.426 |      -0.029 |   0.323 |          10 |  55.093 |
| M            | PATERSON R    |         40 | SCO     |    0.05  |  0.475 |       0.35  |      -0.034 |  -0.278 |           4 |  61.25  |
| M            | MOSANER A     |        218 | ITA     |    0.087 |  0.381 |       0.344 |      -0.044 |   0.211 |          11 |  61.927 |
| M            | CERNOVSKY M   |        134 | CZE     |    0.097 |  0.478 |       0.321 |      -0.045 |   0.784 |           4 |  58.955 |
| M            | VAN DORP J    |         86 | NED     |    0.07  |  0.233 |       0.163 |      -0.047 |   0.056 |           3 |  54.651 |
| M            | YANAGISAWA R  |         43 | JPN     |    0.07  |  0.558 |       0.349 |      -0.047 |  -0.417 |           7 |  55.233 |
| M            | JURIK M       |         40 | CZE     |    0.025 |  0.25  |       0.225 |      -0.052 |   0.181 |           0 |  59.375 |
| M            | WALSTAD S     |         69 | NOR     |    0.101 |  0.565 |       0.333 |      -0.055 |  -0.862 |          10 |  51.087 |
| M            | SMITH B       |         40 | NZL     |    0.075 |  0.375 |       0.15  |      -0.085 |  -0.64  |           1 |  47.5   |
| M            | TIMOFEEV A    |         42 | RUS     |    0.143 |  0.476 |       0.429 |      -0.131 |  -2.124 |           7 |  50     |
| M            | KIISKINEN K   |         41 | FIN     |    0.073 |  0.683 |       0.293 |      -0.16  |  -1.289 |           5 |  43.902 |
| M            | ZOU Q         |         43 | CHN     |    0.047 |  0.605 |       0.326 |      -0.173 |  -0.312 |           3 |  51.744 |

### W

| discipline   | player_key     |   runbacks | teams       |   angled |   busy |   lies_shot |   execution |   wp_pp |   big_makes |   grade |
|:-------------|:---------------|-----------:|:------------|---------:|-------:|------------:|------------:|--------:|------------:|--------:|
| W            | HOMAN R        |         49 | CAN         |    0.102 |  0.694 |       0.612 |       0.155 |   4.381 |          13 |  70.408 |
| W            | KUBESKOVA A    |         48 | CZE         |    0.062 |  0.562 |       0.438 |       0.145 |   0.054 |          14 |  54.167 |
| W            | PAETZ A        |        114 | SUI         |    0.096 |  0.588 |       0.57  |       0.14  |   3.416 |          29 |  63.816 |
| W            | SKASLIEN K     |         75 | NOR         |    0.093 |  0.547 |       0.52  |       0.136 |   2.239 |          16 |  59.667 |
| W            | DUPONT M       |        126 | DEN         |    0.071 |  0.667 |       0.468 |       0.092 |   3.334 |          28 |  54.563 |
| W            | FUJISAWA S     |         58 | JPN         |    0.103 |  0.621 |       0.431 |       0.089 |   0.043 |          16 |  56.034 |
| W            | HASSELBORG A   |        135 | SWE         |    0.074 |  0.652 |       0.533 |       0.085 |   2.705 |          33 |  63.519 |
| W            | GIM E          |         61 | KOR         |    0.148 |  0.672 |       0.541 |       0.079 |   2.684 |          17 |  70.082 |
| W            | POLAT O        |         75 | TUR         |    0.093 |  0.493 |       0.4   |       0.067 |   1.726 |           5 |  69.333 |
| W            | KIM M          |         74 | KOR         |    0.041 |  0.473 |       0.419 |       0.066 |   2.455 |          12 |  64.527 |
| W            | LAWES K        |         46 | CAN         |    0.065 |  0.435 |       0.37  |       0.065 |   1.213 |           3 |  68.478 |
| W            | JENTSCH D      |         90 | GER         |    0.033 |  0.567 |       0.411 |       0.064 |   1.653 |          26 |  53.056 |
| W            | TIRINZONI S    |        112 | SUI         |    0.098 |  0.536 |       0.464 |       0.062 |   1.672 |           8 |  70.312 |
| W            | BIRCHARD S     |         40 | CAN         |    0.025 |  0.125 |       0.425 |       0.055 |   1.872 |           1 |  83.125 |
| W            | EINARSON K     |         60 | CAN         |    0.15  |  0.65  |       0.533 |       0.042 |   1.382 |          12 |  62.083 |
| W            | MUIRHEAD E     |         78 | GBR/SCO     |    0.064 |  0.615 |       0.5   |      -0.004 |  -0.096 |          15 |  54.167 |
| W            | YILDIZ D       |        119 | TUR         |    0.076 |  0.622 |       0.395 |      -0.006 |   1.083 |          21 |  56.78  |
| W            | FLEURY T       |         42 | CAN         |    0.095 |  0.405 |       0.405 |      -0.006 |   1.154 |           1 |  64.881 |
| W            | KIM S          |         44 | KOR         |    0.114 |  0.227 |       0.318 |      -0.006 |   1.156 |           0 |  67.614 |
| W            | KNOCHENHAUER A |         79 | SWE         |    0.089 |  0.304 |       0.278 |      -0.009 |   0.792 |           1 |  64.241 |
| W            | KIM K          |         59 | KOR         |    0.153 |  0.492 |       0.254 |      -0.012 |   0.391 |           2 |  64.831 |
| W            | CONSTANTINI S  |        121 | ITA         |    0.074 |  0.537 |       0.421 |      -0.018 |   0.982 |          21 |  57.231 |
| W            | DONG Z         |         40 | CHN         |    0.05  |  0.4   |       0.3   |      -0.027 |   0.277 |           2 |  63.75  |
| W            | DUPONT D       |         58 | DEN         |    0.121 |  0.431 |       0.241 |      -0.037 |   0.277 |           1 |  53.448 |
| W            | HALSE M        |         82 | DEN         |    0.085 |  0.476 |       0.317 |      -0.053 |  -0.186 |           4 |  57.927 |
| W            | DODDS J        |         80 | GBR/SCO     |    0.088 |  0.275 |       0.238 |      -0.055 |   0.494 |           2 |  55.938 |
| W            | HAN Y          |         42 | CHN         |    0.143 |  0.762 |       0.262 |      -0.062 |  -0.638 |           5 |  60.119 |
| W            | MORRISON R     |         55 | GBR/SCO     |    0.073 |  0.582 |       0.418 |      -0.11  |   0.421 |          11 |  51.364 |
| W            | KOVALEVA A     |         48 | RCF/ROC/RUS |    0.125 |  0.625 |       0.396 |      -0.116 |  -0.671 |           7 |  50.532 |
| W            | KIM E          |         61 | KOR         |    0.082 |  0.689 |       0.377 |      -0.132 |  -1.823 |           9 |  45.492 |

## Scenario probes

One call family from one kind of position, split by what the shot left. `model_v_after` and `model_wp_after` are the model's value of the position the shot left; `real_v` and `real_wp` what the ends from those positions were actually worth; `pg_throw` and `pg_throw_wp_pp` the execution credited. Where the model's gap between two states is smaller than the realised gap, it under-credits the make and under-charges the miss.

### Split house restored, and the walk

Hammer team's hit, stones 6-14, one stone each in the house and no guards. The make restores the split; whether it restores a flat split (the double nearly off) or a staggered one (the walked split, double on) is what the opponent is left.

| state                     |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| opponent still in         |  73 |           0.531 |    0.524 |     -0.204 |           43.974 |    43.675 |           -2.921 |           0.14  |          0.164 |         0.209 |        0.219 |  18.403 |
| other                     |   2 |           0.539 |    0.582 |     -0.307 |           86.137 |    87.866 |           -1.475 |           0.05  |          0     |         0.041 |        0     |  50     |
| rolled out (one in)       | 207 |           0.594 |    0.599 |     -0.21  |           54.989 |    54.83  |           -2.666 |           0.051 |          0.063 |         0.101 |        0.126 |  57.367 |
| split restored, flat      | 196 |           0.993 |    1.082 |      0.16  |           55.068 |    56.657 |            2.15  |           0.046 |          0.02  |         0.525 |        0.602 |  99.872 |
| split restored, staggered | 668 |           0.966 |    0.972 |      0.15  |           54.985 |    55.255 |            1.833 |           0.051 |          0.045 |         0.487 |        0.491 |  98.129 |
| two in, not split         | 103 |           0.927 |    0.658 |      0.12  |           52.614 |    49.605 |            1.413 |           0.051 |          0.029 |         0.442 |        0.184 |  90.049 |

### Peel with hammer, last end, tied

Hammer team's peel, double or take-out, stones 5-8, last end tied with hammer, two or more guards up. The peel gives up points expectation to take the steal away; the question is whether the second is credited for that in win probability, and charged for the miss.

| state               |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| all guards gone     |  69 |           0.44  |    0.449 |     -0     |           79.677 |    81.159 |            3.297 |           0.2   |          0.188 |         0.194 |        0.174 |  98.551 |
| none removed        | 276 |           0.397 |    0.255 |     -0.016 |           76.131 |    69.479 |            0.039 |           0.237 |          0.304 |         0.188 |        0.138 |  64.455 |
| one or more removed | 899 |           0.426 |    0.398 |     -0.011 |           78.55  |    78.955 |            0.808 |           0.212 |          0.209 |         0.189 |        0.161 |  96.051 |

### Peel with hammer, last end, down one

Hammer team's peel, double or take-out, stones 5-8, last end down one with hammer, two or more guards up. The peel gives up points expectation to take the steal away; the question is whether the second is credited for that in win probability, and charged for the miss.

| state               |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| all guards gone     |   2 |           0.482 |    0.418 |      0.047 |           41.393 |    23.812 |            1.376 |           0.26  |          0     |         0.316 |        0     | 100     |
| none removed        | 200 |           0.451 |    0.497 |      0.013 |           41.533 |    41.81  |            0.372 |           0.315 |          0.295 |         0.333 |        0.33  |  73.625 |
| one or more removed | 104 |           0.373 |    0.693 |      0.01  |           38.866 |    50.276 |            0.741 |           0.337 |          0.202 |         0.306 |        0.413 |  88.702 |

### Come-around behind a corner guard

Hammer team's draw or freeze, stones 4-8, with its own corner guard up and not lying shot.

| state              |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:-------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| not shot rock      | 13186 |           0.442 |    0.489 |     -0.039 |           24.808 |    25.264 |           -0.356 |           0.269 |          0.247 |         0.304 |        0.316 |  67.779 |
| shot rock, covered |  4037 |           0.652 |    0.656 |      0.06  |           42.967 |    43.239 |            0.817 |           0.201 |          0.221 |         0.366 |        0.385 |  90.891 |
| shot rock, open    |   776 |           0.569 |    0.638 |      0     |           37.662 |    39.177 |           -0.128 |           0.195 |          0.198 |         0.307 |        0.353 |  76.675 |

### Centre guard without hammer

Non-hammer team's guard or front, stones 1 and 3.

| state                       |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| centre guard placed         | 29128 |           0.638 |    0.625 |      0.005 |           61.938 |    61.845 |            0.09  |           0.208 |          0.213 |         0.341 |        0.337 |  93.212 |
| in the house                |  2285 |           0.586 |    0.613 |      0.014 |           49.402 |    50.11  |            0.145 |           0.191 |          0.182 |         0.304 |        0.311 |  28.743 |
| neither (through or corner) |   453 |           0.732 |    0.803 |     -0.063 |           73.646 |    75.051 |           -0.794 |           0.17  |          0.199 |         0.372 |        0.411 |  52.865 |

### Guard the steal or take the house: the hammer team counts one behind

Non-hammer team to throw, stones 9-14, lying one in the open with the hammer team counts one behind. Guard it and keep the steal (a tight guard, under 8 ft in front, leaves the easier runback), or remove a hammer stone and settle for holding the hammer team to less.

| state                                   |    n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------------------|-----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| guarded long                            | 1124 |           0.447 |    0.477 |      0.041 |           58.648 |    59.05  |            0.692 |           0.281 |          0.268 |         0.285 |        0.296 |  87.478 |
| guarded tight (runback from under 8 ft) | 1136 |           0.399 |    0.455 |      0.075 |           49.978 |    50.633 |            1.1   |           0.284 |          0.262 |         0.264 |        0.266 |  88.138 |
| hammer now lies shot                    |  137 |           0.902 |    0.812 |     -0.372 |           36.308 |    33.761 |           -4.479 |           0.113 |          0.117 |         0.5   |        0.438 |  32.482 |
| hammer stone removed                    | 3244 |           0.377 |    0.364 |      0.101 |           29.129 |    29.153 |            1.312 |           0.199 |          0.195 |         0.18  |        0.174 |  91.014 |
| other                                   | 2244 |           0.675 |    0.652 |     -0.155 |           36.527 |    36.404 |           -1.67  |           0.182 |          0.189 |         0.397 |        0.387 |  64.966 |

### Guard the steal or take the house: the hammer team counts two or more behind (a lonely steal)

Non-hammer team to throw, stones 9-14, lying one in the open with the hammer team counts two or more behind (a lonely steal). Guard it and keep the steal (a tight guard, under 8 ft in front, leaves the easier runback), or remove a hammer stone and settle for holding the hammer team to less.

| state                                   |    n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------------------|-----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| guarded long                            |  424 |           0.672 |    0.608 |      0.043 |           65.995 |    65.199 |            1.073 |           0.259 |          0.264 |         0.388 |        0.342 |  86.144 |
| guarded tight (runback from under 8 ft) |  403 |           0.607 |    0.688 |      0.111 |           59.275 |    60.426 |            1.695 |           0.263 |          0.201 |         0.361 |        0.362 |  87.779 |
| hammer now lies shot                    |   83 |           1.067 |    0.952 |     -0.361 |           38.574 |    37.703 |           -3.788 |           0.118 |          0.169 |         0.57  |        0.518 |  46.951 |
| hammer stone removed                    | 1499 |           0.632 |    0.702 |      0.055 |           32.954 |    33.783 |            0.608 |           0.186 |          0.153 |         0.371 |        0.392 |  86.391 |
| other                                   |  521 |           0.953 |    0.932 |     -0.221 |           51.583 |    50.861 |           -2.603 |           0.17  |          0.175 |         0.511 |        0.501 |  60.721 |

### The steal is on

Hammer team to throw, stones 10-14, the opponent lying shot behind cover. Any call.

| state                    |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:-------------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| hammer lies shot         | 15481 |           0.738 |    0.714 |      0.245 |           50.04  |    49.709 |            3.374 |           0.171 |          0.177 |         0.398 |        0.386 |  90.164 |
| opponent shot, open      |  9071 |           0.321 |    0.279 |      0.021 |           50.413 |    49.768 |            0.442 |           0.272 |          0.299 |         0.192 |        0.181 |  66.881 |
| steal still on (covered) | 18734 |           0.148 |    0.064 |     -0.082 |           35.458 |    34.438 |           -1.034 |           0.395 |          0.426 |         0.205 |        0.182 |  57.267 |
