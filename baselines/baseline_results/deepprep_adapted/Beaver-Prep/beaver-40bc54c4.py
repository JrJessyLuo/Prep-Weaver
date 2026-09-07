import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['SPACE_UNIT_KEY', 'SPACE_USAGE_KEY', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['SPACE_UNIT_KEY', 'SPACE_USAGE_KEY', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'FLOOR_KEY', 'BUILDING_COMPONENT', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE', 'ROOM_COUNTER'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'FLOOR_KEY', 'BUILDING_COMPONENT', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER', 'ROOM_SQUARE_FOOTAGE', 'ROOM_COUNTER'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # DropColumn(table_name="table_1", drop_columns=['BUILDING_STREET_ADDRESS', 'BUILDING_MAILING_ADDRESS', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['BUILDING_STREET_ADDRESS', 'BUILDING_MAILING_ADDRESS', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BUILDING_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BUILDING_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BUILDING_NAME']
    if _dtype == "datetime64":
        table_1['BUILDING_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BUILDING_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BUILDING_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BUILDING_NAME'] = _series.astype(str)

    # ---------------- Step 5 ----------------
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

    # ---------------- Step 6 ----------------
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

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BUILDING_COUNTER", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BUILDING_COUNTER'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BUILDING_COUNTER']
    if _dtype == "datetime64":
        table_1['BUILDING_COUNTER'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BUILDING_COUNTER'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BUILDING_COUNTER'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BUILDING_COUNTER'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'BUILDING_COUNTER'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'BUILDING_COUNTER'] if c in table_1.columns]
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
def _prep_3(table_1):
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # GroupBy(table_name="table_1", by=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME'], agg=[{'column': 'NUM_OF_ROOMS', 'agg_func': 'sum'}])
    # GroupBy
    table_1 = table_1.groupby(['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME'], as_index=False).agg({'NUM_OF_ROOMS': 'sum'})

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'NUM_OF_ROOMS'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'NUM_OF_ROOMS'] if c in table_1.columns]
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'FCLT_FLOOR_KEY', 'FCLT_ORGANIZATION_KEY', 'FCLT_ROOM_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'FCLT_FLOOR_KEY', 'FCLT_ORGANIZATION_KEY', 'FCLT_ROOM_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'FCLT_FLOOR_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_ROOM_KEY'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'FCLT_FLOOR_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_ROOM_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'FCLT_FLOOR_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_ROOM_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'FCLT_FLOOR_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_ROOM_KEY'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_3'])
rooms_by_component = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
building_directory = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
building_summary = prepared_table_3
prepared_table_4 = _prep_4(tables['table_5'])
room_orgs = prepared_table_4

# Assume prepared DataFrames: rooms_by_component, building_directory, building_summary, room_orgs

# 1) Enrich building_directory with total rooms (building level)
bldg_dir_enriched = building_directory.merge(
    building_summary[['BUILDING_NUMBER', 'NUM_OF_ROOMS']],
    on='BUILDING_NUMBER', how='left'
)

# 2) Join room/component facts to building directory on BUILDING_KEY to get building name
rooms_enriched = rooms_by_component.merge(
    bldg_dir_enriched[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','NUM_OF_ROOMS']],
    on='BUILDING_KEY', how='left'
)

# 3) Link room_orgs to rooms via BUILDING_ROOM to attribute organizations to components
room_orgs_linked = room_orgs.merge(
    rooms_enriched[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_COMPONENT','BUILDING_ROOM']],
    on='BUILDING_ROOM', how='inner'
)

# 4) Compute per-building-component metrics
# - Square footage for all rooms: sum ROOM_SQUARE_FOOTAGE per component
# - Total number of floors: count distinct FLOOR_KEY per component
# - Total number of rooms: count distinct BUILDING_ROOM (or sum ROOM_COUNTER if unique)
# - Total number of facility organizations: count distinct FCLT_ORGANIZATION_KEY per component
# Note: Supervisors/supervisees not present in selected tables; will return nulls

# Ensure numeric
rooms_enriched['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(rooms_enriched['ROOM_SQUARE_FOOTAGE'], errors='coerce')

component_agg = (
    rooms_enriched.groupby(['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_COMPONENT'])
    .agg(
        total_room_sqft = ('ROOM_SQUARE_FOOTAGE','sum'),
        total_floors = ('FLOOR_KEY', pd.Series.nunique),
        total_rooms = ('BUILDING_ROOM', pd.Series.nunique)
    )
    .reset_index()
)

org_agg = (
    room_orgs_linked.groupby(['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_COMPONENT'])
    .agg(total_facility_organizations = ('FCLT_ORGANIZATION_KEY', pd.Series.nunique))
    .reset_index()
)

result = component_agg.merge(org_agg,
                             on=['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_COMPONENT'],
                             how='left')

# Supervisors and supervisees placeholders (no data available in provided tables)
result['total_supervisors'] = pd.NA
result['total_supervisees'] = pd.NA

# Select and rename columns to match the question
answer = result[[
    'BUILDING_COMPONENT',
    'BUILDING_NAME',
    'total_room_sqft',
    'total_floors',
    'total_rooms',
    'total_facility_organizations',
    'total_supervisors',
    'total_supervisees'
]].sort_values(['BUILDING_NAME','BUILDING_COMPONENT'])

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
