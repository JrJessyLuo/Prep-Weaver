import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['iap_subject_person_key', 'PERSON_ROLE', 'PERSON_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['iap_subject_person_key', 'PERSON_ROLE', 'PERSON_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['iap_subject_person_key', 'PERSON_ROLE', 'PERSON_NAME'])
    # SelectCol
    _cols = [c for c in ['iap_subject_person_key', 'PERSON_ROLE', 'PERSON_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="PERSON_ROLE", func="""
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
    table_1["PERSON_ROLE"] = table_1["PERSON_ROLE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="PERSON_NAME", func="""
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
    table_1["PERSON_NAME"] = table_1["PERSON_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['iap_subject_person_key', 'PERSON_ROLE', 'PERSON_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['iap_subject_person_key', 'PERSON_ROLE', 'PERSON_NAME'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'ACTIVITY_DESCRIPTION', 'TERM_CODE', 'ENROLLMENT_TYPE', 'MAX_ENROLLMENT', 'ATTENDANCE', 'PREREQUISITES', 'FEE_REASON', 'PREREG_DEADLINE', 'CREATE_DATE', 'LAST_ACTIVITY_DATE', 'IS_MULTIPLE_SESSION', 'IS_CANCELLED', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'ACTIVITY_DESCRIPTION', 'TERM_CODE', 'ENROLLMENT_TYPE', 'MAX_ENROLLMENT', 'ATTENDANCE', 'PREREQUISITES', 'FEE_REASON', 'PREREG_DEADLINE', 'CREATE_DATE', 'LAST_ACTIVITY_DATE', 'IS_MULTIPLE_SESSION', 'IS_CANCELLED', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FEE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FEE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FEE']
    if _dtype == "datetime64":
        table_1['FEE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FEE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FEE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FEE'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="FEE", mode="median")
    # MissingValueImputation
    table_1["FEE"] = table_1["FEE"].fillna(table_1["FEE"].median())

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_PERSON_KEY', 'IAP_SUBJECT_CATEGORY_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_PERSON_KEY', 'IAP_SUBJECT_CATEGORY_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_PERSON_KEY', 'IAP_SUBJECT_CATEGORY_KEY', 'FEE'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_PERSON_KEY', 'IAP_SUBJECT_CATEGORY_KEY', 'FEE'] if c in table_1.columns]
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
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IAP_SUBJECT_CATEGORY_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IAP_SUBJECT_CATEGORY_KEY"] = table_1["IAP_SUBJECT_CATEGORY_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IAP_CATEGORY_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IAP_CATEGORY_NAME"] = table_1["IAP_CATEGORY_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_CATEGORY_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_CATEGORY_KEY'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_subjects = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_categories = prepared_table_3

# Assume prepared_people, prepared_subjects, prepared_categories are available DataFrames
# Clean potential whitespace in category keys to ensure joins
prepared_categories = prepared_categories.assign(IAP_SUBJECT_CATEGORY_KEY=prepared_categories['IAP_SUBJECT_CATEGORY_KEY'].astype(str).str.strip())
prepared_subjects = prepared_subjects.assign(IAP_SUBJECT_CATEGORY_KEY=prepared_subjects['IAP_SUBJECT_CATEGORY_KEY'].astype(str).str.strip())

# Join subjects to people by person key
sp = prepared_subjects.merge(
    prepared_people,
    left_on='IAP_SUBJECT_PERSON_KEY',
    right_on='iap_subject_person_key',
    how='inner'
)

# Join categories to get category name
spc = sp.merge(
    prepared_categories,
    on='IAP_SUBJECT_CATEGORY_KEY',
    how='left'
)

# Convert fee to numeric for averaging
spc['FEE'] = pd.to_numeric(spc['FEE'], errors='coerce')

# Group by role and category name: count distinct people in this role and compute average fee
result = (
    spc.groupby(['PERSON_ROLE', 'IAP_CATEGORY_NAME'])
       .agg(role_count=('PERSON_NAME', lambda s: s.nunique()),
            average_fee=('FEE', 'mean'))
       .reset_index()
)

# Sort by role_count descending
result = result.sort_values(['role_count', 'PERSON_ROLE', 'IAP_CATEGORY_NAME'], ascending=[False, True, True])

# Final columns
result = result[['PERSON_ROLE', 'IAP_CATEGORY_NAME', 'role_count', 'average_fee']]

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
