## Rename

Definition: Use `Rename` when an existing column has the right values but the header does not match the target schema.

Pattern:
Raw table preview:
```text
dr | fn | ln | nat
---|---|---|---
"hamilton" | "Lewis" | "Hamilton" | "British"
```
Target schema:
```sql
CREATE TABLE T (`driverRef` VARCHAR(64), `forename` VARCHAR(255), `surname` VARCHAR(255), `nationality` VARCHAR(255));
```
Correct operation:
```json
{"op":"Rename","params":{"rename_map":[{"old_name":"dr","new_name":"driverRef"},{"old_name":"fn","new_name":"forename"},{"old_name":"ln","new_name":"surname"},{"old_name":"nat","new_name":"nationality"}]},"table_indices":[0]}
```
Expected effect: only column names change; values are preserved.

Do not use Rename to create new values or parse packed columns.
