import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ORGANIZATION_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ORGANIZATION_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ORGANIZATION_ID']
    if _dtype == "datetime64":
        table_1['ORGANIZATION_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ORGANIZATION_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ORGANIZATION_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ORGANIZATION_ID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="organization_key", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['organization_key'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['organization_key']
    if _dtype == "datetime64":
        table_1['organization_key'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['organization_key'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['organization_key'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['organization_key'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ORGANIZATION_NUMBER", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ORGANIZATION_NUMBER'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ORGANIZATION_NUMBER']
    if _dtype == "datetime64":
        table_1['ORGANIZATION_NUMBER'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ORGANIZATION_NUMBER'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ORGANIZATION_NUMBER'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ORGANIZATION_NUMBER'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ORGANIZATION_LEVEL", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ORGANIZATION_LEVEL'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ORGANIZATION_LEVEL']
    if _dtype == "datetime64":
        table_1['ORGANIZATION_LEVEL'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ORGANIZATION_LEVEL'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ORGANIZATION_LEVEL'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ORGANIZATION_LEVEL'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ASSIGNABLE", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ASSIGNABLE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ASSIGNABLE']
    if _dtype == "datetime64":
        table_1['ASSIGNABLE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ASSIGNABLE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ASSIGNABLE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ASSIGNABLE'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ORGANIZATION_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # strip matching leading/trailing quotes
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # strip matching leading/trailing quotes
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
    table_1["ORGANIZATION_NAME"] = table_1["ORGANIZATION_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['organization_key'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['organization_key'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['organization_key', 'ORGANIZATION_ID', 'ORGANIZATION_NUMBER', 'ORGANIZATION_LEVEL', 'ORGANIZATION_NAME', 'ASSIGNABLE'])
    # SelectCol
    _cols = [c for c in ['organization_key', 'ORGANIZATION_ID', 'ORGANIZATION_NUMBER', 'ORGANIZATION_LEVEL', 'ORGANIZATION_NAME', 'ASSIGNABLE'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ORGANIZATION_KEY', 'AREA'])
    # SelectCol
    _cols = [c for c in ['ORGANIZATION_KEY', 'AREA'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ORGANIZATION_KEY", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ORGANIZATION_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ORGANIZATION_KEY']
    if _dtype == "datetime64":
        table_1['ORGANIZATION_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ORGANIZATION_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ORGANIZATION_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ORGANIZATION_KEY'] = _series.astype(str)

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
    # DropNulls(table_name="table_1", subset=['ORGANIZATION_KEY', 'AREA'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ORGANIZATION_KEY', 'AREA'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     # keep only valid positive areas for aggregation
    #     return row[\"AREA\"] is not None and row[\"AREA\"] > 0
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # keep only valid positive areas for aggregation
        return row[\"AREA\"] is not None and row[\"AREA\"] > 0
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_orgs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_rooms = prepared_table_2

# prepared_orgs and prepared_rooms are the synthesized tables per the targets above

# Ensure numeric types for join and calculations
prepared_orgs['organization_key'] = pd.to_numeric(prepared_orgs['organization_key'], errors='coerce')
prepared_orgs['ORGANIZATION_ID'] = pd.to_numeric(prepared_orgs['ORGANIZATION_ID'], errors='coerce')
prepared_orgs['ORGANIZATION_NUMBER'] = pd.to_numeric(prepared_orgs['ORGANIZATION_NUMBER'], errors='coerce')
prepared_orgs['ORGANIZATION_LEVEL'] = pd.to_numeric(prepared_orgs['ORGANIZATION_LEVEL'], errors='coerce')
prepared_orgs['ASSIGNABLE'] = pd.to_numeric(prepared_orgs['ASSIGNABLE'], errors='coerce')

prepared_rooms['ORGANIZATION_KEY'] = pd.to_numeric(prepared_rooms['ORGANIZATION_KEY'], errors='coerce')
prepared_rooms['AREA'] = pd.to_numeric(prepared_rooms['AREA'], errors='coerce')

# Aggregate room metrics per organization
room_agg = prepared_rooms.groupby('ORGANIZATION_KEY', dropna=True).agg(
    total_area=('AREA', 'sum'),
    room_count=('AREA', 'count'),
    avg_area=('AREA', 'mean')
).reset_index().rename(columns={'ORGANIZATION_KEY': 'organization_key'})

# Join orgs with room aggregates (left join to keep orgs with zero rooms)
merged = prepared_orgs.merge(room_agg, on='organization_key', how='left')

# Fill NaNs for orgs with no rooms
merged['total_area'] = merged['total_area'].fillna(0)
merged['room_count'] = merged['room_count'].fillna(0)
merged['avg_area'] = merged.apply(lambda r: (r['total_area'] / r['room_count']) if r['room_count'] > 0 else 0, axis=1)

# Exclude Cambridge-MIT Institute by name
mask_cmi = merged['ORGANIZATION_NAME'].str.strip().str.casefold() == 'cambridge-mit institute'
result = merged.loc[~mask_cmi].copy()

# Format name with leading spaces based on level (levels 2..6 -> 1..5 spaces)
def fmt_name(row):
    lvl = int(row['ORGANIZATION_LEVEL']) if pd.notna(row['ORGANIZATION_LEVEL']) else None
    spaces = max(0, min(6, lvl) - 1) if lvl is not None else 0
    return (' ' * spaces) + str(row['ORGANIZATION_NAME'])

result['Formatted Name'] = result.apply(fmt_name, axis=1)

# Assignable label
result['Assignable Label'] = result['ASSIGNABLE'].apply(lambda x: 'ASSIGNABLE' if pd.notna(x) and int(x) == 1 else 'NON-ASSIGNABLE')

# Round and format numbers with commas
def fmt_int(x):
    try:
        return f"{int(round(float(x))):,}"
    except Exception:
        return ''

result['Total Area'] = result['total_area'].apply(fmt_int)
result['Number of Rooms'] = result['room_count'].apply(fmt_int)
result['Average Room Area'] = result['avg_area'].apply(fmt_int)

# Select and rename output columns
output = result[[
    'ORGANIZATION_ID',
    'ORGANIZATION_NUMBER',
    'ORGANIZATION_LEVEL',
    'Formatted Name',
    'Assignable Label',
    'Total Area',
    'Number of Rooms',
    'Average Room Area'
]].rename(columns={
    'ORGANIZATION_ID': 'Organization ID',
    'ORGANIZATION_NUMBER': 'Organization Number',
    'ORGANIZATION_LEVEL': 'Level'
})

# Final answer dataframe
target = output

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
