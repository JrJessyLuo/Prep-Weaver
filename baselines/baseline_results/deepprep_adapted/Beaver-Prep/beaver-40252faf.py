import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_KEY"] = table_1["TIP_MATERIAL_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_STATUS_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_STATUS_KEY"] = table_1["TIP_MATERIAL_STATUS_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="subject_id", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ISBN", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ISBN"] = table_1["ISBN"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TITLE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return " ".join(s.split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TITLE"] = table_1["TITLE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="AUTHOR", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        return " ".join(s.split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["AUTHOR"] = table_1["AUTHOR"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ISBN", func="""
    # import re
    # def transform_func(s):
    #     # Normalize to digits (and allow trailing X for ISBN-10)
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     s = s.replace('-', '').replace(' ', '')
    #     s = s.upper()
    #     # Keep only digits and X, but X only meaningful at end; easiest: remove non [0-9X]
    #     s = re.sub(r'[^0-9X]', '', s)
    #     if s == '':
    #         return None
    #     # If there are multiple X's, keep them as-is; downstream validation can handle if needed
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        # Normalize to digits (and allow trailing X for ISBN-10)
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        s = s.replace('-', '').replace(' ', '')
        s = s.upper()
        # Keep only digits and X, but X only meaningful at end; easiest: remove non [0-9X]
        s = re.sub(r'[^0-9X]', '', s)
        if s == '':
            return None
        # If there are multiple X's, keep them as-is; downstream validation can handle if needed
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ISBN"] = table_1["ISBN"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR'])
    # SelectCol
    _cols = [c for c in ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_MATERIAL_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_MATERIAL_KEY'], keep='last').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s.lower() in ["nan", "none", "null", ""] else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        return None if s.lower() in ["nan", "none", "null", ""] else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_SUBJECT_OFFERED_KEY"] = table_1["TIP_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip().upper()
    #     return None if s.lower() in ["nan", "none", "null", ""] else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip().upper()
        return None if s.lower() in ["nan", "none", "null", ""] else s
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
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s.lower() in ["nan", "none", "null", ""] else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        return None if s.lower() in ["nan", "none", "null", ""] else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s.lower() in ["nan", "none", "null", ""] else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        return None if s.lower() in ["nan", "none", "null", ""] else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_DEPT_CODE"] = table_1["OFFER_DEPT_CODE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return None if s.lower() in ["nan", "none", "null", ""] else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        return None if s.lower() in ["nan", "none", "null", ""] else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep='last').reset_index(drop=True)

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="LIBRARY_RESERVE_CATALOG_KEY", dtype="int")
    # CastType
    _dtype = 'int'
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
    # DropNulls(table_name="table_1", subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID'], keep='last').reset_index(drop=True)

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
def _prep_5(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="CATALOG_TITLE", mode="mode")
    # MissingValueImputation
    table_1["CATALOG_TITLE"] = table_1["CATALOG_TITLE"].fillna(table_1["CATALOG_TITLE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['library_reserve_catalog_key', 'CATALOG_TITLE', 'CATALOG_AUTHOR_NAME', 'CATALOG_ISBN'])
    # SelectCol
    _cols = [c for c in ['library_reserve_catalog_key', 'CATALOG_TITLE', 'CATALOG_AUTHOR_NAME', 'CATALOG_ISBN'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="library_reserve_catalog_key", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['library_reserve_catalog_key'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['library_reserve_catalog_key']
    if _dtype == "datetime64":
        table_1['library_reserve_catalog_key'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['library_reserve_catalog_key'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['library_reserve_catalog_key'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['library_reserve_catalog_key'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="CATALOG_ISBN", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     if s.lower() in {"nan", "none", ""}:
    #         return None
    #     # keep only digits and X (for ISBN-10 check digit), drop hyphens/spaces/other chars
    #     cleaned = re.sub(r"[^0-9Xx]", "", s).upper()
    #     return cleaned if cleaned else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip().strip('"').strip("'")
        if s.lower() in {"nan", "none", ""}:
            return None
        # keep only digits and X (for ISBN-10 check digit), drop hyphens/spaces/other chars
        cleaned = re.sub(r"[^0-9Xx]", "", s).upper()
        return cleaned if cleaned else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["CATALOG_ISBN"] = table_1["CATALOG_ISBN"].apply(_std_apply)

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
def _prep_6(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['COURSE_NAME', 'DATE_FROM', 'DATE_TO', 'UNIT_CODE', 'UNIT', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['COURSE_NAME', 'DATE_FROM', 'DATE_TO', 'UNIT_CODE', 'UNIT', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'DEPARTMENT'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'DEPARTMENT'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_COURSE_INSTRUCTOR_KEY", func="""
    # def transform_func(s: str):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["LIBRARY_COURSE_INSTRUCTOR_KEY"] = table_1["LIBRARY_COURSE_INSTRUCTOR_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="INSTRUCTOR_NAME", func="""
    # import re
    # def transform_func(s: str):
    #     if not isinstance(s, str):
    #         return s
    #     # collapse repeated whitespace and trim
    #     return re.sub(r'\s+', ' ', s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if not isinstance(s, str):
            return s
        # collapse repeated whitespace and trim
        return re.sub(r'\s+', ' ', s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["INSTRUCTOR_NAME"] = table_1["INSTRUCTOR_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT", func="""
    # import re
    # def transform_func(s: str):
    #     if not isinstance(s, str):
    #         return s
    #     return re.sub(r'\s+', ' ', s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if not isinstance(s, str):
            return s
        return re.sub(r'\s+', ' ', s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT"] = table_1["DEPARTMENT"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'DEPARTMENT'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'DEPARTMENT'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'DEPARTMENT'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'DEPARTMENT'] if c in table_1.columns]
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
def _prep_7(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="LIBRARY_MATERIAL_STATUS", mode="mode")
    # MissingValueImputation
    table_1["LIBRARY_MATERIAL_STATUS"] = table_1["LIBRARY_MATERIAL_STATUS"].fillna(table_1["LIBRARY_MATERIAL_STATUS"].mode().iloc[0])

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep='last').reset_index(drop=True)

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
prepared_tip_material_link = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_tip_material_meta = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_subject_offered = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_library_reserve_links = prepared_table_4
prepared_table_5 = _prep_5(tables['table_3'])
prepared_library_catalog = prepared_table_5
prepared_table_6 = _prep_6(tables['table_7'])
prepared_library_instructors = prepared_table_6
prepared_table_7 = _prep_7(tables['table_9'])
prepared_library_material_status = prepared_table_7

# Assume the prepared tables are already materialized as dataframes with the target columns
so = prepared_subject_offered.copy()
tip_link = prepared_tip_material_link.copy()
tip_meta = prepared_tip_material_meta.copy()
lib_links = prepared_library_reserve_links.copy()
lib_cat = prepared_library_catalog.copy()
lib_status = prepared_library_material_status.copy()
lib_instr = prepared_library_instructors.copy()

# Join TIP subject offerings to material links and metadata
q = tip_link.merge(so, on='TIP_SUBJECT_OFFERED_KEY', how='left')\
        .merge(tip_meta, on='TIP_MATERIAL_KEY', how='left', suffixes=('', '_tipmeta'))

# Join to library reserves via SUBJECT_ID + TERM_CODE
q = q.merge(lib_links, how='left', left_on=['subject_id','TERM_CODE'], right_on=['SUBJECT_ID','TERM_CODE'], suffixes=('', '_lib'))

# Add library catalog details and material status text
q = q.merge(lib_cat, how='left', left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key')\
     .merge(lib_status, how='left', on='LIBRARY_MATERIAL_STATUS_KEY')

# Derive availability flag text
q['Library Availability'] = q['LIBRARY_RESERVE_CATALOG_KEY'].notna().map(lambda x: 'Available in Library' if x else 'Not Available in Library')

# Compute instructors per library book: link instructors via LIBRARY_SUBJECT_OFFERED_KEY = LIBRARY_COURSE_INSTRUCTOR_KEY
# First, count distinct instructors per LIBRARY_RESERVE_CATALOG_KEY
instr_counts = lib_links.merge(lib_instr, left_on='LIBRARY_SUBJECT_OFFERED_KEY', right_on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')\
    .groupby('LIBRARY_RESERVE_CATALOG_KEY', dropna=False)['INSTRUCTOR_NAME'].nunique().rename('Instructors per Library Book').reset_index()

q = q.merge(instr_counts, on='LIBRARY_RESERVE_CATALOG_KEY', how='left')

# Aggregate metrics per department
# Total number of materials available in the library per department
dept_lib_materials = lib_links.merge(so[['SUBJECT_ID','TERM_CODE','OFFER_DEPT_CODE','OFFER_DEPT_NAME']], on=['SUBJECT_ID','TERM_CODE'], how='left')\
    .groupby(['OFFER_DEPT_CODE','OFFER_DEPT_NAME'], dropna=False)['LIBRARY_RESERVE_CATALOG_KEY'].nunique().rename('Total Dept Library Materials').reset_index()

# Total number of available materials across all departments (same unique catalog keys overall)
total_available_all_depts = lib_links['LIBRARY_RESERVE_CATALOG_KEY'].nunique()

# Prepare final per-row fields: department, TIP title/author/ISBN, term code, availability, instructors per book, totals
result = q[
    ['OFFER_DEPT_CODE','OFFER_DEPT_NAME','TITLE','AUTHOR','ISBN','TERM_CODE','Library Availability','LIBRARY_RESERVE_CATALOG_KEY','Instructors per Library Book']
].copy()

# Merge department totals
result = result.merge(dept_lib_materials, on=['OFFER_DEPT_CODE','OFFER_DEPT_NAME'], how='left')

# Fill instructors per book with 0 where missing (no library reserve entry)
result['Instructors per Library Book'] = result['Instructors per Library Book'].fillna(0).astype(int)

# Add global total as a constant column
result['Total Available Materials Across All Departments'] = total_available_all_depts

# Rename columns to match the question wording
result = result.rename(columns={
    'OFFER_DEPT_NAME': 'Department Name',
    'TITLE': 'TIP Material Title',
    'AUTHOR': 'Author',
    'ISBN': 'ISBN',
    'TERM_CODE': 'Library Term Code',
    'Instructors per Library Book': 'Total Instructors per Library Book (Dept)',
    'Total Dept Library Materials': 'Total Materials Available in Library (Dept)'
})

# Select and order output columns
final_columns = [
    'Department Name',
    'TIP Material Title',
    'Author',
    'ISBN',
    'Library Term Code',
    'Library Availability',
    'Total Instructors per Library Book (Dept)',
    'Total Materials Available in Library (Dept)',
    'Total Available Materials Across All Departments'
]

answer = result[final_columns].drop_duplicates()

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
