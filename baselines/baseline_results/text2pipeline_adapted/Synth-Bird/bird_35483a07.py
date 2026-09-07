import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'district_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'frequency', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    s = s.upper()\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'year', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    return s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'month', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    if s.isdigit():\n        return str(int(s)).zfill(2)\n    return s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'day', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    if s.isdigit():\n        return str(int(s)).zfill(2)\n    return s"}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['year', 'month', 'day'], 'target_column': 'acct_date', 'func': 'def transform(row):\n    y = \'\' if row.get(\'year\') is None else str(row.get(\'year\'))\n    m = \'\' if row.get(\'month\') is None else str(row.get(\'month\'))\n    d = \'\' if row.get(\'day\') is None else str(row.get(\'day\'))\n    return f"{y}-{m}-{d}" if y and m and d else \'\''}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'acct_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'frequency', 'new_name': 'statement_frequency'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['account_id', 'statement_frequency', 'acct_date']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'loan_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'date', 'target_columns': ['loan_date'], 'func': 'def transform(s):\n    import pandas as pd\n    try:\n        return [pd.to_datetime(s)]\n    except Exception:\n        return [pd.NaT]'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'metric', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': ['loan_id', 'account_id', 'loan_date', 'status'], 'columns': 'metric', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'duration', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'payments', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['loan_id', 'account_id', 'loan_date', 'status', 'amount', 'duration', 'payments']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['account_id'] = pd.to_numeric(tmp_0['account_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['district_id'] = pd.to_numeric(tmp_1['district_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    s = s.upper()\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['frequency'] = tmp_2['frequency'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    return s", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['year'] = tmp_3['year'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    if s.isdigit():\n        return str(int(s)).zfill(2)\n    return s", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['month'] = tmp_4['month'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    if s.isdigit():\n        return str(int(s)).zfill(2)\n    return s", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['day'] = tmp_5['day'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: Concatenate
    tmp_6 = tmp_5.copy()
    _ns_5 = {}
    exec('def transform(row):\n    y = \'\' if row.get(\'year\') is None else str(row.get(\'year\'))\n    m = \'\' if row.get(\'month\') is None else str(row.get(\'month\'))\n    d = \'\' if row.get(\'day\') is None else str(row.get(\'day\'))\n    return f"{y}-{m}-{d}" if y and m and d else \'\'', globals(), _ns_5)
    _concat_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('concat')
    tmp_6['acct_date'] = tmp_6[['year', 'month', 'day']].apply(_concat_func_5, axis=1)
    # Step 8: StandardizeDatetime
    tmp_7 = tmp_6.copy()
    tmp_7['acct_date'] = pd.to_datetime(tmp_7['acct_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 9: Rename
    tmp_8 = tmp_7.rename(columns={'frequency': 'statement_frequency'})
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['account_id', 'statement_frequency', 'acct_date']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['loan_id'] = pd.to_numeric(tmp_0['loan_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['account_id'] = pd.to_numeric(tmp_1['account_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import pandas as pd\n    try:\n        return [pd.to_datetime(s)]\n    except Exception:\n        return [pd.NaT]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_2['date'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['loan_date'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['status'] = tmp_3['status'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['metric'] = tmp_4['metric'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: Pivot
    tmp_5 = pd.pivot_table(tmp_4, index=['loan_id', 'account_id', 'loan_date', 'status'], columns='metric', values='value', aggfunc='first').reset_index()
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['amount'] = pd.to_numeric(tmp_6['amount'], errors='coerce').astype(float)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['duration'] = pd.to_numeric(tmp_7['duration'], errors='coerce').astype(float)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['payments'] = pd.to_numeric(tmp_8['payments'], errors='coerce').astype(float)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['loan_id', 'account_id', 'loan_date', 'status', 'amount', 'duration', 'payments']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='account_id', how='inner')
# Filter for approved loans (status 'A'), monthly statements, date window, and amount threshold
# Monthly statement values are expected as 'POPLATEK MESICNE' (Czech). Use case-insensitive contains for robustness.
mask_status = integrated['status'].astype(str).str.upper().eq('A')
mask_freq = integrated['statement_frequency'].astype(str).str.upper().str.contains('MESIC', na=False)
start_date = pd.to_datetime('1995-01-01')
end_date = pd.to_datetime('1997-12-31')
mask_date = (integrated['loan_date'] >= start_date) & (integrated['loan_date'] <= end_date)
mask_amount = integrated['amount'] >= 250000
filtered = integrated[mask_status & mask_freq & mask_date & mask_amount]
# Count loans per account ("per account" interpreted as counting loans that meet criteria for accounts with monthly statements)
result = filtered.groupby('account_id', as_index=False).agg(loans_approved=('loan_id', 'nunique'))
# If no rows (overly strict frequency), relax to exact equality fallback to preserve intent
if result.empty and not integrated.empty:
    mask_freq_relax = integrated['statement_frequency'].astype(str).str.upper().eq('POPLATEK MESICNE')
    filtered2 = integrated[mask_status & mask_freq_relax & mask_date & mask_amount]
    result = filtered2.groupby('account_id', as_index=False).agg(loans_approved=('loan_id', 'nunique'))
# Return counts per account; if still empty, return accounts with zero is not allowed per instructions, so return an empty frame with expected columns
target = result.sort_values(['account_id'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
