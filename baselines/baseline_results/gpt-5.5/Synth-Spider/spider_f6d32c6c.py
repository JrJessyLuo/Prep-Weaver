import pandas as pd

b = tables["table_1"].copy()
r = tables["table_2"].copy()

# Build full region name
r["region_name"] = r["Name_Part1"].fillna("").astype(str) + (
    " " + r["Name_Part2"].fillna("").astype(str)
)
r["region_name"] = r["region_name"].str.replace(r"\s+", " ", regex=True).str.strip()

# Unpivot building table to (Building, Region_ID, number_of_stories)
id_vars = ["Building_ID", "Name", "Address", "Completed_Year"]
region_cols = [c for c in b.columns if c not in id_vars and str(c).strip().isdigit()]

bl = b.melt(
    id_vars=id_vars,
    value_vars=region_cols,
    var_name="Region_ID",
    value_name="number_of_stories",
).dropna(subset=["number_of_stories"])

bl["Region_ID"] = bl["Region_ID"].astype(int)

# Filter to Abruzzo
abruzzo_ids = r.loc[r["region_name"].eq("Abruzzo"), ["Region_ID"]].drop_duplicates()
out = bl.merge(abruzzo_ids, on="Region_ID", how="inner")

out = out[["Building_ID", "Name", "number_of_stories"]].rename(columns={"Name": "Building_Name"}).reset_index(drop=True)

result = {"abruzzo_building_stories": out}
