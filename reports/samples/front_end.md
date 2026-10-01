# Front end: what early-end execution values measure

596,002 shots with a post-shot position. Execution is `pg_throw` relative to the event's field for the same shot type and hammer state. Grades appear only as a check; they are never a model input.

## Measurement by position

`repeatability`: Spearman between a player's mean execution in their odd and even games at an event (40+ shots in each half). `grade_agreement_player`: Spearman between a player-event's mean execution and mean grade (80+ shots). `grade_agreement_shot`: Spearman between a shot's execution and its grade. `opponent_same_game`: Spearman between the two teams' mean execution at the position in the same game, and the same for grades.

| position   |   shots |   player_events |   repeatability |   repeatability_wp |   grade_repeatability |   grade_agreement_player |   grade_agreement_shot |   opponent_same_game |   opponent_same_game_grade |
|:-----------|--------:|----------------:|----------------:|-------------------:|----------------------:|-------------------------:|-----------------------:|---------------------:|---------------------------:|
| Lead       |  148584 |             718 |           0.651 |              0.64  |                 0.617 |                   -0.065 |                  0.271 |                0.233 |                      0.212 |
| Second     |  149167 |             731 |           0.528 |              0.475 |                 0.68  |                    0.309 |                  0.375 |                0.174 |                      0.053 |
| Third      |  149031 |             740 |           0.305 |              0.299 |                 0.643 |                    0.5   |                  0.418 |                0.116 |                      0.001 |
| Fourth     |  149220 |             750 |           0.453 |              0.421 |                 0.641 |                    0.816 |                  0.579 |                0.073 |                     -0.19  |

Team-event correlation of mean execution between positions (a shared component that is not the player's):

|        |   Lead |   Second |   Third |   Fourth |
|:-------|-------:|---------:|--------:|---------:|
| Lead   |   1    |     0.53 |    0.23 |    -0.03 |
| Second |   0.53 |     1    |    0.33 |     0.13 |
| Third  |   0.23 |     0.33 |    1    |     0.28 |
| Fourth |  -0.03 |     0.13 |    0.28 |     1    |

Spread of execution per stone (points, and percentage points of win probability), agreement with the grade, and `next_stone`, the correlation with the next stone's execution in the same end (negative: the see-saw of a mispriced position):

|   shot |    sd |   sd_wp_pp |   mean_abs |   grade_agreement |   next_stone |
|-------:|------:|-----------:|-----------:|------------------:|-------------:|
|      1 | 0.025 |      0.432 |      0.019 |             0.127 |        0.113 |
|      2 | 0.034 |      0.56  |      0.03  |             0.144 |        0.056 |
|      3 | 0.052 |      0.792 |      0.037 |             0.33  |        0.096 |
|      4 | 0.072 |      1.033 |      0.057 |             0.347 |        0.089 |
|      5 | 0.085 |      1.311 |      0.062 |             0.383 |        0.12  |
|      6 | 0.115 |      1.623 |      0.083 |             0.407 |        0.081 |
|      7 | 0.121 |      1.84  |      0.087 |             0.322 |        0.151 |
|      8 | 0.132 |      1.99  |      0.099 |             0.4   |        0.106 |
|      9 | 0.144 |      2.198 |      0.105 |             0.354 |        0.145 |
|     10 | 0.154 |      2.325 |      0.113 |             0.429 |       -0.028 |
|     11 | 0.223 |      3.307 |      0.167 |             0.438 |        0.176 |
|     12 | 0.24  |      3.55  |      0.179 |             0.456 |        0.141 |
|     13 | 0.266 |      4.029 |      0.197 |             0.45  |        0.122 |
|     14 | 0.3   |      4.563 |      0.222 |             0.538 |        0.09  |
|     15 | 0.375 |      6.07  |      0.273 |             0.517 |        0.011 |
|     16 | 0.648 |     10.71  |      0.451 |             0.717 |      nan     |

## Style check (leads and seconds)

Team-event mean execution regressed on the team's mix of calls and pre-shot configurations at that position.

- r2_lead: 0.355
- team_events_lead: 749
- r2_second: 0.375
- team_events_second: 750
- lead_second_raw: 0.591
- lead_second_residual: 0.350

## Configuration calibration

For each configuration before the shot and band of rocks remaining: the model's value of the position (`model_v`, hammer-adjusted points, hammer team's view) against the realised value of the end (`real_v`), and the same in win probability (percent). A configuration the field converts better than the model expects has a positive gap.

