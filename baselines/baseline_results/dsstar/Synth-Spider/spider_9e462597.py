import pandas as pd

# Access preloaded tables
customers = tables['table_1']  # spider_9e462597_input_0.pkl
orders = tables['table_2']     # spider_9e462597_input_1.pkl

# Reproduce the same logic as the reference code to find customers without orders
cust_ids = set(customers['customer_id'].tolist())
order_cust_ids = set(orders['customer_id'].tolist())
customers_without_orders_list = sorted(list(cust_ids - order_cust_ids))

# Prepare final answer DataFrame
answer_df = pd.DataFrame({'customer_id': customers_without_orders_list})

# Assign to result as required
result = {
    'customers_without_orders': answer_df
}