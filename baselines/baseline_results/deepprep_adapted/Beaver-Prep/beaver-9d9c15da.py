import pandas as pd
import numpy as np

def _prep_1(table_1):
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SUBJECT_SUMMARY_KEY', 'TERM_CODE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SUBJECT_SUMMARY_KEY', 'TERM_CODE'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_SUMMARY_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_NAME', 'CLUSTER_TYPE', 'HGN_CODE', 'SUBJECT_ENROLLMENT_NUMBER', 'CLUSTER_ENROLLMENT_NUMBER'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_SUMMARY_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_NAME', 'CLUSTER_TYPE', 'HGN_CODE', 'SUBJECT_ENROLLMENT_NUMBER', 'CLUSTER_ENROLLMENT_NUMBER'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
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
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # collapse repeated whitespace
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # collapse repeated whitespace
        return " ".join(str(s).strip().split())
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
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return " ".join(str(s).strip().split())
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
    # StandardizeString(table_name="table_1", column_name="CLUSTER_TYPE", func="""
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
    table_1["CLUSTER_TYPE"] = table_1["CLUSTER_TYPE"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="HGN_CODE", func="""
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
    table_1["HGN_CODE"] = table_1["HGN_CODE"].apply(_std_apply)

    # ---------------- Step 9 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SUBJECT_ENROLLMENT_NUMBER", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SUBJECT_ENROLLMENT_NUMBER'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SUBJECT_ENROLLMENT_NUMBER']
    if _dtype == "datetime64":
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = _series.astype(str)

    # ---------------- Step 10 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CLUSTER_ENROLLMENT_NUMBER", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CLUSTER_ENROLLMENT_NUMBER'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CLUSTER_ENROLLMENT_NUMBER']
    if _dtype == "datetime64":
        table_1['CLUSTER_ENROLLMENT_NUMBER'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CLUSTER_ENROLLMENT_NUMBER'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CLUSTER_ENROLLMENT_NUMBER'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CLUSTER_ENROLLMENT_NUMBER'] = _series.astype(str)

    # ---------------- Step 11 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="SUBJECT_ENROLLMENT_NUMBER", mode="median")
    # MissingValueImputation
    table_1["SUBJECT_ENROLLMENT_NUMBER"] = table_1["SUBJECT_ENROLLMENT_NUMBER"].fillna(table_1["SUBJECT_ENROLLMENT_NUMBER"].median())

    # ---------------- Step 12 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="CLUSTER_ENROLLMENT_NUMBER", mode="median")
    # MissingValueImputation
    table_1["CLUSTER_ENROLLMENT_NUMBER"] = table_1["CLUSTER_ENROLLMENT_NUMBER"].fillna(table_1["CLUSTER_ENROLLMENT_NUMBER"].median())

    # ---------------- Step 13 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SUBJECT_SUMMARY_KEY', 'TERM_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SUBJECT_SUMMARY_KEY', 'TERM_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 14 ----------------
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
    # OutlierDetection(table_name="table_1", column_name="NUM_ENROLLED_STUDENTS", action="add_tag")
    # OutlierDetection (IQR method)
    _q1 = table_1['NUM_ENROLLED_STUDENTS'].quantile(0.25)
    _q3 = table_1['NUM_ENROLLED_STUDENTS'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] = table_1['NUM_ENROLLED_STUDENTS'].apply(lambda x: True if x < _low or x > _high else False)
    if 'add_tag' == 'delete':
        table_1 = table_1[table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] == False]
        table_1.drop(columns=['table_1_NUM_ENROLLED_STUDENTS_is_outlier'], inplace=True)
    elif 'add_tag' == 'add_tag':
        table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] = table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" and s.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" and s.lower() != "nan" else None
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
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" and s.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" and s.lower() != "nan" else None
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
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" and s.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" and s.lower() != "nan" else None
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
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" and s.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" and s.lower() != "nan" else None
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
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" and s.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" and s.lower() != "nan" else None
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
    # MissingValueImputation(table_name="table_1", column_name="NUM_ENROLLED_STUDENTS", mode="median")
    # MissingValueImputation
    table_1["NUM_ENROLLED_STUDENTS"] = table_1["NUM_ENROLLED_STUDENTS"].fillna(table_1["NUM_ENROLLED_STUDENTS"].median())

    # ---------------- Step 8 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_ENROLLED_STUDENTS", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NUM_ENROLLED_STUDENTS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NUM_ENROLLED_STUDENTS']
    if _dtype == "datetime64":
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NUM_ENROLLED_STUDENTS'] = _series.astype(str)

    # ---------------- Step 9 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 10 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 11 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 12 ----------------
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
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY', 'ISBN', 'RECORD_COUNT'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY', 'ISBN', 'RECORD_COUNT'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="subject_id", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
    #         return None
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
            return None
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
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
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
    #         return None
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
            return None
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ISBN", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
    #         return None
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
            return None
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
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

    # ---------------- Step 5 ----------------
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

    # ---------------- Step 6 ----------------
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

    # ---------------- Step 7 ----------------
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

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY', 'ISBN', 'RECORD_COUNT'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY', 'ISBN', 'RECORD_COUNT'], keep='first').reset_index(drop=True)

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
def _prep_5(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="RENTAL_NEW_PRICE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['RENTAL_NEW_PRICE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['RENTAL_NEW_PRICE']
    if _dtype == "datetime64":
        table_1['RENTAL_NEW_PRICE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['RENTAL_NEW_PRICE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['RENTAL_NEW_PRICE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['RENTAL_NEW_PRICE'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NEW_SHELF_PRICE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NEW_SHELF_PRICE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NEW_SHELF_PRICE']
    if _dtype == "datetime64":
        table_1['NEW_SHELF_PRICE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NEW_SHELF_PRICE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NEW_SHELF_PRICE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NEW_SHELF_PRICE'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="USED_SHELF_PRICE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['USED_SHELF_PRICE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['USED_SHELF_PRICE']
    if _dtype == "datetime64":
        table_1['USED_SHELF_PRICE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['USED_SHELF_PRICE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['USED_SHELF_PRICE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['USED_SHELF_PRICE'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_KEY"] = table_1["TIP_MATERIAL_KEY"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ISBN", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # normalize common missing tokens
    #     if s.lower() in {"nan", "none", ""}:
    #         return None
    #     # keep digits/X only (ISBN10 may end with X)
    #     cleaned = re.sub(r'[^0-9Xx]', '', s).upper()
    #     return cleaned if cleaned else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # normalize common missing tokens
        if s.lower() in {"nan", "none", ""}:
            return None
        # keep digits/X only (ISBN10 may end with X)
        cleaned = re.sub(r'[^0-9Xx]', '', s).upper()
        return cleaned if cleaned else None
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
    # StandardizeString(table_name="table_1", column_name="TITLE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # collapse repeated internal whitespace
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # collapse repeated internal whitespace
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TITLE"] = table_1["TITLE"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MATERIAL_INFO_SOURCE", func="""
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
    table_1["MATERIAL_INFO_SOURCE"] = table_1["MATERIAL_INFO_SOURCE"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_MATERIAL_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_MATERIAL_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE', 'MATERIAL_INFO_SOURCE'])
    # SelectCol
    _cols = [c for c in ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE', 'MATERIAL_INFO_SOURCE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
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

prepared_table_1 = _prep_1(tables['table_7'])
prepared_table_2 = _prep_2(tables['table_3'])
prepared_subject_offerings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_tip_subjects = prepared_table_3
prepared_table_4 = _prep_4(tables['table_1'])
prepared_tip_material_links = prepared_table_4
prepared_table_5 = _prep_5(tables['table_4'])
prepared_tip_materials = prepared_table_5

# Start from prepared per-table dataframes: prepared_subject_offerings (table_2), prepared_tip_subjects (table_3), prepared_tip_material_links (table_4), prepared_tip_materials (table_5)

# 1) Filter biology courses: SUBJECT_TITLE contains 'Biology' (case-insensitive)
biol = prepared_subject_offerings[prepared_subject_offerings['SUBJECT_TITLE'].str.contains('biology', case=True, na=False) | prepared_subject_offerings['SUBJECT_TITLE'].str.contains('Biology', na=False)]

# 2) Join offerings to TIP subjects on (SUBJECT_ID, TERM_CODE)
basel = biol.merge(prepared_tip_subjects, how='left', left_on=['SUBJECT_ID','TERM_CODE'], right_on=['SUBJECT_ID','TERM_CODE'], suffixes=('', '_tip'))

# 3) Bring in TIP subject->material links via TIP_SUBJECT_OFFERED_KEY
links = basel.merge(prepared_tip_material_links, how='left', left_on='TIP_SUBJECT_OFFERED_KEY', right_on='TIP_SUBJECT_OFFERED_KEY')

# 4) Bring in material pricing
full = links.merge(prepared_tip_materials, how='left', left_on='TIP_MATERIAL_KEY', right_on='TIP_MATERIAL_KEY', suffixes=('', '_mat'))

# 5) Compute aggregations needed per group: by (CLUSTER_TYPE, HGN_CODE)
# First, per subject offering compute material-level stats
agg_per_subject = full.groupby(['SUBJECT_SUMMARY_KEY','CLUSTER_TYPE','HGN_CODE','OFFER_DEPT_NAME','SUBJECT_TITLE'], dropna=False).agg(
    total_enroll=('SUBJECT_ENROLLMENT_NUMBER','sum'),
    cluster_enroll=('CLUSTER_ENROLLMENT_NUMBER','mean'),
    num_unique_materials=('TIP_MATERIAL_KEY', lambda x: x.dropna().nunique()),
    avg_new_price_tip=('NEW_SHELF_PRICE','mean'),
    avg_used_price_tip=('USED_SHELF_PRICE','mean'),
    tip_material_record_count=('RECORD_COUNT','sum'),
    num_unique_library_titles=('TITLE', lambda x: x.dropna().nunique()),
    num_unique_library_isbns=('ISBN', lambda x: x.dropna().nunique())
).reset_index()

# 6) For each (CLUSTER_TYPE, HGN_CODE) group, list required columns per subject offering
# Also compute average enrollment within its cluster: interpreted as average SUBJECT_ENROLLMENT_NUMBER within same CLUSTER_TYPE; compute from agg_per_subject
cluster_avg = agg_per_subject.groupby(['CLUSTER_TYPE']).agg(
    avg_enroll_within_cluster=('total_enroll','mean')
).reset_index()

result = agg_per_subject.merge(cluster_avg, how='left', on='CLUSTER_TYPE')

# 7) Select and rename columns to match the question wording
result = result.rename(columns={
    'OFFER_DEPT_NAME': 'department_name',
    'SUBJECT_TITLE': 'course_title',
    'CLUSTER_TYPE': 'cluster_type',
    'HGN_CODE': 'course_level',
    'total_enroll': 'total_enrollments',
    'avg_new_price_tip': 'avg_new_price_tip_materials',
    'avg_used_price_tip': 'avg_used_price_tip_materials',
    'tip_material_record_count': 'total_tip_material_record_count',
    'num_unique_library_titles': 'unique_library_titles',
    'num_unique_library_isbns': 'unique_library_isbns',
    'num_unique_materials': 'unique_course_materials'
})

# 8) Final ordering
result = result[[
    'department_name', 'course_title', 'cluster_type', 'total_enrollments',
    'avg_enroll_within_cluster', 'course_level', 'unique_course_materials',
    'avg_new_price_tip_materials', 'avg_used_price_tip_materials',
    'total_tip_material_record_count', 'unique_library_titles', 'unique_library_isbns'
]].sort_values(['cluster_type','course_level','department_name','course_title'])

answer = result

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
