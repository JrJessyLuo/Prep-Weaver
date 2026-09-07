import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df = df.set_index('Employee')
    df = df.loc[['Planet','Level']]
    df = df.T
    df = df.rename(columns={'Planet':'employee_id','Level':'omega_level'}).reset_index(drop=True)
    target = df[['employee_id','omega_level']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.rename(columns={'ygh':'employee_id','Name':'name'})[['employee_id','name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
employee_clearance_levels = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
employees = prepared_table_2

target = employee_clearance_levels.merge(employees, on='employee_id', how='inner'); result = target[target['omega_level'] == 3][['name']].drop_duplicates().sort_values(by='name').reset_index(drop=True)

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
