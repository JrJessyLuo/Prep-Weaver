import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FCLT_FLOOR_KEY', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SPACE_ID', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_NAME', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM_FULL_NAME', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_ROOM', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FCLT_ROOM_KEY', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_ROOM_KEY', 'FCLT_BUILDING_KEY', 'FCLT_FLOOR_KEY', 'FLOOR', 'ROOM', 'SPACE_ID', 'AREA', 'ROOM_FULL_NAME', 'ORGANIZATION_NAME', 'DEPT_CODE', 'BUILDING_ROOM']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ASSIGNABLE_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME_LONG', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ASSIGNABLE_AREA']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ASSIGNABLE_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FCLT_FLOOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'ASSIGNABLE_AREA']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['AREA'] = pd.to_numeric(tmp_0['AREA'], errors='coerce').astype(float)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['FCLT_BUILDING_KEY'] = tmp_1['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['FCLT_FLOOR_KEY'] = tmp_2['FCLT_FLOOR_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['FLOOR'] = tmp_3['FLOOR'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['ROOM'] = tmp_4['ROOM'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['SPACE_ID'] = tmp_5['SPACE_ID'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_6['ORGANIZATION_NAME'] = tmp_6['ORGANIZATION_NAME'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_7['ROOM_FULL_NAME'] = tmp_7['ROOM_FULL_NAME'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_8['BUILDING_ROOM'] = tmp_8['BUILDING_ROOM'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_9 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_9)
    _std_func_9 = _ns_9.get('transform') or _ns_9.get('transform')
    tmp_9['FCLT_ROOM_KEY'] = tmp_9['FCLT_ROOM_KEY'].apply(lambda s: _std_func_9(s) if pd.notna(s) else s)
    # Step 11: SelectCol
    result = tmp_9.loc[:, ['FCLT_ROOM_KEY', 'FCLT_BUILDING_KEY', 'FCLT_FLOOR_KEY', 'FLOOR', 'ROOM', 'SPACE_ID', 'AREA', 'ROOM_FULL_NAME', 'ORGANIZATION_NAME', 'DEPT_CODE', 'BUILDING_ROOM']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ASSIGNABLE_AREA'] = pd.to_numeric(tmp_0['ASSIGNABLE_AREA'], errors='coerce').astype(float)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['FCLT_BUILDING_KEY'] = tmp_1['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['BUILDING_NAME'] = tmp_2['BUILDING_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['BUILDING_NAME_LONG'] = tmp_3['BUILDING_NAME_LONG'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['BUILDING_NUMBER'] = tmp_4['BUILDING_NUMBER'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ASSIGNABLE_AREA']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ASSIGNABLE_AREA'] = pd.to_numeric(tmp_0['ASSIGNABLE_AREA'], errors='coerce').astype(float)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['FCLT_FLOOR_KEY'] = tmp_1['FCLT_FLOOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['FCLT_BUILDING_KEY'] = tmp_2['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['FLOOR'] = tmp_3['FLOOR'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'ASSIGNABLE_AREA']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_10', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge rooms with building-level assignable area and names
integrated = prepared_table_1.merge(
    prepared_table_2.rename(columns={'ASSIGNABLE_AREA': 'ASSIGNABLE_AREA_BUILDING'}),
    how='left', on='FCLT_BUILDING_KEY'
)

# Merge floor-level assignable area
integrated = integrated.merge(
    prepared_table_3[['FCLT_FLOOR_KEY', 'ASSIGNABLE_AREA']].rename(columns={'ASSIGNABLE_AREA': 'ASSIGNABLE_AREA_FLOOR'}),
    how='left', on='FCLT_FLOOR_KEY'
)

# Compute percentages safely
integrated['pct_of_floor_assignable_area'] = (integrated['AREA'] / integrated['ASSIGNABLE_AREA_FLOOR'] * 100)
integrated['pct_of_building_assignable_area'] = (integrated['AREA'] / integrated['ASSIGNABLE_AREA_BUILDING'] * 100)

# Build final building name preference
integrated['BUILDING_NAME_FINAL'] = integrated['BUILDING_NAME']
missing_name = integrated['BUILDING_NAME_FINAL'].isna() | (integrated['BUILDING_NAME_FINAL'].astype(str).str.strip() == '')
integrated.loc[missing_name, 'BUILDING_NAME_FINAL'] = integrated.loc[missing_name, 'BUILDING_NAME_LONG']

# Room full name fallback
name_missing = integrated['ROOM_FULL_NAME'].isna() | (integrated['ROOM_FULL_NAME'].astype(str).str.strip() == '')
integrated.loc[name_missing, 'ROOM_FULL_NAME'] = integrated.loc[name_missing, 'BUILDING_ROOM']
name_missing2 = integrated['ROOM_FULL_NAME'].isna() | (integrated['ROOM_FULL_NAME'].astype(str).str.strip() == '')
integrated.loc[name_missing2, 'ROOM_FULL_NAME'] = integrated.loc[name_missing2, 'SPACE_ID']

# Select and rename columns per request
cols = [
    'ROOM_FULL_NAME',                    # full name of the room
    'BUILDING_NAME_FINAL',               # building name
    'FLOOR',                             # floor number
    'ORGANIZATION_NAME',                 # organizations occupying them
    'DEPT_CODE',                         # department code/name field available
    'pct_of_floor_assignable_area',      # % of floor assignable area
    'pct_of_building_assignable_area',   # % of building assignable area
    'FCLT_BUILDING_KEY',
    'FCLT_FLOOR_KEY',
    'FCLT_ROOM_KEY',
    'ROOM',
    'SPACE_ID',
    'AREA'
]

# Ensure columns exist even if some merges had missing data
available_cols = [c for c in cols if c in integrated.columns]

target = integrated[available_cols].rename(columns={'BUILDING_NAME_FINAL': 'BUILDING_NAME'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
