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

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ROOM", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ROOM'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ROOM']
    if _dtype == "datetime64":
        table_1['ROOM'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ROOM'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ROOM'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ROOM'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SPACE_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SPACE_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SPACE_ID']
    if _dtype == "datetime64":
        table_1['SPACE_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SPACE_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SPACE_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SPACE_ID'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ORGANIZATION_KEY", dtype="string")
    # CastType
    _dtype = 'string'
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

    # ---------------- Step 8 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ORGANIZATION_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ORGANIZATION_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ORGANIZATION_NAME']
    if _dtype == "datetime64":
        table_1['ORGANIZATION_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ORGANIZATION_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ORGANIZATION_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ORGANIZATION_NAME'] = _series.astype(str)

    # ---------------- Step 9 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="DEPT_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['DEPT_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['DEPT_CODE']
    if _dtype == "datetime64":
        table_1['DEPT_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['DEPT_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['DEPT_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['DEPT_CODE'] = _series.astype(str)

    # ---------------- Step 10 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_rooms", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Fill ROOM_FULL_NAME when missing with a stable fallback identifier
    #     if 'ROOM_FULL_NAME' in df.columns:
    #         df['ROOM_FULL_NAME'] = df['ROOM_FULL_NAME'].where(
    #             df['ROOM_FULL_NAME'].notna(),
    #             df['fac_room_key']
    #         )
    #     else:
    #         df['ROOM_FULL_NAME'] = df['fac_room_key']
    # 
    #     # Keep only required columns in required order
    #     out = df[[
    #         "fac_room_key",
    #         "BUILDING_KEY",
    #         "FLOOR",
    #         "FLOOR_KEY",
    #         "ROOM",
    #         "SPACE_ID",
    #         "ROOM_FULL_NAME",
    #         "ORGANIZATION_KEY",
    #         "ORGANIZATION_NAME",
    #         "DEPT_CODE",
    #         "AREA"
    #     ]].copy()
    # 
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Fill ROOM_FULL_NAME when missing with a stable fallback identifier
        if 'ROOM_FULL_NAME' in df.columns:
            df['ROOM_FULL_NAME'] = df['ROOM_FULL_NAME'].where(
                df['ROOM_FULL_NAME'].notna(),
                df['fac_room_key']
            )
        else:
            df['ROOM_FULL_NAME'] = df['fac_room_key']

        # Keep only required columns in required order
        out = df[[
            "fac_room_key",
            "BUILDING_KEY",
            "FLOOR",
            "FLOOR_KEY",
            "ROOM",
            "SPACE_ID",
            "ROOM_FULL_NAME",
            "ORGANIZATION_KEY",
            "ORGANIZATION_NAME",
            "DEPT_CODE",
            "AREA"
        ]].copy()

        return out
    prepared_rooms = process_tables(table_1)

    # ---------------- Step 11 ----------------
    # Original operator:
    # Terminate(result=['prepared_rooms'])
    # Terminate
    result = {'prepared_rooms': prepared_rooms}
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
    # Sort(table_name="table_1", by=['BUILDING_NUMBER'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['BUILDING_NUMBER'], ascending=[True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ASSIGNABLE_AREA'])
    # SelectCol
    _cols = [c for c in ['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ASSIGNABLE_AREA'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # MissingValueImputation(table_name="table_1", column_name="ASSIGNABLE_AREA", mode="median")
    # MissingValueImputation
    table_1["ASSIGNABLE_AREA"] = table_1["ASSIGNABLE_AREA"].fillna(table_1["ASSIGNABLE_AREA"].median())

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FAC_BUILDING_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FAC_BUILDING_KEY'], keep='last').reset_index(drop=True)

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
    # Sort(table_name="table_1", by=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM_NUMBER'], ascending=[True, True, True])
    # Sort
    table_1 = table_1.sort_values(by=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM_NUMBER'], ascending=[True, True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'FLOOR_KEY', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE'], how='any').reset_index(drop=True)

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
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_floors = prepared_table_3

# Assume prepared_* DataFrames exist as specified.
rooms = prepared_rooms.copy()
bldgs = prepared_buildings.copy()
floors = prepared_floors.copy()

# Coerce numeric fields
rooms['AREA'] = pd.to_numeric(rooms['AREA'], errors='coerce')
bldgs['ASSIGNABLE_AREA'] = pd.to_numeric(bldgs['ASSIGNABLE_AREA'], errors='coerce')

# Join buildings to get building names and assignable area
rooms_b = rooms.merge(
    bldgs.rename(columns={'FAC_BUILDING_KEY':'BUILDING_KEY'}),
    on='BUILDING_KEY', how='left'
)

# Compute floor total area per building-floor using floors table
# First, ensure join keys align for per-room mapping (ROOM matches ROOM_NUMBER)
floors_subset = floors[['BUILDING_KEY','FLOOR_KEY','ROOM_NUMBER','ROOM_SQUARE_FOOTAGE']].copy()
floors_subset['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(floors_subset['ROOM_SQUARE_FOOTAGE'], errors='coerce')

# Floor totals
floor_totals = floors_subset.groupby(['BUILDING_KEY','FLOOR_KEY'], as_index=False)['ROOM_SQUARE_FOOTAGE'].sum()
floor_totals = floor_totals.rename(columns={'ROOM_SQUARE_FOOTAGE':'FLOOR_TOTAL_AREA'})

# Attach floor totals to each room via BUILDING_KEY and FLOOR_KEY
rooms_b = rooms_b.merge(floor_totals, on=['BUILDING_KEY','FLOOR_KEY'], how='left')

# Percentages: room over floor total and over building assignable area
rooms_b['pct_room_over_floor'] = rooms_b['AREA'] / rooms_b['FLOOR_TOTAL_AREA']
rooms_b['pct_room_over_building'] = rooms_b['AREA'] / rooms_b['ASSIGNABLE_AREA']

# Select requested output columns
target = rooms_b[[
    'ROOM_FULL_NAME',            # full room name
    'BUILDING_NAME',             # building name (short)
    'BUILDING_NAME_LONG',        # building name (long)
    'FLOOR',                     # floor number
    'ORGANIZATION_NAME',         # occupying organization name
    'DEPT_CODE',                 # department code (name not available in provided tables)
    'AREA',                      # room area (evidence for percentages)
    'FLOOR_TOTAL_AREA',          # floor total area (evidence)
    'ASSIGNABLE_AREA',           # building assignable area (evidence)
    'pct_room_over_floor',
    'pct_room_over_building'
]].copy()

# Optionally format percentages
# target['pct_room_over_floor'] = (target['pct_room_over_floor']*100).round(2)
# target['pct_room_over_building'] = (target['pct_room_over_building']*100).round(2)

result = target

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
