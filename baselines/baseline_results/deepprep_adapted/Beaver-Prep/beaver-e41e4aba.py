import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
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
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_CODE"] = table_1["SCHOOL_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DLC_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DLC_KEY"] = table_1["DLC_KEY"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DLC_KEY'])
    # SelectCol
    _cols = [c for c in ['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DLC_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DLC_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DLC_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SCHOOL_CODE', 'DEPARTMENT_CODE', 'DLC_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SCHOOL_CODE', 'DEPARTMENT_CODE', 'DLC_KEY'], keep='first').reset_index(drop=True)

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
    # DropNulls(table_name="table_1", subset=['SCHOOL_CODE', 'DEPARTMENT_CODE', 'SUBJECT_CODE', 'COURSE_NUMBER'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SCHOOL_CODE', 'DEPARTMENT_CODE', 'SUBJECT_CODE', 'COURSE_NUMBER'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["SCHOOL_CODE"] = table_1["SCHOOL_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["SUBJECT_CODE"] = table_1["SUBJECT_CODE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COURSE_NUMBER", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # COURSE_NUMBER values appear to be codes; normalize for consistent min/max and joins.
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # COURSE_NUMBER values appear to be codes; normalize for consistent min/max and joins.
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["COURSE_NUMBER"] = table_1["COURSE_NUMBER"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'SUBJECT_CODE', 'COURSE_NUMBER'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'SUBJECT_CODE', 'COURSE_NUMBER'], keep='first').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'SUBJECT_CODE', 'COURSE_NUMBER'])
    # SelectCol
    _cols = [c for c in ['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'SUBJECT_CODE', 'COURSE_NUMBER'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row.get('COURSE_NUMBER') is not None and str(row.get('COURSE_NUMBER')).strip() != ''
    # """)
    # Filter
    def filter_func(row):
        return row.get('COURSE_NUMBER') is not None and str(row.get('COURSE_NUMBER')).strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['COURSE_NUMBER', 'HGN_CODE'])
    # SelectCol
    _cols = [c for c in ['COURSE_NUMBER', 'HGN_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COURSE_NUMBER", func="""
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
    table_1["COURSE_NUMBER"] = table_1["COURSE_NUMBER"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="HGN_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return s if s != "" and s.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        return s if s != "" and s.lower() != "nan" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["HGN_CODE"] = table_1["HGN_CODE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['COURSE_NUMBER'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['COURSE_NUMBER'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="answer_code", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Keep minimal slice
    #     df = df[['COURSE_NUMBER', 'HGN_CODE']]
    # 
    #     # If multiple HGN_CODE values exist for a COURSE_NUMBER, prefer grad-like codes.
    #     # (Heuristic: prioritize codes containing 'G' or 'GRAD' or 'H'/'N' if those are used in your system.)
    #     priority = {
    #         # common patterns
    #         'G': 1, 'GRAD': 1,
    #         # fallback buckets
    #         'H': 2, 'N': 3, 'U': 4
    #     }
    # 
    #     def score(code):
    #         if code is None or (isinstance(code, float) and pd.isna(code)):
    #             return 999
    #         c = str(code).strip().upper()
    #         if c in priority:
    #             return priority[c]
    #         # contains-based preference
    #         if 'GRAD' in c or c.startswith('G'):
    #             return 1
    #         return 50  # unknown but non-null
    # 
    #     df['__score'] = df['HGN_CODE'].apply(score)
    # 
    #     # Sort so the best code per course is first, then dedupe
    #     df = df.sort_values(by=['COURSE_NUMBER', '__score', 'HGN_CODE'], ascending=[True, True, True])
    # 
    #     out = df.drop_duplicates(subset=['COURSE_NUMBER'], keep='first').drop(columns=['__score'])
    # 
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Keep minimal slice
        df = df[['COURSE_NUMBER', 'HGN_CODE']]

        # If multiple HGN_CODE values exist for a COURSE_NUMBER, prefer grad-like codes.
        # (Heuristic: prioritize codes containing 'G' or 'GRAD' or 'H'/'N' if those are used in your system.)
        priority = {
            # common patterns
            'G': 1, 'GRAD': 1,
            # fallback buckets
            'H': 2, 'N': 3, 'U': 4
        }

        def score(code):
            if code is None or (isinstance(code, float) and pd.isna(code)):
                return 999
            c = str(code).strip().upper()
            if c in priority:
                return priority[c]
            # contains-based preference
            if 'GRAD' in c or c.startswith('G'):
                return 1
            return 50  # unknown but non-null

        df['__score'] = df['HGN_CODE'].apply(score)

        # Sort so the best code per course is first, then dedupe
        df = df.sort_values(by=['COURSE_NUMBER', '__score', 'HGN_CODE'], ascending=[True, True, True])

        out = df.drop_duplicates(subset=['COURSE_NUMBER'], keep='first').drop(columns=['__score'])

        return out
    answer_code = process_tables(table_1)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Terminate(result=['answer_code'])
    # Terminate
    result = {'answer_code': answer_code}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_departments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_subject_codes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_subject_offerings = prepared_table_3

# Assume prepared tables are provided as dataframes: prepared_departments, prepared_subject_codes, prepared_subject_offerings

# 1) Derive graduate level per course number using offerings (G present => Graduate, else if N only => Not for grad credit, else other codes retained). 
# Normalize COURSE_NUMBER whitespace/case across tables
psc = prepared_subject_codes.copy()
pso = prepared_subject_offerings.copy()
pdpt = prepared_departments.copy()

for df in (psc, pso):
    if 'COURSE_NUMBER' in df.columns:
        df['COURSE_NUMBER'] = df['COURSE_NUMBER'].astype(str).str.strip().str.upper()

# Deduplicate offerings by COURSE_NUMBER and compute graduate flag
pso_g = (
    pso.assign(
        COURSE_NUMBER=lambda d: d['COURSE_NUMBER'].astype(str).str.strip().str.upper(),
        HGN_CODE=lambda d: d['HGN_CODE'].astype(str).str.upper()
    )
)
# For each COURSE_NUMBER, determine grad_level: 'Graduate' if any HGN_CODE == 'G', else 'Not for graduate credit' if all 'N', else 'Mixed/Other'
agg = (
    pso_g.groupby('COURSE_NUMBER')['HGN_CODE']
         .agg(lambda s: ('Graduate' if (s == 'G').any() else ('Not for graduate credit' if (s.replace({'N': 'N'}).isin(['N'])).all() else 'Mixed/Other')))
         .reset_index()
         .rename(columns={'HGN_CODE': 'GRADUATE_LEVEL'})
)

# 2) Attach graduate level to subject codes via COURSE_NUMBER (left join, some course numbers may lack offerings)
psc_gl = psc.merge(agg, on='COURSE_NUMBER', how='left')

# 3) Compute school-level aggregates from subject codes
# Total number of SIS subjects per school: count distinct SUBJECT_CODE per SCHOOL_CODE
subjects_per_school = (
    psc[['SCHOOL_CODE','SUBJECT_CODE']]
      .dropna()
      .drop_duplicates()
      .groupby('SCHOOL_CODE')
      .size()
      .rename('TOTAL_SIS_SUBJECTS')
      .reset_index()
)

# 4) Min/Max course numbers per school (based on normalized COURSE_NUMBER strings)
course_minmax = (
    psc[['SCHOOL_CODE','COURSE_NUMBER']]
      .dropna()
      .assign(COURSE_NUMBER=lambda d: d['COURSE_NUMBER'].astype(str).str.strip().str.upper())
      .drop_duplicates()
      .groupby('SCHOOL_CODE')
      .agg(MIN_COURSE_NUMBER=('COURSE_NUMBER','min'), MAX_COURSE_NUMBER=('COURSE_NUMBER','max'))
      .reset_index()
)

# 5) Total number of departments offering subjects per school
depts_per_school = (
    pdpt[['SCHOOL_CODE','DEPARTMENT_CODE']]
        .dropna()
        .drop_duplicates()
        .merge(psc[['DEPARTMENT_CODE']].drop_duplicates(), on='DEPARTMENT_CODE', how='inner')
        .groupby('SCHOOL_CODE')
        .size()
        .rename('TOTAL_DEPARTMENTS_OFFERING_SUBJECTS')
        .reset_index()
)

# 6) Determine school-level graduate level from course numbers present in that school (priority: Graduate if any Graduate; else Not for graduate credit if all are that; else Mixed/Other)
school_grad = (
    psc_gl[['SCHOOL_CODE','GRADUATE_LEVEL']]
      .dropna(subset=['SCHOOL_CODE'])
)
# If a school has no GRADUATE_LEVEL values (no offerings matched), treat as Mixed/Other
logic = (
    school_grad.groupby('SCHOOL_CODE')['GRADUATE_LEVEL']
      .agg(lambda s: ('Graduate' if (s == 'Graduate').any() else ('Not for graduate credit' if len(s)>0 and (s.replace({'Not for graduate credit':'NFG'}).isin(['Not for graduate credit'])).all() else 'Mixed/Other')))
      .reset_index()
      .rename(columns={'GRADUATE_LEVEL':'SCHOOL_GRADUATE_LEVEL'})
)

# 7) One row per school with school name and DLC key: DLC_KEY is department-level; preserve but cannot aggregate meaningfully across multiple depts.
# We will present DLC_KEY as null at school level unless there is a unique DLC per school (rare); collect none/ambiguous as null.
# Build school dimension from departments, choosing a canonical SCHOOL_NAME per SCHOOL_CODE.
school_dim = (
    pdpt[['SCHOOL_CODE','SCHOOL_NAME']]
        .dropna(subset=['SCHOOL_CODE'])
        .drop_duplicates()
)

# 8) Combine all school-level pieces
result = (
    school_dim
      .merge(subjects_per_school, on='SCHOOL_CODE', how='left')
      .merge(course_minmax, on='SCHOOL_CODE', how='left')
      .merge(depts_per_school, on='SCHOOL_CODE', how='left')
      .merge(logic, on='SCHOOL_CODE', how='left')
)

# 9) Add DLC_KEY: if a school has exactly one unique DLC_KEY across its departments, keep it; else set to None.
dlc_by_school = (
    pdpt[['SCHOOL_CODE','DLC_KEY']].dropna()
        .drop_duplicates()
        .groupby('SCHOOL_CODE')['DLC_KEY']
        .agg(lambda s: s.iloc[0] if s.nunique()==1 else None)
        .reset_index()
)
result = result.merge(dlc_by_school, on='SCHOOL_CODE', how='left')

# Final columns in requested order
final = result[['SCHOOL_CODE','SCHOOL_NAME','DLC_KEY','SCHOOL_GRADUATE_LEVEL','TOTAL_SIS_SUBJECTS','MIN_COURSE_NUMBER','MAX_COURSE_NUMBER','TOTAL_DEPARTMENTS_OFFERING_SUBJECTS']].sort_values('SCHOOL_CODE')

target = final

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
