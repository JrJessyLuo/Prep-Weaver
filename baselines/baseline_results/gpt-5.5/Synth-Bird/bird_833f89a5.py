import pandas as pd

circuits = tables["table_1"]
races_kv = tables["table_2"]

# Find Brands Hatch circuitId(s)
brands_hatch_ids = circuits.loc[
    circuits["name"].astype(str).str.contains("Brands Hatch", case=False, na=False),
    "circuitId"
].unique()

# Pivot races key-value table to wide
races = (
    races_kv.pivot_table(index="raceId", columns="attribute", values="value", aggfunc="first")
    .reset_index()
)

# Ensure proper dtypes
for col in ["year", "circuitId"]:
    if col in races.columns:
        races[col] = pd.to_numeric(races[col], errors="coerce")

# Filter to British Grand Prix at Brands Hatch and take latest season (year)
bh_british = races[
    races["name"].astype(str).str.fullmatch("British Grand Prix", case=False, na=False)
    & races["circuitId"].isin(brands_hatch_ids)
].copy()

last_year = bh_british["year"].max()

result = {
    "last_brands_hatch_british_gp_season": pd.DataFrame({"year": [int(last_year)] if pd.notna(last_year) else [pd.NA]})
}
