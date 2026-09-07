import pandas as pd
import numpy as np

def _prep_1(table_1):
    cols = ['SUBJECT_CODE','SUBJECT_CODE_DESC','DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_CODE','SCHOOL_NAME']
    target = table_1[cols].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['DEPARTMENT','DEPARTMENT_NAME','SCHOOL_NAME','COURSE','COURSE_OPTION','COURSE_LEVEL','IS_DEGREE_GRANTING']].copy()
    df['COURSE_OPTION'] = df['COURSE_OPTION'].astype('string').str.strip().replace({'nan': pd.NA, 'NaN': pd.NA, '': pd.NA})
    target = df.drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_subject_catalog = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_degree_catalog = prepared_table_2

# prepared_subject_catalog: from table_1 with selected columns
# prepared_degree_catalog: from table_2 with selected columns

# Integrate catalogs at department within the same school
merged = prepared_subject_catalog.merge(
    prepared_degree_catalog,
    left_on=["DEPARTMENT_CODE", "SCHOOL_NAME"],
    right_on=["DEPARTMENT", "SCHOOL_NAME"],
    how="left",
    indicator=False
)

# For each school, compute:
# - total number of distinct subject codes appearing in the SIS subject code catalog
# - total number of distinct degree-granting courses (from merged rows where IS_DEGREE_GRANTING == 'Y')

# Total subjects per school (from subject catalog only)
subjects_per_school = (
    prepared_subject_catalog.groupby("SCHOOL_NAME")["SUBJECT_CODE"].nunique().reset_index(name="total_subjects_in_catalog")
)

# Degree-granting courses per school (count distinct COURSE where flag is 'Y')
degree_courses_per_school = (
    merged.loc[merged["IS_DEGREE_GRANTING"].eq("Y")]
          .groupby("SCHOOL_NAME")["COURSE"].nunique()
          .reset_index(name="total_degree_granting_courses_in_catalog")
)

# Combine and fill missing degree counts with 0
target = subjects_per_school.merge(
    degree_courses_per_school,
    on="SCHOOL_NAME",
    how="left"
).fillna({"total_degree_granting_courses_in_catalog": 0}).astype({"total_degree_granting_courses_in_catalog": int})

# Final select and rename for clarity
target = target.rename(columns={"SCHOOL_NAME": "school_name"})

# target has columns: school_name, total_subjects_in_catalog, total_degree_granting_courses_in_catalog

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
