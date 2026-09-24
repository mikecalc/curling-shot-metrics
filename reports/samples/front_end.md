# Front end: what early-end execution values measure

596,002 shots with a post-shot position. Execution is `pg_throw` relative to the event's field for the same shot type and hammer state. Grades appear only as a check; they are never a model input.

## Measurement by position

`repeatability`: Spearman between a player's mean execution in their odd and even games at an event (40+ shots in each half). `grade_agreement_player`: Spearman between a player-event's mean execution and mean grade (80+ shots). `grade_agreement_shot`: Spearman between a shot's execution and its grade. `opponent_same_game`: Spearman between the two teams' mean execution at the position in the same game, and the same for grades.

| position   |   shots |   player_events |   repeatability |   repeatability_wp |   grade_repeatability |   grade_agreement_player |   grade_agreement_shot |   opponent_same_game |   opponent_same_game_grade |
|:-----------|--------:|----------------:|----------------:|-------------------:|----------------------:|-------------------------:|-----------------------:|---------------------:|---------------------------:|
| Lead       |  148584 |             718 |           0.653 |              0.617 |                 0.617 |                   -0.065 |                  0.214 |                0.151 |                      0.212 |
| Second     |  149167 |             731 |           0.491 |              0.429 |                 0.68  |                    0.214 |                  0.347 |                0.156 |                      0.053 |
| Third      |  149031 |             740 |           0.298 |              0.293 |                 0.643 |                    0.454 |                  0.409 |                0.13  |                      0.001 |
| Fourth     |  149220 |             750 |           0.456 |              0.436 |                 0.641 |                    0.818 |                  0.576 |                0.069 |                     -0.19  |

Team-event correlation of mean execution between positions (a shared component that is not the player's):

|        |   Lead |   Second |   Third |   Fourth |
|:-------|-------:|---------:|--------:|---------:|
| Lead   |   1    |     0.56 |    0.34 |     0.01 |
| Second |   0.56 |     1    |    0.35 |     0.04 |
| Third  |   0.34 |     0.35 |    1    |     0.24 |
| Fourth |   0.01 |     0.04 |    0.24 |     1    |

Spread of execution per stone (points, and percentage points of win probability), agreement with the grade, and `next_stone`, the correlation with the next stone's execution in the same end (negative: the see-saw of a mispriced position):

|   shot |    sd |   sd_wp_pp |   mean_abs |   grade_agreement |   next_stone |
|-------:|------:|-----------:|-----------:|------------------:|-------------:|
|      1 | 0.023 |      0.385 |      0.019 |             0.172 |       -0.112 |
|      2 | 0.034 |      0.554 |      0.026 |             0.109 |       -0.056 |
|      3 | 0.055 |      0.821 |      0.041 |             0.27  |        0.114 |
|      4 | 0.063 |      0.961 |      0.047 |             0.304 |       -0.031 |
|      5 | 0.085 |      1.315 |      0.062 |             0.371 |        0.158 |
|      6 | 0.096 |      1.422 |      0.071 |             0.323 |        0.079 |
|      7 | 0.107 |      1.638 |      0.077 |             0.31  |        0.07  |
|      8 | 0.127 |      1.904 |      0.094 |             0.391 |        0.061 |
|      9 | 0.146 |      2.199 |      0.107 |             0.37  |        0.14  |
|     10 | 0.167 |      2.504 |      0.123 |             0.409 |        0.102 |
|     11 | 0.192 |      2.892 |      0.144 |             0.409 |        0.149 |
|     12 | 0.218 |      3.245 |      0.16  |             0.455 |        0.128 |
|     13 | 0.258 |      3.914 |      0.193 |             0.448 |        0.128 |
|     14 | 0.296 |      4.521 |      0.219 |             0.521 |        0.101 |
|     15 | 0.378 |      6.064 |      0.279 |             0.503 |        0.014 |
|     16 | 0.645 |     10.694 |      0.452 |             0.724 |      nan     |

## Style check (leads and seconds)

Team-event mean execution regressed on the team's mix of calls and pre-shot configurations at that position.

- r2_lead: 0.351
- team_events_lead: 749
- r2_second: 0.357
- team_events_second: 750
- lead_second_raw: 0.637
- lead_second_residual: 0.362

## Configuration calibration

For each configuration before the shot and band of rocks remaining: the model's value of the position (`model_v`, hammer-adjusted points, hammer team's view) against the realised value of the end (`real_v`), and the same in win probability (percent). A configuration the field converts better than the model expects has a positive gap.

