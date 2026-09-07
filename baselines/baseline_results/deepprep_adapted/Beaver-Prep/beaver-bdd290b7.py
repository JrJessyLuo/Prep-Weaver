import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_PERSON_KEY', 'TERM_CODE', 'FEE', 'MAX_ENROLLMENT'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_PERSON_KEY', 'TERM_CODE', 'FEE', 'MAX_ENROLLMENT'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

    # ---------------- Step 4 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="FEE", mode="median")
    # MissingValueImputation
    table_1["FEE"] = table_1["FEE"].fillna(table_1["FEE"].median())

    # ---------------- Step 5 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="MAX_ENROLLMENT", mode="median")
    # MissingValueImputation
    table_1["MAX_ENROLLMENT"] = table_1["MAX_ENROLLMENT"].fillna(table_1["MAX_ENROLLMENT"].median())

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_PERSON_KEY', 'TERM_CODE', 'FEE', 'MAX_ENROLLMENT'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_PERSON_KEY', 'TERM_CODE', 'FEE', 'MAX_ENROLLMENT'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['iap_subject_person_key'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['iap_subject_person_key'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="PERSON_EMAIL", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
    #         return None
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
            return None
        return str(s).strip().lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["PERSON_EMAIL"] = table_1["PERSON_EMAIL"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="iap_person_dim", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1[['iap_subject_person_key','PERSON_NAME','PERSON_EMAIL']].copy()
    # 
    #     # Normalize null-like values
    #     for c in ['PERSON_NAME','PERSON_EMAIL']:
    #         df[c] = df[c].apply(lambda x: None if pd.isna(x) else x)
    # 
    #     # One row per person key; pick first non-null email/name if duplicates exist
    #     def first_non_null(s):
    #         s2 = s.dropna()
    #         return s2.iloc[0] if len(s2) else None
    # 
    #     out = (
    #         df.groupby('iap_subject_person_key', as_index=False)
    #           .agg({
    #               'PERSON_NAME': first_non_null,
    #               'PERSON_EMAIL': first_non_null
    #           })
    #     )
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1[['iap_subject_person_key','PERSON_NAME','PERSON_EMAIL']].copy()

        # Normalize null-like values
        for c in ['PERSON_NAME','PERSON_EMAIL']:
            df[c] = df[c].apply(lambda x: None if pd.isna(x) else x)

        # One row per person key; pick first non-null email/name if duplicates exist
        def first_non_null(s):
            s2 = s.dropna()
            return s2.iloc[0] if len(s2) else None

        out = (
            df.groupby('iap_subject_person_key', as_index=False)
              .agg({
                  'PERSON_NAME': first_non_null,
                  'PERSON_EMAIL': first_non_null
              })
        )
        return out
    iap_person_dim = process_tables(table_1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="iap_person_dim", columns=['iap_subject_person_key', 'PERSON_NAME', 'PERSON_EMAIL'])
    # SelectCol
    _cols = [c for c in ['iap_subject_person_key', 'PERSON_NAME', 'PERSON_EMAIL'] if c in iap_person_dim.columns]
    iap_person_dim = iap_person_dim[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['iap_person_dim'])
    # Terminate
    result = {'iap_person_dim': iap_person_dim}
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
iap_persons = prepared_table_2

# Assume prepared tables are provided as dataframes: iap_subjects, iap_persons
# 1) Integrate on person key
merged = iap_subjects.merge(iap_persons, left_on='IAP_SUBJECT_PERSON_KEY', right_on='iap_subject_person_key', how='left')

# 2) Derive academic year from TERM_CODE (e.g., '2021JA' -> '2021')
merged['ACADEMIC_YEAR'] = merged['TERM_CODE'].astype(str).str[:4]

# 3) Ensure numeric types for aggregations
merged['FEE_num'] = pd.to_numeric(merged['FEE'], errors='coerce')
merged['MAX_ENROLLMENT_num'] = pd.to_numeric(merged['MAX_ENROLLMENT'], errors='coerce')

# 4) Aggregate per individual and academic year
agg = (
    merged.groupby(['iap_subject_person_key','PERSON_EMAIL','PERSON_NAME','ACADEMIC_YEAR'], dropna=False)
          .agg(
              total_iap_subjects=('IAP_SUBJECT_PERSON_KEY','size'),
              min_fee=('FEE_num','min'),
              max_fee=('FEE_num','max'),
              total_course_enrollment=('MAX_ENROLLMENT_num','sum')
          )
          .reset_index()
)

# 5) Select and rename columns for the final answer
answer = agg.rename(columns={
    'PERSON_EMAIL': 'email',
    'PERSON_NAME': 'name',
    'ACADEMIC_YEAR': 'academic_year',
    'total_iap_subjects': 'total_number_of_IAP_subjects',
    'min_fee': 'minimum_fee',
    'max_fee': 'maximum_fee',
    'total_course_enrollment': 'total_course_enrollment'
})

target = answer[['email','name','academic_year','total_number_of_IAP_subjects','minimum_fee','maximum_fee','total_course_enrollment']]

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
