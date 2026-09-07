import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER_TYPE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_ACTIVE', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MOIRA_MAILING_LIST', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MOIRA_GROUP', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_NFS_GROUP', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_PUBLIC', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_HIDDEN', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC', 'IS_HIDDEN']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'LAST_UPDATE_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'COUNTER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
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
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_3['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MOIRA_LIST_NAME'] = tmp_1['MOIRA_LIST_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['IS_ACTIVE'] = tmp_2['IS_ACTIVE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['IS_MOIRA_MAILING_LIST'] = tmp_3['IS_MOIRA_MAILING_LIST'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['IS_MOIRA_GROUP'] = tmp_4['IS_MOIRA_GROUP'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['IS_NFS_GROUP'] = tmp_5['IS_NFS_GROUP'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['IS_PUBLIC'] = tmp_6['IS_PUBLIC'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_7['IS_HIDDEN'] = tmp_7['IS_HIDDEN'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC', 'IS_HIDDEN']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
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
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['LAST_UPDATE_DATE'] = pd.to_datetime(tmp_3['LAST_UPDATE_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_4['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['COUNTER'] = pd.to_numeric(tmp_5['COUNTER'], errors='coerce').fillna(0).astype(int)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_3.merge(prepared_table_1, how='left', on='MOIRA_LIST_OWNER_KEY').merge(prepared_table_2, how='left', on='MOIRA_LIST_KEY')
# Derive member visibility label from IS_PUBLIC/IS_HIDDEN with relaxed handling
vis = integrated.copy()
vis_public = vis['IS_PUBLIC'].astype(str).str.upper().eq('Y')
vis_hidden = vis['IS_HIDDEN'].astype(str).str.upper().eq('Y')
vis['member_visibility'] = 'Hidden Members'
vis.loc[vis_public & ~vis_hidden, 'member_visibility'] = 'Public Members'
# Count members per list, owner, owner type, and visibility
by_list_vis = vis.groupby(['MOIRA_LIST_KEY','MOIRA_LIST_NAME','OWNER','OWNER_TYPE','member_visibility'], dropna=False).size().reset_index(name='member_count')
# Grand totals per owner and owner type (across all lists and both visibilities)
by_owner_total = vis.groupby(['OWNER','OWNER_TYPE'], dropna=False).size().reset_index(name='member_count')
by_owner_total['MOIRA_LIST_KEY'] = None
by_owner_total['MOIRA_LIST_NAME'] = None
by_owner_total['member_visibility'] = None
# Align columns and union
cols = ['MOIRA_LIST_KEY','MOIRA_LIST_NAME','OWNER','OWNER_TYPE','member_visibility','member_count']
by_list_vis = by_list_vis[cols]
by_owner_total = by_owner_total[cols]
result = __import__('pandas').concat([by_list_vis, by_owner_total], ignore_index=True)
# Final assignment
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
