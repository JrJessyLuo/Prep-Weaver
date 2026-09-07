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
    # SelectCol(table_name="table_1", columns=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_COURSE_INSTRUCTOR_KEY'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_COURSE_INSTRUCTOR_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_COURSE_INSTRUCTOR_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_COURSE_INSTRUCTOR_KEY'], how='any').reset_index(drop=True)

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
    # Deduplicate(table_name="table_1", subset=['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="LIBRARY_MATERIAL_STATUS", mode="mode")
    # MissingValueImputation
    table_1["LIBRARY_MATERIAL_STATUS"] = table_1["LIBRARY_MATERIAL_STATUS"].fillna(table_1["LIBRARY_MATERIAL_STATUS"].mode().iloc[0])

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE', 'LIBRARY_MATERIAL_STATUS'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE', 'LIBRARY_MATERIAL_STATUS'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_DESCRIPTION", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["TERM_DESCRIPTION"] = table_1["TERM_DESCRIPTION"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['term_code', 'TERM_DESCRIPTION'])
    # SelectCol
    _cols = [c for c in ['term_code', 'TERM_DESCRIPTION'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['term_code'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['term_code'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['term_code'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['term_code'], keep='last').reset_index(drop=True)

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
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # normalize whitespace
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # normalize whitespace
        return " ".join(str(s).strip().split())
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
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
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
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TERM_CODE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TERM_CODE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_library_reserves = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_material_status_ref = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_terms = prepared_table_3
prepared_table_4 = _prep_4(tables['table_8'])
prepared_subject_org = prepared_table_4

# Start from prepared tables
res = prepared_library_reserves.copy()
status_ref = prepared_material_status_ref.copy()
terms = prepared_terms.copy()
org = prepared_subject_org.copy()

# Join status reference (many-to-one)
res1 = res.merge(status_ref, on='LIBRARY_MATERIAL_STATUS_KEY', how='left')

# Join term description
res2 = res1.merge(terms, left_on='TERM_CODE', right_on='term_code', how='left')

# Join organizational mapping by term to enable counting occurrences across departments and schools
res_org = res2.merge(org[['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME']], on='TERM_CODE', how='left')

# Derive instructor id from composite if needed (assume instructor component precedes term in LIBRARY_COURSE_INSTRUCTOR_KEY separated by '-')
# If the composite structure is different, adjust parsing accordingly.
def extract_instructor(x):
    if pd.isna(x):
        return pd.NA
    # Example formats observed like '4.602-VANCE2010SP:4.602'; take segment before TERM_CODE by splitting on ':' first
    left = str(x).split(':')[0]
    # then split on '-' to separate subject and instructor+term; take middle if present
    parts = left.split('-')
    if len(parts) >= 2:
        return parts[1]
    return left

res_org['INSTRUCTOR_TOKEN'] = res_org['LIBRARY_COURSE_INSTRUCTOR_KEY'].apply(extract_instructor)

# Aggregate metrics per material status code and term code
agg = res_org.groupby(['LIBRARY_MATERIAL_STATUS_CODE','TERM_CODE','LIBRARY_MATERIAL_STATUS','TERM_DESCRIPTION'], dropna=False).agg(
    total_courses=pd.NamedAgg(column='SUBJECT_ID', aggfunc=lambda s: s.dropna().nunique()),
    total_materials=pd.NamedAgg(column='LIBRARY_RESERVE_CATALOG_KEY', aggfunc=lambda s: s.dropna().nunique()),
    occurrences_in_departments=pd.NamedAgg(column='DEPARTMENT_CODE', aggfunc=lambda s: s.dropna().nunique()),
    occurrences_in_schools=pd.NamedAgg(column='SCHOOL_NAME', aggfunc=lambda s: s.dropna().nunique()),
    total_instructors=pd.NamedAgg(column='INSTRUCTOR_TOKEN', aggfunc=lambda s: s.dropna().nunique())
).reset_index()

# Final selection and ordering
target = agg.rename(columns={
    'LIBRARY_MATERIAL_STATUS_CODE': 'material_status_code',
    'LIBRARY_MATERIAL_STATUS': 'material_status',
    'TERM_CODE': 'term_code',
    'TERM_DESCRIPTION': 'term_description'
})

# target now has: material_status_code, material_status, term_code, term_description,
# total_courses, total_materials, occurrences_in_departments, occurrences_in_schools, total_instructors

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