| configuration         | rocks_left   |     n |   model_v |   real_v |    gap |   model_wp |   real_wp |   gap_wp_pp |
|:----------------------|:-------------|------:|----------:|---------:|-------:|-----------:|----------:|------------:|
| empty                 | 16-13        | 37619 |     0.586 |    0.582 | -0.004 |     47.197 |    47.26  |       0.064 |
| guards_only           | 16-13        | 29832 |     0.626 |    0.612 | -0.014 |     60.861 |    60.778 |      -0.083 |
| guards_only           | 12-9         |  7227 |     0.57  |    0.575 |  0.004 |     56.309 |    57.017 |       0.708 |
| guards_only           | 8-5          |  6099 |     0.555 |    0.56  |  0.005 |     55.426 |    55.713 |       0.287 |
| guards_only           | 4-1          |  4450 |     0.495 |    0.519 |  0.024 |     53.821 |    54.396 |       0.575 |
| own_centre_guard      | 16-13        |  2980 |     0.545 |    0.482 | -0.063 |     45.782 |    45.132 |      -0.651 |
| own_centre_guard      | 12-9         | 18122 |     0.482 |    0.479 | -0.003 |     44.237 |    44.025 |      -0.212 |
| own_centre_guard      | 8-5          | 26709 |     0.477 |    0.46  | -0.018 |     45.528 |    45.265 |      -0.264 |
| own_centre_guard      | 4-1          | 29367 |     0.424 |    0.403 | -0.021 |     45.092 |    44.835 |      -0.258 |
| opp_centre_guard      | 16-13        | 60218 |     0.646 |    0.628 | -0.018 |     60.73  |    60.537 |      -0.193 |
| opp_centre_guard      | 12-9         | 88082 |     0.616 |    0.605 | -0.01  |     55.069 |    55.1   |       0.031 |
| opp_centre_guard      | 8-5          | 63574 |     0.589 |    0.583 | -0.005 |     52.272 |    52.345 |       0.072 |
| opp_centre_guard      | 4-1          | 56484 |     0.566 |    0.568 |  0.001 |     49.543 |    49.658 |       0.114 |
| own_corner_guard      | 16-13        | 37623 |     0.527 |    0.541 |  0.014 |     31.719 |    32.137 |       0.417 |
| own_corner_guard      | 12-9         | 80117 |     0.511 |    0.542 |  0.031 |     35.195 |    35.725 |       0.531 |
| own_corner_guard      | 8-5          | 77395 |     0.524 |    0.531 |  0.007 |     40.784 |    40.974 |       0.19  |
| own_corner_guard      | 4-1          | 78389 |     0.517 |    0.509 | -0.009 |     43.116 |    43.112 |      -0.005 |
| opp_corner_guard      | 16-13        |  2422 |     0.683 |    0.654 | -0.029 |     72.386 |    72.864 |       0.478 |
| opp_corner_guard      | 12-9         | 16294 |     0.65  |    0.653 |  0.004 |     56.09  |    56.493 |       0.403 |
| opp_corner_guard      | 8-5          | 32199 |     0.646 |    0.653 |  0.007 |     49.24  |    49.455 |       0.216 |
| opp_corner_guard      | 4-1          | 40617 |     0.658 |    0.652 | -0.007 |     48.119 |    48.13  |       0.011 |
| open_house            | 16-13        | 63603 |     0.566 |    0.559 | -0.006 |     42.51  |    42.623 |       0.113 |
| open_house            | 12-9         | 14159 |     0.592 |    0.546 | -0.046 |     48.147 |    47.788 |      -0.359 |
| open_house            | 8-5          | 23770 |     0.601 |    0.588 | -0.013 |     48.065 |    48.049 |      -0.017 |
| open_house            | 4-1          | 27173 |     0.63  |    0.618 | -0.012 |     47.821 |    47.802 |      -0.019 |
| own_shot              | 16-13        | 22150 |     0.726 |    0.705 | -0.021 |     69.438 |    69.106 |      -0.333 |
| own_shot              | 12-9         | 52435 |     0.746 |    0.732 | -0.014 |     63.24  |    63.179 |      -0.061 |
| own_shot              | 8-5          | 56790 |     0.809 |    0.812 |  0.003 |     56.957 |    57.054 |       0.097 |
| own_shot              | 4-1          | 64861 |     0.945 |    0.96  |  0.014 |     54.306 |    54.526 |       0.22  |
| opp_shot              | 16-13        | 58983 |     0.518 |    0.519 |  0.001 |     31.861 |    32.128 |       0.267 |
| opp_shot              | 12-9         | 89501 |     0.481 |    0.494 |  0.014 |     36.789 |    37.024 |       0.234 |
| opp_shot              | 8-5          | 86142 |     0.43  |    0.432 |  0.002 |     39.998 |    40.1   |       0.103 |
| opp_shot              | 4-1          | 79908 |     0.301 |    0.278 | -0.023 |     41.018 |    40.837 |      -0.181 |
| own_two_plus          | 12-9         | 14234 |     0.913 |    0.881 | -0.032 |     74.415 |    73.941 |      -0.474 |
| own_two_plus          | 8-5          | 17622 |     1.045 |    1.054 |  0.009 |     63.701 |    63.795 |       0.094 |
| own_two_plus          | 4-1          | 22152 |     1.355 |    1.382 |  0.028 |     62.258 |    62.674 |       0.416 |
| opp_two_plus          | 16-13        |  8165 |     0.465 |    0.468 |  0.003 |     19.014 |    19.43  |       0.416 |
| opp_two_plus          | 12-9         | 34368 |     0.37  |    0.394 |  0.025 |     24.368 |    24.724 |       0.356 |
| opp_two_plus          | 8-5          | 35242 |     0.26  |    0.262 |  0.002 |     31.153 |    31.307 |       0.155 |
| opp_two_plus          | 4-1          | 33685 |    -0.001 |   -0.045 | -0.044 |     32.747 |    32.452 |      -0.295 |
| split_house           | 12-9         |  4922 |     0.904 |    0.888 | -0.016 |     73.507 |    73.099 |      -0.407 |
| split_house           | 8-5          |  5612 |     1.025 |    1.052 |  0.027 |     61.323 |    61.562 |       0.239 |
| split_house           | 4-1          |  6234 |     1.308 |    1.362 |  0.054 |     62.397 |    63.112 |       0.715 |
| split_flat            | 12-9         |   641 |     0.902 |    0.895 | -0.007 |     69.524 |    69.541 |       0.017 |
| split_flat            | 8-5          |  1041 |     0.969 |    1.036 |  0.067 |     58.8   |    60.322 |       1.522 |
| split_flat            | 4-1          |  1272 |     1.214 |    1.322 |  0.108 |     58.541 |    60.198 |       1.656 |
| split_staggered       | 12-9         |  4281 |     0.905 |    0.888 | -0.017 |     74.103 |    73.632 |      -0.471 |
| split_staggered       | 8-5          |  4571 |     1.038 |    1.056 |  0.018 |     61.898 |    61.845 |      -0.053 |
| split_staggered       | 4-1          |  4962 |     1.332 |    1.372 |  0.04  |     63.385 |    63.86  |       0.474 |
| own_shot_covered      | 16-13        | 14549 |     0.736 |    0.725 | -0.011 |     70.123 |    69.956 |      -0.167 |
| own_shot_covered      | 12-9         | 35732 |     0.761 |    0.745 | -0.016 |     65.23  |    65.186 |      -0.045 |
| own_shot_covered      | 8-5          | 33077 |     0.828 |    0.833 |  0.005 |     58.607 |    58.704 |       0.097 |
| own_shot_covered      | 4-1          | 35430 |     0.984 |    1.019 |  0.035 |     55.194 |    55.666 |       0.473 |
| deuce_loose           | 8-5          |  8894 |     0.918 |    0.934 |  0.016 |     54.838 |    55.216 |       0.378 |
| deuce_loose           | 4-1          | 12073 |     1.151 |    1.18  |  0.029 |     53.9   |    54.378 |       0.478 |
| steal_setup           | 16-13        |  4750 |     0.721 |    0.671 | -0.049 |     76.95  |    76.316 |      -0.635 |
| steal_setup           | 12-9         | 18370 |     0.689 |    0.65  | -0.039 |     67.764 |    67.443 |      -0.321 |
| steal_setup           | 8-5          | 10149 |     0.601 |    0.578 | -0.022 |     53.858 |    53.423 |      -0.435 |
| steal_setup           | 4-1          | 10771 |     0.537 |    0.524 | -0.012 |     47.345 |    47.144 |      -0.201 |
| steal_on              | 16-13        | 17073 |     0.52  |    0.516 | -0.005 |     35.241 |    35.376 |       0.136 |
| steal_on              | 12-9         | 55495 |     0.453 |    0.464 |  0.01  |     36.509 |    36.707 |       0.199 |
| steal_on              | 8-5          | 46561 |     0.368 |    0.36  | -0.008 |     40.08  |    40.094 |       0.014 |
| steal_on              | 4-1          | 42009 |     0.166 |    0.118 | -0.047 |     39.451 |    38.958 |      -0.493 |
| opp_exposed           | 16-13        | 48193 |     0.514 |    0.517 |  0.003 |     29.851 |    30.196 |       0.346 |
| opp_exposed           | 12-9         | 65536 |     0.526 |    0.543 |  0.017 |     37.735 |    38.028 |       0.293 |
| opp_exposed           | 8-5          | 83706 |     0.538 |    0.543 |  0.005 |     42.25  |    42.362 |       0.112 |
| opp_exposed           | 4-1          | 88725 |     0.532 |    0.524 | -0.007 |     43.682 |    43.668 |      -0.014 |
| open_shot_own         | 16-13        |  3043 |     0.665 |    0.646 | -0.019 |     58.546 |    58.597 |       0.051 |
| open_shot_own         | 12-9         |  5347 |     0.694 |    0.658 | -0.036 |     58.641 |    58.362 |      -0.278 |
| open_shot_own         | 8-5          |  9818 |     0.749 |    0.737 | -0.012 |     57.688 |    57.808 |       0.121 |
| open_shot_own         | 4-1          | 12098 |     0.857 |    0.852 | -0.004 |     53.018 |    53.144 |       0.126 |
| open_shot_opp         | 16-13        | 22725 |     0.519 |    0.51  | -0.009 |     32.49  |    32.701 |       0.21  |
| open_shot_opp         | 12-9         |  8480 |     0.528 |    0.473 | -0.054 |     41.257 |    40.837 |      -0.42  |
| open_shot_opp         | 8-5          | 13373 |     0.494 |    0.48  | -0.013 |     40.805 |    40.705 |      -0.1   |
| open_shot_opp         | 4-1          | 14273 |     0.444 |    0.423 | -0.02  |     43.245 |    43.087 |      -0.158 |
| shot_runback_straight | 16-13        | 29820 |     0.628 |    0.624 | -0.004 |     52.667 |    52.666 |      -0.001 |
| shot_runback_straight | 12-9         | 89071 |     0.584 |    0.586 |  0.002 |     49.061 |    49.176 |       0.116 |
| shot_runback_straight | 8-5          | 78019 |     0.567 |    0.564 | -0.003 |     48.202 |    48.21  |       0.008 |
| shot_runback_straight | 4-1          | 77859 |     0.551 |    0.539 | -0.012 |     46.783 |    46.653 |      -0.13  |
| shot_runback_angled   | 16-13        | 19701 |     0.537 |    0.534 | -0.003 |     32.574 |    32.792 |       0.218 |
| shot_runback_angled   | 12-9         | 35462 |     0.555 |    0.577 |  0.022 |     38.907 |    39.154 |       0.248 |
| shot_runback_angled   | 8-5          | 39855 |     0.591 |    0.612 |  0.022 |     43.033 |    43.32  |       0.287 |
| shot_runback_angled   | 4-1          | 36596 |     0.627 |    0.635 |  0.008 |     45.866 |    46.09  |       0.224 |
| lonely_steal          | 12-9         |  5843 |     0.708 |    0.701 | -0.007 |     62.776 |    62.794 |       0.018 |
| lonely_steal          | 8-5          |  8920 |     0.742 |    0.758 |  0.016 |     52.996 |    53.052 |       0.057 |
| lonely_steal          | 4-1          |  9645 |     0.768 |    0.774 |  0.006 |     52.629 |    52.61  |      -0.02  |
| lonely_steal_exposed  | 12-9         |  5558 |     0.705 |    0.695 | -0.01  |     62.705 |    62.743 |       0.038 |
| lonely_steal_exposed  | 8-5          |  8066 |     0.736 |    0.749 |  0.013 |     52.986 |    52.974 |      -0.012 |
| lonely_steal_exposed  | 4-1          |  8781 |     0.752 |    0.745 | -0.007 |     52.322 |    52.226 |      -0.096 |
| busy_house            | 12-9         | 15237 |     0.608 |    0.633 |  0.025 |     49.106 |    49.283 |       0.178 |
| busy_house            | 8-5          | 40003 |     0.593 |    0.598 |  0.005 |     44.237 |    44.241 |       0.004 |
| busy_house            | 4-1          | 58436 |     0.58  |    0.569 | -0.011 |     44.007 |    43.863 |      -0.144 |
| near_tie              | 16-13        |   356 |     0.66  |    0.681 |  0.021 |     61.25  |    61.588 |       0.338 |
| near_tie              | 12-9         |  5419 |     0.621 |    0.626 |  0.005 |     51.658 |    51.742 |       0.085 |
| near_tie              | 8-5          |  8036 |     0.617 |    0.62  |  0.003 |     47.738 |    47.874 |       0.136 |
| near_tie              | 4-1          | 10620 |     0.599 |    0.603 |  0.004 |     45.619 |    45.773 |       0.154 |

