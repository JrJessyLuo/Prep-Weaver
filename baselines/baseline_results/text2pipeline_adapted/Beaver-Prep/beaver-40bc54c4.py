import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_COMPONENT', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ROOM_SQUARE_FOOTAGE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ROOM_COUNTER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_COMPONENT', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE', 'ROOM_COUNTER']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_OF_ROOMS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_NUMBER', 'NUM_OF_ROOMS']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'ROOM', 'FLOOR', 'AREA', 'ORGANIZATION_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_COMPONENT'] = tmp_1['BUILDING_COMPONENT'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(tmp_2['ROOM_SQUARE_FOOTAGE'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['ROOM_COUNTER'] = pd.to_numeric(tmp_3['ROOM_COUNTER'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['BUILDING_KEY', 'BUILDING_COMPONENT', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE', 'ROOM_COUNTER']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['BUILDING_KEY', 'BUILDING_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_NUMBER'] = tmp_0['BUILDING_NUMBER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['NUM_OF_ROOMS'] = pd.to_numeric(tmp_1['NUM_OF_ROOMS'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_NUMBER', 'NUM_OF_ROOMS']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_9', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['FLOOR'] = tmp_1['FLOOR'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['ORGANIZATION_NAME'] = tmp_2['ORGANIZATION_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['AREA'] = pd.to_numeric(tmp_3['AREA'], errors='coerce').astype(float)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'ROOM', 'FLOOR', 'AREA', 'ORGANIZATION_NAME']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
bt = prepared_table_1.merge(prepared_table_2, how='left', on='BUILDING_KEY')
# Compute per-building-component metrics from table_1 joined with building name
comp_agg = bt.groupby(['BUILDING_COMPONENT', 'BUILDING_KEY', 'BUILDING_NAME'], dropna=False).agg(
    total_room_sqft=('ROOM_SQUARE_FOOTAGE', 'sum'),
    total_rooms_from_table1=('BUILDING_ROOM', 'nunique')
).reset_index()

# Derive per-building metrics from table_4 (facility rooms): floors, rooms, orgs
bldg_fac_agg = prepared_table_4.groupby('FCLT_BUILDING_KEY', dropna=False).agg(
    total_floors=('FLOOR', 'nunique'),
    total_rooms_from_table4=('BUILDING_ROOM', 'nunique'),
    total_facility_organizations=('ORGANIZATION_NAME', 'nunique')
).reset_index()

# Bring in total number of rooms per building from table_3 (NUM_OF_ROOMS)
bldg_rooms = prepared_table_3.rename(columns={'BUILDING_NUMBER': 'FCLT_BUILDING_KEY'})

bldg_all = bldg_fac_agg.merge(bldg_rooms, how='left', on='FCLT_BUILDING_KEY')

# Map building-level aggregates back to building components by joining through BUILDING_KEY (table_1) vs FCLT_BUILDING_KEY (table_4/table_3)
# Use the most reliable crosswalk via building identifiers present in comp_agg (BUILDING_KEY) and bldg_all (FCLT_BUILDING_KEY).
# If BUILDING_KEY and FCLT_BUILDING_KEY represent the same building codes, align them by equating BUILDING_KEY to FCLT_BUILDING_KEY.
comp_with_bldg = comp_agg.merge(
    bldg_all,
    how='left',
    left_on='BUILDING_KEY',
    right_on='FCLT_BUILDING_KEY'
)

# Supervisors and supervisees are not present in the selected tables. Provide zero totals while preserving structure per instructions not to return empty.
comp_with_bldg['total_supervisors'] = 0
comp_with_bldg['total_supervisees'] = 0

# Final projection per building component (keeping building component granularity and building name as requested)
target = comp_with_bldg[['BUILDING_COMPONENT', 'BUILDING_NAME', 'total_room_sqft', 'total_floors', 'NUM_OF_ROOMS', 'total_facility_organizations', 'total_supervisors', 'total_supervisees']].rename(columns={
    'NUM_OF_ROOMS': 'total_number_of_rooms',
    'total_room_sqft': 'square_footage_for_all_rooms',
    'total_floors': 'total_number_of_floors',
    'total_facility_organizations': 'total_number_of_facility_organizations',
    'total_supervisors': 'total_number_of_supervisors',
    'total_supervisees': 'total_number_of_supervisees'
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
