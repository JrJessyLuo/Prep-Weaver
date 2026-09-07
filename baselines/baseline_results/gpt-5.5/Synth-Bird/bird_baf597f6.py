import pandas as pd

drivers = tables["table_1"].copy()
races = tables["table_2"].copy()
results_tbl = tables["table_3"].copy()

# Clean raceId in races table (appears as strings like '"1"')
races["raceId_clean"] = (
    races["raceId"]
    .astype(str)
    .str.strip()
    .str.strip('"')
    .str.strip("'")
)
races["raceId_clean"] = pd.to_numeric(races["raceId_clean"], errors="coerce")

# Get 2008 Australian Grand Prix raceId
race_id_2008_aus = races.loc[
    (races["year"] == 2008) & (races["name"] == "Australian Grand Prix"),
    "raceId_clean"
].dropna()

race_id_2008_aus = None if race_id_2008_aus.empty else int(race_id_2008_aus.iloc[0])

# Distinct participating drivers in that race
if race_id_2008_aus is None:
    count_un = 0
else:
    participating_driver_ids = results_tbl.loc[
        results_tbl["raceId"] == race_id_2008_aus, "driverId"
    ].dropna().unique()

    # Count drivers whose nationality (gj) is 'UN' (case-insensitive)
    count_un = drivers.loc[
        drivers["driverId"].isin(participating_driver_ids)
        & drivers["gj"].astype(str).str.strip().str.upper().eq("UN"),
        "driverId"
    ].nunique()

result = {
    "un_drivers_2008_australian_gp": pd.DataFrame(
        {"number_of_drivers": [int(count_un)]}
    )
}
