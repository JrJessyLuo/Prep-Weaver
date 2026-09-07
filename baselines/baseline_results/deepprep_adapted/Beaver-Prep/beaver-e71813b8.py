import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'ROOM', 'ROOM_FULL_NAME', 'AREA', 'MAJOR_USE_DESC', 'ORGANIZATION_NAME', 'SPACE_ID', 'FLOOR'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'ROOM', 'ROOM_FULL_NAME', 'AREA', 'MAJOR_USE_DESC', 'ORGANIZATION_NAME', 'SPACE_ID', 'FLOOR'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # CodeGeneration(table_names=['table_1'], target_table="prepared_rooms", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Strip whitespace for stable grouping/labels (safe for non-strings)
    #     for c in ["BUILDING_KEY","ROOM","MAJOR_USE_DESC","ORGANIZATION_NAME","SPACE_ID","FLOOR","ROOM_FULL_NAME"]:
    #         if c in df.columns:
    #             df[c] = df[c].astype("string").str.strip()
    # 
    #     # Fill ROOM_FULL_NAME: existing -> SPACE_ID -> BUILDING_KEY-FLOOR-ROOM
    #     fallback = (
    #         df["BUILDING_KEY"].fillna("") + "-" +
    #         df["FLOOR"].fillna("") + "-" +
    #         df["ROOM"].fillna("")
    #     ).str.strip("-")
    # 
    #     df["ROOM_FULL_NAME"] = df["ROOM_FULL_NAME"].replace({"<NA>": pd.NA, "nan": pd.NA, "None": pd.NA})
    #     df["ROOM_FULL_NAME"] = df["ROOM_FULL_NAME"].fillna(df["SPACE_ID"])
    #     df["ROOM_FULL_NAME"] = df["ROOM_FULL_NAME"].fillna(fallback)
    # 
    #     # Keep exactly the target columns in the requested order
    #     out = df[["BUILDING_KEY","ROOM","ROOM_FULL_NAME","AREA","MAJOR_USE_DESC","ORGANIZATION_NAME","SPACE_ID","FLOOR"]].copy()
    # 
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Strip whitespace for stable grouping/labels (safe for non-strings)
        for c in ["BUILDING_KEY","ROOM","MAJOR_USE_DESC","ORGANIZATION_NAME","SPACE_ID","FLOOR","ROOM_FULL_NAME"]:
            if c in df.columns:
                df[c] = df[c].astype("string").str.strip()

        # Fill ROOM_FULL_NAME: existing -> SPACE_ID -> BUILDING_KEY-FLOOR-ROOM
        fallback = (
            df["BUILDING_KEY"].fillna("") + "-" +
            df["FLOOR"].fillna("") + "-" +
            df["ROOM"].fillna("")
        ).str.strip("-")

        df["ROOM_FULL_NAME"] = df["ROOM_FULL_NAME"].replace({"<NA>": pd.NA, "nan": pd.NA, "None": pd.NA})
        df["ROOM_FULL_NAME"] = df["ROOM_FULL_NAME"].fillna(df["SPACE_ID"])
        df["ROOM_FULL_NAME"] = df["ROOM_FULL_NAME"].fillna(fallback)

        # Keep exactly the target columns in the requested order
        out = df[["BUILDING_KEY","ROOM","ROOM_FULL_NAME","AREA","MAJOR_USE_DESC","ORGANIZATION_NAME","SPACE_ID","FLOOR"]].copy()

        return out
    prepared_rooms = process_tables(table_1)

    # ---------------- Step 4 ----------------
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row['BUILDING_NUMBER'] == '45'
    # """)
    # Filter
    def filter_func(row):
        return row['BUILDING_NUMBER'] == '45'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG'])
    # SelectCol
    _cols = [c for c in ['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_NUMBER'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_NUMBER'], keep='first').reset_index(drop=True)

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
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_buildings = prepared_table_2

# Assume prepared_rooms and prepared_buildings are provided per the target schemas
# 1) Identify building 45 and join to rooms
b45 = prepared_buildings[prepared_buildings['BUILDING_NUMBER'].astype(str).str.strip() == '45']
rooms_b45 = prepared_rooms.merge(b45[['FAC_BUILDING_KEY']], left_on='BUILDING_KEY', right_on='FAC_BUILDING_KEY', how='inner')

# 2) List all rooms with requested details
rooms_list = rooms_b45[['ROOM', 'ROOM_FULL_NAME', 'AREA', 'MAJOR_USE_DESC', 'ORGANIZATION_NAME']].copy()
# Ensure AREA is numeric for later aggregations
rooms_list['AREA'] = pd.to_numeric(rooms_list['AREA'], errors='coerce')

# 3) Count of rooms per major use
count_per_major_use = rooms_b45.groupby('MAJOR_USE_DESC', dropna=False)['ROOM'].nunique().reset_index(name='room_count')

# 4) Total area per organization
area_per_org = rooms_b45.assign(AREA=pd.to_numeric(rooms_b45['AREA'], errors='coerce')) \
    .groupby('ORGANIZATION_NAME', dropna=False)['AREA'].sum().reset_index(name='total_area')

# Package outputs
result = {
    'rooms': rooms_list.sort_values(['MAJOR_USE_DESC','ORGANIZATION_NAME','ROOM'], na_position='last').reset_index(drop=True),
    'rooms_per_major_use': count_per_major_use.sort_values('room_count', ascending=False).reset_index(drop=True),
    'total_area_per_organization': area_per_org.sort_values('total_area', ascending=False).reset_index(drop=True)
}

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
