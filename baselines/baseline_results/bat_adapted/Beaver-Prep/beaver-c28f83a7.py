import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['LIBRARY_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','LIBRARY_RESERVE_CATALOG_KEY']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['LIBRARY_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','LIBRARY_RESERVE_CATALOG_KEY']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1.copy()
    prepared['LIBRARY_SUBJECT_OFFERED_KEY'] = prepared['LIBRARY_SUBJECT_OFFERED_KEY'].astype(str).str.strip()
    target = prepared[['LIBRARY_SUBJECT_OFFERED_KEY','term_code','SUBJECT_ID','OFFER_DEPT_NAME','NUM_ENROLLED_STUDENTS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_6'])
prepared_reserve_links = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_course_offerings = prepared_table_2

# prepared_reserve_links and prepared_course_offerings are the synthesized per-table outputs
links = prepared_reserve_links.copy()
courses = prepared_course_offerings.copy()

# Normalize course key whitespace if needed
for df, col in [(links, 'LIBRARY_SUBJECT_OFFERED_KEY'), (courses, 'LIBRARY_SUBJECT_OFFERED_KEY')]:
    df[col] = df[col].astype(str).str.strip()

# Join reserves to course metadata
joined = links.merge(
    courses,
    how='inner',
    left_on='LIBRARY_SUBJECT_OFFERED_KEY',
    right_on='LIBRARY_SUBJECT_OFFERED_KEY'
)

# Compute per-course metrics first
# - courses_using_materials: count distinct course keys that appear in reserves (will be 1 per course in this per-course table)
# - catalog_items_per_course: count distinct catalog item keys per course
per_course = (
    joined.groupby(['LIBRARY_SUBJECT_OFFERED_KEY', 'OFFER_DEPT_NAME'], as_index=False)
          .agg(
              catalog_items_per_course=('LIBRARY_RESERVE_CATALOG_KEY', 'nunique'),
              avg_enrollment_course=('NUM_ENROLLED_STUDENTS', 'first')
          )
)
# Mark each course that uses materials (presence in joined implies usage)
per_course['courses_using_materials'] = 1

# Aggregate to department level
by_dept = (
    per_course.groupby('OFFER_DEPT_NAME', as_index=False)
              .agg(
                  total_courses_using_materials=('courses_using_materials', 'sum'),
                  total_catalog_items=('catalog_items_per_course', 'sum'),
                  avg_enrollment_per_course=('avg_enrollment_course', 'mean')
              )
)
by_dept = by_dept.rename(columns={'OFFER_DEPT_NAME': 'Department'})

# Compute grand total across all departments
grand = pd.DataFrame({
    'Department': ['Grand Total'],
    'total_courses_using_materials': [per_course['courses_using_materials'].sum()],
    'total_catalog_items': [per_course['catalog_items_per_course'].sum()],
    'avg_enrollment_per_course': [per_course['avg_enrollment_course'].mean()]
})

# Final result with department rows plus grand total
target = pd.concat([by_dept, grand], ignore_index=True)

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
