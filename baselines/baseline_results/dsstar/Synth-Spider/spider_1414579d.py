import pandas as pd

# Access pre-loaded DataFrames from `tables`
df_customers = tables['table_1']
df_orders = tables['table_2']

# Reproduce the SAME logic as the reference code
unique_customers = set(df_customers['customer_id'].unique())
unique_orders_customers = set(df_orders['customer_id'].unique())

customers_not_in_orders = sorted(unique_customers.difference(unique_orders_customers))

# Prepare final answer DataFrame: count of customers who have not made an order
answer_df = pd.DataFrame({
    'customers_without_orders_count': [len(customers_not_in_orders)]
})

# Assign to result as required
result = {'customers_without_orders_count': answer_df}