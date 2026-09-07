import pandas as pd

# Input tables (already loaded in scope as `tables`)
races = tables["table_2"]
results_tbl = tables["table_3"]

# 1) Filter races for Austrian Grand Prix
austrian_races = races[races["mingcheng"] == "Austrian Grand Prix"].copy()

# 2) Join races -> results on raceId
austrian_results = results_tbl.merge(
    austrian_races[["raceId", "year", "round", "luquId", "mingcheng", "date"]],
    on="raceId",
    how="inner",
)

# 3) Compute minimum fastest lap:
# Prefer fastestLapTime (parsed to ms). If none parseable, fall back to 'milliseconds'.
austrian_results["_fastestLapTime_ms"] = pd.to_timedelta(
    austrian_results["fastestLapTime"].astype(str),
    errors="coerce",
).dt.total_seconds().mul(1000)

austrian_results["_best_fastest_ms"] = austrian_results["_fastestLapTime_ms"]

if austrian_results["_best_fastest_ms"].isna().all() and "milliseconds" in austrian_results.columns:
    austrian_results["_best_fastest_ms"] = austrian_results["milliseconds"]

valid = austrian_results[austrian_results["_best_fastest_ms"].notna()].copy()

min_fastest_lap_row = None
if not valid.empty:
    idx = valid["_best_fastest_ms"].idxmin()
    min_fastest_lap_row = valid.loc[idx]

# Final answer table (lap record time)
answer_df = pd.DataFrame(
    {
        "lap_record": [None if min_fastest_lap_row is None else min_fastest_lap_row.get("fastestLapTime")]
    }
)

# Required output variable: dict[str, pandas.DataFrame]
result = {"austrian_gp_lap_record": answer_df}