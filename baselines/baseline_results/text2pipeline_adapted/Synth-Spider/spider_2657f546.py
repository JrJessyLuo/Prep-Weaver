import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'CustomerId', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ReceiptNumber', 'func': 'def transform(s):\n    s = str(s)\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        return s[1:-1]\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%d-%b-%Y'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ReceiptNumber', 'Date', 'CustomerId']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'Id', 'func': 'def transform(s):\n    s = str(s)\n    # remove surrounding single or double quotes if present\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'xing', 'new_name': 'LastName'}, {'old_name': 'ming', 'new_name': 'FirstName'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FirstName', 'func': 'def transform(s):\n    # Trim whitespace but preserve original capitalization\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LastName', 'func': 'def transform(s):\n    # Trim whitespace but preserve original capitalization\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Id', 'FirstName', 'LastName']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['CustomerId'] = tmp_0['CustomerId'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        return s[1:-1]\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['ReceiptNumber'] = tmp_1['ReceiptNumber'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Date'] = pd.to_datetime(tmp_2['Date'], errors='coerce').dt.strftime('%d-%b-%Y')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ReceiptNumber', 'Date', 'CustomerId']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    # remove surrounding single or double quotes if present\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['Id'] = tmp_0['Id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'xing': 'LastName', 'ming': 'FirstName'})
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Trim whitespace but preserve original capitalization\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['FirstName'] = tmp_2['FirstName'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    # Trim whitespace but preserve original capitalization\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['LastName'] = tmp_3['LastName'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['Id', 'FirstName', 'LastName']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', left_on='CustomerId', right_on='Id')
# Identify earliest visit date
min_date = integrated['Date'].min()
result = integrated[integrated['Date'] == min_date]
# Project first and last names
target = result[['FirstName', 'LastName']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
