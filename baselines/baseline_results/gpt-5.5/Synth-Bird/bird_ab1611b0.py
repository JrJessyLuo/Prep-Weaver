import pandas as pd

drivers = tables["table_1"]
results_df = tables["table_2"]

top_driver_id = (
    results_df.loc[results_df["fastestLapSpeed"].notna()]
    .sort_values("fastestLapSpeed", ascending=False)
    .head(1)["driverId"]
    .iloc[0]
)

out = drivers.loc[drivers["driverId"] == top_driver_id, ["nationality"]].drop_duplicates().reset_index(drop=True)

result = {"fastest_lap_driver_nationality": out}
