import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'SUBJECT_ID', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'SUBJECT_ID', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # StandardizeString(table_name="table_1", column_name="LIBRARY_MATERIAL_STATUS_KEY", func="""
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
    table_1["LIBRARY_MATERIAL_STATUS_KEY"] = table_1["LIBRARY_MATERIAL_STATUS_KEY"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_MATERIAL_STATUS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     # normalize common null spellings
    #     s_str = str(s).strip()
    #     if s_str.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     # collapse internal whitespace
    #     return " ".join(s_str.split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        # normalize common null spellings
        s_str = str(s).strip()
        if s_str.lower() in ["nan", "none", "null", ""]:
            return None
        # collapse internal whitespace
        return " ".join(s_str.split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["LIBRARY_MATERIAL_STATUS"] = table_1["LIBRARY_MATERIAL_STATUS"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="library_material_status_lkp", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # Key-based fill for missing descriptions (extendable lookup)
    #     fill_map = {
    #         "R": "Required Course Material",
    #         "U": "Unknown",
    #         "N": "Non-Required Course Material",
    #         "O": "Reserve only",
    #         "X": "No Required Textbook",
    #     }
    # 
    #     df["LIBRARY_MATERIAL_STATUS_KEY"] = df["LIBRARY_MATERIAL_STATUS_KEY"].astype(str).str.strip()
    #     df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].where(df["LIBRARY_MATERIAL_STATUS"].notna(),
    #                                                                       df["LIBRARY_MATERIAL_STATUS_KEY"].map(fill_map))
    # 
    #     # Fallback if still missing: use code (if present) as a second chance, else label as Unknown
    #     if "LIBRARY_MATERIAL_STATUS_CODE" in df.columns:
    #         df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].where(
    #             df["LIBRARY_MATERIAL_STATUS"].notna(),
    #             df["LIBRARY_MATERIAL_STATUS_CODE"].astype(str).str.strip().map(fill_map)
    #         )
    #     df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].fillna("Unknown")
    # 
    #     out = df[["LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS"]].copy()
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # Key-based fill for missing descriptions (extendable lookup)
        fill_map = {
            "R": "Required Course Material",
            "U": "Unknown",
            "N": "Non-Required Course Material",
            "O": "Reserve only",
            "X": "No Required Textbook",
        }

        df["LIBRARY_MATERIAL_STATUS_KEY"] = df["LIBRARY_MATERIAL_STATUS_KEY"].astype(str).str.strip()
        df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].where(df["LIBRARY_MATERIAL_STATUS"].notna(),
                                                                          df["LIBRARY_MATERIAL_STATUS_KEY"].map(fill_map))

        # Fallback if still missing: use code (if present) as a second chance, else label as Unknown
        if "LIBRARY_MATERIAL_STATUS_CODE" in df.columns:
            df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].where(
                df["LIBRARY_MATERIAL_STATUS"].notna(),
                df["LIBRARY_MATERIAL_STATUS_CODE"].astype(str).str.strip().map(fill_map)
            )
        df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].fillna("Unknown")

        out = df[["LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS"]].copy()
        return out
    library_material_status_lkp = process_tables(table_1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="library_material_status_lkp", subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep="last")
    # Deduplicate
    library_material_status_lkp = library_material_status_lkp.drop_duplicates(subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Sort(table_name="library_material_status_lkp", by=['LIBRARY_MATERIAL_STATUS_KEY'], ascending=[True])
    # Sort
    library_material_status_lkp = library_material_status_lkp.sort_values(by=['LIBRARY_MATERIAL_STATUS_KEY'], ascending=[True])

    # ---------------- Step 6 ----------------
    # Original operator:
    # Terminate(result=['library_material_status_lkp'])
    # Terminate
    result = {'library_material_status_lkp': library_material_status_lkp}
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
    # MissingValueImputation(table_name="table_1", column_name="CATALOG_YEAR", mode="median")
    # MissingValueImputation
    table_1["CATALOG_YEAR"] = table_1["CATALOG_YEAR"].fillna(table_1["CATALOG_YEAR"].median())

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CATALOG_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CATALOG_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CATALOG_YEAR']
    if _dtype == "datetime64":
        table_1['CATALOG_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CATALOG_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CATALOG_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CATALOG_YEAR'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="CATALOG_RECORD_CREATE_DATE", date_format="%Y-%m-%d")
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
    table_1['CATALOG_RECORD_CREATE_DATE'] = table_1['CATALOG_RECORD_CREATE_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['CATALOG_RECORD_CREATE_DATE'] = table_1['CATALOG_RECORD_CREATE_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['library_reserve_catalog_key', 'CATALOG_YEAR', 'CATALOG_RECORD_CREATE_DATE'])
    # SelectCol
    _cols = [c for c in ['library_reserve_catalog_key', 'CATALOG_YEAR', 'CATALOG_RECORD_CREATE_DATE'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # Rename(table_name="table_1", rename_map=[{'old_name': 'OFFER_DEPT_NAME', 'new_name': 'OFFER_DEPT_NAME'}, {'old_name': 'NUM_ENROLLED_STUDENTS', 'new_name': 'NUM_ENROLLED_STUDENTS'}, {'old_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'new_name': 'LIBRARY_SUBJECT_OFFERED_KEY'}, {'old_name': 'term_code', 'new_name': 'term_code'}])
    # Rename
    table_1 = table_1.rename(columns={'OFFER_DEPT_NAME': 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS': 'NUM_ENROLLED_STUDENTS', 'LIBRARY_SUBJECT_OFFERED_KEY': 'LIBRARY_SUBJECT_OFFERED_KEY', 'term_code': 'term_code'})

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
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
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
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].apply(_std_apply)

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
    # DropNulls(table_name="table_1", subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_course_materials = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_material_status = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_catalog = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
prepared_subject_offered = prepared_table_4

# Assume the prepared tables are dataframes: prepared_course_materials (pcm), prepared_material_status (pms), prepared_catalog (pcat), prepared_subject_offered (pso)

# 1) Integrate tables
m1 = pcm.merge(pcat, left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key', how='inner')
m2 = m1.merge(pms, on='LIBRARY_MATERIAL_STATUS_KEY', how='left')
full = m2.merge(pso, left_on=['LIBRARY_SUBJECT_OFFERED_KEY','TERM_CODE'], right_on=['LIBRARY_SUBJECT_OFFERED_KEY','term_code'], how='left')

# 2) Filter to books cataloged on or after 2000.
# Prefer CATALOG_YEAR when available; fall back to parsed year from CATALOG_RECORD_CREATE_DATE if CATALOG_YEAR is 0/NaN.
cat_year = pd.to_numeric(full['CATALOG_YEAR'], errors='coerce')
# Parse year from date like '19-APR-12' -> 2012 (assuming YY>=50 => 1900s else 2000s). Adjust as needed for actual format.
create_dt = pd.to_datetime(full['CATALOG_RECORD_CREATE_DATE'], errors='coerce', infer_datetime_format=True)
create_year = create_dt.dt.year

use_year = cat_year.where(cat_year.notna() & (cat_year > 0), create_year)
filtered = full[use_year >= 2000].copy()

# 3) Prepare aggregations: count of catalog items and total enrolled students per material status and department.
# Each row corresponds to a catalog item tied to a course offering; count distinct catalog items by key to avoid double-counting duplicates per join.
filtered['catalog_item'] = filtered['library_reserve_catalog_key']

# For student totals, sum NUM_ENROLLED_STUDENTS across associated offerings; convert to numeric safely.
filtered['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(filtered['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0)

# Detail grouping
detail = (
    filtered.groupby(['LIBRARY_MATERIAL_STATUS', 'OFFER_DEPT_NAME'], dropna=False)
    .agg(num_catalog_items=('catalog_item','nunique'), total_enrolled_students=('NUM_ENROLLED_STUDENTS','sum'))
    .reset_index()
)

# Subtotals per status
status_sub = (
    filtered.groupby(['LIBRARY_MATERIAL_STATUS'], dropna=False)
    .agg(num_catalog_items=('catalog_item','nunique'), total_enrolled_students=('NUM_ENROLLED_STUDENTS','sum'))
    .reset_index()
)
status_sub['OFFER_DEPT_NAME'] = 'Subtotal'

# Grand total
grand = pd.DataFrame({
    'LIBRARY_MATERIAL_STATUS': ['Grand Total'],
    'OFFER_DEPT_NAME': ['Grand Total'],
    'num_catalog_items': [filtered['catalog_item'].nunique()],
    'total_enrolled_students': [filtered['NUM_ENROLLED_STUDENTS'].sum()]
})

# Combine
result = pd.concat([detail, status_sub, grand], ignore_index=True)

# Final select/rename as needed for output
result = result.rename(columns={
    'LIBRARY_MATERIAL_STATUS': 'material_status',
    'OFFER_DEPT_NAME': 'department_name',
    'num_catalog_items': 'num_associated_catalog_items',
    'total_enrolled_students': 'total_enrolled_students'
})

# Optionally sort for presentation (not required by schema)
# result = result.sort_values(['material_status','department_name'])

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
