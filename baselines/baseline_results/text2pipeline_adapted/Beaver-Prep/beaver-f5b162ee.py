import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'FCLT_MAJOR_USE_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MAJOR_USE_DESC', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['BUILDING_ROOM', 'FCLT_BUILDING_KEY', 'FLOOR', 'FCLT_FLOOR_KEY', 'ROOM', 'SPACE_ID', 'FCLT_USE_KEY', 'USE_DESC', 'FCLT_MINOR_USE_KEY', 'MINOR_USE_DESC', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_MINOR_ORGANIZATION_KEY', 'MINOR_ORGANIZATION', 'ROOM_FULL_NAME', 'DEPT_CODE', 'ACCESS_LEVEL', 'LATITUDE_WGS', 'LONGITUDE_WGS', 'NORTHING_SPCS', 'EASTING_SPCS', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_ROOM_KEY', 'FCLT_MAJOR_USE_KEY', 'MAJOR_USE_DESC', 'AREA']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'FCLT_MAJOR_USE_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ASSIGNABLE', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DESCRIPTION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'DESCRIPTION', 'new_name': 'MAJOR_USE_DESC'}]}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['MAJOR_USE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_MAJOR_USE_KEY', 'ASSIGNABLE', 'MAJOR_USE_DESC']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FCLT_MAJOR_USE_KEY'] = pd.to_numeric(tmp_0['FCLT_MAJOR_USE_KEY'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['AREA'] = pd.to_numeric(tmp_1['AREA'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['MAJOR_USE_DESC'] = tmp_2['MAJOR_USE_DESC'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['BUILDING_ROOM', 'FCLT_BUILDING_KEY', 'FLOOR', 'FCLT_FLOOR_KEY', 'ROOM', 'SPACE_ID', 'FCLT_USE_KEY', 'USE_DESC', 'FCLT_MINOR_USE_KEY', 'MINOR_USE_DESC', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_MINOR_ORGANIZATION_KEY', 'MINOR_ORGANIZATION', 'ROOM_FULL_NAME', 'DEPT_CODE', 'ACCESS_LEVEL', 'LATITUDE_WGS', 'LONGITUDE_WGS', 'NORTHING_SPCS', 'EASTING_SPCS', 'WAREHOUSE_LOAD_DATE'], errors='ignore').copy()
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['FCLT_ROOM_KEY', 'FCLT_MAJOR_USE_KEY', 'MAJOR_USE_DESC', 'AREA']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_7', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FCLT_MAJOR_USE_KEY'] = pd.to_numeric(tmp_0['FCLT_MAJOR_USE_KEY'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ASSIGNABLE'] = pd.to_numeric(tmp_1['ASSIGNABLE'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['DESCRIPTION'] = tmp_2['DESCRIPTION'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'DESCRIPTION': 'MAJOR_USE_DESC'})
    # Step 5: DropColumn
    tmp_4 = tmp_3.drop(columns=['MAJOR_USE', 'WAREHOUSE_LOAD_DATE'], errors='ignore').copy()
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['FCLT_MAJOR_USE_KEY', 'ASSIGNABLE', 'MAJOR_USE_DESC']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='FCLT_MAJOR_USE_KEY', how='left')
# Prefer the lookup description if present; otherwise keep the room's own description
integrated['MAJOR_USE_DESC_FINAL'] = integrated['MAJOR_USE_DESC_y'].where(integrated['MAJOR_USE_DESC_y'].notna() & (integrated['MAJOR_USE_DESC_y'].astype(str).str.len()>0), integrated['MAJOR_USE_DESC_x'])
# Filter out rows where either major use code or description starts with 'ZUSE.' (case-insensitive, robust to nulls)
starts_with_zuse = (
    integrated['MAJOR_USE_DESC_FINAL'].astype(str).str.upper().str.startswith('ZUSE.') |
    integrated['MAJOR_USE_DESC_x'].astype(str).str.upper().str.startswith('ZUSE.')
)
integrated = integrated.loc[~starts_with_zuse].copy()
# Compute group aggregates by assignable and major use description
# Map ASSIGNABLE numeric to labels for display grouping
assignable_label = integrated['ASSIGNABLE'].map({1: 'ASSIGNABLE', 0: 'NON-ASSIGNABLE'})
integrated['ASSIGNABLE_LABEL'] = assignable_label
# If ASSIGNABLE is missing, infer NON-ASSIGNABLE as fallback to avoid losing rows
integrated.loc[integrated['ASSIGNABLE_LABEL'].isna(), 'ASSIGNABLE_LABEL'] = 'NON-ASSIGNABLE'
# Clean final description text
integrated['MAJOR_USE_DESC_FINAL'] = integrated['MAJOR_USE_DESC_FINAL'].fillna('')
# Aggregate counts and areas
grp = integrated.groupby(['ASSIGNABLE_LABEL', 'MAJOR_USE_DESC_FINAL'], dropna=False).agg(
    TOTAL_ROOMS=('FCLT_ROOM_KEY', 'count'),
    TOTAL_AREA=('AREA', 'sum'),
    AVG_AREA=('AREA', 'mean')
).reset_index()
# Sort by assignable then description
grp = grp.sort_values(['ASSIGNABLE_LABEL', 'MAJOR_USE_DESC_FINAL'], kind='mergesort').reset_index(drop=True)
# Build subtotal rows per assignable group
subtotals = grp.groupby('ASSIGNABLE_LABEL', as_index=False).agg(
    TOTAL_ROOMS=('TOTAL_ROOMS', 'sum'),
    TOTAL_AREA=('TOTAL_AREA', 'sum'),
    AVG_AREA=('AVG_AREA', 'mean')
)
subtotals['MAJOR_USE_DESC_FINAL'] = 'Subtotal'
# Insert subtotal rows after each assignable group while keeping sort order
rows = []
for label, block in grp.groupby('ASSIGNABLE_LABEL', sort=False):
    rows.append(block)
    rows.append(subtotals.loc[subtotals['ASSIGNABLE_LABEL'] == label, ['ASSIGNABLE_LABEL','MAJOR_USE_DESC_FINAL','TOTAL_ROOMS','TOTAL_AREA','AVG_AREA']])
stacked = pd.concat(rows, ignore_index=True)
# Grand total row
grand = pd.DataFrame({
    'ASSIGNABLE_LABEL': [''],
    'MAJOR_USE_DESC_FINAL': ['Grand Total'],
    'TOTAL_ROOMS': [stacked.loc[stacked['MAJOR_USE_DESC_FINAL']!='Subtotal','TOTAL_ROOMS'].sum()],
    'TOTAL_AREA': [stacked.loc[stacked['MAJOR_USE_DESC_FINAL']!='Subtotal','TOTAL_AREA'].sum()],
    'AVG_AREA': [grp['AVG_AREA'].mean()]
})
# For subtotal rows, blank out assignable label; for data rows, we'll blank repeated values later
stacked.loc[stacked['MAJOR_USE_DESC_FINAL']=='Subtotal', 'ASSIGNABLE_LABEL'] = ''
# Append grand total
result = pd.concat([stacked, grand], ignore_index=True)
# Suppress repeated display values: only show assignable/description when they differ from previous row
result = result.sort_values(['ASSIGNABLE_LABEL', 'MAJOR_USE_DESC_FINAL'], kind='mergesort').reset_index(drop=True)
prev_assign = None
prev_desc = None
assign_shown = []
desc_shown = []
for i, row in result.iterrows():
    a = row['ASSIGNABLE_LABEL']
    d = row['MAJOR_USE_DESC_FINAL']
    if d in ['Subtotal', 'Grand Total']:
        assign_shown.append('')
        desc_shown.append(d)
        prev_assign = a if d=='Subtotal' else prev_assign
        prev_desc = d if d=='Subtotal' else prev_desc
        continue
    show_a = a if a != prev_assign else ''
    show_d = d if d != prev_desc else ''
    assign_shown.append(show_a)
    desc_shown.append(show_d)
    prev_assign = a
    prev_desc = d
result['ASSIGNABLE_STATUS'] = assign_shown
result['MAJOR_USE_DESCRIPTION'] = desc_shown
# Final sort as required
result = result.sort_values(['ASSIGNABLE_STATUS', 'MAJOR_USE_DESCRIPTION'], kind='mergesort').reset_index(drop=True)
# Final projection and column order
target = result[['ASSIGNABLE_STATUS', 'MAJOR_USE_DESCRIPTION', 'TOTAL_ROOMS', 'TOTAL_AREA', 'AVG_AREA']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
