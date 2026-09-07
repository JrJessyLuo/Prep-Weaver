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
    target = table_1[['client_id','account_id','attribute','value']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['account_id','k_symbol']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['account_id']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_5'])
clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
client_account_roles = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
orders = prepared_table_3
prepared_table_4 = _prep_4(tables['table_6'])
loans = prepared_table_4

# Inputs expected: clients, client_account_roles, orders, loans

# Determine, per account, whether there exists a permanent order and/or a loan
# Here we assume k_symbol 'SIPO' denotes a permanent order (typical in Czech bank datasets)
orders_perm = orders[orders['k_symbol'] == 'SIPO'][['account_id']].drop_duplicates()
orders_perm['has_perm_order'] = True

loans_flag = loans[['account_id']].drop_duplicates()
loans_flag['has_loan'] = True

# Map account-level rights to client-account roles (any role gives the client the potential right on that account)
car = client_account_roles[['client_id','account_id']].drop_duplicates()
car = car.merge(orders_perm, on='account_id', how='left')
car = car.merge(loans_flag, on='account_id', how='left')
car['has_perm_order'] = car['has_perm_order'].fillna(False)
car['has_loan'] = car['has_loan'].fillna(False)

# Aggregate to client level: for each client, collect the set of rights they have on any of their accounts
agg = car.groupby('client_id').agg(
    has_any_perm_order = ('has_perm_order','any'),
    has_any_loan = ('has_loan','any')
).reset_index()

# Eligible clients: can only have the right to issue permanent orders or apply for loans
# i.e., they have no other rights beyond these two. Since only these two rights are modeled here,
# we interpret the condition as clients who do NOT have both rights simultaneously (only one of the two).
eligible = agg[(agg['has_any_perm_order'] ^ agg['has_any_loan'])]

# Attach district and produce final columns
result = eligible.merge(clients[['client_id','district_id']], on='client_id', how='left')
result = result[['client_id','district_id']].drop_duplicates()

# result is the final answer dataframe

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
