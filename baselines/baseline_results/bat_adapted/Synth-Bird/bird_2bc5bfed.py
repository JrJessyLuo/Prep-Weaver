import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['income_id','link_to_member','year','month','day','amount','source','notes']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['member_id','first_name','last_name','email','position','t_shirt_size','phone','zip','link_to_major']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_income = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_members = prepared_table_2

target = prepared_income.merge(prepared_members, left_on='link_to_member', right_on='member_id', how='inner')
# Filter for the specific member name
mask = (target['first_name'].str.strip().str.casefold() == 'casey') & (target['last_name'].str.strip().str.casefold() == 'mason')
ans = target.loc[mask].copy()
# Construct received date as YYYY-MM-DD (zero-pad month/day)
ans['received_date'] = ans['year'].astype(str).str.zfill(4) + '-' + ans['month'].astype(str).str.zfill(2) + '-' + ans['day'].astype(str).str.zfill(2)
# Select evidence columns
answer = ans[['first_name','last_name','received_date','amount','source','income_id']]

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
