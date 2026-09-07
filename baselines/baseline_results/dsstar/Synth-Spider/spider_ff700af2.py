import pandas as pd

# Access pre-loaded tables
customers_df = tables['table_1']
orders_df = tables['table_2']

# Locate Jeromy’s customer_id
jeromy_rows = customers_df[customers_df['customer_name'] == 'Jeromy']

# Prepare the final answer DataFrame
if not jeromy_rows.empty:
    jeromy_id = jeromy_rows.iloc[0]['customer_id']
    jeromy_orders = orders_df[orders_df['customer_id'] == jeromy_id][['order_id', 'order_date_only', 'order_status_code']]
    jeromy_orders = jeromy_orders.rename(columns={
        'order_id': 'order_id',
        'order_date_only': 'order_date',
        'order_status_code': 'order_status_code'
    })
else:
    jeromy_orders = pd.DataFrame(columns=['order_id', 'order_date', 'order_status_code'])

# Assign to result as required
result = {"jeromy_orders": jeromy_orders}