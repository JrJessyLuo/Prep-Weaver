import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return str(row.get('IS_DEGREE_GRANTING', '')).strip().upper() == 'Y'
    # """)
    # Filter
    def filter_func(row):
        return str(row.get('IS_DEGREE_GRANTING', '')).strip().upper() == 'Y'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CIP_PROGRAM_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CIP_PROGRAM_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CIP_PROGRAM_CODE']
    if _dtype == "datetime64":
        table_1['CIP_PROGRAM_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CIP_PROGRAM_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CIP_PROGRAM_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CIP_PROGRAM_CODE'] = _series.astype(str)

    # ---------------- Step 3 ----------------
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
    # DropNulls(table_name="table_1", subset=['CIP_PROGRAM_CODE', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['CIP_PROGRAM_CODE', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CIP_PROGRAM_CODE', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING', 'DEPARTMENT_NAME', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['CIP_PROGRAM_CODE', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING', 'DEPARTMENT_NAME', 'SCHOOL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['CIP_PROGRAM_CODE', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['CIP_PROGRAM_CODE', 'COURSE_LEVEL', 'IS_DEGREE_GRANTING', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], keep='last').reset_index(drop=True)

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
    # StandardizeString(table_name="table_1", column_name="CATEGORY_TITLE", func="""
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
    table_1["CATEGORY_TITLE"] = table_1["CATEGORY_TITLE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['PROGRAM_CODE', 'CATEGORY_CODE', 'CATEGORY_TITLE', 'VERSION'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['PROGRAM_CODE', 'CATEGORY_CODE', 'CATEGORY_TITLE', 'VERSION'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="PROGRAM_CODE", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['PROGRAM_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['PROGRAM_CODE']
    if _dtype == "datetime64":
        table_1['PROGRAM_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['PROGRAM_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['PROGRAM_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['PROGRAM_CODE'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CATEGORY_CODE", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CATEGORY_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CATEGORY_CODE']
    if _dtype == "datetime64":
        table_1['CATEGORY_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CATEGORY_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CATEGORY_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CATEGORY_CODE'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="VERSION", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['VERSION'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['VERSION']
    if _dtype == "datetime64":
        table_1['VERSION'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['VERSION'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['VERSION'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['VERSION'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['PROGRAM_CODE', 'CATEGORY_CODE', 'CATEGORY_TITLE', 'VERSION'])
    # SelectCol
    _cols = [c for c in ['PROGRAM_CODE', 'CATEGORY_CODE', 'CATEGORY_TITLE', 'VERSION'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['VERSION', 'PROGRAM_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['VERSION', 'PROGRAM_CODE'], keep='last').reset_index(drop=True)

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
prepared_courses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_cip_lookup = prepared_table_2

# Assume prepared tables are provided as dataframes: prepared_courses, prepared_cip_lookup
# Ensure join key types match
prepared_courses = prepared_courses.copy()
prepared_cip_lookup = prepared_cip_lookup.copy()
prepared_courses['CIP_PROGRAM_CODE'] = prepared_courses['CIP_PROGRAM_CODE'].astype(str).str.strip()
prepared_cip_lookup['PROGRAM_CODE'] = prepared_cip_lookup['PROGRAM_CODE'].astype(str).str.strip()

# Join courses to CIP lookup to bring in category/title/version
courses_cip = prepared_courses.merge(
    prepared_cip_lookup,
    left_on='CIP_PROGRAM_CODE',
    right_on='PROGRAM_CODE',
    how='left'
)

# Total number of courses for each course level per CIP category code
total_by_level = (
    courses_cip
    .groupby(['CATEGORY_CODE', 'COURSE_LEVEL'], dropna=False)
    .size()
    .reset_index(name='total_courses_for_level')
)

# Total number of degree-granting courses per CIP category code
deg_mask = courses_cip['IS_DEGREE_GRANTING'].astype(str).str.upper().str.strip() == 'Y'
degree_totals = (
    courses_cip.loc[deg_mask]
    .groupby(['CATEGORY_CODE'], dropna=False)
    .size()
    .reset_index(name='total_degree_granting_courses')
)

# Bring in representative category title and version (per category code). If multiple versions exist, pick the max version as string-numeric.
cip_meta = (
    courses_cip
    .assign(VERSION_num=pd.to_numeric(courses_cip['VERSION'], errors='coerce'))
    .sort_values(['CATEGORY_CODE', 'VERSION_num'], ascending=[True, False])
    .drop_duplicates(['CATEGORY_CODE'])
    [['CATEGORY_CODE', 'CATEGORY_TITLE', 'VERSION']]
)

# For department and school name, there can be many within a category; aggregate as unique lists
dept_school_agg = (
    courses_cip
    .groupby('CATEGORY_CODE', dropna=False)
    .agg({
        'DEPARTMENT_NAME': lambda s: sorted(pd.unique(s.dropna().astype(str))),
        'SCHOOL_NAME': lambda s: sorted(pd.unique(s.dropna().astype(str)))
    })
    .reset_index()
)

# Combine metadata and degree totals
category_summary = (
    cip_meta
    .merge(dept_school_agg, on='CATEGORY_CODE', how='left')
    .merge(degree_totals, on='CATEGORY_CODE', how='left')
)

# Final output per category and course level with totals
result = (
    total_by_level
    .merge(category_summary, on='CATEGORY_CODE', how='left')
    .rename(columns={
        'CATEGORY_TITLE': 'category_title',
        'VERSION': 'version',
        'DEPARTMENT_NAME': 'department_name_list',
        'SCHOOL_NAME': 'school_name_list'
    })
    [['CATEGORY_CODE', 'category_title', 'version', 'department_name_list', 'school_name_list', 'COURSE_LEVEL', 'total_courses_for_level', 'total_degree_granting_courses']]
    .sort_values(['CATEGORY_CODE', 'COURSE_LEVEL'])
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
