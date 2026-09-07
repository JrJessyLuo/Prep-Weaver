import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Building_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Region_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Region_ID', 'Building_ID']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Region_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Area', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Population', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Capital', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Name_Part1', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Name_Part2', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Name_Part1', 'func': 'def transform(s):\n    return "" if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Name_Part2', 'func': 'def transform(s):\n    return "" if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Name_Part1', 'Name_Part2'], 'target_column': 'Region_Name', 'func': 'def transform(row):\n    p1 = row.get(\'Name_Part1\')\n    p2 = row.get(\'Name_Part2\')\n    p1 = "" if p1 is None else str(p1).strip()\n    p2 = "" if p2 is None else str(p2).strip()\n    if p2 == "None" or p2 == "":\n        return p1\n    return f"{p1} {p2}"'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Region_ID', 'Region_Name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Building_ID'] = pd.to_numeric(tmp_0['Building_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Region_ID'] = pd.to_numeric(tmp_1['Region_ID'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Region_ID', 'Building_ID']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Region_ID'] = pd.to_numeric(tmp_0['Region_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Area'] = pd.to_numeric(tmp_1['Area'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Population'] = pd.to_numeric(tmp_2['Population'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Capital'] = tmp_3['Capital'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['Name_Part1'] = tmp_4['Name_Part1'].astype(str)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['Name_Part2'] = tmp_5['Name_Part2'].astype(str)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return "" if s is None else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_6['Name_Part1'] = tmp_6['Name_Part1'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return "" if s is None else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_7['Name_Part2'] = tmp_7['Name_Part2'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 9: Concatenate
    tmp_8 = tmp_7.copy()
    _ns_3 = {}
    exec('def transform(row):\n    p1 = row.get(\'Name_Part1\')\n    p2 = row.get(\'Name_Part2\')\n    p1 = "" if p1 is None else str(p1).strip()\n    p2 = "" if p2 is None else str(p2).strip()\n    if p2 == "None" or p2 == "":\n        return p1\n    return f"{p1} {p2}"', globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_8['Region_Name'] = tmp_8[['Name_Part1', 'Name_Part2']].apply(_concat_func_3, axis=1)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['Region_ID', 'Region_Name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
regions = prepared_table_2
buildings = prepared_table_1
integrated = regions.merge(buildings, on='Region_ID', how='left')
no_bldg = integrated[integrated['Building_ID'].isna()]
result = no_bldg[['Region_Name']].drop_duplicates().sort_values('Region_Name')
target = result.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
