import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['major_id','major_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[table_1['shuxing'].eq('link_to_major'), ['member_id', 'zhi']].rename(columns={'zhi': 'major_id'}).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
majors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
member_major_links = prepared_table_2

env_major_ids = majors[majors['major_name'].str.strip().str.lower() == 'environmental engineering']['major_id'].unique()
linked = member_major_links[member_major_links['major_id'].isin(env_major_ids)]
# Count distinct members in the Student_Club who have the Environmental Engineering major
answer = linked['member_id'].nunique()

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
