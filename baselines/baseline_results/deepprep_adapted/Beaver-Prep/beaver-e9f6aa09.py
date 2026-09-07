import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SCHOOL_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SCHOOL_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SCHOOL_CODE']
    if _dtype == "datetime64":
        table_1['SCHOOL_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SCHOOL_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SCHOOL_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SCHOOL_CODE'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_CODE"] = table_1["SUBJECT_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_CODE"] = table_1["SCHOOL_CODE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_CODE_DESC", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_CODE_DESC"] = table_1["SUBJECT_CODE_DESC"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SUBJECT_CODE', 'DEPARTMENT_CODE', 'SCHOOL_CODE'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SUBJECT_CODE', 'DEPARTMENT_CODE', 'SCHOOL_CODE'], keep='first').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
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
    # MissingValueImputation(table_name="table_1", column_name="COURSE_OPTION", mode="mode")
    # MissingValueImputation
    table_1["COURSE_OPTION"] = table_1["COURSE_OPTION"].fillna(table_1["COURSE_OPTION"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'COURSE', 'COURSE_OPTION', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'COURSE', 'COURSE_OPTION', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['DEPARTMENT', 'COURSE', 'COURSE_OPTION', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['DEPARTMENT', 'COURSE', 'COURSE_OPTION', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['SCHOOL_NAME', 'DEPARTMENT', 'COURSE', 'COURSE_LEVEL', 'COURSE_OPTION'], ascending=[True, True, True, True, True])
    # Sort
    table_1 = table_1.sort_values(by=['SCHOOL_NAME', 'DEPARTMENT', 'COURSE', 'COURSE_LEVEL', 'COURSE_OPTION'], ascending=[True, True, True, True, True])

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
