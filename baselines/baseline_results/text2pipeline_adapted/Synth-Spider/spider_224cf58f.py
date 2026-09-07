import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'customer_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['customer_id', 'address_id', 'payment_method_code', 'customer_number', 'customer_name', 'customer_address', 'customer_phone', 'customer_email']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'order_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'customer_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'order_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['order_id', 'customer_id', 'order_date', 'order_status_code']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['customer_id'] = pd.to_numeric(tmp_0['customer_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['customer_id', 'address_id', 'payment_method_code', 'customer_number', 'customer_name', 'customer_address', 'customer_phone', 'customer_email']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['order_id'] = pd.to_numeric(tmp_0['order_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['customer_id'] = pd.to_numeric(tmp_1['customer_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['order_date'] = pd.to_datetime(tmp_2['order_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['order_id', 'customer_id', 'order_date', 'order_status_code']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
orders = prepared_table_2.copy()
customers = prepared_table_1.copy()
# Left join customers to orders to find customers with no matching order rows
cust_orders = customers.merge(orders[['customer_id']].drop_duplicates(), on='customer_id', how='left', indicator=True)
no_order = cust_orders[cust_orders['_merge'] == 'left_only']
# Return only the customer ids as requested
target = no_order[['customer_id']].drop_duplicates().sort_values('customer_id').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
