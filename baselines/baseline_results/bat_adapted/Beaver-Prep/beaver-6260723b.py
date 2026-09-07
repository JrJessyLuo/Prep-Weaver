import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['term_code','TERM_DESCRIPTION','ACADEMIC_YEAR']].copy()
    prepared = prepared.drop_duplicates(subset=['term_code','TERM_DESCRIPTION','ACADEMIC_YEAR'])
    target = prepared[['term_code','TERM_DESCRIPTION','ACADEMIC_YEAR']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','PREREQUISITES']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','RESPONSIBLE_FACULTY_NAME']].copy()
    df = df.replace({'nan': pd.NA, 'NaN': pd.NA, '': pd.NA})
    df['SUBJECT_TITLE'] = df['SUBJECT_TITLE'].astype('string')
    df['RESPONSIBLE_FACULTY_NAME'] = df['RESPONSIBLE_FACULTY_NAME'].astype('string')
    agg = df.groupby(['TERM_CODE','SUBJECT_ID'], as_index=False).agg({'SUBJECT_TITLE': lambda s: s.dropna().iloc[0] if s.dropna().size else pd.NA, 'RESPONSIBLE_FACULTY_NAME': lambda s: s.dropna().iloc[0] if s.dropna().size else pd.NA})
    target = agg[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','RESPONSIBLE_FACULTY_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_5'])
prepared_terms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_subjects = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_offerings = prepared_table_3

# Assume prepared_terms, prepared_subjects, prepared_offerings are dataframes synthesized per targets
# 1) Filter to 2023 Fall term code (e.g., '2023FA')
fa23_code = '2023FA'

# Join offerings with subjects on (TERM_CODE, SUBJECT_ID)
off_sub = prepared_offerings.merge(
    prepared_subjects,
    on=["TERM_CODE", "SUBJECT_ID"],
    how="inner",
    suffixes=("_off", "_sub")
)

# Bring in term description
joined = off_sub.merge(
    prepared_terms.rename(columns={"term_code": "TERM_CODE"}),
    on="TERM_CODE",
    how="left"
)

# Filter to Fall 2023
fa23 = joined[joined["TERM_CODE"] == fa23_code].copy()

# Unique term descriptions
unique_term_descriptions = sorted(fa23["TERM_DESCRIPTION"].dropna().unique().tolist())

# Subject titles with their prerequisites for Fall 2023
subjects_with_prereqs = (
    fa23[["SUBJECT_TITLE_sub", "PREREQUISITES"]]
      .drop_duplicates()
      .rename(columns={"SUBJECT_TITLE_sub": "SUBJECT_TITLE"})
)

# Total number of types of subjects per term code (for 2023FA)
subjects_per_term = (
    fa23.groupby("TERM_CODE")["SUBJECT_ID"].nunique().reset_index(name="num_subject_types")
)

# Instructor(s) of this course (from offerings in 2023FA)
instructors_fa23 = (
    fa23["RESPONSIBLE_FACULTY_NAME"]
      .dropna()
      .drop_duplicates()
      .tolist()
)

# Number of types of courses ever taught by the instructor: count distinct SUBJECT_ID per instructor across all terms
instructor_course_counts = (
    joined.dropna(subset=["RESPONSIBLE_FACULTY_NAME"]) 
          .groupby("RESPONSIBLE_FACULTY_NAME")["SUBJECT_ID"].nunique()
          .reset_index(name="num_course_types_ever")
)

# For the instructors present in Fall 2023, get their overall counts
instructor_counts_fa23 = instructor_course_counts[
    instructor_course_counts["RESPONSIBLE_FACULTY_NAME"].isin(instructors_fa23)
]

# Package results
target = {
    "unique_term_descriptions": unique_term_descriptions,
    "subjects_with_prereqs": subjects_with_prereqs,
    "subjects_per_term": subjects_per_term,
    "instructors_fa23": instructors_fa23,
    "instructor_course_type_counts": instructor_counts_fa23,
}

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
