import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_CODE", func="""
    # def transform_func(s: str):
    #     return None if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        return None if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_DEPT_CODE"] = table_1["OFFER_DEPT_CODE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s: str):
    #     return None if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        return None if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["LIBRARY_SUBJECT_OFFERED_KEY"] = table_1["LIBRARY_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="term_code", func="""
    # def transform_func(s: str):
    #     return None if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        return None if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["term_code"] = table_1["term_code"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s: str):
    #     return None if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        return None if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s: str):
    #     return None if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        return None if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
    # def transform_func(s: str):
    #     return None if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        return None if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="RESPONSIBLE_FACULTY_NAME", func="""
    # def transform_func(s: str):
    #     return None if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        return None if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["RESPONSIBLE_FACULTY_NAME"] = table_1["RESPONSIBLE_FACULTY_NAME"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="RESPONSIBLE_FACULTY_MIT_ID", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['RESPONSIBLE_FACULTY_MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['RESPONSIBLE_FACULTY_MIT_ID']
    if _dtype == "datetime64":
        table_1['RESPONSIBLE_FACULTY_MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['RESPONSIBLE_FACULTY_MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['RESPONSIBLE_FACULTY_MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['RESPONSIBLE_FACULTY_MIT_ID'] = _series.astype(str)

    # ---------------- Step 9 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_SUBJECT_OFFERED_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_SUBJECT_OFFERED_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 10 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RESPONSIBLE_FACULTY_NAME', 'RESPONSIBLE_FACULTY_MIT_ID'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RESPONSIBLE_FACULTY_NAME', 'RESPONSIBLE_FACULTY_MIT_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 11 ----------------
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
    # MissingValueImputation(table_name="table_1", column_name="TERM_CODE", mode="mode")
    # MissingValueImputation
    table_1["TERM_CODE"] = table_1["TERM_CODE"].fillna(table_1["TERM_CODE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'TERM_CODE', 'SUBJECT_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'TERM_CODE', 'SUBJECT_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'TERM_CODE', 'SUBJECT_ID'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'TERM_CODE', 'SUBJECT_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep='first').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="INSTRUCTOR_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['INSTRUCTOR_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['INSTRUCTOR_NAME']
    if _dtype == "datetime64":
        table_1['INSTRUCTOR_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['INSTRUCTOR_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['INSTRUCTOR_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['INSTRUCTOR_NAME'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="DATE_FROM", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['DATE_FROM'] = table_1['DATE_FROM'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['DATE_FROM'] = table_1['DATE_FROM'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="DATE_TO", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['DATE_TO'] = table_1['DATE_TO'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['DATE_TO'] = table_1['DATE_TO'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'DEPARTMENT', 'DATE_FROM', 'DATE_TO', 'UNIT_CODE', 'UNIT'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'DEPARTMENT', 'DATE_FROM', 'DATE_TO', 'UNIT_CODE', 'UNIT'] if c in table_1.columns]
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
prepared_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_reserves = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_course_instructors = prepared_table_3

# prepared_offerings, prepared_reserves, prepared_course_instructors are assumed to be created per targets above

# Join offerings to reserves to associate reserve materials with offerings
off_res = prepared_offerings.merge(
    prepared_reserves[["LIBRARY_SUBJECT_OFFERED_KEY", "LIBRARY_RESERVE_CATALOG_KEY"]],
    on="LIBRARY_SUBJECT_OFFERED_KEY",
    how="left"
)

# Compute per-department metrics
# Unique courses offered per department: count distinct SUBJECT_ID within department
# Unique reserved materials per department: count distinct LIBRARY_RESERVE_CATALOG_KEY within department
# Unique instructors per department: count distinct RESPONSIBLE_FACULTY_NAME within department
agg = (
    off_res.groupby(["OFFER_DEPT_CODE", "OFFER_DEPT_NAME"], dropna=False)
    .agg(
        unique_courses=("SUBJECT_ID", lambda s: s.dropna().nunique()),
        unique_reserved_materials=("LIBRARY_RESERVE_CATALOG_KEY", lambda s: s.dropna().nunique()),
        unique_instructors=("RESPONSIBLE_FACULTY_NAME", lambda s: s.dropna().nunique())
    )
    .reset_index()
)

# Final selection and sorting
result = (
    agg.rename(columns={
        "OFFER_DEPT_NAME": "department_name",
        "unique_courses": "num_unique_courses",
        "unique_reserved_materials": "num_unique_reserved_materials",
        "unique_instructors": "num_unique_instructors"
    })
    .loc[:, ["department_name", "num_unique_courses", "num_unique_reserved_materials", "num_unique_instructors"]]
    .sort_values(by=["num_unique_courses", "department_name"], ascending=[False, True])
    .reset_index(drop=True)
)

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
