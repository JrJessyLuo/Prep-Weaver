import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY', 'moira_list_member'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY', 'moira_list_member'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     val = row.get('MOIRA_LIST_KEY')
    #     return isinstance(val, str) and val.strip() == 'ocean-apple'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        val = row.get('MOIRA_LIST_KEY')
        return isinstance(val, str) and val.strip() == 'ocean-apple'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return s
    #     s = str(s).strip()
    #     # normalize for joins (Moira usernames are typically case-insensitive)
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return s
        s = str(s).strip()
        # normalize for joins (Moira usernames are typically case-insensitive)
        return s.lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["moira_list_member"] = table_1["moira_list_member"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'] if c in table_1.columns]
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
    # SelectCol(table_name="table_1", columns=['EMAIL_ADDRESS', 'FULL_NAME', 'FULL_NAME_UPPERCASE', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR'])
    # SelectCol
    _cols = [c for c in ['EMAIL_ADDRESS', 'FULL_NAME', 'FULL_NAME_UPPERCASE', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # DropNulls(table_name="table_1", subset=['EMAIL_ADDRESS'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['EMAIL_ADDRESS'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['EMAIL_ADDRESS'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['EMAIL_ADDRESS'], keep='first').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SIS_ADMIN_DEPARTMENT_CODE'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SIS_ADMIN_DEPARTMENT_CODE'], keep='first').reset_index(drop=True)

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
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in {"nan", "none", ""}:
    #         return None
    #     # keep digits only
    #     digits = re.sub(r"\D+", "", s)
    #     return digits if digits != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in {"nan", "none", ""}:
            return None
        # keep digits only
        digits = re.sub(r"\D+", "", s)
        return digits if digits != "" else None
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
    # CastType(table_name="table_1", column="DEPARTMENT_PHONE_AREA_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['DEPARTMENT_PHONE_AREA_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['DEPARTMENT_PHONE_AREA_CODE']
    if _dtype == "datetime64":
        table_1['DEPARTMENT_PHONE_AREA_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['DEPARTMENT_PHONE_AREA_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['DEPARTMENT_PHONE_AREA_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['DEPARTMENT_PHONE_AREA_CODE'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_PHONE_AREA_CODE", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in {"nan", "none", ""}:
    #         return None
    #     digits = re.sub(r"\D+", "", s)
    #     # keep as-is (could be null); do not force 3 digits without requirements
    #     return digits if digits != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in {"nan", "none", ""}:
            return None
        digits = re.sub(r"\D+", "", s)
        # keep as-is (could be null); do not force 3 digits without requirements
        return digits if digits != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_PHONE_AREA_CODE"] = table_1["DEPARTMENT_PHONE_AREA_CODE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SIS_ADMIN_DEPARTMENT_CODE', 'SIS_ADMIN_DEPARTMENT_NAME', 'DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number'])
    # SelectCol
    _cols = [c for c in ['SIS_ADMIN_DEPARTMENT_CODE', 'SIS_ADMIN_DEPARTMENT_NAME', 'DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_4'])
prepared_mailing_list_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_people = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_departments = prepared_table_3

# 1) Filter mailing list to the requested list and normalize username
ml = prepared_mailing_list_members.copy()
ml = ml[ml['MOIRA_LIST_KEY'] == 'ocean-apple']
ml['member_user'] = ml['moira_list_member'].astype(str).str.strip().str.lower()

# 2) Prepare people with username extracted from email and keep only students
pp = prepared_people.copy()
pp['email_user'] = pp['EMAIL_ADDRESS'].astype(str).str.split('@').str[0].str.strip().str.lower()
# Consider a record a student if STUDENT_YEAR not null/empty
pp_students = pp[pp['STUDENT_YEAR'].notna() & (pp['STUDENT_YEAR'].astype(str).str.strip() != '')]

# 3) Join mailing list members to people via username = email local part
m_join = ml.merge(pp_students, left_on='member_user', right_on='email_user', how='inner')

# 4) Normalize department names for joining to department phone table
m_join['dept_name_norm'] = m_join['DEPARTMENT_NAME'].astype(str).str.strip().str.lower()

pdpt = prepared_departments.copy()
pdpt['dept_name_norm'] = pdpt['SIS_ADMIN_DEPARTMENT_NAME'].astype(str).str.strip().str.lower()

# 5) Join to get department phone
mj = m_join.merge(pdpt[['dept_name_norm','DEPARTMENT_PHONE_AREA_CODE','department_phone_number','SIS_ADMIN_DEPARTMENT_NAME']],
                  on='dept_name_norm', how='left')

# 6) Aggregate: count students per department name; keep phone fields
grp = mj.groupby(['DEPARTMENT_NAME','DEPARTMENT_PHONE_AREA_CODE','department_phone_number'], dropna=False).size().reset_index(name='student_count')

# 7) Find max and filter departments with that max
max_cnt = grp['student_count'].max() if len(grp) else 0
result = grp[grp['student_count'] == max_cnt].copy()

# 8) Prepare final columns: department name, phone number, total students
# Compose phone as area code + number when available
def format_phone(row):
    ac = '' if pd.isna(row['DEPARTMENT_PHONE_AREA_CODE']) else str(int(float(row['DEPARTMENT_PHONE_AREA_CODE'])))
    num = '' if pd.isna(row['department_phone_number']) else str(int(float(row['department_phone_number'])))
    if ac and num:
        return f"({ac}) {num}"
    elif num:
        return num
    else:
        return None

result['PHONE'] = result.apply(format_phone, axis=1)
answer = result[['DEPARTMENT_NAME','PHONE','student_count']].rename(columns={'DEPARTMENT_NAME':'department_name','PHONE':'phone','student_count':'total_students'})
# 'answer' is the final DataFrame

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
