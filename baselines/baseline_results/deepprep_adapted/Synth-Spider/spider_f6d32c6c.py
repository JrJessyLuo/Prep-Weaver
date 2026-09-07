import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_buildings", func="""
    # import pandas as pd
    # import numpy as np
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    #     story_cols = ['1','2','4','5','6','8','9','10']
    #     long_df = df.melt(
    #         id_vars=['Building_ID','Name','Address','Completed_Year'],
    #         value_vars=[c for c in story_cols if c in df.columns],
    #         var_name='stories',
    #         value_name='stories_value'
    #     )
    #     long_df = long_df[long_df['stories_value'].notna()].copy()
    #     long_df['stories'] = pd.to_numeric(long_df['stories'], errors='coerce').astype('Int64')
    #     out = long_df[['Building_ID','Name','Address','Completed_Year','stories']].copy()
    #     return out
    # """)
    # CodeGeneration
    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()
        story_cols = ['1','2','4','5','6','8','9','10']
        long_df = df.melt(
            id_vars=['Building_ID','Name','Address','Completed_Year'],
            value_vars=[c for c in story_cols if c in df.columns],
            var_name='stories',
            value_name='stories_value'
        )
        long_df = long_df[long_df['stories_value'].notna()].copy()
        long_df['stories'] = pd.to_numeric(long_df['stories'], errors='coerce').astype('Int64')
        out = long_df[['Building_ID','Name','Address','Completed_Year','stories']].copy()
        return out
    prepared_buildings = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_buildings", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # Story columns may appear as ints (1,2,...) in the input table
    #     candidate_story_cols = [1, 2, 4, 5, 6, 8, 9, 10]
    #     story_cols = [c for c in candidate_story_cols if c in df.columns]
    # 
    #     # Consolidate into a single 'stories' column:
    #     # take the first (left-to-right) story column that is non-null in the row.
    #     def pick_story(row):
    #         for c in story_cols:
    #             v = row.get(c, np.nan)
    #             if pd.notna(v):
    #                 return int(c)
    #         return pd.NA
    # 
    #     df["stories"] = df.apply(pick_story, axis=1).astype("Int64")
    # 
    #     out = df[["Building_ID", "Name", "Address", "Completed_Year", "stories"]].copy()
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # Story columns may appear as ints (1,2,...) in the input table
        candidate_story_cols = [1, 2, 4, 5, 6, 8, 9, 10]
        story_cols = [c for c in candidate_story_cols if c in df.columns]

        # Consolidate into a single 'stories' column:
        # take the first (left-to-right) story column that is non-null in the row.
        def pick_story(row):
            for c in story_cols:
                v = row.get(c, np.nan)
                if pd.notna(v):
                    return int(c)
            return pd.NA

        df["stories"] = df.apply(pick_story, axis=1).astype("Int64")

        out = df[["Building_ID", "Name", "Address", "Completed_Year", "stories"]].copy()
        return out
    prepared_buildings = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['prepared_buildings'])
    # Terminate
    result = {'prepared_buildings': prepared_buildings}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Region_ID', 'Capital', 'Area', 'Population', 'Name_Part1'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Region_ID', 'Capital', 'Area', 'Population', 'Name_Part1'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Concatenate(table_name="table_1", concatenate_columns=['Name_Part1', 'Name_Part2'], target_column="Region_Name", func="""
    # import pandas as pd
    # def concat(row: pd.Series) -> str:
    #     p1 = row.get('Name_Part1')
    #     p2 = row.get('Name_Part2')
    #     if pd.isna(p2) or p2 is None or str(p2).strip() == "":
    #         return str(p1).strip()
    #     return f"{str(p1).strip()} {str(p2).strip()}"
    #  """)
    # Concatenate
    def concat(row: pd.Series) -> str:
        p1 = row.get('Name_Part1')
        p2 = row.get('Name_Part2')
        if pd.isna(p2) or p2 is None or str(p2).strip() == "":
            return str(p1).strip()
        return f"{str(p1).strip()} {str(p2).strip()}"
    def _cat_apply(row):
        try:
            return concat(row)
        except Exception:
            return None
    table_1["Region_Name"] = table_1[['Name_Part1', 'Name_Part2']].apply(_cat_apply, axis=1)
    table_1 = table_1.drop(columns=['Name_Part1', 'Name_Part2'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['Name_Part1', 'Name_Part2'])
    # DropColumn
    table_1 = table_1.drop(columns=['Name_Part1', 'Name_Part2'], errors='ignore')

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Region_ID', 'Capital', 'Area', 'Population', 'Region_Name'])
    # SelectCol
    _cols = [c for c in ['Region_ID', 'Capital', 'Area', 'Population', 'Region_Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
