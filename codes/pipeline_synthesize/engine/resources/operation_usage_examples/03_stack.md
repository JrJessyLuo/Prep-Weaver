## Stack

Definition: Use `Stack` when many sibling wide columns should become rows, usually to create an attribute/value or variable/value target schema.

Pattern:
Raw table preview:
```text
student_id | math_2020 | math_2021 | math_2022
---|---|---|---
1 | 80 | 85 | 90
2 | 70 | 75 | 78
```
Target schema:
```sql
CREATE TABLE T (`student_id` INT, `year_metric` VARCHAR(64), `score` DOUBLE);
```
Correct operation:
```json
{"op":"Stack","params":{"id_vars":["student_id"],"value_vars":["math_2020","math_2021","math_2022"],"var_name":"year_metric","value_name":"score"},"table_indices":[0]}
```
Expected effect: wide sibling columns become rows with `year_metric` holding old column names and `score` holding old values.

For very wide tables, use `"value_vars":"__all_except_id_vars__"` instead of enumerating hundreds of columns.
