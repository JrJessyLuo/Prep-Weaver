import pandas as pd

# tables are preloaded pandas DataFrames in a dict named `tables`
drivers = tables["table_1"]   # bird_ffd581c9_input_0.pkl
results_tbl = tables["table_11"]  # formula_1_results.pkl

# Load drivers and get French driverIds
french_driver_ids = (
    drivers.loc[drivers["guoji"].eq("French"), "driverId"]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

# Filter results to French drivers with non-null fastestLapTime
fr_results = results_tbl.loc[
    results_tbl["driverId"].isin(french_driver_ids) & results_tbl["fastestLapTime"].notna(),
    ["driverId", "raceId", "fastestLapTime"],
].copy()

# Convert fastestLapTime from "m:ss.mmm" to total seconds
ft = fr_results["fastestLapTime"].astype(str).str.strip()
mm_ss = ft.str.split(":", n=1, expand=True)
minutes = pd.to_numeric(mm_ss[0], errors="coerce")
sec_ms = mm_ss[1].str.split(".", n=1, expand=True)
seconds = pd.to_numeric(sec_ms[0], errors="coerce")
milliseconds = pd.to_numeric(sec_ms[1], errors="coerce")

fr_results["fastestLapSeconds"] = minutes * 60 + seconds + (milliseconds / 1000)

# Keep rows with total seconds < 120.0 and count distinct drivers
fast_driver_ids = (
    fr_results.loc[fr_results["fastestLapSeconds"].lt(120.0), "driverId"]
    .dropna()
    .astype(int)
    .unique()
)
answer = int(pd.Series(fast_driver_ids).nunique())

# Final answer table
answer_df = pd.DataFrame({"french_driver_count_lap_lt_02_00_00": [answer]})

# Assign to `result` as required
result = {"answer": answer_df}