import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ORGANIZATION_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ORGANIZATION_NAME"] = table_1["ORGANIZATION_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="AREA", mode="median")
    # MissingValueImputation
    table_1["AREA"] = table_1["AREA"].fillna(table_1["AREA"].median())

    # ---------------- Step 5 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row['ORGANIZATION_NAME'] == 'DOF'
    # """)
    # Filter
    def filter_func(row):
        return row['ORGANIZATION_NAME'] == 'DOF'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'AREA', 'ORGANIZATION_NAME', 'ACCESS_LEVEL'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'AREA', 'ORGANIZATION_NAME', 'ACCESS_LEVEL'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'AREA', 'ORGANIZATION_NAME', 'ACCESS_LEVEL'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM', 'AREA', 'ORGANIZATION_NAME', 'ACCESS_LEVEL'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_KEY", func="""
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
    table_1["BUILDING_KEY"] = table_1["BUILDING_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FLOOR", func="""
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
    table_1["FLOOR"] = table_1["FLOOR"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FLOOR_KEY", func="""
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
    table_1["FLOOR_KEY"] = table_1["FLOOR_KEY"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FLOOR", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FLOOR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FLOOR']
    if _dtype == "datetime64":
        table_1['FLOOR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FLOOR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FLOOR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FLOOR'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FLOOR_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FLOOR_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FLOOR_KEY']
    if _dtype == "datetime64":
        table_1['FLOOR_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FLOOR_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FLOOR_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FLOOR_KEY'] = _series.astype(str)

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
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['WAREHOUSE_LOAD_DATE', 'FLOOR_SORT_SEQUENCE'], ascending=[False, True])
    # Sort
    table_1 = table_1.sort_values(by=['WAREHOUSE_LOAD_DATE', 'FLOOR_SORT_SEQUENCE'], ascending=[False, True])

    # ---------------- Step 10 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FLOOR_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FLOOR_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 11 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ACCESS_LEVEL'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ACCESS_LEVEL'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 12 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['BUILDING_KEY', 'FLOOR'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['BUILDING_KEY', 'FLOOR'], ascending=[True, True])

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FAC_BUILDING_KEY', 'BUILDING_NUMBER'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FAC_BUILDING_KEY', 'BUILDING_NUMBER'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'ACCESS_LEVEL_CODE'])
    # SelectCol
    _cols = [c for c in ['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'ACCESS_LEVEL_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACCESS_LEVEL_CODE", dtype="int")
    # CastType
    _dtype = 'int'
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FAC_BUILDING_KEY', 'BUILDING_NUMBER'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FAC_BUILDING_KEY', 'BUILDING_NUMBER'], keep='first').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_STREET_ADDRESS", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     # collapse repeated whitespace
    #     s = re.sub(r'\s+', ' ', s).strip()
    # 
    #     # normalize common suffix abbreviations at word boundaries
    #     # e.g., 'ALBANY ST' -> 'ALBANY STREET'
    #     s = re.sub(r'\bST\b', 'STREET', s)
    #     s = re.sub(r'\bAVE\b', 'AVENUE', s)
    #     s = re.sub(r'\bRD\b', 'ROAD', s)
    #     s = re.sub(r'\bDR\b', 'DRIVE', s)
    #     s = re.sub(r'\bBLVD\b', 'BOULEVARD', s)
    # 
    #     # final whitespace cleanup
    #     s = re.sub(r'\s+', ' ', s).strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        # collapse repeated whitespace
        s = re.sub(r'\s+', ' ', s).strip()

        # normalize common suffix abbreviations at word boundaries
        # e.g., 'ALBANY ST' -> 'ALBANY STREET'
        s = re.sub(r'\bST\b', 'STREET', s)
        s = re.sub(r'\bAVE\b', 'AVENUE', s)
        s = re.sub(r'\bRD\b', 'ROAD', s)
        s = re.sub(r'\bDR\b', 'DRIVE', s)
        s = re.sub(r'\bBLVD\b', 'BOULEVARD', s)

        # final whitespace cleanup
        s = re.sub(r'\s+', ' ', s).strip()
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
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prep_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prep_floors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prep_buildings_meta = prepared_table_3
prepared_table_4 = _prep_4(tables['table_10'])
prep_buildings_addr = prepared_table_4

