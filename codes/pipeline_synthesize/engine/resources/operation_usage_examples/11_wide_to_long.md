## WideToLong

Definition: Use `WideToLong` when repeated column groups share a stub and suffix, e.g. `fee_monthly`, `fee_weekly`, or `score_1`, `score_2`.

Pattern:
Raw table preview:
```text
account_id | district_id | fee_monthly | fee_weekly
---|---|---|---
1 | 10 | "2020-01-01" | "2020-01-07"
```
Target schema:
```sql
CREATE TABLE T (`account_id` INT, `district_id` INT, `fee_type` VARCHAR(64), `fee_date` DATE);
```
Correct operation:
```json
{"op":"WideToLong","params":{"subnames":["fee"],"i":["account_id","district_id"],"j":"fee_type","sep":"_","suffix":".+"},"table_indices":[0]}
```
Expected effect: repeated wide groups become long rows keyed by `fee_type`.
