import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ACCESS_LEVEL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["ACCESS_LEVEL_NAME"] = table_1["ACCESS_LEVEL_NAME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'BUILDING_NAME', 'ACCESS_LEVEL_CODE', 'ACCESS_LEVEL_NAME'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'BUILDING_NAME', 'ACCESS_LEVEL_CODE', 'ACCESS_LEVEL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FCLT_BUILDING_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FCLT_BUILDING_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FCLT_BUILDING_KEY']
    if _dtype == "datetime64":
        table_1['FCLT_BUILDING_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FCLT_BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FCLT_BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FCLT_BUILDING_KEY'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BUILDING_NUMBER", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BUILDING_NUMBER'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BUILDING_NUMBER']
    if _dtype == "datetime64":
        table_1['BUILDING_NUMBER'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BUILDING_NUMBER'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BUILDING_NUMBER'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BUILDING_NUMBER'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACCESS_LEVEL_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACCESS_LEVEL_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACCESS_LEVEL_CODE']
    if _dtype == "datetime64":
        table_1['ACCESS_LEVEL_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACCESS_LEVEL_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACCESS_LEVEL_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACCESS_LEVEL_CODE'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACCESS_LEVEL_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACCESS_LEVEL_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACCESS_LEVEL_NAME']
    if _dtype == "datetime64":
        table_1['ACCESS_LEVEL_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACCESS_LEVEL_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACCESS_LEVEL_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACCESS_LEVEL_NAME'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MAJOR_USE_DESC", func="""
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MAJOR_USE_DESC"] = table_1["MAJOR_USE_DESC"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="USE_DESC", func="""
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["USE_DESC"] = table_1["USE_DESC"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="USE_DESC_PREP", func="""
    # def compute(row: pd.Series):
    #     use_desc = row.get('USE_DESC')
    #     major = row.get('MAJOR_USE_DESC')
    #     if use_desc is None or (isinstance(use_desc, float) and pd.isna(use_desc)) or str(use_desc).strip() == '':
    #         return major
    #     return use_desc
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        use_desc = row.get('USE_DESC')
        major = row.get('MAJOR_USE_DESC')
        if use_desc is None or (isinstance(use_desc, float) and pd.isna(use_desc)) or str(use_desc).strip() == '':
            return major
        return use_desc
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["USE_DESC_PREP"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['USE_DESC'])
    # DropColumn
    table_1 = table_1.drop(columns=['USE_DESC'], errors='ignore')

    # ---------------- Step 5 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'USE_DESC_PREP', 'new_name': 'USE_DESC'}])
    # Rename
    table_1 = table_1.rename(columns={'USE_DESC_PREP': 'USE_DESC'})

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="AREA", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['AREA'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['AREA']
    if _dtype == "datetime64":
        table_1['AREA'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['AREA'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['AREA'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['AREA'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACCESS_LEVEL", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACCESS_LEVEL'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACCESS_LEVEL']
    if _dtype == "datetime64":
        table_1['ACCESS_LEVEL'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACCESS_LEVEL'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACCESS_LEVEL'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACCESS_LEVEL'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_ROOM_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_ROOM_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_ROOM_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'ROOM', 'SPACE_ID', 'MAJOR_USE_DESC', 'USE_DESC', 'AREA', 'ACCESS_LEVEL', 'ROOM_FULL_NAME'])
    # SelectCol
    _cols = [c for c in ['FCLT_ROOM_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'ROOM', 'SPACE_ID', 'MAJOR_USE_DESC', 'USE_DESC', 'AREA', 'ACCESS_LEVEL', 'ROOM_FULL_NAME'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prep_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prep_rooms = prepared_table_2

# Inputs: prep_buildings, prep_rooms are DataFrames synthesized per targets above

# 1) Filter to Stata building only (Building 32 a.k.a. Stata). Identify by BUILDING_NUMBER == '32' or BUILDING_NAME contains 'Stata'
stata_bldg = prep_buildings[
    (prep_buildings['BUILDING_NUMBER'].astype(str).str.strip() == '32') |
    (prep_buildings['BUILDING_NAME'].astype(str).str.contains('STATA', case=False, na=False)) |
    (prep_buildings['BUILDING_NAME_LONG'].astype(str).str.contains('STATA', case=False, na=False))
].copy()

# 2) Join rooms to the Stata building(s)
rooms = prep_rooms.merge(
    stata_bldg[['FCLT_BUILDING_KEY','ACCESS_LEVEL_CODE','ACCESS_LEVEL_NAME','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG']],
    on='FCLT_BUILDING_KEY', how='inner'
)

# 3) Exclude usage types that include 'STORAGE' (match in either USE_DESC or MAJOR_USE_DESC)
mask_storage = (
    rooms['USE_DESC'].astype(str).str.contains('STORAGE', case=False, na=False) |
    rooms['MAJOR_USE_DESC'].astype(str).str.contains('STORAGE', case=False, na=False)
)
rooms = rooms.loc[~mask_storage].copy()

# 4) Derive usage_type (prefer USE_DESC if present, else MAJOR_USE_DESC)
rooms['usage_type'] = rooms['USE_DESC'].astype(str)
rooms.loc[rooms['usage_type'].isna() | (rooms['usage_type'].str.lower()=='nan') | (rooms['usage_type'].str.strip()==''), 'usage_type'] = rooms['MAJOR_USE_DESC'].astype(str)

# 5) Derive access_level to report (prefer room-level ACCESS_LEVEL if present, else building ACCESS_LEVEL_NAME/ACCESS_LEVEL_CODE)
# Normalize room access to string; if missing, fallback to ACCESS_LEVEL_NAME then ACCESS_LEVEL_CODE
rooms['access_level_str'] = rooms['ACCESS_LEVEL'].astype('Int64').astype(str)
missing_al = rooms['access_level_str'].isin(['<NA>','nan','None'])
rooms.loc[missing_al, 'access_level_str'] = rooms['ACCESS_LEVEL_NAME'].astype(str)
missing_al2 = rooms['access_level_str'].isin(['<NA>','nan','None'])
rooms.loc[missing_al2, 'access_level_str'] = rooms['ACCESS_LEVEL_CODE'].astype(str)

# 6) Define space name from SPACE_ID prefix (building-level space name) or ROOM_FULL_NAME as name; default to SPACE_ID
# Here, treat each SPACE_ID as a space; name it by the building-number + first segment after building if helpful.
rooms['space_name'] = rooms['SPACE_ID'].astype(str)

# 7) Aggregate per space (within access level and usage type): count rooms, total area, avg area
grp_cols = ['access_level_str','usage_type','space_name']
agg = rooms.groupby(grp_cols, dropna=False).agg(
    num_spaces=('SPACE_ID', 'nunique'),  # each SPACE_ID is a space; grouping by it yields 1, but keep for clarity
    num_rooms=('FCLT_ROOM_KEY','nunique'),
    total_area=('AREA','sum'),
    avg_area=('AREA','mean')
).reset_index()
# Since grouping includes space_name, num_spaces will be 1; redefine num_spaces as 1 for each row
agg['num_spaces'] = 1

# 8) Rounding and formatting
for c in ['num_spaces','num_rooms','total_area','avg_area']:
    if c in ['total_area','avg_area']:
        agg[c] = agg[c].round(0).astype('Int64')
    else:
        agg[c] = agg[c].astype('Int64')
for c in ['num_spaces','num_rooms','total_area','avg_area']:
    agg[c] = agg[c].map(lambda x: f"{int(x):,}" if pd.notna(x) else '')

# 9) Build subtotals by space_name, by usage_type within access, by access, and a grand total
# Base detail rows
detail = agg.copy()

# Subtotal per space (within access_level and usage_type): already identical to detail; so skip redundant subtotal

# Subtotal per usage_type within access_level
ut_sub = rooms.groupby(['access_level_str','usage_type']).agg(
    num_spaces=('SPACE_ID','nunique'),
    num_rooms=('FCLT_ROOM_KEY','nunique'),
    total_area=('AREA','sum'),
    avg_area=('AREA','mean')
).reset_index()
ut_sub['space_name'] = 'Subtotal: usage type'

# Subtotal per access_level
al_sub = rooms.groupby(['access_level_str']).agg(
    num_spaces=('SPACE_ID','nunique'),
    num_rooms=('FCLT_ROOM_KEY','nunique'),
    total_area=('AREA','sum'),
    avg_area=('AREA','mean')
).reset_index()
al_sub['usage_type'] = 'Subtotal: access level'
al_sub['space_name'] = ''

# Grand total
gt = pd.DataFrame({
    'access_level_str': ['Grand total'],
    'usage_type': [''],
    'space_name': [''],
    'num_spaces': [rooms['SPACE_ID'].nunique()],
    'num_rooms': [rooms['FCLT_ROOM_KEY'].nunique()],
    'total_area': [rooms['AREA'].sum()],
    'avg_area': [rooms['AREA'].mean()]
})

# Round and format subtotal/grand total blocks
def round_fmt(df):
    df = df.copy()
    for c in ['num_spaces','num_rooms','total_area','avg_area']:
        if c in ['total_area','avg_area']:
            df[c] = df[c].round(0).astype('Int64')
        else:
            df[c] = df[c].astype('Int64')
    for c in ['num_spaces','num_rooms','total_area','avg_area']:
        df[c] = df[c].map(lambda x: f"{int(x):,}" if pd.notna(x) else '')
    return df

ut_sub = round_fmt(ut_sub)
al_sub = round_fmt(al_sub)
gt = round_fmt(gt)

# 10) Concatenate in order: detail rows grouped/sorted by access_level, usage_type, space_name with display rule: show access level only when it changes
out = pd.concat([
    detail.sort_values(['access_level_str','usage_type','space_name']).rename(columns={'access_level_str':'access_level'}),
    ut_sub.rename(columns={'access_level_str':'access_level'}),
    al_sub.rename(columns={'access_level_str':'access_level'}),
    gt.rename(columns={'access_level_str':'access_level'})
], ignore_index=True)

# Apply display rule for access level: blank repeated values in consecutive rows
mask = out['access_level'].astype(str)
shown = []
prev = None
for v in mask:
    if v == prev:
        shown.append('')
    else:
        shown.append(v)
        prev = v
out['access_level'] = shown

# Final columns
result = out[['access_level','usage_type','space_name','num_spaces','total_area','avg_area']]

# The variable 'result' is the final answer table ready for display.

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
