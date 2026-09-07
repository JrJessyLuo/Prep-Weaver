import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Build transaction datetime (robust to different date formats)
t2["Date_norm"] = (
    t2["Date"].astype(str)
    .str.replace(r"\s*/\s*", "-", regex=True)
    .str.replace(r"\s+", "", regex=True)
)
t2["dt"] = pd.to_datetime(t2["Date_norm"] + " " + t2["Time"].astype(str), errors="coerce")

target_dt = pd.to_datetime("2012-08-24 12:42:00")

# Prepare country code
t1["Country"] = t1["Country_Part1"].astype(str) + t1["Country_Part2"].astype(str)

out = (
    t2.loc[t2["dt"].eq(target_dt), ["GasStationID"]]
    .merge(t1[["GasStationID", "Country"]], on="GasStationID", how="left")
    .drop_duplicates(subset=["Country"])
    .loc[:, ["Country"]]
    .reset_index(drop=True)
)

result = {"country_for_deal": out}
