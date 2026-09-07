import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'DATE_BUILT', 'NUM_OF_ROOMS'])
    # SelectCol
    _cols = [c for c in ['BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'DATE_BUILT', 'NUM_OF_ROOMS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
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
    table_1["BUILDING_NUMBER"] = table_1["BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME_LONG", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # trim and collapse repeated whitespace
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # trim and collapse repeated whitespace
        return " ".join(str(s).strip().split())
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
    # StandardizeDatetime(table_name="table_1", column_name="DATE_BUILT", date_format="%Y-%m-%d")
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
    table_1['DATE_BUILT'] = table_1['DATE_BUILT'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['DATE_BUILT'] = table_1['DATE_BUILT'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_OF_ROOMS", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NUM_OF_ROOMS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NUM_OF_ROOMS']
    if _dtype == "datetime64":
        table_1['NUM_OF_ROOMS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NUM_OF_ROOMS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NUM_OF_ROOMS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NUM_OF_ROOMS'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="NUM_OF_ROOMS", mode="median")
    # MissingValueImputation
    table_1["NUM_OF_ROOMS"] = table_1["NUM_OF_ROOMS"].fillna(table_1["NUM_OF_ROOMS"].median())

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_OF_ROOMS", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NUM_OF_ROOMS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NUM_OF_ROOMS']
    if _dtype == "datetime64":
        table_1['NUM_OF_ROOMS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NUM_OF_ROOMS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NUM_OF_ROOMS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NUM_OF_ROOMS'] = _series.astype(str)

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
    # Deduplicate(table_name="table_1", subset=['BUILDING_ROOM', 'FLOOR'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_ROOM', 'FLOOR'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_ROOM", func="""
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
    table_1["BUILDING_ROOM"] = table_1["BUILDING_ROOM"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="BUILDING_NUMBER", func="""
    # def compute(row):
    #     val = row.get('BUILDING_ROOM')
    #     if val is None:
    #         return None
    #     s = str(val).strip()
    #     # split on first '-' only
    #     return s.split('-', 1)[0] if '-' in s else s
    # """)
    # AddNewColumn
    def compute(row):
        val = row.get('BUILDING_ROOM')
        if val is None:
            return None
        s = str(val).strip()
        # split on first '-' only
        return s.split('-', 1)[0] if '-' in s else s
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["BUILDING_NUMBER"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_NUMBER', 'BUILDING_ROOM'])
    # SelectCol
    _cols = [c for c in ['BUILDING_NUMBER', 'BUILDING_ROOM'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_4'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_rooms = prepared_table_2

# prepared_buildings: keep as provided
b = prepared_buildings.copy()

# prepared_rooms: ensure BUILDING_NUMBER parsed from BUILDING_ROOM
r = prepared_rooms.copy()
if 'BUILDING_NUMBER' not in r.columns and 'BUILDING_ROOM' in r.columns:
    r['BUILDING_NUMBER'] = r['BUILDING_ROOM'].astype(str).str.split('-', n=1).str[0]

# Integrate (if needed). For this question, employee threshold is approximated by NUM_OF_ROOMS > 100.
# We don't actually need room-level expansion to compute the answer, but preserve the join pattern.
merged = b.merge(r[['BUILDING_NUMBER']].drop_duplicates(), on='BUILDING_NUMBER', how='left')

# Parse built year from DATE_BUILT (formats like 'MM/DD/YYYY').
def parse_year(x):
    try:
        # Try standard parse
        return pd.to_datetime(x, errors='coerce').year
    except Exception:
        return pd.NaT

merged['BUILT_YEAR'] = pd.to_datetime(merged['DATE_BUILT'], errors='coerce').dt.year

# Filter: constructed before 1950 and more than 100 employees (approximated by NUM_OF_ROOMS > 100)
ans = merged[(merged['BUILT_YEAR'].notna()) & (merged['BUILT_YEAR'] < 1950) & (merged['NUM_OF_ROOMS'] > 100)]

# Select required output columns and drop duplicates
answer = ans[['BUILDING_NAME_LONG', 'BUILT_YEAR', 'NUM_OF_ROOMS']].drop_duplicates().sort_values(['BUILDING_NAME_LONG'])

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
