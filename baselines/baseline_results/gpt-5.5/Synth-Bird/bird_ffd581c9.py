import pandas as pd

drivers = tables["table_1"]
lap_wide = tables["table_2"]

# table_2 is a transposed/denormalized lap-times table:
# rows (in 'raceId' col) are attributes like driverId/lap/position/time/milliseconds,
# columns are records. Convert it back to a normal (long) table.
lap_long = (
    lap_wide.set_index("raceId")
    .T.reset_index(drop=False)
    .rename(columns={"index": "record"})
)

# Ensure required numeric fields
lap_long["driverId"] = pd.to_numeric(lap_long.get("driverId"), errors="coerce").astype("Int64")
lap_long["milliseconds"] = pd.to_numeric(lap_long.get("milliseconds"), errors="coerce")

# French drivers
french_ids = set(drivers.loc[drivers["guoji"].eq("French"), "driverId"])

# Count distinct French drivers with any lap time < 02:00.00 (120000 ms)
count_french = (
    lap_long.loc[
        lap_long["driverId"].isin(french_ids) & (lap_long["milliseconds"] < 120000),
        "driverId",
    ]
    .dropna()
    .nunique()
)

result = {
    "french_drivers_under_02_00_00": pd.DataFrame(
        {"count": [int(count_french)]}
    )
}
