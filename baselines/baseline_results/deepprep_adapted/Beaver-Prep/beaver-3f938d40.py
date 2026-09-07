import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
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
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
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
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COURSE_NUMBER", func="""
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
    table_1["COURSE_NUMBER"] = table_1["COURSE_NUMBER"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
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
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="HGN_CODE_DESC", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # normalize whitespace
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # normalize whitespace
        return " ".join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["HGN_CODE_DESC"] = table_1["HGN_CODE_DESC"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TOTAL_UNITS", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TOTAL_UNITS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TOTAL_UNITS']
    if _dtype == "datetime64":
        table_1['TOTAL_UNITS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TOTAL_UNITS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TOTAL_UNITS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TOTAL_UNITS'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="HGN_CODE_DESC", mode="mode")
    # MissingValueImputation
    table_1["HGN_CODE_DESC"] = table_1["HGN_CODE_DESC"].fillna(table_1["HGN_CODE_DESC"].mode().iloc[0])

    # ---------------- Step 8 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="TOTAL_UNITS", mode="median")
    # MissingValueImputation
    table_1["TOTAL_UNITS"] = table_1["TOTAL_UNITS"].fillna(table_1["TOTAL_UNITS"].median())

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'COURSE_NUMBER', 'SUBJECT_ID', 'SUBJECT_TITLE', 'HGN_CODE_DESC', 'TOTAL_UNITS'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'COURSE_NUMBER', 'SUBJECT_ID', 'SUBJECT_TITLE', 'HGN_CODE_DESC', 'TOTAL_UNITS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SUBJECT_ID', 'TERM_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SUBJECT_ID', 'TERM_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 11 ----------------
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
    # Deduplicate(table_name="table_1", subset=['BUILDING_ROOM'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_ROOM'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_ROOM', 'FCLT_BUILDING_KEY', 'ROOM', 'ORGANIZATION_NAME', 'AREA', 'MAJOR_USE_DESC'])
    # SelectCol
    _cols = [c for c in ['BUILDING_ROOM', 'FCLT_BUILDING_KEY', 'ROOM', 'ORGANIZATION_NAME', 'AREA', 'MAJOR_USE_DESC'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_8'])
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_rooms = prepared_table_2

# Inputs: prepared_subjects, prepared_rooms, plus an external meetings table providing per-course meeting location/time
# Assumptions for integration:
# - A meetings/preparation step (not shown in table_targets) produces prepared_meetings with columns:
#   ['TERM_CODE','SUBJECT_ID','COURSE_NUMBER','BUILDING_ROOM','MEET_PLACE','MEET_TIME']
# - BUILDING_ROOM in prepared_meetings matches BUILDING_ROOM in prepared_rooms (e.g., '10-250').

# Filter out NULL meet place or meet times
meetings_valid = prepared_meetings.dropna(subset=['MEET_PLACE','MEET_TIME'])

# Integrate subjects with meetings (by term and subject) to assign course instances to rooms
sub_meet = meetings_valid.merge(
    prepared_subjects,
    on=['TERM_CODE','SUBJECT_ID','COURSE_NUMBER'],
    how='inner'
)

# Join to room attributes via BUILDING_ROOM
sub_meet_room = sub_meet.merge(
    prepared_rooms,
    on='BUILDING_ROOM',
    how='left'
)

# Derive requested fields
# - room number of course location: ROOM
# - building name and number, city, state are not present; only building code (FCLT_BUILDING_KEY) available
# - organization name: ORGANIZATION_NAME
# - room usage: MAJOR_USE_DESC
# - term code: TERM_CODE
# - course level: HGN_CODE_DESC
# - total number of subjects per course offering: count distinct SUBJECT_ID per course-term
# - unique meeting times: count distinct MEET_TIME per course-term
# - total units: TOTAL_UNITS (may need aggregation if multiple subjects per course)

agg = (
    sub_meet_room
    .groupby(['TERM_CODE','COURSE_NUMBER','SUBJECT_ID','BUILDING_ROOM','ROOM','FCLT_BUILDING_KEY','ORGANIZATION_NAME','MAJOR_USE_DESC','HGN_CODE_DESC'], dropna=False)
    .agg(
        total_subjects=('SUBJECT_ID','nunique'),
        unique_meeting_times=('MEET_TIME','nunique'),
        total_units=('TOTAL_UNITS', lambda x: pd.to_numeric(x, errors='coerce').max())
    )
    .reset_index()
)

# Rename/prepare final projection
answer = agg.rename(columns={
    'ROOM': 'room_number',
    'FCLT_BUILDING_KEY': 'building_number',
    'ORGANIZATION_NAME': 'organization_name',
    'MAJOR_USE_DESC': 'room_usage',
    'HGN_CODE_DESC': 'course_level'
})[
    [
        'COURSE_NUMBER',            # course
        'room_number',              # room number of course location
        'building_number',          # building number (name not available)
        # building name, city, state not available in selected tables
        'organization_name',
        'room_usage',
        'TERM_CODE',                # term code
        'course_level',             # course level
        'total_subjects',           # total number of subjects
        'unique_meeting_times',     # unique meeting times
        'total_units'               # total units
    ]
]

# If building name/city/state are required, an additional building dimension table would need to be joined on FCLT_BUILDING_KEY before final projection.

target = answer

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
