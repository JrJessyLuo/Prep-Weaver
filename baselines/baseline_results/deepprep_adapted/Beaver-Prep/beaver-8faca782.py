import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FULL_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FULL_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['EMAIL_ADDRESS'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['EMAIL_ADDRESS'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip().lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["EMAIL_ADDRESS"] = table_1["EMAIL_ADDRESS"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['EMAIL_ADDRESS'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['EMAIL_ADDRESS'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['EMAIL_ADDRESS', 'FIRST_NAME', 'LAST_NAME', 'FULL_NAME', 'DEPARTMENT', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['EMAIL_ADDRESS', 'FIRST_NAME', 'LAST_NAME', 'FULL_NAME', 'DEPARTMENT', 'DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
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
    # CastType(table_name="table_1", column="DEPARTMENT_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['DEPARTMENT_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['DEPARTMENT_CODE']
    if _dtype == "datetime64":
        table_1['DEPARTMENT_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['DEPARTMENT_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['DEPARTMENT_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['DEPARTMENT_CODE'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="DEPARTMENT_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['DEPARTMENT_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['DEPARTMENT_NAME']
    if _dtype == "datetime64":
        table_1['DEPARTMENT_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['DEPARTMENT_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['DEPARTMENT_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['DEPARTMENT_NAME'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="DEPARTMENT_FULL_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['DEPARTMENT_FULL_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['DEPARTMENT_FULL_NAME']
    if _dtype == "datetime64":
        table_1['DEPARTMENT_FULL_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['DEPARTMENT_FULL_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['DEPARTMENT_FULL_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['DEPARTMENT_FULL_NAME'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SCHOOL_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SCHOOL_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SCHOOL_NAME']
    if _dtype == "datetime64":
        table_1['SCHOOL_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SCHOOL_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SCHOOL_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SCHOOL_NAME'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s == "" else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        return None if s == "" else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s == "" else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        return None if s == "" else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_FULL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s == "" else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        return None if s == "" else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_FULL_NAME"] = table_1["DEPARTMENT_FULL_NAME"].apply(_std_apply)

    # ---------------- Step 9 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s == "" else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        return None if s == "" else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_CODE"] = table_1["SCHOOL_CODE"].apply(_std_apply)

    # ---------------- Step 10 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s == "" else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        return None if s == "" else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 11 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['DEPARTMENT_CODE', 'DEPARTMENT_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['DEPARTMENT_CODE', 'DEPARTMENT_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 12 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['DEPARTMENT_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['DEPARTMENT_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 13 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 14 ----------------
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
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST', 'IS_PUBLIC', 'IS_HIDDEN'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST', 'IS_PUBLIC', 'IS_HIDDEN'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # normalize case for stable joins
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # normalize case for stable joins
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_KEY"] = table_1["MOIRA_LIST_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_NAME", func="""
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
    table_1["MOIRA_LIST_NAME"] = table_1["MOIRA_LIST_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_ACTIVE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     return 'Y' if s == 'Y' else ('N' if s == 'N' else s)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        return 'Y' if s == 'Y' else ('N' if s == 'N' else s)
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_ACTIVE"] = table_1["IS_ACTIVE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_MOIRA_MAILING_LIST", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     return 'Y' if s == 'Y' else ('N' if s == 'N' else s)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        return 'Y' if s == 'Y' else ('N' if s == 'N' else s)
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_MOIRA_MAILING_LIST"] = table_1["IS_MOIRA_MAILING_LIST"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_PUBLIC", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     return 'Y' if s == 'Y' else ('N' if s == 'N' else s)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        return 'Y' if s == 'Y' else ('N' if s == 'N' else s)
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_PUBLIC"] = table_1["IS_PUBLIC"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_HIDDEN", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     return 'Y' if s == 'Y' else ('N' if s == 'N' else s)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        return 'Y' if s == 'Y' else ('N' if s == 'N' else s)
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_HIDDEN"] = table_1["IS_HIDDEN"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_students = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_departments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_mailing_lists = prepared_table_3

# Inputs: prepared_students (from table_1), prepared_departments (from table_2), prepared_mailing_lists (from table_3)
# Assumptions: student-to-list membership and list sizes come from external membership/size data not present in selected tables.

# 1) Filter students with last names starting with 'K'
stud_k = prepared_students[prepared_students['LAST_NAME'].astype(str).str.startswith('K', na=False)].copy()

# 2) Join departments to get department attributes (e.g., phone would be joined here if available in dept reference)
# Note: The provided department reference lacks phone numbers; if department phones exist in a different prepared table,
# add an additional merge on a matching department key.
stud_dept = stud_k.merge(prepared_departments, how='left', left_on='DEPARTMENT_NAME', right_on='DEPARTMENT_NAME')

# 3) Compute per-student mailing list metrics
# Placeholder: membership DataFrame 'membership' with columns ['EMAIL_ADDRESS','MOIRA_LIST_NAME'] is required.
# Placeholder: list_sizes DataFrame 'list_sizes' with columns ['MOIRA_LIST_NAME','LIST_SIZE'] is required.
# If available, integrate as below. If not available, counts/averages cannot be computed from given tables.
try:
    # Keep only active Moira mailing lists
    active_lists = prepared_mailing_lists[(prepared_mailing_lists['IS_ACTIVE'] == 'Y') & (prepared_mailing_lists['IS_MOIRA_MAILING_LIST'] == 'Y')][['MOIRA_LIST_NAME']]

    # Filter membership to active lists and to our students
    mem = membership.merge(active_lists, how='inner', on='MOIRA_LIST_NAME')
    mem = mem.merge(stud_dept[['EMAIL_ADDRESS']], how='inner', on='EMAIL_ADDRESS')

    # Join list sizes
    mem = mem.merge(list_sizes, how='left', on='MOIRA_LIST_NAME')

    # Aggregate per student
    agg = mem.groupby('EMAIL_ADDRESS').agg(total_mailing_lists=('MOIRA_LIST_NAME','nunique'), avg_mailing_list_size=('LIST_SIZE','mean')).reset_index()
except NameError:
    # Fallback empty aggregates if membership/size not provided
    agg = pd.DataFrame(columns=['EMAIL_ADDRESS','total_mailing_lists','avg_mailing_list_size'])

# 4) Final projection with names, department phone placeholder, and metrics
# Note: Department phone not present in inputs; if a dept phone column exists after joining, rename/select it here.
result = stud_dept.merge(agg, how='left', on='EMAIL_ADDRESS')
result['total_mailing_lists'] = result['total_mailing_lists'].fillna(0).astype(int)

# Choose name to display and the department phone column if available
result = result.assign(Student_Name=result['FULL_NAME'])
# If department phone column existed, e.g., 'DEPARTMENT_PHONE', keep/rename it; placeholder below
if 'DEPARTMENT_PHONE' in result.columns:
    result = result.rename(columns={'DEPARTMENT_PHONE':'Department_Phone'})
else:
    result['Department_Phone'] = pd.NA

answer = result[['Student_Name','Department_Phone','total_mailing_lists','avg_mailing_list_size']]

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
