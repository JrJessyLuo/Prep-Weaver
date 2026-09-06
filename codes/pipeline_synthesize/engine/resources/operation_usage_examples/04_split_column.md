## SplitColumn

Definition: Use `SplitColumn` when one packed/composite source column contains multiple target fields.

Pattern:
Raw table preview:
```text
country_id_name | population
---|---
"1-Belgium" | 11000000
"2-England" | 56000000
```
Target schema:
```sql
CREATE TABLE T (`country_id` INT, `name` VARCHAR(255), `population` INT);
```
Correct operation:
```json
{"op":"SplitColumn","params":{"source_column":"country_id_name","target_columns":["country_id","name"],"func":"def transform(s):
    parts = str(s).split('-', 1)
    return [parts[0], parts[1] if len(parts) > 1 else None]"},"table_indices":[0]}
```
Expected effect: creates `country_id` and `name` from the packed value. The source column must already exist in the current table.

Use SplitColumn before Pivot/Join when a later operation needs a key or attribute that is packed inside one column.
