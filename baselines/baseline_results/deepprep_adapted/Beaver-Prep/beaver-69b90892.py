import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="LIBRARY_RESERVE_CATALOG_KEY", dtype="string")
    # CastType
    _dtype = 'string'
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
    # SelectCol(table_name="table_1", columns=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['library_reserve_catalog_key'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['library_reserve_catalog_key'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     val = row.get('CATALOG_TITLE')
    #     # keep rows with a non-null, non-empty title
    #     return pd.notna(val) and str(val).strip() != ''
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        val = row.get('CATALOG_TITLE')
        # keep rows with a non-null, non-empty title
        return pd.notna(val) and str(val).strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['library_reserve_catalog_key', 'CATALOG_TITLE'])
    # SelectCol
    _cols = [c for c in ['library_reserve_catalog_key', 'CATALOG_TITLE'] if c in table_1.columns]
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
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
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'SUBJECT_TITLE', 'term_code', 'SUBJECT_ID'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'SUBJECT_TITLE', 'term_code', 'SUBJECT_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_SUBJECT_OFFERED_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_SUBJECT_OFFERED_KEY'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_reserve_links = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_catalog = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_subject_offered = prepared_table_3

# Merge reserve links to catalog to get material titles (sometimes used as course title)
rl_cat = prepared_reserve_links.merge(
    prepared_catalog,
    left_on='LIBRARY_RESERVE_CATALOG_KEY',
    right_on='library_reserve_catalog_key',
    how='left'
)

# Merge to subject offered to get course titles
rl_full = rl_cat.merge(
    prepared_subject_offered[['LIBRARY_SUBJECT_OFFERED_KEY','SUBJECT_TITLE']],
    on='LIBRARY_SUBJECT_OFFERED_KEY',
    how='left'
)

# Define course title preference: use SUBJECT_TITLE when available; otherwise fall back to CATALOG_TITLE
rl_full['COURSE_TITLE'] = rl_full['SUBJECT_TITLE'].where(rl_full['SUBJECT_TITLE'].notna() & (rl_full['SUBJECT_TITLE'].astype(str).str.strip() != ''), rl_full['CATALOG_TITLE'])

# Aggregate per course title
result = (
    rl_full.groupby('COURSE_TITLE', dropna=False)
           .agg(total_reserved_materials=('LIBRARY_RESERVE_CATALOG_KEY','count'),
                distinct_material_status=('LIBRARY_MATERIAL_STATUS_KEY', lambda s: s.dropna().nunique()))
           .reset_index()
)

# Sort by total number of reserved materials descending
result = result.sort_values(['total_reserved_materials','COURSE_TITLE'], ascending=[False, True]).reset_index(drop=True)

target = result[['COURSE_TITLE','total_reserved_materials','distinct_material_status']]

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
