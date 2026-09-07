import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FULL_NAME", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     s = re.sub(r'\.+$', '.', s)  # normalize trailing dots
    #     s = re.sub(r'\s*\.\s*$', '.', s)  # ensure single final dot if present
    #     s = re.sub(r'\s*,\s*', ', ', s)  # normalize comma spacing
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        s = re.sub(r'\.+$', '.', s)  # normalize trailing dots
        s = re.sub(r'\s*\.\s*$', '.', s)  # ensure single final dot if present
        s = re.sub(r'\s*,\s*', ', ', s)  # normalize comma spacing
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FULL_NAME"] = table_1["FULL_NAME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['DEPARTMENT_NAME', 'FULL_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['DEPARTMENT_NAME', 'FULL_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT_NAME', 'FULL_NAME'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_NAME', 'FULL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SIS_ADMIN_DEPARTMENT_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SIS_ADMIN_DEPARTMENT_NAME'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="department_phone_number", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['department_phone_number'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['department_phone_number']
    if _dtype == "datetime64":
        table_1['department_phone_number'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['department_phone_number'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['department_phone_number'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['department_phone_number'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="department_phone_number", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     # Treat pandas missing markers
    #     if isinstance(s, float) and pd.isna(s):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     # Remove trailing .0 from values like 2683470.0
    #     if s.endswith(".0"):
    #         s = s[:-2]
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        # Treat pandas missing markers
        if isinstance(s, float) and pd.isna(s):
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        # Remove trailing .0 from values like 2683470.0
        if s.endswith(".0"):
            s = s[:-2]
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["department_phone_number"] = table_1["department_phone_number"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SIS_ADMIN_DEPARTMENT_NAME', 'department_phone_number'])
    # SelectCol
    _cols = [c for c in ['SIS_ADMIN_DEPARTMENT_NAME', 'department_phone_number'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_students = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_departments = prepared_table_2

# Assume prepared_students and prepared_departments already materialized as per target schemas
# 1) Integrate on department name
merged = prepared_students.merge(
    prepared_departments,
    left_on='DEPARTMENT_NAME',
    right_on='SIS_ADMIN_DEPARTMENT_NAME',
    how='left'
)

# 2) Compute per-department aggregates
# Name length based on FULL_NAME string length
merged['name_len'] = merged['FULL_NAME'].fillna('').str.len()

gb = merged.groupby(['DEPARTMENT_NAME', 'department_phone_number'], dropna=False)
result = gb.agg(
    number_of_students=('FULL_NAME', 'count'),
    longest_full_name_length=('name_len', 'max')
).reset_index()

# 3) Rename columns to match requested output semantics
result = result.rename(columns={
    'DEPARTMENT_NAME': 'department_name',
    'department_phone_number': 'department_phone_number'
})

# Final output in result with columns: department_name, department_phone_number, number_of_students, longest_full_name_length
output = result[['department_name', 'department_phone_number', 'number_of_students', 'longest_full_name_length']]

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