| configuration         | rocks_left   |     n |   model_v |   real_v |    gap |   model_wp |   real_wp |   gap_wp_pp |
|:----------------------|:-------------|------:|----------:|---------:|-------:|-----------:|----------:|------------:|
| empty                 | 16-13        | 37619 |     0.586 |    0.582 | -0.004 |     47.182 |    47.26  |       0.078 |
| guards_only           | 16-13        | 29832 |     0.632 |    0.612 | -0.02  |     60.916 |    60.778 |      -0.137 |
| guards_only           | 12-9         |  7227 |     0.572 |    0.575 |  0.003 |     56.346 |    57.017 |       0.671 |
| guards_only           | 8-5          |  6099 |     0.549 |    0.56  |  0.011 |     55.353 |    55.713 |       0.36  |
| guards_only           | 4-1          |  4450 |     0.504 |    0.519 |  0.015 |     53.982 |    54.396 |       0.414 |
| own_centre_guard      | 16-13        |  2980 |     0.504 |    0.482 | -0.022 |     45.367 |    45.132 |      -0.235 |
| own_centre_guard      | 12-9         | 18122 |     0.479 |    0.479 |  0     |     44.282 |    44.025 |      -0.257 |
| own_centre_guard      | 8-5          | 26709 |     0.461 |    0.46  | -0.002 |     45.348 |    45.265 |      -0.083 |
| own_centre_guard      | 4-1          | 29367 |     0.419 |    0.403 | -0.016 |     45.058 |    44.835 |      -0.223 |
| opp_centre_guard      | 16-13        | 60218 |     0.648 |    0.628 | -0.02  |     60.742 |    60.537 |      -0.205 |
| opp_centre_guard      | 12-9         | 88082 |     0.621 |    0.605 | -0.015 |     55.158 |    55.1   |      -0.058 |
| opp_centre_guard      | 8-5          | 63574 |     0.597 |    0.583 | -0.013 |     52.393 |    52.345 |      -0.048 |
| opp_centre_guard      | 4-1          | 56484 |     0.572 |    0.568 | -0.004 |     49.614 |    49.658 |       0.044 |
| own_corner_guard      | 16-13        | 37623 |     0.502 |    0.541 |  0.039 |     31.381 |    32.137 |       0.756 |
| own_corner_guard      | 12-9         | 80117 |     0.51  |    0.542 |  0.032 |     35.177 |    35.725 |       0.548 |
| own_corner_guard      | 8-5          | 77395 |     0.525 |    0.531 |  0.005 |     40.817 |    40.974 |       0.158 |
| own_corner_guard      | 4-1          | 78389 |     0.518 |    0.509 | -0.009 |     43.118 |    43.112 |      -0.006 |
| opp_corner_guard      | 16-13        |  2422 |     0.681 |    0.654 | -0.027 |     72.438 |    72.864 |       0.426 |
| opp_corner_guard      | 12-9         | 16294 |     0.647 |    0.653 |  0.006 |     56.115 |    56.493 |       0.377 |
| opp_corner_guard      | 8-5          | 32199 |     0.645 |    0.653 |  0.008 |     49.254 |    49.455 |       0.201 |
| opp_corner_guard      | 4-1          | 40617 |     0.654 |    0.652 | -0.002 |     48.049 |    48.13  |       0.081 |
| open_house            | 16-13        | 63603 |     0.56  |    0.559 | -0.001 |     42.431 |    42.623 |       0.192 |
| open_house            | 12-9         | 14159 |     0.592 |    0.546 | -0.046 |     48.165 |    47.788 |      -0.377 |
| open_house            | 8-5          | 23770 |     0.602 |    0.588 | -0.014 |     48.074 |    48.049 |      -0.025 |
| open_house            | 4-1          | 27173 |     0.625 |    0.618 | -0.007 |     47.758 |    47.802 |       0.044 |
| own_shot              | 16-13        | 22150 |     0.74  |    0.705 | -0.035 |     69.663 |    69.106 |      -0.558 |
| own_shot              | 12-9         | 52435 |     0.762 |    0.732 | -0.03  |     63.483 |    63.179 |      -0.303 |
| own_shot              | 8-5          | 56790 |     0.821 |    0.812 | -0.009 |     57.127 |    57.054 |      -0.073 |
| own_shot              | 4-1          | 64861 |     0.931 |    0.96  |  0.029 |     54.121 |    54.526 |       0.405 |
| opp_shot              | 16-13        | 58983 |     0.498 |    0.519 |  0.021 |     31.604 |    32.128 |       0.524 |
| opp_shot              | 12-9         | 89501 |     0.48  |    0.494 |  0.014 |     36.777 |    37.024 |       0.247 |
| opp_shot              | 8-5          | 86142 |     0.429 |    0.432 |  0.003 |     39.983 |    40.1   |       0.117 |
| opp_shot              | 4-1          | 79908 |     0.308 |    0.278 | -0.03  |     41.1   |    40.837 |      -0.263 |
| own_two_plus          | 12-9         | 14234 |     0.929 |    0.881 | -0.048 |     74.643 |    73.941 |      -0.701 |
| own_two_plus          | 8-5          | 17622 |     1.062 |    1.054 | -0.008 |     63.949 |    63.795 |      -0.154 |
| own_two_plus          | 4-1          | 22152 |     1.329 |    1.382 |  0.053 |     61.905 |    62.674 |       0.769 |
| opp_two_plus          | 16-13        |  8165 |     0.434 |    0.468 |  0.034 |     18.656 |    19.43  |       0.774 |
| opp_two_plus          | 12-9         | 34368 |     0.376 |    0.394 |  0.018 |     24.408 |    24.724 |       0.316 |
| opp_two_plus          | 8-5          | 35242 |     0.263 |    0.262 | -0.002 |     31.184 |    31.307 |       0.123 |
| opp_two_plus          | 4-1          | 33685 |     0.011 |   -0.045 | -0.056 |     32.862 |    32.452 |      -0.41  |
| split_house           | 12-9         |  4922 |     0.918 |    0.888 | -0.03  |     73.691 |    73.099 |      -0.592 |
| split_house           | 8-5          |  5612 |     1.042 |    1.052 |  0.009 |     61.591 |    61.562 |      -0.029 |
| split_house           | 4-1          |  6234 |     1.296 |    1.362 |  0.066 |     62.214 |    63.112 |       0.898 |
| split_flat            | 12-9         |   641 |     0.923 |    0.895 | -0.029 |     69.84  |    69.541 |      -0.299 |
| split_flat            | 8-5          |  1041 |     1.027 |    1.036 |  0.01  |     59.684 |    60.322 |       0.638 |
| split_flat            | 4-1          |  1272 |     1.241 |    1.322 |  0.081 |     58.926 |    60.198 |       1.272 |
| split_staggered       | 12-9         |  4281 |     0.917 |    0.888 | -0.03  |     74.267 |    73.632 |      -0.635 |
| split_staggered       | 8-5          |  4571 |     1.046 |    1.056 |  0.009 |     62.026 |    61.845 |      -0.181 |
| split_staggered       | 4-1          |  4962 |     1.31  |    1.372 |  0.062 |     63.057 |    63.86  |       0.803 |
| own_shot_covered      | 16-13        | 14549 |     0.761 |    0.725 | -0.036 |     70.544 |    69.956 |      -0.588 |
| own_shot_covered      | 12-9         | 35732 |     0.781 |    0.745 | -0.036 |     65.543 |    65.186 |      -0.357 |
| own_shot_covered      | 8-5          | 33077 |     0.844 |    0.833 | -0.011 |     58.824 |    58.704 |      -0.12  |
| own_shot_covered      | 4-1          | 35430 |     0.975 |    1.019 |  0.044 |     55.071 |    55.666 |       0.595 |
| deuce_loose           | 8-5          |  8894 |     0.954 |    0.934 | -0.02  |     55.32  |    55.216 |      -0.104 |
| deuce_loose           | 4-1          | 12073 |     1.145 |    1.18  |  0.035 |     53.837 |    54.378 |       0.541 |
| steal_setup           | 16-13        |  4750 |     0.729 |    0.671 | -0.057 |     76.92  |    76.316 |      -0.604 |
| steal_setup           | 12-9         | 18370 |     0.692 |    0.65  | -0.042 |     67.782 |    67.443 |      -0.339 |
| steal_setup           | 8-5          | 10149 |     0.602 |    0.578 | -0.023 |     53.865 |    53.423 |      -0.442 |
| steal_setup           | 4-1          | 10771 |     0.556 |    0.524 | -0.032 |     47.624 |    47.144 |      -0.48  |
| steal_on              | 16-13        | 17073 |     0.484 |    0.516 |  0.032 |     34.733 |    35.376 |       0.644 |
| steal_on              | 12-9         | 55495 |     0.447 |    0.464 |  0.016 |     36.413 |    36.707 |       0.294 |
| steal_on              | 8-5          | 46561 |     0.361 |    0.36  | -0.001 |     39.987 |    40.094 |       0.107 |
| steal_on              | 4-1          | 42009 |     0.161 |    0.118 | -0.042 |     39.387 |    38.958 |      -0.429 |
| opp_exposed           | 16-13        | 48193 |     0.5   |    0.517 |  0.018 |     29.683 |    30.196 |       0.513 |
| opp_exposed           | 12-9         | 65536 |     0.536 |    0.543 |  0.007 |     37.857 |    38.028 |       0.172 |
| opp_exposed           | 8-5          | 83706 |     0.542 |    0.543 |  0.001 |     42.295 |    42.362 |       0.067 |
| opp_exposed           | 4-1          | 88725 |     0.528 |    0.524 | -0.004 |     43.615 |    43.668 |       0.053 |
| open_shot_own         | 16-13        |  3043 |     0.634 |    0.646 |  0.012 |     58.064 |    58.597 |       0.533 |
| open_shot_own         | 12-9         |  5347 |     0.698 |    0.658 | -0.04  |     58.713 |    58.362 |      -0.35  |
| open_shot_own         | 8-5          |  9818 |     0.76  |    0.737 | -0.024 |     57.838 |    57.808 |      -0.029 |
| open_shot_own         | 4-1          | 12098 |     0.839 |    0.852 |  0.014 |     52.833 |    53.144 |       0.311 |
| open_shot_opp         | 16-13        | 22725 |     0.507 |    0.51  |  0.003 |     32.357 |    32.701 |       0.343 |
| open_shot_opp         | 12-9         |  8480 |     0.525 |    0.473 | -0.052 |     41.233 |    40.837 |      -0.396 |
| open_shot_opp         | 8-5          | 13373 |     0.487 |    0.48  | -0.007 |     40.714 |    40.705 |      -0.009 |
| open_shot_opp         | 4-1          | 14273 |     0.449 |    0.423 | -0.026 |     43.28  |    43.087 |      -0.193 |
| shot_runback_straight | 16-13        | 29820 |     0.62  |    0.624 |  0.004 |     52.573 |    52.666 |       0.093 |
| shot_runback_straight | 12-9         | 89071 |     0.587 |    0.586 | -0.002 |     49.118 |    49.176 |       0.059 |
| shot_runback_straight | 8-5          | 78019 |     0.568 |    0.564 | -0.004 |     48.218 |    48.21  |      -0.008 |
| shot_runback_straight | 4-1          | 77859 |     0.545 |    0.539 | -0.006 |     46.693 |    46.653 |      -0.04  |
| shot_runback_angled   | 16-13        | 19701 |     0.524 |    0.534 |  0.01  |     32.429 |    32.792 |       0.363 |
| shot_runback_angled   | 12-9         | 35462 |     0.567 |    0.577 |  0.01  |     39.057 |    39.154 |       0.097 |
| shot_runback_angled   | 8-5          | 39855 |     0.601 |    0.612 |  0.011 |     43.182 |    43.32  |       0.138 |
| shot_runback_angled   | 4-1          | 36596 |     0.632 |    0.635 |  0.003 |     45.922 |    46.09  |       0.169 |
| lonely_steal          | 12-9         |  5843 |     0.695 |    0.701 |  0.005 |     62.607 |    62.794 |       0.187 |
| lonely_steal          | 8-5          |  8920 |     0.715 |    0.758 |  0.043 |     52.611 |    53.052 |       0.442 |
| lonely_steal          | 4-1          |  9645 |     0.76  |    0.774 |  0.013 |     52.502 |    52.61  |       0.108 |
| lonely_steal_exposed  | 12-9         |  5558 |     0.691 |    0.695 |  0.004 |     62.515 |    62.743 |       0.228 |
| lonely_steal_exposed  | 8-5          |  8066 |     0.704 |    0.749 |  0.045 |     52.534 |    52.974 |       0.441 |
| lonely_steal_exposed  | 4-1          |  8781 |     0.737 |    0.745 |  0.007 |     52.131 |    52.226 |       0.095 |
| busy_house            | 12-9         | 15237 |     0.632 |    0.633 |  0.001 |     49.428 |    49.283 |      -0.144 |
| busy_house            | 8-5          | 40003 |     0.598 |    0.598 |  0     |     44.269 |    44.241 |      -0.027 |
| busy_house            | 4-1          | 58436 |     0.58  |    0.569 | -0.011 |     43.983 |    43.863 |      -0.12  |
| near_tie              | 16-13        |   356 |     0.684 |    0.681 | -0.003 |     61.641 |    61.588 |      -0.053 |
| near_tie              | 12-9         |  5419 |     0.634 |    0.626 | -0.008 |     51.855 |    51.742 |      -0.113 |
| near_tie              | 8-5          |  8036 |     0.622 |    0.62  | -0.002 |     47.82  |    47.874 |       0.054 |
| near_tie              | 4-1          | 10620 |     0.598 |    0.603 |  0.005 |     45.574 |    45.773 |       0.199 |

