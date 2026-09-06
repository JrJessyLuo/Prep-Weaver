## Pivot

Definition: Use `Pivot` when a table is already long/key-value style and target columns appear as values in an attribute/field column.

Pattern:
Raw table preview:
```text
raceId | attribute | value
---|---|---
1 | "year" | 2009
1 | "round" | 1
1 | "name" | "Australian Grand Prix"
2 | "year" | 2009
2 | "round" | 2
```
Target schema:
```sql
CREATE TABLE T (`raceId` INT, `year` INT, `round` INT, `name` VARCHAR(255));
```
Correct operation:
```json
{"op":"Pivot","params":{"index":["raceId"],"columns":"attribute","values":"value","aggfunc":"first"},"table_indices":[0]}
```
Expected effect: distinct values from `attribute` become columns; `value` provides cell values.

Use Pivot when target column names are visible in cell values. Use Transpose when target column names are row labels in the first column of a wide transposed table.
