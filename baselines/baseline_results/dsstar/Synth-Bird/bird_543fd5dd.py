import pandas as pd
import re

# Tables (already loaded)
races = tables["table_1"]
results_tbl = tables["table_2"]
drivers = tables["table_8"]
status_lu = tables["table_13"]

# --- Find the 2008 Chinese Grand Prix raceId (same as reference logic) ---
mask = (races["year"] == 2008) & (races["name"] == "Chinese Grand Prix")
chinese_gp_2008 = races.loc[mask].copy()
raceId_2008_chinese_gp = int(chinese_gp_2008.iloc[0]["raceId"])

# --- Load results for that race and join statuses ---
results_race = results_tbl.loc[results_tbl["raceId"] == raceId_2008_chinese_gp].copy()
results_race = results_race.merge(status_lu, on="statusId", how="left")

# Determine which column to use for "position order not null"
pos_order_col = None
for candidate in ["positionOrder", "positionorder", "position_order"]:
    if candidate in results_race.columns:
        pos_order_col = candidate
        break
if pos_order_col is None:
    for candidate in ["position", "order", "rank"]:
        if candidate in results_race.columns:
            pos_order_col = candidate
            break
if pos_order_col is None:
    raise KeyError(
        "Could not find a position/order column (expected 'positionOrder' or similar) in results table. "
        f"Available columns: {list(results_race.columns)}"
    )

# Finisher criterion (same as reference):
# - positionOrder (or similar) not null
# - status == 'Finished' OR status like '+<number> Laps'
status_series = results_race["status"].astype("string")
is_finished_status = status_series.eq("Finished")
is_plus_laps_status = status_series.str.match(r"^\+\d+\s+Laps?$", na=False)
pos_not_null = results_race[pos_order_col].notna()

finishers = results_race.loc[pos_not_null & (is_finished_status | is_plus_laps_status)].copy()
finished_driver_ids = sorted(finishers["driverId"].dropna().astype(int).unique().tolist())

# --- Among those finishers, count how many have participated in F1 races ---
# Operationalized as: driverId exists in drivers table (i.e., is a known F1 driver record).
driver_ids_in_drivers = set(drivers["driverId"].dropna().astype(int).unique().tolist())
count_participated = sum(1 for d in finished_driver_ids if d in driver_ids_in_drivers)

answer_df = pd.DataFrame(
    [{"count_drivers_finished_and_participated_in_f1": int(count_participated)}]
)

result = {"answer": answer_df}