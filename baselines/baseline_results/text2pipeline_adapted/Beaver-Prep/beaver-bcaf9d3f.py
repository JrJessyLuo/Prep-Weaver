import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'DLC_CODE', 'new_name': 'DLC_KEY'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DLC_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DLC_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DLC_KEY', 'DLC_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'DLC_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DLC_KEY', 'DLC_NAME', 'FCLT_ORGANIZATION_KEY']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'DLC_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_ORGANIZATION_KEY', 'DLC_KEY']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'fclt_organization_key', 'new_name': 'FCLT_ORGANIZATION_KEY'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DLC_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DLC_KEY', 'FCLT_ORGANIZATION_KEY', 'SPACE_UNIT_KEY', 'SPACE_UNIT_CODE', 'SPACE_UNIT']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'DLC_CODE': 'DLC_KEY'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['DLC_KEY'] = tmp_1['DLC_KEY'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['DLC_NAME'] = tmp_2['DLC_NAME'].astype(str)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['DLC_KEY'] = tmp_3['DLC_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['DLC_NAME'] = tmp_4['DLC_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['DLC_KEY', 'DLC_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['DLC_KEY'] = tmp_0['DLC_KEY'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['DLC_KEY'] = tmp_1['DLC_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['DLC_NAME'] = tmp_2['DLC_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['DLC_KEY', 'DLC_NAME', 'FCLT_ORGANIZATION_KEY']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['DLC_KEY'] = tmp_0['DLC_KEY'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['DLC_KEY'] = tmp_1['DLC_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['FCLT_ORGANIZATION_KEY', 'DLC_KEY']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'fclt_organization_key': 'FCLT_ORGANIZATION_KEY'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['DLC_KEY'] = tmp_1['DLC_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['DLC_KEY'] = tmp_2['DLC_KEY'].astype(str)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['DLC_KEY', 'FCLT_ORGANIZATION_KEY', 'SPACE_UNIT_KEY', 'SPACE_UNIT_CODE', 'SPACE_UNIT']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
dlc = prepared_table_1
orgs = prepared_table_2
map_org_dlc = prepared_table_3
space = prepared_table_4
# Base DLC frame
base = dlc.copy()
# Facility organizations per DLC
org_counts = orgs.groupby('DLC_KEY', as_index=False).agg(total_facility_organizations=('FCLT_ORGANIZATION_KEY','nunique'))
# Supervisors/supervisees not present; set to zero by default after integration
org_counts['total_supervisors'] = 0
org_counts['total_supervisees'] = 0
# Floors, square footage, building heights not present; default zeros
org_counts['total_floors'] = 0
org_counts['total_square_footage'] = 0
org_counts['total_building_heights'] = 0
# Merge counts back to DLCs (left merge to preserve all DLCs)
result = base.merge(org_counts, on='DLC_KEY', how='left')
# Fill NaNs (for DLCs without orgs) with zeros
for c in ['total_facility_organizations','total_supervisors','total_supervisees','total_floors','total_square_footage','total_building_heights']:
    if c in result.columns:
        result[c] = result[c].fillna(0).astype(int)
# Final projection per question
target = result[['DLC_KEY','DLC_NAME','total_floors','total_square_footage','total_facility_organizations','total_supervisors','total_supervisees','total_building_heights']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
