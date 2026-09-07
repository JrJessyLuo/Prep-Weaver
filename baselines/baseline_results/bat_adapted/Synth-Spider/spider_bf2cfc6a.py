import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['customer_id','customer_number','customer_name']].drop_duplicates(subset=['customer_id'], keep='first')
    target = prepared[['customer_id','customer_number','customer_name']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    customer_row = df[df['order_id'].eq('customer_id')]
    long = customer_row.melt(id_vars=['order_id'], var_name='order_id', value_name='customer_id')
    long = long.drop(columns=['order_id_0']) if 'order_id_0' in long.columns else long
    long['order_id'] = long['order_id'].astype(str)
    target = long[['order_id','customer_id']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_customers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_orders = prepared_table_2

# prepared_customers already has: customer_id (int), customer_number (int), customer_name (str)
# prepared_orders must be synthesized from the pivot-like table_2:
# - Row with order_id=='customer_id' contains the customer_id for each order column (1..15)
# - Build a long dataframe of orders with columns: order_col (int), customer_id (int)

# Assume access to the already loaded raw tables as dataframes: table_1, table_2

# 1) Build prepared_customers
prepared_customers = table_1[["customer_id", "customer_number", "customer_name"]].copy()

# 2) Build prepared_orders by unpivoting table_2
# Identify the row that holds customer_id values
cust_row = table_2[table_2["order_id"] == "customer_id"].iloc[0]
# Collect numbered columns
num_cols = [c for c in table_2.columns if isinstance(c, (int, float)) or (isinstance(c, str) and c.isdigit())]
# Ensure numeric column labels are treated uniformly as strings when indexing
# Convert to long format: one row per order (per numbered column)
orders_long = (
    pd.DataFrame({
        "order_col": num_cols,
        "customer_id": [cust_row[c] for c in num_cols]
    })
)
# Clean types
orders_long["order_col"] = orders_long["order_col"].astype(int)
orders_long["customer_id"] = pd.to_numeric(orders_long["customer_id"], errors="coerce").astype('Int64')
# Filter valid rows
orders_long = orders_long.dropna(subset=["customer_id"]).copy()
orders_long["customer_id"] = orders_long["customer_id"].astype(int)

# Create a stable order_id from the column index (e.g., prefix with 'O')
prepared_orders = orders_long.rename(columns={"order_col": "order_seq"})
prepared_orders["order_id"] = "O" + prepared_orders["order_seq"].astype(str)
prepared_orders = prepared_orders[["order_id", "customer_id"]]

# 3) Integrate and compute counts per customer
merged = prepared_customers.merge(prepared_orders, on="customer_id", how="left")
result = (
    merged.groupby(["customer_id", "customer_name"], as_index=False)
          .agg(number_of_orders=("order_id", "count"))
)
# Final selection with id, name, and order count
target = result[["customer_id", "customer_name", "number_of_orders"]]

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
