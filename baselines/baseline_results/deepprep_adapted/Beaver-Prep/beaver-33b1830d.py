import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COURSE_LEVEL", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip().upper()
    #     # normalize common variants
    #     if s2 in {"UNDERGRAD", "UNDERGRADUATE"}:
    #         return "U"
    #     if s2 in {"GRAD", "GRADUATE"}:
    #         return "G"
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s2 = str(s).strip().upper()
        # normalize common variants
        if s2 in {"UNDERGRAD", "UNDERGRADUATE"}:
            return "U"
        if s2 in {"GRAD", "GRADUATE"}:
            return "G"
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["COURSE_LEVEL"] = table_1["COURSE_LEVEL"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_DEGREE_GRANTING", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip().upper()
    #     if s2 in {"Y", "YES", "TRUE", "T", "1"}:
    #         return "Y"
    #     if s2 in {"N", "NO", "FALSE", "F", "0"}:
    #         return "N"
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s2 = str(s).strip().upper()
        if s2 in {"Y", "YES", "TRUE", "T", "1"}:
            return "Y"
        if s2 in {"N", "NO", "FALSE", "F", "0"}:
            return "N"
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_DEGREE_GRANTING"] = table_1["IS_DEGREE_GRANTING"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['DEPARTMENT', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['DEPARTMENT', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING'] if c in table_1.columns]
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
    # MissingValueImputation(table_name="table_1", column_name="SCHOOL_CODE", mode="mode")
    # MissingValueImputation
    table_1["SCHOOL_CODE"] = table_1["SCHOOL_CODE"].fillna(table_1["SCHOOL_CODE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="department_full_name", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["department_full_name"] = table_1["department_full_name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
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
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['DEPARTMENT_CODE', 'SCHOOL_CODE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['DEPARTMENT_CODE', 'SCHOOL_CODE'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['DEPARTMENT_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['DEPARTMENT_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT_CODE', 'department_full_name', 'SCHOOL_CODE', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_CODE', 'department_full_name', 'SCHOOL_CODE', 'SCHOOL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_courses_by_dept_level = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_department_lookup = prepared_table_2

integrated = prepared_courses_by_dept_level.merge(prepared_department_lookup, left_on='DEPARTMENT', right_on='DEPARTMENT_CODE', how='left')
# Normalize degree-granting flag
integrated['is_deg'] = (integrated['IS_DEGREE_GRANTING'].astype(str).str.upper() == 'Y')
# Aggregate by school code, school name, department full name, and course level
answer = (
    integrated.groupby(['SCHOOL_CODE', 'SCHOOL_NAME_y', 'department_full_name', 'COURSE_LEVEL'], dropna=False)
    .agg(total_courses=('COURSE_LEVEL', 'size'), total_degree_granting=('is_deg', 'sum'))
    .reset_index()
)
# Rename SCHOOL_NAME_y to SCHOOL_NAME if merge produced suffixes
if 'SCHOOL_NAME_y' in answer.columns:
    answer = answer.rename(columns={'SCHOOL_NAME_y': 'SCHOOL_NAME'})
# Final selected columns in required order
answer = answer[['SCHOOL_CODE', 'SCHOOL_NAME', 'department_full_name', 'COURSE_LEVEL', 'total_courses', 'total_degree_granting']]

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
