import pandas as pd

# Tables are preloaded in a dict named `tables`
drivers = tables["table_1"]   # bird_bb2a300c_input_0.pkl
races = tables["table_2"]     # bird_bb2a300c_input_1.pkl
results = tables["table_3"]   # bird_bb2a300c_input_2.pkl
status = tables["table_13"]   # formula_1_status.pkl

# Filter races to 2007-2009
races_070809 = races.loc[races["year"].isin([2007, 2008, 2009])].copy()
race_ids_070809 = races_070809["raceId"].tolist()

# Get Japanese driverIds
jpn_driver_ids = (
    drivers.loc[drivers["nationality"].eq("Japanese"), "driverId"]
    .unique()
    .tolist()
)

# Filter results to 2007-2009 races and Japanese drivers
results_jpn_070809 = results[
    results["raceId"].isin(race_ids_070809) & results["driverId"].isin(jpn_driver_ids)
].copy()

# Join races to get year, and status to get status text
results_jpn_070809 = (
    results_jpn_070809.merge(races_070809[["raceId", "year"]], on="raceId", how="inner")
    .merge(status, on="statusId", how="left")
)

# Aggregate per year: total starts vs finished, and completion percentage
completion_by_year = (
    results_jpn_070809.groupby("year", as_index=False)
    .agg(
        total_starts=("resultId", "size"),
        finished=("status", lambda s: (s == "Finished").sum()),
    )
)

completion_by_year["completion_pct"] = (
    completion_by_year["finished"] / completion_by_year["total_starts"] * 100
).round(2)

completion_by_year = completion_by_year.sort_values("year").reset_index(drop=True)

# Final answer
result = {"japanese_driver_completion_pct_2007_2009": completion_by_year}