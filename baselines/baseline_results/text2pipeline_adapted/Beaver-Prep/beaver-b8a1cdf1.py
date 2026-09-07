import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'FCLT_BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACCESS_LEVEL_CODE', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ACCESS_LEVEL_CODE', 'new_name': 'BUILDING_ACCESS_LEVEL'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME_LONG', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_ACCESS_LEVEL']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'FCLT_BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACCESS_LEVEL', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MAJOR_USE_DESC', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'USE_DESC', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MINOR_USE_DESC', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SPACE_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM_FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'ACCESS_LEVEL', 'MAJOR_USE_DESC', 'USE_DESC', 'MINOR_USE_DESC', 'SPACE_ID', 'AREA', 'ROOM', 'FLOOR', 'ROOM_FULL_NAME', 'ORGANIZATION_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ACCESS_LEVEL_CODE'] = pd.to_numeric(tmp_1['ACCESS_LEVEL_CODE'], errors='coerce').fillna(0).astype(int)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'ACCESS_LEVEL_CODE': 'BUILDING_ACCESS_LEVEL'})
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['BUILDING_NAME'] = tmp_3['BUILDING_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['BUILDING_NAME_LONG'] = tmp_4['BUILDING_NAME_LONG'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_ACCESS_LEVEL']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ACCESS_LEVEL'] = pd.to_numeric(tmp_1['ACCESS_LEVEL'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['AREA'] = pd.to_numeric(tmp_2['AREA'], errors='coerce').astype(float)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['MAJOR_USE_DESC'] = tmp_3['MAJOR_USE_DESC'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['USE_DESC'] = tmp_4['USE_DESC'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_5['MINOR_USE_DESC'] = tmp_5['MINOR_USE_DESC'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_6['ORGANIZATION_NAME'] = tmp_6['ORGANIZATION_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_7['ROOM'] = tmp_7['ROOM'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_8['FLOOR'] = tmp_8['FLOOR'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_9['SPACE_ID'] = tmp_9['SPACE_ID'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_10['ROOM_FULL_NAME'] = tmp_10['ROOM_FULL_NAME'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 12: SelectCol
    result = tmp_10.loc[:, ['FCLT_BUILDING_KEY', 'ACCESS_LEVEL', 'MAJOR_USE_DESC', 'USE_DESC', 'MINOR_USE_DESC', 'SPACE_ID', 'AREA', 'ROOM', 'FLOOR', 'ROOM_FULL_NAME', 'ORGANIZATION_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='left', on='FCLT_BUILDING_KEY')
# Final access level: prefer room ACCESS_LEVEL else BUILDING_ACCESS_LEVEL
integrated['ACCESS_LEVEL_FINAL'] = integrated['ACCESS_LEVEL']
mask_null = integrated['ACCESS_LEVEL_FINAL'].isna()
integrated.loc[mask_null, 'ACCESS_LEVEL_FINAL'] = integrated.loc[mask_null, 'BUILDING_ACCESS_LEVEL']

# Exclude usage types containing STORAGE (case-insensitive) using multiple plausible columns
u_major = integrated['MAJOR_USE_DESC'].astype(str)
u_use = integrated['USE_DESC'].astype(str)
u_minor = integrated['MINOR_USE_DESC'].astype(str)
keep_mask = ~(
    u_major.str.contains('STORAGE', case=False, na=False) |
    u_use.str.contains('STORAGE', case=False, na=False) |
    u_minor.str.contains('STORAGE', case=False, na=False)
)
filtered = integrated[keep_mask].copy()

# Space name: prefer ROOM_FULL_NAME, else SPACE_ID
space_name = filtered['ROOM_FULL_NAME']
space_name = space_name.where(space_name.notna() & (space_name.astype(str).str.strip() != ''), filtered['SPACE_ID'])
filtered['SPACE_NAME'] = space_name

# Aggregate at space level within access level and usage type
grp_cols = ['ACCESS_LEVEL_FINAL', 'MAJOR_USE_DESC', 'SPACE_NAME']
space_agg = filtered.groupby(grp_cols, dropna=False).agg(
    ROOMS_COUNT=('SPACE_ID', 'count'),
    TOTAL_AREA=('AREA', 'sum'),
    AVG_AREA=('AREA', 'mean')
).reset_index()

# Round to integers
for c in ['ROOMS_COUNT', 'TOTAL_AREA', 'AVG_AREA']:
    space_agg[c] = space_agg[c].round(0).astype('Int64')

# Subtotal by (access level, usage type)
sub_usage = space_agg.groupby(['ACCESS_LEVEL_FINAL', 'MAJOR_USE_DESC'], dropna=False).agg(
    ROOMS_COUNT=('ROOMS_COUNT', 'sum'),
    TOTAL_AREA=('TOTAL_AREA', 'sum')
).reset_index()
sub_usage['AVG_AREA'] = (sub_usage['TOTAL_AREA'] / sub_usage['ROOMS_COUNT']).round(0).astype('Int64')
sub_usage['SPACE_NAME'] = 'Subtotal (Access, Usage)'

# Subtotal by access level only
sub_access = space_agg.groupby(['ACCESS_LEVEL_FINAL'], dropna=False).agg(
    ROOMS_COUNT=('ROOMS_COUNT', 'sum'),
    TOTAL_AREA=('TOTAL_AREA', 'sum')
).reset_index()
sub_access['MAJOR_USE_DESC'] = 'Subtotal (Access)'
sub_access['SPACE_NAME'] = ''
sub_access['AVG_AREA'] = (sub_access['TOTAL_AREA'] / sub_access['ROOMS_COUNT']).round(0).astype('Int64')

# Grand total across all access levels
grand = space_agg[['ROOMS_COUNT','TOTAL_AREA']].sum().to_dict()
grand_df = pd.DataFrame([grand])
grand_df['AVG_AREA'] = (grand_df['TOTAL_AREA'] / grand_df['ROOMS_COUNT']).round(0).astype('Int64')
grand_df['ACCESS_LEVEL_FINAL'] = 'All'
grand_df['MAJOR_USE_DESC'] = 'Grand Total'
grand_df['SPACE_NAME'] = ''

# Per-(access, usage, space) subtotal rows (i.e., subtotal at the space name level within each group)
sub_space = space_agg.copy()
sub_space['SPACE_NAME'] = 'Subtotal (Space)'
sub_space = sub_space.groupby(['ACCESS_LEVEL_FINAL', 'MAJOR_USE_DESC', 'SPACE_NAME'], dropna=False).agg(
    ROOMS_COUNT=('ROOMS_COUNT', 'sum'),
    TOTAL_AREA=('TOTAL_AREA', 'sum')
).reset_index()
sub_space['AVG_AREA'] = (sub_space['TOTAL_AREA'] / sub_space['ROOMS_COUNT']).round(0).astype('Int64')

# Detail rows
detail = space_agg.copy()

# Ensure numeric columns are Int64 for all component frames before formatting
for df in [detail, sub_space, sub_usage, sub_access, grand_df]:
    for c in ['ROOMS_COUNT', 'TOTAL_AREA', 'AVG_AREA']:
        df[c] = df[c].astype('Int64')

# Combine all parts
combined = pd.concat([
    detail.assign(_order_level=1, _label='Detail'),
    sub_space.assign(_order_level=2, _label='Subtotal (Space)'),
    sub_usage.assign(_order_level=3, _label='Subtotal (Access, Usage)'),
    sub_access.assign(_order_level=4, _label='Subtotal (Access)'),
    grand_df.assign(_order_level=5, _label='Grand Total')
], ignore_index=True)

# Sort by Access Level, Usage, Space, then order level
combined = combined.sort_values(by=['ACCESS_LEVEL_FINAL', 'MAJOR_USE_DESC', 'SPACE_NAME', '_order_level'], kind='mergesort')

# Format integers with commas
for c in ['ROOMS_COUNT', 'TOTAL_AREA', 'AVG_AREA']:
    combined[c] = combined[c].apply(lambda x: (f"{int(x):,}" if pd.notna(x) else None))

# Display access level only when it differs from the previous entry
combined['ACCESS_LEVEL_DISPLAY'] = combined['ACCESS_LEVEL_FINAL']
combined['ACCESS_LEVEL_DISPLAY'] = combined['ACCESS_LEVEL_DISPLAY'].where(
    combined['ACCESS_LEVEL_FINAL'].ne(combined['ACCESS_LEVEL_FINAL'].shift(1)),
    ''
)

# Final projection and column names
target = combined[[
    'ACCESS_LEVEL_DISPLAY',
    'MAJOR_USE_DESC',
    'SPACE_NAME',
    'ROOMS_COUNT',
    'TOTAL_AREA',
    'AVG_AREA',
    '_label'
]].rename(columns={
    'ACCESS_LEVEL_DISPLAY': 'Access Level',
    'MAJOR_USE_DESC': 'Usage Type',
    'SPACE_NAME': 'Space Name',
    'ROOMS_COUNT': 'Number of Spaces',
    'TOTAL_AREA': 'Total Area',
    'AVG_AREA': 'Average Area',
    '_label': 'Row Type'
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
