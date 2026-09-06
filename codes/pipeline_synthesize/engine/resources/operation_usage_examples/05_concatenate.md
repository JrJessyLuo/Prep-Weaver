## Concatenate

Definition: Use `Concatenate` when a target field is composed from multiple existing columns, such as date, address, full name, or code.

Pattern:
Raw table preview:
```text
event_id | location_prefix | location_suffix
---|---|---
1 | "MU" | "215"
2 | "Campus" | "Stadium"
```
Target schema:
```sql
CREATE TABLE T (`event_id` INT, `location` VARCHAR(255));
```
Correct operation:
```json
{"op":"Concatenate","params":{"concatenate_columns":["location_prefix","location_suffix"],"target_column":"location","func":"def transform(row):
    a = row.get('location_prefix')
    b = row.get('location_suffix')
    if pd.notna(a) and pd.notna(b):
        return str(a) + ' ' + str(b)
    return None"},"table_indices":[0]}
```
Expected effect: creates `location` with values such as `MU 215`.

Use Concatenate when the target column does not exist but can be deterministically assembled from visible columns.
