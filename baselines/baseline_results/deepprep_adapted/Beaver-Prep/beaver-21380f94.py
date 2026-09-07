import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['EMAIL_ADDRESS', 'FULL_NAME'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['EMAIL_ADDRESS', 'FULL_NAME'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.lower() if s else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.lower() if s else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["EMAIL_ADDRESS"] = table_1["EMAIL_ADDRESS"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FULL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FULL_NAME"] = table_1["FULL_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['EMAIL_ADDRESS', 'FULL_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['EMAIL_ADDRESS', 'FULL_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['EMAIL_ADDRESS', 'FULL_NAME', 'STUDENT_YEAR', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['EMAIL_ADDRESS', 'FULL_NAME', 'STUDENT_YEAR', 'DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
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
    # Sort(table_name="table_1", by=['SCHOOL_CODE', 'DEPARTMENT_NAME'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['SCHOOL_CODE', 'DEPARTMENT_NAME'], ascending=[True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT_NAME', 'DEPARTMENT_CODE', 'SCHOOL_CODE', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_NAME', 'DEPARTMENT_CODE', 'SCHOOL_CODE', 'SCHOOL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['DEPARTMENT_NAME', 'DEPARTMENT_CODE', 'SCHOOL_CODE', 'SCHOOL_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['DEPARTMENT_NAME', 'DEPARTMENT_CODE', 'SCHOOL_CODE', 'SCHOOL_NAME'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['SCHOOL_CODE', 'DEPARTMENT_NAME'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['SCHOOL_CODE', 'DEPARTMENT_NAME'], ascending=[True, True])

    # ---------------- Step 7 ----------------
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

prepared_table_1 = _prep_1(tables['table_7'])
prepared_duo_users = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_departments = prepared_table_2

# prepared_duo_users and prepared_departments are the synthesized per-table outputs

# 1) Identify students in the duo mailing list (assuming STUDENT_YEAR non-null/non-empty denotes a student)
students = prepared_duo_users.copy()
students['STUDENT_YEAR'] = students['STUDENT_YEAR'].astype(str).str.strip()
students = students[students['STUDENT_YEAR'].notna() & (students['STUDENT_YEAR'] != '')]

# 2) Join to department-school mapping on department name
joined = students.merge(
    prepared_departments,
    how='left',
    left_on='DEPARTMENT_NAME',
    right_on='DEPARTMENT_NAME'
)

# 3) Compute required counts
num_students = students['EMAIL_ADDRESS'].nunique()
num_departments = joined['DEPARTMENT_NAME'].nunique()
num_schools = joined['SCHOOL_NAME'].dropna().nunique()

answer = {
    'num_students_in_mailing_list': int(num_students),
    'num_departments_for_these_students': int(num_departments),
    'num_schools_for_these_students': int(num_schools)
}

target = pd.DataFrame([answer])

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
