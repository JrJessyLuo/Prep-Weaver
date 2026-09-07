import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="frequency", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return ' '.join(s.split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return ' '.join(s.split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["frequency"] = table_1["frequency"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['account_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['account_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['account_id', 'frequency'])
    # SelectCol
    _cols = [c for c in ['account_id', 'frequency'] if c in table_1.columns]
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['loan_id', 'account_id', 'date', 'status', 'metric', 'value'])
    # SelectCol
    _cols = [c for c in ['loan_id', 'account_id', 'date', 'status', 'metric', 'value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['loan_id', 'account_id', 'date', 'status', 'metric', 'value'], how="all")
    # DropNulls
    table_1 = table_1.dropna(subset=['loan_id', 'account_id', 'date', 'status', 'metric', 'value'], how='all').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_accounts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_loans_long = prepared_table_2

# Assume prepared_accounts and prepared_loans_long are materialized as specified
loans = prepared_loans_long.copy()
accts = prepared_accounts.copy()

# Join loans to accounts on account_id
joined = loans.merge(accts, on='account_id', how='inner')

# Ensure date is datetime
joined['date'] = pd.to_datetime(joined['date'], errors='coerce')

# Filter: accounts with monthly statement issuance (exact match or contains, case-insensitive)
monthly_mask = joined['frequency'].str.upper().str.contains('MESICNE')
joined = joined[monthly_mask]

# Filter loans approved between 1995-01-01 and 1997-12-31 (inclusive)
start = pd.Timestamp('1995-01-01')
end = pd.Timestamp('1997-12-31')
approved = joined[(joined['status'] == 'A') & (joined['date'] >= start) & (joined['date'] <= end)]

# Pivot/extract amount per loan from long metrics
amounts = approved[approved['metric'] == 'amount'][['loan_id', 'account_id', 'date', 'value']].rename(columns={'value': 'amount'})

# Keep loans with amount >= 250000
eligible = amounts[amounts['amount'] >= 250000]

# Count loans per account (as asked: how many loans ... per account)
result = eligible.groupby('account_id', as_index=False).agg(loan_count=('loan_id', 'nunique'))

# If a single overall total is required instead, use: total_count = int(eligible['loan_id'].nunique())

target = result

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
