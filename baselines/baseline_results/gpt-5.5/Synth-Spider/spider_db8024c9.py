import pandas as pd

df_bld = tables["table_1"].copy()
df_reg = tables["table_2"].copy()

# Build full region name
df_reg["region_name"] = (
    df_reg["Name_Part1"].fillna("").astype(str).str.strip()
    + " "
    + df_reg["Name_Part2"].fillna("").astype(str).str.strip()
).str.replace(r"\s+", " ", regex=True).str.strip()

# Get Region_ID for Abruzzo
abruzzo_id = df_reg.loc[df_reg["region_name"].str.casefold().eq("abruzzo"), "Region_ID"].iloc[0]
region_col = str(abruzzo_id)

# Filter buildings belonging to Abruzzo (non-null in the region-id column)
abr = df_bld[df_bld[region_col].notna()].copy()
abr["Building_Name"] = abr[region_col]

out = abr[["Building_ID", "Building_Name", "Number_of_Stories"]].sort_values("Building_ID").reset_index(drop=True)

result = {"abruzzo_building_stories": out}
