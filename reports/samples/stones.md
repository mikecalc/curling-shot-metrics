# The life of a stone

Every stone of every end followed through the diagrams: 2,435,437 stone positions over 37,623 ends, 36,024 of them with a final diagram. How each stone got to where it is after a shot: unmoved 71.6%, the thrown stone (marked) 11.9%, new without a mark 8.7% (almost all thrown stones whose marker is missing), moved 7.7%.

## What a stone ends up doing

For a stone at a given place and stage of the end, the share that, when the end is over, **count**, **cover** a counting stone of their own team (in front of it within a stone's width, not counting themselves), or **back up** a counting stone of the other team (behind it within two stone widths). A stone removed before the end does none of the three. Stones with 12 or more rocks still to come:

| team       | zone              |   r_count |   r_cover |   r_backs_opp |     n |
|:-----------|:------------------|----------:|----------:|--------------:|------:|
| hammer     | centre guard <6ft |       2.4 |       9.8 |           0   |  5307 |
| hammer     | centre guard long |       0.3 |      12.7 |           0.3 |  1090 |
| hammer     | corner guard <6ft |       0.6 |       7.8 |           0   | 49687 |
| hammer     | corner guard long |       0.2 |       7.9 |           0   | 12448 |
| hammer     | house back 4ft    |      12.8 |       0.4 |           3.4 |  5883 |
| hammer     | house back 8-12   |      10.3 |       0.3 |           0.9 |  9685 |
| hammer     | house front 4ft   |      14   |       0.5 |           1   | 18167 |
| hammer     | house front 8-12  |       8.4 |       2.1 |           0.2 | 24067 |
| hammer     | out               |       1.6 |       0   |           0.2 |  1223 |
| non-hammer | centre guard <6ft |       0.5 |       3.3 |           0.1 | 70612 |
| non-hammer | centre guard long |       0.1 |       3.6 |           0.1 | 20063 |
| non-hammer | corner guard <6ft |       0.5 |       1.9 |           0   |  3765 |
| non-hammer | corner guard long |       0.1 |       1.3 |           0   |  1015 |
| non-hammer | house back 4ft    |       5.4 |       0   |           5.2 | 14001 |
| non-hammer | house back 8-12   |       3.6 |       0   |           2.9 |  8206 |
| non-hammer | house front 4ft   |       6.6 |       0.2 |           1.9 | 41650 |
| non-hammer | house front 8-12  |       3.1 |       1.2 |           0.8 | 34073 |
| non-hammer | out               |       0.3 |       0   |           1.2 |   861 |

A non-hammer stone behind the tee backs up an opponent's counter about as often as it counts itself; the same stone in front of the tee counts three times as often as it helps the other side. Guards almost never count themselves; their value is in covering. The full table by stage of the end is in `stones_roles.csv`.

## Late risers

Of the stones in play after stone 8 that count when the end is over, 38% were not counting then: a stone left in play that became a counter. Where they were after stone 8:

| zone              |   share |
|:------------------|--------:|
| house front 8-12  |    39.3 |
| house back 8-12   |    23   |
| house front 4ft   |    18.7 |
| house back 4ft    |     7.1 |
| centre guard <6ft |     6   |
| corner guard <6ft |     4.5 |
| out               |     0.7 |
| centre guard long |     0.3 |
| corner guard long |     0.3 |

## How flat is the model?

The calibration slope of the end's realised value (hammer-adjusted points) on the model's value before each stone, by stage of the end. At 1 the model's differences between positions are the right size; under 1 they are too small. `sd` is the spread of the model's values.

| rocks_left   |      n |   slope (current model) |   sd (current) |   slope (final-label model) |   sd (final-label) |
|:-------------|-------:|------------------------:|---------------:|----------------------------:|-------------------:|
| 16-12        | 188120 |                   1.017 |          0.162 |                       0.995 |              0.17  |
| 11-8         | 150495 |                   1.003 |          0.232 |                       0.978 |              0.241 |
| 7-4          | 150494 |                   1.05  |          0.354 |                       1.059 |              0.348 |
| 3-1          | 112554 |                   1.097 |          0.553 |                       1.105 |              0.544 |
