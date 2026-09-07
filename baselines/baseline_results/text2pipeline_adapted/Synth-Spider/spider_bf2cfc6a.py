import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'customer_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'customer_number', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'customer_name', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['customer_id', 'customer_name', 'customer_number']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': ['order_id'], 'value_vars': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'var_name': 'order_col', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'order_col', 'columns': 'order_id', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'order_col', 'new_name': 'order_id'}, {'old_name': 'date_part', 'new_name': 'order_date'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'customer_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'order_status_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'order_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['order_id', 'customer_id', 'order_status_code', 'order_date']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['customer_id'] = pd.to_numeric(tmp_0['customer_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['customer_number'] = pd.to_numeric(tmp_1['customer_number'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['customer_name'] = tmp_2['customer_name'].astype(str)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['customer_id', 'customer_name', 'customer_number']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['order_id'], value_vars=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], var_name='order_col', value_name='value')
    # Step 2: Pivot
    tmp_1 = pd.pivot_table(tmp_0, index='order_col', columns='order_id', values='value', aggfunc='first').reset_index()
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'order_col': 'order_id', 'date_part': 'order_date'})
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['customer_id'] = pd.to_numeric(tmp_3['customer_id'], errors='coerce').fillna(0).astype(int)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['order_status_code'] = tmp_4['order_status_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['order_date'] = pd.to_datetime(tmp_5['order_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['order_id', 'customer_id', 'order_status_code', 'order_date']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
orders = prepared_table_2.copy()
customers = prepared_table_1.copy()
# Join customers to orders on customer_id
integrated = orders.merge(customers, how='left', on='customer_id')
# Aggregate number of orders by customer
agg = integrated.groupby(['customer_id', 'customer_name'], as_index=False).size().rename(columns={'size': 'order_count'})
# Select required columns: customer name, id, and number of orders
target = agg[['customer_name', 'customer_id', 'order_count']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
