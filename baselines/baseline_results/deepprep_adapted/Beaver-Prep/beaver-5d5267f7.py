import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['TIP_SUBJECT_OFFERED_KEY', 'ISBN', 'RECORD_COUNT', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['TIP_SUBJECT_OFFERED_KEY', 'ISBN', 'RECORD_COUNT', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_MATERIAL_STATUS_KEY', 'TIP_MATERIAL_KEY', 'subject_id', 'TERM_CODE'])
    # SelectCol
    _cols = [c for c in ['TIP_MATERIAL_STATUS_KEY', 'TIP_MATERIAL_KEY', 'subject_id', 'TERM_CODE'] if c in table_1.columns]
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
    # DropColumn(table_name="table_1", drop_columns=['WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="tip_material_status_key", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return s2 if s2 != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s2 = str(s).strip()
        return s2 if s2 != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["tip_material_status_key"] = table_1["tip_material_status_key"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_STATUS", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return s2 if s2 != "" and s2.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s2 = str(s).strip()
        return s2 if s2 != "" and s2.lower() != "nan" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_STATUS"] = table_1["TIP_MATERIAL_STATUS"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['tip_material_status_key'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['tip_material_status_key'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['tip_material_status_key', 'TIP_MATERIAL_STATUS'])
    # SelectCol
    _cols = [c for c in ['tip_material_status_key', 'TIP_MATERIAL_STATUS'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SUBJECT_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SUBJECT_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['DEPARTMENT_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['DEPARTMENT_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_ID', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_ID', 'DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SUBJECT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SUBJECT_ID'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_material_usage = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_material_status_lu = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_subjects = prepared_table_3

# Assume prepared dataframes: prepared_material_usage, prepared_material_status_lu, prepared_subjects

# Normalize join keys/cases
mu = prepared_material_usage.copy()
sl = prepared_material_status_lu.copy()
subj = prepared_subjects.copy()

# Join to status lookup
mu_sl = mu.merge(sl, left_on='TIP_MATERIAL_STATUS_KEY', right_on='tip_material_status_key', how='left')

# Join to subjects to get school/department
mu_full = mu_sl.merge(subj, left_on='subject_id', right_on='SUBJECT_ID', how='left')

# Derive publication year from TERM_CODE when possible (e.g., '2016FA' -> 2016)
def extract_year(term):
    if pd.isna(term):
        return pd.NA
    s = str(term)
    # take leading 4 digits if present
    return int(s[:4]) if len(s) >= 4 and s[:4].isdigit() else pd.NA

mu_full['PUB_YEAR'] = mu_full['TERM_CODE'].apply(extract_year)

# Group by material status (use description when available, else fall back to key)
status_name = mu_full['TIP_MATERIAL_STATUS'].fillna('')
status_fallback = mu_full['TIP_MATERIAL_STATUS_KEY'].fillna('')
mu_full['MATERIAL_STATUS'] = status_name.where(status_name.str.len() > 0, status_fallback)

# Compute aggregations per material status
agg = mu_full.groupby('MATERIAL_STATUS').agg(
    total_materials=('TIP_MATERIAL_KEY', lambda s: s.dropna().nunique()),
    total_subjects=('subject_id', lambda s: s.dropna().nunique()),
    total_schools=('DEPARTMENT_NAME', lambda s: s.dropna().nunique()),
    most_recent_publication_year=('PUB_YEAR', lambda s: s.dropna().max() if len(s.dropna())>0 else pd.NA)
).reset_index()

# Final result per material status
target = agg.sort_values('MATERIAL_STATUS')

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
