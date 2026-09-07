import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['address_id', 'payment_method_code', 'customer_address', 'customer_phone', 'customer_email'])
    # DropColumn
    table_1 = table_1.drop(columns=['address_id', 'payment_method_code', 'customer_address', 'customer_phone', 'customer_email'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="customer_name", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping single/double quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["customer_name"] = table_1["customer_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="customer_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['customer_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['customer_id']
    if _dtype == "datetime64":
        table_1['customer_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['customer_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['customer_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['customer_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="customer_number", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['customer_number'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['customer_number']
    if _dtype == "datetime64":
        table_1['customer_number'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['customer_number'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['customer_number'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['customer_number'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['customer_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['customer_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
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
    # CodeGeneration(table_names=['table_1'], target_table="normalized_orders", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     # table_1 is in a pivoted layout:
    #     # first column 'order_id' contains field names (e.g., customer_id, order_status_code, date_part)
    #     # numbered columns are order instances.
    #     df = table_1.copy()
    #     key_col = df.columns[0]  # 'order_id'
    #     df = df.set_index(key_col).T.reset_index().rename(columns={'index': 'order_id'})
    #     # keep only required columns
    #     out = df[['order_id', 'customer_id']].copy()
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        # table_1 is in a pivoted layout:
        # first column 'order_id' contains field names (e.g., customer_id, order_status_code, date_part)
        # numbered columns are order instances.
        df = table_1.copy()
        key_col = df.columns[0]  # 'order_id'
        df = df.set_index(key_col).T.reset_index().rename(columns={'index': 'order_id'})
        # keep only required columns
        out = df[['order_id', 'customer_id']].copy()
        return out
    normalized_orders = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="normalized_orders", column="order_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = normalized_orders['order_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = normalized_orders['order_id']
    if _dtype == "datetime64":
        normalized_orders['order_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        normalized_orders['order_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        normalized_orders['order_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        normalized_orders['order_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="normalized_orders", column="customer_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = normalized_orders['customer_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = normalized_orders['customer_id']
    if _dtype == "datetime64":
        normalized_orders['customer_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        normalized_orders['customer_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        normalized_orders['customer_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        normalized_orders['customer_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['normalized_orders'])
    # Terminate
    result = {'normalized_orders': normalized_orders}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