## What each configuration leaves the opponent

Before a stone (not the last), by who throws it: how often the configuration survives the stone, and the end's realised value (hammer-adjusted points, hammer team's view) when it survived and when it was wrecked. `model_gap` is the model's gap between the positions left; where `real_gap` is larger, the model under-credits keeping the configuration and under-charges losing it. The `_wp_pp` columns are the same gaps in percentage points of win probability.

| configuration         | thrower    |      n |   survives |   real_kept |   real_wrecked |   real_gap |   model_gap |   real_gap_wp_pp |   model_gap_wp_pp |
|:----------------------|:-----------|-------:|-----------:|------------:|---------------:|-----------:|------------:|-----------------:|------------------:|
| guards_only           | non-hammer |  17198 |      0.393 |       0.586 |          0.5   |      0.086 |       0.079 |           10.62  |            10.158 |
| guards_only           | hammer     |  29355 |      0.381 |       0.531 |          0.682 |     -0.151 |      -0.136 |           -7.632 |            -7.933 |
| own_centre_guard      | non-hammer |  40047 |      0.92  |       0.433 |          0.691 |     -0.258 |      -0.255 |           14.098 |            14.059 |
| own_centre_guard      | hammer     |  29738 |      0.853 |       0.464 |          0.335 |      0.129 |       0.137 |           -6.512 |            -6.329 |
| opp_centre_guard      | non-hammer | 111952 |      0.971 |       0.608 |          0.898 |     -0.289 |      -0.325 |            3.392 |             2.735 |
| opp_centre_guard      | hammer     | 141875 |      0.784 |       0.617 |          0.485 |      0.132 |       0.143 |           -7.259 |            -7.051 |
| own_corner_guard      | non-hammer | 141251 |      0.931 |       0.525 |          0.616 |     -0.091 |      -0.084 |           13.4   |            13.339 |
| own_corner_guard      | hammer     | 112690 |      0.989 |       0.532 |          0.42  |      0.112 |       0.075 |          -14.507 |           -14.323 |
| opp_corner_guard      | non-hammer |  41729 |      0.976 |       0.644 |          0.801 |     -0.158 |      -0.138 |           13.253 |            13.622 |
| opp_corner_guard      | hammer     |  38868 |      0.963 |       0.662 |          0.535 |      0.127 |       0.167 |          -15.125 |           -14.708 |
| open_house            | non-hammer |  73233 |      0.661 |       0.559 |          0.622 |     -0.063 |      -0.07  |          -23.582 |           -23.784 |
| open_house            | hammer     |  48606 |      0.593 |       0.579 |          0.531 |      0.049 |       0.127 |           19.162 |            20.047 |
| own_shot              | non-hammer | 132579 |      0.458 |       0.964 |          0.6   |      0.365 |       0.383 |           14.238 |            14.484 |
| own_shot              | hammer     |  54809 |      0.952 |       0.896 |          0.544 |      0.353 |       0.39  |            3.046 |             3.669 |
| opp_shot              | non-hammer | 111201 |      0.98  |       0.36  |          0.758 |     -0.398 |      -0.403 |           -4.378 |            -4.424 |
| opp_shot              | hammer     | 175929 |      0.607 |       0.362 |          0.667 |     -0.305 |      -0.316 |          -16.468 |           -16.495 |
| own_two_plus          | non-hammer |  42437 |      0.257 |       1.396 |          0.97  |      0.427 |       0.496 |           15.681 |            16.721 |
| own_two_plus          | hammer     |   9675 |      0.944 |       1.247 |          0.753 |      0.495 |       0.558 |           -3.065 |            -2.427 |
| opp_two_plus          | non-hammer |  29284 |      0.969 |       0.106 |          0.541 |     -0.435 |      -0.441 |            5.124 |             5.222 |
| opp_two_plus          | hammer     |  69214 |      0.392 |       0.112 |          0.464 |     -0.352 |      -0.38  |          -14.035 |           -14.256 |
| split_house           | non-hammer |  14562 |      0.118 |       1.452 |          1.018 |      0.434 |       0.501 |           11.914 |            13.011 |
| split_house           | hammer     |   1891 |      0.734 |       1.316 |          1.304 |      0.012 |      -0.062 |            2.709 |             2.103 |
| split_flat            | non-hammer |   2643 |      0.061 |       1.348 |          1.063 |      0.285 |       0.45  |           13.667 |            15.046 |
| split_flat            | hammer     |    260 |      0.346 |       1.107 |          1.504 |     -0.397 |      -0.383 |           14.625 |            13.062 |
| split_staggered       | non-hammer |  11919 |      0.122 |       1.44  |          1.015 |      0.426 |       0.486 |           11.876 |            12.983 |
| split_staggered       | hammer     |   1631 |      0.73  |       1.308 |          1.293 |      0.016 |      -0.066 |            2.241 |             1.632 |
| own_shot_covered      | non-hammer |  74646 |      0.534 |       0.922 |          0.661 |      0.261 |       0.286 |           15.864 |            16.165 |
| own_shot_covered      | hammer     |  38063 |      0.847 |       0.873 |          0.804 |      0.069 |       0.115 |           -3.059 |            -2.397 |
| deuce_loose           | non-hammer |  15884 |      0.25  |       1.341 |          0.875 |      0.466 |       0.449 |            7.76  |             7.665 |
| deuce_loose           | hammer     |   3640 |      0.83  |       1.24  |          1.042 |      0.198 |       0.228 |           -8.573 |            -8.216 |
| steal_setup           | non-hammer |  14246 |      0.944 |       0.634 |          1.048 |     -0.414 |      -0.413 |           -1.709 |            -1.536 |
| steal_setup           | hammer     |  26477 |      0.535 |       0.657 |          0.526 |      0.131 |       0.161 |           -6.643 |            -6.04  |
| steal_on              | non-hammer |  53575 |      0.883 |       0.262 |          0.519 |     -0.257 |      -0.219 |            5.395 |             5.682 |
| steal_on              | hammer     |  93406 |      0.512 |       0.28  |          0.569 |     -0.289 |      -0.278 |          -15.373 |           -15.221 |
| opp_exposed           | non-hammer | 119599 |      0.836 |       0.502 |          0.458 |      0.044 |       0.016 |           -9.866 |           -10.215 |
| opp_exposed           | hammer     | 140610 |      0.679 |       0.501 |          0.685 |     -0.184 |      -0.18  |          -18.139 |           -18.123 |
| open_shot_own         | non-hammer |  22617 |      0.202 |       1.083 |          0.596 |      0.487 |       0.436 |            7.57  |             6.745 |
| open_shot_own         | hammer     |   6417 |      0.783 |       0.907 |          0.749 |      0.158 |       0.259 |           11.027 |            12.249 |
| open_shot_opp         | non-hammer |  12691 |      0.717 |       0.362 |          0.452 |     -0.09  |      -0.111 |          -25.92  |           -25.953 |
| open_shot_opp         | hammer     |  40782 |      0.182 |       0.318 |          0.549 |     -0.231 |      -0.165 |           -9.332 |            -8.54  |
| shot_runback_straight | non-hammer | 125182 |      0.847 |       0.571 |          0.722 |     -0.151 |      -0.117 |            6.098 |             6.559 |
| shot_runback_straight | hammer     | 129122 |      0.749 |       0.563 |          0.546 |      0.017 |       0.032 |           -6.747 |            -6.485 |
| shot_runback_angled   | non-hammer |  73777 |      0.506 |       0.605 |          0.531 |      0.074 |       0.063 |           -3.137 |            -3.345 |
| shot_runback_angled   | hammer     |  49756 |      0.64  |       0.597 |          0.67  |     -0.073 |      -0.072 |           -9.182 |            -9.032 |
| lonely_steal          | non-hammer |  13783 |      0.341 |       0.745 |          0.547 |      0.198 |       0.297 |           21.39  |            22.33  |
| lonely_steal          | hammer     |   8215 |      0.501 |       0.626 |          1.123 |     -0.497 |      -0.482 |           -3.27  |            -2.999 |
| lonely_steal_exposed  | non-hammer |  12415 |      0.342 |       0.722 |          0.538 |      0.184 |       0.292 |           20.336 |            21.353 |
| lonely_steal_exposed  | hammer     |   7741 |      0.47  |       0.594 |          1.085 |     -0.491 |      -0.443 |           -6.126 |            -5.549 |
| busy_house            | non-hammer |  53215 |      0.866 |       0.584 |          0.703 |     -0.119 |      -0.086 |            9.9   |            10.169 |
| busy_house            | hammer     |  44093 |      0.872 |       0.595 |          0.586 |      0.009 |       0.005 |           -9.77  |            -9.698 |
| near_tie              | non-hammer |  11955 |      0.49  |       0.577 |          0.566 |      0.011 |       0.036 |            7.597 |             8.034 |
| near_tie              | hammer     |   9607 |      0.482 |       0.595 |          0.728 |     -0.133 |      -0.157 |           -0.781 |            -1.048 |

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
| M            | JACOBS B      |         40 | CAN     |    0.125 |  0.625 |       0.725 |       0.242 |   4.205 |          13 |  81.875 |
| M            | DROPKIN K     |         56 | USA     |    0.107 |  0.661 |       0.482 |       0.176 |   3.505 |          18 |  60.714 |
| M            | SCHWARZ B     |        114 | SUI     |    0.079 |  0.491 |       0.518 |       0.146 |   2.607 |          25 |  64.254 |
| M            | MOROZUMI Y    |         56 | JPN     |    0.054 |  0.554 |       0.571 |       0.133 |   3.149 |          16 |  68.304 |
| M            | MUSKATEWITZ M |        108 | GER     |    0.083 |  0.556 |       0.509 |       0.13  |   2.651 |          28 |  69.907 |
| M            | MOUAT B       |        186 | GBR/SCO |    0.108 |  0.554 |       0.602 |       0.129 |   3.818 |          42 |  70.968 |
| M            | GUSHUE B      |         62 | CAN     |    0.129 |  0.597 |       0.565 |       0.115 |   2.803 |          14 |  72.951 |
| M            | HOOD A        |         50 | NZL     |    0.16  |  0.56  |       0.46  |       0.107 |   1.926 |          10 |  61     |
| M            | SHUSTER J     |        126 | USA     |    0.087 |  0.635 |       0.46  |       0.088 |   2.526 |          24 |  61.706 |
| M            | DE CRUZ P     |         67 | SUI     |    0.134 |  0.194 |       0.343 |       0.074 |   2.183 |           2 |  73.507 |
| M            | ULSRUD T      |         60 | NOR     |    0.117 |  0.483 |       0.567 |       0.057 |   0.258 |           9 |  67.083 |
| M            | SCHWALLER Y   |        109 | SUI     |    0.083 |  0.44  |       0.422 |       0.052 |   2.186 |          11 |  66.435 |
| M            | RETORNAZ J    |        242 | ITA     |    0.107 |  0.463 |       0.442 |       0.049 |   1.881 |          48 |  58.574 |
| M            | WANG Z        |         48 | CHN     |    0.062 |  0.229 |       0.312 |       0.048 |   1.513 |           2 |  69.792 |
| M            | NICHOLS M     |         85 | CAN     |    0.118 |  0.471 |       0.424 |       0.045 |   1.592 |           6 |  68.529 |
| M            | PAETZ C       |         52 | SUI     |    0.154 |  0.365 |       0.269 |      -0.028 |   0.532 |           0 |  58.173 |
| M            | NERGAARD T    |         78 | NOR     |    0.09  |  0.321 |       0.41  |      -0.029 |   0.596 |           3 |  68.269 |
| M            | LEE J         |         44 | KOR     |    0.068 |  0.295 |       0.227 |      -0.029 |  -0.301 |           4 |  57.955 |
| M            | HOEIBERG M    |         43 | NOR     |    0.093 |  0.209 |       0.256 |      -0.03  |   0.561 |           1 |  60.465 |
| M            | BAUMANN A     |         54 | GER     |    0.093 |  0.37  |       0.426 |      -0.037 |   0.191 |          11 |  55.093 |
| M            | VAN DORP J    |         86 | NED     |    0.07  |  0.233 |       0.163 |      -0.043 |   0.115 |           3 |  54.651 |
| M            | MOSANER A     |        218 | ITA     |    0.087 |  0.381 |       0.344 |      -0.044 |   0.211 |          12 |  61.927 |
| M            | CERNOVSKY M   |        134 | CZE     |    0.097 |  0.478 |       0.321 |      -0.044 |   0.839 |           4 |  58.955 |
| M            | JURIK M       |         40 | CZE     |    0.025 |  0.25  |       0.225 |      -0.05  |   0.249 |           0 |  59.375 |
| M            | WALSTAD S     |         69 | NOR     |    0.101 |  0.565 |       0.333 |      -0.058 |  -0.991 |          11 |  51.087 |
| M            | YANAGISAWA R  |         43 | JPN     |    0.07  |  0.558 |       0.349 |      -0.066 |  -0.676 |           6 |  55.233 |
| M            | SMITH B       |         40 | NZL     |    0.075 |  0.375 |       0.15  |      -0.091 |  -0.742 |           0 |  47.5   |
| M            | TIMOFEEV A    |         42 | RUS     |    0.143 |  0.476 |       0.429 |      -0.122 |  -2.033 |           6 |  50     |
| M            | KIISKINEN K   |         41 | FIN     |    0.073 |  0.683 |       0.293 |      -0.149 |  -0.96  |           4 |  43.902 |
| M            | ZOU Q         |         43 | CHN     |    0.047 |  0.605 |       0.326 |      -0.176 |  -0.202 |           3 |  51.744 |

