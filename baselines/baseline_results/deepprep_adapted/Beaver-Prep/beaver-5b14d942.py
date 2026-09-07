import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['term_code', 'TERM_DESCRIPTION', 'IS_CURRENT_TERM'])
    # SelectCol
    _cols = [c for c in ['term_code', 'TERM_DESCRIPTION', 'IS_CURRENT_TERM'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row['IS_CURRENT_TERM']).strip().upper() == 'Y'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row['IS_CURRENT_TERM']).strip().upper() == 'Y'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # keep rows with non-null core identifiers
    #     return (row.get('TERM_CODE') is not None) and (row.get('SUBJECT_ID') is not None)
    # """)
    # Filter
    def filter_func(row):
        # keep rows with non-null core identifiers
        return (row.get('TERM_CODE') is not None) and (row.get('SUBJECT_ID') is not None)
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s: str):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s: str):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COURSE_NUMBER", func="""
    # def transform_func(s: str):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["COURSE_NUMBER"] = table_1["COURSE_NUMBER"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s: str):
    #     return " ".join(s.split()) if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        return " ".join(s.split()) if isinstance(s, str) else s
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

    # ---------------- Step 7 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="TOTAL_UNITS", mode="median")
    # MissingValueImputation
    table_1["TOTAL_UNITS"] = table_1["TOTAL_UNITS"].fillna(table_1["TOTAL_UNITS"].median())

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'COURSE_NUMBER', 'SUBJECT_TITLE', 'HGN_CODE', 'HGN_CODE_DESC', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RESPONSIBLE_FACULTY_NAME', 'RESPONSIBLE_FACULTY_MIT_ID', 'TOTAL_UNITS'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'COURSE_NUMBER', 'SUBJECT_TITLE', 'HGN_CODE', 'HGN_CODE_DESC', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RESPONSIBLE_FACULTY_NAME', 'RESPONSIBLE_FACULTY_MIT_ID', 'TOTAL_UNITS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID', 'COURSE_NUMBER'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID', 'COURSE_NUMBER'], keep='last').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'FULL_NAME', 'EMAIL_ADDRESS'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'FULL_NAME', 'EMAIL_ADDRESS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FULL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        return " ".join(str(s).strip().split())
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
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        return str(s).strip().lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["EMAIL_ADDRESS"] = table_1["EMAIL_ADDRESS"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['MIT_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['MIT_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MIT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MIT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'FULL_NAME', 'EMAIL_ADDRESS'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'FULL_NAME', 'EMAIL_ADDRESS'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_8'])
prepared_current_term = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_subject_offerings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_people_directory = prepared_table_3

# Assume prepared_current_term, prepared_subject_offerings, prepared_people_directory are DataFrames
cur_term = prepared_current_term[prepared_current_term['IS_CURRENT_TERM'].str.upper().eq('Y')]
# Join subjects to current term
cur_subjects = prepared_subject_offerings.merge(cur_term[['term_code','TERM_DESCRIPTION']], left_on='TERM_CODE', right_on='term_code', how='inner')
# Enrich with person directory (name/email may be missing if MIT_ID null or no match)
cur_subjects = cur_subjects.merge(prepared_people_directory[['MIT_ID','FULL_NAME','EMAIL_ADDRESS']], left_on='RESPONSIBLE_FACULTY_MIT_ID', right_on='MIT_ID', how='left')
# Compute per-course-type counts and average units as requested at the course/department/HGN granularity
# Coerce TOTAL_UNITS to numeric for averaging
cur_subjects['TOTAL_UNITS_NUM'] = pd.to_numeric(cur_subjects['TOTAL_UNITS'], errors='coerce')
# Prepare final details
result = cur_subjects.assign(
    academic_year=cur_subjects['TERM_DESCRIPTION'].str.extract(r'(\d{4}-\d{4})', expand=False),
    term_code=cur_subjects['TERM_CODE'],
    hgn_code=cur_subjects['HGN_CODE'],
    department_name=cur_subjects['OFFER_DEPT_NAME'],
    person_in_charge_name=cur_subjects['FULL_NAME'].fillna(cur_subjects['RESPONSIBLE_FACULTY_NAME']),
    person_in_charge_email=cur_subjects['EMAIL_ADDRESS']
)
# Aggregate total number of types of courses (distinct SUBJECT_ID) and average units by dept and HGN (and optionally course number)
aggr = result.groupby(['academic_year','term_code','hgn_code','department_name','person_in_charge_name','person_in_charge_email'], dropna=False).agg(
    total_number_of_types_of_courses=pd.NamedAgg(column='SUBJECT_ID', aggfunc=lambda s: s.nunique()),
    average_number_of_units=pd.NamedAgg(column='TOTAL_UNITS_NUM', aggfunc='mean')
).reset_index()
# Rename columns to match question phrasing
aggr = aggr[['academic_year','term_code','hgn_code','total_number_of_types_of_courses','average_number_of_units','department_name','person_in_charge_name','person_in_charge_email']]
# target output
target = aggr

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
