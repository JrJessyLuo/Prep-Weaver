import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['ACADEMIC_YEAR', 'SUBJECT_CODE', 'SUBJECT_NUMBER'], ascending=[True, True, True])
    # Sort
    table_1 = table_1.sort_values(by=['ACADEMIC_YEAR', 'SUBJECT_CODE', 'SUBJECT_NUMBER'], ascending=[True, True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="subject_id", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["subject_id"] = table_1["subject_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_CODE"] = table_1["SUBJECT_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_NUMBER", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_NUMBER"] = table_1["SUBJECT_NUMBER"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="GRADE_TYPE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["GRADE_TYPE"] = table_1["GRADE_TYPE"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="HGN_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["HGN_CODE"] = table_1["HGN_CODE"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACADEMIC_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACADEMIC_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACADEMIC_YEAR']
    if _dtype == "datetime64":
        table_1['ACADEMIC_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACADEMIC_YEAR'] = _series.astype(str)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ACADEMIC_YEAR', 'SUBJECT_CODE', 'SUBJECT_NUMBER', 'subject_id', 'SUBJECT_TITLE', 'GRADE_TYPE', 'HGN_CODE'])
    # SelectCol
    _cols = [c for c in ['ACADEMIC_YEAR', 'SUBJECT_CODE', 'SUBJECT_NUMBER', 'subject_id', 'SUBJECT_TITLE', 'GRADE_TYPE', 'HGN_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ACADEMIC_YEAR', 'subject_id', 'SUBJECT_CODE', 'SUBJECT_NUMBER'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ACADEMIC_YEAR', 'subject_id', 'SUBJECT_CODE', 'SUBJECT_NUMBER'], how='any').reset_index(drop=True)

    # ---------------- Step 11 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ACADEMIC_YEAR', 'subject_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ACADEMIC_YEAR', 'subject_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 12 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['ACADEMIC_YEAR', 'SUBJECT_CODE', 'SUBJECT_NUMBER'], ascending=[True, True, True])
    # Sort
    table_1 = table_1.sort_values(by=['ACADEMIC_YEAR', 'SUBJECT_CODE', 'SUBJECT_NUMBER'], ascending=[True, True, True])

    # ---------------- Step 13 ----------------
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
    # MissingValueImputation(table_name="table_1", column_name="FORM_TYPE", mode="mode")
    # MissingValueImputation
    table_1["FORM_TYPE"] = table_1["FORM_TYPE"].fillna(table_1["FORM_TYPE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="RESPONSIBLE_FACULTY_NAME", mode="mode")
    # MissingValueImputation
    table_1["RESPONSIBLE_FACULTY_NAME"] = table_1["RESPONSIBLE_FACULTY_NAME"].fillna(table_1["RESPONSIBLE_FACULTY_NAME"].mode().iloc[0])

    # ---------------- Step 3 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="FORM_TYPE_DESC", mode="mode")
    # MissingValueImputation
    table_1["FORM_TYPE_DESC"] = table_1["FORM_TYPE_DESC"].fillna(table_1["FORM_TYPE_DESC"].mode().iloc[0])

    # ---------------- Step 4 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="OFFER_DEPT_CODE", mode="mode")
    # MissingValueImputation
    table_1["OFFER_DEPT_CODE"] = table_1["OFFER_DEPT_CODE"].fillna(table_1["OFFER_DEPT_CODE"].mode().iloc[0])

    # ---------------- Step 5 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="OFFER_DEPT_NAME", mode="mode")
    # MissingValueImputation
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].fillna(table_1["OFFER_DEPT_NAME"].mode().iloc[0])

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_ID', 'SUBJECT_TITLE', 'TERM_CODE', 'RESPONSIBLE_FACULTY_NAME', 'FORM_TYPE', 'FORM_TYPE_DESC', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_ID', 'SUBJECT_TITLE', 'TERM_CODE', 'RESPONSIBLE_FACULTY_NAME', 'FORM_TYPE', 'FORM_TYPE_DESC', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subject_catalog = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_subject_offerings = prepared_table_2

# Assume prepared_subject_catalog and prepared_subject_offerings are dataframes synthesized per target schemas.

# 1) Integrate catalog with offerings on subject_id keys
integrated = prepared_subject_catalog.merge(
    prepared_subject_offerings,
    left_on="subject_id",
    right_on="SUBJECT_ID",
    how="inner"
)

# 2) Filter for academic year 2022 and valid instructor names
filtered = integrated[(integrated["ACADEMIC_YEAR"] == 2022) & (~integrated["RESPONSIBLE_FACULTY_NAME"].isna()) & (integrated["RESPONSIBLE_FACULTY_NAME"].astype(str).str.strip() != "")]

# 3) Derive course type. Prefer FORM_TYPE_DESC when available, else FORM_TYPE, else fallback to non-null SUBJECT_TITLE grouping if needed
course_type = (
    filtered["FORM_TYPE_DESC"].where(filtered["FORM_TYPE_DESC"].notna(), filtered["FORM_TYPE"])
)
filtered = filtered.assign(COURSE_TYPE=course_type)

# 4) Aggregate: total number of distinct types of courses per instructor in AY 2022
agg = (
    filtered.groupby(["ACADEMIC_YEAR", "RESPONSIBLE_FACULTY_NAME"])\
        ["COURSE_TYPE"].nunique(dropna=True)\
        .reset_index(name="total_course_types")
)

# 5) Select output columns
target = agg[["ACADEMIC_YEAR", "RESPONSIBLE_FACULTY_NAME", "total_course_types"]]

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
