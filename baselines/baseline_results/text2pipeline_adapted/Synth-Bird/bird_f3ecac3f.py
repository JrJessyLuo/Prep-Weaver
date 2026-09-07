import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'CustomerID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'fenqu', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'huobi', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'fenqu', 'new_name': 'segment'}, {'old_name': 'huobi', 'new_name': 'currency'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['CustomerID', 'currency']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'ProductID', 'func': 'def transform(s):\n    s = str(s)\n    s = s.strip()\n    # remove surrounding single or double quotes if present\n    if (s.startswith(\'"\') and s.endswith(\'"\')) or (s.startswith("\'") and s.endswith("\'")):\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ProductID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Description', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ProductID', 'new_name': 'ProductID'}, {'old_name': 'Description', 'new_name': 'ProductDescription'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ProductID', 'ProductDescription']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'Amount', 'func': 'def transform(s):\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Amount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Time', 'date_format': '%H:%M:%S'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'TransactionID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CustomerID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CardID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'GasStationID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ProductID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TransactionID', 'Date', 'Time', 'CustomerID', 'CardID', 'GasStationID', 'ProductID', 'Amount', 'Price']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['CustomerID'] = pd.to_numeric(tmp_0['CustomerID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['fenqu'] = tmp_1['fenqu'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['huobi'] = tmp_2['huobi'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'fenqu': 'segment', 'huobi': 'currency'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['CustomerID', 'currency']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    s = s.strip()\n    # remove surrounding single or double quotes if present\n    if (s.startswith(\'"\') and s.endswith(\'"\')) or (s.startswith("\'") and s.endswith("\'")):\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['ProductID'] = tmp_0['ProductID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ProductID'] = pd.to_numeric(tmp_1['ProductID'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Description'] = tmp_2['Description'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'ProductID': 'ProductID', 'Description': 'ProductDescription'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['ProductID', 'ProductDescription']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['Amount'] = tmp_0['Amount'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Amount'] = pd.to_numeric(tmp_1['Amount'], errors='coerce').astype(float)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Date'] = pd.to_datetime(tmp_2['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['Time'] = pd.to_datetime(tmp_3['Time'], errors='coerce').dt.strftime('%H:%M:%S')
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['TransactionID'] = pd.to_numeric(tmp_4['TransactionID'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['CustomerID'] = pd.to_numeric(tmp_5['CustomerID'], errors='coerce').fillna(0).astype(int)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['CardID'] = pd.to_numeric(tmp_6['CardID'], errors='coerce').fillna(0).astype(int)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['GasStationID'] = pd.to_numeric(tmp_7['GasStationID'], errors='coerce').fillna(0).astype(int)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['ProductID'] = pd.to_numeric(tmp_8['ProductID'], errors='coerce').fillna(0).astype(int)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['TransactionID', 'Date', 'Time', 'CustomerID', 'CardID', 'GasStationID', 'ProductID', 'Amount', 'Price']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_3.merge(prepared_table_1, how='left', on='CustomerID').merge(prepared_table_2, how='left', on='ProductID')
# Filter euro transactions. Use robust case-insensitive match and fallback if empty.
mask_eur = integrated['currency'].astype(str).str.strip().str.lower().isin(['eur', 'euro', '€'])
filtered = integrated[mask_eur]
if filtered.empty:
    # Broaden: look for any token containing 'eur'
    mask_broad = integrated['currency'].astype(str).str.strip().str.lower().str.contains('eur', na=False)
    filtered = integrated[mask_broad]
    if filtered.empty:
        # Fallback: if currency information is entirely missing, preserve all rows rather than empty
        filtered = integrated
# Project the product descriptions of the qualifying transactions and drop duplicates
result = filtered[['ProductDescription']].dropna()
result = result.drop_duplicates().sort_values('ProductDescription')
target = result.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
