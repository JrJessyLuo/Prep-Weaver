## StandardizeString

Definition: Use `StandardizeString` when a target text column exists but values need normalization for matching/filtering/joining.

Pattern:
Raw table preview:
```text
status
---
" Gold "
"gold"
"GOLD"
```
Target schema:
```sql
CREATE TABLE T (`status` VARCHAR(64));
```
Correct operation:
```json
{"op":"StandardizeString","params":{"column_name":"status","func":"def transform(s):
    return str(s).strip().lower()"},"table_indices":[0]}
```
Expected effect: values become consistent, e.g. `gold`.

Do not use StandardizeString to fix a column that contains values from the wrong semantic field; use rewrite/replace with structural repair instead.
