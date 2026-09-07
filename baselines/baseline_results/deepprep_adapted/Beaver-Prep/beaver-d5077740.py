import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_CODE", func="""
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
    table_1["OFFER_DEPT_CODE"] = table_1["OFFER_DEPT_CODE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="CLUSTER_TYPE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper() if s else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper() if s else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["CLUSTER_TYPE"] = table_1["CLUSTER_TYPE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
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
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_subject_offering_facts", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Coerce numeric fields (robust to strings like '0', blanks, etc.)
    #     for col in ["SUBJECT_ENROLLMENT_NUMBER", "NUM_ENROLLED_STUDENTS"]:
    #         if col in df.columns:
    #             df[col] = pd.to_numeric(df[col], errors="coerce")
    # 
    #     # Select and order exactly the required columns
    #     out = df[[
    #         "CLUSTER_TYPE",
    #         "CLUSTER_TYPE_DESC",
    #         "OFFER_DEPT_CODE",
    #         "OFFER_DEPT_NAME",
    #         "OFFER_SCHOOL_NAME",
    #         "SUBJECT_ID",
    #         "TERM_CODE",
    #         "SUBJECT_ENROLLMENT_NUMBER",
    #         "NUM_ENROLLED_STUDENTS"
    #     ]].copy()
    # 
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Coerce numeric fields (robust to strings like '0', blanks, etc.)
        for col in ["SUBJECT_ENROLLMENT_NUMBER", "NUM_ENROLLED_STUDENTS"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Select and order exactly the required columns
        out = df[[
            "CLUSTER_TYPE",
            "CLUSTER_TYPE_DESC",
            "OFFER_DEPT_CODE",
            "OFFER_DEPT_NAME",
            "OFFER_SCHOOL_NAME",
            "SUBJECT_ID",
            "TERM_CODE",
            "SUBJECT_ENROLLMENT_NUMBER",
            "NUM_ENROLLED_STUDENTS"
        ]].copy()

        return out
    prepared_subject_offering_facts = process_tables(table_1)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['prepared_subject_offering_facts'])
    # Terminate
    result = {'prepared_subject_offering_facts': prepared_subject_offering_facts}
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
    # MissingValueImputation(table_name="table_1", column_name="DEPARTMENT_NAME", mode="mode")
    # MissingValueImputation
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].fillna(table_1["DEPARTMENT_NAME"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="dept_reference_prepared", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # Canonicalize names: prefer commencement book versions when available, else fallback
    #     def pick(preferred, fallback):
    #         # treat NaN / None / empty string as missing
    #         if pd.isna(preferred) or str(preferred).strip().lower() in ["", "nan", "none"]:
    #             return fallback
    #         return preferred
    # 
    #     df["DEPARTMENT_NAME_CANON"] = df.apply(
    #         lambda r: pick(r.get("DEPT_NAME_IN_COMMENCEMENT_BK"), r.get("DEPARTMENT_NAME")),
    #         axis=1
    #     )
    #     df["SCHOOL_NAME_CANON"] = df.apply(
    #         lambda r: pick(r.get("SCHOOL_NAME_IN_COMMENCEMENT_BK"), r.get("SCHOOL_NAME")),
    #         axis=1
    #     )
    # 
    #     out = df[["DEPARTMENT_CODE", "DEPARTMENT_NAME_CANON", "SCHOOL_NAME_CANON", "IS_DEGREE_GRANTING"]].copy()
    #     out = out.rename(columns={
    #         "DEPARTMENT_NAME_CANON": "DEPARTMENT_NAME",
    #         "SCHOOL_NAME_CANON": "SCHOOL_NAME"
    #     })
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # Canonicalize names: prefer commencement book versions when available, else fallback
        def pick(preferred, fallback):
            # treat NaN / None / empty string as missing
            if pd.isna(preferred) or str(preferred).strip().lower() in ["", "nan", "none"]:
                return fallback
            return preferred

        df["DEPARTMENT_NAME_CANON"] = df.apply(
            lambda r: pick(r.get("DEPT_NAME_IN_COMMENCEMENT_BK"), r.get("DEPARTMENT_NAME")),
            axis=1
        )
        df["SCHOOL_NAME_CANON"] = df.apply(
            lambda r: pick(r.get("SCHOOL_NAME_IN_COMMENCEMENT_BK"), r.get("SCHOOL_NAME")),
            axis=1
        )

        out = df[["DEPARTMENT_CODE", "DEPARTMENT_NAME_CANON", "SCHOOL_NAME_CANON", "IS_DEGREE_GRANTING"]].copy()
        out = out.rename(columns={
            "DEPARTMENT_NAME_CANON": "DEPARTMENT_NAME",
            "SCHOOL_NAME_CANON": "SCHOOL_NAME"
        })
        return out
    dept_reference_prepared = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="dept_reference_prepared", subset=['DEPARTMENT_CODE'], keep="last")
    # Deduplicate
    dept_reference_prepared = dept_reference_prepared.drop_duplicates(subset=['DEPARTMENT_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="dept_reference_prepared", columns=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'IS_DEGREE_GRANTING'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'IS_DEGREE_GRANTING'] if c in dept_reference_prepared.columns]
    dept_reference_prepared = dept_reference_prepared[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['dept_reference_prepared'])
    # Terminate
    result = {'dept_reference_prepared': dept_reference_prepared}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_subject_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_7'])
prepared_departments = prepared_table_2

# Assume prepared_subject_offerings (s1) and prepared_departments (d1) are provided per the targets above
s1 = prepared_subject_offerings.copy()
d1 = prepared_departments.copy()

# Integrate on department code
merged = s1.merge(d1, left_on='OFFER_DEPT_CODE', right_on='DEPARTMENT_CODE', how='left')

# Compute enrollment per row; prefer NUM_ENROLLED_STUDENTS if present, else SUBJECT_ENROLLMENT_NUMBER
enroll = merged['NUM_ENROLLED_STUDENTS']
if 'NUM_ENROLLED_STUDENTS' in merged and merged['NUM_ENROLLED_STUDENTS'].notna().any():
    enroll = merged['NUM_ENROLLED_STUDENTS']
else:
    enroll = merged['SUBJECT_ENROLLMENT_NUMBER']
merged['enrollment_val'] = pd.to_numeric(enroll, errors='coerce')

# Exclude groups with no student data: drop rows where enrollment is NaN or 0
merged_nonzero = merged[merged['enrollment_val'] > 0]

# Group and aggregate
grp_cols = [
    'CLUSTER_TYPE',
    'OFFER_DEPT_NAME',
    'SCHOOL_NAME'
]
agg_df = (
    merged_nonzero
    .groupby(grp_cols, dropna=False)
    .agg(
        IS_DEGREE_GRANTING=('IS_DEGREE_GRANTING', 'first'),
        total_subjects=('SUBJECT_ID', 'nunique'),
        total_enrollment=('enrollment_val', 'sum'),
        average_enrollment=('enrollment_val', 'mean')
    )
    .reset_index()
)

# Rename for final output clarity
agg_df = agg_df.rename(columns={
    'CLUSTER_TYPE': 'cluster_type',
    'OFFER_DEPT_NAME': 'department_name',
    'SCHOOL_NAME': 'school_name',
    'IS_DEGREE_GRANTING': 'department_grants_degrees',
    'total_subjects': 'total_number_of_subjects',
    'total_enrollment': 'total_enrollment',
    'average_enrollment': 'average_enrollment'
})

# Result in agg_df with required columns
result = agg_df[['cluster_type', 'department_name', 'school_name', 'department_grants_degrees', 'total_number_of_subjects', 'total_enrollment', 'average_enrollment']]

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
