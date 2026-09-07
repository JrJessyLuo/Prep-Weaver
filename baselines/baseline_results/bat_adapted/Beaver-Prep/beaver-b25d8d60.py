import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME','COURSE_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_MATERIAL_STATUS_KEY','TERM_CODE']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_MATERIAL_STATUS_KEY','TERM_CODE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1[['SUBJECT_ID','TERM_CODE','ACADEMIC_YEAR']].copy()
    df = df.dropna(subset=['SUBJECT_ID','TERM_CODE','ACADEMIC_YEAR'])
    df['ACADEMIC_YEAR'] = df['ACADEMIC_YEAR'].astype('int64')
    target = df.drop_duplicates(subset=['SUBJECT_ID','TERM_CODE','ACADEMIC_YEAR'])[['SUBJECT_ID','TERM_CODE','ACADEMIC_YEAR']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_instructors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_material_assignments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_table_4 = _prep_4(tables['table_3'])
prepared_subject_terms = prepared_table_4

# Merge instructors with material assignments
m = prepared_instructors.merge(
    prepared_material_assignments,
    on='LIBRARY_COURSE_INSTRUCTOR_KEY',
    how='left'
)

# If SUBJECT_ID is not present in prepared_material_assignments, attempt to derive it from LIBRARY_COURSE_INSTRUCTOR_KEY prefix before ':'
if 'SUBJECT_ID' not in m.columns or m['SUBJECT_ID'].isna().all():
    # Example LIBRARY_COURSE_INSTRUCTOR_KEY looks like '4.602-VANCE2010SP:4.602'
    # Prefer the segment after the colon if present; else take leading subject-like token
    subj_after_colon = m['LIBRARY_COURSE_INSTRUCTOR_KEY'].str.split(':').str[-1]
    m['SUBJECT_ID'] = subj_after_colon

# Join to subject terms on SUBJECT_ID and TERM_CODE to get academic year
m = m.merge(
    prepared_subject_terms[['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR']],
    on=['SUBJECT_ID', 'TERM_CODE'],
    how='left'
)

# Aggregate per instructor
agg = m.groupby('INSTRUCTOR_NAME').agg(
    unique_courses=('COURSE_NAME', lambda s: s.dropna().nunique()),
    total_material_assignments=('LIBRARY_RESERVE_CATALOG_KEY', 'count'),
    avg_publication_year=('ACADEMIC_YEAR', 'mean'),
    distinct_status=('LIBRARY_MATERIAL_STATUS_KEY', lambda s: s.dropna().nunique())
).reset_index()

# Final formatting and sorting
agg['avg_publication_year'] = agg['avg_publication_year'].round(2)
result = agg.sort_values(['unique_courses', 'INSTRUCTOR_NAME'], ascending=[False, True])

target = result[['INSTRUCTOR_NAME', 'unique_courses', 'total_material_assignments', 'avg_publication_year', 'distinct_status']]

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
