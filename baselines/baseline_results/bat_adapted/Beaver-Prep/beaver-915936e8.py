import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['ACADEMIC_YEAR','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','SUBJECT_SHORT_TITLE']].copy()
    df['SUBJECT_TITLE'] = df['SUBJECT_TITLE'].astype('string')
    df['SUBJECT_SHORT_TITLE'] = df['SUBJECT_SHORT_TITLE'].astype('string')
    df['SUBJECT_TITLE'] = df['SUBJECT_TITLE'].mask(df['SUBJECT_TITLE'].str.strip().eq('') | df['SUBJECT_TITLE'].isna(), df['SUBJECT_SHORT_TITLE'])
    target = df[['ACADEMIC_YEAR','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','SUBJECT_SHORT_TITLE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['term_code','ACADEMIC_YEAR','FIRST_DAY_OF_CLASSES']].copy()
    prepared['FIRST_DAY_OF_CLASSES'] = pd.to_datetime(prepared['FIRST_DAY_OF_CLASSES'], format='%d-%b-%y', errors='coerce')
    prepared['ACADEMIC_YEAR'] = pd.to_numeric(prepared['ACADEMIC_YEAR'], errors='coerce').astype('Int64')
    target = prepared[['term_code','ACADEMIC_YEAR','FIRST_DAY_OF_CLASSES']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_6'])
prepared_courses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_terms = prepared_table_2

# Merge courses with term calendar to get start dates and ensure academic year alignment
merged = prepared_courses.merge(prepared_terms, left_on='TERM_CODE', right_on='term_code', how='left', suffixes=('', '_term'))

# Choose course name, prefer SUBJECT_TITLE then fallback to SUBJECT_SHORT_TITLE
merged['course_name'] = merged['SUBJECT_TITLE'].fillna(merged['SUBJECT_SHORT_TITLE'])

# Parse FIRST_DAY_OF_CLASSES to datetime for ordering
merged['start_date'] = pd.to_datetime(merged['FIRST_DAY_OF_CLASSES'], errors='coerce', dayfirst=False, infer_datetime_format=True)

# Within each academic year, sort by start date ascending and compute cumulative count
merged = merged.sort_values(['ACADEMIC_YEAR', 'start_date', 'TERM_CODE', 'SUBJECT_ID'])
merged['cumulative_courses_in_year_and_prior'] = merged.groupby('ACADEMIC_YEAR').cumcount() + 1

# Select final columns: course name, building name placeholder (not available in selected tables), cumulative count
# Building name of the course location is not present in the provided tables; leave as None/NaN
result = merged[['course_name', 'ACADEMIC_YEAR', 'start_date', 'cumulative_courses_in_year_and_prior']].copy()
result['building_name'] = pd.NA

# Reorder as requested: course name, building name, cumulative number (partitioned by academic year, ordered by start date)
final_answer = result.sort_values(['ACADEMIC_YEAR', 'start_date'])[['course_name', 'building_name', 'cumulative_courses_in_year_and_prior']]

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
