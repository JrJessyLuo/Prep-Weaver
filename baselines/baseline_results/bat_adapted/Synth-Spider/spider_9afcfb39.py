import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['StuID','city_code']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['cid','city_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
students_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
cities_prepared = prepared_table_2

target = students_prepared.merge(cities_prepared, left_on='city_code', right_on='cid', how='left')
answer = target.groupby('city_name', dropna=False)['StuID'].count().reset_index(name='num_students').sort_values(['num_students','city_name'], ascending=[False,True])

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
