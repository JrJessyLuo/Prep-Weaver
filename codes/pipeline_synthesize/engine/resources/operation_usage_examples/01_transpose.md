## Transpose

Definition: Use `Transpose` when real attributes are stored as row labels, often in the first column, and examples/records are stored across many numbered columns.

Pattern:
Raw table preview:
```text
id | 101 | 102 | 103
---|---|---|---
season | "2016" | "2015" | "2014"
home_team_goal | 2 | 0 | 1
away_team_goal | 2 | 1 | 1
league_id | 1 | 1 | 2
```
Target schema:
```sql
CREATE TABLE T (`id` INT, `season` VARCHAR(32), `home_team_goal` DOUBLE, `away_team_goal` DOUBLE, `league_id` INT);
```
Correct operation:
```json
{"op":"Transpose","params":{"use_first_column_as_header":true,"new_index_column":"id"},"table_indices":[0]}
```
Expected effect: first-column row labels become output columns (`season`, `home_team_goal`, `away_team_goal`, `league_id`); old wide headers become row/entity ids.

Do not use Stack/Pivot for this pattern unless the target schema is long-form attribute/value rows.