### W

| discipline   | player_key     |   runbacks | teams       |   angled |   busy |   lies_shot |   execution |   wp_pp |   big_makes |   grade |
|:-------------|:---------------|-----------:|:------------|---------:|-------:|------------:|------------:|--------:|------------:|--------:|
| W            | HOMAN R        |         49 | CAN         |    0.102 |  0.694 |       0.612 |       0.153 |   4.155 |          13 |  70.408 |
| W            | KUBESKOVA A    |         48 | CZE         |    0.062 |  0.562 |       0.438 |       0.15  |   0.145 |          14 |  54.167 |
| W            | PAETZ A        |        114 | SUI         |    0.096 |  0.588 |       0.57  |       0.144 |   3.415 |          29 |  63.816 |
| W            | SKASLIEN K     |         75 | NOR         |    0.093 |  0.547 |       0.52  |       0.13  |   2.118 |          17 |  59.667 |
| W            | HASSELBORG A   |        135 | SWE         |    0.074 |  0.652 |       0.533 |       0.097 |   2.897 |          32 |  63.519 |
| W            | FUJISAWA S     |         58 | JPN         |    0.103 |  0.621 |       0.431 |       0.088 |  -0.009 |          17 |  56.034 |
| W            | DUPONT M       |        126 | DEN         |    0.071 |  0.667 |       0.468 |       0.087 |   3.325 |          29 |  54.563 |
| W            | GIM E          |         61 | KOR         |    0.148 |  0.672 |       0.541 |       0.081 |   2.795 |          16 |  70.082 |
| W            | POLAT O        |         75 | TUR         |    0.093 |  0.493 |       0.4   |       0.068 |   1.792 |           5 |  69.333 |
| W            | KIM M          |         74 | KOR         |    0.041 |  0.473 |       0.419 |       0.062 |   2.396 |          11 |  64.527 |
| W            | LAWES K        |         46 | CAN         |    0.065 |  0.435 |       0.37  |       0.061 |   1.155 |           3 |  68.478 |
| W            | TIRINZONI S    |        112 | SUI         |    0.098 |  0.536 |       0.464 |       0.059 |   1.774 |           8 |  70.312 |
| W            | JENTSCH D      |         90 | GER         |    0.033 |  0.567 |       0.411 |       0.057 |   1.406 |          28 |  53.056 |
| W            | BIRCHARD S     |         40 | CAN         |    0.025 |  0.125 |       0.425 |       0.055 |   1.87  |           2 |  83.125 |
| W            | EINARSON K     |         60 | CAN         |    0.15  |  0.65  |       0.533 |       0.039 |   1.314 |          12 |  62.083 |
| W            | ABBES E        |         77 | GER         |    0.104 |  0.312 |       0.325 |      -0.005 |   0.204 |           4 |  59.091 |
| W            | KIM K          |         59 | KOR         |    0.153 |  0.492 |       0.254 |      -0.005 |   0.475 |           1 |  64.831 |
| W            | KNOCHENHAUER A |         79 | SWE         |    0.089 |  0.304 |       0.278 |      -0.008 |   0.831 |           0 |  64.241 |
| W            | SLOAN A        |         48 | GBR/SCO     |    0.104 |  0.312 |       0.333 |      -0.008 |   0.66  |           2 |  57.812 |
| W            | FLEURY T       |         42 | CAN         |    0.095 |  0.405 |       0.405 |      -0.009 |   1.177 |           1 |  64.881 |
| W            | MUIRHEAD E     |         78 | GBR/SCO     |    0.064 |  0.615 |       0.5   |      -0.011 |  -0.242 |          16 |  54.167 |
| W            | CONSTANTINI S  |        121 | ITA         |    0.074 |  0.537 |       0.421 |      -0.016 |   1.071 |          24 |  57.231 |
| W            | DONG Z         |         40 | CHN         |    0.05  |  0.4   |       0.3   |      -0.024 |   0.38  |           1 |  63.75  |
| W            | DUPONT D       |         58 | DEN         |    0.121 |  0.431 |       0.241 |      -0.036 |   0.3   |           1 |  53.448 |
| W            | HAN Y          |         42 | CHN         |    0.143 |  0.762 |       0.262 |      -0.056 |  -0.748 |           5 |  60.119 |
| W            | HALSE M        |         82 | DEN         |    0.085 |  0.476 |       0.317 |      -0.056 |  -0.331 |           5 |  57.927 |
| W            | DODDS J        |         80 | GBR/SCO     |    0.088 |  0.275 |       0.238 |      -0.058 |   0.361 |           3 |  55.938 |
| W            | MORRISON R     |         55 | GBR/SCO     |    0.073 |  0.582 |       0.418 |      -0.118 |   0.391 |          12 |  51.364 |
| W            | KOVALEVA A     |         48 | RCF/ROC/RUS |    0.125 |  0.625 |       0.396 |      -0.12  |  -0.79  |           6 |  50.532 |
| W            | KIM E          |         61 | KOR         |    0.082 |  0.689 |       0.377 |      -0.122 |  -1.674 |           9 |  45.492 |

