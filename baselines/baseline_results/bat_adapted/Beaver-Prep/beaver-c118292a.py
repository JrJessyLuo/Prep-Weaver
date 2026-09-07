import pandas as pd
import numpy as np

def _prep_1(table_1):
    source = table_1[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','RESPONSIBLE_FACULTY_NAME','responsible_faculty_mit_id']].copy()
    source['RESPONSIBLE_FACULTY_NAME'] = source['RESPONSIBLE_FACULTY_NAME'].replace('nan', pd.NA)
    source['responsible_faculty_mit_id'] = source['responsible_faculty_mit_id'].replace('nan', pd.NA)
    target = source.drop_duplicates()[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','RESPONSIBLE_FACULTY_NAME','responsible_faculty_mit_id']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_7'])
prepared_subject_offerings = prepared_table_1

# Start from the prepared table
subjects = prepared_subject_offerings.copy()

# Identify fall term rows. Assuming TERM_CODE encodes year+term where 'FA' or similar marks fall.
# If fall is encoded differently (e.g., '2012FA' or '2012F'), adjust the pattern accordingly.
fall_mask = subjects['TERM_CODE'].astype(str).str.contains('FA', case=False, na=False)
fall_subjects = subjects.loc[fall_mask].copy()

# Keep unique subjects by SUBJECT_ID and TERM_CODE, preserving title and instructor
fall_unique = (
    fall_subjects
    .dropna(subset=['SUBJECT_ID', 'SUBJECT_TITLE'])
    .drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID'])
)

# Compute total number of unique subject types (unique SUBJECT_IDs) per instructor
counts_per_instructor = (
    fall_unique
    .dropna(subset=['RESPONSIBLE_FACULTY_NAME'])
    .groupby(['RESPONSIBLE_FACULTY_NAME'], dropna=True)['SUBJECT_ID']
    .nunique()
    .reset_index(name='total_subject_types_per_instructor')
)

# Attach counts back to each subject row
result = fall_unique.merge(counts_per_instructor, on='RESPONSIBLE_FACULTY_NAME', how='left')

# Select and rename final columns; email not available in this table, set as None
result['instructor_email'] = None
answer = result[['SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME', 'instructor_email', 'total_subject_types_per_instructor']].drop_duplicates()

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