# Assume the prepared tables already exist: prep_rooms, prep_floors, prep_buildings_meta, prep_buildings_addr

# 1) Filter to Facilities department rooms (e.g., ORGANIZATION_NAME == 'DOF')
rooms_fac = prep_rooms[prep_rooms['ORGANIZATION_NAME'].str.upper() == 'DOF']

# 2) Join floor metadata (if needed for corroboration; not strictly required for metrics)
rooms_fac = rooms_fac.merge(prep_floors[['FLOOR_KEY','ACCESS_LEVEL']].rename(columns={'ACCESS_LEVEL':'ACCESS_LEVEL_FLOOR'}), on='FLOOR_KEY', how='left')

# 3) Join building metadata for building name and building-level access evidence
rooms_fac = rooms_fac.merge(
    prep_buildings_meta[['BUILDING_NUMBER','BUILDING_NAME','ACCESS_LEVEL_CODE']].rename(columns={'BUILDING_NUMBER':'BUILDING_KEY_META'}),
    left_on='BUILDING_KEY', right_on='BUILDING_KEY_META', how='left'
)
# Prefer building name from meta when available, else fall back later to addr table name

# 4) Join building address table for street address (to parse ZIP and City) and alternate building name
rooms_fac = rooms_fac.merge(
    prep_buildings_addr[['BUILDING_NUMBER','BUILDING_NAME','BUILDING_STREET_ADDRESS']].rename(columns={'BUILDING_NUMBER':'BUILDING_KEY_ADDR','BUILDING_NAME':'BUILDING_NAME_ADDR'}),
    left_on='BUILDING_KEY', right_on='BUILDING_KEY_ADDR', how='left'
)

# 5) Choose building name and access level for output
rooms_fac['BUILDING_NAME_OUT'] = rooms_fac['BUILDING_NAME'].combine_first(rooms_fac['BUILDING_NAME_ADDR'])
# Access level preference: room's ACCESS_LEVEL, else building ACCESS_LEVEL_CODE, else floor access
rooms_fac['ACCESS_LEVEL_OUT'] = rooms_fac['ACCESS_LEVEL'].fillna(rooms_fac['ACCESS_LEVEL_CODE']).fillna(rooms_fac['ACCESS_LEVEL_FLOOR'])

# 6) Parse ZIP and City from BUILDING_STREET_ADDRESS when possible
# Expect formats like "235  ALBANY ST" without city/zip in many rows; if city/zip absent, leave NaN

def parse_city_zip(addr):
    if not isinstance(addr, str):
        return pd.Series({'CITY': pd.NA, 'ZIP': pd.NA})
    # Try patterns like "City, ST 02139" or trailing ZIP 5-digits
    mzip = re.search(r'(\b\d{5})(?:-\d{4})?\b', addr)
    zipc = mzip.group(1) if mzip else pd.NA
    # crude city extraction: token(s) before state code and ZIP
    mcity = re.search(r'([^,\d]+),\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?\b', addr)
    city = mcity.group(1).strip() if mcity else pd.NA
    return pd.Series({'CITY': city, 'ZIP': zipc})

addr_parsed = rooms_fac['BUILDING_STREET_ADDRESS'].apply(parse_city_zip)
rooms_fac = pd.concat([rooms_fac, addr_parsed], axis=1)

# 7) Compute per floor metrics: number of rooms and total area
# Ensure AREA numeric
rooms_fac['AREA_NUM'] = pd.to_numeric(rooms_fac['AREA'], errors='coerce')

floor_group = rooms_fac.groupby(['BUILDING_KEY','FLOOR_KEY','FLOOR'], dropna=False).agg(
    ROOMS_COUNT=('ROOM','nunique'),
    TOTAL_AREA=('AREA_NUM','sum')
).reset_index()

# Attach building name/access/zip/city to floor rows
floor_enriched = floor_group.merge(
    rooms_fac[['BUILDING_KEY','FLOOR_KEY','BUILDING_NAME_OUT','ACCESS_LEVEL_OUT','ZIP','CITY']].drop_duplicates(subset=['BUILDING_KEY','FLOOR_KEY']),
    on=['BUILDING_KEY','FLOOR_KEY'], how='left'
)

