import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'Customer_ID', 'new_name': 'Customer_ID'}, {'old_name': 'Name', 'new_name': 'Name'}])
    # Rename
    table_1 = table_1.rename(columns={'Customer_ID': 'Customer_ID', 'Name': 'Name'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Name", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding double quotes if present
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1].strip()
    #     # remove surrounding single quotes if present (including cases like ''Denis Compton'')
    #     s = re.sub(r"^'+|'+$", "", s).strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding double quotes if present
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1].strip()
        # remove surrounding single quotes if present (including cases like ''Denis Compton'')
        s = re.sub(r"^'+|'+$", "", s).strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Name"] = table_1["Name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Customer_ID', 'Name'])
    # SelectCol
    _cols = [c for c in ['Customer_ID', 'Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Ma Po Tofu", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Ma Po Tofu'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Ma Po Tofu']
    if _dtype == "datetime64":
        table_1['Ma Po Tofu'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Ma Po Tofu'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Ma Po Tofu'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Ma Po Tofu'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Customer_ID', 'Branch_ID', 'Chow Mein', 'Kung Pao Chicken', 'Ma Po Tofu', 'Peking Roasted Duck', 'Spring Rolls'])
    # SelectCol
    _cols = [c for c in ['Customer_ID', 'Branch_ID', 'Chow Mein', 'Kung Pao Chicken', 'Ma Po Tofu', 'Peking Roasted Duck', 'Spring Rolls'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