## What each configuration leaves the opponent

Before a stone (not the last), by who throws it: how often the configuration survives the stone, and the end's realised value (hammer-adjusted points, hammer team's view) when it survived and when it was wrecked. `model_gap` is the model's gap between the positions left; where `real_gap` is larger, the model under-credits keeping the configuration and under-charges losing it. The `_wp_pp` columns are the same gaps in percentage points of win probability.

| configuration         | thrower    |      n |   survives |   real_kept |   real_wrecked |   real_gap |   model_gap |   real_gap_wp_pp |   model_gap_wp_pp |
|:----------------------|:-----------|-------:|-----------:|------------:|---------------:|-----------:|------------:|-----------------:|------------------:|
| guards_only           | non-hammer |  17198 |      0.393 |       0.586 |          0.5   |      0.086 |       0.089 |           10.62  |            10.272 |
| guards_only           | hammer     |  29355 |      0.381 |       0.531 |          0.682 |     -0.151 |      -0.148 |           -7.632 |            -8.108 |
| own_centre_guard      | non-hammer |  40047 |      0.92  |       0.433 |          0.691 |     -0.258 |      -0.262 |           14.098 |            14.057 |
| own_centre_guard      | hammer     |  29738 |      0.853 |       0.464 |          0.335 |      0.129 |       0.094 |           -6.512 |            -6.9   |
| opp_centre_guard      | non-hammer | 111952 |      0.971 |       0.608 |          0.898 |     -0.289 |      -0.31  |            3.392 |             2.953 |
| opp_centre_guard      | hammer     | 141875 |      0.784 |       0.617 |          0.485 |      0.132 |       0.141 |           -7.259 |            -7.108 |
| own_corner_guard      | non-hammer | 141251 |      0.931 |       0.525 |          0.616 |     -0.091 |      -0.088 |           13.4   |            13.286 |
| own_corner_guard      | hammer     | 112690 |      0.989 |       0.532 |          0.42  |      0.112 |       0.063 |          -14.507 |           -14.539 |
| opp_corner_guard      | non-hammer |  41729 |      0.976 |       0.644 |          0.801 |     -0.158 |      -0.129 |           13.253 |            13.757 |
| opp_corner_guard      | hammer     |  38868 |      0.963 |       0.662 |          0.535 |      0.127 |       0.161 |          -15.125 |           -14.795 |
| open_house            | non-hammer |  73233 |      0.661 |       0.559 |          0.622 |     -0.063 |      -0.095 |          -23.582 |           -24.081 |
| open_house            | hammer     |  48606 |      0.593 |       0.579 |          0.531 |      0.049 |       0.129 |           19.162 |            20.032 |
| own_shot              | non-hammer | 132579 |      0.458 |       0.964 |          0.6   |      0.365 |       0.395 |           14.238 |            14.666 |
| own_shot              | hammer     |  54809 |      0.952 |       0.896 |          0.544 |      0.353 |       0.391 |            3.046 |             3.72  |
| opp_shot              | non-hammer | 111201 |      0.98  |       0.36  |          0.758 |     -0.398 |      -0.41  |           -4.378 |            -4.501 |
| opp_shot              | hammer     | 175929 |      0.607 |       0.362 |          0.667 |     -0.305 |      -0.313 |          -16.468 |           -16.48  |
| own_two_plus          | non-hammer |  42437 |      0.257 |       1.396 |          0.97  |      0.427 |       0.497 |           15.681 |            16.647 |
| own_two_plus          | hammer     |   9675 |      0.944 |       1.247 |          0.753 |      0.495 |       0.558 |           -3.065 |            -2.37  |
| opp_two_plus          | non-hammer |  29284 |      0.969 |       0.106 |          0.541 |     -0.435 |      -0.438 |            5.124 |             5.344 |
| opp_two_plus          | hammer     |  69214 |      0.392 |       0.112 |          0.464 |     -0.352 |      -0.359 |          -14.035 |           -14.106 |
| split_house           | non-hammer |  14562 |      0.118 |       1.452 |          1.018 |      0.434 |       0.481 |           11.914 |            12.636 |
| split_house           | hammer     |   1891 |      0.734 |       1.316 |          1.304 |      0.012 |      -0.049 |            2.709 |             2.296 |
| split_flat            | non-hammer |   2643 |      0.061 |       1.348 |          1.063 |      0.285 |       0.441 |           13.667 |            14.785 |
| split_flat            | hammer     |    260 |      0.346 |       1.107 |          1.504 |     -0.397 |      -0.347 |           14.625 |            13.504 |
| split_staggered       | non-hammer |  11919 |      0.122 |       1.44  |          1.015 |      0.426 |       0.462 |           11.876 |            12.541 |
| split_staggered       | hammer     |   1631 |      0.73  |       1.308 |          1.293 |      0.016 |      -0.057 |            2.241 |             1.772 |
| own_shot_covered      | non-hammer |  74646 |      0.534 |       0.922 |          0.661 |      0.261 |       0.304 |           15.864 |            16.428 |
| own_shot_covered      | hammer     |  38063 |      0.847 |       0.873 |          0.804 |      0.069 |       0.128 |           -3.059 |            -2.188 |
| deuce_loose           | non-hammer |  15884 |      0.25  |       1.341 |          0.875 |      0.466 |       0.464 |            7.76  |             7.901 |
| deuce_loose           | hammer     |   3640 |      0.83  |       1.24  |          1.042 |      0.198 |       0.245 |           -8.573 |            -8.004 |
| steal_setup           | non-hammer |  14246 |      0.944 |       0.634 |          1.048 |     -0.414 |      -0.38  |           -1.709 |            -1.09  |
| steal_setup           | hammer     |  26477 |      0.535 |       0.657 |          0.526 |      0.131 |       0.158 |           -6.643 |            -6.122 |
| steal_on              | non-hammer |  53575 |      0.883 |       0.262 |          0.519 |     -0.257 |      -0.227 |            5.395 |             5.62  |
| steal_on              | hammer     |  93406 |      0.512 |       0.28  |          0.569 |     -0.289 |      -0.294 |          -15.373 |           -15.515 |
| opp_exposed           | non-hammer | 119599 |      0.836 |       0.502 |          0.458 |      0.044 |       0.011 |           -9.866 |           -10.308 |
| opp_exposed           | hammer     | 140610 |      0.679 |       0.501 |          0.685 |     -0.184 |      -0.176 |          -18.139 |           -18.096 |
| open_shot_own         | non-hammer |  22617 |      0.202 |       1.083 |          0.596 |      0.487 |       0.432 |            7.57  |             6.786 |
| open_shot_own         | hammer     |   6417 |      0.783 |       0.907 |          0.749 |      0.158 |       0.263 |           11.027 |            12.302 |
| open_shot_opp         | non-hammer |  12691 |      0.717 |       0.362 |          0.452 |     -0.09  |      -0.137 |          -25.92  |           -26.339 |
| open_shot_opp         | hammer     |  40782 |      0.182 |       0.318 |          0.549 |     -0.231 |      -0.147 |           -9.332 |            -8.367 |
| shot_runback_straight | non-hammer | 125182 |      0.847 |       0.571 |          0.722 |     -0.151 |      -0.119 |            6.098 |             6.558 |
| shot_runback_straight | hammer     | 129122 |      0.749 |       0.563 |          0.546 |      0.017 |       0.016 |           -6.747 |            -6.726 |
| shot_runback_angled   | non-hammer |  73777 |      0.506 |       0.605 |          0.531 |      0.074 |       0.081 |           -3.137 |            -3.117 |
| shot_runback_angled   | hammer     |  49756 |      0.64  |       0.597 |          0.67  |     -0.073 |      -0.066 |           -9.182 |            -8.97  |
| lonely_steal          | non-hammer |  13783 |      0.341 |       0.745 |          0.547 |      0.198 |       0.294 |           21.39  |            22.308 |
| lonely_steal          | hammer     |   8215 |      0.501 |       0.626 |          1.123 |     -0.497 |      -0.468 |           -3.27  |            -2.86  |
| lonely_steal_exposed  | non-hammer |  12415 |      0.342 |       0.722 |          0.538 |      0.184 |       0.288 |           20.336 |            21.331 |
| lonely_steal_exposed  | hammer     |   7741 |      0.47  |       0.594 |          1.085 |     -0.491 |      -0.435 |           -6.126 |            -5.504 |
| busy_house            | non-hammer |  53215 |      0.866 |       0.584 |          0.703 |     -0.119 |      -0.082 |            9.9   |            10.198 |
| busy_house            | hammer     |  44093 |      0.872 |       0.595 |          0.586 |      0.009 |       0.013 |           -9.77  |            -9.65  |
| near_tie              | non-hammer |  11955 |      0.49  |       0.577 |          0.566 |      0.011 |       0.047 |            7.597 |             8.21  |
| near_tie              | hammer     |   9607 |      0.482 |       0.595 |          0.728 |     -0.133 |      -0.145 |           -0.781 |            -0.816 |

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
| M            | JACOBS B      |         40 | CAN     |    0.125 |  0.625 |       0.725 |       0.229 |   4.06  |          12 |  81.875 |
| M            | DROPKIN K     |         56 | USA     |    0.107 |  0.661 |       0.482 |       0.169 |   3.305 |          17 |  60.714 |
| M            | MOROZUMI Y    |         56 | JPN     |    0.054 |  0.554 |       0.571 |       0.151 |   3.563 |          15 |  68.304 |
| M            | MUSKATEWITZ M |        108 | GER     |    0.083 |  0.556 |       0.509 |       0.132 |   2.63  |          23 |  69.907 |
| M            | MOUAT B       |        186 | GBR/SCO |    0.108 |  0.554 |       0.602 |       0.12  |   3.838 |          47 |  70.968 |
| M            | SCHWARZ B     |        114 | SUI     |    0.079 |  0.491 |       0.518 |       0.119 |   2.353 |          22 |  64.254 |
| M            | GUSHUE B      |         62 | CAN     |    0.129 |  0.597 |       0.565 |       0.117 |   2.628 |          14 |  72.951 |
| M            | HOOD A        |         50 | NZL     |    0.16  |  0.56  |       0.46  |       0.096 |   1.566 |           9 |  61     |
| M            | ERIKSSON O    |        265 | SWE     |    0.147 |  0.423 |       0.472 |       0.063 |   2.099 |          18 |  72.075 |
| M            | HARDIE G      |        201 | GBR/SCO |    0.07  |  0.338 |       0.468 |       0.061 |   2.392 |           8 |  73.01  |
| M            | SCHWALLER Y   |        109 | SUI     |    0.083 |  0.44  |       0.422 |       0.056 |   2.083 |          11 |  66.435 |
| M            | SHUSTER J     |        126 | USA     |    0.087 |  0.635 |       0.46  |       0.055 |   2.238 |          24 |  61.706 |
| M            | DE CRUZ P     |         67 | SUI     |    0.134 |  0.194 |       0.343 |       0.053 |   1.65  |           1 |  73.507 |
| M            | NICHOLS M     |         85 | CAN     |    0.118 |  0.471 |       0.424 |       0.052 |   1.653 |           6 |  68.529 |
| M            | SHIMIZU T     |         85 | JPN     |    0.106 |  0.365 |       0.424 |       0.043 |   1.581 |           8 |  66.765 |
| M            | CERNOVSKY M   |        134 | CZE     |    0.097 |  0.478 |       0.321 |      -0.024 |   1.077 |           2 |  58.955 |
| M            | LEE J         |         44 | KOR     |    0.068 |  0.295 |       0.227 |      -0.026 |  -0.111 |           3 |  57.955 |
| M            | RAMSFJELL M   |        103 | NOR     |    0.117 |  0.515 |       0.427 |      -0.026 |   0.331 |          15 |  58.333 |
| M            | HOEIBERG M    |         43 | NOR     |    0.093 |  0.209 |       0.256 |      -0.026 |   0.607 |           1 |  60.465 |
| M            | BAUMANN A     |         54 | GER     |    0.093 |  0.37  |       0.426 |      -0.037 |   0.072 |           7 |  55.093 |
| M            | MOSANER A     |        218 | ITA     |    0.087 |  0.381 |       0.344 |      -0.037 |   0.488 |          12 |  61.927 |
| M            | JURIK M       |         40 | CZE     |    0.025 |  0.25  |       0.225 |      -0.04  |   0.397 |           0 |  59.375 |
| M            | VAN DORP J    |         86 | NED     |    0.07  |  0.233 |       0.163 |      -0.05  |   0.111 |           1 |  54.651 |
| M            | YANAGISAWA R  |         43 | JPN     |    0.07  |  0.558 |       0.349 |      -0.057 |  -0.581 |           4 |  55.233 |
| M            | PATERSON R    |         40 | SCO     |    0.05  |  0.475 |       0.35  |      -0.072 |  -0.922 |           3 |  61.25  |
| M            | WALSTAD S     |         69 | NOR     |    0.101 |  0.565 |       0.333 |      -0.087 |  -1.047 |          10 |  51.087 |
| M            | SMITH B       |         40 | NZL     |    0.075 |  0.375 |       0.15  |      -0.087 |  -0.664 |           0 |  47.5   |
| M            | TIMOFEEV A    |         42 | RUS     |    0.143 |  0.476 |       0.429 |      -0.137 |  -2.131 |           5 |  50     |
| M            | KIISKINEN K   |         41 | FIN     |    0.073 |  0.683 |       0.293 |      -0.155 |  -1.121 |           3 |  43.902 |
| M            | ZOU Q         |         43 | CHN     |    0.047 |  0.605 |       0.326 |      -0.176 |  -0.084 |           4 |  51.744 |

