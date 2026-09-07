import pandas as pd
import numpy as np

def _prep_1(table_1):
    rooms = table_1[['FCLT_ROOM_KEY','ROOM_FULL_NAME','FCLT_BUILDING_KEY']].copy()
    rooms['ROOM_FULL_NAME'] = rooms['ROOM_FULL_NAME'].replace(['nan','NaN','None',''], pd.NA)
    rooms = rooms.groupby(['FCLT_ROOM_KEY','FCLT_BUILDING_KEY'], as_index=False).agg({'ROOM_FULL_NAME': lambda s: s.dropna().iloc[0] if s.notna().any() else pd.NA})
    target = rooms[['FCLT_ROOM_KEY','ROOM_FULL_NAME','FCLT_BUILDING_KEY']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['FCLT_BUILDING_KEY','BUILDING_NAME','BUILDING_NAME_LONG','BUILDING_HEIGHT']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['BUILDING_KEY','ADDRESS_PURPOSE','STREET_NUMBER','STREET_NUMBER_SUFFIX','PRE_DIRECTIONAL','STREET_NAME','STREET_SUFFIX','POST_DIRECTIONAL','CITY','STATE','POSTAL_CODE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_5(table_1):
    prepared = table_1[['subject_id','DEPARTMENT_CODE','DEPARTMENT_NAME']].copy()
    prepared['DEPARTMENT_NAME'] = prepared['DEPARTMENT_NAME'].replace('nan', pd.NA)
    prepared = prepared.groupby(['subject_id','DEPARTMENT_CODE'], as_index=False).agg({'DEPARTMENT_NAME': lambda s: s.dropna().iloc[0] if s.dropna().shape[0] > 0 else pd.NA})
    target = prepared[['subject_id','DEPARTMENT_CODE','DEPARTMENT_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_building_addresses = prepared_table_3
prepared_table_4 = _prep_4(tables['table_9'])
prepared_table_5 = _prep_5(tables['table_8'])
prepared_subjects = prepared_table_5

# Inputs assumed to be dataframes with names matching target_table_name
# prepared_rooms, prepared_buildings, prepared_building_addresses, prepared_subjects

# 1) Identify subjects that Computer Science students can enroll in.
# Heuristic: subjects offered by EECS department (DEPARTMENT_CODE == '6' or DEPARTMENT_NAME contains 'Computer Sci').
cs_subjects = prepared_subjects[(prepared_subjects['DEPARTMENT_CODE'] == '6') | (prepared_subjects['DEPARTMENT_NAME'].str.contains('Computer Sci', case=False, na=False))]

# 2) We need rooms associated with those subjects. No direct subject-to-room mapping is present in the selected tables.
# Therefore, we cannot filter rooms by subjects with the current inputs. Proceed by returning empty result if association data is missing.
# If another table providing section/meeting locations linked by subject_id and room (e.g., meeting schedule) is available, join it here.

# Compose building info (for potential later filtering once room-subject association exists)
rooms_buildings = prepared_rooms.merge(prepared_buildings, on='FCLT_BUILDING_KEY', how='left')

# Keep street addresses only from addresses table
addr_street = prepared_building_addresses[prepared_building_addresses['ADDRESS_PURPOSE'].str.upper().eq('STREET')]

rooms_bldg_addr = rooms_buildings.merge(addr_street, left_on='FCLT_BUILDING_KEY', right_on='BUILDING_KEY', how='left')

# Compose street address string
def compose_address(row):
    parts = [str(row.get('STREET_NUMBER') or '').strip(), str(row.get('STREET_NUMBER_SUFFIX') or '').strip(), str(row.get('PRE_DIRECTIONAL') or '').strip(), str(row.get('STREET_NAME') or '').strip(), str(row.get('STREET_SUFFIX') or '').strip(), str(row.get('POST_DIRECTIONAL') or '').strip()]
    parts = [p for p in parts if p and p.lower() != 'nan']
    return ' '.join(parts) if parts else None

rooms_bldg_addr['STREET_ADDRESS'] = rooms_bldg_addr.apply(compose_address, axis=1)

# Placeholder for subject-room association: expecting a dataframe 'subject_room' with columns ['subject_id','FCLT_ROOM_KEY'].
# If available, uncomment and integrate as below:
# associated_rooms = subject_room.merge(cs_subjects[['subject_id']], on='subject_id', how='inner').drop_duplicates('FCLT_ROOM_KEY')
# result = associated_rooms.merge(rooms_bldg_addr, on='FCLT_ROOM_KEY', how='left')
# Otherwise, return empty with correct columns.

# Prepare final columns and ensure uniqueness
cols = ['ROOM_FULL_NAME', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'STREET_ADDRESS', 'CITY', 'STATE', 'POSTAL_CODE', 'BUILDING_HEIGHT']
empty = pd.DataFrame(columns=cols)

# If association exists, replace 'empty' with the computed 'result[cols].drop_duplicates()'
# result = result[cols].drop_duplicates()
# target = result

target = empty

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
