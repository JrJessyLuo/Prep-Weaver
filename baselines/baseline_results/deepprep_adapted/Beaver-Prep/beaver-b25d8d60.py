import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="COURSE_NAME", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return len(s) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip()
        return len(s) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['COURSE_NAME'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="LIBRARY_COURSE_INSTRUCTOR_KEY", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return len(s) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip()
        return len(s) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['LIBRARY_COURSE_INSTRUCTOR_KEY'].apply(_err_apply)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="INSTRUCTOR_NAME", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return len(s) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip()
        return len(s) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['INSTRUCTOR_NAME'].apply(_err_apply)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'COURSE_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'COURSE_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'COURSE_NAME'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'COURSE_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep='last').reset_index(drop=True)

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
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE'], how='any').reset_index(drop=True)

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
def _prep_3(table_1):
    return table_1.copy()
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CalculateStatistic(table_name="table_1", statistic_name="row_count", func="""
    # def calculate_stat(df):
    #     return len(df)
    # """)
    # CalculateStatistic -> statistic_table
    def calculate_stat(df):
        return len(df)
    _stat_val = calculate_stat(table_1)
    _stat_row = pd.DataFrame({'operator': ['CalculateStatistic(table_name="table_1", statistic_name="row_count", func="""\ndef calculate_stat(df):\n    return len(df)\n""")'], 'statistic_name': ['row_count'], 'value': [_stat_val]})
    try:
        statistic_table = pd.concat([statistic_table, _stat_row], ignore_index=True)
    except NameError:
        statistic_table = _stat_row

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
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
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACADEMIC_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACADEMIC_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACADEMIC_YEAR']
    if _dtype == "datetime64":
        table_1['ACADEMIC_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACADEMIC_YEAR'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR'], keep='first').reset_index(drop=True)

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
prepared_instructors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_material_assignments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_table_4 = _prep_4(tables['table_3'])
prepared_subject_terms = prepared_table_4

# Merge instructors with material assignments
m = prepared_instructors.merge(
    prepared_material_assignments,
    on='LIBRARY_COURSE_INSTRUCTOR_KEY',
    how='left'
)

# If SUBJECT_ID is not present in prepared_material_assignments, attempt to derive it from LIBRARY_COURSE_INSTRUCTOR_KEY prefix before ':'
if 'SUBJECT_ID' not in m.columns or m['SUBJECT_ID'].isna().all():
    # Example LIBRARY_COURSE_INSTRUCTOR_KEY looks like '4.602-VANCE2010SP:4.602'
    # Prefer the segment after the colon if present; else take leading subject-like token
    subj_after_colon = m['LIBRARY_COURSE_INSTRUCTOR_KEY'].str.split(':').str[-1]
    m['SUBJECT_ID'] = subj_after_colon

# Join to subject terms on SUBJECT_ID and TERM_CODE to get academic year
m = m.merge(
    prepared_subject_terms[['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR']],
    on=['SUBJECT_ID', 'TERM_CODE'],
    how='left'
)

# Aggregate per instructor
agg = m.groupby('INSTRUCTOR_NAME').agg(
    unique_courses=('COURSE_NAME', lambda s: s.dropna().nunique()),
    total_material_assignments=('LIBRARY_RESERVE_CATALOG_KEY', 'count'),
    avg_publication_year=('ACADEMIC_YEAR', 'mean'),
    distinct_status=('LIBRARY_MATERIAL_STATUS_KEY', lambda s: s.dropna().nunique())
).reset_index()

# Final formatting and sorting
agg['avg_publication_year'] = agg['avg_publication_year'].round(2)
result = agg.sort_values(['unique_courses', 'INSTRUCTOR_NAME'], ascending=[False, True])

target = result[['INSTRUCTOR_NAME', 'unique_courses', 'total_material_assignments', 'avg_publication_year', 'distinct_status']]

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
