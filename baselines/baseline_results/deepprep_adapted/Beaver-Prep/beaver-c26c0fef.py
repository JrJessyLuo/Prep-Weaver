import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="FORM_TYPE_DESC", mode="mode")
    # MissingValueImputation
    table_1["FORM_TYPE_DESC"] = table_1["FORM_TYPE_DESC"].fillna(table_1["FORM_TYPE_DESC"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SUBJECT_ENROLLMENT_NUMBER", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SUBJECT_ENROLLMENT_NUMBER'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SUBJECT_ENROLLMENT_NUMBER']
    if _dtype == "datetime64":
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SUBJECT_ENROLLMENT_NUMBER'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID', 'MEET_PLACE', 'FORM_TYPE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID', 'MEET_PLACE', 'FORM_TYPE'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'MEET_PLACE', 'FORM_TYPE', 'FORM_TYPE_DESC', 'SUBJECT_ENROLLMENT_NUMBER'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'MEET_PLACE', 'FORM_TYPE', 'FORM_TYPE_DESC', 'SUBJECT_ENROLLMENT_NUMBER'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="fac_room_key", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['fac_room_key'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['fac_room_key']
    if _dtype == "datetime64":
        table_1['fac_room_key'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['fac_room_key'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['fac_room_key'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['fac_room_key'] = _series.astype(str)

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['fac_room_key', 'ROOM', 'FLOOR', 'BUILDING_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['fac_room_key', 'ROOM', 'FLOOR', 'BUILDING_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['fac_room_key'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['fac_room_key'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['fac_room_key', 'ROOM', 'FLOOR', 'BUILDING_KEY'])
    # SelectCol
    _cols = [c for c in ['fac_room_key', 'ROOM', 'FLOOR', 'BUILDING_KEY'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_4'])
prepared_subject_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_8'])
prepared_rooms = prepared_table_2

# Assume prepared_subject_offerings and prepared_rooms are already materialized per above schemas
# Join courses to room directory
joined = prepared_subject_offerings.merge(
    prepared_rooms,
    how='left',
    left_on='MEET_PLACE',
    right_on='fac_room_key'
)

# Coerce enrollment to numeric and filter > 300 attendees
joined['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(joined['SUBJECT_ENROLLMENT_NUMBER'], errors='coerce')
filtered = joined[joined['SUBJECT_ENROLLMENT_NUMBER'] > 300]

# Select and rename columns for final output
result = filtered[[
    'TERM_CODE',                 # unique term code
    'SUBJECT_TITLE',             # subject title
    'ROOM',                      # room
    'FLOOR',                     # floor
    'BUILDING_KEY',              # building key
    'FORM_TYPE',                 # formats (code)
    'FORM_TYPE_DESC',            # formats (description)
    'SUBJECT_ENROLLMENT_NUMBER'  # number of enrolled students
]].drop_duplicates()

# Note: Building street address, city, state, and postal code are not available in selected tables.
# If a building/address table is available, join on BUILDING_KEY to add address fields before returning.

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
