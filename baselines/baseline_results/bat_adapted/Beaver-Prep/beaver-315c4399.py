import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['ACADEMIC_YEAR','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['ACADEMIC_YEAR','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['term_code','ACADEMIC_YEAR','FIRST_DAY_OF_CLASSES','LAST_DAY_OF_CLASSES']].copy()
    prepared['FIRST_DAY_OF_CLASSES'] = pd.to_datetime(prepared['FIRST_DAY_OF_CLASSES'].replace({'nan': pd.NA, 'NaN': pd.NA, '': pd.NA}), format='%d-%b-%y', errors='coerce')
    prepared['LAST_DAY_OF_CLASSES'] = pd.to_datetime(prepared['LAST_DAY_OF_CLASSES'].replace({'nan': pd.NA, 'NaN': pd.NA, '': pd.NA}), format='%d-%b-%y', errors='coerce')
    prepared['ACADEMIC_YEAR'] = pd.to_numeric(prepared['ACADEMIC_YEAR'], errors='coerce').astype('Int64')
    target = prepared[['term_code','ACADEMIC_YEAR','FIRST_DAY_OF_CLASSES','LAST_DAY_OF_CLASSES']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_7'])
prepared_courses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_terms = prepared_table_2

# Assume prepared_courses and prepared_terms are provided as per the target schemas
# 1) Join courses to terms on term code
joined = prepared_courses.merge(prepared_terms, left_on='TERM_CODE', right_on='term_code', how='inner', suffixes=('', '_term'))

# 2) Parse dates and compute duration in days (inclusive of both endpoints if desired; here use difference in days + 1)
for col in ['FIRST_DAY_OF_CLASSES', 'LAST_DAY_OF_CLASSES']:
    joined[col] = pd.to_datetime(joined[col], errors='coerce')

joined['duration_days'] = (joined['LAST_DAY_OF_CLASSES'] - joined['FIRST_DAY_OF_CLASSES']).dt.days + 1

# 3) Compute running average over window of 2 preceding and 2 following courses within academic year ordered by course start date
joined = joined.sort_values(['ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES', 'SUBJECT_ID'])
rolling_avg = (
    joined
    .groupby('ACADEMIC_YEAR', group_keys=False)['duration_days']
    .apply(lambda s: s.rolling(window=5, min_periods=1, center=True).mean())
)
joined['running_avg_duration_days'] = rolling_avg

# 4) Select required output columns
result = joined[['SUBJECT_TITLE', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES', 'duration_days', 'running_avg_duration_days']]
result = result.rename(columns={
    'SUBJECT_TITLE': 'course_title',
    'FIRST_DAY_OF_CLASSES': 'course_start_date'
})

# The final answer expects: for each course: title, building of the course location, duration (days), and running average.
# Note: The selected tables do not include a building/location column. If building info exists in other tables, it must be joined there.
# For now, produce without building, or fill as NaN to indicate missing from provided sources.
result['building_name'] = pd.NA
result = result[['course_title', 'building_name', 'duration_days', 'running_avg_duration_days', 'ACADEMIC_YEAR', 'course_start_date']]

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
