import pandas as pd

drivers = tables["table_1"]
results_df = tables["table_3"]
races_kv = tables["table_2"]

# Get Lewis Hamilton's driverId
ham_ids = drivers.loc[
    (drivers["fn"].str.lower() == "lewis") & (drivers["ln"].str.lower() == "hamilton"),
    "driverId",
].unique()

# RaceIds where Lewis Hamilton participated (appears in results)
ham_race_ids = results_df.loc[results_df["driverId"].isin(ham_ids), ["raceId"]].drop_duplicates()

# Pivot race key-value table to get year per raceId
races_wide = (
    races_kv.pivot_table(index="raceId", columns="attr", values="val", aggfunc="first")
    .reset_index()
)

# Ensure year is numeric
if "year" in races_wide.columns:
    races_wide["year"] = pd.to_numeric(races_wide["year"], errors="coerce")

years = (
    ham_race_ids.merge(races_wide[["raceId", "year"]], on="raceId", how="left")["year"]
    .dropna()
    .astype(int)
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
)

result = {"hamilton_race_years": pd.DataFrame({"year": years})}
