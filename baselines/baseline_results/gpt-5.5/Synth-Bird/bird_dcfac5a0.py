import pandas as pd

# Drivers table is stored transposed: rows are attributes, columns are driverIds
drivers_raw = tables["table_1"].copy()
drivers = drivers_raw.set_index("driverId").T.reset_index().rename(columns={"index": "driverId"})
drivers["driverId"] = pd.to_numeric(drivers["driverId"], errors="coerce")
drivers = drivers.dropna(subset=["driverId"])
drivers["driverId"] = drivers["driverId"].astype(int)

# Find nationality column (robust to case)
nat_col = next((c for c in drivers.columns if str(c).strip().lower() == "nationality"), None)
if nat_col is None:
    # fallback: any column containing "national"
    nat_col = next((c for c in drivers.columns if "national" in str(c).strip().lower()), None)

# Parse status table: "statusId-status"
status = tables["table_2"].copy()
status[["statusId", "status"]] = status["status_combined"].astype(str).str.split("-", n=1, expand=True)
status["statusId"] = pd.to_numeric(status["statusId"], errors="coerce").astype("Int64")

puncture_status_ids = status.loc[
    status["status"].str.contains(r"\bpuncture\b", case=False, na=False),
    "statusId"
].dropna().astype(int)

results = tables["table_3"].copy()
puncture_driver_ids = results.loc[results["statusId"].isin(puncture_status_ids), "driverId"].dropna().astype(int).unique()

american_puncture_count = drivers.loc[
    drivers["driverId"].isin(puncture_driver_ids)
    & drivers[nat_col].astype(str).str.contains(r"\bAmerican\b", case=False, na=False),
    "driverId"
].nunique()

result = {
    "american_drivers_with_puncture_status": pd.DataFrame(
        {"american_drivers_with_puncture_status": [american_puncture_count]}
    )
}
