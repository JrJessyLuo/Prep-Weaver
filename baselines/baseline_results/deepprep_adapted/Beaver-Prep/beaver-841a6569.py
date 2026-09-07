import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_KEY", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # strip leading/trailing whitespace and collapse any internal whitespace to single spaces
    #     s2 = re.sub(r'\s+', ' ', str(s).strip())
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # strip leading/trailing whitespace and collapse any internal whitespace to single spaces
        s2 = re.sub(r'\s+', ' ', str(s).strip())
        return s2
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
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC'] if c in table_1.columns]
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        return s.upper()
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
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
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
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_MEMBER_MIT_ID", func="""
    # import pandas as pd
    # import re
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     # common artifact: "984301411.0" -> "984301411"
    #     s = re.sub(r'\.0$', '', s)
    #     # keep only digits if any stray whitespace exists
    #     s = re.sub(r'\s+', '', s)
    #     if not re.fullmatch(r'\d+', s):
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        # common artifact: "984301411.0" -> "984301411"
        s = re.sub(r'\.0$', '', s)
        # keep only digits if any stray whitespace exists
        s = re.sub(r'\s+', '', s)
        if not re.fullmatch(r'\d+', s):
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_MEMBER_MIT_ID"] = table_1["MOIRA_LIST_MEMBER_MIT_ID"].apply(_std_apply)

    # ---------------- Step 5 ----------------
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

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY', 'moira_list_member'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY', 'moira_list_member'], keep='last').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="STUDENT_YEAR", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['STUDENT_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['STUDENT_YEAR']
    if _dtype == "datetime64":
        table_1['STUDENT_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['STUDENT_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['STUDENT_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['STUDENT_YEAR'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
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
    # StandardizeString(table_name="table_1", column_name="FULL_NAME_UPPERCASE", func="""
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
    table_1["FULL_NAME_UPPERCASE"] = table_1["FULL_NAME_UPPERCASE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
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

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FULL_NAME', 'FULL_NAME_UPPERCASE', 'EMAIL_ADDRESS', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR'])
    # SelectCol
    _cols = [c for c in ['FULL_NAME', 'FULL_NAME_UPPERCASE', 'EMAIL_ADDRESS', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['EMAIL_ADDRESS'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['EMAIL_ADDRESS'], keep='last').reset_index(drop=True)

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
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
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = " ".join(s.split())
        return s
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
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_FULL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_FULL_NAME"] = table_1["DEPARTMENT_FULL_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_CODE"] = table_1["SCHOOL_CODE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['DEPARTMENT_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['DEPARTMENT_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_memberships = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_people = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
prepared_departments = prepared_table_4

# Assume the prepared tables are provided as DataFrames: prepared_lists, prepared_memberships, prepared_people, prepared_departments

# 1) Join lists to memberships
lm = prepared_memberships.merge(prepared_lists, on='MOIRA_LIST_KEY', how='inner')

# 2) Normalize identifiers for joining memberships to people via email address
# Derive username from EMAIL_ADDRESS in people and compare to moira_list_member (both upper-trimmed)
people = prepared_people.copy()
people['EMAIL_USER'] = people['EMAIL_ADDRESS'].fillna('').str.split('@').str[0]
people['EMAIL_USER_NORM'] = people['EMAIL_USER'].str.strip().str.upper()

m = lm.copy()
m['MEMBER_NORM'] = m['moira_list_member'].astype(str).str.strip().str.upper()

# Primary join via email username == moira_list_member
lm_person = m.merge(
    people,
    left_on='MEMBER_NORM',
    right_on='EMAIL_USER_NORM',
    how='left',
    suffixes=('', '_p')
)

# For members not matched by email, try FULL_NAME matching using provided full name in memberships when available
unmatched = lm_person[lm_person['EMAIL_USER_NORM'].isna()].copy()
if not unmatched.empty:
    people_name = people[['FULL_NAME', 'FULL_NAME_UPPERCASE', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR']].copy()
    people_name['FULL_NAME_NORM'] = people_name['FULL_NAME'].fillna('').str.strip().str.upper()
    unmatched['MEMBER_FULLNAME_NORM'] = unmatched['MOIRA_LIST_MEMBER_FULL_NAME'].fillna('').str.strip().str.upper()
    rematch = unmatched.merge(
        people_name,
        left_on='MEMBER_FULLNAME_NORM',
        right_on='FULL_NAME_NORM',
        how='left',
        suffixes=('', '_n')
    )
    # Combine back, preferring email-based matches when present
    matched_email = lm_person[~lm_person['EMAIL_USER_NORM'].isna()]
    lm_person = pd.concat([matched_email, rematch], ignore_index=True, sort=False)

# 3) Compute total subscribers per list (distinct members to be safe)
lm_person['member_id_for_count'] = lm_person['moira_list_member'].astype(str).str.strip().str.upper()
subs_per_list = (
    lm_person.groupby(['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC'])['member_id_for_count']
    .nunique()
    .reset_index(name='total_subscribers')
)

# 4) Identify students and their departments (filter student indicator; keep department code/name)
lm_person['IS_STUDENT'] = lm_person['STUDENT_YEAR'].notna() & (lm_person['STUDENT_YEAR'].astype(str).str.strip() != '')
student_rows = lm_person[lm_person['IS_STUDENT']].copy()

# Map department code/name via departments reference when department code is present
student_rows = student_rows.merge(
    prepared_departments,
    left_on='DEPARTMENT',
    right_on='DEPARTMENT_CODE',
    how='left',
    suffixes=('', '_dept')
)

# Prefer canonical department name from departments table, else fallback to people.DEPRTMENT_NAME
student_rows['DEPT_NAME_FINAL'] = student_rows['DEPARTMENT_NAME'].where(
    student_rows['DEPARTMENT_NAME'].notna() & (student_rows['DEPARTMENT_NAME'].astype(str).str.strip() != ''),
    student_rows['DEPARTMENT_NAME_dept']
)
student_rows['DEPT_NAME_FINAL'] = student_rows['DEPT_NAME_FINAL'].fillna(student_rows['DEPARTMENT_NAME_dept'])

# Count students per department within each list
stud_counts = (
    student_rows.groupby(['MOIRA_LIST_KEY', 'DEPT_NAME_FINAL'])['member_id_for_count']
    .nunique()
    .reset_index(name='students_in_dept')
)

# For each list, select department with max students; ties broken by alphabetical department name for determinism
stud_counts_sorted = stud_counts.sort_values(['MOIRA_LIST_KEY', 'students_in_dept', 'DEPT_NAME_FINAL'], ascending=[True, False, True])
max_dept_per_list = stud_counts_sorted.groupby('MOIRA_LIST_KEY').head(1)

# 5) Combine totals with max department info
result = subs_per_list.merge(max_dept_per_list[['MOIRA_LIST_KEY', 'DEPT_NAME_FINAL', 'students_in_dept']], on='MOIRA_LIST_KEY', how='left')

# 6) Select top 100 lists by total subscribers
result_top100 = result.sort_values('total_subscribers', ascending=False).head(100)

# 7) Final projection
final = result_top100.rename(columns={
    'MOIRA_LIST_NAME': 'list_name',
    'IS_PUBLIC': 'is_public',
    'DEPT_NAME_FINAL': 'top_department_name',
    'students_in_dept': 'students_from_top_department'
})[
    ['list_name', 'total_subscribers', 'is_public', 'top_department_name', 'students_from_top_department']
]

target = final

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
