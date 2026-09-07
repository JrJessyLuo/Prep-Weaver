import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Concatenate', 'params': {'concatenate_columns': ['budget_id_prefix', 'budget_id_suffix'], 'target_column': 'budget_id', 'func': "def transform(row):\n    a = '' if row.get('budget_id_prefix') is None else str(row.get('budget_id_prefix'))\n    b = '' if row.get('budget_id_suffix') is None else str(row.get('budget_id_suffix'))\n    return a + b"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'value', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'category', 'func': 'def transform(s):\n    if s is None:\n        return None\n    # trim but preserve original case\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'event_status', 'func': 'def transform(s):\n    if s is None:\n        return None\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'link_to_event', 'func': 'def transform(s):\n    if s is None:\n        return None\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'metric', 'func': 'def transform(s):\n    if s is None:\n        return None\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'link_to_event', 'new_name': 'event_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['budget_id', 'category', 'event_status', 'metric', 'value', 'event_id']}, 'table_indices': [0]}], [{'op': 'StandardizeDatetime', 'params': {'column_name': 'expense_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'items', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['expense_id', 'expense_date', 'cost', 'approved', 'link_to_member', 'link_to_budget', 'items']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Concatenate
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(row):\n    a = '' if row.get('budget_id_prefix') is None else str(row.get('budget_id_prefix'))\n    b = '' if row.get('budget_id_suffix') is None else str(row.get('budget_id_suffix'))\n    return a + b", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_0['budget_id'] = tmp_0[['budget_id_prefix', 'budget_id_suffix']].apply(_concat_func_1, axis=1)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['value'] = pd.to_numeric(tmp_1['value'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    # trim but preserve original case\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['category'] = tmp_2['category'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['event_status'] = tmp_3['event_status'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['link_to_event'] = tmp_4['link_to_event'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['metric'] = tmp_5['metric'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'link_to_event': 'event_id'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['budget_id', 'category', 'event_status', 'metric', 'value', 'event_id']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['expense_date'] = pd.to_datetime(tmp_0['expense_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['items'] = tmp_1['items'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['expense_id', 'expense_date', 'cost', 'approved', 'link_to_member', 'link_to_budget', 'items']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='left', left_on='link_to_budget', right_on='budget_id')
# Identify pizza-related expenses between $50 and $100 (exclusive of 100 per question: more than 50 and less than 100)
mask_pizza = integrated['items'].astype(str).str.contains('pizza', case=False, na=False)
mask_amount = (integrated['cost'] > 50) & (integrated['cost'] < 100)
# If there is an event name/date elsewhere, we only have event_id and expense_date here. Treat expense_date as the event date proxy.
result = integrated.loc[mask_pizza & mask_amount, ['event_id', 'expense_date', 'cost', 'items']]
# Rename columns to match requested output semantics: event name (if event_id is the only identifier, present it as the event key) and date
result = result.rename(columns={'event_id': 'event_name_or_id', 'expense_date': 'event_date'})
# Sort by date for readability
result = result.sort_values(['event_date', 'event_name_or_id']).reset_index(drop=True)
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
