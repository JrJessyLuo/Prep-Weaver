import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['DEPARTMENT_CODE','DEPARTMENT_NAME','SUBJECT_CODE','SUBJECT_CODE_DESC','SCHOOL_CODE','SCHOOL_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['DEPARTMENT_CODE','DEPARTMENT_NAME','SUBJECT_CODE','SUBJECT_NUMBER','SUBJECT_ID','HGN_DESC']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_dept_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_subject_offerings = prepared_table_2

# Start from prepared tables
left = prepared_dept_subjects.copy()
right = prepared_subject_offerings.copy()

# Integrate: inner join on both department and subject code to align subjects with their dept mapping
joined = left.merge(right, on=["DEPARTMENT_CODE", "SUBJECT_CODE"], how="inner", suffixes=("_dept", "_subj"))

# Derive course identity to count unique courses per department (use SUBJECT_ID if available; else fallback to SUBJECT_CODE+SUBJECT_NUMBER)
course_id = joined["SUBJECT_ID"].where(joined["SUBJECT_ID"].notna() & (joined["SUBJECT_ID"].astype(str).str.len() > 0), joined["SUBJECT_CODE"].astype(str) + "." + joined["SUBJECT_NUMBER"].astype(str))
joined = joined.assign(_COURSE_ID=course_id)

# Map graduate level flag from HGN_DESC (e.g., 'Graduate' vs 'Undergraduate'); keep the textual level per joined row
joined["GRADUATE_LEVEL"] = joined["HGN_DESC"]

# Aggregate: total number of unique courses per department (across its subject codes)
agg = (
    joined.groupby(["DEPARTMENT_CODE", "DEPARTMENT_NAME", "SUBJECT_CODE", "SUBJECT_CODE_DESC", "GRADUATE_LEVEL"], dropna=False)["_COURSE_ID"]
    .nunique()
    .reset_index(name="TOTAL_COURSES")
)

# Select and sort final columns per request
target = agg[[
    "DEPARTMENT_NAME",
    "SUBJECT_CODE",
    "SUBJECT_CODE_DESC",
    "GRADUATE_LEVEL",
    "TOTAL_COURSES"
]].sort_values(["DEPARTMENT_NAME", "SUBJECT_CODE"])

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
