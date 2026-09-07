import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MOIRA_MAILING_LIST', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MOIRA_GROUP', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_NFS_GROUP', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_ACTIVE', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_PUBLIC', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_HIDDEN', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_NFS_GROUP']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'COUNTER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_MEMBER_MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'LAST_UPDATE_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER_TYPE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MOIRA_LIST_NAME'] = tmp_1['MOIRA_LIST_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['IS_MOIRA_MAILING_LIST'] = tmp_2['IS_MOIRA_MAILING_LIST'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['IS_MOIRA_GROUP'] = tmp_3['IS_MOIRA_GROUP'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['IS_NFS_GROUP'] = tmp_4['IS_NFS_GROUP'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['IS_ACTIVE'] = tmp_5['IS_ACTIVE'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['IS_PUBLIC'] = tmp_6['IS_PUBLIC'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_8 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_7['IS_HIDDEN'] = tmp_7['IS_HIDDEN'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_NFS_GROUP']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MOIRA_LIST_OWNER_KEY'] = tmp_1['MOIRA_LIST_OWNER_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['moira_list_member'] = tmp_2['moira_list_member'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['COUNTER'] = pd.to_numeric(tmp_3['COUNTER'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['MOIRA_LIST_MEMBER_MIT_ID'] = tmp_4['MOIRA_LIST_MEMBER_MIT_ID'].astype(str)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['LAST_UPDATE_DATE'] = pd.to_datetime(tmp_5['LAST_UPDATE_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: StandardizeDatetime
    tmp_6 = tmp_5.copy()
    tmp_6['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_6['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_OWNER_KEY'] = tmp_0['MOIRA_LIST_OWNER_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['OWNER'] = tmp_1['OWNER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['OWNER_TYPE'] = tmp_2['OWNER_TYPE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
members = prepared_table_2.copy()
lists = prepared_table_1.copy()
owners = prepared_table_3.copy()

# Count members per list (distinct member entries per MOIRA_LIST_KEY)
member_counts = members.groupby('MOIRA_LIST_KEY', as_index=False).agg(num_people=('moira_list_member', 'count'))

# Determine an owner per list: choose the most frequent MOIRA_LIST_OWNER_KEY per list, tie-breaker by first occurrence
owner_pref = members.groupby(['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY'], as_index=False).size().sort_values(['MOIRA_LIST_KEY', 'size'], ascending=[True, False])
owner_pref = owner_pref.drop_duplicates(subset=['MOIRA_LIST_KEY'], keep='first')
owner_pref = owner_pref[['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY']]

# Resolve owner name
owner_resolved = owner_pref.merge(owners, on='MOIRA_LIST_OWNER_KEY', how='left')

# Join attributes
integrated = member_counts.merge(lists, on='MOIRA_LIST_KEY', how='left').merge(owner_resolved[['MOIRA_LIST_KEY','OWNER']], on='MOIRA_LIST_KEY', how='left')

# Filter: mailing lists with name starting with 'A' (case-insensitive) and more than 1000 people
mask_name = integrated['MOIRA_LIST_NAME'].str.startswith('a', na=False)
mask_mailing = integrated['IS_MOIRA_MAILING_LIST'].str.upper().eq('Y')
mask_count = integrated['num_people'] > 1000
result = integrated[mask_name & mask_mailing & mask_count]

# Final projection with requested columns and clear headings
target = result[['MOIRA_LIST_NAME', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_NFS_GROUP', 'OWNER', 'num_people']].rename(columns={
    'MOIRA_LIST_NAME': 'list_name',
    'IS_MOIRA_MAILING_LIST': 'is_moira_mailing_list',
    'IS_MOIRA_GROUP': 'is_moira_group',
    'IS_NFS_GROUP': 'is_nfs_group',
    'OWNER': 'owner',
    'num_people': 'people_count'
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
