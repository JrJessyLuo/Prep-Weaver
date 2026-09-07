import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeDatetime', 'params': {'column_name': 'event_date', 'date_format': '%Y-%m-%dT%H:%M:%S'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'event_id', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'event_name', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'type', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'notes', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'building', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'room', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'event_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'event_name', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'type', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'notes', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'status', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'building', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'room', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': []}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['event_id', 'event_name', 'building', 'room']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'budget_id', 'func': 'def transform(s):\n    s = str(s)\n    s = s.strip()\n    # collapse surrounding quotes only\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'amount', 'func': 'def transform(s):\n    s = str(s).strip()\n    # remove surrounding quotes to aid numeric cast\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'event_status', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'link_to_event', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'leading_spaces', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'remaining_category', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'spent', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'remaining', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': []}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['link_to_event', 'spent', 'remaining', 'amount']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['event_date'] = pd.to_datetime(tmp_0['event_date'], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S')
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['event_id'] = tmp_1['event_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['event_name'] = tmp_2['event_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['type'] = tmp_3['type'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['notes'] = tmp_4['notes'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['status'] = tmp_5['status'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_6['building'] = tmp_6['building'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_7['room'] = tmp_7['room'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['event_id'] = tmp_8['event_id'].astype(str)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['event_name'] = tmp_9['event_name'].astype(str)
    # Step 11: CastType
    tmp_10 = tmp_9.copy()
    tmp_10['type'] = tmp_10['type'].astype(str)
    # Step 12: CastType
    tmp_11 = tmp_10.copy()
    tmp_11['notes'] = tmp_11['notes'].astype(str)
    # Step 13: CastType
    tmp_12 = tmp_11.copy()
    tmp_12['status'] = tmp_12['status'].astype(str)
    # Step 14: CastType
    tmp_13 = tmp_12.copy()
    tmp_13['building'] = tmp_13['building'].astype(str)
    # Step 15: CastType
    tmp_14 = tmp_13.copy()
    tmp_14['room'] = tmp_14['room'].astype(str)
    # Step 16: Rename
    tmp_15 = tmp_14.rename(columns={})
    # Step 17: SelectCol
    result = tmp_15.loc[:, ['event_id', 'event_name', 'building', 'room']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    s = s.strip()\n    # collapse surrounding quotes only\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['budget_id'] = tmp_0['budget_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    # remove surrounding quotes to aid numeric cast\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['amount'] = tmp_1['amount'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['event_status'] = tmp_2['event_status'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['link_to_event'] = tmp_3['link_to_event'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['leading_spaces'] = tmp_4['leading_spaces'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['remaining_category'] = tmp_5['remaining_category'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['amount'] = pd.to_numeric(tmp_6['amount'], errors='coerce').astype(float)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['spent'] = pd.to_numeric(tmp_7['spent'], errors='coerce').astype(float)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['remaining'] = pd.to_numeric(tmp_8['remaining'], errors='coerce').astype(float)
    # Step 10: Rename
    tmp_9 = tmp_8.rename(columns={})
    # Step 11: SelectCol
    result = tmp_9.loc[:, ['link_to_event', 'spent', 'remaining', 'amount']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='left', left_on='link_to_event', right_on='event_id')
# Identify underspend where remaining > 0 (positive unspent budget)
mask = integrated['remaining'] > 0
result = integrated.loc[mask, ['event_name', 'building', 'room']].drop_duplicates()
# If no rows due to strict positive, relax to remaining >= 0 as fallback
if result.shape[0] == 0:
    result = integrated.loc[integrated['remaining'] >= 0, ['event_name', 'building', 'room']].drop_duplicates()
# Final projection: name and location
target = result.rename(columns={'event_name': 'name'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
