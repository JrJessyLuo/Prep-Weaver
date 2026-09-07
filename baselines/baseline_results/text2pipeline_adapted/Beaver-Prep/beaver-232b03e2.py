import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FLOOR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'FLOOR']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME_LONG', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['FLOOR'] = tmp_1['FLOOR'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['FLOOR'] = pd.to_numeric(tmp_2['FLOOR'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['FCLT_BUILDING_KEY', 'FLOOR']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_NAME'] = tmp_1['BUILDING_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['BUILDING_NAME_LONG'] = tmp_2['BUILDING_NAME_LONG'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_10', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='FCLT_BUILDING_KEY', how='inner')
# Prefer BUILDING_NAME, fallback to BUILDING_NAME_LONG
integrated['BUILDING_NAME_EFF'] = integrated['BUILDING_NAME']
mask_null = integrated['BUILDING_NAME_EFF'].isna() | (integrated['BUILDING_NAME_EFF'].astype(str).str.strip() == '')
integrated.loc[mask_null, 'BUILDING_NAME_EFF'] = integrated.loc[mask_null, 'BUILDING_NAME_LONG']
# Compute the maximum FLOOR across all buildings, then select rows at that max and return name and floor
# Coerce FLOOR to numeric again defensively (in case any non-numeric slipped through as strings)
integrated['FLOOR_NUM'] = integrated['FLOOR']
max_floor = integrated['FLOOR_NUM'].max()
# If max is NaN (all non-numeric), relax by trying to parse digits from FLOOR as fallback
if pd.isna(max_floor):
    parsed = pd.to_numeric(integrated['FLOOR'].astype(str).str.extract(r'(-?\d+)', expand=False), errors='coerce')
    integrated['FLOOR_NUM'] = parsed
    max_floor = integrated['FLOOR_NUM'].max()
# If still NaN, fallback to keeping rows with non-null FLOOR and arbitrary max via sort by FLOOR string
if pd.isna(max_floor):
    tmp = integrated[integrated['FLOOR'].notna()].copy()
    if tmp.empty:
        target = integrated[['BUILDING_NAME_EFF', 'FLOOR']].drop_duplicates()
    else:
        tmp = tmp.sort_values(by='FLOOR', ascending=False)
        top = tmp.head(1)
        target = top[['BUILDING_NAME_EFF', 'FLOOR']].rename(columns={'BUILDING_NAME_EFF': 'BUILDING_NAME'})
else:
    top = integrated[integrated['FLOOR_NUM'] == max_floor]
    # Deduplicate on building and floor; if multiple buildings share same top floor, include them all
    result = top[['BUILDING_NAME_EFF', 'FLOOR_NUM']].drop_duplicates()
    target = result.rename(columns={'BUILDING_NAME_EFF': 'BUILDING_NAME', 'FLOOR_NUM': 'FLOOR'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
