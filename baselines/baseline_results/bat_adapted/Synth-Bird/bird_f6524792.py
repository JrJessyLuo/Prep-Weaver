import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['first_name','last_name','position','ltm']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[table_1['attribute'].isin(['major_name','department'])][['major_id','attribute','value']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_majors = prepared_table_2

# prepared_members and prepared_majors are the synthesized tables per the targets above
merged = prepared_members.merge(prepared_majors, left_on='ltm', right_on='major_id', how='inner')
# Filter to the person of interest
person = merged[(merged['first_name'] == 'Garrett') & (merged['last_name'] == 'Gerke')]
# Pivot attributes to columns to get both major_name and department
pivoted = person.pivot_table(index=['first_name','last_name','position','ltm'], columns='attribute', values='value', aggfunc='first').reset_index()
# Select and rename for final output
result = pivoted[['first_name','last_name','major_name','department']]
# result contains the major (major_name) of Garrett Gerke and its department
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
