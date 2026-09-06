## DropColumn

Definition: Use `DropColumn` only after required target columns and join keys are safe, to remove misleading or unusable extra columns.

Pattern:
Raw table preview:
```text
id | name | unused_blob
---|---|---
1 | "A" | "..."
```
Target schema:
```sql
CREATE TABLE T (`id` INT, `name` VARCHAR(255));
```
Correct operation:
```json
{"op":"DropColumn","params":{"drop_columns":["unused_blob"]},"table_indices":[0]}
```
Expected effect: removes existing columns only. Do not drop columns listed as required, primary key, or declared join keys.
