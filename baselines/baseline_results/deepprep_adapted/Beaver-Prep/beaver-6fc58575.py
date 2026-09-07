import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="AREA", mode="median")
    # MissingValueImputation
    table_1["AREA"] = table_1["AREA"].fillna(table_1["AREA"].median())

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_ROOM_KEY', 'SPACE_ID', 'FCLT_BUILDING_KEY', 'FCLT_FLOOR_KEY', 'FLOOR', 'ROOM', 'ROOM_FULL_NAME', 'ORGANIZATION_NAME', 'DEPT_CODE', 'AREA'])
    # SelectCol
    _cols = [c for c in ['FCLT_ROOM_KEY', 'SPACE_ID', 'FCLT_BUILDING_KEY', 'FCLT_FLOOR_KEY', 'FLOOR', 'ROOM', 'ROOM_FULL_NAME', 'ORGANIZATION_NAME', 'DEPT_CODE', 'AREA'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME_LONG", func="""
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
    table_1["BUILDING_NAME_LONG"] = table_1["BUILDING_NAME_LONG"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s.lower() not in ["nan", "(null)", "none", ""] else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s.lower() not in ["nan", "(null)", "none", ""] else None
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ASSIGNABLE_AREA'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ASSIGNABLE_AREA'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'ASSIGNABLE_AREA'])
    # SelectCol
    _cols = [c for c in ['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'ASSIGNABLE_AREA'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'ASSIGNABLE_AREA'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'ASSIGNABLE_AREA'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_FLOOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_FLOOR_KEY'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_10'])
prepared_floors = prepared_table_3

# Assume prepared_rooms, prepared_buildings, prepared_floors are pre-synthesized per targets above

# Ensure numeric types for area fields
for col in ["AREA"]:
    prepared_rooms[col] = pd.to_numeric(prepared_rooms[col], errors="coerce")
prepared_buildings["ASSIGNABLE_AREA"] = pd.to_numeric(prepared_buildings["ASSIGNABLE_AREA"], errors="coerce")
prepared_floors["ASSIGNABLE_AREA"] = pd.to_numeric(prepared_floors["ASSIGNABLE_AREA"], errors="coerce")

# Join rooms -> buildings
rb = prepared_rooms.merge(
    prepared_buildings[["FCLT_BUILDING_KEY", "BUILDING_NAME", "BUILDING_NAME_LONG", "ASSIGNABLE_AREA"]],
    on="FCLT_BUILDING_KEY",
    how="left",
    suffixes=("", "_BUILDING")
)

# Join rooms -> floors
rbf = rb.merge(
    prepared_floors[["FCLT_FLOOR_KEY", "ASSIGNABLE_AREA"]],
    on="FCLT_FLOOR_KEY",
    how="left",
    suffixes=("", "_FLOOR")
)

# Compute percentages
rbf["pct_of_floor"] = (rbf["AREA"] / rbf["ASSIGNABLE_AREA_FLOOR"]) * 100
rbf["pct_of_building"] = (rbf["AREA"] / rbf["ASSIGNABLE_AREA_BUILDING"]) * 100

# Prepare final fields
target = rbf[[
    "ROOM_FULL_NAME",
    "BUILDING_NAME",
    "BUILDING_NAME_LONG",
    "FLOOR",
    "ORGANIZATION_NAME",
    "DEPT_CODE",
    "AREA",
    "pct_of_floor",
    "pct_of_building",
    "SPACE_ID",
    "FCLT_BUILDING_KEY",
    "FCLT_FLOOR_KEY"
]].rename(columns={
    "FLOOR": "FLOOR_NUMBER",
    "BUILDING_NAME_LONG": "BUILDING_NAME_LONG_FORMAL"
})

# Note: Any sorting/filtering for presentation can be applied after 'target' is produced.

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
