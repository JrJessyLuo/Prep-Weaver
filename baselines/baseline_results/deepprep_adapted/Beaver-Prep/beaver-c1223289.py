import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="WAREHOUSE_LOAD_DATE", date_format="%d-%b-%y")
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
    table_1['WAREHOUSE_LOAD_DATE'] = table_1['WAREHOUSE_LOAD_DATE'].apply(_sd_parse)
    if '%d-%b-%y':
        table_1['WAREHOUSE_LOAD_DATE'] = table_1['WAREHOUSE_LOAD_DATE'].dt.strftime('%d-%b-%y')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip()
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s2 = str(s).strip()
        return s2
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
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip()
    #     # keep original "Last, First" formatting, just trim
    #     return s2 if s2.lower() != 'nan' else ''
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s2 = str(s).strip()
        # keep original "Last, First" formatting, just trim
        return s2 if s2.lower() != 'nan' else ''
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
    # AddNewColumn(table_name="table_1", new_column_name="MOIRA_LIST_MEMBER_FULL_NAME_FILLED", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     v = row.get('MOIRA_LIST_MEMBER_FULL_NAME', None)
    #     if v is None:
    #         v = ''
    #     v = str(v).strip()
    #     if v == '' or v.lower() == 'nan':
    #         return str(row.get('moira_list_member', '')).strip()
    #     return v
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        v = row.get('MOIRA_LIST_MEMBER_FULL_NAME', None)
        if v is None:
            v = ''
        v = str(v).strip()
        if v == '' or v.lower() == 'nan':
            return str(row.get('moira_list_member', '')).strip()
        return v
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["MOIRA_LIST_MEMBER_FULL_NAME_FILLED"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['MOIRA_LIST_MEMBER_FULL_NAME'])
    # DropColumn
    table_1 = table_1.drop(columns=['MOIRA_LIST_MEMBER_FULL_NAME'], errors='ignore')

    # ---------------- Step 6 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'MOIRA_LIST_MEMBER_FULL_NAME_FILLED', 'new_name': 'MOIRA_LIST_MEMBER_FULL_NAME'}])
    # Rename
    table_1 = table_1.rename(columns={'MOIRA_LIST_MEMBER_FULL_NAME_FILLED': 'MOIRA_LIST_MEMBER_FULL_NAME'})

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME'], keep='last').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="INSTRUCTOR_NAME", func="""
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
    table_1["INSTRUCTOR_NAME"] = table_1["INSTRUCTOR_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['INSTRUCTOR_NAME', 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME', 'DATE_FROM', 'DATE_TO'])
    # SelectCol
    _cols = [c for c in ['INSTRUCTOR_NAME', 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME', 'DATE_FROM', 'DATE_TO'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="LIBRARY_RESERVE_CATALOG_KEY", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['LIBRARY_RESERVE_CATALOG_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['LIBRARY_RESERVE_CATALOG_KEY']
    if _dtype == "datetime64":
        table_1['LIBRARY_RESERVE_CATALOG_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['LIBRARY_RESERVE_CATALOG_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['LIBRARY_RESERVE_CATALOG_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['LIBRARY_RESERVE_CATALOG_KEY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep='first').reset_index(drop=True)

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # OutlierDetection(table_name="table_1", column_name="NUM_ENROLLED_STUDENTS", action="add_tag")
    # OutlierDetection (IQR method)
    _q1 = table_1['NUM_ENROLLED_STUDENTS'].quantile(0.25)
    _q3 = table_1['NUM_ENROLLED_STUDENTS'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] = table_1['NUM_ENROLLED_STUDENTS'].apply(lambda x: True if x < _low or x > _high else False)
    if 'add_tag' == 'delete':
        table_1 = table_1[table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] == False]
        table_1.drop(columns=['table_1_NUM_ENROLLED_STUDENTS_is_outlier'], inplace=True)
    elif 'add_tag' == 'add_tag':
        table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] = table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_SUBJECT_OFFERED_KEY", func="""
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
    table_1["LIBRARY_SUBJECT_OFFERED_KEY"] = table_1["LIBRARY_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="term_code", func="""
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
    table_1["term_code"] = table_1["term_code"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
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
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_ENROLLED_STUDENTS", dtype="int")
    # CastType
    _dtype = 'int'
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
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'NUM_ENROLLED_STUDENTS'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'NUM_ENROLLED_STUDENTS'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_6'])
prepared_moira_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_course_instructors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_course_offerings_link = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_subject_offerings = prepared_table_4

# Assume prepared_* DataFrames exist per targets

# 1) Filter to the specified mailing list
ml = prepared_moira_members.copy()
ml['MOIRA_LIST_KEY_norm'] = ml['MOIRA_LIST_KEY'].str.strip().str.lower()
ml_f = ml[ml['MOIRA_LIST_KEY_norm'] == 'keeper-zephyr']

# 2) Normalize names for joining
left = ml_f.rename(columns={'MOIRA_LIST_MEMBER_FULL_NAME':'INSTRUCTOR_NAME'})
left['INSTRUCTOR_NAME'] = left['INSTRUCTOR_NAME'].astype(str).str.strip()
ci = prepared_course_instructors.copy()
ci['INSTRUCTOR_NAME'] = ci['INSTRUCTOR_NAME'].astype(str).str.strip()

# 3) Join mailing list members to instructor assignments by name
m1 = pd.merge(left, ci, on='INSTRUCTOR_NAME', how='inner')

# 4) Link to offerings via course-instructor key
b = prepared_course_offerings_link.copy()
m2 = pd.merge(m1, b, on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')

# 5) Join to subject offerings for enrollment
so = prepared_subject_offerings.copy()
m3 = pd.merge(m2, so, on='LIBRARY_SUBJECT_OFFERED_KEY', how='left')

# 6) Derive publication year from DATE_FROM/DATE_TO (take years)
def parse_year(s):
    # Expect formats like '04-JAN-10' -> 2010; handle 2- or 4-digit years
    if pd.isna(s):
        return pd.NA
    s = str(s)
    # simple extract last 2 or 4 digit year
    m4 = re.search(r'(19|20)\d{2}', s)
    if m4:
        return int(m4.group(0))
    m2d = re.search(r'(\d{2})(?!\d)', s)
    if m2d:
        y = int(m2d.group(1))
        return 2000 + y if y <= 49 else 1900 + y
    return pd.NA

m3['YEAR_FROM'] = m3['DATE_FROM'].apply(parse_year)
m3['YEAR_TO'] = m3['DATE_TO'].apply(parse_year)

# 7) Aggregate per instructor (list), instructor name, earliest/latest publication years, total enrolled students
# Treat NUM_ENROLLED_STUDENTS as numeric and sum over offerings linked to that instructor
m3['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(m3.get('NUM_ENROLLED_STUDENTS'), errors='coerce')

agg = (m3.groupby(['MOIRA_LIST_KEY', 'INSTRUCTOR_NAME'], dropna=False)
         .agg(earliest_publication_year=('YEAR_FROM', 'min'),
              latest_publication_year=('YEAR_TO', 'max'),
              total_enrolled_students=('NUM_ENROLLED_STUDENTS', 'sum'))
         .reset_index())

# 8) Prepare final columns as requested
result = agg.rename(columns={'MOIRA_LIST_KEY':'mailing_list',
                             'INSTRUCTOR_NAME':'instructor_name'})
# If multiple lists somehow present after filtering, keep as-is

output = result[['mailing_list','instructor_name','earliest_publication_year','latest_publication_year','total_enrolled_students']]

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
