import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="FCLT_ROOM_KEY", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return len(s) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip()
        return len(s) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['FCLT_ROOM_KEY'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FCLT_ROOM_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["FCLT_ROOM_KEY"] = table_1["FCLT_ROOM_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FCLT_BUILDING_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["FCLT_BUILDING_KEY"] = table_1["FCLT_BUILDING_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="ROOM_FULL_NAME_PREP", func="""
    # def compute(row):
    #     # Fill ROOM_FULL_NAME using best available surrogate
    #     val = row.get('ROOM_FULL_NAME')
    #     if val is not None and str(val).strip().lower() not in ('nan', ''):
    #         return str(val).strip()
    #     for c in ['BUILDING_ROOM', 'SPACE_ID', 'FCLT_ROOM_KEY']:
    #         v = row.get(c)
    #         if v is not None and str(v).strip().lower() not in ('nan', ''):
    #             return str(v).strip()
    #     return None
    # """)
    # AddNewColumn
    def compute(row):
        # Fill ROOM_FULL_NAME using best available surrogate
        val = row.get('ROOM_FULL_NAME')
        if val is not None and str(val).strip().lower() not in ('nan', ''):
            return str(val).strip()
        for c in ['BUILDING_ROOM', 'SPACE_ID', 'FCLT_ROOM_KEY']:
            v = row.get(c)
            if v is not None and str(v).strip().lower() not in ('nan', ''):
                return str(v).strip()
        return None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["ROOM_FULL_NAME_PREP"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['ROOM_FULL_NAME'])
    # DropColumn
    table_1 = table_1.drop(columns=['ROOM_FULL_NAME'], errors='ignore')

    # ---------------- Step 6 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'ROOM_FULL_NAME_PREP', 'new_name': 'ROOM_FULL_NAME'}])
    # Rename
    table_1 = table_1.rename(columns={'ROOM_FULL_NAME_PREP': 'ROOM_FULL_NAME'})

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_ROOM_KEY', 'ROOM_FULL_NAME', 'FCLT_BUILDING_KEY'])
    # SelectCol
    _cols = [c for c in ['FCLT_ROOM_KEY', 'ROOM_FULL_NAME', 'FCLT_BUILDING_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_ROOM_KEY', 'FCLT_BUILDING_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_ROOM_KEY', 'FCLT_BUILDING_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_ROOM_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_ROOM_KEY'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_NAME_LONG'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_NAME_LONG'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_HEIGHT'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_HEIGHT'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # collapse repeated whitespace
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # collapse repeated whitespace
        return " ".join(s.split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME_LONG", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["BUILDING_NAME_LONG"] = table_1["BUILDING_NAME_LONG"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BUILDING_HEIGHT", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BUILDING_HEIGHT'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BUILDING_HEIGHT']
    if _dtype == "datetime64":
        table_1['BUILDING_HEIGHT'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BUILDING_HEIGHT'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BUILDING_HEIGHT'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BUILDING_HEIGHT'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='last').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="STREET_SUFFIX", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['STREET_SUFFIX'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['STREET_SUFFIX']
    if _dtype == "datetime64":
        table_1['STREET_SUFFIX'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['STREET_SUFFIX'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['STREET_SUFFIX'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['STREET_SUFFIX'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BUILDING_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BUILDING_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BUILDING_KEY']
    if _dtype == "datetime64":
        table_1['BUILDING_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BUILDING_KEY'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ADDRESS_PURPOSE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ADDRESS_PURPOSE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ADDRESS_PURPOSE']
    if _dtype == "datetime64":
        table_1['ADDRESS_PURPOSE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ADDRESS_PURPOSE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ADDRESS_PURPOSE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ADDRESS_PURPOSE'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="STREET_NUMBER", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['STREET_NUMBER'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['STREET_NUMBER']
    if _dtype == "datetime64":
        table_1['STREET_NUMBER'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['STREET_NUMBER'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['STREET_NUMBER'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['STREET_NUMBER'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="STREET_NUMBER_SUFFIX", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['STREET_NUMBER_SUFFIX'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['STREET_NUMBER_SUFFIX']
    if _dtype == "datetime64":
        table_1['STREET_NUMBER_SUFFIX'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['STREET_NUMBER_SUFFIX'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['STREET_NUMBER_SUFFIX'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['STREET_NUMBER_SUFFIX'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="PRE_DIRECTIONAL", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['PRE_DIRECTIONAL'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['PRE_DIRECTIONAL']
    if _dtype == "datetime64":
        table_1['PRE_DIRECTIONAL'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['PRE_DIRECTIONAL'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['PRE_DIRECTIONAL'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['PRE_DIRECTIONAL'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="STREET_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['STREET_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['STREET_NAME']
    if _dtype == "datetime64":
        table_1['STREET_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['STREET_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['STREET_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['STREET_NAME'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="POST_DIRECTIONAL", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['POST_DIRECTIONAL'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['POST_DIRECTIONAL']
    if _dtype == "datetime64":
        table_1['POST_DIRECTIONAL'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['POST_DIRECTIONAL'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['POST_DIRECTIONAL'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['POST_DIRECTIONAL'] = _series.astype(str)

    # ---------------- Step 9 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CITY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CITY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CITY']
    if _dtype == "datetime64":
        table_1['CITY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CITY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CITY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CITY'] = _series.astype(str)

    # ---------------- Step 10 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="STATE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['STATE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['STATE']
    if _dtype == "datetime64":
        table_1['STATE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['STATE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['STATE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['STATE'] = _series.astype(str)

    # ---------------- Step 11 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="POSTAL_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['POSTAL_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['POSTAL_CODE']
    if _dtype == "datetime64":
        table_1['POSTAL_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['POSTAL_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['POSTAL_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['POSTAL_CODE'] = _series.astype(str)

    # ---------------- Step 12 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="STREET_SUFFIX", func="""
    # def transform_func(s: str):
    #     # Convert string-literal missing markers to empty (so it behaves like missing downstream)
    #     if s is None:
    #         return s
    #     v = str(s).strip()
    #     if v.lower() in {"nan", "none", "null", ""}:
    #         return ""
    #     return v
    # """)
    # StandardizeString
    def transform_func(s: str):
        # Convert string-literal missing markers to empty (so it behaves like missing downstream)
        if s is None:
            return s
        v = str(s).strip()
        if v.lower() in {"nan", "none", "null", ""}:
            return ""
        return v
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["STREET_SUFFIX"] = table_1["STREET_SUFFIX"].apply(_std_apply)

    # ---------------- Step 13 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_4(table_1):
    return table_1.copy()
def _prep_5(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="subject_id", func="""
    # def transform_func(s):
    #     return str(s).strip() if s is not None else s
    # """)
    # StandardizeString
    def transform_func(s):
        return str(s).strip() if s is not None else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["subject_id"] = table_1["subject_id"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['subject_id', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['subject_id', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s):
    #     return str(s).strip() if s is not None and str(s) != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        return str(s).strip() if s is not None and str(s) != 'nan' else None
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
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s):
    #     return str(s).strip() if s is not None and str(s) != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        return str(s).strip() if s is not None and str(s) != 'nan' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['subject_id', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['subject_id', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['subject_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['subject_id'], keep='last').reset_index(drop=True)

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
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_building_addresses = prepared_table_3
prepared_table_4 = _prep_4(tables['table_9'])
prepared_table_5 = _prep_5(tables['table_8'])
prepared_subjects = prepared_table_5

# Inputs assumed to be dataframes with names matching target_table_name
# prepared_rooms, prepared_buildings, prepared_building_addresses, prepared_subjects

# 1) Identify subjects that Computer Science students can enroll in.
# Heuristic: subjects offered by EECS department (DEPARTMENT_CODE == '6' or DEPARTMENT_NAME contains 'Computer Sci').
cs_subjects = prepared_subjects[(prepared_subjects['DEPARTMENT_CODE'] == '6') | (prepared_subjects['DEPARTMENT_NAME'].str.contains('Computer Sci', case=False, na=False))]

# 2) We need rooms associated with those subjects. No direct subject-to-room mapping is present in the selected tables.
# Therefore, we cannot filter rooms by subjects with the current inputs. Proceed by returning empty result if association data is missing.
# If another table providing section/meeting locations linked by subject_id and room (e.g., meeting schedule) is available, join it here.

# Compose building info (for potential later filtering once room-subject association exists)
rooms_buildings = prepared_rooms.merge(prepared_buildings, on='FCLT_BUILDING_KEY', how='left')

# Keep street addresses only from addresses table
addr_street = prepared_building_addresses[prepared_building_addresses['ADDRESS_PURPOSE'].str.upper().eq('STREET')]

rooms_bldg_addr = rooms_buildings.merge(addr_street, left_on='FCLT_BUILDING_KEY', right_on='BUILDING_KEY', how='left')

# Compose street address string
def compose_address(row):
    parts = [str(row.get('STREET_NUMBER') or '').strip(), str(row.get('STREET_NUMBER_SUFFIX') or '').strip(), str(row.get('PRE_DIRECTIONAL') or '').strip(), str(row.get('STREET_NAME') or '').strip(), str(row.get('STREET_SUFFIX') or '').strip(), str(row.get('POST_DIRECTIONAL') or '').strip()]
    parts = [p for p in parts if p and p.lower() != 'nan']
    return ' '.join(parts) if parts else None

rooms_bldg_addr['STREET_ADDRESS'] = rooms_bldg_addr.apply(compose_address, axis=1)

# Placeholder for subject-room association: expecting a dataframe 'subject_room' with columns ['subject_id','FCLT_ROOM_KEY'].
# If available, uncomment and integrate as below:
# associated_rooms = subject_room.merge(cs_subjects[['subject_id']], on='subject_id', how='inner').drop_duplicates('FCLT_ROOM_KEY')
# result = associated_rooms.merge(rooms_bldg_addr, on='FCLT_ROOM_KEY', how='left')
# Otherwise, return empty with correct columns.

# Prepare final columns and ensure uniqueness
cols = ['ROOM_FULL_NAME', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'STREET_ADDRESS', 'CITY', 'STATE', 'POSTAL_CODE', 'BUILDING_HEIGHT']
empty = pd.DataFrame(columns=cols)

# If association exists, replace 'empty' with the computed 'result[cols].drop_duplicates()'
# result = result[cols].drop_duplicates()
# target = result

target = empty

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
