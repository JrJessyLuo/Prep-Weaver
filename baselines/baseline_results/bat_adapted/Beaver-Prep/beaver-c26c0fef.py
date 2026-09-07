import pandas as pd
import numpy as np

def _prep_1(table_1):
    source = table_1.copy()
    source = source.replace({'nan': pd.NA, 'NaN': pd.NA, 'None': pd.NA, '': pd.NA})
    source['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(source['SUBJECT_ENROLLMENT_NUMBER'], errors='coerce')
    target = source[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','MEET_PLACE','FORM_TYPE','FORM_TYPE_DESC','SUBJECT_ENROLLMENT_NUMBER']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared_rooms = table_1[['fac_room_key','ROOM','FLOOR','BUILDING_KEY']].copy()
    prepared_rooms = prepared_rooms.drop_duplicates(subset=['fac_room_key'])
    target = prepared_rooms[['fac_room_key','ROOM','FLOOR','BUILDING_KEY']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
