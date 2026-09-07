import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','nm']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['id','discount_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_discounts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_rental_history = prepared_table_2

target = prepared_rental_history.merge(prepared_discounts, left_on='discount_id', right_on='id', how='left')
agg = target.groupby('nm', dropna=False)['id_x'].count().reset_index(name='rental_count')
result = agg.sort_values(['rental_count','nm'], ascending=[False, True]).head(1)[['nm']]

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