### W

| discipline   | player_key     |   runbacks | teams       |   angled |   busy |   lies_shot |   execution |   wp_pp |   big_makes |   grade |
|:-------------|:---------------|-----------:|:------------|---------:|-------:|------------:|------------:|--------:|------------:|--------:|
| W            | KUBESKOVA A    |         48 | CZE         |    0.062 |  0.562 |       0.438 |       0.15  |   0.349 |          15 |  54.167 |
| W            | PAETZ A        |        114 | SUI         |    0.096 |  0.588 |       0.57  |       0.146 |   3.449 |          27 |  63.816 |
| W            | HOMAN R        |         49 | CAN         |    0.102 |  0.694 |       0.612 |       0.133 |   4.241 |          15 |  70.408 |
| W            | SKASLIEN K     |         75 | NOR         |    0.093 |  0.547 |       0.52  |       0.124 |   2.154 |          19 |  59.667 |
| W            | HASSELBORG A   |        135 | SWE         |    0.074 |  0.652 |       0.533 |       0.108 |   2.907 |          34 |  63.519 |
| W            | GIM E          |         61 | KOR         |    0.148 |  0.672 |       0.541 |       0.087 |   2.846 |          11 |  70.082 |
| W            | DUPONT M       |        126 | DEN         |    0.071 |  0.667 |       0.468 |       0.082 |   3.019 |          28 |  54.563 |
| W            | FUJISAWA S     |         58 | JPN         |    0.103 |  0.621 |       0.431 |       0.081 |  -0.162 |          17 |  56.034 |
| W            | KIM M          |         74 | KOR         |    0.041 |  0.473 |       0.419 |       0.081 |   2.454 |          12 |  64.527 |
| W            | TIRINZONI S    |        112 | SUI         |    0.098 |  0.536 |       0.464 |       0.062 |   1.713 |           8 |  70.312 |
| W            | LAWES K        |         46 | CAN         |    0.065 |  0.435 |       0.37  |       0.059 |   1.438 |           4 |  68.478 |
| W            | BIRCHARD S     |         40 | CAN         |    0.025 |  0.125 |       0.425 |       0.05  |   1.764 |           1 |  83.125 |
| W            | SWEETING V     |         55 | CAN         |    0.091 |  0.455 |       0.473 |       0.042 |   1.635 |           3 |  67.273 |
| W            | BAUDYSOVA A    |         60 | CZE         |    0.1   |  0.383 |       0.283 |       0.039 |   0.213 |           6 |  49.583 |
| W            | JENTSCH D      |         90 | GER         |    0.033 |  0.567 |       0.411 |       0.036 |   0.95  |          23 |  53.056 |
| W            | FLEURY T       |         42 | CAN         |    0.095 |  0.405 |       0.405 |       0.001 |   1.235 |           1 |  64.881 |
| W            | KIM K          |         59 | KOR         |    0.153 |  0.492 |       0.254 |      -0.002 |   0.688 |           2 |  64.831 |
| W            | KNOCHENHAUER A |         79 | SWE         |    0.089 |  0.304 |       0.278 |      -0.005 |   0.924 |           1 |  64.241 |
| W            | SLOAN A        |         48 | GBR/SCO     |    0.104 |  0.312 |       0.333 |      -0.02  |   0.501 |           1 |  57.812 |
| W            | YILDIZ D       |        119 | TUR         |    0.076 |  0.622 |       0.395 |      -0.021 |   0.673 |          20 |  56.78  |
| W            | DONG Z         |         40 | CHN         |    0.05  |  0.4   |       0.3   |      -0.026 |   0.379 |           1 |  63.75  |
| W            | ABBES E        |         77 | GER         |    0.104 |  0.312 |       0.325 |      -0.026 |   0.137 |           2 |  59.091 |
| W            | MUIRHEAD E     |         78 | GBR/SCO     |    0.064 |  0.615 |       0.5   |      -0.033 |  -0.315 |          16 |  54.167 |
| W            | DUPONT D       |         58 | DEN         |    0.121 |  0.431 |       0.241 |      -0.047 |   0.261 |           0 |  53.448 |
| W            | HALSE M        |         82 | DEN         |    0.085 |  0.476 |       0.317 |      -0.051 |  -0.053 |           2 |  57.927 |
| W            | DODDS J        |         80 | GBR/SCO     |    0.088 |  0.275 |       0.238 |      -0.072 |   0.153 |           2 |  55.938 |
| W            | HAN Y          |         42 | CHN         |    0.143 |  0.762 |       0.262 |      -0.077 |  -0.891 |           4 |  60.119 |
| W            | KOVALEVA A     |         48 | RCF/ROC/RUS |    0.125 |  0.625 |       0.396 |      -0.1   |  -0.308 |           7 |  50.532 |
| W            | KIM E          |         61 | KOR         |    0.082 |  0.689 |       0.377 |      -0.13  |  -1.44  |           7 |  45.492 |
| W            | MORRISON R     |         55 | GBR/SCO     |    0.073 |  0.582 |       0.418 |      -0.132 |   0.12  |          11 |  51.364 |

