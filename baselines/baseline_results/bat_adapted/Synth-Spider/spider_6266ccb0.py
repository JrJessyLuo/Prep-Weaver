import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['student_id','StuID','attribute_value']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['city_code','city_name','state_country']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
student_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
cities = prepared_table_2

# Assume prepared tables are provided as dataframes: student_attributes, cities

# 1) Derive country from state_country field
cities2 = cities.copy()
# state_country like 'MD~U.S.A.'; split on '~' and take the last segment as country
cities2['country'] = cities2['state_country'].astype(str).str.split('~').str[-1].str.strip().str.replace('.', '', regex=False).str.upper()

# 2) Identify rows in student_attributes that encode the student's city (attribute name likely 'City' or similar). Since schema is generic, match where attribute_value equals a known city_code by joining on attribute_value=city_code.
student_city = student_attributes.merge(cities2[['city_code','country']], left_on='attribute_value', right_on='city_code', how='inner')

# 3) Count students whose joined country equals 'CHINA'
answer = int((student_city['country'] == 'CHINA').sum())

result = answer

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
