import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','OFFER_DEPT_CODE','OFFER_SCHOOL_NAME','COURSE_NUMBER','SUBJECT_TITLE','SUBJECT_ID','NUM_ENROLLED_STUDENTS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['SUBJECT_ID'] = df['subject_id'].astype(str).str.strip()
    df['TERM_CODE'] = df['TERM_CODE'].astype(str).str.strip()
    df['ISBN'] = df['ISBN'].astype(str).str.strip()
    df = df[~df['SUBJECT_ID'].isin(['', 'nan', 'None', 'NaN'])]
    df = df[~df['ISBN'].isin(['', 'nan', 'None', 'NaN'])]
    target = df[['SUBJECT_ID', 'TERM_CODE', 'ISBN']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_materials = prepared_table_2

# Assume prepared_offerings and prepared_materials already materialized per targets.
# Standardize key casing/whitespace
prepared_offerings['SUBJECT_ID'] = prepared_offerings['SUBJECT_ID'].astype(str).str.strip()
prepared_materials['SUBJECT_ID'] = prepared_materials['SUBJECT_ID'].astype(str).str.strip()
prepared_offerings['TERM_CODE'] = prepared_offerings['TERM_CODE'].astype(str).str.strip()
prepared_materials['TERM_CODE'] = prepared_materials['TERM_CODE'].astype(str).str.strip()

# Join on SUBJECT_ID and TERM_CODE to align materials with offerings in the same term
merged = prepared_offerings.merge(
    prepared_materials,
    how='left',
    left_on=['SUBJECT_ID', 'TERM_CODE'],
    right_on=['SUBJECT_ID', 'TERM_CODE']
)

# Compute distinct ISBNs per offering (excluding null/blank)
merged['ISBN_clean'] = merged['ISBN'].where(merged['ISBN'].notna() & (merged['ISBN'].astype(str).str.strip() != ''), pd.NA)

agg = (
    merged.groupby([
        'OFFER_DEPT_CODE', 'OFFER_SCHOOL_NAME', 'COURSE_NUMBER', 'SUBJECT_TITLE', 'TERM_CODE'
    ], dropna=False)
    .agg(
        total_enrolled=('NUM_ENROLLED_STUDENTS', 'first'),  # enrollment is per offering row
        distinct_catalog_isbns=('ISBN_clean', pd.Series.nunique)
    )
    .reset_index()
)

# Build summary row for current term (assume current term = max TERM_CODE present in offerings)
current_term = prepared_offerings['TERM_CODE'].dropna().astype(str).max()
cur = merged[merged['TERM_CODE'] == current_term]
cur_total_students = cur.drop_duplicates(['SUBJECT_ID', 'TERM_CODE'])['NUM_ENROLLED_STUDENTS'].sum()
cur_distinct_isbns = cur['ISBN_clean'].nunique()

summary_row = pd.DataFrame([
    {
        'OFFER_DEPT_CODE': 'TOTAL:',
        'OFFER_SCHOOL_NAME': None,
        'COURSE_NUMBER': None,
        'SUBJECT_TITLE': None,
        'total_enrolled': int(cur_total_students),
        'TERM_CODE': None,
        'distinct_catalog_isbns': int(cur_distinct_isbns)
    }
])

# Final result with requested columns
result = agg.rename(columns={
    'OFFER_DEPT_CODE': 'department',
    'OFFER_SCHOOL_NAME': 'school',
    'COURSE_NUMBER': 'course_number',
    'SUBJECT_TITLE': 'subject_title',
    'TERM_CODE': 'term_code',
    'total_enrolled': 'total_number_of_enrolled_students',
    'distinct_catalog_isbns': 'count_of_distinct_catalog_isbns'
})

summary_out = summary_row.rename(columns={
    'OFFER_DEPT_CODE': 'department',
    'OFFER_SCHOOL_NAME': 'school',
    'COURSE_NUMBER': 'course_number',
    'SUBJECT_TITLE': 'subject_title',
    'TERM_CODE': 'term_code',
    'total_enrolled': 'total_number_of_enrolled_students',
    'distinct_catalog_isbns': 'count_of_distinct_catalog_isbns'
})

final = pd.concat([result, summary_out], ignore_index=True)

final = final[['department', 'school', 'course_number', 'subject_title', 'total_number_of_enrolled_students', 'term_code', 'count_of_distinct_catalog_isbns']]

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
