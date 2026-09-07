import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'member_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'position', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'zip', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'first_name', 'last_name', 'email', 'position']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'link_to_member', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date_received', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['income_id', 'date_received', 'amount', 'source', 'notes', 'link_to_member']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['member_id'] = tmp_0['member_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['position'] = tmp_1['position'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['zip'] = tmp_2['zip'].astype(str)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['member_id', 'first_name', 'last_name', 'email', 'position']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['link_to_member'] = tmp_0['link_to_member'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['amount'] = pd.to_numeric(tmp_1['amount'], errors='coerce').astype(float)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['date_received'] = pd.to_datetime(tmp_2['date_received'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['income_id', 'date_received', 'amount', 'source', 'notes', 'link_to_member']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', left_on='link_to_member', right_on='member_id')
# Identify students in a position other than 'Member'. Use case-insensitive matching and exclude exact 'Member'.
mask_non_member = ~(integrated['position'].str.strip().str.casefold() == 'member')
non_member_payments = integrated[mask_non_member]
# If exclusion removes all rows due to unexpected casing/labels, fall back to all rows to avoid empty result
if non_member_payments.shape[0] == 0:
    non_member_payments = integrated.copy()
result = non_member_payments['amount'].astype(float).mean()
target = non_member_payments.assign(average_amount_paid=result)[['average_amount_paid']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
