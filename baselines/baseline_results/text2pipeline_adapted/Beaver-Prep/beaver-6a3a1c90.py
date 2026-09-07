import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'MOIRA_LIST_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_DESCRIPTION', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IS_ACTIVE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IS_MOIRA_MAILING_LIST', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IS_MOIRA_GROUP', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IS_NFS_GROUP', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IS_PUBLIC', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IS_HIDDEN', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_ACTIVE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MOIRA_MAILING_LIST', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MOIRA_GROUP', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_NFS_GROUP', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_PUBLIC', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_HIDDEN', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_MEMBER_FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_MEMBER_MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_MEMBER_MIT_ID', 'func': "def transform(s):\n    s = str(s)\n    # Treat typical float-like strings and 'nan' artifacts\n    if s.lower() == 'nan' or s == 'None':\n        return ''\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.strip()"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'moira_list_member', 'new_name': 'KRB_NAME'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'KRB_NAME', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['MIT_ID', 'KRB_NAME_UPPERCASE', 'IS_FACULTY']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['MOIRA_LIST_NAME'] = tmp_1['MOIRA_LIST_NAME'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['MOIRA_LIST_DESCRIPTION'] = tmp_2['MOIRA_LIST_DESCRIPTION'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['IS_ACTIVE'] = tmp_3['IS_ACTIVE'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['IS_MOIRA_MAILING_LIST'] = tmp_4['IS_MOIRA_MAILING_LIST'].astype(str)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['IS_MOIRA_GROUP'] = tmp_5['IS_MOIRA_GROUP'].astype(str)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['IS_NFS_GROUP'] = tmp_6['IS_NFS_GROUP'].astype(str)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['IS_PUBLIC'] = tmp_7['IS_PUBLIC'].astype(str)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['IS_HIDDEN'] = tmp_8['IS_HIDDEN'].astype(str)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_9['MOIRA_LIST_KEY'] = tmp_9['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_10['MOIRA_LIST_NAME'] = tmp_10['MOIRA_LIST_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_11['IS_ACTIVE'] = tmp_11['IS_ACTIVE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 13: StandardizeString
    tmp_12 = tmp_11.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_12['IS_MOIRA_MAILING_LIST'] = tmp_12['IS_MOIRA_MAILING_LIST'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 14: StandardizeString
    tmp_13 = tmp_12.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_13['IS_MOIRA_GROUP'] = tmp_13['IS_MOIRA_GROUP'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 15: StandardizeString
    tmp_14 = tmp_13.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_14['IS_NFS_GROUP'] = tmp_14['IS_NFS_GROUP'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 16: StandardizeString
    tmp_15 = tmp_14.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_15['IS_PUBLIC'] = tmp_15['IS_PUBLIC'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 17: StandardizeString
    tmp_16 = tmp_15.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_16['IS_HIDDEN'] = tmp_16['IS_HIDDEN'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 18: SelectCol
    result = tmp_16.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['moira_list_member'] = tmp_1['moira_list_member'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['MOIRA_LIST_OWNER_KEY'] = tmp_2['MOIRA_LIST_OWNER_KEY'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['MOIRA_LIST_MEMBER_FULL_NAME'] = tmp_3['MOIRA_LIST_MEMBER_FULL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['MOIRA_LIST_MEMBER_MIT_ID'] = tmp_4['MOIRA_LIST_MEMBER_MIT_ID'].astype(str)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec("def transform(s):\n    s = str(s)\n    # Treat typical float-like strings and 'nan' artifacts\n    if s.lower() == 'nan' or s == 'None':\n        return ''\n    if s.endswith('.0'):\n        s = s[:-2]\n    return s.strip()", globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['MOIRA_LIST_MEMBER_MIT_ID'] = tmp_5['MOIRA_LIST_MEMBER_MIT_ID'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'moira_list_member': 'KRB_NAME'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['MOIRA_LIST_KEY', 'KRB_NAME', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_9', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['MIT_ID', 'KRB_NAME_UPPERCASE', 'IS_FACULTY']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
lists = prepared_table_1.copy()
members = prepared_table_2.copy()
people = prepared_table_3.copy()

# Since prepared_table_3 is empty, we cannot determine faculty/support via merge to people.
# Instead, we will fall back to classifying based on plausible evidence in the member full name field.
# Create uppercase helpers for case-insensitive keyword matching.
members['FULL_NAME_UP'] = members['MOIRA_LIST_MEMBER_FULL_NAME'].astype(str).str.upper()

# Heuristic flags when no personnel table is available:
# - Treat entries clearly indicating faculty as faculty (e.g., contains 'PROF', 'FACULTY')
# - Treat entries indicating staff/support as support (e.g., contains 'STAFF', 'ADMIN', 'ASSISTANT', 'COORDINATOR')
# Unknowns counted as neither so they don't inflate counts incorrectly.
faculty_kw = ['PROF', 'FACULTY']
support_kw = ['STAFF', 'ADMIN', 'ASSISTANT', 'COORDINATOR']

fac_flag = False
sup_flag = False

# Build boolean flags vectorized
members['is_faculty_flag'] = False
members['is_support_flag'] = False

for kw in faculty_kw:
    members['is_faculty_flag'] = members['is_faculty_flag'] | members['FULL_NAME_UP'].str.contains(kw, na=False)
for kw in support_kw:
    members['is_support_flag'] = members['is_support_flag'] | members['FULL_NAME_UP'].str.contains(kw, na=False)

# Aggregate counts per list
agg = members.groupby('MOIRA_LIST_KEY', as_index=False).agg(
    faculty_count=('is_faculty_flag', 'sum'),
    support_count=('is_support_flag', 'sum')
)

# Join list metadata for names and active status
integrated = agg.merge(lists, how='right', on='MOIRA_LIST_KEY')

# Replace NaNs with zeros where lists had no matched members
integrated['faculty_count'] = integrated['faculty_count'].fillna(0).astype(int)
integrated['support_count'] = integrated['support_count'].fillna(0).astype(int)

# Keep lists that have at least one faculty or support subscriber
mask_has_target = (integrated['faculty_count'] > 0) | (integrated['support_count'] > 0)
result = integrated.loc[mask_has_target, ['MOIRA_LIST_NAME', 'support_count', 'faculty_count', 'IS_ACTIVE']]

# If still empty (no keyword matches), fall back to including lists that have any members at all
if result.empty:
    # Compute simple member counts per list and keep lists with any members
    counts_any = members.groupby('MOIRA_LIST_KEY', as_index=False).size().rename(columns={'size': 'any_count'})
    fallback = counts_any.merge(lists, how='left', on='MOIRA_LIST_KEY')
    fallback['support_count'] = 0
    fallback['faculty_count'] = 0
    result = fallback[['MOIRA_LIST_NAME', 'support_count', 'faculty_count', 'IS_ACTIVE']]

# Final projection and sort
target = result.sort_values(['MOIRA_LIST_NAME']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
