import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ISBN', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Title', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ISBN', 'Title', 'Author', 'PurchasePrice', 'SalePrice']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'ISBN_amount', 'target_columns': ['ISBN', 'Amount'], 'func': "def transform(s):\n    try:\n        left, right = str(s).split('-', 1)\n    except Exception:\n        left, right = str(s), None\n    return [left, right]"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IdOrder', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ISBN', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Amount', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IdOrder', 'ISBN', 'Amount']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': []}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IdOrder', 'func': 'def transform(s):\n    return str(s)'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IdClient', 'func': 'def transform(s):\n    return str(s)'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DateOrder', 'func': 'def transform(s):\n    return "" if s is None or str(s).lower()=="none" else str(s)'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DateExped', 'func': 'def transform(s):\n    return "" if s is None or str(s).lower()=="none" else str(s)'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IdOrder', 'IdClient', 'DateOrder', 'DateExped']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ISBN'] = tmp_0['ISBN'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Title'] = tmp_1['Title'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['ISBN', 'Title', 'Author', 'PurchasePrice', 'SalePrice']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    try:\n        left, right = str(s).split('-', 1)\n    except Exception:\n        left, right = str(s), None\n    return [left, right]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['ISBN_amount'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['ISBN'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['Amount'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['IdOrder'] = tmp_1['IdOrder'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['ISBN'] = tmp_2['ISBN'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Amount'] = pd.to_numeric(tmp_3['Amount'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['IdOrder', 'ISBN', 'Amount']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s)', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['IdOrder'] = tmp_1['IdOrder'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s)', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['IdClient'] = tmp_2['IdClient'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return "" if s is None or str(s).lower()=="none" else str(s)', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['DateOrder'] = tmp_3['DateOrder'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return "" if s is None or str(s).lower()=="none" else str(s)', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['DateExped'] = tmp_4['DateExped'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['IdOrder', 'IdClient', 'DateOrder', 'DateExped']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', on='ISBN')
# Filter for the target title using case-insensitive robust match over Title
mask = integrated['Title'].str.strip().str.lower() == 'pride and prejudice'
filtered = integrated[mask]
# If no rows due to minor title variations, relax to contains match
if filtered.empty:
    mask2 = integrated['Title'].str.strip().str.lower().str.contains('pride') & integrated['Title'].str.strip().str.lower().str.contains('prejudice')
    filtered = integrated[mask2]
# Count distinct orders that include the book (any quantity counts as one order)
result = filtered[['IdOrder']].drop_duplicates()
result['NumberOfOrders'] = 1
agg = result.agg({'NumberOfOrders':'sum'}).to_frame().T
agg['Title'] = 'Pride and Prejudice'
# Reorder columns
target = agg[['Title','NumberOfOrders']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
