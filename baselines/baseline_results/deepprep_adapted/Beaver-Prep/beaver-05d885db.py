import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['OFFICE_LOCATION', 'OFFICE_PHONE', 'STUDENT_YEAR', 'FULL_NAME_UPPERCASE', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['OFFICE_LOCATION', 'OFFICE_PHONE', 'STUDENT_YEAR', 'FULL_NAME_UPPERCASE', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MIDDLE_NAME", func="""
    # def transform_func(s):
    #     # Normalize missing/NULL-like values to empty string
    #     if s is None:
    #         return ""
    #     s_str = str(s).strip()
    #     if s_str.lower() in {"nan", "none", "null", ""}:
    #         return ""
    #     return s_str
    # """)
    # StandardizeString
    def transform_func(s):
        # Normalize missing/NULL-like values to empty string
        if s is None:
            return ""
        s_str = str(s).strip()
        if s_str.lower() in {"nan", "none", "null", ""}:
            return ""
        return s_str
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MIDDLE_NAME"] = table_1["MIDDLE_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return ""
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return ""
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
    # StandardizeString(table_name="table_1", column_name="FULL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return ""
    #     s_str = str(s).strip()
    #     # Remove a trailing period if present (common in source FULL_NAME)
    #     if s_str.endswith("."):
    #         s_str = s_str[:-1].strip()
    #     return s_str
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return ""
        s_str = str(s).strip()
        # Remove a trailing period if present (common in source FULL_NAME)
        if s_str.endswith("."):
            s_str = s_str[:-1].strip()
        return s_str
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FULL_NAME"] = table_1["FULL_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['EMAIL_ADDRESS'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['EMAIL_ADDRESS'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'DEPARTMENT', 'DEPARTMENT_NAME', 'EMAIL_ADDRESS'])
    # SelectCol
    _cols = [c for c in ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'DEPARTMENT', 'DEPARTMENT_NAME', 'EMAIL_ADDRESS'] if c in table_1.columns]
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
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_MIT_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_MIT_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # normalize whitespace and case for stable username joins
    #     s = str(s).strip()
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # normalize whitespace and case for stable username joins
        s = str(s).strip()
        return s.lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["moira_list_member"] = table_1["moira_list_member"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_MEMBER_FULL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # normalize internal whitespace
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # normalize internal whitespace
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_MEMBER_FULL_NAME"] = table_1["MOIRA_LIST_MEMBER_FULL_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="MOIRA_LIST_MEMBER_MIT_ID", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID']
    if _dtype == "datetime64":
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return str(row.get('IS_MOIRA_MAILING_LIST','')).strip().upper() == 'Y'
    # """)
    # Filter
    def filter_func(row):
        return str(row.get('IS_MOIRA_MAILING_LIST','')).strip().upper() == 'Y'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # normalize to canonical key style
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # normalize to canonical key style
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
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['MOIRA_LIST_KEY'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['MOIRA_LIST_KEY'], ascending=[True])

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['DEPARTMENT_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['DEPARTMENT_NAME'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT_CODE', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_CODE', 'DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
prepared_table_2 = _prep_2(tables['table_3'])
prepared_mailing_list_members = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_mailing_lists = prepared_table_3
prepared_table_4 = _prep_4(tables['table_5'])
prepared_departments = prepared_table_4

# Assume prepared tables are provided as DataFrames: prepared_students, prepared_mailing_list_members, prepared_mailing_lists, prepared_departments

# Normalize keys and names for robust matching
ml = prepared_mailing_lists.copy()
ml['MOIRA_LIST_KEY_norm'] = ml['MOIRA_LIST_KEY'].astype(str).str.strip().str.lower()
ml['MOIRA_LIST_NAME_norm'] = ml['MOIRA_LIST_NAME'].astype(str).str.strip().str.lower()

mlm = prepared_mailing_list_members.copy()
mlm['MOIRA_LIST_KEY_norm'] = mlm['MOIRA_LIST_KEY'].astype(str).str.strip().str.lower()
mlm['MOIRA_LIST_MEMBER_FULL_NAME_norm'] = mlm['MOIRA_LIST_MEMBER_FULL_NAME'].astype(str).str.strip().str.upper()

stud = prepared_students.copy()
stud['FULL_NAME_UPPER_norm'] = stud['FULL_NAME'].astype(str).str.strip().str.upper()
stud['LAST_INITIAL'] = stud['LAST_NAME'].astype(str).str.strip().str[:1].str.upper()

# Filter to the target mailing list by name
target_list_name = 'beacon-date-date'
ml_target = ml[ml['MOIRA_LIST_NAME_norm'] == target_list_name]

# Join members with the target list via key
members_of_target = mlm.merge(ml_target[['MOIRA_LIST_KEY_norm','MOIRA_LIST_NAME_norm']], on='MOIRA_LIST_KEY_norm', how='inner')

# Compute list size (number of member rows) for the target list
list_size = len(members_of_target)

# Join students to members by normalized full name; also restrict to last names starting with 'H'
students_H = stud[stud['LAST_INITIAL'] == 'H']
joined = students_H.merge(
    members_of_target,
    left_on='FULL_NAME_UPPER_norm',
    right_on='MOIRA_LIST_MEMBER_FULL_NAME_norm',
    how='inner'
)

# Prepare department phone: table_1 contains OFFICE_PHONE but request asks for phone numbers of departments they belong to; no department phone exists in provided tables.
# Use OFFICE_PHONE as the available phone field associated with the student's department context.

# Build final output columns and attach list size
result = joined[['FIRST_NAME','MIDDLE_NAME','LAST_NAME','FULL_NAME','DEPARTMENT','DEPARTMENT_NAME']].copy()
# Use OFFICE_PHONE if present in original students table; if not available in prepared_students, attempt to fetch from original if accessible. Here we assume not included; thus no phone unless OFFICE_PHONE was preserved. If OFFICE_PHONE exists in prepared_students, include it.
if 'OFFICE_PHONE' in students_H.columns:
    result = joined[['FIRST_NAME','MIDDLE_NAME','LAST_NAME','FULL_NAME','DEPARTMENT','DEPARTMENT_NAME','OFFICE_PHONE']].copy()
    result = result.rename(columns={'OFFICE_PHONE':'DEPARTMENT_PHONE'})
else:
    result['DEPARTMENT_PHONE'] = pd.NA

result['MAILING_LIST_NAME'] = target_list_name
result['MAILING_LIST_SIZE'] = list_size

# Deduplicate in case of multiple matches per person
result = result.drop_duplicates(subset=['FULL_NAME'])

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
