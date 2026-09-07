import pandas as pd

races = tables["table_1"][["raceId", "year"]]
results_df = tables["table_11"][["raceId", "fastestLapSpeed"]].copy()

results_df["fastestLapSpeed"] = pd.to_numeric(results_df["fastestLapSpeed"], errors="coerce")

df = results_df.merge(races, on="raceId", how="left").dropna(subset=["fastestLapSpeed", "year"])

min_speed = df["fastestLapSpeed"].min()
out = (
    df.loc[df["fastestLapSpeed"].eq(min_speed), ["year"]]
    .drop_duplicates()
    .sort_values("year")
    .assign(lowest_fastest_lap_speed=min_speed)
    .reset_index(drop=True)
)

result = {"lowest_lap_time_speed_year": out}