## Scenario probes

One call family from one kind of position, split by what the shot left. `model_v_after` and `model_wp_after` are the model's value of the position the shot left; `real_v` and `real_wp` what the ends from those positions were actually worth; `pg_throw` and `pg_throw_wp_pp` the execution credited. Where the model's gap between two states is smaller than the realised gap, it under-credits the make and under-charges the miss.

### Split house restored, and the walk

Hammer team's hit, stones 6-14, one stone each in the house and no guards. The make restores the split; whether it restores a flat split (the double nearly off) or a staggered one (the walked split, double on) is what the opponent is left.

| state                     |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| opponent still in         |  73 |           0.525 |    0.524 |     -0.2   |           43.884 |    43.675 |           -2.906 |           0.135 |          0.164 |         0.196 |        0.219 |  18.403 |
| other                     |   2 |           0.531 |    0.582 |     -0.34  |           86.018 |    87.866 |           -1.827 |           0.053 |          0     |         0.034 |        0     |  50     |
| rolled out (one in)       | 207 |           0.592 |    0.599 |     -0.206 |           54.929 |    54.83  |           -2.691 |           0.055 |          0.063 |         0.105 |        0.126 |  57.367 |
| split restored, flat      | 196 |           1.053 |    1.082 |      0.238 |           55.943 |    56.657 |            3.259 |           0.043 |          0.02  |         0.591 |        0.602 |  99.872 |
| split restored, staggered | 668 |           0.976 |    0.972 |      0.173 |           55.156 |    55.255 |            2.123 |           0.053 |          0.045 |         0.5   |        0.491 |  98.129 |
| two in, not split         | 103 |           0.886 |    0.658 |      0.085 |           52.148 |    49.605 |            0.937 |           0.056 |          0.029 |         0.403 |        0.184 |  90.049 |

