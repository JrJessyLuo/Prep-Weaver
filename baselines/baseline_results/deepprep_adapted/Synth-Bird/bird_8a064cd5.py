import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TransactionID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TransactionID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TransactionID']
    if _dtype == "datetime64":
        table_1['TransactionID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TransactionID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TransactionID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TransactionID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ProductID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ProductID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ProductID']
    if _dtype == "datetime64":
        table_1['ProductID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ProductID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ProductID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ProductID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ProductID', 'TransactionID'])
    # SelectCol
    _cols = [c for c in ['ProductID', 'TransactionID'] if c in table_1.columns]
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
    # Deduplicate(table_name="table_1", subset=['ProductID', 'Popis'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ProductID', 'Popis'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ProductID', 'Popis'])
    # SelectCol
    _cols = [c for c in ['ProductID', 'Popis'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ProductID", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ProductID"] = table_1["ProductID"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Popis", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Popis"] = table_1["Popis"].apply(_std_apply)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_transactions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_products = prepared_table_2

# Assume prepared_transactions and prepared_products are available DataFrames
# 1) Clean datatypes for join
pt = prepared_transactions.copy()
pp = prepared_products.copy()

# Ensure ProductID comparable as string
pt['ProductID'] = pt['ProductID'].astype(str)
pp['ProductID'] = pp['ProductID'].astype(str)

# Some rows in prepared_products sample show header-like corruption; drop rows where ProductID equals column name or Popis equals column name
pp = pp[(pp['ProductID'].str.lower() != 'popis') & (pp['Popis'].str.lower() != 'popis')]

# 2) Join to get names
joined = pt.merge(pp, on='ProductID', how='left')

# 3) Count sales by product (number of transactions)
counts = joined.groupby(['ProductID', 'Popis'], dropna=False)['TransactionID'].nunique().reset_index(name='sales_count')

# 4) Get top 5 by sales_count
result = counts.sort_values(['sales_count', 'ProductID'], ascending=[False, True]).head(5)

# Final answer: list of full names in order
answer = result['Popis'].tolist()
answer_df = result[['Popis', 'sales_count']]

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
