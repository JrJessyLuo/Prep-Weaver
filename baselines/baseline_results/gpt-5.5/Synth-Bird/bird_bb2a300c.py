import pandas as pd

drivers = tables["table_1"]
races = tables["table_2"]
results_df = tables["table_3"]
status = tables["table_13"]

# Japanese drivers
jp_driver_ids = drivers.loc[drivers["nationality"].eq("Japanese"), "driverId"].unique()

# Races in 2007-2009
races_0709 = races.loc[races["year"].between(2007, 2009), ["raceId", "year"]]

# Results for Japanese drivers in 2007-2009
df = (
    results_df.merge(races_0709, on="raceId", how="inner")
              .merge(status[["statusId", "status"]], on="statusId", how="left")
)
df = df[df["driverId"].isin(jp_driver_ids)].copy()

# Treat "Finished" and "+n Lap(s)" statuses as completed races
df["completed"] = df["status"].fillna("").eq("Finished") | df["status"].fillna("").str.match(r"^\+\d+\s+Lap", na=False)

out = (
    df.groupby("year", as_index=False)
      .agg(total_starts=("resultId", "count"), completed_races=("completed", "sum"))
)
out["completion_percentage"] = (out["completed_races"] / out["total_starts"]) * 100

# Ensure all years 2007-2009 appear
out = (
    pd.DataFrame({"year": [2007, 2008, 2009]})
      .merge(out, on="year", how="left")
      .sort_values("year")
      .reset_index(drop=True)
)

result = {"japanese_drivers_race_completion_percentage_2007_2009": out}
