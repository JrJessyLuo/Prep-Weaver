import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ROOM", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() == 'nan':
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() == 'nan':
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ROOM"] = table_1["ROOM"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ORGANIZATION_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s == "" or s.lower() == "nan":
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s == "" or s.lower() == "nan":
            return None
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
    # CastType(table_name="table_1", column="FISCAL_PERIOD", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FISCAL_PERIOD'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FISCAL_PERIOD']
    if _dtype == "datetime64":
        table_1['FISCAL_PERIOD'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FISCAL_PERIOD'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FISCAL_PERIOD'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FISCAL_PERIOD'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'ORGANIZATION_NAME', 'FISCAL_PERIOD', 'FCLT_ROOM_KEY', 'ROOM', 'BUILDING_ROOM'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'ORGANIZATION_NAME', 'FISCAL_PERIOD', 'FCLT_ROOM_KEY', 'ROOM', 'BUILDING_ROOM'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'ORGANIZATION_NAME', 'FISCAL_PERIOD', 'FCLT_ROOM_KEY', 'ROOM', 'BUILDING_ROOM'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_BUILDING_KEY', 'ORGANIZATION_NAME', 'FISCAL_PERIOD', 'FCLT_ROOM_KEY', 'ROOM', 'BUILDING_ROOM'], how='any').reset_index(drop=True)

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
    # MissingValueImputation(table_name="table_1", column_name="BUILDING_NAME_LONG", mode="mode")
    # MissingValueImputation
    table_1["BUILDING_NAME_LONG"] = table_1["BUILDING_NAME_LONG"].fillna(table_1["BUILDING_NAME_LONG"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if pd.isna(s):
    #         return s
    #     s = str(s).strip()
    #     if s.upper() in {"(NULL)", "NULL", "NAN", ""}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if pd.isna(s):
            return s
        s = str(s).strip()
        if s.upper() in {"(NULL)", "NULL", "NAN", ""}:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME_LONG", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if pd.isna(s):
    #         return s
    #     s = str(s).strip()
    #     if s.upper() in {"(NULL)", "NULL", "NAN", ""}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if pd.isna(s):
            return s
        s = str(s).strip()
        if s.upper() in {"(NULL)", "NULL", "NAN", ""}:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME_LONG"] = table_1["BUILDING_NAME_LONG"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='last').reset_index(drop=True)

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
    # StandardizeDatetime(table_name="table_1", column_name="WAREHOUSE_LOAD_DATE", date_format="%d-%b-%y")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['WAREHOUSE_LOAD_DATE'] = table_1['WAREHOUSE_LOAD_DATE'].apply(_sd_parse)
    if '%d-%b-%y':
        table_1['WAREHOUSE_LOAD_DATE'] = table_1['WAREHOUSE_LOAD_DATE'].dt.strftime('%d-%b-%y')

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
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_8'])
prepared_rooms_by_org = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_building_addresses = prepared_table_3

# Assume the three prepared tables exist: prepared_rooms_by_org, prepared_buildings, prepared_building_addresses
# 1) Identify rows for the History department; allow common variants
hist_mask = prepared_rooms_by_org['ORGANIZATION_NAME'].str.contains(r'\bHISTORY\b|\bHIST\b', case=False, na=False)
hist_rooms = prepared_rooms_by_org.loc[hist_mask].copy()

# 2) Get the most recent fiscal period per building to represent current occupancy
# If FISCAL_PERIOD is numeric-like string YYYYMM, coerce to int for ordering
fp = pd.to_numeric(hist_rooms['FISCAL_PERIOD'], errors='coerce')
hist_rooms = hist_rooms.assign(_FP=fp)
latest_by_bldg = hist_rooms.sort_values('_FP').groupby('FCLT_BUILDING_KEY', as_index=False).tail(1)

# 3) Join to buildings (optional metadata) and addresses
hist_with_bldg = latest_by_bldg.merge(prepared_buildings, on='FCLT_BUILDING_KEY', how='left')

# Prefer STREET purpose for physical street address; if multiple, pick STREET else fallback to MAIL or E911_1
addr_pref_order = ['STREET', 'E911_1', 'MAIL']
# Rank addresses by preference within each building
addr = prepared_building_addresses.copy()
addr['_addr_rank'] = addr['ADDRESS_PURPOSE'].apply(lambda x: addr_pref_order.index(x) if isinstance(x, str) and x in addr_pref_order else len(addr_pref_order))
addr_best = addr.sort_values(['FCLT_BUILDING_KEY', '_addr_rank']).groupby('FCLT_BUILDING_KEY', as_index=False).first()

hist_with_addr = hist_with_bldg.merge(addr_best.drop(columns=['_addr_rank']), on='FCLT_BUILDING_KEY', how='left')

# 4) Build street address string
parts = [
    hist_with_addr['STREET_NUMBER'].fillna('').astype(str).str.strip(),
    hist_with_addr['STREET_NUMBER_SUFFIX'].fillna('').astype(str).str.strip(),
    hist_with_addr['PRE_DIRECTIONAL'].fillna('').astype(str).str.strip(),
    hist_with_addr['STREET_NAME'].fillna('').astype(str).str.strip(),
    hist_with_addr['STREET_SUFFIX'].fillna('').astype(str).str.strip(),
    hist_with_addr['POST_DIRECTIONAL'].fillna('').astype(str).str.strip(),
]
# Join non-empty parts with spaces and collapse multiple spaces
street = (
    pd.Series([' '.join([p for p in row if p and p.lower() != "nan"]).strip() for row in zip(*parts)])
      .str.replace(r'\s+', ' ', regex=True)
)

result = hist_with_addr.assign(
    building_key=hist_with_addr['FCLT_BUILDING_KEY'],
    street_address=street,
    city=hist_with_addr['CITY'],
    state=hist_with_addr['STATE'],
    postal_code=hist_with_addr['POSTAL_CODE']
)[['building_key', 'street_address', 'city', 'state', 'postal_code']].drop_duplicates()

# 'result' holds the current building key and address info for the History department
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
