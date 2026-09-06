## StandardizeDatetime

Definition: Use `StandardizeDatetime` when a date/time column exists and should be normalized to a consistent format.

Pattern:
Raw table preview:
```text
issued
---
"1/5/2020"
"2020-02-03"
```
Target schema:
```sql
CREATE TABLE T (`issued` DATE);
```
Correct operation:
```json
{"op":"StandardizeDatetime","params":{"column_name":"issued","date_format":"%Y-%m-%d"},"table_indices":[0]}
```
Expected effect: parseable dates become ISO-like strings. It does not create a date from separate year/month/day columns; use Concatenate first for that.
