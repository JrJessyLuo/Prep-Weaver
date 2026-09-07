import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['TERM_CODE','COURSE_NUMBER','SUBJECT_ID','SUBJECT_TITLE','HGN_CODE_DESC','TOTAL_UNITS']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['TERM_CODE','COURSE_NUMBER','SUBJECT_ID','SUBJECT_TITLE','HGN_CODE_DESC','TOTAL_UNITS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['BUILDING_ROOM','FCLT_BUILDING_KEY','ROOM','ORGANIZATION_NAME','AREA','MAJOR_USE_DESC']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
