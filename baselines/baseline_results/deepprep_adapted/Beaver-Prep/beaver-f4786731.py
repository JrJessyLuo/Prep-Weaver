import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME', 'INSTRUCTOR_NAME', 'DEPARTMENT', 'UNIT_CODE', 'UNIT', 'WAREHOUSE_LOAD_DATE'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME', 'INSTRUCTOR_NAME', 'DEPARTMENT', 'UNIT_CODE', 'UNIT', 'WAREHOUSE_LOAD_DATE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_COURSE_INSTRUCTOR_KEY", func="""
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
    table_1["LIBRARY_COURSE_INSTRUCTOR_KEY"] = table_1["LIBRARY_COURSE_INSTRUCTOR_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COURSE_NAME", func="""
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
    table_1["COURSE_NAME"] = table_1["COURSE_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="INSTRUCTOR_NAME", func="""
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
    table_1["INSTRUCTOR_NAME"] = table_1["INSTRUCTOR_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT", func="""
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
    table_1["DEPARTMENT"] = table_1["DEPARTMENT"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="UNIT_CODE", func="""
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
    table_1["UNIT_CODE"] = table_1["UNIT_CODE"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="UNIT", func="""
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
    table_1["UNIT"] = table_1["UNIT"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="WAREHOUSE_LOAD_DATE", date_format="%Y-%m-%d")
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
    if '%Y-%m-%d':
        table_1['WAREHOUSE_LOAD_DATE'] = table_1['WAREHOUSE_LOAD_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 9 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 10 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'WAREHOUSE_LOAD_DATE'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'WAREHOUSE_LOAD_DATE'], ascending=[True, True])

    # ---------------- Step 11 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep='last').reset_index(drop=True)

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
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
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
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_SUBJECT_OFFERED_KEY", func="""
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
    table_1["LIBRARY_SUBJECT_OFFERED_KEY"] = table_1["LIBRARY_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="term_code", func="""
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
    table_1["term_code"] = table_1["term_code"].apply(_std_apply)

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
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

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
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
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="WAREHOUSE_LOAD_DATE", date_format="%Y-%m-%d")
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
    if '%Y-%m-%d':
        table_1['WAREHOUSE_LOAD_DATE'] = table_1['WAREHOUSE_LOAD_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'WAREHOUSE_LOAD_DATE'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'WAREHOUSE_LOAD_DATE'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_instructors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_materials = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_subject_offered = prepared_table_3

# Assume prepared_instructors, prepared_materials, prepared_subject_offered are provided

# 1) Join instructors to materials on LIBRARY_COURSE_INSTRUCTOR_KEY
im = prepared_instructors.merge(
    prepared_materials,
    on='LIBRARY_COURSE_INSTRUCTOR_KEY',
    how='inner'
)

# 2) Join to subject offered on LIBRARY_SUBJECT_OFFERED_KEY
ims = im.merge(
    prepared_subject_offered[['LIBRARY_SUBJECT_OFFERED_KEY','SUBJECT_ID','SUBJECT_TITLE','term_code']],
    on='LIBRARY_SUBJECT_OFFERED_KEY',
    how='left'
)

# 3) Compute amount of material per instructor key and subject offered key
# Use count of unique LIBRARY_RESERVE_CATALOG_KEY as the amount of material
agg = (
    ims.groupby(['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_SUBJECT_OFFERED_KEY','INSTRUCTOR_NAME','COURSE_NAME'], dropna=False)
       .agg(amount_of_material=('LIBRARY_RESERVE_CATALOG_KEY','nunique'))
       .reset_index()
)

# 4) Select required columns and ensure uniqueness
result = agg[['INSTRUCTOR_NAME','COURSE_NAME','amount_of_material','LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_SUBJECT_OFFERED_KEY']].drop_duplicates()

# 'result' contains unique instructor names, course titles, amount of material, along with the instructor key and the key of subject offered.

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
