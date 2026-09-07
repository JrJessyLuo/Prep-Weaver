import pandas as pd

drivers = tables["table_1"].copy()
raw_map = tables["table_2"].copy()

# Make duplicate column names unique (e.g., '1', '1' -> '1', '1.1', ...)
seen = {}
new_cols = []
for c in raw_map.columns.astype(str):
    if c in seen:
        seen[c] += 1
        new_cols.append(f"{c}.{seen[c]}")
    else:
        seen[c] = 0
        new_cols.append(c)
raw_map.columns = new_cols

value_cols = [c for c in raw_map.columns if c != "Driver_ID"]

long_map = raw_map.melt(
    id_vars=["Driver_ID"],
    value_vars=value_cols,
    var_name="Driver_ID_col",
    value_name="Vehicle_ID"
)

long_map["Driver_ID"] = pd.to_numeric(
    long_map["Driver_ID_col"].astype(str).str.extract(r"^(\d+)")[0],
    errors="coerce"
)
long_map["Vehicle_ID"] = pd.to_numeric(long_map["Vehicle_ID"], errors="coerce")

drivers_with_cars = set(long_map.loc[long_map["Vehicle_ID"].notna(), "Driver_ID"].dropna().astype(int).unique())
num_without_cars = int((~drivers["Driver_ID"].isin(drivers_with_cars)).sum())

result = {
    "drivers_without_cars_count": pd.DataFrame({"number_of_drivers_without_cars": [num_without_cars]})
}
