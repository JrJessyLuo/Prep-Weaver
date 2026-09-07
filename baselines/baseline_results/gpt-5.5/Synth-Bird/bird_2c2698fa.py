import pandas as pd

# Load tables
drivers_kv = tables["table_1"]
lap_times = tables["table_2"]
circuits = tables["table_3"]
races = tables["table_10"]
results_df = tables["table_11"]

# Pivot driver key-value table to wide to identify Lewis Hamilton
drivers_wide = (
    drivers_kv.pivot_table(index="driverId", columns="attribute", values="value", aggfunc="first")
    .reset_index()
)

ham_mask = False
if "url" in drivers_wide.columns:
    ham_mask = ham_mask | drivers_wide["url"].astype(str).str.contains("Lewis_Hamilton", case=False, na=False)
if "surname" in drivers_wide.columns:
    ham_mask = ham_mask | (drivers_wide["surname"].astype(str).str.lower() == "hamilton")

ham_driver_ids = drivers_wide.loc[ham_mask, "driverId"].dropna().unique()
ham_driver_id = int(ham_driver_ids[0]) if len(ham_driver_ids) else None

# Filter Hamilton results with a recorded fastest lap
ham_results = results_df.copy()
if ham_driver_id is not None:
    ham_results = ham_results[ham_results["driverId"] == ham_driver_id]

ham_results = ham_results[ham_results["fastestLap"].notna()].copy()
ham_results["fastestLap_int"] = pd.to_numeric(ham_results["fastestLap"], errors="coerce").astype("Int64")
ham_results = ham_results[ham_results["fastestLap_int"].notna()].copy()

# Get Hamilton position on his fastest lap from lap times
ham_fastlap_pos = ham_results[["raceId", "driverId", "fastestLap_int"]].rename(columns={"fastestLap_int": "lap"})
ham_fastlap_pos = ham_fastlap_pos.merge(
    lap_times[["raceId", "driverId", "lap", "position"]],
    on=["raceId", "driverId", "lap"],
    how="left"
)

# Add circuit info (via races -> circuits)
out = ham_fastlap_pos.merge(
    races[["raceId", "year", "round", "circuitId", "name"]].rename(columns={"name": "race_name"}),
    on="raceId",
    how="left"
).merge(
    circuits[["circuitId", "name"]].rename(columns={"name": "circuit_name"}),
    on="circuitId",
    how="left"
)

out = out.rename(columns={"position": "position_during_fastest_lap"})
out = out.sort_values(["year", "round", "raceId"], na_position="last").reset_index(drop=True)

result = {
    "hamilton_fastest_lap_circuit_positions": out[["year", "race_name", "circuit_name", "lap", "position_during_fastest_lap"]]
}