# Average area per floor at building level will be computed from building-level aggregation

# 8) Building-level subtotals
bldg_totals = floor_group.groupby('BUILDING_KEY', dropna=False).agg(
    ROOMS_COUNT=('ROOMS_COUNT','sum'),
    TOTAL_AREA=('TOTAL_AREA','sum'),
    FLOORS=('FLOOR_KEY','nunique')
).reset_index()
bldg_totals['AVG_AREA_PER_FLOOR'] = bldg_totals['TOTAL_AREA'] / bldg_totals['FLOORS']

# Attach building display info (no ZIP/CITY per requirement for subtotals)
bldg_totals = bldg_totals.merge(
    rooms_fac[['BUILDING_KEY','BUILDING_NAME_OUT','ACCESS_LEVEL_OUT']].drop_duplicates(subset=['BUILDING_KEY']),
    on='BUILDING_KEY', how='left'
)

# 9) Grand total across all buildings (no ZIP/CITY)
grand = pd.DataFrame({
    'BUILDING_KEY': ['ALL BUILDINGS'],
    'FLOOR_KEY': [pd.NA],
    'FLOOR': [pd.NA],
    'ROOMS_COUNT': [int(floor_group['ROOMS_COUNT'].sum())],
    'TOTAL_AREA': [floor_group['TOTAL_AREA'].sum()],
    'AVG_AREA_PER_FLOOR': [bldg_totals['AVG_AREA_PER_FLOOR'].mean()],
    'BUILDING_NAME_OUT': ['Grand Total'],
    'ACCESS_LEVEL_OUT': [pd.NA],
    'ZIP': [pd.NA],
    'CITY': [pd.NA],
    'ROW_TYPE': ['GRAND_TOTAL']
})

# 10) Shape floor-level rows for output
floor_out = floor_enriched.copy()
floor_out['AVG_AREA_PER_FLOOR'] = pd.NA  # only for building/grand rows per requirement
floor_out['ROW_TYPE'] = 'FLOOR'

# 11) Shape building subtotal rows for output
bldg_out = bldg_totals.copy()
bldg_out['FLOOR_KEY'] = pd.NA
bldg_out['FLOOR'] = pd.NA
bldg_out['ZIP'] = pd.NA
bldg_out['CITY'] = pd.NA
bldg_out['ROW_TYPE'] = 'BUILDING_TOTAL'

# 12) Formatting: round to integers and add commas
def fmt_int(x):
    try:
        xi = int(round(float(x)))
        return f"{xi:,}"
    except Exception:
        return ''

for df in [floor_out, bldg_out, grand]:
    df['ROOMS_COUNT'] = df['ROOMS_COUNT'].apply(fmt_int)
    df['TOTAL_AREA'] = df['TOTAL_AREA'].apply(fmt_int)
    if 'AVG_AREA_PER_FLOOR' in df.columns:
        df['AVG_AREA_PER_FLOOR'] = df['AVG_AREA_PER_FLOOR'].apply(lambda v: fmt_int(v) if pd.notna(v) else '')

# 13) Choose columns and concatenate in desired order
cols = ['BUILDING_KEY','FLOOR_KEY','FLOOR','ROOMS_COUNT','TOTAL_AREA','AVG_AREA_PER_FLOOR','BUILDING_NAME_OUT','ACCESS_LEVEL_OUT','ZIP','CITY','ROW_TYPE']
result = pd.concat([
    floor_out[cols],
    bldg_out[cols],
    grand[cols]
], ignore_index=True)

# 14) Sort: by building key, then floors; keep grand total at end
result['sort_bldg'] = result['BUILDING_KEY'].astype(str)
result['sort_floor'] = result['FLOOR'].astype(str)
result['row_rank'] = result['ROW_TYPE'].map({'FLOOR':0,'BUILDING_TOTAL':1,'GRAND_TOTAL':2})
result = result.sort_values(by=['row_rank','sort_bldg','sort_floor']).drop(columns=['sort_bldg','sort_floor','row_rank'])

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
