import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ISBN', 'Title'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ISBN', 'Title'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ISBN', 'Title'])
    # SelectCol
    _cols = [c for c in ['ISBN', 'Title'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ISBN'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ISBN'], keep='first').reset_index(drop=True)

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
    # AddNewColumn(table_name="table_1", new_column_name="ISBN", func="""
    # def compute(row):
    #     val = row.get('ISBN_amount')
    #     if val is None:
    #         return None
    #     s = str(val).strip()
    #     if '-' in s:
    #         return s.rsplit('-', 1)[0].strip() or None
    #     return s or None
    # """)
    # AddNewColumn
    def compute(row):
        val = row.get('ISBN_amount')
        if val is None:
            return None
        s = str(val).strip()
        if '-' in s:
            return s.rsplit('-', 1)[0].strip() or None
        return s or None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["ISBN"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="Quantity", func="""
    # import re
    # def compute(row):
    #     val = row.get('ISBN_amount')
    #     if val is None:
    #         return None
    #     s = str(val).strip()
    #     if not s:
    #         return None
    #     # quantity is the part after the last hyphen, e.g., "8233771378567-1" -> 1
    #     if '-' in s:
    #         qty_part = s.rsplit('-', 1)[1].strip()
    #     else:
    #         qty_part = None
    #     if qty_part is None or qty_part == '':
    #         return None
    #     # keep only numeric quantities
    #     if re.fullmatch(r"\d+", qty_part):
    #         return int(qty_part)
    #     return None
    # """)
    # AddNewColumn
    def compute(row):
        val = row.get('ISBN_amount')
        if val is None:
            return None
        s = str(val).strip()
        if not s:
            return None
        # quantity is the part after the last hyphen, e.g., "8233771378567-1" -> 1
        if '-' in s:
            qty_part = s.rsplit('-', 1)[1].strip()
        else:
            qty_part = None
        if qty_part is None or qty_part == '':
            return None
        # keep only numeric quantities
        if re.fullmatch(r"\d+", qty_part):
            return int(qty_part)
        return None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["Quantity"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Quantity", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Quantity'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Quantity']
    if _dtype == "datetime64":
        table_1['Quantity'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Quantity'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Quantity'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Quantity'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IdOrder', 'ISBN', 'Quantity'])
    # SelectCol
    _cols = [c for c in ['IdOrder', 'ISBN', 'Quantity'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
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
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="DateExped", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['DateExped'] = table_1['DateExped'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['DateExped'] = table_1['DateExped'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IdOrder'])
    # SelectCol
    _cols = [c for c in ['IdOrder'] if c in table_1.columns]
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
books = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
order_lines = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
orders = prepared_table_3

# Assume prepared tables exist: books, order_lines, orders
# order_lines has ISBN and Quantity parsed from ISBN_amount (e.g., '8233771378567-1')

ol_books = order_lines.merge(books, on='ISBN', how='inner')
# Optional join to orders (kept to honor integration plan; not strictly needed for the count)
ol_full = ol_books.merge(orders, on='IdOrder', how='left')

# Filter for the target title and sum quantities
answer = int(ol_full.loc[ol_full['Title'].str.strip().str.lower() == 'pride and prejudice', 'Quantity'].sum())
result = pd.DataFrame({'number_of_orders_received_for_pride_and_prejudice': [answer]})

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
