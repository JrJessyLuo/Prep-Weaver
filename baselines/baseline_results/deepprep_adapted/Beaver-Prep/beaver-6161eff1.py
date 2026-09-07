import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="FEE", mode="mode")
    # MissingValueImputation
    table_1["FEE"] = table_1["FEE"].fillna(table_1["FEE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'ACTIVITY_TITLE', 'FEE'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'ACTIVITY_TITLE', 'FEE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'ACTIVITY_TITLE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'ACTIVITY_TITLE'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'ACTIVITY_TITLE', 'FEE'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'ACTIVITY_TITLE', 'FEE'], keep='first').reset_index(drop=True)

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
    # DropColumn(table_name="table_1", drop_columns=['IAP_CATEGORY_DESC', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['IAP_CATEGORY_DESC', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IAP_SUBJECT_CATEGORY_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ["nan", "none", "null", ""] else s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ["nan", "none", "null", ""] else s2
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
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ["nan", "none", "null", ""] else s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ["nan", "none", "null", ""] else s2
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
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'] if c in table_1.columns]
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
    # DropNulls(table_name="table_1", subset=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_SPONSOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_SPONSOR_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
iap_activities = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
iap_categories = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
iap_sponsors = prepared_table_3

# Assume prepared tables already loaded as DataFrames: iap_activities, iap_categories, iap_sponsors
# Join activities to category and sponsor dimensions
fact_dim = (
    iap_activities
    .merge(iap_categories, on='IAP_SUBJECT_CATEGORY_KEY', how='left')
    .merge(iap_sponsors, on='IAP_SUBJECT_SPONSOR_KEY', how='left')
)

# Clean fee to numeric and drop NaNs for averaging
fact_dim['FEE'] = pd.to_numeric(fact_dim['FEE'], errors='coerce')

# Group by category name and sponsor name
agg = (
    fact_dim
    .groupby(['IAP_CATEGORY_NAME', 'SPONSOR_NAME'], dropna=False)
    .agg(
        activities_offered=('ACTIVITY_TITLE', 'nunique'),
        avg_fee_per_activity=('FEE', 'mean')
    )
    .reset_index()
)

# Sort by number of activities descending
result = agg.sort_values(by='activities_offered', ascending=False)

target = result[['IAP_CATEGORY_NAME', 'SPONSOR_NAME', 'activities_offered', 'avg_fee_per_activity']]

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
