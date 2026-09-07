import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['product_name'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['product_name'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="product_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['product_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['product_id']
    if _dtype == "datetime64":
        table_1['product_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['product_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['product_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['product_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['product_id', 'product_name'])
    # SelectCol
    _cols = [c for c in ['product_id', 'product_name'] if c in table_1.columns]
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
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="order_items_long", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    #     # first column holds variable names: order_id / product_id / order_quantity
    #     df = df.set_index('order_item_id').T.reset_index(drop=True)
    #     # keep only required columns
    #     out = df[['order_id', 'product_id']].copy()
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()
        # first column holds variable names: order_id / product_id / order_quantity
        df = df.set_index('order_item_id').T.reset_index(drop=True)
        # keep only required columns
        out = df[['order_id', 'product_id']].copy()
        return out
    order_items_long = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="order_items_long", column="order_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = order_items_long['order_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = order_items_long['order_id']
    if _dtype == "datetime64":
        order_items_long['order_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        order_items_long['order_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        order_items_long['order_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        order_items_long['order_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="order_items_long", column="product_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = order_items_long['product_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = order_items_long['product_id']
    if _dtype == "datetime64":
        order_items_long['product_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        order_items_long['product_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        order_items_long['product_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        order_items_long['product_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="order_items_long", subset=['order_id', 'product_id'], how="any")
    # DropNulls
    order_items_long = order_items_long.dropna(subset=['order_id', 'product_id'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="order_items_long", subset=['order_id', 'product_id'], keep="first")
    # Deduplicate
    order_items_long = order_items_long.drop_duplicates(subset=['order_id', 'product_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="order_items_long", columns=['order_id', 'product_id'])
    # SelectCol
    _cols = [c for c in ['order_id', 'product_id'] if c in order_items_long.columns]
    order_items_long = order_items_long[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Terminate(result=['order_items_long'])
    # Terminate
    result = {'order_items_long': order_items_long}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
products = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_table_3 = _prep_3(tables['table_2'])
order_items_long = prepared_table_3

# Assume products is already the selected columns from table_1
# For table_3, unpivot to long format using the first row as order_id values and second row as product_id values

def prepare_order_items_long(table_3):
    # table_3 has rows labeled by 'order_item_id' with subsequent columns 1..N holding values
    # Extract rows
    row_map = {r['order_item_id']: r for _, r in table_3.iterrows()}
    # Collect numeric column labels (as strings in DataFrame)
    value_cols = [c for c in table_3.columns if c != 'order_item_id']
    order_ids = [row_map['order_id'][c] for c in value_cols]
    product_ids = [row_map['product_id'][c] for c in value_cols]
    df = pd.DataFrame({'order_id': order_ids, 'product_id': product_ids})
    # Ensure dtypes are numeric where possible
    df['order_id'] = pd.to_numeric(df['order_id'], errors='coerce')
    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce')
    # Drop any rows with missing ids
    df = df.dropna(subset=['product_id'])
    return df

# prepared tables available as variables: products (cols: product_id, product_name) and table_3
order_items_long = prepare_order_items_long(table_3)

# Left-anti join: products without any matching order_items
ordered_products = order_items_long[['product_id']].drop_duplicates()
result = products.merge(ordered_products, on='product_id', how='left', indicator=True)
result = result[result['_merge'] == 'left_only']

# Final projection: product names without an order
answer = result[['product_name']].drop_duplicates().reset_index(drop=True)

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
