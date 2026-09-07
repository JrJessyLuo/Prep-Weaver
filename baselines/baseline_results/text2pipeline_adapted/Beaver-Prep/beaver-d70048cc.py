import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM_FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['fac_room_key', 'BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'SPACE_ID', 'AREA', 'ROOM_FULL_NAME', 'ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'DEPT_CODE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ASSIGNABLE_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'EXT_GROSS_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME_LONG', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FAC_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ROOM_SQUARE_FOOTAGE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM_NUMBER', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR_KEY', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['AREA'] = pd.to_numeric(tmp_0['AREA'], errors='coerce').astype(float)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['ROOM'] = tmp_1['ROOM'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['ROOM_FULL_NAME'] = tmp_2['ROOM_FULL_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['ORGANIZATION_NAME'] = tmp_3['ORGANIZATION_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['fac_room_key', 'BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'SPACE_ID', 'AREA', 'ROOM_FULL_NAME', 'ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'DEPT_CODE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ASSIGNABLE_AREA'] = pd.to_numeric(tmp_0['ASSIGNABLE_AREA'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['EXT_GROSS_AREA'] = pd.to_numeric(tmp_1['EXT_GROSS_AREA'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['BUILDING_NAME'] = tmp_2['BUILDING_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['BUILDING_NAME_LONG'] = tmp_3['BUILDING_NAME_LONG'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['FAC_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(tmp_0['ROOM_SQUARE_FOOTAGE'], errors='coerce').astype(float)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['ROOM_NUMBER'] = tmp_1['ROOM_NUMBER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_KEY', 'FLOOR_KEY', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
rooms = prepared_table_1.copy()
# Join room square footage from table_3
rooms_areas = rooms.merge(
    prepared_table_3,
    how='left',
    left_on=['BUILDING_KEY','FLOOR_KEY','ROOM'],
    right_on=['BUILDING_KEY','FLOOR_KEY','ROOM_NUMBER']
)
# Prefer AREA from table_1 when present; otherwise use ROOM_SQUARE_FOOTAGE
rooms_areas['room_area'] = rooms_areas['AREA']
mask_na = rooms_areas['room_area'].isna()
rooms_areas.loc[mask_na, 'room_area'] = rooms_areas.loc[mask_na, 'ROOM_SQUARE_FOOTAGE']
# Compute floor area by aggregating room_area within BUILDING_KEY+FLOOR_KEY
floor_area = rooms_areas.groupby(['BUILDING_KEY','FLOOR_KEY'], as_index=False)['room_area'].sum().rename(columns={'room_area':'floor_total_area'})
rooms_floor = rooms_areas.merge(floor_area, how='left', on=['BUILDING_KEY','FLOOR_KEY'])
# Join building info
rooms_bldg = rooms_floor.merge(
    prepared_table_2,
    how='left',
    left_on='BUILDING_KEY',
    right_on='FAC_BUILDING_KEY'
)
# Compute percentages; use ASSIGNABLE_AREA as building denominator when available; fallback to EXT_GROSS_AREA
rooms_bldg['pct_room_of_floor'] = (rooms_bldg['room_area'] / rooms_bldg['floor_total_area']) * 100.0
# Building denominator selection
bldg_denom = rooms_bldg['ASSIGNABLE_AREA'].where(~rooms_bldg['ASSIGNABLE_AREA'].isna(), rooms_bldg['EXT_GROSS_AREA'])
rooms_bldg['pct_room_of_building'] = (rooms_bldg['room_area'] / bldg_denom) * 100.0
# Choose room full name with fallback to SPACE_ID or ROOM
rooms_bldg['room_full_name_final'] = rooms_bldg['ROOM_FULL_NAME']
rooms_bldg.loc[rooms_bldg['room_full_name_final'].isna() | (rooms_bldg['room_full_name_final'].astype(str).str.strip() == ''), 'room_full_name_final'] = rooms_bldg['SPACE_ID']
rooms_bldg.loc[rooms_bldg['room_full_name_final'].isna() | (rooms_bldg['room_full_name_final'].astype(str).str.strip() == ''), 'room_full_name_final'] = rooms_bldg['ROOM']
# Pick a building name with preference to BUILDING_NAME, fallback to BUILDING_NAME_LONG
rooms_bldg['building_name_final'] = rooms_bldg['BUILDING_NAME']
rooms_bldg.loc[rooms_bldg['building_name_final'].isna() | (rooms_bldg['building_name_final'].astype(str).str.strip() == ''), 'building_name_final'] = rooms_bldg['BUILDING_NAME_LONG']
# Final selection of requested details
target = rooms_bldg[[
    'room_full_name_final',
    'building_name_final',
    'FLOOR',
    'ORGANIZATION_NAME',
    'DEPT_CODE',
    'room_area',
    'floor_total_area',
    'ASSIGNABLE_AREA',
    'EXT_GROSS_AREA',
    'pct_room_of_floor',
    'pct_room_of_building'
]].rename(columns={
    'room_full_name_final':'room_full_name',
    'building_name_final':'building_name',
    'FLOOR':'floor_number',
    'ORGANIZATION_NAME':'organization_name',
    'DEPT_CODE':'department_code',
    'ASSIGNABLE_AREA':'building_assignable_area',
    'EXT_GROSS_AREA':'building_gross_area'
})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
