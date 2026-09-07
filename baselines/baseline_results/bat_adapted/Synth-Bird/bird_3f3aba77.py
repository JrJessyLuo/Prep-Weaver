import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['member_id','position']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['link_to_member','amount','source','date_received']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_income = prepared_table_2

joined = prepared_income.merge(prepared_members, left_on='link_to_member', right_on='member_id', how='inner')
non_member_payments = joined[joined['position'].str.lower() != 'member']
result = non_member_payments['amount'].astype(float).mean()
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
