import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['University_ID','yxmc']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Major_ID','Major_Name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['u_id','m_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
universities = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
majors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
university_major_offerings = prepared_table_3

majors_filtered = majors[majors['Major_Name'].isin(['Accounting', 'Urban Education'])]
offerings_joined = university_major_offerings.merge(majors_filtered, left_on='m_id', right_on='Major_ID', how='inner')
# Count distinct matched majors per university and keep those with both
major_counts = offerings_joined.groupby('u_id')['Major_Name'].nunique().reset_index(name='num_majors')
unis_with_both = major_counts[major_counts['num_majors'] == 2]
result = unis_with_both.merge(universities, left_on='u_id', right_on='University_ID', how='inner')
answer = result['yxmc'].drop_duplicates().sort_values().tolist()

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
