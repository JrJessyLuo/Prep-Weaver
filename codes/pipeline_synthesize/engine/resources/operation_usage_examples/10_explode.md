## Explode

Definition: Use `Explode` when one cell contains multiple row-level values, especially comma-separated IDs/links.

Pattern:
Raw table preview:
```text
event_id | link_to_member
---|---
1 | "m1,m2,m3"
2 | "m4"
```
Target schema:
```sql
CREATE TABLE T (`event_id` INT, `link_to_member` VARCHAR(64));
```
Correct operation:
```json
{"op":"Explode","params":{"column":"link_to_member","split_comma":true},"table_indices":[0]}
```
Expected effect: one row per member link.
