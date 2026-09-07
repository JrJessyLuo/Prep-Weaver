import pandas as pd
import numpy as np

def _prep_1(table_1):
    cols = ['LIBRARY_SUBJECT_OFFERED_KEY','term_code','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','RESPONSIBLE_FACULTY_NAME','RESPONSIBLE_FACULTY_MIT_ID']
    target = table_1.loc[:, cols].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['LIBRARY_SUBJECT_OFFERED_KEY','LIBRARY_RESERVE_CATALOG_KEY','TERM_CODE','SUBJECT_ID']]
    prepared = prepared.drop_duplicates()
    target = prepared[['LIBRARY_SUBJECT_OFFERED_KEY','LIBRARY_RESERVE_CATALOG_KEY','TERM_CODE','SUBJECT_ID']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME','DEPARTMENT','DATE_FROM','DATE_TO','UNIT_CODE','UNIT']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_4'])
prepared_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_reserves = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_course_instructors = prepared_table_3

# prepared_offerings, prepared_reserves, prepared_course_instructors are assumed to be created per targets above

# Join offerings to reserves to associate reserve materials with offerings
off_res = prepared_offerings.merge(
    prepared_reserves[["LIBRARY_SUBJECT_OFFERED_KEY", "LIBRARY_RESERVE_CATALOG_KEY"]],
    on="LIBRARY_SUBJECT_OFFERED_KEY",
    how="left"
)

# Compute per-department metrics
# Unique courses offered per department: count distinct SUBJECT_ID within department
# Unique reserved materials per department: count distinct LIBRARY_RESERVE_CATALOG_KEY within department
# Unique instructors per department: count distinct RESPONSIBLE_FACULTY_NAME within department
agg = (
    off_res.groupby(["OFFER_DEPT_CODE", "OFFER_DEPT_NAME"], dropna=False)
    .agg(
        unique_courses=("SUBJECT_ID", lambda s: s.dropna().nunique()),
        unique_reserved_materials=("LIBRARY_RESERVE_CATALOG_KEY", lambda s: s.dropna().nunique()),
        unique_instructors=("RESPONSIBLE_FACULTY_NAME", lambda s: s.dropna().nunique())
    )
    .reset_index()
)

# Final selection and sorting
result = (
    agg.rename(columns={
        "OFFER_DEPT_NAME": "department_name",
        "unique_courses": "num_unique_courses",
        "unique_reserved_materials": "num_unique_reserved_materials",
        "unique_instructors": "num_unique_instructors"
    })
    .loc[:, ["department_name", "num_unique_courses", "num_unique_reserved_materials", "num_unique_instructors"]]
    .sort_values(by=["num_unique_courses", "department_name"], ascending=[False, True])
    .reset_index(drop=True)
)

target = result

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
