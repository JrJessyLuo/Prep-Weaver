import pandas as pd
import numpy as np

def _prep_1(table_1):
    cols = ['ACADEMIC_YEAR','SUBJECT_CODE','SUBJECT_NUMBER','subject_id','SUBJECT_TITLE','GRADE_TYPE','HGN_CODE']
    df = table_1[cols].copy()
    df = df.replace({"nan": pd.NA})
    df = df.groupby(['ACADEMIC_YEAR','SUBJECT_CODE','SUBJECT_NUMBER','subject_id'], as_index=False).agg({'SUBJECT_TITLE': lambda s: s.dropna().iloc[0] if s.notna().any() else pd.NA, 'GRADE_TYPE': lambda s: s.dropna().iloc[0] if s.notna().any() else pd.NA, 'HGN_CODE': lambda s: s.dropna().iloc[0] if s.notna().any() else pd.NA})
    target = df[['ACADEMIC_YEAR','SUBJECT_CODE','SUBJECT_NUMBER','subject_id','SUBJECT_TITLE','GRADE_TYPE','HGN_CODE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    source = table_1[['SUBJECT_ID','SUBJECT_TITLE','TERM_CODE','RESPONSIBLE_FACULTY_NAME','FORM_TYPE','FORM_TYPE_DESC','OFFER_DEPT_CODE','OFFER_DEPT_NAME']].copy()
    source = source.drop_duplicates()
    target = source[['SUBJECT_ID','SUBJECT_TITLE','TERM_CODE','RESPONSIBLE_FACULTY_NAME','FORM_TYPE','FORM_TYPE_DESC','OFFER_DEPT_CODE','OFFER_DEPT_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subject_catalog = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_subject_offerings = prepared_table_2

# Assume prepared_subject_catalog and prepared_subject_offerings are dataframes synthesized per target schemas.

# 1) Integrate catalog with offerings on subject_id keys
integrated = prepared_subject_catalog.merge(
    prepared_subject_offerings,
    left_on="subject_id",
    right_on="SUBJECT_ID",
    how="inner"
)

# 2) Filter for academic year 2022 and valid instructor names
filtered = integrated[(integrated["ACADEMIC_YEAR"] == 2022) & (~integrated["RESPONSIBLE_FACULTY_NAME"].isna()) & (integrated["RESPONSIBLE_FACULTY_NAME"].astype(str).str.strip() != "")]

# 3) Derive course type. Prefer FORM_TYPE_DESC when available, else FORM_TYPE, else fallback to non-null SUBJECT_TITLE grouping if needed
course_type = (
    filtered["FORM_TYPE_DESC"].where(filtered["FORM_TYPE_DESC"].notna(), filtered["FORM_TYPE"])
)
filtered = filtered.assign(COURSE_TYPE=course_type)

# 4) Aggregate: total number of distinct types of courses per instructor in AY 2022
agg = (
    filtered.groupby(["ACADEMIC_YEAR", "RESPONSIBLE_FACULTY_NAME"])\
        ["COURSE_TYPE"].nunique(dropna=True)\
        .reset_index(name="total_course_types")
)

# 5) Select output columns
target = agg[["ACADEMIC_YEAR", "RESPONSIBLE_FACULTY_NAME", "total_course_types"]]

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
