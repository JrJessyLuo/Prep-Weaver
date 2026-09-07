import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'ROOM', 'ROOM_FULL_NAME', 'AREA', 'MAJOR_USE_DESC', 'ORGANIZATION_NAME', 'fac_room_key']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FAC_BUILDING_KEY', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['AREA'] = pd.to_numeric(tmp_1['AREA'], errors='coerce').astype(float)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_KEY', 'ROOM', 'ROOM_FULL_NAME', 'AREA', 'MAJOR_USE_DESC', 'ORGANIZATION_NAME', 'fac_room_key']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FAC_BUILDING_KEY'] = tmp_0['FAC_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, left_on='BUILDING_KEY', right_on='FAC_BUILDING_KEY', how='inner')
# Filter to building 45 using multiple plausible columns (string-compare, case-insensitive); fallback keeps any rows with BUILDING_KEY == '45'
bnum_mask = (integrated['BUILDING_NUMBER'].astype(str).str.strip().str.lower() == '45') if 'BUILDING_NUMBER' in integrated.columns else False
bkey_mask = integrated['BUILDING_KEY'].astype(str).str.strip().str.lower() == '45'
mask = bnum_mask | bkey_mask
filtered = integrated[mask]
if filtered.empty:
    filtered = integrated[integrated['BUILDING_KEY'].astype(str).str.strip().str.lower() == '45']
# Compute counts per major use and total area per organization for the filtered building
# Prepare helper aggregations
counts_per_major_use = filtered.groupby('MAJOR_USE_DESC', dropna=False)['fac_room_key'].count().rename('rooms_per_major_use')
area_per_org = filtered.groupby('ORGANIZATION_NAME', dropna=False)['AREA'].sum(min_count=1).rename('total_area_by_org')
# Attach aggregations back to each room row for reference
result = filtered.merge(counts_per_major_use.reset_index(), on='MAJOR_USE_DESC', how='left')
result = result.merge(area_per_org.reset_index(), on='ORGANIZATION_NAME', how='left')
# Final projection: list all rooms in building 45 with requested fields
cols = [
    'ROOM',
    'ROOM_FULL_NAME',
    'AREA',
    'MAJOR_USE_DESC',
    'ORGANIZATION_NAME',
    'rooms_per_major_use',
    'total_area_by_org'
]
# Ensure columns exist even if some descriptors are missing
existing_cols = [c for c in cols if c in result.columns]
target = result[existing_cols].sort_values(by=['MAJOR_USE_DESC','ROOM'], kind='stable')

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
