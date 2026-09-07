import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'invoice_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'invoice_id', 'func': 'def transform(s):\n    s = str(s)\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['invoice_id', 'client_id'], 'value_vars': ['Finish', 'Starting', 'Working'], 'var_name': 'status_type', 'value_name': 'status_value'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status_type', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status_value', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'status_type', 'new_name': 'status_field'}, {'old_name': 'status_value', 'new_name': 'status'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['invoice_id', 'status']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'column', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'value', 'target_columns': ['invoice_part', 'method_part'], 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    if '-' in s:\n        left, right = s.split('-', 1)\n        return [left, right]\n    return [s, None]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'invoice_part', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    # Normalize to numeric then back to string to remove leading zeros/spaces\n    try:\n        if s == '':\n            return ''\n        n = int(float(s))\n        return str(n)\n    except Exception:\n        # If not numeric, return trimmed string\n        return s"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'invoice_part', 'new_name': 'invoice_id'}, {'old_name': 'method_part', 'new_name': 'payment_method'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['payment_id', 'invoice_id', 'payment_method']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['invoice_id'] = tmp_0['invoice_id'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['invoice_id'] = tmp_1['invoice_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Stack
    tmp_2 = tmp_1.melt(id_vars=['invoice_id', 'client_id'], value_vars=['Finish', 'Starting', 'Working'], var_name='status_type', value_name='status_value')
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['status_type'] = tmp_3['status_type'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['status_value'] = tmp_4['status_value'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'status_type': 'status_field', 'status_value': 'status'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['invoice_id', 'status']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['column'] = tmp_0['column'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    if '-' in s:\n        left, right = s.split('-', 1)\n        return [left, right]\n    return [s, None]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['value'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['invoice_part'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['method_part'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    # Normalize to numeric then back to string to remove leading zeros/spaces\n    try:\n        if s == '':\n            return ''\n        n = int(float(s))\n        return str(n)\n    except Exception:\n        # If not numeric, return trimmed string\n        return s", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['invoice_part'] = tmp_2['invoice_part'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'invoice_part': 'invoice_id', 'method_part': 'payment_method'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['payment_id', 'invoice_id', 'payment_method']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='left', on='invoice_id')
# Identify rows that actually represent invoice payments: prefer where payment_method is not null and prepared from a value like 'N-Card'. Keep robustness by also allowing when original column suggested invoice linkage; since we did not carry 'column', we infer from having a hyphen-derived payment_method.
integrated['has_method'] = integrated['payment_method'].notna() & (integrated['payment_method'].astype(str).str.len() > 0)
filtered = integrated[integrated['has_method']]
# We need all different invoice ids and statuses of the payments. Some invoices may have multiple status rows; keep distinct pairs per invoice across possibly multiple payments.
result = filtered[['invoice_id', 'status']].drop_duplicates()
# Final target
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
