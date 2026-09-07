import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="DEPARTMENT", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['DEPARTMENT'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['DEPARTMENT']
    if _dtype == "datetime64":
        table_1['DEPARTMENT'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['DEPARTMENT'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['DEPARTMENT'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['DEPARTMENT'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        return s.lower()
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
    # StandardizeString(table_name="table_1", column_name="FIRST_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FIRST_NAME"] = table_1["FIRST_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MIDDLE_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MIDDLE_NAME"] = table_1["MIDDLE_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LAST_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["LAST_NAME"] = table_1["LAST_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FULL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FULL_NAME"] = table_1["FULL_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().strip('"').strip("'")
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
    # Deduplicate(table_name="table_1", subset=['EMAIL_ADDRESS'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['EMAIL_ADDRESS'], keep='last').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'EMAIL_ADDRESS', 'DEPARTMENT', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'EMAIL_ADDRESS', 'DEPARTMENT', 'DEPARTMENT_NAME'] if c in table_1.columns]
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     val = row.get('IS_DEGREE_GRANTING', None)
    #     return val is None or str(val).strip().upper() in ['Y','YES','TRUE','T','1']
    # """)
    # Filter
    def filter_func(row):
        val = row.get('IS_DEGREE_GRANTING', None)
        return val is None or str(val).strip().upper() in ['Y','YES','TRUE','T','1']
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return s if s != '' and s.lower() != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        return s if s != '' and s.lower() != 'nan' else None
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
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return s if s != '' and s.lower() != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        return s if s != '' and s.lower() != 'nan' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return s if s != '' and s.lower() != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        return s if s != '' and s.lower() != 'nan' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['DEPARTMENT_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['DEPARTMENT_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['DEPARTMENT_CODE'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['DEPARTMENT_CODE'], ascending=[True])

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_students = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_departments = prepared_table_2

# Assume prepared_students and prepared_departments are already synthesized from table_1 and table_2 respectively.

# Inner join students to departments on department code
joined = prepared_students.merge(
    prepared_departments,
    left_on='DEPARTMENT',
    right_on='DEPARTMENT_CODE',
    how='inner'
)

# Filter to first name Kevin (case-insensitive, robust to whitespace)
mask_kevin = joined['FIRST_NAME'].astype(str).str.strip().str.casefold() == 'kevin'
kevin_rows = joined[mask_kevin].copy()

# Build full name (prefer existing FULL_NAME; if missing, compose Last, First Middle)
# Keep the provided FULL_NAME as-is and also ensure a fallback
fallback_full = (
    kevin_rows['LAST_NAME'].fillna('').str.strip() + ', ' +
    kevin_rows['FIRST_NAME'].fillna('').str.strip() +
    kevin_rows.apply(lambda r: (' ' + r['MIDDLE_NAME'].strip() + '.') if isinstance(r['MIDDLE_NAME'], str) and r['MIDDLE_NAME'].strip() else '', axis=1)
)
kevin_rows['FULL_NAME_OUT'] = kevin_rows['FULL_NAME'].where(kevin_rows['FULL_NAME'].notna() & (kevin_rows['FULL_NAME'].astype(str).str.strip()!=''), fallback_full)

# Compute total student counts per department and per school (across all students, not just Kevins)
# Use the same join base for global counts
all_joined = joined.copy()

dept_counts = all_joined.groupby(['DEPARTMENT_CODE', 'DEPARTMENT_NAME'], dropna=False).size().reset_index(name='TOTAL_STUDENTS_IN_DEPARTMENT')
school_counts = all_joined.groupby(['SCHOOL_NAME'], dropna=False).size().reset_index(name='TOTAL_STUDENTS_IN_SCHOOL')

# Attach counts to Kevin rows
kevin_with_dept = kevin_rows.merge(dept_counts, on=['DEPARTMENT_CODE', 'DEPARTMENT_NAME'], how='left')
kevin_final = kevin_with_dept.merge(school_counts, on='SCHOOL_NAME', how='left')

# Select and rename output columns; one row per department affiliation
result = kevin_final[[
    'FIRST_NAME',
    'FULL_NAME_OUT',
    'EMAIL_ADDRESS',
    'DEPARTMENT_NAME',
    # Department phone number not available in provided tables; set as None/NaN placeholder
    'SCHOOL_NAME',
    'TOTAL_STUDENTS_IN_DEPARTMENT',
    'TOTAL_STUDENTS_IN_SCHOOL'
]].rename(columns={
    'FULL_NAME_OUT': 'FULL_NAME'
})

# Add department phone placeholder if required by downstream consumers
if 'DEPARTMENT_PHONE' not in result.columns:
    result.insert(result.columns.get_loc('SCHOOL_NAME'), 'DEPARTMENT_PHONE', pd.NA)

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
