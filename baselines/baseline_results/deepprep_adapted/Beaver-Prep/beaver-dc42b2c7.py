import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COMM_REQ_ATTRIBUTE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s.lower() not in {"nan","none","null",""} else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s.lower() not in {"nan","none","null",""} else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["COMM_REQ_ATTRIBUTE"] = table_1["COMM_REQ_ATTRIBUTE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COMM_REQ_ATTRIBUTE_DESC", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s.lower() not in {"nan","none","null",""} else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s.lower() not in {"nan","none","null",""} else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["COMM_REQ_ATTRIBUTE_DESC"] = table_1["COMM_REQ_ATTRIBUTE_DESC"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TOTAL_UNITS", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TOTAL_UNITS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TOTAL_UNITS']
    if _dtype == "datetime64":
        table_1['TOTAL_UNITS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TOTAL_UNITS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TOTAL_UNITS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TOTAL_UNITS'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SUBJECT_ID', 'SUBJECT_CODE', 'SUBJECT_TITLE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SUBJECT_ID', 'SUBJECT_CODE', 'SUBJECT_TITLE'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_ID', 'SUBJECT_CODE', 'SUBJECT_TITLE', 'SUBJECT_DESCRIPTION', 'TOTAL_UNITS', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'COMM_REQ_ATTRIBUTE', 'COMM_REQ_ATTRIBUTE_DESC'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_ID', 'SUBJECT_CODE', 'SUBJECT_TITLE', 'SUBJECT_DESCRIPTION', 'TOTAL_UNITS', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'COMM_REQ_ATTRIBUTE', 'COMM_REQ_ATTRIBUTE_DESC'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="CIS_ATTRIBUTE_GROUP_NOTE", func="""
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
    table_1["CIS_ATTRIBUTE_GROUP_NOTE"] = table_1["CIS_ATTRIBUTE_GROUP_NOTE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="hass_attribute", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["hass_attribute"] = table_1["hass_attribute"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DESCRIPTION_ON_FORM", func="""
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
    table_1["DESCRIPTION_ON_FORM"] = table_1["DESCRIPTION_ON_FORM"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DESCRIPTION_IN_BULLETIN", func="""
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
    table_1["DESCRIPTION_IN_BULLETIN"] = table_1["DESCRIPTION_IN_BULLETIN"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="CIS_ATTRIBUTE_GROUP", func="""
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
    table_1["CIS_ATTRIBUTE_GROUP"] = table_1["CIS_ATTRIBUTE_GROUP"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['hass_attribute'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['hass_attribute'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['hass_attribute'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['hass_attribute'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['hass_attribute', 'DESCRIPTION_ON_FORM', 'DESCRIPTION_IN_BULLETIN', 'CIS_ATTRIBUTE_GROUP', 'CIS_ATTRIBUTE_GROUP_NOTE'])
    # SelectCol
    _cols = [c for c in ['hass_attribute', 'DESCRIPTION_ON_FORM', 'DESCRIPTION_IN_BULLETIN', 'CIS_ATTRIBUTE_GROUP', 'CIS_ATTRIBUTE_GROUP_NOTE'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="SUBJECT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_CODE"] = table_1["SUBJECT_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'], keep='first').reset_index(drop=True)

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
    # MissingValueImputation(table_name="table_1", column_name="OFFER_DEPT_CODE", mode="mode")
    # MissingValueImputation
    table_1["OFFER_DEPT_CODE"] = table_1["OFFER_DEPT_CODE"].fillna(table_1["OFFER_DEPT_CODE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_ID', 'TERM_CODE', 'TOTAL_UNITS', 'SUBJECT_ENROLLMENT_NUMBER', 'NUM_ENROLLED_STUDENTS', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_ID', 'TERM_CODE', 'TOTAL_UNITS', 'SUBJECT_ENROLLMENT_NUMBER', 'NUM_ENROLLED_STUDENTS', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TOTAL_UNITS", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TOTAL_UNITS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TOTAL_UNITS']
    if _dtype == "datetime64":
        table_1['TOTAL_UNITS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TOTAL_UNITS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TOTAL_UNITS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TOTAL_UNITS'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SUBJECT_ENROLLMENT_NUMBER", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SUBJECT_ENROLLMENT_NUMBER'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SUBJECT_ENROLLMENT_NUMBER']
    if _dtype == "datetime64":
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_ENROLLED_STUDENTS", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NUM_ENROLLED_STUDENTS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NUM_ENROLLED_STUDENTS']
    if _dtype == "datetime64":
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NUM_ENROLLED_STUDENTS'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="OFFER_DEPT_NAME", mode="mode")
    # MissingValueImputation
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].fillna(table_1["OFFER_DEPT_NAME"].mode().iloc[0])

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SUBJECT_ID', 'TERM_CODE', 'OFFER_DEPT_CODE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SUBJECT_ID', 'TERM_CODE', 'OFFER_DEPT_CODE'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SUBJECT_ID', 'TERM_CODE', 'OFFER_DEPT_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SUBJECT_ID', 'TERM_CODE', 'OFFER_DEPT_CODE'], keep='last').reset_index(drop=True)

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
def _prep_5(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT', 'DEPARTMENT_NAME', 'IS_DEGREE_GRANTING'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT', 'DEPARTMENT_NAME', 'IS_DEGREE_GRANTING'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_DEGREE_GRANTING", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip().upper()
    #     if s2 in ["Y", "YES", "TRUE", "T", "1"]:
    #         return "Y"
    #     if s2 in ["N", "NO", "FALSE", "F", "0"]:
    #         return "N"
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s2 = str(s).strip().upper()
        if s2 in ["Y", "YES", "TRUE", "T", "1"]:
            return "Y"
        if s2 in ["N", "NO", "FALSE", "F", "0"]:
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     name = row.get('DEPARTMENT_NAME', None)
    #     if name is None:
    #         return False
    #     return 'POLITICAL SCIENCE' in str(name).upper()
    # """)
    # Filter
    def filter_func(row):
        name = row.get('DEPARTMENT_NAME', None)
        if name is None:
            return False
        return 'POLITICAL SCIENCE' in str(name).upper()
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="is_degree_granting_int", func="""
    # def compute(row):
    #     return 1 if row.get('IS_DEGREE_GRANTING') == 'Y' else 0
    # """)
    # AddNewColumn
    def compute(row):
        return 1 if row.get('IS_DEGREE_GRANTING') == 'Y' else 0
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["is_degree_granting_int"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 5 ----------------
    # Original operator:
    # GroupBy(table_name="table_1", by=['DEPARTMENT', 'DEPARTMENT_NAME'], agg=[{'column': 'is_degree_granting_int', 'agg_func': 'max'}])
    # GroupBy
    table_1 = table_1.groupby(['DEPARTMENT', 'DEPARTMENT_NAME'], as_index=False).agg({'is_degree_granting_int': 'max'})

    # ---------------- Step 6 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="IS_DEGREE_GRANTING", func="""
    # def compute(row):
    #     return 'Y' if row.get('is_degree_granting_int', 0) == 1 else 'N'
    # """)
    # AddNewColumn
    def compute(row):
        return 'Y' if row.get('is_degree_granting_int', 0) == 1 else 'N'
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["IS_DEGREE_GRANTING"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['is_degree_granting_int'])
    # DropColumn
    table_1 = table_1.drop(columns=['is_degree_granting_int'], errors='ignore')

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_hass_attributes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_subject_codes = prepared_table_3
prepared_table_4 = _prep_4(tables['table_7'])
prepared_offerings = prepared_table_4
prepared_table_5 = _prep_5(tables['table_8'])
prepared_departments = prepared_table_5

# Start from prepared tables
subjects = prepared_subjects.copy()
hass_ref = prepared_hass_attributes.copy()
code_map = prepared_subject_codes.copy()
offerings = prepared_offerings.copy()
departments = prepared_departments.copy()

# 1) Identify Political Science by SUBJECT_CODE description and restrict to HASS-bearing attributes
# Political Science code is typically '17'. Use SUBJECT_CODE_DESC to be robust
pol_codes = code_map[code_map['SUBJECT_CODE_DESC'].str.contains('Political Science', case=False, na=False)]['SUBJECT_CODE'].unique()
pol_subjects = subjects[subjects['SUBJECT_CODE'].isin(pol_codes)].copy()

# HASS attributes live in COMM_REQ_ATTRIBUTE; keep rows where attribute present and exists in HASS ref
pol_subjects = pol_subjects.merge(hass_ref, left_on='COMM_REQ_ATTRIBUTE', right_on='hass_attribute', how='inner')

# 2) Add subject code description for output
pol_subjects = pol_subjects.merge(code_map[['SUBJECT_CODE','SUBJECT_CODE_DESC']], on='SUBJECT_CODE', how='left')

# 3) Aggregate enrollments across offerings per subject and attribute
offer_agg = offerings.groupby('SUBJECT_ID', as_index=False).agg(
    total_enrollment=('SUBJECT_ENROLLMENT_NUMBER','sum'),
    total_enrolled_students=('NUM_ENROLLED_STUDENTS','sum'),
    avg_units=('TOTAL_UNITS','mean')
)

pol_enriched = pol_subjects.merge(offer_agg, on='SUBJECT_ID', how='left')

# 4) Count degree-granting departments involved: join departments on department code and flag
dept_merge = pol_subjects[['SUBJECT_ID','DEPARTMENT_CODE']].drop_duplicates().merge(
    departments[['DEPARTMENT','IS_DEGREE_GRANTING']], left_on='DEPARTMENT_CODE', right_on='DEPARTMENT', how='left'
)
# normalize flag
dept_merge['is_deg'] = dept_merge['IS_DEGREE_GRANTING'].astype(str).str.upper().str.strip().eq('Y')

dept_counts = dept_merge.groupby('SUBJECT_ID', as_index=False)['is_deg'].sum().rename(columns={'is_deg':'num_deg_granting_depts'})

pol_enriched = pol_enriched.merge(dept_counts, on='SUBJECT_ID', how='left')

# 5) Final aggregation per HASS attribute (code), providing attribute name/description, counts, averages, totals
result = pol_enriched.groupby(['COMM_REQ_ATTRIBUTE','DESCRIPTION_ON_FORM','DESCRIPTION_IN_BULLETIN','SUBJECT_CODE_DESC'], as_index=False).agg(
    num_unique_subjects=('SUBJECT_ID','nunique'),
    average_units=('avg_units','mean'),
    total_enrollment=('total_enrollment','sum'),
    num_departments_granting_degrees=('num_deg_granting_depts','sum')
)

# Rename columns as requested
result = result.rename(columns={
    'COMM_REQ_ATTRIBUTE': 'attribute_code',
    'DESCRIPTION_ON_FORM': 'attribute_name',
    'DESCRIPTION_IN_BULLETIN': 'attribute_description',
    'SUBJECT_CODE_DESC': 'subject_code_description'
})

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
