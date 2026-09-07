import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Customer_ID','Name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Customer_ID','Branch_ID','Chow Mein','Kung Pao Chicken','Ma Po Tofu','Peking Roasted Duck','Spring Rolls']].copy()
    target[['Chow Mein','Kung Pao Chicken','Ma Po Tofu','Peking Roasted Duck','Spring Rolls']] = target[['Chow Mein','Kung Pao Chicken','Ma Po Tofu','Peking Roasted Duck','Spring Rolls']].fillna(0)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
customers_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
orders_prepared = prepared_table_2

# Assume orders_prepared and customers_prepared are available DataFrames
# 1) Unpivot dish columns to long format to get dish name and quantity per order row
meal_cols = ["Chow Mein", "Kung Pao Chicken", "Ma Po Tofu", "Peking Roasted Duck", "Spring Rolls"]
long_orders = orders_prepared.melt(
    id_vars=["Customer_ID", "Branch_ID"],
    value_vars=meal_cols,
    var_name="Dish",
    value_name="Quantity"
)
# Keep only positive/non-null quantities
long_orders = long_orders.dropna(subset=["Quantity"]).query("Quantity > 0")

# 2) Join with customers to get customer name
joined = long_orders.merge(customers_prepared, on="Customer_ID", how="left")

# 3) Prepare final result: for each order row, show customer name and dish name, sorted by quantity desc
# If multiple rows per customer/branch/dish exist, keep as-is (no aggregation per instructions)
result = joined[["Customer_ID", "Branch_ID", "Name", "Dish", "Quantity"]]
result = result.sort_values(by=["Quantity", "Customer_ID", "Branch_ID", "Dish"], ascending=[False, True, True, True])

# Final projection as requested: customer name and dish name, sorted by quantity descending
answer = result[["Name", "Dish", "Quantity"]]

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
