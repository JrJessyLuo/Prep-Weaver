import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['account_id','district_id','date']].copy()
    target['date'] = pd.to_datetime(target['date'], errors='coerce').dt.date
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['account_id','client_id','type']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    clients = table_1[['client_id','gender']].copy()
    clients = clients.drop_duplicates(subset=['client_id'])
    target = clients[['client_id','gender']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1[['district_number','value']].copy()
    df['district_number'] = pd.to_numeric(df['district_number'], errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    target = df[['district_number','value']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
accounts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
dispositions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
clients = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
district_metrics = prepared_table_4

# Assume prepared tables exist: accounts, dispositions, clients, district_metrics
# 1) Convert keys to comparable types
accounts = accounts.copy()
accounts['district_id'] = pd.to_numeric(accounts['district_id'], errors='coerce')

metrics = district_metrics.copy()
metrics['district_number'] = pd.to_numeric(metrics['district_number'], errors='coerce')
metrics['value'] = pd.to_numeric(metrics['value'], errors='coerce')

# 2) Join accounts to district metrics to get average salary per account's district
acc_with_salary = accounts.merge(metrics, left_on='district_id', right_on='district_number', how='inner')

# 3) Keep only districts with average salary > 10000
rich_acc = acc_with_salary[acc_with_salary['value'] > 10000][['account_id']]

# 4) Link dispositions (only owners) to those accounts
owners = dispositions[dispositions['type'].str.upper() == 'OWNER']
rich_owner_links = owners.merge(rich_acc, on='account_id', how='inner')

# 5) Join to clients to get gender
rich_clients = rich_owner_links.merge(clients[['client_id','gender']], on='client_id', how='left')

# 6) Compute percentage of women among these clients
denom = len(rich_clients)
if denom == 0:
    result = 0.0
else:
    num_women = (rich_clients['gender'].str.upper() == 'F').sum()
    result = 100.0 * num_women / denom

answer = result

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
