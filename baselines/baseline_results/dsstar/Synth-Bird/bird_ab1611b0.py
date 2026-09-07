import pandas as pd

# Tables are already loaded in-scope as `tables`
drivers = tables["table_1"]   # bird_ab1611b0_input_0.pkl
results = tables["table_2"]   # bird_ab1611b0_input_1.pkl

# Find the driver(s) with the global maximum fastestLapSpeed
max_fastest_lap_speed = results["fastestLapSpeed"].max(skipna=True)
max_speed_rows = results.loc[results["fastestLapSpeed"] == max_fastest_lap_speed, ["driverId"]].dropna()

# Join to drivers to get nationality
answer_df = (
    max_speed_rows.drop_duplicates()
    .merge(drivers[["driverId", "nationality"]], on="driverId", how="left")
    .loc[:, ["nationality"]]
    .dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)

# Final answer per evaluation convention
result = {"fastest_lap_speed_driver_nationality": answer_df}