import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TERM_CODE', 'new_name': 'term_code'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'term_code', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_SESSION_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'term_code']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'iap_subject_session_key', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'SESSION_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['iap_subject_session_key', 'SESSION_DATE', 'HAS_SESSION_INFO']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'term_code', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_CURRENT_TERM', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'IS_CURRENT_TERM', 'target_columns': ['CURRENT_STATUS', '_drop_helper'], 'func': "def transform(s):\n    val = str(s)\n    status = 'CURRENT' if val == 'Y' else 'NOT CURRENT'\n    return [status, None]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['_drop_helper']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['term_code', 'CURRENT_STATUS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'TERM_CODE': 'term_code'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['term_code'] = tmp_1['term_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['IAP_SUBJECT_SESSION_KEY'] = tmp_2['IAP_SUBJECT_SESSION_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'term_code']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['iap_subject_session_key'] = tmp_0['iap_subject_session_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['SESSION_DATE'] = pd.to_datetime(tmp_1['SESSION_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['iap_subject_session_key', 'SESSION_DATE', 'HAS_SESSION_INFO']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['term_code'] = tmp_0['term_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['IS_CURRENT_TERM'] = tmp_1['IS_CURRENT_TERM'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    val = str(s)\n    status = 'CURRENT' if val == 'Y' else 'NOT CURRENT'\n    return [status, None]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_2['IS_CURRENT_TERM'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['CURRENT_STATUS'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['_drop_helper'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['_drop_helper'], errors='ignore').copy()
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['term_code', 'CURRENT_STATUS']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_10', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_3, on='term_code', how='left')
# Join session instances
integrated = integrated.merge(prepared_table_2, left_on='IAP_SUBJECT_SESSION_KEY', right_on='iap_subject_session_key', how='left')
# Derive a countable flag for session rows (count all rows in table_2 linked to a session; if no rows, count as 0)
integrated['session_row'] = 1
# For IAP session time in days, we don't have explicit durations; interpret each distinct SESSION_DATE per session as 1 day
# Convert SESSION_DATE to datetime for distinct-day counting; non-parsable remains NaT and will be excluded from day counts
try:
    integrated['SESSION_DATE_PARSED'] = pd.to_datetime(integrated['SESSION_DATE'], errors='coerce', dayfirst=False, format='%d-%b-%y')
except Exception:
    integrated['SESSION_DATE_PARSED'] = pd.to_datetime(integrated['SESSION_DATE'], errors='coerce')
# Aggregate per CURRENT_STATUS and session (name + key)
per_session = (
    integrated.groupby(['CURRENT_STATUS', 'ACTIVITY_TITLE', 'IAP_SUBJECT_SESSION_KEY'], dropna=False)
    .agg(
        IAP_SESSIONS_COUNT=('session_row', 'sum'),
        TOTAL_DAYS=('SESSION_DATE_PARSED', lambda s: s.dropna().nunique())
    )
    .reset_index()
)
# If a session has no linked rows in table_2, IAP_SESSIONS_COUNT will be NaN (since sum on all-NaN becomes 0?), ensure zeros
per_session['IAP_SESSIONS_COUNT'] = per_session['IAP_SESSIONS_COUNT'].fillna(0).astype(int)
per_session['TOTAL_DAYS'] = per_session['TOTAL_DAYS'].fillna(0).astype(int)
# Average IAP session time in days per session is TOTAL_DAYS / IAP_SESSIONS_COUNT where count>0; else 0
per_session['AVG_DAYS'] = per_session.apply(lambda r: (r['TOTAL_DAYS'] / r['IAP_SESSIONS_COUNT']) if r['IAP_SESSIONS_COUNT']>0 else 0.0, axis=1)
# Subtotals per CURRENT_STATUS
subtotals = (
    per_session.groupby(['CURRENT_STATUS'], as_index=False)
    .agg(
        IAP_SESSIONS_COUNT=('IAP_SESSIONS_COUNT', 'sum'),
        TOTAL_DAYS=('TOTAL_DAYS', 'sum')
    )
)
subtotals['AVG_DAYS'] = subtotals.apply(lambda r: (r['TOTAL_DAYS'] / r['IAP_SESSIONS_COUNT']) if r['IAP_SESSIONS_COUNT']>0 else 0.0, axis=1)
subtotals['ACTIVITY_TITLE'] = 'Subtotal'
# For ordering by cluster type, treat CURRENT before NOT CURRENT; add sort key
order_map = {'CURRENT': 0, 'NOT CURRENT': 1}
per_session['CURRENT_ORDER'] = per_session['CURRENT_STATUS'].map(order_map).fillna(2).astype(int)
subtotals['CURRENT_ORDER'] = subtotals['CURRENT_STATUS'].map(order_map).fillna(2).astype(int)
# Assemble detailed + subtotals per CURRENT_STATUS
detailed_and_sub = pd.concat([
    per_session[['CURRENT_STATUS','ACTIVITY_TITLE','IAP_SESSIONS_COUNT','TOTAL_DAYS','AVG_DAYS','CURRENT_ORDER']],
    subtotals[['CURRENT_STATUS','ACTIVITY_TITLE','IAP_SESSIONS_COUNT','TOTAL_DAYS','AVG_DAYS','CURRENT_ORDER']]
], ignore_index=True)
# Grand total across all statuses
grand = pd.DataFrame({
    'CURRENT_STATUS': ['Grand Total'],
    'ACTIVITY_TITLE': ['Grand Total'],
    'IAP_SESSIONS_COUNT': [per_session['IAP_SESSIONS_COUNT'].sum()],
    'TOTAL_DAYS': [per_session['TOTAL_DAYS'].sum()],
    'AVG_DAYS': [ (per_session['TOTAL_DAYS'].sum() / per_session['IAP_SESSIONS_COUNT'].sum()) if per_session['IAP_SESSIONS_COUNT'].sum()>0 else 0.0 ],
    'CURRENT_ORDER': [3]
})
# Sort by current status cluster
detailed_and_sub = detailed_and_sub.sort_values(by=['CURRENT_ORDER','ACTIVITY_TITLE'], kind='mergesort')
# Append grand total at end
result = pd.concat([detailed_and_sub, grand], ignore_index=True)
# Display CURRENT_STATUS only when it differs from previous; create a display column
result = result.reset_index(drop=True)
cs = result['CURRENT_STATUS'].tolist()
show = []
prev = None
for v in cs:
    if v != prev:
        show.append(v)
        prev = v
    else:
        show.append('')
result['CURRENT_STATUS_DISPLAY'] = show
# Final projection and ordering of columns
target = result[['CURRENT_STATUS_DISPLAY','ACTIVITY_TITLE','IAP_SESSIONS_COUNT','TOTAL_DAYS','AVG_DAYS']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
