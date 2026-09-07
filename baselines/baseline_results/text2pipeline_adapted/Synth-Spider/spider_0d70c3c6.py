import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'product_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['product_id', 'product_name', 'product_type_code', 'product_price']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['order_id', 'customer_id', 'order_date', 'order_status_code']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': ['order_item_id'], 'value_vars': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], 'var_name': 'order_item_seq', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': ['order_item_seq'], 'columns': 'order_item_id', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'order_item_seq', 'new_name': 'order_item_seq'}, {'old_name': 'order_id', 'new_name': 'order_id'}, {'old_name': 'product_id', 'new_name': 'product_id'}, {'old_name': 'order_quantity', 'new_name': 'order_quantity'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'order_item_seq', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'order_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'product_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'order_quantity', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['order_item_seq', 'order_id', 'product_id', 'order_quantity']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['product_id'] = pd.to_numeric(tmp_0['product_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['product_id', 'product_name', 'product_type_code', 'product_price']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['order_id', 'customer_id', 'order_date', 'order_status_code']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['order_item_id'], value_vars=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], var_name='order_item_seq', value_name='value')
    # Step 2: Pivot
    tmp_1 = pd.pivot_table(tmp_0, index=['order_item_seq'], columns='order_item_id', values='value', aggfunc='first').reset_index()
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'order_item_seq': 'order_item_seq', 'order_id': 'order_id', 'product_id': 'product_id', 'order_quantity': 'order_quantity'})
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['order_item_seq'] = tmp_3['order_item_seq'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['order_id'] = pd.to_numeric(tmp_4['order_id'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['product_id'] = pd.to_numeric(tmp_5['product_id'], errors='coerce').fillna(0).astype(int)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['order_quantity'] = pd.to_numeric(tmp_6['order_quantity'], errors='coerce').fillna(0).astype(int)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['order_item_seq', 'order_id', 'product_id', 'order_quantity']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
oi = prepared_table_3.copy()
prods = prepared_table_1[['product_id','product_name']].copy()
# Find product_ids that appear in any order item
ordered_pids = oi[['product_id']].drop_duplicates()
# Left join products to ordered_pids to identify missing matches
merged = prods.merge(ordered_pids, on='product_id', how='left', indicator=True)
no_order = merged[merged['_merge'] == 'left_only']
# Project the required output: product names without an order
target = no_order[['product_name']].reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
