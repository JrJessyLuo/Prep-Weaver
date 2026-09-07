import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'FCLT_ORGANIZATION_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ORGANIZATION_LEVEL', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ORGANIZATION_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ORGANIZATION_ID', 'new_name': 'ORG_ID_STR'}, {'old_name': 'ORGANIZATION_LEVEL', 'new_name': 'ORG_LEVEL'}, {'old_name': 'ORGANIZATION_NUMBER', 'new_name': 'ORG_NUMBER_NUM'}, {'old_name': 'ORGANIZATION', 'new_name': 'ORG_CODE'}, {'old_name': 'ORGANIZATION_NAME', 'new_name': 'ORG_NAME'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_ORGANIZATION_KEY', 'ORG_ID_STR', 'ORG_CODE', 'ORG_NAME', 'ORG_LEVEL', 'ORGANIZATION_SORT', 'DLC_KEY', 'DLC_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'FCLT_ORGANIZATION_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_ORGANIZATION_KEY', 'DLC_KEY']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'dlc_key', 'new_name': 'DLC_KEY'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'HIERARCHY_TYPE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MASTER_DEPT_HIER_LEVEL_5_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MASTER_DEPT_HIER_LEVEL_5_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DLC_KEY', 'HIERARCHY_TYPE', 'DLC_NAME', 'MASTER_DEPT_HIER_LEVEL_1_CODE', 'MASTER_DEPT_HIER_LEVEL_1_NAME', 'MASTER_DEPT_HIER_LEVEL_2_CODE', 'MASTER_DEPT_HIER_LEVEL_2_NAME', 'MASTER_DEPT_HIER_LEVEL_3_CODE', 'MASTER_DEPT_HIER_LEVEL_3_NAME', 'MASTER_DEPT_HIER_LEVEL_4_CODE', 'MASTER_DEPT_HIER_LEVEL_4_NAME', 'MASTER_DEPT_HIER_LEVEL_5_CODE', 'MASTER_DEPT_HIER_LEVEL_5_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'HR_ORG_UNIT_TITLE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DIRECTORY_ORG_UNIT_TITLE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MIT_ID', 'EMERITUS_STATUS', 'HR_ORG_UNIT_TITLE', 'DIRECTORY_ORG_UNIT_TITLE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FCLT_ORGANIZATION_KEY'] = pd.to_numeric(tmp_0['FCLT_ORGANIZATION_KEY'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ORGANIZATION_LEVEL'] = pd.to_numeric(tmp_1['ORGANIZATION_LEVEL'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['ORGANIZATION_ID'] = tmp_2['ORGANIZATION_ID'].astype(str)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['ORGANIZATION_ID'] = tmp_3['ORGANIZATION_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['ORGANIZATION'] = tmp_4['ORGANIZATION'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_5['ORGANIZATION_NAME'] = tmp_5['ORGANIZATION_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_6['DLC_NAME'] = tmp_6['DLC_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 8: Rename
    tmp_7 = tmp_6.rename(columns={'ORGANIZATION_ID': 'ORG_ID_STR', 'ORGANIZATION_LEVEL': 'ORG_LEVEL', 'ORGANIZATION_NUMBER': 'ORG_NUMBER_NUM', 'ORGANIZATION': 'ORG_CODE', 'ORGANIZATION_NAME': 'ORG_NAME'})
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['FCLT_ORGANIZATION_KEY', 'ORG_ID_STR', 'ORG_CODE', 'ORG_NAME', 'ORG_LEVEL', 'ORGANIZATION_SORT', 'DLC_KEY', 'DLC_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FCLT_ORGANIZATION_KEY'] = pd.to_numeric(tmp_0['FCLT_ORGANIZATION_KEY'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['DLC_KEY'] = tmp_1['DLC_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['FCLT_ORGANIZATION_KEY', 'DLC_KEY']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_9', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'dlc_key': 'DLC_KEY'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['DLC_KEY'] = tmp_1['DLC_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['HIERARCHY_TYPE'] = tmp_2['HIERARCHY_TYPE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['MASTER_DEPT_HIER_LEVEL_5_CODE'] = tmp_3['MASTER_DEPT_HIER_LEVEL_5_CODE'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['MASTER_DEPT_HIER_LEVEL_5_NAME'] = tmp_4['MASTER_DEPT_HIER_LEVEL_5_NAME'].astype(str)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['DLC_KEY', 'HIERARCHY_TYPE', 'DLC_NAME', 'MASTER_DEPT_HIER_LEVEL_1_CODE', 'MASTER_DEPT_HIER_LEVEL_1_NAME', 'MASTER_DEPT_HIER_LEVEL_2_CODE', 'MASTER_DEPT_HIER_LEVEL_2_NAME', 'MASTER_DEPT_HIER_LEVEL_3_CODE', 'MASTER_DEPT_HIER_LEVEL_3_NAME', 'MASTER_DEPT_HIER_LEVEL_4_CODE', 'MASTER_DEPT_HIER_LEVEL_4_NAME', 'MASTER_DEPT_HIER_LEVEL_5_CODE', 'MASTER_DEPT_HIER_LEVEL_5_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['MIT_ID'] = tmp_0['MIT_ID'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['HR_ORG_UNIT_TITLE'] = tmp_1['HR_ORG_UNIT_TITLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['DIRECTORY_ORG_UNIT_TITLE'] = tmp_2['DIRECTORY_ORG_UNIT_TITLE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['MIT_ID', 'EMERITUS_STATUS', 'HR_ORG_UNIT_TITLE', 'DIRECTORY_ORG_UNIT_TITLE']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
org_base = prepared_table_1.copy()
# Join org->DLC mapping in case table_1 DLC_KEY is incomplete in some rows
org_map = prepared_table_2.copy()
org_joined = org_base.merge(org_map, on='FCLT_ORGANIZATION_KEY', how='left', suffixes=('', '_MAP'))
# Prefer DLC_KEY from table_1 when present; otherwise use mapped value
org_joined['DLC_KEY_FINAL'] = org_joined['DLC_KEY']
org_joined.loc[org_joined['DLC_KEY_FINAL'].isna() & org_joined['DLC_KEY_MAP'].notna(), 'DLC_KEY_FINAL'] = org_joined['DLC_KEY_MAP']

# Join hierarchy by DLC_KEY
hier = prepared_table_3.copy()
integrated = org_joined.merge(hier, left_on='DLC_KEY_FINAL', right_on='DLC_KEY', how='left', suffixes=('', '_H'))

# Derive break group, formatted name by level, and org number
# Break group: use MAJOR hierarchy top-level name when available, else DLC_NAME from hierarchy, else organization name
integrated['BREAK_GROUP'] = integrated['MASTER_DEPT_HIER_LEVEL_1_NAME']
integrated.loc[integrated['BREAK_GROUP'].isna() | (integrated['BREAK_GROUP'].astype(str).str.strip()=='nan'), 'BREAK_GROUP'] = integrated['DLC_NAME_H']
integrated.loc[integrated['BREAK_GROUP'].isna(), 'BREAK_GROUP'] = integrated['ORG_NAME']

# Organization number from ORG_ID_STR (preferred) or fallback to ORG_CODE
integrated['ORGANIZATION_NUMBER'] = integrated['ORG_ID_STR']
integrated.loc[integrated['ORGANIZATION_NUMBER'].isna() | (integrated['ORGANIZATION_NUMBER'].astype(str).str.strip()=='nan'), 'ORGANIZATION_NUMBER'] = integrated['ORG_CODE']

# Formatted name according to level: simple example prefixing with level indicators from hierarchy where available
# Prefer the most specific available name from hierarchy levels, otherwise use org name
integrated['FORMATTED_NAME'] = integrated['ORG_NAME']
for lvl_name_col in ['MASTER_DEPT_HIER_LEVEL_5_NAME','MASTER_DEPT_HIER_LEVEL_4_NAME','MASTER_DEPT_HIER_LEVEL_3_NAME','MASTER_DEPT_HIER_LEVEL_2_NAME']:
    mask = integrated[lvl_name_col].notna() & (integrated[lvl_name_col].astype(str).str.strip()!='nan')
    integrated.loc[mask, 'FORMATTED_NAME'] = integrated.loc[mask, lvl_name_col]

# Emeritus vs non-emeritus: approximate by counting members per organization title match.
# Build a person-to-org title DataFrame and match loosely against ORG_NAME to estimate membership composition.
ppl = prepared_table_4.copy()
# Combine possible org-title columns
ppl['ORG_TITLE_COMBINED'] = ppl['HR_ORG_UNIT_TITLE']
mask_dir = ppl['ORG_TITLE_COMBINED'].isna() | (ppl['ORG_TITLE_COMBINED'].astype(str).str.strip()=='')
ppl.loc[mask_dir, 'ORG_TITLE_COMBINED'] = ppl.loc[mask_dir, 'DIRECTORY_ORG_UNIT_TITLE']
# Normalize emeritus flag
def emeritus_flag(s):
    s = ('' if s is None else str(s)).strip().lower()
    if s in ['emeritus','emerita','emeriti','emeritus status','emeritus/emerita']:
        return 'Emeritus'
    if s in ['non-emeritus','active','']:
        return 'Non-Emeritus'
    return 'Non-Emeritus'

ppl['EMERITUS_GROUP'] = ppl['EMERITUS_STATUS'].apply(emeritus_flag)

# Fuzzy-ish match: case-insensitive containment of org name in person's org title
ppl['ORG_TITLE_COMBINED_N'] = ppl['ORG_TITLE_COMBINED'].astype(str).str.strip().str.lower()
integrated['ORG_NAME_N'] = integrated['ORG_NAME'].astype(str).str.strip().str.lower()

# Expand match by cross-merge limited to rows where titles are not null, then filter by containment
left = integrated[['FCLT_ORGANIZATION_KEY','ORG_NAME','ORG_NAME_N']].drop_duplicates()
right = ppl[['MIT_ID','EMERITUS_GROUP','ORG_TITLE_COMBINED_N']].dropna(subset=['ORG_TITLE_COMBINED_N'])
# To avoid Cartesian explosion, prefilter right to only titles that could match any org name substring length > 2
right = right[right['ORG_TITLE_COMBINED_N'].str.len()>2]

# Perform a merge via temporary key to evaluate containment row-wise
left['_tmp'] = 1
right['_tmp'] = 1
lr = left.merge(right, on='_tmp', how='inner')
match_mask = lr.apply(lambda r: r['ORG_NAME_N'] in r['ORG_TITLE_COMBINED_N'] if isinstance(r['ORG_TITLE_COMBINED_N'], str) and isinstance(r['ORG_NAME_N'], str) else False, axis=1)
lr = lr[match_mask]

# Aggregate emeritus composition per organization
emer_counts = lr.groupby(['FCLT_ORGANIZATION_KEY','EMERITUS_GROUP'], as_index=False).size().rename(columns={'size':'member_count'})
# Pivot to labels per org (if any emeritus present label 'Emeritus', else 'Non-Emeritus'; if both, prefer both as 'Non-Emeritus' only when emeritus none)
emer_pivot = emer_counts.pivot(index='FCLT_ORGANIZATION_KEY', columns='EMERITUS_GROUP', values='member_count').fillna(0)
emer_pivot['MEMBERSHIP_STATUS'] = emer_pivot.apply(lambda r: 'Emeritus' if r.get('Emeritus',0)>0 and r.get('Non-Emeritus',0)==0 else ('Non-Emeritus' if r.get('Emeritus',0)==0 and (r.get('Non-Emeritus',0)>0) else ('Emeritus and Non-Emeritus' if r.get('Emeritus',0)>0 and r.get('Non-Emeritus',0)>0 else 'Non-Emeritus')), axis=1)
emer_pivot = emer_pivot[['MEMBERSHIP_STATUS']].reset_index()

integrated = integrated.merge(emer_pivot, on='FCLT_ORGANIZATION_KEY', how='left')
integrated['MEMBERSHIP_STATUS'] = integrated['MEMBERSHIP_STATUS'].fillna('Non-Emeritus')

# Employer count: count matched members per org from the same lr table; fall back to 0 if none matched
emp_counts = lr.groupby('FCLT_ORGANIZATION_KEY', as_index=False)['MIT_ID'].nunique().rename(columns={'MIT_ID':'EMPLOYER_COUNT'})
integrated = integrated.merge(emp_counts, on='FCLT_ORGANIZATION_KEY', how='left')
integrated['EMPLOYER_COUNT'] = integrated['EMPLOYER_COUNT'].fillna(0).astype(int)

# Exclude organizations '139' and '250' by organization number (ORG_ID_STR)
integrated = integrated[~integrated['ORGANIZATION_NUMBER'].astype(str).isin(['139','250'])]

# Prepare final columns
final_cols = {
    'BREAK_GROUP':'BREAK_GROUP',
    'ORGANIZATION_NUMBER':'ORGANIZATION_NUMBER',
    'ORG_CODE':'ORGANIZATION_ID',
    'ORG_NAME':'ORGANIZATION_NAME',
    'FORMATTED_NAME':'FORMATTED_NAME',
    'MEMBERSHIP_STATUS':'MEMBERS_EMERITUS_STATUS',
    'ORG_LEVEL':'LEVEL',
    'EMPLOYER_COUNT':'EMPLOYER_COUNT',
    'HIERARCHY_TYPE':'HIERARCHY_TYPE'
}
result = integrated[list(final_cols.keys())].rename(columns=final_cols)

# Sort by hierarchy type, then by organization name for stability
result = result.sort_values(['HIERARCHY_TYPE','ORGANIZATION_NAME','ORGANIZATION_ID'], kind='stable')

# Add total row per hierarchy type for employer counts
totals = result.groupby('HIERARCHY_TYPE', as_index=False)['EMPLOYER_COUNT'].sum()
totals['BREAK_GROUP'] = 'TOTAL'
totals['ORGANIZATION_NUMBER'] = ''
totals['ORGANIZATION_ID'] = ''
totals['ORGANIZATION_NAME'] = ''
totals['FORMATTED_NAME'] = ''
totals['MEMBERS_EMERITUS_STATUS'] = ''
totals['LEVEL'] = ''
# Arrange columns to match result
totals = totals[['BREAK_GROUP','ORGANIZATION_NUMBER','ORGANIZATION_ID','ORGANIZATION_NAME','FORMATTED_NAME','MEMBERS_EMERITUS_STATUS','LEVEL','EMPLOYER_COUNT','HIERARCHY_TYPE']]

# Append totals after per-type sections
target = pd.concat([result, totals], ignore_index=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
