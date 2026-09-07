import pandas as pd

races = tables["table_1"]
results_df = tables["table_2"]
status = tables["table_13"]

# 2008 Chinese Grand Prix raceId
race_id = races.loc[(races["year"] == 2008) & (races["name"] == "Chinese Grand Prix"), "raceId"].iloc[0]

# Results for that race + status text
race_results = results_df[results_df["raceId"] == race_id].merge(status, on="statusId", how="left")

# Drivers who finished (including lapped finishers like "+1 Lap", "+2 Laps", etc.)
finished_mask = (
    (race_results["status"] == "Finished")
    | race_results["status"].astype(str).str.match(r"^\+\d+\s+Lap(s)?$", na=False)
)
finishers = race_results.loc[finished_mask, "driverId"].dropna().unique()

# Drivers who have participated in F1 races (appear in results table at least once)
f1_participants = results_df["driverId"].dropna().unique()

count_val = int(pd.Index(finishers).isin(f1_participants).sum())

result = {
    "finished_drivers_participated_in_f1_count": pd.DataFrame(
        {"num_drivers": [count_val]}
    )
}
