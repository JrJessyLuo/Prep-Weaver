import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['parent_product_id', 'product_size', 'product_description'])
    # DropColumn
    table_1 = table_1.drop(columns=['parent_product_id', 'product_size', 'product_description'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # Explode(table_name="table_1", column=['product_id', 'product_name', 'product_price'], split_comma=False)
    # Explode
    _ex_cols = ['product_id', 'product_name', 'product_price'] if isinstance(['product_id', 'product_name', 'product_price'], list) else [['product_id', 'product_name', 'product_price']]
    if all(_c in table_1.columns for _c in _ex_cols):
        try:
            for _col in _ex_cols:
                _nn = table_1[_col].dropna()
                _sample = _nn.iloc[0] if not _nn.empty else None
                if isinstance(_sample, str) or (pd.isna(_sample) and False):
                    if False:
                        table_1[_col] = table_1[_col].apply(lambda x: [i.strip() for i in str(x).split(',')] if pd.notna(x) and x != '' else [])
                    else:
                        def _ex_parse(x):
                            if pd.isna(x) or x == '':
                                return []
                            try:
                                _r = ast.literal_eval(str(x))
                                return _r if isinstance(_r, list) else [_r]
                            except Exception:
                                return [i.strip() for i in str(x).split()]
                        table_1[_col] = table_1[_col].apply(_ex_parse)
                elif not isinstance(_sample, list) and _sample is not None:
                    table_1[_col] = table_1[_col].apply(lambda x: [x] if pd.notna(x) else [])
            if len(_ex_cols) == 1:
                table_1 = table_1.explode(_ex_cols[0]).reset_index(drop=True)
            else:
                table_1 = table_1.explode(_ex_cols).reset_index(drop=True)
        except Exception:
            pass

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="product_price", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['product_price'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['product_price']
    if _dtype == "datetime64":
        table_1['product_price'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['product_price'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['product_price'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['product_price'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['product_id', 'product_name', 'product_price', 'product_color'])
    # SelectCol
    _cols = [c for c in ['product_id', 'product_name', 'product_price', 'product_color'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['product_id'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['product_id'], ascending=[True])

    # ---------------- Step 7 ----------------
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
    # Sort(table_name="table_1", by=['product_id', 'order_item_id'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['product_id', 'order_item_id'], ascending=[True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['product_id', 'order_item_id', 'order_id'])
    # SelectCol
    _cols = [c for c in ['product_id', 'order_item_id', 'order_id'] if c in table_1.columns]
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
def _prep_3(table_1):
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
products_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
order_items_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])

# Assume products_prepared and order_items_prepared are the synthesized tables
# Count order items per product
order_counts = order_items_prepared.groupby('product_id', dropna=False)['order_item_id'].nunique().reset_index(name='order_item_count')

# Left join counts to products
prod_with_counts = products_prepared.merge(order_counts, on='product_id', how='left')
prod_with_counts['order_item_count'] = prod_with_counts['order_item_count'].fillna(0)

# Filter products listed in less than two orders (interpreted as fewer than 2 order line items)
filtered = prod_with_counts[prod_with_counts['order_item_count'] < 2]

# Select required columns
answer = filtered[['product_id', 'product_name', 'product_price', 'product_color']]

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
