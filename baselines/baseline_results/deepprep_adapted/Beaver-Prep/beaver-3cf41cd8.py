import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # OutlierDetection(table_name="table_1", column_name="NUM_ENROLLED_STUDENTS", action="delete")
    # OutlierDetection (IQR method)
    _q1 = table_1['NUM_ENROLLED_STUDENTS'].quantile(0.25)
    _q3 = table_1['NUM_ENROLLED_STUDENTS'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] = table_1['NUM_ENROLLED_STUDENTS'].apply(lambda x: True if x < _low or x > _high else False)
    if 'delete' == 'delete':
        table_1 = table_1[table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] == False]
        table_1.drop(columns=['table_1_NUM_ENROLLED_STUDENTS_is_outlier'], inplace=True)
    elif 'delete' == 'add_tag':
        table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] = table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_SUBJECT_OFFERED_KEY", func="""
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
    table_1["TIP_SUBJECT_OFFERED_KEY"] = table_1["TIP_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
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
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_CODE", func="""
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
    table_1["OFFER_DEPT_CODE"] = table_1["OFFER_DEPT_CODE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_SCHOOL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return " ".join(str(s).split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return " ".join(str(s).split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_SCHOOL_NAME"] = table_1["OFFER_SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
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

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return " ".join(str(s).split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return " ".join(str(s).split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
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
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 9 ----------------
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

    # ---------------- Step 10 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 11 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'OFFER_DEPT_CODE', 'OFFER_SCHOOL_NAME', 'COURSE_NUMBER', 'SUBJECT_TITLE', 'SUBJECT_ID', 'NUM_ENROLLED_STUDENTS'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'OFFER_DEPT_CODE', 'OFFER_SCHOOL_NAME', 'COURSE_NUMBER', 'SUBJECT_TITLE', 'SUBJECT_ID', 'NUM_ENROLLED_STUDENTS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 12 ----------------
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
    # Deduplicate(table_name="table_1", subset=['subject_id', 'TERM_CODE', 'ISBN'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['subject_id', 'TERM_CODE', 'ISBN'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="subject_id", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     # normalize internal whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     # if it looks like a number with trailing .0, remove it (common ingestion artifact)
    #     if re.fullmatch(r'\d+\.0', s):
    #         s = s[:-2]
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip().strip('"').strip("'")
        # normalize internal whitespace
        s = re.sub(r'\s+', ' ', s)
        # if it looks like a number with trailing .0, remove it (common ingestion artifact)
        if re.fullmatch(r'\d+\.0', s):
            s = s[:-2]
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["subject_id"] = table_1["subject_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ISBN", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     if s == '' or s.lower() == 'nan':
    #         return None
    #     # keep only ISBN characters, remove hyphens/spaces; normalize X
    #     s = re.sub(r'[^0-9Xx]', '', s)
    #     s = s.upper()
    #     return s if s != '' else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip().strip('"').strip("'")
        if s == '' or s.lower() == 'nan':
            return None
        # keep only ISBN characters, remove hyphens/spaces; normalize X
        s = re.sub(r'[^0-9Xx]', '', s)
        s = s.upper()
        return s if s != '' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ISBN"] = table_1["ISBN"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     if s == '' or s.lower() == 'nan':
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip().strip('"').strip("'")
        if s == '' or s.lower() == 'nan':
            return None
        return s
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
    # Rename(table_name="table_1", rename_map=[{'old_name': 'subject_id', 'new_name': 'SUBJECT_ID'}])
    # Rename
    table_1 = table_1.rename(columns={'subject_id': 'SUBJECT_ID'})

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SUBJECT_ID', 'TERM_CODE', 'ISBN'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SUBJECT_ID', 'TERM_CODE', 'ISBN'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_ID', 'TERM_CODE', 'ISBN'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_ID', 'TERM_CODE', 'ISBN'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_materials = prepared_table_2

# Assume prepared_offerings and prepared_materials already materialized per targets.
# Standardize key casing/whitespace
prepared_offerings['SUBJECT_ID'] = prepared_offerings['SUBJECT_ID'].astype(str).str.strip()
prepared_materials['SUBJECT_ID'] = prepared_materials['SUBJECT_ID'].astype(str).str.strip()
prepared_offerings['TERM_CODE'] = prepared_offerings['TERM_CODE'].astype(str).str.strip()
prepared_materials['TERM_CODE'] = prepared_materials['TERM_CODE'].astype(str).str.strip()

# Join on SUBJECT_ID and TERM_CODE to align materials with offerings in the same term
merged = prepared_offerings.merge(
    prepared_materials,
    how='left',
    left_on=['SUBJECT_ID', 'TERM_CODE'],
    right_on=['SUBJECT_ID', 'TERM_CODE']
)

# Compute distinct ISBNs per offering (excluding null/blank)
merged['ISBN_clean'] = merged['ISBN'].where(merged['ISBN'].notna() & (merged['ISBN'].astype(str).str.strip() != ''), pd.NA)

agg = (
    merged.groupby([
        'OFFER_DEPT_CODE', 'OFFER_SCHOOL_NAME', 'COURSE_NUMBER', 'SUBJECT_TITLE', 'TERM_CODE'
    ], dropna=False)
    .agg(
        total_enrolled=('NUM_ENROLLED_STUDENTS', 'first'),  # enrollment is per offering row
        distinct_catalog_isbns=('ISBN_clean', pd.Series.nunique)
    )
    .reset_index()
)

# Build summary row for current term (assume current term = max TERM_CODE present in offerings)
current_term = prepared_offerings['TERM_CODE'].dropna().astype(str).max()
cur = merged[merged['TERM_CODE'] == current_term]
cur_total_students = cur.drop_duplicates(['SUBJECT_ID', 'TERM_CODE'])['NUM_ENROLLED_STUDENTS'].sum()
cur_distinct_isbns = cur['ISBN_clean'].nunique()

summary_row = pd.DataFrame([
    {
        'OFFER_DEPT_CODE': 'TOTAL:',
        'OFFER_SCHOOL_NAME': None,
        'COURSE_NUMBER': None,
        'SUBJECT_TITLE': None,
        'total_enrolled': int(cur_total_students),
        'TERM_CODE': None,
        'distinct_catalog_isbns': int(cur_distinct_isbns)
    }
])

# Final result with requested columns
result = agg.rename(columns={
    'OFFER_DEPT_CODE': 'department',
    'OFFER_SCHOOL_NAME': 'school',
    'COURSE_NUMBER': 'course_number',
    'SUBJECT_TITLE': 'subject_title',
    'TERM_CODE': 'term_code',
    'total_enrolled': 'total_number_of_enrolled_students',
    'distinct_catalog_isbns': 'count_of_distinct_catalog_isbns'
})

summary_out = summary_row.rename(columns={
    'OFFER_DEPT_CODE': 'department',
    'OFFER_SCHOOL_NAME': 'school',
    'COURSE_NUMBER': 'course_number',
    'SUBJECT_TITLE': 'subject_title',
    'TERM_CODE': 'term_code',
    'total_enrolled': 'total_number_of_enrolled_students',
    'distinct_catalog_isbns': 'count_of_distinct_catalog_isbns'
})

final = pd.concat([result, summary_out], ignore_index=True)

final = final[['department', 'school', 'course_number', 'subject_title', 'total_number_of_enrolled_students', 'term_code', 'count_of_distinct_catalog_isbns']]

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
