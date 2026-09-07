import pandas as pd

# Tables provided in-scope as `tables`
races = tables["table_1"]       # bird_ef8a899f_input_0.pkl
results = tables["table_11"]    # formula_1_results.pkl

# 1) Clean fastestLapSpeed -> numeric, drop missing
results = results.copy()
results["fastestLapSpeed"] = pd.to_numeric(results["fastestLapSpeed"], errors="coerce")
results_clean = results.dropna(subset=["fastestLapSpeed"]).copy()

# 2) Attach race metadata (year, race name/date) via raceId
results_with_race = (
    results_clean.merge(
        races[["raceId", "year", "name", "date"]],
        on="raceId",
        how="left",
        validate="m:1",
    )
    .dropna(subset=["year"])
    .copy()
)
results_with_race["year"] = results_with_race["year"].astype(int)

# 3) Compute per-year minimum fastestLapSpeed, then select the year with the overall minimum
per_year_min = (
    results_with_race.groupby("year", as_index=False)["fastestLapSpeed"]
    .min()
    .rename(columns={"fastestLapSpeed": "min_fastestLapSpeed"})
)

global_min_of_year_mins = per_year_min["min_fastestLapSpeed"].min()
worst_years = (
    per_year_min.loc[per_year_min["min_fastestLapSpeed"].eq(global_min_of_year_mins), "year"]
    .astype(int)
    .sort_values()
    .tolist()
)

answer_df = pd.DataFrame({"year": worst_years})

result = {"lowest_lap_speed_year": answer_df}