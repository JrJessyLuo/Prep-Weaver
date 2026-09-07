import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TIP_MATERIAL_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TIP_MATERIAL_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TIP_MATERIAL_KEY']
    if _dtype == "datetime64":
        table_1['TIP_MATERIAL_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TIP_MATERIAL_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TIP_MATERIAL_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TIP_MATERIAL_KEY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TIP_SUBJECT_OFFERED_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TIP_SUBJECT_OFFERED_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TIP_SUBJECT_OFFERED_KEY']
    if _dtype == "datetime64":
        table_1['TIP_SUBJECT_OFFERED_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TIP_SUBJECT_OFFERED_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TIP_SUBJECT_OFFERED_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TIP_SUBJECT_OFFERED_KEY'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TIP_MATERIAL_STATUS_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TIP_MATERIAL_STATUS_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TIP_MATERIAL_STATUS_KEY']
    if _dtype == "datetime64":
        table_1['TIP_MATERIAL_STATUS_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TIP_MATERIAL_STATUS_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TIP_MATERIAL_STATUS_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TIP_MATERIAL_STATUS_KEY'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TERM_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TERM_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TERM_CODE']
    if _dtype == "datetime64":
        table_1['TERM_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TERM_CODE'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="subject_id", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['subject_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['subject_id']
    if _dtype == "datetime64":
        table_1['subject_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['subject_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['subject_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['subject_id'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ISBN", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ISBN'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ISBN']
    if _dtype == "datetime64":
        table_1['ISBN'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ISBN'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ISBN'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ISBN'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="RECORD_COUNT", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['RECORD_COUNT'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['RECORD_COUNT']
    if _dtype == "datetime64":
        table_1['RECORD_COUNT'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['RECORD_COUNT'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['RECORD_COUNT'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['RECORD_COUNT'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN', 'RECORD_COUNT'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN', 'RECORD_COUNT'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # keep only plausible ISBNs when present; allow null/empty
    #     v = row.get('ISBN', None)
    #     if v is None:
    #         return True
    #     s = str(v).strip()
    #     if s == '' or s.lower() == 'nan':
    #         return True
    #     digits = ''.join(ch for ch in s if ch.isdigit())
    #     return len(digits) in (10, 13)
    # """)
    # Filter
    def filter_func(row):
        # keep only plausible ISBNs when present; allow null/empty
        v = row.get('ISBN', None)
        if v is None:
            return True
        s = str(v).strip()
        if s == '' or s.lower() == 'nan':
            return True
        digits = ''.join(ch for ch in s if ch.isdigit())
        return len(digits) in (10, 13)
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="material_dim_prepared", func="""
    # import pandas as pd
    # import numpy as np
    # import re
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # --- Standardize ISBN: digits only, keep NaN if empty ---
    #     def norm_isbn(v):
    #         if pd.isna(v):
    #             return np.nan
    #         s = str(v).strip()
    #         if s == '' or s.lower() == 'nan':
    #             return np.nan
    #         digits = re.sub(r'\D+', '', s)
    #         return digits if digits else np.nan
    # 
    #     df['ISBN'] = df['ISBN'].apply(norm_isbn)
    # 
    #     # --- Trim and normalize text fields ---
    #     for col in ['TIP_MATERIAL_KEY', 'TITLE', 'AUTHOR', 'EDITION', 'PUBLISHER']:
    #         if col in df.columns:
    #             df[col] = df[col].astype('string')
    #             df[col] = df[col].str.replace(r'\s+', ' ', regex=True).str.strip()
    #             df.loc[df[col].str.lower().isin(['nan', 'none', 'null', '']), col] = pd.NA
    # 
    #     # --- YEAR: numeric nullable integer ---
    #     if 'YEAR' in df.columns:
    #         df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')
    #         # keep as nullable Int64 where possible
    #         df['YEAR'] = df['YEAR'].round().astype('Int64')
    # 
    #     # --- Keep only requested columns ---
    #     keep_cols = ['TIP_MATERIAL_KEY', 'ISBN', 'AUTHOR', 'TITLE', 'EDITION', 'PUBLISHER', 'YEAR']
    #     df = df[keep_cols]
    # 
    #     # --- Deduplicate for stable dimension keys ---
    #     # Prefer records with an ISBN when available; then keep the last occurrence.
    #     df['_has_isbn'] = df['ISBN'].notna().astype(int)
    #     df = df.sort_values(by=['TIP_MATERIAL_KEY', '_has_isbn'], ascending=[True, False])
    #     df = df.drop_duplicates(subset=['TIP_MATERIAL_KEY', 'ISBN'], keep='first')
    #     df = df.drop(columns=['_has_isbn'])
    # 
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # --- Standardize ISBN: digits only, keep NaN if empty ---
        def norm_isbn(v):
            if pd.isna(v):
                return np.nan
            s = str(v).strip()
            if s == '' or s.lower() == 'nan':
                return np.nan
            digits = re.sub(r'\D+', '', s)
            return digits if digits else np.nan

        df['ISBN'] = df['ISBN'].apply(norm_isbn)

        # --- Trim and normalize text fields ---
        for col in ['TIP_MATERIAL_KEY', 'TITLE', 'AUTHOR', 'EDITION', 'PUBLISHER']:
            if col in df.columns:
                df[col] = df[col].astype('string')
                df[col] = df[col].str.replace(r'\s+', ' ', regex=True).str.strip()
                df.loc[df[col].str.lower().isin(['nan', 'none', 'null', '']), col] = pd.NA

        # --- YEAR: numeric nullable integer ---
        if 'YEAR' in df.columns:
            df['YEAR'] = pd.to_numeric(df['YEAR'], errors='coerce')
            # keep as nullable Int64 where possible
            df['YEAR'] = df['YEAR'].round().astype('Int64')

        # --- Keep only requested columns ---
        keep_cols = ['TIP_MATERIAL_KEY', 'ISBN', 'AUTHOR', 'TITLE', 'EDITION', 'PUBLISHER', 'YEAR']
        df = df[keep_cols]

        # --- Deduplicate for stable dimension keys ---
        # Prefer records with an ISBN when available; then keep the last occurrence.
        df['_has_isbn'] = df['ISBN'].notna().astype(int)
        df = df.sort_values(by=['TIP_MATERIAL_KEY', '_has_isbn'], ascending=[True, False])
        df = df.drop_duplicates(subset=['TIP_MATERIAL_KEY', 'ISBN'], keep='first')
        df = df.drop(columns=['_has_isbn'])

        return df
    material_dim_prepared = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['material_dim_prepared'])
    # Terminate
    result = {'material_dim_prepared': material_dim_prepared}
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
    # CastType(table_name="table_1", column="TERM_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TERM_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TERM_CODE']
    if _dtype == "datetime64":
        table_1['TERM_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TERM_CODE'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s)
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s)
        return s.strip()
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
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s)
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s)
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_DEPT_CODE"] = table_1["OFFER_DEPT_CODE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_SCHOOL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s)
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s)
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_SCHOOL_NAME"] = table_1["OFFER_SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep='first').reset_index(drop=True)

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
prepared_material_fact = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_material_dim = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_subject_offered = prepared_table_3

# Start from prepared tables
fact = prepared_material_fact.copy()
mat = prepared_material_dim.copy()
off = prepared_subject_offered.copy()

# Join fact to material dimension to get author
fm = fact.merge(mat, how='left', on='TIP_MATERIAL_KEY')

# Join to offerings to get school
fmo = fm.merge(off[['TIP_SUBJECT_OFFERED_KEY','OFFER_SCHOOL_NAME','SUBJECT_ID']], how='left', on='TIP_SUBJECT_OFFERED_KEY')

# Normalize types and clean
fmo['RECORD_COUNT'] = pd.to_numeric(fmo['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
# Treat missing/placeholder authors consistently
fmo['AUTHOR'] = fmo['AUTHOR'].fillna('Unknown')
# Material status as-is from fact
fmo['TIP_MATERIAL_STATUS_KEY'] = fmo['TIP_MATERIAL_STATUS_KEY'].fillna('Unknown')

# Compute aggregations per author, school, material status
group_cols = ['AUTHOR','OFFER_SCHOOL_NAME','TIP_MATERIAL_STATUS_KEY']
agg = fmo.groupby(group_cols).agg(
    total_record_counts=('RECORD_COUNT','sum'),
    total_number_of_types_of_courses=('SUBJECT_ID', pd.Series.nunique)
).reset_index()

# Final output per author and school with material status, totals and distinct course types
target = agg

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
