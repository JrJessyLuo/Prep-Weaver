## CastType

Definition: Use `CastType` when the target column exists but its dtype does not satisfy the SQL type contract.

Pattern:
Raw table preview:
```text
account_id | amount
---|---
"1" | "12.50"
"2" | "8.00"
```
Target schema:
```sql
CREATE TABLE T (`account_id` INT, `amount` FLOAT);
```
Correct operation:
```json
{"op":"CastType","params":{"column":"account_id","dtype":"int"},"table_indices":[0]}
```
Expected effect: converts existing values; it does not create missing columns. Use another CastType turn for `amount` if needed.