## Scenario probes

One call family from one kind of position, split by what the shot left. `model_v_after` and `model_wp_after` are the model's value of the position the shot left; `real_v` and `real_wp` what the ends from those positions were actually worth; `pg_throw` and `pg_throw_wp_pp` the execution credited. Where the model's gap between two states is smaller than the realised gap, it under-credits the make and under-charges the miss.

### Split house restored, and the walk

Hammer team's hit, stones 6-14, one stone each in the house and no guards. The make restores the split; whether it restores a flat split (the double nearly off) or a staggered one (the walked split, double on) is what the opponent is left.

| state                     |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| opponent still in         |  73 |           0.528 |    0.524 |     -0.21  |           43.906 |    43.675 |           -3.037 |           0.141 |          0.164 |         0.206 |        0.219 |  18.403 |
| other                     |   2 |           0.54  |    0.582 |     -0.276 |           86.156 |    87.866 |           -1.226 |           0.049 |          0     |         0.044 |        0     |  50     |
| rolled out (one in)       | 207 |           0.594 |    0.599 |     -0.211 |           54.993 |    54.83  |           -2.698 |           0.052 |          0.063 |         0.102 |        0.126 |  57.367 |
| split restored, flat      | 196 |           0.992 |    1.082 |      0.156 |           55.056 |    56.657 |            2.101 |           0.047 |          0.02  |         0.525 |        0.602 |  99.872 |
| split restored, staggered | 668 |           0.967 |    0.972 |      0.151 |           55.002 |    55.255 |            1.832 |           0.051 |          0.045 |         0.49  |        0.491 |  98.129 |
| two in, not split         | 103 |           0.923 |    0.658 |      0.118 |           52.59  |    49.605 |            1.393 |           0.05  |          0.029 |         0.437 |        0.184 |  90.049 |