### Peel with hammer, last end, tied

Hammer team's peel, double or take-out, stones 5-8, last end tied with hammer, two or more guards up. The peel gives up points expectation to take the steal away; the question is whether the second is credited for that in win probability, and charged for the miss.

| state               |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| all guards gone     |  69 |           0.436 |    0.449 |     -0.027 |           79.882 |    81.159 |            2.889 |           0.199 |          0.188 |         0.196 |        0.174 |  98.551 |
| none removed        | 276 |           0.41  |    0.255 |     -0.029 |           76.984 |    69.479 |            0.107 |           0.228 |          0.304 |         0.194 |        0.138 |  64.455 |
| one or more removed | 899 |           0.439 |    0.398 |     -0.019 |           79.187 |    78.955 |            0.72  |           0.206 |          0.209 |         0.196 |        0.161 |  96.051 |

### Peel with hammer, last end, down one

Hammer team's peel, double or take-out, stones 5-8, last end down one with hammer, two or more guards up. The peel gives up points expectation to take the steal away; the question is whether the second is credited for that in win probability, and charged for the miss.

| state               |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| all guards gone     |   2 |           0.519 |    0.418 |      0.033 |           44.457 |    23.812 |            2.395 |           0.249 |          0     |         0.352 |        0     | 100     |
| none removed        | 200 |           0.45  |    0.497 |      0.005 |           41.565 |    41.81  |            0.147 |           0.318 |          0.295 |         0.335 |        0.33  |  73.625 |
| one or more removed | 104 |           0.394 |    0.693 |      0.014 |           39.775 |    50.276 |            0.931 |           0.328 |          0.202 |         0.314 |        0.413 |  88.702 |

