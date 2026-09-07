import pandas as pd

buildings = tables["table_1"]
regions = tables["table_2"]

# Region IDs that have at least one building record
regions_with_buildings = set(buildings["Region_ID"].dropna().unique())

# Build full region name from parts
name_part2 = regions["Name_Part2"].fillna("").astype(str).str.strip()
regions["Region_Name"] = regions["Name_Part1"].astype(str).str.strip() + (
    " " + name_part2.where(name_part2.ne(""), "")
)
regions["Region_Name"] = regions["Region_Name"].str.strip()

# Regions with no buildings
out = regions.loc[~regions["Region_ID"].isin(regions_with_buildings), ["Region_Name"]].drop_duplicates()
out = out.sort_values("Region_Name").reset_index(drop=True)

result = {"regions_with_no_buildings": out}
