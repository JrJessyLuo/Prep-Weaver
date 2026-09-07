import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Pivot(table_name="table_1", index="IdClient", columns="attribute", values="details", aggfunc="first")
    # Pivot
    table_1 = table_1.pivot_table(index='IdClient', columns='attribute', values='details', aggfunc='first').reset_index()

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IdClient', 'Name'])
    # SelectCol
    _cols = [c for c in ['IdClient', 'Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Name'], how='any').reset_index(drop=True)

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
    # DropNulls(table_name="table_1", subset=['IdOrder'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['IdOrder'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="IdClient_clean", func="""
    # import pandas as pd
    # import re
    # 
    # def compute(row: pd.Series):
    #     val = row.get('IdClient', None)
    #     if pd.isna(val):
    #         return None
    #     s = str(val).strip()
    #     # remove any double-quote characters and surrounding whitespace
    #     s = s.replace('"', '').strip()
    #     # if the result is empty, return None
    #     return s if s != '' else None
    # """)
    # AddNewColumn

    def compute(row: pd.Series):
        val = row.get('IdClient', None)
        if pd.isna(val):
            return None
        s = str(val).strip()
        # remove any double-quote characters and surrounding whitespace
        s = s.replace('"', '').strip()
        # if the result is empty, return None
        return s if s != '' else None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["IdClient_clean"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IdOrder', 'IdClient_clean'])
    # SelectCol
    _cols = [c for c in ['IdOrder', 'IdClient_clean'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IdOrder_suffix", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IdOrder_suffix"] = table_1["IdOrder_suffix"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IdOrder_num", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IdOrder_num"] = table_1["IdOrder_num"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Concatenate(table_name="table_1", concatenate_columns=['IdOrder_num', 'IdOrder_suffix'], target_column="IdOrder", func="""
    # def concat(row: pd.Series) -> str:
    #     num = "" if pd.isna(row["IdOrder_num"]) else str(row["IdOrder_num"])
    #     suf = "" if pd.isna(row["IdOrder_suffix"]) else str(row["IdOrder_suffix"])
    #     return f"{num}{suf}"
    #  """)
    # Concatenate
    def concat(row: pd.Series) -> str:
        num = "" if pd.isna(row["IdOrder_num"]) else str(row["IdOrder_num"])
        suf = "" if pd.isna(row["IdOrder_suffix"]) else str(row["IdOrder_suffix"])
        return f"{num}{suf}"
    def _cat_apply(row):
        try:
            return concat(row)
        except Exception:
            return None
    table_1["IdOrder"] = table_1[['IdOrder_num', 'IdOrder_suffix']].apply(_cat_apply, axis=1)
    table_1 = table_1.drop(columns=['IdOrder_num', 'IdOrder_suffix'])

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="amount", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['amount'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['amount']
    if _dtype == "datetime64":
        table_1['amount'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['amount'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['amount'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['amount'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IdOrder', 'amount'])
    # SelectCol
    _cols = [c for c in ['IdOrder', 'amount'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_1'])
clients_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
orders_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
order_lines_prepared = prepared_table_3

# Assume input DataFrames: table_1, table_2, table_3

# Prepare clients: select Name attribute and cast IdClient to string for consistent joins
clients_prepared = (
    table_1.loc[table_1['attribute'] == 'Name', ['IdClient', 'details']]
           .rename(columns={'details': 'Name'})
)
clients_prepared['IdClient'] = clients_prepared['IdClient'].astype(str).str.strip()

# Prepare orders: clean IdClient and keep IdOrder
orders_prepared = table_2[['IdOrder', 'IdClient']].copy()
orders_prepared['IdOrder'] = orders_prepared['IdOrder'].astype(str).str.strip()
orders_prepared['IdClient_clean'] = (
    orders_prepared['IdClient'].astype(str).str.strip().str.replace('^\"|\"$', '', regex=True)
)
orders_prepared = orders_prepared[['IdOrder', 'IdClient_clean']]

# Prepare order lines: compose IdOrder and coerce amount numeric
order_lines_prepared = table_3[['IdOrder_num', 'IdOrder_suffix', 'amount']].copy()
order_lines_prepared['IdOrder'] = order_lines_prepared['IdOrder_num'].astype(str) + order_lines_prepared['IdOrder_suffix'].astype(str)
order_lines_prepared['IdOrder'] = order_lines_prepared['IdOrder'].str.strip()
order_lines_prepared['amount'] = pd.to_numeric(order_lines_prepared['amount'], errors='coerce').fillna(0).astype(int)
order_lines_prepared = order_lines_prepared[['IdOrder', 'amount']]

# Integration: lines -> orders -> clients
lines_orders = order_lines_prepared.merge(orders_prepared, on='IdOrder', how='inner')
full = lines_orders.merge(clients_prepared, left_on='IdClient_clean', right_on='IdClient', how='inner')

# Aggregate total amounts of books per client name
answer = (full.groupby('Name', as_index=False)['amount'].sum()
               .rename(columns={'amount': 'total_books_ordered'}))

target = answer

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
