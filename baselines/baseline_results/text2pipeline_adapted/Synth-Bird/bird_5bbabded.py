import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'lx', 'new_name': 'event_type'}]}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'event_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'event_id', 'func': 'def transform(s):\n    # Trim whitespace; keep original casing/content\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'event_name', 'func': 'def transform(s):\n    # Trim whitespace; keep human-readable casing\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'event_type', 'func': 'def transform(s):\n    # Trim whitespace; do not lower-case to preserve readability\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status', 'func': 'def transform(s):\n    # Trim whitespace; keep casing\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'wz', 'func': 'def transform(s):\n    # Trim whitespace; keep casing\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['event_id', 'event_name', 'event_date', 'event_type', 'status']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'link_to_event', 'new_name': 'event_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'spent', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'remaining', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'budget_id', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'event_id', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['budget_id', 'category', 'spent', 'remaining', 'amount', 'event_status', 'event_id']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'expense_date', 'dtype': 'datetime64'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'cost', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'expense_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'approved', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'link_to_member', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'link_to_budget', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'link_to_budget', 'new_name': 'budget_id'}, {'old_name': 'link_to_member', 'new_name': 'member_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['expense_id', 'expense_description', 'expense_date', 'cost', 'approved', 'member_id', 'budget_id']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'member_id', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'email', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'position', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 't_shirt_size', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'phone', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'zip', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'first_name', 'last_name', 'email', 'position', 't_shirt_size', 'phone', 'zip', 'link_to_major']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'lx': 'event_type'})
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['event_date'] = pd.to_datetime(tmp_1['event_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim whitespace; keep original casing/content\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['event_id'] = tmp_2['event_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Trim whitespace; keep human-readable casing\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['event_name'] = tmp_3['event_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    # Trim whitespace; do not lower-case to preserve readability\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['event_type'] = tmp_4['event_type'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    # Trim whitespace; keep casing\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['status'] = tmp_5['status'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_5 = {}
    exec('def transform(s):\n    # Trim whitespace; keep casing\n    return None if s is None or (isinstance(s, float) and np.isnan(s)) else str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_6['wz'] = tmp_6['wz'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['event_id', 'event_name', 'event_date', 'event_type', 'status']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'link_to_event': 'event_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['spent'] = pd.to_numeric(tmp_1['spent'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['remaining'] = pd.to_numeric(tmp_2['remaining'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['amount'] = pd.to_numeric(tmp_3['amount'], errors='coerce').fillna(0).astype(int)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['budget_id'] = tmp_4['budget_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['event_id'] = tmp_5['event_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['budget_id', 'category', 'spent', 'remaining', 'amount', 'event_status', 'event_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['expense_date'] = pd.to_datetime(tmp_0['expense_date'], errors='coerce')
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['cost'] = pd.to_numeric(tmp_1['cost'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['expense_id'] = tmp_2['expense_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['approved'] = tmp_3['approved'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['link_to_member'] = tmp_4['link_to_member'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['link_to_budget'] = tmp_5['link_to_budget'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'link_to_budget': 'budget_id', 'link_to_member': 'member_id'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['expense_id', 'expense_description', 'expense_date', 'cost', 'approved', 'member_id', 'budget_id']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['member_id'] = tmp_0['member_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['first_name'] = tmp_1['first_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['last_name'] = tmp_2['last_name'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['email'] = tmp_3['email'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['position'] = tmp_4['position'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['t_shirt_size'] = tmp_5['t_shirt_size'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['phone'] = tmp_6['phone'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['zip'] = tmp_7['zip'].astype(str)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['member_id', 'first_name', 'last_name', 'email', 'position', 't_shirt_size', 'phone', 'zip', 'link_to_major']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
events = prepared_table_1.copy()
# Integrate budgets to ensure we have an event-level bridge if needed later; keep all events
ev_budget = events.merge(prepared_table_2[['event_id', 'budget_id']], on='event_id', how='left')
# Derive attendance per event: use expenses as member-linked evidence of attendance. One expense represents participation by the submitting member for that event via its budget.
# Join expenses to budget to map each expense to its event, then to members (optional for deduping by member).
exp_with_event = prepared_table_3.merge(prepared_table_2[['budget_id', 'event_id']], on='budget_id', how='left')
# If some expenses lack an event_id due to missing budget linkage, they won't contribute. Proceed with available links.
# Compute number of distinct members per event from expenses as attendance proxy.
att_per_event = exp_with_event.dropna(subset=['event_id', 'member_id']).groupby('event_id', as_index=False)['member_id'].nunique().rename(columns={'member_id':'member_count'})
# Attach attendance to events and filter by >10
ev_att = events.merge(att_per_event, on='event_id', how='left')
ev_att['member_count'] = ev_att['member_count'].fillna(0).astype(int)
eligible = ev_att[ev_att['member_count'] > 10]
# Count how many of these eligible events are meetings. Use case-insensitive check over event_type and fallback to event_name contains 'meeting'.
etype = eligible['event_type'].fillna('')
ename = eligible['event_name'].fillna('')
mask_meeting = etype.str.strip().str.lower().eq('meeting') | ename.str.contains('meeting', case=False, na=False)
result = eligible[mask_meeting]
# Final answer: single-row DataFrame with the count
target = result.assign(meeting_event_count=1)['meeting_event_count'].to_frame()
target = target.agg({'meeting_event_count':'sum'}).to_frame().T.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
