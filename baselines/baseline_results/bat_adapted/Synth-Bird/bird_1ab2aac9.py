import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['account_id','date']].drop_duplicates(subset=['account_id']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df_long = table_1.melt(id_vars=['loan_id'], var_name='loan_key', value_name='value')
    df_wide = df_long.pivot(index='loan_key', columns='loan_id', values='value').reset_index(drop=True)
    df_wide = df_wide.rename(columns={c: 'duration' for c in df_wide.columns if str(c).strip().lower() in ['dur', 'duration', 'months', 'month', 'validity', 'validity_months', 'term', 'term_months']})
    df_wide['account_id'] = pd.to_numeric(df_wide['account_id'], errors='coerce') if 'account_id' in df_wide.columns else pd.Series([pd.NA] * len(df_wide))
    df_wide['amount'] = pd.to_numeric(df_wide['amount'], errors='coerce') if 'amount' in df_wide.columns else pd.Series([pd.NA] * len(df_wide))
    df_wide['duration'] = pd.to_numeric(df_wide['duration'], errors='coerce') if 'duration' in df_wide.columns else pd.Series([pd.NA] * len(df_wide))
    target = df_wide[['account_id', 'amount', 'duration']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
accounts_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_table_3 = _prep_3(tables['table_2'])
loans_prepared = prepared_table_3

# Assume accounts_prepared has columns: account_id (as str/int consistently) and date (YYYY-MM-DD)
# Assume loans_prepared has columns: account_id, amount (numeric), duration (months, numeric)

# 1) Integrate on account_id
merged = loans_prepared.merge(accounts_prepared, on='account_id', how='inner')

# 2) Filter: loan validity > 12 months and account opening year = 1993
merged['year'] = pd.to_datetime(merged['date'], errors='coerce').dt.year
flt = (merged['duration'] > 12) & (merged['year'] == 1993)
eligible = merged.loc[flt]

# 3) Find the highest approved amount among eligible accounts
if not eligible.empty:
    max_amt = eligible['amount'].max()
    target = eligible.loc[eligible['amount'] == max_amt, ['account_id', 'amount', 'date']].drop_duplicates()
else:
    target = eligible[['account_id', 'amount', 'date']]

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
