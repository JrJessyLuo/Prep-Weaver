import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['member_id','first_name','last_name','link_to_major']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['major_id','major_info']].copy()
    target = target.dropna(subset=['major_id','major_info'])
    target = target.drop_duplicates(subset=['major_id'], keep='first')
    target = target.astype({'major_id':'string','major_info':'string'})
    target = target.reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_student_club_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_majors = prepared_table_2

target = prepared_student_club_members.merge(prepared_majors, left_on='link_to_major', right_on='major_id', how='inner')
# Split major_info into components: [major_name, department_or_school, college]
split_cols = target['major_info'].str.split('::', n=2, expand=True)
split_cols.columns = ['major_name', 'department_or_school', 'college']
target = target.join(split_cols)
# Filter to members whose department/school is exactly 'Art and Design Department'
filtered = target[target['department_or_school'] == 'Art and Design Department']
# Create full name
filtered['full_name'] = filtered['first_name'].str.strip() + ' ' + filtered['last_name'].str.strip()
# Select final output column
answer = filtered[['full_name']].drop_duplicates().reset_index(drop=True)

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
