import pandas as pd

# Tables are preloaded in the dict `tables` per the evaluation convention.
drivers = tables["table_1"]
results = tables["table_2"]

# 1) Load drivers and filter to 1971-born drivers (keep driverId, code)
drivers_1971 = (
    drivers.assign(dob_parsed=pd.to_datetime(drivers["dob"], errors="coerce"))
    .loc[lambda df: df["dob_parsed"].dt.year == 1971, ["driverId", "code"]]
    .dropna(subset=["driverId"])
    .drop_duplicates()
    .reset_index(drop=True)
)

# 2) Load results and compute fastest lap per race:
#    - Use rank==1 when present
#    - Otherwise use minimum parsed fastestLapTime per race
results_with_time = results.assign(
    fastestLapTime_td=pd.to_timedelta(results["fastestLapTime"], errors="coerce")
)

rank1_rows = (
    results_with_time.loc[
        results_with_time["rank"].eq(1)
        & results_with_time["raceId"].notna()
        & results_with_time["driverId"].notna(),
        ["raceId", "driverId"],
    ]
    .drop_duplicates()
)

races_with_rank1 = set(rank1_rows["raceId"].unique())

min_time_rows = results_with_time.loc[
    ~results_with_time["raceId"].isin(races_with_rank1),
    ["raceId", "driverId", "fastestLapTime_td"],
].dropna(subset=["raceId", "driverId", "fastestLapTime_td"])

min_time_per_race = min_time_rows.groupby("raceId", as_index=False)["fastestLapTime_td"].min()

min_time_winners = (
    min_time_rows.merge(min_time_per_race, on=["raceId", "fastestLapTime_td"], how="inner")[
        ["raceId", "driverId"]
    ]
    .drop_duplicates()
)

fastest_per_race = pd.concat([rank1_rows, min_time_winners], ignore_index=True).drop_duplicates()

# 3) Join to 1971-born drivers; output distinct driverId and code
answer_df = (
    fastest_per_race.merge(drivers_1971, on="driverId", how="inner")[["driverId", "code"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Final result per required convention
result = {"drivers_born_1971_with_fastest_lap": answer_df}