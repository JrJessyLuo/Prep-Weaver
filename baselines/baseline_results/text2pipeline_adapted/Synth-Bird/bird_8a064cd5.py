import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'TransactionID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CustomerID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CardID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'GasStationID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ProductID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Time', 'func': 'def transform(s):\n    s = str(s).strip()\n    # Normalize to HH:MM:SS\n    parts = s.split(\':\')\n    if len(parts) == 2:\n        return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:00"\n    if len(parts) == 3:\n        return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:{parts[2].zfill(2)}"\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'je', 'func': 'def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'je', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'jg', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'je', 'new_name': 'Quantity'}, {'old_name': 'jg', 'new_name': 'Amount'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TransactionID', 'Date', 'Time', 'CustomerID', 'CardID', 'GasStationID', 'ProductID', 'Quantity', 'Amount']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'ProductID', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Code', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Popis', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Code', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Popis', 'new_name': 'ProductName'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Code', 'ProductName']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TransactionID'] = pd.to_numeric(tmp_0['TransactionID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['CustomerID'] = pd.to_numeric(tmp_1['CustomerID'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['CardID'] = pd.to_numeric(tmp_2['CardID'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['GasStationID'] = pd.to_numeric(tmp_3['GasStationID'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['ProductID'] = pd.to_numeric(tmp_4['ProductID'], errors='coerce').fillna(0).astype(int)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['Date'] = pd.to_datetime(tmp_5['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    # Normalize to HH:MM:SS\n    parts = s.split(\':\')\n    if len(parts) == 2:\n        return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:00"\n    if len(parts) == 3:\n        return f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:{parts[2].zfill(2)}"\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_6['Time'] = tmp_6['Time'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_7['je'] = tmp_7['je'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['je'] = pd.to_numeric(tmp_8['je'], errors='coerce').astype(float)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['jg'] = pd.to_numeric(tmp_9['jg'], errors='coerce').astype(float)
    # Step 11: Rename
    tmp_10 = tmp_9.rename(columns={'je': 'Quantity', 'jg': 'Amount'})
    # Step 12: SelectCol
    result = tmp_10.loc[:, ['TransactionID', 'Date', 'Time', 'CustomerID', 'CardID', 'GasStationID', 'ProductID', 'Quantity', 'Amount']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['ProductID'] = tmp_0['ProductID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['Code'] = tmp_1['Code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['Popis'] = tmp_2['Popis'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Code'] = pd.to_numeric(tmp_3['Code'], errors='coerce').fillna(0).astype(int)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'Popis': 'ProductName'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['Code', 'ProductName']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', left_on='ProductID', right_on='Code')
# Aggregate total sales by product using monetary Amount; if Amount has multiple currencies, assume single currency as data suggests.
sales = integrated.groupby(['ProductID', 'ProductName'], as_index=False)['Amount'].sum()
sales = sales.sort_values('Amount', ascending=False).head(5)
# Project the full product names of the top five best-selling products
target = sales[['ProductName']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
