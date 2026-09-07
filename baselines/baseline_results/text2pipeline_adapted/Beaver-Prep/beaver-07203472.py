import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'BUILDING_NUMBER', 'new_name': 'BUILDING_KEY'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'EXT_GROSS_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_USE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'PARENT_BUILDING_NUMBER', 'EXT_GROSS_AREA', 'BUILDING_USE']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FCLT_BUILDING_KEY', 'new_name': 'BUILDING_KEY'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_NAME', 'func': "def transform(s):\n    return str(s).strip().upper() if s is not None and str(s).lower() != 'nan' else None"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'BUILDING_NUMBER': 'BUILDING_KEY'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['EXT_GROSS_AREA'] = pd.to_numeric(tmp_1['EXT_GROSS_AREA'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['BUILDING_USE'] = tmp_2['BUILDING_USE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['BUILDING_KEY', 'PARENT_BUILDING_NUMBER', 'EXT_GROSS_AREA', 'BUILDING_USE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_6', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'FCLT_BUILDING_KEY': 'BUILDING_KEY'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip().upper() if s is not None and str(s).lower() != 'nan' else None", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['ORGANIZATION_NAME'] = tmp_1['ORGANIZATION_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
b = prepared_table_1.copy()
r = prepared_table_2.copy()

# Exclude subdivisions by keeping only buildings where PARENT_BUILDING_NUMBER is null/NaN or empty after strip
b['PARENT_BUILDING_NUMBER'] = b['PARENT_BUILDING_NUMBER'].astype(str)
b['PARENT_BUILDING_NUMBER'] = b['PARENT_BUILDING_NUMBER'].where(~b['PARENT_BUILDING_NUMBER'].str.lower().isin(['nan', 'none']), '')
b_main = b[b['PARENT_BUILDING_NUMBER'].fillna('').str.strip() == ''].copy()

# Determine use display, with RESIDENTIAL override when BUILDING_USE indicates residence
use_series = b_main['BUILDING_USE'].fillna('').astype(str).str.strip()
use_series_upper = use_series.str.upper()
# Heuristic for residential classifications
is_res = use_series_upper.str.startswith('RES') | use_series_upper.isin(['RES', 'RESIDENTIAL', 'HOUSING', 'DORM', 'DORMITORY'])
# If residential, label as RESIDENTIAL; otherwise keep original (preserve original case where possible)
b_main['USE_DISPLAY'] = use_series.where(~is_res, 'RESIDENTIAL')

# Ensure EXT_GROSS_AREA numeric already float; keep as is
# Count buildings and sum gross area by use
buildings_by_use = b_main.groupby('USE_DISPLAY', as_index=False).agg(
    buildings_count=('BUILDING_KEY', 'nunique'),
    gross_sqft=('EXT_GROSS_AREA', 'sum')
)

# Join rooms to buildings to associate organizations by use
rooms_join = r.merge(b_main[['BUILDING_KEY', 'USE_DISPLAY']], on='BUILDING_KEY', how='inner')
# Build an organization uniqueness token preferring key, falling back to name
org_id = rooms_join['FCLT_ORGANIZATION_KEY'].astype(str)
org_id = org_id.where(~org_id.str.lower().isin(['nan', 'none']), '')
org_name = rooms_join['ORGANIZATION_NAME'].fillna('').astype(str).str.strip()
rooms_join['ORG_UNIQUE'] = org_id
mask_empty = rooms_join['ORG_UNIQUE'] == ''
rooms_join.loc[mask_empty, 'ORG_UNIQUE'] = 'NAME::' + org_name[mask_empty]

orgs_by_use = rooms_join.groupby('USE_DISPLAY', as_index=False)['ORG_UNIQUE'].nunique().rename(columns={'ORG_UNIQUE': 'organizations_count'})

# Combine counts
out = buildings_by_use.merge(orgs_by_use, on='USE_DISPLAY', how='left')
out['organizations_count'] = out['organizations_count'].fillna(0).astype(int)

# Totals row across all uses
total_buildings = b_main['BUILDING_KEY'].nunique()
total_gross = b_main['EXT_GROSS_AREA'].sum()
all_orgs = rooms_join['ORG_UNIQUE'].nunique()

# Round and ensure int types for formatting
out['buildings_count'] = out['buildings_count'].round(0).astype(int)
out['gross_sqft'] = out['gross_sqft'].round(0).astype(int)

# Create totals row DataFrame
total_row_df = out.iloc[0:0].copy()
total_row_df.loc[:, 'USE_DISPLAY'] = ['TOTAL']
total_row_df.loc[:, 'buildings_count'] = [int(round(total_buildings))]
total_row_df.loc[:, 'gross_sqft'] = [int(round(total_gross))]
total_row_df.loc[:, 'organizations_count'] = [int(all_orgs)]

# Concatenate totals row
out = out.sort_values('USE_DISPLAY').reset_index(drop=True)
out = pd.concat([out, total_row_df], ignore_index=True)

# Final formatting with commas
out['buildings_count'] = out['buildings_count'].map(lambda x: f"{x:,}")
out['gross_sqft'] = out['gross_sqft'].map(lambda x: f"{x:,}")
out['organizations_count'] = out['organizations_count'].map(lambda x: f"{x:,}")

# Final projection and column names per question
out = out.rename(columns={'USE_DISPLAY': 'USE_TYPE', 'buildings_count': 'NUMBER_OF_BUILDINGS', 'gross_sqft': 'TOTAL_GROSS_SQFT', 'organizations_count': 'NUMBER_OF_ORGANIZATIONS'})

target = out[['USE_TYPE', 'NUMBER_OF_BUILDINGS', 'TOTAL_GROSS_SQFT', 'NUMBER_OF_ORGANIZATIONS']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
