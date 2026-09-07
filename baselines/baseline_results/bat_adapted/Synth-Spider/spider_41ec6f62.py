import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['EmployeeID','Name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    shipments = table_1[['Shipment','Sender','Recipient']].copy()
    target = shipments.groupby('Shipment', as_index=False).agg({'Sender':'first','Recipient':'first'})[['Shipment','Sender','Recipient']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
employees_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
shipments_prepared = prepared_table_2

emp = employees_prepared
target_name = 'Phillip J. Fry'
fry_ids = emp.loc[emp['Name'] == target_name, 'EmployeeID']
ship = shipments_prepared
# Find shipments where Fry is sender or recipient
res = ship[ship['Sender'].isin(fry_ids) | ship['Recipient'].isin(fry_ids)][['Shipment']].drop_duplicates().sort_values('Shipment')
answer = res['Shipment'].tolist()

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
