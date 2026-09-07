import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    parts = df['amount_duration_payments'].astype(str).str.split('-', n=2, expand=True)
    df['amount'] = pd.to_numeric(parts[0], errors='coerce').astype('Int64')
    df['duration'] = pd.to_numeric(parts[1], errors='coerce').astype('Int64')
    df['payments'] = pd.to_numeric(parts[2], errors='coerce')
    target = df[['loan_id','account_id','date','status','amount','duration','payments']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['issuance_frequency'] = (df['freq_part1'].fillna('').astype(str).str.strip() + ' ' + df['freq_part2'].fillna('').astype(str).str.strip()).str.strip()
    target = df[['account_id','district_id','date','issuance_frequency']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_loans = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_accounts = prepared_table_2

# Assume prepared_loans and prepared_accounts are produced as per targets above.
# 1) Filter loans to approved in 1997
loans_1997 = prepared_loans.copy()
# interpret approved status as 'A' (based on sample); adjust if schema dictionary specifies otherwise
loans_1997 = loans_1997[loans_1997['status'] == 'A']
loans_1997 = loans_1997[pd.to_datetime(loans_1997['date'], errors='coerce').dt.year == 1997]

# 2) Find lowest approved amount among these
min_amount = loans_1997['amount'].min()
lowest_loans = loans_1997[loans_1997['amount'] == min_amount]

# 3) Join to accounts to get issuance frequency and select weekly issuance
merged = lowest_loans.merge(prepared_accounts, on='account_id', how='left')

# Normalize issuance_frequency to detect weekly; common Czech dataset uses 'TYDNE' for weekly
freq_norm = merged['issuance_frequency'].astype(str).str.lower()
is_weekly = freq_norm.str.contains('tydne') | freq_norm.str.contains('weekly') | freq_norm.str.contains('tyden')
weekly_lowest = merged[is_weekly]

# 4) Return the accounts (unique) that meet criteria, along with evidence columns
result = weekly_lowest[['account_id', 'loan_id', 'amount', 'date', 'issuance_frequency']].drop_duplicates().sort_values(['account_id', 'loan_id'])

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