### Peel with hammer, last end, tied

Hammer team's peel, double or take-out, stones 5-8, last end tied with hammer, two or more guards up. The peel gives up points expectation to take the steal away; the question is whether the second is credited for that in win probability, and charged for the miss.

| state               |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| all guards gone     |  69 |           0.444 |    0.449 |      0.005 |           79.898 |    81.159 |            3.566 |           0.198 |          0.188 |         0.197 |        0.174 |  98.551 |
| none removed        | 276 |           0.396 |    0.255 |     -0.016 |           76.141 |    69.479 |            0.031 |           0.237 |          0.304 |         0.187 |        0.138 |  64.455 |
| one or more removed | 899 |           0.426 |    0.398 |     -0.01  |           78.574 |    78.955 |            0.871 |           0.212 |          0.209 |         0.189 |        0.161 |  96.051 |

### Peel with hammer, last end, down one

Hammer team's peel, double or take-out, stones 5-8, last end down one with hammer, two or more guards up. The peel gives up points expectation to take the steal away; the question is whether the second is credited for that in win probability, and charged for the miss.

| state               |   n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:--------------------|----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| all guards gone     |   2 |           0.485 |    0.418 |      0.036 |           41.553 |    23.812 |            1.247 |           0.259 |          0     |         0.318 |        0     | 100     |
| none removed        | 200 |           0.459 |    0.497 |      0.014 |           41.848 |    41.81  |            0.5   |           0.312 |          0.295 |         0.337 |        0.33  |  73.625 |
| one or more removed | 104 |           0.383 |    0.693 |      0.019 |           39.263 |    50.276 |            1.136 |           0.333 |          0.202 |         0.309 |        0.413 |  88.702 |

