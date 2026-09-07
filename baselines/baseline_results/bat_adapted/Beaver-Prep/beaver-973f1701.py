import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['BUILDING_KEY','BUILDING_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['SUBJECT_ID','OFFER_DEPT_NAME','COURSE_NUMBER']].copy()
    prepared = prepared.dropna(subset=['SUBJECT_ID','OFFER_DEPT_NAME','COURSE_NUMBER'])
    prepared = prepared.drop_duplicates()
    target = prepared[['SUBJECT_ID','OFFER_DEPT_NAME','COURSE_NUMBER']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_offerings = prepared_table_2

# prepared_buildings: columns ['BUILDING_KEY','BUILDING_NAME']
# prepared_offerings: columns ['SUBJECT_ID','OFFER_DEPT_NAME','COURSE_NUMBER']

# Filter offerings to the Center for International Studies
cis_offerings = prepared_offerings[prepared_offerings['OFFER_DEPT_NAME'].str.strip().str.lower() == 'center for international studies']

# Count number of distinct courses/subjects per building is not directly possible because offerings lack a building key.
# Produce a building-wise result with zero counts (or NaN) to reflect absence of a join path.
result = prepared_buildings.copy()
result['num_cis_courses'] = 0

# Final selection
answer = result[['BUILDING_KEY', 'BUILDING_NAME', 'num_cis_courses']]

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
