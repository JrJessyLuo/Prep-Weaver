import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # keep non-negative (or null) areas/heights
    #     for c in ['BUILDING_HEIGHT','ASSIGNABLE_AREA','EXT_GROSS_AREA']:
    #         v = row.get(c)
    #         if v is not None and v == v and v < 0:
    #             return False
    #     return True
    # """)
    # Filter
    def filter_func(row):
        # keep non-negative (or null) areas/heights
        for c in ['BUILDING_HEIGHT','ASSIGNABLE_AREA','EXT_GROSS_AREA']:
            v = row.get(c)
            if v is not None and v == v and v < 0:
                return False
        return True
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_NUMBER'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_NUMBER'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_NUMBER'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_NUMBER'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and s != s):
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and s != s):
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME_LONG", func="""
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and s != s):
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and s != s):
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME_LONG"] = table_1["BUILDING_NAME_LONG"].apply(_std_apply)

    # ---------------- Step 6 ----------------
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

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ASSIGNABLE_AREA", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ASSIGNABLE_AREA'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ASSIGNABLE_AREA']
    if _dtype == "datetime64":
        table_1['ASSIGNABLE_AREA'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ASSIGNABLE_AREA'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ASSIGNABLE_AREA'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ASSIGNABLE_AREA'] = _series.astype(str)

    # ---------------- Step 8 ----------------
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

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_HEIGHT', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA'])
    # SelectCol
    _cols = [c for c in ['BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_HEIGHT', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA'] if c in table_1.columns]
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
def _prep_2(table_1):
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_STREET_ADDRESS", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     # collapse repeated whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     # normalize common street suffix (simple, conservative rule)
    #     s = re.sub(r'\bST\b', 'STREET', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip().upper()
        # collapse repeated whitespace
        s = re.sub(r'\s+', ' ', s)
        # normalize common street suffix (simple, conservative rule)
        s = re.sub(r'\bST\b', 'STREET', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_STREET_ADDRESS"] = table_1["BUILDING_STREET_ADDRESS"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # collapse repeated whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # collapse repeated whitespace
        s = re.sub(r'\s+', ' ', s)
        return s
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
    # Deduplicate(table_name="table_1", subset=['BUILDING_NUMBER'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_NUMBER'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'])
    # SelectCol
    _cols = [c for c in ['BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'] if c in table_1.columns]
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="HR_DEPARTMENT_NAME", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     if s == "" or s.lower() in {"nan", "none", "null"}:
    #         return False
    #     return True
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip()
        if s == "" or s.lower() in {"nan", "none", "null"}:
            return False
        return True
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['HR_DEPARTMENT_NAME'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['HR_DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['HR_DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="HR_DEPARTMENT_NAME", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # treat common null-like tokens as missing
    #     if s == "" or s.lower() in {"nan", "none", "null"}:
    #         return None
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize internal whitespace
    #     s = re.sub(r"\s+", " ", s).strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # treat common null-like tokens as missing
        if s == "" or s.lower() in {"nan", "none", "null"}:
            return None
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize internal whitespace
        s = re.sub(r"\s+", " ", s).strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["HR_DEPARTMENT_NAME"] = table_1["HR_DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['HR_DEPARTMENT_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['HR_DEPARTMENT_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['HR_DEPARTMENT_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['HR_DEPARTMENT_NAME'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['HR_DEPARTMENT_NAME'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['HR_DEPARTMENT_NAME'], ascending=[True])

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

prepared_table_1 = _prep_1(tables['table_4'])
prepared_buildings_core = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_table_3 = _prep_3(tables['table_1'])
prepared_building_addresses = prepared_table_3
prepared_table_4 = _prep_4(tables['table_8'])
prepared_hr_departments = prepared_table_4

# Merge core building data with addresses on BUILDING_NUMBER
b = merge(prepared_buildings_core, prepared_building_addresses, on='BUILDING_NUMBER', how='left')

# Choose a building name preference order: use BUILDING_NAME from core if present, else from addresses, else BUILDING_NAME_LONG
b['BUILDING_NAME_FINAL'] = b['BUILDING_NAME_x'].fillna(b['BUILDING_NAME_y']).fillna(b['BUILDING_NAME_LONG'])

# Derive required outputs
result = b.rename(columns={
    'BUILDING_NUMBER': 'building_number',
    'BUILDING_NAME_FINAL': 'building_name',
    'BUILDING_HEIGHT': 'building_height',
    'BUILDING_STREET_ADDRESS': 'street_address',
    'ASSIGNABLE_AREA': 'assignable_square_footage',
    'EXT_GROSS_AREA': 'total_square_footage'
})

# Average square footage (assignable) as requested context; if intended as per-room or per-building average not defined in data, compute assignable avg per building = assignable/1
# Here interpret as average of assignable and non-assignable not available; fall back to average per building using total/1. If both present, compute average of assignable and total.
result['average_square_footage'] = np.where(
    result['assignable_square_footage'].notna() & result['total_square_footage'].notna(),
    (result['assignable_square_footage'] + result['total_square_footage']) / 2.0,
    result['assignable_square_footage'].fillna(result['total_square_footage'])
)

# No city/state columns exist in selected tables; set as MIT default placeholders if required
result['city'] = np.nan
result['state'] = np.nan

# HR department name not linkable from provided schemas; leave null
result['HR_department_name'] = np.nan

# Select and order columns
result = result[[
    'building_name',
    'building_number',
    'building_height',
    'street_address',
    'city',
    'state',
    'HR_department_name',
    'assignable_square_footage',
    'total_square_footage',
    'average_square_footage'
]]

# Order descending by assignable, then total, then average square footage
result = result.sort_values(by=['assignable_square_footage','total_square_footage','average_square_footage'], ascending=[False, False, False])

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
