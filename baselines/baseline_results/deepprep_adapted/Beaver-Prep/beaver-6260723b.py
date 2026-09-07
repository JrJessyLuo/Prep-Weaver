import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['ACADEMIC_TERMS_KEY', 'TERM_SELECTOR', 'TERM_START_DATE', 'TERM_END_DATE', 'ACADEMIC_YEAR_DESC', 'IS_CURRENT_TERM', 'TERM_STATUS_INDICATOR', 'FINANCIAL_AID_YEAR', 'DEGREE_YEAR', 'LAST_DAY_OF_FINAL_EXAM', 'PRE_REGISTRATION_START_DAY', 'REGISTRATION_DAY', 'FIRST_DAY_OF_CLASSES', 'LAST_DAY_OF_CLASSES', 'GRADUATE_AWARD_START_DATE', 'GRADUATE_AWARD_END_DATE', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['ACADEMIC_TERMS_KEY', 'TERM_SELECTOR', 'TERM_START_DATE', 'TERM_END_DATE', 'ACADEMIC_YEAR_DESC', 'IS_CURRENT_TERM', 'TERM_STATUS_INDICATOR', 'FINANCIAL_AID_YEAR', 'DEGREE_YEAR', 'LAST_DAY_OF_FINAL_EXAM', 'PRE_REGISTRATION_START_DAY', 'REGISTRATION_DAY', 'FIRST_DAY_OF_CLASSES', 'LAST_DAY_OF_CLASSES', 'GRADUATE_AWARD_START_DATE', 'GRADUATE_AWARD_END_DATE', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # Keep 2023 Fall terms; term_code commonly ends with 'FA' for Fall
    #     desc = str(row['TERM_DESCRIPTION']) if row['TERM_DESCRIPTION'] is not None else ''
    #     code = str(row['term_code']) if row['term_code'] is not None else ''
    #     return (row['ACADEMIC_YEAR'] == 2023) and (code.upper().endswith('FA') or ('FALL' in desc.upper()))
    # """)
    # Filter
    def filter_func(row):
        # Keep 2023 Fall terms; term_code commonly ends with 'FA' for Fall
        desc = str(row['TERM_DESCRIPTION']) if row['TERM_DESCRIPTION'] is not None else ''
        code = str(row['term_code']) if row['term_code'] is not None else ''
        return (row['ACADEMIC_YEAR'] == 2023) and (code.upper().endswith('FA') or ('FALL' in desc.upper()))
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['term_code', 'TERM_DESCRIPTION', 'ACADEMIC_YEAR'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['term_code', 'TERM_DESCRIPTION', 'ACADEMIC_YEAR'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['term_code', 'TERM_DESCRIPTION', 'ACADEMIC_YEAR'])
    # SelectCol
    _cols = [c for c in ['term_code', 'TERM_DESCRIPTION', 'ACADEMIC_YEAR'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TERM_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TERM_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TERM_CODE']
    if _dtype == "datetime64":
        table_1['TERM_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TERM_CODE'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'PREREQUISITES'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'PREREQUISITES'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return None if s.lower() in {"nan", "none", ""} else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return None if s.lower() in {"nan", "none", ""} else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s.lower() in {"nan", "none", ""} else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        return None if s.lower() in {"nan", "none", ""} else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s.lower() in {"nan", "none", ""} else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        return None if s.lower() in {"nan", "none", ""} else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="RESPONSIBLE_FACULTY_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s.lower() in {"nan", "none", ""} else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        return None if s.lower() in {"nan", "none", ""} else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["RESPONSIBLE_FACULTY_NAME"] = table_1["RESPONSIBLE_FACULTY_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
