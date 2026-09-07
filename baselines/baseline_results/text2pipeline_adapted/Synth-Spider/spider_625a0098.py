import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['Headphone_ID', 'Model', 'Class', 'Driver-matched_dB', 'Price', 'Construction_Earpads']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Store_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Headphone_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Quantity', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    # remove surrounding single/double quotes and whitespace\n    s = s.strip().strip(\'"\').strip("\'")\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Quantity', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Store_ID', 'Headphone_ID', 'Quantity']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['Headphone_ID', 'Model', 'Class', 'Driver-matched_dB', 'Price', 'Construction_Earpads']].copy()
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
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    # remove surrounding single/double quotes and whitespace\n    s = s.strip().strip(\'"\').strip("\'")\n    return s', globals(), _ns_1)
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
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='Headphone_ID')
# Aggregate total stock per headphone across all stores
stock_by_model = integrated.groupby(['Headphone_ID', 'Model'], as_index=False)['Quantity'].sum(min_count=1)
# Models not in stock in any store: either no inventory rows (NaN) or total quantity == 0
mask_no_stock = stock_by_model['Quantity'].isna() | (stock_by_model['Quantity'] == 0)
result = stock_by_model.loc[mask_no_stock, ['Model']].drop_duplicates().sort_values('Model')
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