### Come-around behind a corner guard

Hammer team's draw or freeze, stones 4-8, with its own corner guard up and not lying shot.

| state              |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:-------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| not shot rock      | 13186 |           0.424 |    0.489 |     -0.032 |           24.506 |    25.264 |           -0.292 |           0.27  |          0.247 |         0.293 |        0.316 |  67.779 |
| shot rock, covered |  4037 |           0.649 |    0.656 |      0.078 |           42.936 |    43.239 |            1.12  |           0.203 |          0.221 |         0.365 |        0.385 |  90.891 |
| shot rock, open    |   776 |           0.567 |    0.638 |      0.013 |           37.629 |    39.177 |            0.066 |           0.198 |          0.198 |         0.306 |        0.353 |  76.675 |

### Centre guard without hammer

Non-hammer team's guard or front, stones 1 and 3.

| state                       |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| centre guard placed         | 29128 |           0.639 |    0.625 |      0.003 |           61.902 |    61.845 |            0.107 |           0.209 |          0.213 |         0.344 |        0.337 |  93.212 |
| in the house                |  2285 |           0.577 |    0.613 |      0.017 |           49.301 |    50.11  |            0.187 |           0.191 |          0.182 |         0.298 |        0.311 |  28.743 |
| neither (through or corner) |   453 |           0.735 |    0.803 |     -0.064 |           73.655 |    75.051 |           -0.806 |           0.166 |          0.199 |         0.375 |        0.411 |  52.865 |