### Come-around behind a corner guard

Hammer team's draw or freeze, stones 4-8, with its own corner guard up and not lying shot.

| state              |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:-------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| not shot rock      | 13186 |           0.442 |    0.489 |     -0.039 |           24.819 |    25.264 |           -0.35  |           0.268 |          0.247 |         0.304 |        0.316 |  67.779 |
| shot rock, covered |  4037 |           0.651 |    0.656 |      0.06  |           42.96  |    43.239 |            0.815 |           0.201 |          0.221 |         0.366 |        0.385 |  90.891 |
| shot rock, open    |   776 |           0.571 |    0.638 |      0.004 |           37.683 |    39.177 |           -0.091 |           0.195 |          0.198 |         0.309 |        0.353 |  76.675 |

### Centre guard without hammer

Non-hammer team's guard or front, stones 1 and 3.

| state                       |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| centre guard placed         | 29128 |           0.638 |    0.625 |      0.006 |           61.935 |    61.845 |            0.1   |           0.208 |          0.213 |         0.342 |        0.337 |  93.212 |
| in the house                |  2285 |           0.589 |    0.613 |      0.012 |           49.427 |    50.11  |            0.131 |           0.191 |          0.182 |         0.305 |        0.311 |  28.743 |
| neither (through or corner) |   453 |           0.731 |    0.803 |     -0.061 |           73.638 |    75.051 |           -0.785 |           0.17  |          0.199 |         0.372 |        0.411 |  52.865 |

