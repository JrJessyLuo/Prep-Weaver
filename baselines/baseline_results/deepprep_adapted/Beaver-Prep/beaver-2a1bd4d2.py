import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="BUILDING_TYPE", mode="mode")
    # MissingValueImputation
    table_1["BUILDING_TYPE"] = table_1["BUILDING_TYPE"].fillna(table_1["BUILDING_TYPE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_TYPE', 'EXT_GROSS_AREA'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_TYPE', 'EXT_GROSS_AREA'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="EXT_GROSS_AREA", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['EXT_GROSS_AREA'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['EXT_GROSS_AREA']
    if _dtype == "datetime64":
        table_1['EXT_GROSS_AREA'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['EXT_GROSS_AREA'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['EXT_GROSS_AREA'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['EXT_GROSS_AREA'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='first').reset_index(drop=True)

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
    # DropNulls(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'ADDRESS_PURPOSE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'ADDRESS_PURPOSE'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FCLT_BUILDING_KEY", func="""
    # def transform_func(s):
    #     if s is None: 
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None: 
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s
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
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # def transform_func(s):
    #     if s is None: 
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None: 
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NUMBER"] = table_1["BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ADDRESS_PURPOSE", func="""
    # def transform_func(s):
    #     if s is None: 
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None: 
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ADDRESS_PURPOSE"] = table_1["ADDRESS_PURPOSE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="STREET_NUMBER", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["STREET_NUMBER"] = table_1["STREET_NUMBER"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="STREET_NUMBER_SUFFIX", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["STREET_NUMBER_SUFFIX"] = table_1["STREET_NUMBER_SUFFIX"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="PRE_DIRECTIONAL", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["PRE_DIRECTIONAL"] = table_1["PRE_DIRECTIONAL"].apply(_std_apply)

    # ---------------- Step 9 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="STREET_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["STREET_NAME"] = table_1["STREET_NAME"].apply(_std_apply)

    # ---------------- Step 10 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="STREET_SUFFIX", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["STREET_SUFFIX"] = table_1["STREET_SUFFIX"].apply(_std_apply)

    # ---------------- Step 11 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="POST_DIRECTIONAL", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["POST_DIRECTIONAL"] = table_1["POST_DIRECTIONAL"].apply(_std_apply)

    # ---------------- Step 12 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="CITY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["CITY"] = table_1["CITY"].apply(_std_apply)

    # ---------------- Step 13 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="STATE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["STATE"] = table_1["STATE"].apply(_std_apply)

    # ---------------- Step 14 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="POSTAL_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     # keep only digits if it's a simple numeric postal; otherwise keep as-is
    #     digits = ''.join(ch for ch in s if ch.isdigit())
    #     if digits:
    #         # pad to 5 if shorter (common US ZIP); if longer, keep full digit string
    #         return digits.zfill(5) if len(digits) < 5 else digits
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        # keep only digits if it's a simple numeric postal; otherwise keep as-is
        digits = ''.join(ch for ch in s if ch.isdigit())
        if digits:
            # pad to 5 if shorter (common US ZIP); if longer, keep full digit string
            return digits.zfill(5) if len(digits) < 5 else digits
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["POSTAL_CODE"] = table_1["POSTAL_CODE"].apply(_std_apply)

    # ---------------- Step 15 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_building_addresses", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     cols = [
    #         "FCLT_BUILDING_KEY",
    #         "BUILDING_NUMBER",
    #         "ADDRESS_PURPOSE",
    #         "STREET_NUMBER",
    #         "STREET_NUMBER_SUFFIX",
    #         "PRE_DIRECTIONAL",
    #         "STREET_NAME",
    #         "STREET_SUFFIX",
    #         "POST_DIRECTIONAL",
    #         "CITY",
    #         "STATE",
    #         "POSTAL_CODE"
    #     ]
    #     df = table_1.loc[:, cols].copy()
    # 
    #     # De-duplicate to unique address records per building/type (and address components)
    #     df = df.drop_duplicates(subset=cols, keep="first").reset_index(drop=True)
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        cols = [
            "FCLT_BUILDING_KEY",
            "BUILDING_NUMBER",
            "ADDRESS_PURPOSE",
            "STREET_NUMBER",
            "STREET_NUMBER_SUFFIX",
            "PRE_DIRECTIONAL",
            "STREET_NAME",
            "STREET_SUFFIX",
            "POST_DIRECTIONAL",
            "CITY",
            "STATE",
            "POSTAL_CODE"
        ]
        df = table_1.loc[:, cols].copy()

        # De-duplicate to unique address records per building/type (and address components)
        df = df.drop_duplicates(subset=cols, keep="first").reset_index(drop=True)
        return df
    prepared_building_addresses = process_tables(table_1)

    # ---------------- Step 16 ----------------
    # Original operator:
    # Terminate(result=['prepared_building_addresses'])
    # Terminate
    result = {'prepared_building_addresses': prepared_building_addresses}
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
    # CastType(table_name="table_1", column="MIT_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MIT_ID']
    if _dtype == "datetime64":
        table_1['MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MIT_ID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="OFFICE_LOCATION", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['OFFICE_LOCATION'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['OFFICE_LOCATION']
    if _dtype == "datetime64":
        table_1['OFFICE_LOCATION'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['OFFICE_LOCATION'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['OFFICE_LOCATION'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['OFFICE_LOCATION'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFICE_LOCATION", func="""
    # def transform_func(s):
    #     # Keep missing values as-is
    #     if s is None:
    #         return s
    #     s = str(s)
    #     if s.strip().lower() in ["nan", "none", "null", ""]:
    #         return None
    #     # Normalize spacing/casing for consistent downstream parsing (e.g., building extraction)
    #     return s.strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        # Keep missing values as-is
        if s is None:
            return s
        s = str(s)
        if s.strip().lower() in ["nan", "none", "null", ""]:
            return None
        # Normalize spacing/casing for consistent downstream parsing (e.g., building extraction)
        return s.strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFICE_LOCATION"] = table_1["OFFICE_LOCATION"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'OFFICE_LOCATION'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'OFFICE_LOCATION'] if c in table_1.columns]
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BUILDING_COMPONENT", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BUILDING_COMPONENT'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BUILDING_COMPONENT']
    if _dtype == "datetime64":
        table_1['BUILDING_COMPONENT'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BUILDING_COMPONENT'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BUILDING_COMPONENT'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BUILDING_COMPONENT'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_ROOM", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip().upper()
    #     # remove any surrounding quotes
    #     s = s.strip('"').strip("'")
    #     # collapse internal whitespace
    #     s = re.sub(r'\s+', '', s)
    #     # keep typical building-room pattern like '1-073', '1-062D', '1-081F'
    #     m = re.match(r'^([A-Z0-9]+)-([A-Z0-9]+)$', s)
    #     if m:
    #         return f"{m.group(1)}-{m.group(2)}"
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip().upper()
        # remove any surrounding quotes
        s = s.strip('"').strip("'")
        # collapse internal whitespace
        s = re.sub(r'\s+', '', s)
        # keep typical building-room pattern like '1-073', '1-062D', '1-081F'
        m = re.match(r'^([A-Z0-9]+)-([A-Z0-9]+)$', s)
        if m:
            return f"{m.group(1)}-{m.group(2)}"
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_ROOM"] = table_1["BUILDING_ROOM"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_ROOM', 'BUILDING_COMPONENT'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_ROOM', 'BUILDING_COMPONENT'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_ROOM'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_ROOM'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_ROOM', 'BUILDING_COMPONENT'])
    # SelectCol
    _cols = [c for c in ['BUILDING_ROOM', 'BUILDING_COMPONENT'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_6'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_addresses = prepared_table_2
prepared_table_3 = _prep_3(tables['table_10'])
prepared_employees = prepared_table_3
prepared_table_4 = _prep_4(tables['table_9'])
prepared_rooms = prepared_table_4

# Assume prepared_* DataFrames are available
b = prepared_buildings.copy()
# Normalize building number to string for joins
b['BUILDING_NUMBER'] = b['BUILDING_NUMBER'].astype(str).str.strip()
# Standardize building type for special display case later
b['BUILDING_TYPE_NORM'] = b['BUILDING_TYPE'].astype(str).str.strip()

# Addresses join on building key
addr = prepared_addresses.copy()
addr['FCLT_BUILDING_KEY'] = addr['FCLT_BUILDING_KEY'].astype(str).str.strip()
addr['POSTAL_CODE'] = addr['POSTAL_CODE'].astype(str).str.strip()

# Merge building to addresses (many addresses per building)
b_addr = b.merge(addr, on='FCLT_BUILDING_KEY', how='left', suffixes=('', '_addr'))

# Build a canonical street address string for uniqueness
street_parts = [
    b_addr['STREET_NUMBER'].fillna('').astype(str).str.strip(),
    b_addr['STREET_NUMBER_SUFFIX'].fillna('').astype(str).str.strip(),
    b_addr['PRE_DIRECTIONAL'].fillna('').astype(str).str.strip(),
    b_addr['STREET_NAME'].fillna('').astype(str).str.strip(),
    b_addr['STREET_SUFFIX'].fillna('').astype(str).str.strip(),
    b_addr['POST_DIRECTIONAL'].fillna('').astype(str).str.strip()
]
b_addr['STREET_ADDRESS_CANON'] = (
    pd.Series(street_parts).T.apply(lambda r: ' '.join([x for x in r if x])).str.upper().str.replace('\s+', ' ', regex=True).str.strip()
)

# Derive per-building unique address dimensions
addr_agg = b_addr.groupby(['FCLT_BUILDING_KEY'], dropna=False).agg(
    unique_street_address_count=('STREET_ADDRESS_CANON', lambda s: s.dropna().replace('', pd.NA).nunique()),
    unique_city_count=('CITY', lambda s: s.dropna().replace('', pd.NA).str.upper().nunique()),
    unique_state_count=('STATE', lambda s: s.dropna().replace('', pd.NA).str.upper().nunique()),
    unique_postal_code_count=('POSTAL_CODE', lambda s: s.dropna().replace('', pd.NA).nunique())
).reset_index()

# Employees: infer building number from OFFICE_LOCATION by matching BUILDING_ROOM
emp = prepared_employees.copy()
rooms = prepared_rooms.copy()

# Clean fields
emp['OFFICE_LOCATION'] = emp['OFFICE_LOCATION'].astype(str).str.strip()
rooms['BUILDING_ROOM'] = rooms['BUILDING_ROOM'].astype(str).str.strip()
rooms['BUILDING_COMPONENT'] = rooms['BUILDING_COMPONENT'].astype(str).str.strip()

# Inner join employees to rooms via exact office location to building_room
emp_rooms = emp.merge(rooms[['BUILDING_ROOM','BUILDING_COMPONENT']], left_on='OFFICE_LOCATION', right_on='BUILDING_ROOM', how='inner')

# Map room building component to buildings via BUILDING_NUMBER
emp_rooms['BUILDING_COMPONENT'] = emp_rooms['BUILDING_COMPONENT'].astype(str).str.strip()
b['BUILDING_NUMBER'] = b['BUILDING_NUMBER'].astype(str).str.strip()
emp_building = emp_rooms.merge(b[['FCLT_BUILDING_KEY','BUILDING_NUMBER']], left_on='BUILDING_COMPONENT', right_on='BUILDING_NUMBER', how='left')

# Count employees per building key (unique MIT_ID to avoid duplicates)
emp_counts = emp_building.dropna(subset=['FCLT_BUILDING_KEY']).groupby('FCLT_BUILDING_KEY')['MIT_ID'].nunique().reset_index(name='employee_count')

# Combine building-level facts: address dims and employee counts
b_facts = b[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_TYPE_NORM','EXT_GROSS_AREA']].merge(addr_agg, on='FCLT_BUILDING_KEY', how='left').merge(emp_counts, on='FCLT_BUILDING_KEY', how='left')

# Non-subdivisions: buildings without a parent (parent building number null/blank) are not subdivisions.
# Since parent column isn't in prepared schema, recreate from original via a left merge if available; else assume not subdivisions by uniqueness of BUILDING_NUMBER.
# Here we treat any building with a non-null BUILDING_NUMBER as a building; count 1 per building for non-subdivision count.
b_facts['not_subdivision_flag'] = 1

# Clean numerics
b_facts['employee_count'] = b_facts['employee_count'].fillna(0).astype(int)
b_facts['EXT_GROSS_AREA'] = pd.to_numeric(b_facts['EXT_GROSS_AREA'], errors='coerce').fillna(0.0)

# Aggregate per building type
type_grp = b_facts.groupby('BUILDING_TYPE_NORM', dropna=False).agg(
    buildings_not_subdivisions=('not_subdivision_flag','sum'),
    employees=('employee_count','sum'),
    unique_building_street_address=('unique_street_address_count','sum'),
    unique_city=('unique_city_count','sum'),
    unique_state=('unique_state_count','sum'),
    unique_postal_code=('unique_postal_code_count','sum'),
    total_gross_area=('EXT_GROSS_AREA','sum')
).reset_index()

# Average gross square footage per employee
type_grp['avg_gsf_per_employee'] = type_grp.apply(lambda r: (r['total_gross_area'] / r['employees']) if r['employees'] else 0.0, axis=1)

# Rename 'resident' to 'RESIDENTIAL' (case-insensitive match)
type_grp['BUILDING_TYPE_NORM'] = type_grp['BUILDING_TYPE_NORM'].astype(str)
type_grp.loc[type_grp['BUILDING_TYPE_NORM'].str.lower()=='resident', 'BUILDING_TYPE_NORM'] = 'RESIDENTIAL'

# Grand total row
tot = pd.Series({
    'BUILDING_TYPE_NORM':'TOTAL',
    'buildings_not_subdivisions': int(b_facts['not_subdivision_flag'].sum()),
    'employees': int(b_facts['employee_count'].sum()),
    'unique_building_street_address': int(b_facts['unique_street_address_count'].fillna(0).sum()),
    'unique_city': int(b_facts['unique_city_count'].fillna(0).sum()),
    'unique_state': int(b_facts['unique_state_count'].fillna(0).sum()),
    'unique_postal_code': int(b_facts['unique_postal_code_count'].fillna(0).sum()),
    'total_gross_area': float(b_facts['EXT_GROSS_AREA'].sum())
})

tot['avg_gsf_per_employee'] = (tot['total_gross_area'] / tot['employees']) if tot['employees'] else 0.0

answer = pd.concat([type_grp, pd.DataFrame([tot])], ignore_index=True)[[
    'BUILDING_TYPE_NORM',
    'buildings_not_subdivisions',
    'employees',
    'unique_building_street_address',
    'unique_city',
    'unique_state',
    'unique_postal_code',
    'avg_gsf_per_employee'
]].rename(columns={'BUILDING_TYPE_NORM':'building_type'})

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
