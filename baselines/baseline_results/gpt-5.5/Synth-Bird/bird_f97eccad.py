import pandas as pd
import numpy as np

drivers = tables["table_1"].copy()
results_df = tables["table_2"].copy()

# Drivers born in 1971
drivers["dob"] = pd.to_datetime(drivers["dob"], errors="coerce")
drivers_1971 = drivers.loc[drivers["dob"].dt.year == 1971, ["driverId", "code"]]

# Parse fastestLapTime ("m:ss.mmm" or "ss.mmm") into milliseconds
flt = results_df["fastestLapTime"].astype("string")

parts = flt.str.split(":", n=1, expand=True)
has_min = parts.shape[1] == 2

mins = pd.to_numeric(parts[0], errors="coerce") if has_min else pd.Series(np.nan, index=results_df.index)
sec_ms_str = parts[1] if has_min else parts[0]

sec_ms = sec_ms_str.str.split(".", n=1, expand=True)
secs = pd.to_numeric(sec_ms[0], errors="coerce")
ms = pd.to_numeric(sec_ms[1], errors="coerce").fillna(0)

results_df["fastestLapTime_ms"] = np.where(
    has_min,
    mins * 60_000 + secs * 1_000 + ms,
    secs * 1_000 + ms,
).astype("float64")

# Fastest lap per race (ties included)
valid = results_df.dropna(subset=["raceId", "driverId", "fastestLapTime_ms"]).copy()
min_per_race = valid.groupby("raceId")["fastestLapTime_ms"].transform("min")
fastest_per_race = valid.loc[valid["fastestLapTime_ms"].eq(min_per_race), ["driverId"]].drop_duplicates()

# Filter to 1971-born drivers and return id + code
out = (
    fastest_per_race.merge(drivers_1971, on="driverId", how="inner")[["driverId", "code"]]
    .drop_duplicates()
    .sort_values("driverId")
    .reset_index(drop=True)
)

result = {"drivers_born_1971_with_fastest_lap": out}
