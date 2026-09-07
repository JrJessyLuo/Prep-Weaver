import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BLDG_GROSS_SQUARE_FOOTAGE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BLDG_GROSS_SQUARE_FOOTAGE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BLDG_GROSS_SQUARE_FOOTAGE']
    if _dtype == "datetime64":
        table_1['BLDG_GROSS_SQUARE_FOOTAGE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BLDG_GROSS_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BLDG_GROSS_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BLDG_GROSS_SQUARE_FOOTAGE'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BLDG_ASSIGNABLE_SQUARE_FOOTAGE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE']
    if _dtype == "datetime64":
        table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = _series.astype(str)

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
    # Deduplicate(table_name="table_1", subset=['BUILDING_NUMBER'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_NUMBER'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_HEIGHT'])
    # SelectCol
    _cols = [c for c in ['BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_HEIGHT'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # Trim and collapse internal whitespace
    #     return re.sub(r'\s+', ' ', str(s).strip())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # Trim and collapse internal whitespace
        return re.sub(r'\s+', ' ', str(s).strip())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NUMBER"] = table_1["BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # Trim and collapse internal whitespace for consistent name reference
    #     return re.sub(r'\s+', ' ', str(s).strip())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # Trim and collapse internal whitespace for consistent name reference
        return re.sub(r'\s+', ' ', str(s).strip())
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
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY', 'LEVEL_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY', 'LEVEL_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY', 'LEVEL_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY', 'LEVEL_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'LEVEL_ID'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'LEVEL_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
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
    # GroupBy(table_name="table_1", by=['BUILDING_KEY'], agg=[{'column': 'ROOM_SQUARE_FOOTAGE', 'agg_func': 'sum'}])
    # GroupBy
    table_1 = table_1.groupby(['BUILDING_KEY'], as_index=False).agg({'ROOM_SQUARE_FOOTAGE': 'sum'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ROOM_SQUARE_FOOTAGE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ROOM_SQUARE_FOOTAGE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ROOM_SQUARE_FOOTAGE']
    if _dtype == "datetime64":
        table_1['ROOM_SQUARE_FOOTAGE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ROOM_SQUARE_FOOTAGE'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['BUILDING_KEY'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['BUILDING_KEY'], ascending=[True])

    # ---------------- Step 4 ----------------
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
prepared_building_directory = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_building_characteristics = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_floors = prepared_table_3
prepared_table_4 = _prep_4(tables['table_9'])
prepared_rooms = prepared_table_4

# Assume the following DataFrames exist from the per-table targets:
# prepared_building_directory, prepared_building_characteristics, prepared_floors, prepared_rooms

# 1) Merge directory with characteristics on BUILDING_NUMBER to get height
dir_char = prepared_building_directory.merge(
    prepared_building_characteristics[["BUILDING_NUMBER","BUILDING_HEIGHT"]],
    on="BUILDING_NUMBER",
    how="left"
)

# 2) Aggregate floors to get smallest and largest level per building
floors_agg = prepared_floors.groupby("BUILDING_KEY", as_index=False).agg(
    SMALLEST_LEVEL=("LEVEL_ID", "min"),
    LARGEST_LEVEL=("LEVEL_ID", "max")
)

# 3) Aggregate rooms to get total room area per building
rooms_agg = prepared_rooms.groupby("BUILDING_KEY", as_index=False).agg(
    TOTAL_ROOM_AREA=("ROOM_SQUARE_FOOTAGE", "sum")
)

# 4) Combine all by BUILDING_KEY
result = dir_char.merge(floors_agg, on="BUILDING_KEY", how="left") \
                 .merge(rooms_agg, on="BUILDING_KEY", how="left")

# 5) Select and rename columns for the final answer
final_columns = [
    "BUILDING_KEY",
    "BUILDING_NAME",
    "BUILDING_HEIGHT",
    "BUILDING_STREET_ADDRESS",
    # City, State, Postal Code are not present in provided schemas; keep placeholders if needed
    # If available in extended data, they should be included in prepared_building_directory
    "BLDG_GROSS_SQUARE_FOOTAGE",
    "BLDG_ASSIGNABLE_SQUARE_FOOTAGE",
    "SMALLEST_LEVEL",
    "LARGEST_LEVEL",
    "TOTAL_ROOM_AREA"
]

# Ensure presence of the columns even if some are missing due to upstream data
for c in final_columns:
    if c not in result.columns:
        result[c] = pd.NA

target = result[final_columns]

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
