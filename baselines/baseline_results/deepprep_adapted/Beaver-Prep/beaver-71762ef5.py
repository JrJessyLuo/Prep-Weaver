import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_CODE_DESC", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return " ".join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_CODE_DESC"] = table_1["SUBJECT_CODE_DESC"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COURSE_NUMBER", func="""
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
    table_1["COURSE_NUMBER"] = table_1["COURSE_NUMBER"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_CODE"] = table_1["SUBJECT_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return " ".join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_CODE"] = table_1["SCHOOL_CODE"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return " ".join(str(s).strip().split())
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
    # SelectCol(table_name="table_1", columns=['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'COURSE_NUMBER'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'COURSE_NUMBER'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SUBJECT_CODE', 'COURSE_NUMBER', 'DEPARTMENT_CODE', 'SCHOOL_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SUBJECT_CODE', 'COURSE_NUMBER', 'DEPARTMENT_CODE', 'SCHOOL_CODE'], keep='last').reset_index(drop=True)

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
    # DropColumn(table_name="table_1", drop_columns=['department_full_name', 'DEPT_BUDGET_CODE', 'IS_DEGREE_GRANTING', 'DEPT_NAME_IN_COMMENCEMENT_BK', 'SCHOOL_NAME_IN_COMMENCEMENT_BK', 'DEPARTMENT_NAME_HISTORY', 'DEPARTMENT_LAST_ACTIVITY_DATE', 'DLC_KEY', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['department_full_name', 'DEPT_BUDGET_CODE', 'IS_DEGREE_GRANTING', 'DEPT_NAME_IN_COMMENCEMENT_BK', 'SCHOOL_NAME_IN_COMMENCEMENT_BK', 'DEPARTMENT_NAME_HISTORY', 'DEPARTMENT_LAST_ACTIVITY_DATE', 'DLC_KEY', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip().upper()
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
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
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
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['DEPARTMENT_CODE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['DEPARTMENT_CODE'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['DEPARTMENT_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['DEPARTMENT_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="department_phone_number", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     # convert float-like '2683470.0' to '2683470'
    #     if re.fullmatch(r'\d+\.0', s):
    #         s = s[:-2]
    #     # keep digits only
    #     digits = re.sub(r'\D+', '', s)
    #     return digits if digits != '' else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        # convert float-like '2683470.0' to '2683470'
        if re.fullmatch(r'\d+\.0', s):
            s = s[:-2]
        # keep digits only
        digits = re.sub(r'\D+', '', s)
        return digits if digits != '' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["department_phone_number"] = table_1["department_phone_number"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['department_phone_number'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['department_phone_number'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SIS_ADMIN_DEPARTMENT_CODE', 'department_phone_number'])
    # SelectCol
    _cols = [c for c in ['SIS_ADMIN_DEPARTMENT_CODE', 'department_phone_number'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_departments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_dept_phones = prepared_table_3

# Start from prepared subjects (SIS subjects) and link to canonical departments/schools
subj = prepared_subjects.copy()
depts = prepared_departments.copy()
phones = prepared_dept_phones.copy()

# Normalize key columns to string and trim whitespace
for df, cols in [
    (subj, ["DEPARTMENT_CODE", "COURSE_NUMBER", "SUBJECT_CODE", "SUBJECT_CODE_DESC", "SCHOOL_CODE", "SCHOOL_NAME", "DEPARTMENT_NAME"]),
    (depts, ["DEPARTMENT_CODE", "DEPARTMENT_NAME", "SCHOOL_CODE", "SCHOOL_NAME"]),
    (phones, ["SIS_ADMIN_DEPARTMENT_CODE", "department_phone_number"])]:
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

# Join subjects to departments to get authoritative school/department names
sj = subj.merge(
    depts,
    on="DEPARTMENT_CODE",
    how="left",
    suffixes=("_from_subjects", "")
)

# Prefer department/school names from the canonical table when available
sj["DEPARTMENT_NAME_FINAL"] = sj["DEPARTMENT_NAME"].where(sj["DEPARTMENT_NAME"].notna() & (sj["DEPARTMENT_NAME"] != "nan"), sj.get("DEPARTMENT_NAME_from_subjects"))
sj["SCHOOL_NAME_FINAL"] = sj["SCHOOL_NAME"].where(sj["SCHOOL_NAME"].notna() & (sj["SCHOOL_NAME"] != "nan"), sj.get("SCHOOL_NAME_from_subjects"))
sj["SCHOOL_CODE_FINAL"] = sj["SCHOOL_CODE"].where(sj["SCHOOL_CODE"].notna() & (sj["SCHOOL_CODE"] != "nan"), sj.get("SCHOOL_CODE_from_subjects"))

# Prepare phone counts per department (count distinct non-null numbers)
phones_clean = phones[phones["department_phone_number"].notna() & (phones["department_phone_number"] != "nan")].copy()
phones_clean["department_phone_number"] = phones_clean["department_phone_number"].str.replace(".0$", "", regex=True)
phone_counts = (
    phones_clean.groupby("SIS_ADMIN_DEPARTMENT_CODE")["department_phone_number"]
    .nunique()
    .reset_index()
    .rename(columns={"SIS_ADMIN_DEPARTMENT_CODE": "DEPARTMENT_CODE", "department_phone_number": "total_phone_numbers"})
)

# Derive course level from COURSE_NUMBER (e.g., take leading digits; fallback 'Unknown')
def extract_level(cn):
    if pd.isna(cn):
        return "Unknown"
    s = str(cn).strip()
    m = re.search(r"(\d+)", s)
    if not m:
        return "Unknown"
    num = m.group(1)
    # Define level by first digit (e.g., 1xx, 2xx, etc.)
    return num[0] + "xx" if len(num) >= 1 else "Unknown"

sj["course_level"] = sj["COURSE_NUMBER"].apply(extract_level)

# For each department, determine the most common course level among its SIS subjects
level_mode = (
    sj.groupby(["SCHOOL_CODE_FINAL", "SCHOOL_NAME_FINAL", "DEPARTMENT_CODE", "DEPARTMENT_NAME_FINAL"])['course_level']
      .agg(lambda s: s.value_counts().index[0] if len(s) else "Unknown")
      .reset_index()
)

# Attach phone counts
result = level_mode.merge(phone_counts, on="DEPARTMENT_CODE", how="left")
result["total_phone_numbers"].fillna(0, inplace=True)
result["total_phone_numbers"] = result["total_phone_numbers"].astype(int)

# Final selection and rename
final = result.rename(columns={
    "SCHOOL_CODE_FINAL": "school_code",
    "SCHOOL_NAME_FINAL": "school_name",
    "DEPARTMENT_CODE": "department_code",
    "DEPARTMENT_NAME_FINAL": "department_name",
    "course_level": "most_common_course_level"
})[
    [
        "school_code",
        "school_name",
        "department_code",
        "department_name",
        "total_phone_numbers",
        "most_common_course_level"
    ]
]

# Keep only schools/departments that offer SIS courses (already ensured by starting from subj)
target = final.sort_values(["school_code", "department_code"]).reset_index(drop=True)

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
