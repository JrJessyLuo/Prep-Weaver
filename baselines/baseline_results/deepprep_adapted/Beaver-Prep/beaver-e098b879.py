import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['FORM_OF_ADDRESS_SHORT', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'KRB_NAME_UPPERCASE', 'JOB_ID', 'JOB_TITLE', 'ADMIN_EMPLOYEE_TYPE', 'HR_DEPARTMENT_CODE_OLD', 'HR_DEPARTMENT_NAME', 'HR_ORG_UNIT_ID', 'ADMIN_ORG_UNIT_TITLE', 'ADMIN_POSITION_TITLE', 'PAYROLL_RANK', 'EMPLOYMENT_PERCENT', 'IS_CONSULT_PRIV', 'IS_PAID_APPT', 'SUMMER_SESSION_MONTHS', 'IS_SABBATICAL', 'SABBATICAL_BEGIN_DATE', 'SABBATICAL_END_DATE', 'IS_OPA_REQUIRED', 'IS_6MO_APPT', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['FORM_OF_ADDRESS_SHORT', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'KRB_NAME_UPPERCASE', 'JOB_ID', 'JOB_TITLE', 'ADMIN_EMPLOYEE_TYPE', 'HR_DEPARTMENT_CODE_OLD', 'HR_DEPARTMENT_NAME', 'HR_ORG_UNIT_ID', 'ADMIN_ORG_UNIT_TITLE', 'ADMIN_POSITION_TITLE', 'PAYROLL_RANK', 'EMPLOYMENT_PERCENT', 'IS_CONSULT_PRIV', 'IS_PAID_APPT', 'SUMMER_SESSION_MONTHS', 'IS_SABBATICAL', 'SABBATICAL_BEGIN_DATE', 'SABBATICAL_END_DATE', 'IS_OPA_REQUIRED', 'IS_6MO_APPT', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s == "" or s.lower() in {"nan", "none", "null"}:
    #         return None
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s == "" or s.lower() in {"nan", "none", "null"}:
            return None
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
    # CastType(table_name="table_1", column="MIT_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MIT_ID']
    if _dtype == "datetime64":
        table_1['MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MIT_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FULL_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FULL_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FULL_NAME']
    if _dtype == "datetime64":
        table_1['FULL_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FULL_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FULL_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FULL_NAME'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="EMAIL_ADDRESS", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['EMAIL_ADDRESS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['EMAIL_ADDRESS']
    if _dtype == "datetime64":
        table_1['EMAIL_ADDRESS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['EMAIL_ADDRESS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['EMAIL_ADDRESS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['EMAIL_ADDRESS'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="IS_FACULTY", dtype="bool")
    # CastType
    _dtype = 'bool'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IS_FACULTY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IS_FACULTY']
    if _dtype == "datetime64":
        table_1['IS_FACULTY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IS_FACULTY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IS_FACULTY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IS_FACULTY'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="IS_SUMMER_SESSION_APPT", dtype="bool")
    # CastType
    _dtype = 'bool'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IS_SUMMER_SESSION_APPT'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IS_SUMMER_SESSION_APPT']
    if _dtype == "datetime64":
        table_1['IS_SUMMER_SESSION_APPT'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IS_SUMMER_SESSION_APPT'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IS_SUMMER_SESSION_APPT'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IS_SUMMER_SESSION_APPT'] = _series.astype(str)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['term_code'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['term_code'], ascending=[True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FINANCIAL_AID_YEAR'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FINANCIAL_AID_YEAR'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FINANCIAL_AID_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FINANCIAL_AID_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FINANCIAL_AID_YEAR']
    if _dtype == "datetime64":
        table_1['FINANCIAL_AID_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FINANCIAL_AID_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FINANCIAL_AID_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FINANCIAL_AID_YEAR'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row[\"FINANCIAL_AID_YEAR\"] > 2001
    # """)
    # Filter
    def filter_func(row):
        return row[\"FINANCIAL_AID_YEAR\"] > 2001
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['term_code', 'TERM_DESCRIPTION', 'FINANCIAL_AID_YEAR'])
    # SelectCol
    _cols = [c for c in ['term_code', 'TERM_DESCRIPTION', 'FINANCIAL_AID_YEAR'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['term_code'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['term_code'], keep='last').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ACADEMIC_TERM_DESCRIPTION", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s.lower() != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s.lower() != 'nan' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ACADEMIC_TERM_DESCRIPTION"] = table_1["ACADEMIC_TERM_DESCRIPTION"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ACADEMIC_TERM_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s == "" or s.lower() == "nan":
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s == "" or s.lower() == "nan":
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ACADEMIC_TERM_CODE"] = table_1["ACADEMIC_TERM_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FINANCIAL_AID_YEAR", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FINANCIAL_AID_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FINANCIAL_AID_YEAR']
    if _dtype == "datetime64":
        table_1['FINANCIAL_AID_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FINANCIAL_AID_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FINANCIAL_AID_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FINANCIAL_AID_YEAR'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ACADEMIC_TERM_CODE', 'ACADEMIC_TERM_DESCRIPTION', 'FINANCIAL_AID_YEAR'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ACADEMIC_TERM_CODE', 'ACADEMIC_TERM_DESCRIPTION', 'FINANCIAL_AID_YEAR'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ACADEMIC_TERM_CODE', 'ACADEMIC_TERM_DESCRIPTION', 'FINANCIAL_AID_YEAR'])
    # SelectCol
    _cols = [c for c in ['ACADEMIC_TERM_CODE', 'ACADEMIC_TERM_DESCRIPTION', 'FINANCIAL_AID_YEAR'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
people_directory = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
academic_terms = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
calendar_terms = prepared_table_3

# Inputs: prepared tables
people = people_directory.copy()
terms = academic_terms.copy()
cal_terms = calendar_terms.copy()

# 1) Identify summer terms in FA years > 2001 using either terms table (primary) or calendar_terms (backup)
terms_summer = terms[terms['TERM_DESCRIPTION'].str.contains('Summer', case=False, na=False)].copy()
terms_summer = terms_summer[pd.to_numeric(terms_summer['FINANCIAL_AID_YEAR'], errors='coerce') > 2001]

cal_terms_summer = cal_terms[cal_terms['ACADEMIC_TERM_DESCRIPTION'].str.contains('Summer', case=False, na=False)].copy()
cal_terms_summer = cal_terms_summer[pd.to_numeric(cal_terms_summer['FINANCIAL_AID_YEAR'], errors='coerce') > 2001]

# Merge to unify term codes considered summer after 2001
summer_codes = pd.Series(dtype=object)
if not terms_summer.empty:
    summer_codes = pd.concat([summer_codes, terms_summer['term_code']])
if not cal_terms_summer.empty:
    summer_codes = pd.concat([summer_codes, cal_terms_summer['ACADEMIC_TERM_CODE']])
summer_codes = summer_codes.dropna().drop_duplicates()

# 2) Identify faculty who teach in summer: we only have a summer-session appointment flag in people
faculty_summer = people.copy()
faculty_summer['is_fac'] = people['IS_FACULTY'].astype(str).str.upper().isin(['Y', 'YES', 'TRUE', '1'])
faculty_summer['is_summer'] = people['IS_SUMMER_SESSION_APPT'].astype(str).str.upper().isin(['Y', 'YES', 'TRUE', '1'])
faculty_summer = faculty_summer[faculty_summer['is_fac'] & faculty_summer['is_summer']]

# 3) Email lists starting with C: Not present in selected tables. We cannot compute list membership counts without a mailing list table and a membership bridge.
# Return an empty result with the expected columns to indicate no data available from provided tables.

result = pd.DataFrame(columns=['list_name', 'num_people_in_list', 'num_faculty_in_list'])

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
