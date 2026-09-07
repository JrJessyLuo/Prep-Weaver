import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'EXT_GROSS_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_OF_ROOMS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNERSHIP_TYPE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_USE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'OWNERSHIP_TYPE', 'BUILDING_USE', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'FCLT_ORGANIZATION_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_NAME', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['EXT_GROSS_AREA'] = pd.to_numeric(tmp_0['EXT_GROSS_AREA'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['NUM_OF_ROOMS'] = pd.to_numeric(tmp_1['NUM_OF_ROOMS'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['OWNERSHIP_TYPE'] = tmp_2['OWNERSHIP_TYPE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['BUILDING_USE'] = tmp_3['BUILDING_USE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['FCLT_BUILDING_KEY', 'OWNERSHIP_TYPE', 'BUILDING_USE', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FCLT_ORGANIZATION_KEY'] = pd.to_numeric(tmp_0['FCLT_ORGANIZATION_KEY'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['ORGANIZATION_NAME'] = tmp_1['ORGANIZATION_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
b = prepared_table_1.copy()
# Merge buildings with room/org assignments to compute distinct orgs per building
bro = prepared_table_2.copy()
# Prefer org key for distinctness; fallback to name if key is null
bro['_org_id'] = bro['FCLT_ORGANIZATION_KEY']
# Build per-building distinct org counts
org_counts = (
    bro.assign(_org_fallback=bro['_org_id'].astype('Int64'))
)
# If org key is missing, use name; create a unified token
org_counts['_org_token'] = org_counts['_org_fallback'].astype('string')
mask_missing = org_counts['_org_fallback'].isna()
org_counts.loc[mask_missing, '_org_token'] = org_counts.loc[mask_missing, 'ORGANIZATION_NAME'].astype('string')
org_counts = org_counts[['FCLT_BUILDING_KEY', '_org_token']].drop_duplicates()
org_counts = org_counts.groupby('FCLT_BUILDING_KEY', as_index=False).size().rename(columns={'size': 'ORG_COUNT'})
# Join org counts to buildings (left join to preserve buildings without rooms)
b_merged = b.merge(org_counts, on='FCLT_BUILDING_KEY', how='left')
b_merged['ORG_COUNT'] = b_merged['ORG_COUNT'].fillna(0).astype(int)
# Prepare grouping fields
b_merged['OWNERSHIP_TYPE'] = b_merged['OWNERSHIP_TYPE'].fillna('').str.strip().str.upper()
b_merged['BUILDING_USE'] = b_merged['BUILDING_USE'].fillna('').str.strip()
# Map ownership grouping to Owned vs Leased buckets; leave other as-is
bucket = b_merged['OWNERSHIP_TYPE']
# Normalize common variants
bucket = bucket.replace({'OWNED': 'OWNED', 'LEASED': 'LEASED'})
b_merged['OWNERSHIP_GROUP'] = bucket.where(bucket.isin(['OWNED', 'LEASED']), 'OTHER')
# Aggregate per ownership group and usage type
grp = b_merged.groupby(['OWNERSHIP_GROUP', 'BUILDING_USE'], as_index=False).agg(
    BUILDINGS=('FCLT_BUILDING_KEY', 'nunique'),
    GROSS_SF=('EXT_GROSS_AREA', 'sum'),
    ROOMS=('NUM_OF_ROOMS', 'sum'),
    ORGS=('ORG_COUNT', 'sum')
)
# Subtotals per ownership group
subs = grp.groupby('OWNERSHIP_GROUP', as_index=False).agg(
    BUILDINGS=('BUILDINGS', 'sum'),
    GROSS_SF=('GROSS_SF', 'sum'),
    ROOMS=('ROOMS', 'sum'),
    ORGS=('ORGS', 'sum')
)
subs['BUILDING_USE'] = ''
subs['ROW_TYPE'] = 'Subtotal'
# Mark detail rows
grp['ROW_TYPE'] = 'Detail'
# Concatenate detail and subtotals, ordered by ownership group, with detail rows first
ordered_groups = ['OWNED', 'LEASED', 'OTHER']
grp['OWNERSHIP_GROUP'] = pd.Categorical(grp['OWNERSHIP_GROUP'], ordered=True, categories=ordered_groups + [g for g in grp['OWNERSHIP_GROUP'].unique() if g not in ordered_groups])
subs['OWNERSHIP_GROUP'] = pd.Categorical(subs['OWNERSHIP_GROUP'], ordered=True, categories=grp['OWNERSHIP_GROUP'].cat.categories)
combined = pd.concat([grp, subs], ignore_index=True)
combined = combined.sort_values(['OWNERSHIP_GROUP', 'ROW_TYPE', 'BUILDING_USE'])
# Grand total
grand = combined[combined['ROW_TYPE'].isin(['Detail', 'Subtotal'])].agg({
    'BUILDINGS': 'sum', 'GROSS_SF': 'sum', 'ROOMS': 'sum', 'ORGS': 'sum'
}).to_frame().T
grand['OWNERSHIP_GROUP'] = ''
grand['BUILDING_USE'] = ''
grand['ROW_TYPE'] = 'Grand Total'
# Append grand total
final = pd.concat([combined, grand], ignore_index=True)
# Round and format GROSS_SF with commas
final['GROSS_SF'] = final['GROSS_SF'].round(0).astype('Int64').map(lambda x: f"{int(x):,}" if pd.notna(x) else '')
# For subtotal and grand total rows, suppress ownership and usage display
mask_total = final['ROW_TYPE'].isin(['Subtotal', 'Grand Total'])
final.loc[mask_total, 'OWNERSHIP_GROUP'] = ''
final.loc[mask_total, 'BUILDING_USE'] = ''
# Display ownership type only when it differs from previous row
# Implement by blanking repeated ownership in consecutive detail rows within sorted order
display_col = []
prev = None
for _, r in final.iterrows():
    if r['ROW_TYPE'] == 'Detail':
        val = r['OWNERSHIP_GROUP']
        if val == prev:
            display_col.append('')
        else:
            display_col.append(val)
            prev = val
    else:
        display_col.append('')
        # reset prev at boundary of totals to ensure next group's header shows
        prev = None
final['OWNERSHIP_DISPLAY'] = display_col
# Reorder and rename columns for output
target = final[['OWNERSHIP_DISPLAY', 'BUILDING_USE', 'BUILDINGS', 'GROSS_SF', 'ROOMS', 'ORGS', 'ROW_TYPE']].rename(columns={
    'OWNERSHIP_DISPLAY': 'Ownership Type',
    'BUILDING_USE': 'Usage Type',
    'BUILDINGS': 'Buildings',
    'GROSS_SF': 'Gross Sq Ft',
    'ROOMS': 'Rooms',
    'ORGS': 'Associated Orgs',
    'ROW_TYPE': 'Row Type'
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
