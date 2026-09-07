import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
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
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_CATEGORY_KEY', 'TERM_CODE', 'FEE', 'MAX_ENROLLMENT'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_CATEGORY_KEY', 'TERM_CODE', 'FEE', 'MAX_ENROLLMENT'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="MAX_ENROLLMENT", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MAX_ENROLLMENT'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MAX_ENROLLMENT']
    if _dtype == "datetime64":
        table_1['MAX_ENROLLMENT'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MAX_ENROLLMENT'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MAX_ENROLLMENT'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MAX_ENROLLMENT'] = _series.astype(str)

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
    # MissingValueImputation(table_name="table_1", column_name="IAP_CATEGORY_NAME", mode="mode")
    # MissingValueImputation
    table_1["IAP_CATEGORY_NAME"] = table_1["IAP_CATEGORY_NAME"].fillna(table_1["IAP_CATEGORY_NAME"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IAP_SUBJECT_CATEGORY_KEY", func="""
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
    table_1["IAP_SUBJECT_CATEGORY_KEY"] = table_1["IAP_SUBJECT_CATEGORY_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_CATEGORY_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_CATEGORY_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['TERM_CODE', 'ACADEMIC_YEAR'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['TERM_CODE', 'ACADEMIC_YEAR'], ascending=[True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row.get('IS_OFFERED_IAP', '')).strip().upper() == 'Y'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row.get('IS_OFFERED_IAP', '')).strip().upper() == 'Y'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'ACADEMIC_YEAR'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'ACADEMIC_YEAR'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TERM_CODE', 'ACADEMIC_YEAR'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TERM_CODE', 'ACADEMIC_YEAR'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'ACADEMIC_YEAR'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'ACADEMIC_YEAR'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['TERM_CODE', 'ACADEMIC_YEAR'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['TERM_CODE', 'ACADEMIC_YEAR'], ascending=[True, True])

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
iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
iap_categories = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
term_years = prepared_table_3

# Start from prepared tables
s = iap_subjects.copy()
# Normalize keys and numeric fields
s['IAP_SUBJECT_CATEGORY_KEY'] = s['IAP_SUBJECT_CATEGORY_KEY'].astype(str).str.strip()
# Coerce fee and max enrollment to numeric, treating non-numeric as NaN
s['FEE'] = pd.to_numeric(s['FEE'], errors='coerce')
s['MAX_ENROLLMENT'] = pd.to_numeric(s['MAX_ENROLLMENT'], errors='coerce')

cats = iap_categories.copy()
cats['IAP_SUBJECT_CATEGORY_KEY'] = cats['IAP_SUBJECT_CATEGORY_KEY'].astype(str).strip()

terms = term_years.copy()

# Join to get academic year
sj = s.merge(terms[['TERM_CODE','ACADEMIC_YEAR']].drop_duplicates(), on='TERM_CODE', how='left')
# Join to get category name
sj = sj.merge(cats[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']].drop_duplicates(), on='IAP_SUBJECT_CATEGORY_KEY', how='left')

# Aggregate by category and academic year
result = (
    sj.groupby(['IAP_CATEGORY_NAME','ACADEMIC_YEAR'], dropna=False)
      .agg(
          total_fee_collected = ('FEE', lambda x: pd.Series(x).dropna().sum()),
          total_iap_subjects = ('TERM_CODE', 'count'),
          min_enrollment = ('MAX_ENROLLMENT', 'min'),
          max_enrollment = ('MAX_ENROLLMENT', 'max')
      )
      .reset_index()
      .rename(columns={'IAP_CATEGORY_NAME':'category_name','ACADEMIC_YEAR':'academic_year'})
)

# Optional sorting for readability
result = result.sort_values(['category_name','academic_year'])

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
