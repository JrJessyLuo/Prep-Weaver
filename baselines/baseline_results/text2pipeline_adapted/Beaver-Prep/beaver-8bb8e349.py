import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'BLDG_GROSS_SQUARE_FOOTAGE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_STREET_ADDRESS', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'BUILDING_HEIGHT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_NUMBER', 'BUILDING_HEIGHT', 'BUILDING_NAME', 'SITE', 'CAMPUS_SECTOR']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FLOOR', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ROOM_SQUARE_FOOTAGE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'ROOM_SQUARE_FOOTAGE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BLDG_GROSS_SQUARE_FOOTAGE'] = pd.to_numeric(tmp_0['BLDG_GROSS_SQUARE_FOOTAGE'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = pd.to_numeric(tmp_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['BUILDING_KEY'] = tmp_2['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['BUILDING_NUMBER'] = tmp_3['BUILDING_NUMBER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['BUILDING_NAME'] = tmp_4['BUILDING_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['BUILDING_STREET_ADDRESS'] = tmp_5['BUILDING_STREET_ADDRESS'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_HEIGHT'] = pd.to_numeric(tmp_0['BUILDING_HEIGHT'], errors='coerce').astype(float)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['BUILDING_NUMBER'] = tmp_1['BUILDING_NUMBER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['BUILDING_NAME'] = tmp_2['BUILDING_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['BUILDING_NUMBER', 'BUILDING_HEIGHT', 'BUILDING_NAME', 'SITE', 'CAMPUS_SECTOR']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['FLOOR'] = tmp_1['FLOOR'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['FLOOR'] = pd.to_numeric(tmp_2['FLOOR'], errors='coerce').astype(float)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['BUILDING_KEY', 'FLOOR']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(tmp_1['ROOM_SQUARE_FOOTAGE'], errors='coerce').astype(float)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_KEY', 'ROOM_SQUARE_FOOTAGE']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
b = prepared_table_1.copy()
f = prepared_table_3.copy()
r = prepared_table_4.copy()
meta = prepared_table_2.copy()

# Join building metadata (height) to base building table via BUILDING_NUMBER
bf = b.merge(meta, how='left', on='BUILDING_NUMBER')

# Compute smallest and largest floor level per building using numeric-capable casting when possible
# Attempt to cast FLOOR to numeric; errors become NaN and will be ignored in min/max
f_num = f.copy()
try:
    f_num['FLOOR_NUM'] = pd.to_numeric(f_num['FLOOR'], errors='coerce')
except Exception:
    f_num['FLOOR_NUM'] = pd.to_numeric(f_num['FLOOR'].astype(str).str.strip(), errors='coerce')

floor_agg = (
    f_num.groupby('BUILDING_KEY', as_index=False)
         .agg(SMALLEST_FLOOR_LEVEL=('FLOOR_NUM', 'min'), LARGEST_FLOOR_LEVEL=('FLOOR_NUM', 'max'))
)

# Aggregate total room area per building
rooms_agg = (
    r.groupby('BUILDING_KEY', as_index=False)
     .agg(TOTAL_ROOM_AREA_SF=('ROOM_SQUARE_FOOTAGE', 'sum'))
)

# Integrate all on BUILDING_KEY
integrated = (
    bf.merge(floor_agg, how='left', on='BUILDING_KEY')
      .merge(rooms_agg, how='left', on='BUILDING_KEY')
)

# Prepare final projection and column names required by the question
# City, state, and postal code are not present as discrete columns; provide best-available fields.
# Use placeholders by omitting non-existent columns and returning available address context.
cols = [
    'BUILDING_KEY',
    'BUILDING_NAME',
    'BUILDING_HEIGHT',
    'BUILDING_STREET_ADDRESS',
    'SITE',
    'CAMPUS_SECTOR',
    'BLDG_GROSS_SQUARE_FOOTAGE',
    'BLDG_ASSIGNABLE_SQUARE_FOOTAGE',
    'SMALLEST_FLOOR_LEVEL',
    'LARGEST_FLOOR_LEVEL',
    'TOTAL_ROOM_AREA_SF'
]
existing_cols = [c for c in cols if c in integrated.columns]
target = integrated[existing_cols]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
