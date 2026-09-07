import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['account_id', 'date'])
    # SelectCol
    _cols = [c for c in ['account_id', 'date'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="account_id", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # remove wrapping quotes and any stray quotes/spaces
    #     s2 = str(s).strip()
    #     s2 = re.sub(r'^"+|"+$', '', s2)   # trim leading/trailing quotes
    #     s2 = s2.replace('"', '').strip()  # remove any remaining quotes
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # remove wrapping quotes and any stray quotes/spaces
        s2 = str(s).strip()
        s2 = re.sub(r'^"+|"+$', '', s2)   # trim leading/trailing quotes
        s2 = s2.replace('"', '').strip()  # remove any remaining quotes
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["account_id"] = table_1["account_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date", date_format="%Y-%m-%d")
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
    table_1['date'] = table_1['date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['date'] = table_1['date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     # keep accounts opened in year 1993
    #     try:
    #         return str(row['date'])[:4] == '1993'
    #     except Exception:
    #         return False
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # keep accounts opened in year 1993
        try:
            return str(row['date'])[:4] == '1993'
        except Exception:
            return False
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

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
def _prep_2(table_1):
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['loan_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['loan_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="loan_tidy", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # First column holds attribute names (e.g., account_id/amount/duration)
    #     df = df.set_index('loan_id').T.reset_index(drop=True)
    # 
    #     # Keep only required columns (if present)
    #     required = ['account_id', 'amount', 'duration']
    #     df = df[[c for c in required if c in df.columns]]
    # 
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # First column holds attribute names (e.g., account_id/amount/duration)
        df = df.set_index('loan_id').T.reset_index(drop=True)

        # Keep only required columns (if present)
        required = ['account_id', 'amount', 'duration']
        df = df[[c for c in required if c in df.columns]]

        return df
    loan_tidy = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="loan_tidy", column="account_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = loan_tidy['account_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = loan_tidy['account_id']
    if _dtype == "datetime64":
        loan_tidy['account_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        loan_tidy['account_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        loan_tidy['account_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        loan_tidy['account_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="loan_tidy", column="amount", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = loan_tidy['amount'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = loan_tidy['amount']
    if _dtype == "datetime64":
        loan_tidy['amount'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        loan_tidy['amount'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        loan_tidy['amount'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        loan_tidy['amount'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="loan_tidy", column="duration", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = loan_tidy['duration'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = loan_tidy['duration']
    if _dtype == "datetime64":
        loan_tidy['duration'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        loan_tidy['duration'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        loan_tidy['duration'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        loan_tidy['duration'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Terminate(result=['loan_tidy'])
    # Terminate
    result = {'loan_tidy': loan_tidy}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_accounts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_table_3 = _prep_3(tables['table_2'])
prepared_loans = prepared_table_3

# prepared_accounts has columns: account_id (as string), date (YYYY-MM-DD)
# prepared_loans has columns: account_id (as string), amount (numeric), duration (numeric months)

# Integrate
merged = prepared_loans.merge(prepared_accounts, on='account_id', how='inner')

# Filter: duration > 12 months and account opening year = 1993
merged['year'] = pd.to_datetime(merged['date'], errors='coerce').dt.year
filtered = merged[(merged['duration'] > 12) & (merged['year'] == 1993)]

# Find highest approved amount among the filtered
if filtered.empty:
    target = filtered[['account_id', 'amount', 'date']].drop_duplicates()
else:
    max_amt = filtered['amount'].max()
    target = filtered[filtered['amount'] == max_amt][['account_id', 'amount', 'date']].drop_duplicates().sort_values('account_id')

# 'target' lists the accounts with the highest approved amount satisfying the conditions.

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