### Guard the steal or take the house: the hammer team counts one behind

Non-hammer team to throw, stones 9-14, lying one in the open with the hammer team counts one behind. Guard it and keep the steal (a tight guard, under 8 ft in front, leaves the easier runback), or remove a hammer stone and settle for holding the hammer team to less.

| state                                   |    n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------------------|-----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| guarded long                            | 1124 |           0.451 |    0.477 |      0.036 |           58.704 |    59.05  |            0.645 |           0.279 |          0.268 |         0.287 |        0.296 |  87.478 |
| guarded tight (runback from under 8 ft) | 1136 |           0.394 |    0.455 |      0.077 |           49.895 |    50.633 |            1.147 |           0.286 |          0.262 |         0.262 |        0.266 |  88.138 |
| hammer now lies shot                    |  137 |           0.9   |    0.812 |     -0.372 |           36.282 |    33.761 |           -4.505 |           0.113 |          0.117 |         0.499 |        0.438 |  32.482 |
| hammer stone removed                    | 3244 |           0.377 |    0.364 |      0.101 |           29.145 |    29.153 |            1.302 |           0.199 |          0.195 |         0.181 |        0.174 |  91.014 |
| other                                   | 2244 |           0.674 |    0.652 |     -0.157 |           36.516 |    36.404 |           -1.697 |           0.182 |          0.189 |         0.397 |        0.387 |  64.966 |

### Guard the steal or take the house: the hammer team counts two or more behind (a lonely steal)

Non-hammer team to throw, stones 9-14, lying one in the open with the hammer team counts two or more behind (a lonely steal). Guard it and keep the steal (a tight guard, under 8 ft in front, leaves the easier runback), or remove a hammer stone and settle for holding the hammer team to less.

| state                                   |    n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:----------------------------------------|-----:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| guarded long                            |  424 |           0.684 |    0.608 |      0.026 |           66.12  |    65.199 |            0.909 |           0.257 |          0.264 |         0.393 |        0.342 |  86.144 |
| guarded tight (runback from under 8 ft) |  403 |           0.596 |    0.688 |      0.116 |           59.177 |    60.426 |            1.72  |           0.266 |          0.201 |         0.357 |        0.362 |  87.779 |
| hammer now lies shot                    |   83 |           1.06  |    0.952 |     -0.359 |           38.499 |    37.703 |           -3.773 |           0.119 |          0.169 |         0.568 |        0.518 |  46.951 |
| hammer stone removed                    | 1499 |           0.63  |    0.702 |      0.054 |           32.93  |    33.783 |            0.579 |           0.187 |          0.153 |         0.37  |        0.392 |  86.391 |
| other                                   |  521 |           0.95  |    0.932 |     -0.22  |           51.569 |    50.861 |           -2.571 |           0.171 |          0.175 |         0.509 |        0.501 |  60.721 |

### The steal is on

Hammer team to throw, stones 10-14, the opponent lying shot behind cover. Any call.

| state                    |     n |   model_v_after |   real_v |   pg_throw |   model_wp_after |   real_wp |   pg_throw_wp_pp |   model_p_steal |   real_p_steal |   model_p_two |   real_p_two |   grade |
|:-------------------------|------:|----------------:|---------:|-----------:|-----------------:|----------:|-----------------:|----------------:|---------------:|--------------:|-------------:|--------:|
| hammer lies shot         | 15481 |           0.739 |    0.714 |      0.246 |           50.066 |    49.709 |            3.402 |           0.17  |          0.177 |         0.399 |        0.386 |  90.164 |
| opponent shot, open      |  9071 |           0.321 |    0.279 |      0.019 |           50.416 |    49.768 |            0.436 |           0.272 |          0.299 |         0.191 |        0.181 |  66.881 |
| steal still on (covered) | 18734 |           0.15  |    0.064 |     -0.082 |           35.479 |    34.438 |           -1.029 |           0.395 |          0.426 |         0.206 |        0.182 |  57.267 |
