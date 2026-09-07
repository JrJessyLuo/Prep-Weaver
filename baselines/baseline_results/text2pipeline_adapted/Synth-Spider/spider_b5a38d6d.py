import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'IdClient', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'details', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'IdClient', 'columns': 'attribute', 'values': 'details', 'aggfunc': 'max'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Name', 'new_name': 'ClientName'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IdClient', 'ClientName']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'IdClient', 'func': 'def transform(s):\n    s = str(s)\n    s = s.strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IdClient', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IdOrder', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IdOrder', 'IdClient']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IdOrder_num', 'func': 'def transform(s):\n    s = str(s).strip()\n    # preserve as 7-character string if already provided; otherwise left-pad to 7\n    return s if len(s) == 7 else s.zfill(7)'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IdOrder_suffix', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['IdOrder_num', 'IdOrder_suffix'], 'target_column': 'IdOrder', 'func': "def transform(row):\n    return str(row['IdOrder_num']) + str(row['IdOrder_suffix'])"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IdOrder', 'amount']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['IdClient'] = tmp_0['IdClient'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['attribute'] = tmp_1['attribute'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['details'] = tmp_2['details'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Pivot
    tmp_3 = pd.pivot_table(tmp_2, index='IdClient', columns='attribute', values='details', aggfunc='max').reset_index()
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'Name': 'ClientName'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['IdClient', 'ClientName']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    s = s.strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IdClient'] = tmp_0['IdClient'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['IdClient'] = tmp_1['IdClient'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['IdOrder'] = tmp_2['IdOrder'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['IdOrder', 'IdClient']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['amount'] = pd.to_numeric(tmp_0['amount'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    # preserve as 7-character string if already provided; otherwise left-pad to 7\n    return s if len(s) == 7 else s.zfill(7)', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['IdOrder_num'] = tmp_1['IdOrder_num'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['IdOrder_suffix'] = tmp_2['IdOrder_suffix'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Concatenate
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(row):\n    return str(row['IdOrder_num']) + str(row['IdOrder_suffix'])", globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_3['IdOrder'] = tmp_3[['IdOrder_num', 'IdOrder_suffix']].apply(_concat_func_3, axis=1)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['IdOrder', 'amount']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
orders_clients = prepared_table_2.merge(prepared_table_1, how='left', on='IdClient')
orders_lines = orders_clients.merge(prepared_table_3, how='left', on='IdOrder')
agg = orders_lines.groupby(['IdClient','ClientName'], dropna=False, as_index=False)['amount'].sum(min_count=1)
agg['amount'] = agg['amount'].fillna(0).astype(int)
target = agg[['ClientName','amount']].rename(columns={'amount':'total_books_ordered'}).sort_values(['ClientName'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
