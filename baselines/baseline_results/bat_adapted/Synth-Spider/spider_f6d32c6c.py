import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    story_cols = [c for c in df.columns if isinstance(c, (int, float))]
    df['stories'] = df[story_cols].bfill(axis=1).iloc[:, 0]
    target = df[['Building_ID', 'Name', 'Address', 'Completed_Year', 'stories']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['Name_Part2'] = df['Name_Part2'].replace('None', pd.NA)
    df['Region_Name'] = df['Name_Part1'].where(df['Name_Part2'].isna(), df['Name_Part1'].astype(str).str.cat(df['Name_Part2'].astype(str), sep=' '))
    target = df[['Region_ID', 'Capital', 'Area', 'Population', 'Region_Name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_regions = prepared_table_2

# Assume table_1_df and table_2_df are the original DataFrames

# Prepare buildings: melt/select the non-null stories value from the integer-labeled columns
story_cols = [c for c in table_1_df.columns if isinstance(c, (int, np.integer)) or str(c).isdigit()]
# Ensure columns are treated as strings for selection safety
story_cols = [int(c) if isinstance(c, str) and c.isdigit() else c for c in story_cols]

# Coalesce the first non-null across story columns into 'stories'
prepared_buildings = table_1_df.copy()
if story_cols:
    prepared_buildings['stories'] = prepared_buildings[story_cols].bfill(axis=1).iloc[:, 0]
else:
    prepared_buildings['stories'] = np.nan

prepared_buildings = prepared_buildings[['Building_ID', 'Name', 'Address', 'Completed_Year', 'stories']]

# Prepare regions: combine name parts into Region_Name
prepared_regions = table_2_df.copy()
name2 = prepared_regions['Name_Part2'].replace({'None': np.nan}) if 'Name_Part2' in prepared_regions.columns else np.nan
part2_clean = name2.where(name2.notna() & (name2.str.len() > 0), '')
prepared_regions['Region_Name'] = prepared_regions['Name_Part1'].astype(str) + ((' ' + part2_clean) if isinstance(part2_clean, pd.Series) else '')
prepared_regions['Region_Name'] = prepared_regions['Region_Name'].str.strip()
prepared_regions = prepared_regions[['Region_ID', 'Capital', 'Area', 'Population', 'Region_Name']]

# No natural join keys exist between buildings and regions in the provided schemas.
# The question only requires filtering by region name and reporting number of stories of buildings in that region.
# Since buildings lack a region field, integration is not applicable; we filter regions to validate the region exists, then proceed as data allows.

# Filter to the target region name
target_region = 'Abruzzo'
region_exists = prepared_regions.loc[prepared_regions['Region_Name'].str.casefold() == target_region.casefold()]

# If buildings had a region key, we'd join here. In absence of that, we cannot link buildings to regions.
# Return empty result to reflect no buildings can be attributed to the specified region with given data.

# Final answer DataFrame (could be empty due to missing linkage)
answer = pd.DataFrame({'stories': []})

# If a buildings-to-region linkage column appears in upstream prep, replace the above with an explicit merge like:
# merged = prepared_buildings.merge(prepared_regions[prepared_regions['Region_Name'].str.casefold()==target_region.casefold()], on='Region_Name')
# answer = merged[['stories']]

target = answer

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
