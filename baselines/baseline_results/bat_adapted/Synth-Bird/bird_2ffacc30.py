import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['loan_id', 'zh_id', 'date']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['disp_id','client_id','account_id','type']].copy()
    target['type'] = target['type'].astype('string').str.strip().str.upper()
    target = target.dropna(subset=['disp_id','client_id','account_id'])
    target['disp_id'] = target['disp_id'].astype('int64')
    target['client_id'] = target['client_id'].astype('int64')
    target['account_id'] = target['account_id'].astype('int64')
    target = target.drop_duplicates(subset=['disp_id'], keep='first')
    target = target.reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['client_id','district_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_loans = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_dispositions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_clients = prepared_table_3

# Assume prepared_* DataFrames are available
loans = prepared_loans.copy()
disps = prepared_dispositions.copy()
clients = prepared_clients.copy()

# Integrate: loan -> disposition (by account), then -> client (by client_id)
loan_disps = loans.merge(disps, left_on='zh_id', right_on='account_id', how='inner')
loan_disps_clients = loan_disps.merge(clients, on='client_id', how='inner')

# Filter for the specific approval date
loan_disps_clients['date'] = pd.to_datetime(loan_disps_clients['date'])
result = loan_disps_clients[loan_disps_clients['date'] == pd.Timestamp('1994-08-25')]

# Select district_id of the branch/account (via client district)
answer = result[['district_id']].drop_duplicates()

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
