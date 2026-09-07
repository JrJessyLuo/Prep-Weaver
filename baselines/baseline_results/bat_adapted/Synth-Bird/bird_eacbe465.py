import pandas as pd
import numpy as np

def _prep_1(table_1):
    members = table_1[['member_id','phone','full_name']].copy()
    members['member_id'] = members['member_id'].astype(str)
    target = members.drop_duplicates(subset=['member_id'], keep='first').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    id_col = 'link_to_member'
    value_vars = [c for c in df.columns if c != id_col]
    long_df = df.melt(id_vars=[id_col], value_vars=value_vars, var_name='member_id', value_name='attendance_value')
    long_df['attendance_value'] = long_df['attendance_value'].astype('string')
    long_df = long_df[long_df['attendance_value'].notna() & (long_df['attendance_value'].str.strip() != '')]
    target = long_df[['member_id']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
members_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
attendance_prepared = prepared_table_2

target = members_prepared.merge(attendance_prepared, on='member_id', how='inner')
answer = target.loc[target['phone'].str.replace('[^0-9]', '', regex=True) == '9545556240']
result = answer['member_id'].value_counts().iloc[0] if not answer.empty else 0

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
