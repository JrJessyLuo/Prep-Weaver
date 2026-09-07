import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Store_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Store_ID', 'Name', 'shequ', 'tingche', 'kaiye']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Store_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Headphone_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Quantity', 'func': 'def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Quantity', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Store_ID', 'Headphone_ID', 'Quantity']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Store_ID'] = pd.to_numeric(tmp_0['Store_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['Store_ID', 'Name', 'shequ', 'tingche', 'kaiye']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Store_ID'] = pd.to_numeric(tmp_0['Store_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Headphone_ID'] = pd.to_numeric(tmp_1['Headphone_ID'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['Quantity'] = tmp_2['Quantity'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Quantity'] = pd.to_numeric(tmp_3['Quantity'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['Store_ID', 'Headphone_ID', 'Quantity']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
stock = prepared_table_2.copy()
# After preparation, Quantity is numeric. Aggregate per store to total headphone units.
stock_per_store = stock.groupby('Store_ID', as_index=False)['Quantity'].sum()
# Left join all stores to stock totals
stores_with_stock = prepared_table_1.merge(stock_per_store, on='Store_ID', how='left')
# Stores without any headphones are those with no matching stock rows or summed Quantity <= 0
no_headphones = stores_with_stock[(stores_with_stock['Quantity'].isna()) | (stores_with_stock['Quantity'] <= 0)]
# Project store names
target = no_headphones[['Name']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
