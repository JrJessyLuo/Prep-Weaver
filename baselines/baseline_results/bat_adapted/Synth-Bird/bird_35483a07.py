import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['account_id','frequency']].drop_duplicates(subset=['account_id'])
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['loan_id','account_id','date','status','metric','value']].copy()
    target['date'] = pd.to_datetime(target['date'], errors='coerce')
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
