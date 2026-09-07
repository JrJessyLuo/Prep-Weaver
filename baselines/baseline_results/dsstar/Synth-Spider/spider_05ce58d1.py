import pandas as pd

# Access pre-loaded tables
df_buildings = tables['table_1']
df_regions = tables['table_2']

# Group buildings by Region_ID to get regions that have any buildings
regions_with_buildings = set(df_buildings['Region_ID'].dropna().unique().tolist())

# Filter df_regions to Region_IDs not in that set (regions without buildings)
regions_without_buildings = df_regions[~df_regions['Region_ID'].isin(regions_with_buildings)].copy()

# Construct full region names by combining Name_Part1 and Name_Part2 where present
def combine_name(row):
    p1 = str(row['Name_Part1']).strip() if pd.notna(row['Name_Part1']) else ""
    p2 = str(row['Name_Part2']).strip() if pd.notna(row['Name_Part2']) else ""
    if p2 and p2.lower() != "none":
        return f"{p1} {p2}".strip()
    return p1

regions_without_buildings['Full_Name'] = regions_without_buildings.apply(combine_name, axis=1)

# Prepare final answer DataFrame with only the region names
answer_df = regions_without_buildings[['Full_Name']].rename(columns={'Full_Name': 'Region_Name'}).reset_index(drop=True)

# Assign to result as required
result = {"regions_without_buildings": answer_df}