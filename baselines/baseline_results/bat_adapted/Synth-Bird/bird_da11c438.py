import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['client_id','district_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['district_id', 21]].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['client_id','account_id','lx']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1.loc[:, ['account_id','mt','vl']].copy()
    target['account_id'] = target['account_id'].astype(str).str.strip().str.replace('^"|"$', '', regex=True)
    target['mt'] = target['mt'].astype(str).str.strip()
    target['vl'] = target['vl'].astype(str).str.strip()
    target = target.loc[:, ['account_id','mt','vl']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_5'])
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_district_lookup = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_dispositions = prepared_table_3
prepared_table_4 = _prep_4(tables['table_1'])
prepared_account_kv = prepared_table_4

# Assume prepared tables are provided as dataframes with the target names
# 1) Extract account-level district_id from key-value table
acct_district = prepared_account_kv[prepared_account_kv['mt'] == 'district_id'].copy()
# Normalize types/strings
acct_district['account_id'] = acct_district['account_id'].astype(str).str.replace('^"|"$', '', regex=True)
acct_district['account_district_id'] = acct_district['vl'].astype(str)
acct_district = acct_district[['account_id', 'account_district_id']].drop_duplicates()

# 2) Join dispositions to get accounts and roles
disp = prepared_dispositions.copy()
disp['account_id'] = disp['account_id'].astype(str)

acct_with_disp = disp.merge(acct_district, on='account_id', how='left')

# 3) Prepare district lookup: map integer-like column index 21 to a proper name
# Column '21' contains district names (e.g., 'Tabor')
district_lookup = prepared_district_lookup.rename(columns={'21': 'district_name'})[['district_id', 'district_name']]
district_lookup['district_id'] = district_lookup['district_id'].astype(str)

# 4) Filter to accounts whose district name is Tabor via the account's district_id
acct_with_names = acct_with_disp.merge(district_lookup, left_on='account_district_id', right_on='district_id', how='left')

# 5) Keep only Tabor and roles eligible for loans. Assuming eligibility means OWNER dispositions.
eligible_roles = {'OWNER'}
result = acct_with_names[(acct_with_names['district_name'] == 'Tabor') & (acct_with_names['lx'].isin(eligible_roles))]

# 6) Return the list of account_ids (unique)
answer = result[['account_id']].drop_duplicates().sort_values('account_id')

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