### Guard the steal or take the house: the hammer team counts one behind

Non-hammer team to throw, stones 9-14, lying one in the open with the hammer team counts one behind. Guard it and keep the steal (a tight guard, under 8 ft in front, leaves the easier runback), or remove a hammer stone and settle for holding the hammer team to less.

| state                                   |    n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------------------|-----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| guarded long                            | 1124 |           0.432 |    0.477 |      0.069 |           58.545 |    59.05  |            1.107 |           0.287 |          0.268 |         0.28  |        0.296 |  87.478 |
| guarded tight (runback from under 8 ft) | 1136 |           0.387 |    0.455 |      0.103 |           49.877 |    50.633 |            1.531 |           0.289 |          0.262 |         0.259 |        0.266 |  88.138 |
| hammer now lies shot                    |  137 |           0.903 |    0.812 |     -0.36  |           36.322 |    33.761 |           -4.387 |           0.111 |          0.117 |         0.502 |        0.438 |  32.482 |
| hammer stone removed                    | 3244 |           0.373 |    0.364 |      0.126 |           29.062 |    29.153 |            1.621 |           0.202 |          0.195 |         0.18  |        0.174 |  91.014 |
| other                                   | 2244 |           0.693 |    0.652 |     -0.167 |           36.739 |    36.404 |           -1.824 |           0.175 |          0.189 |         0.407 |        0.387 |  64.966 |

### Guard the steal or take the house: the hammer team counts two or more behind (a lonely steal)

Non-hammer team to throw, stones 9-14, lying one in the open with the hammer team counts two or more behind (a lonely steal). Guard it and keep the steal (a tight guard, under 8 ft in front, leaves the easier runback), or remove a hammer stone and settle for holding the hammer team to less.

| state                                   |    n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------------------|-----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| guarded long                            |  424 |           0.62  |    0.608 |      0.095 |           65.365 |    65.199 |            1.681 |           0.277 |          0.264 |         0.362 |        0.342 |  86.144 |
| guarded tight (runback from under 8 ft) |  403 |           0.586 |    0.688 |      0.145 |           59.038 |    60.426 |            2.155 |           0.272 |          0.201 |         0.348 |        0.362 |  87.779 |
| hammer now lies shot                    |   83 |           1.019 |    0.952 |     -0.306 |           37.967 |    37.703 |           -2.936 |           0.125 |          0.169 |         0.551 |        0.518 |  46.951 |
| hammer stone removed                    | 1499 |           0.636 |    0.702 |      0.072 |           33.017 |    33.783 |            0.878 |           0.183 |          0.153 |         0.376 |        0.392 |  86.391 |
| other                                   |  521 |           0.946 |    0.932 |     -0.228 |           51.405 |    50.861 |           -2.64  |           0.171 |          0.175 |         0.507 |        0.501 |  60.721 |

### The steal is on

Hammer team to throw, stones 10-14, the opponent lying shot behind cover. Any call.

| state                    |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:-------------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| hammer lies shot         | 15481 |           0.739 |    0.714 |      0.258 |           50.071 |    49.709 |            3.571 |           0.172 |          0.177 |         0.401 |        0.386 |  90.164 |
| opponent shot, open      |  9071 |           0.347 |    0.279 |      0.052 |           50.803 |    49.768 |            0.893 |           0.259 |          0.299 |         0.196 |        0.181 |  66.881 |
| steal still on (covered) | 18734 |           0.139 |    0.064 |     -0.101 |           35.282 |    34.438 |           -1.321 |           0.401 |          0.426 |         0.203 |        0.182 |  57.267 |
