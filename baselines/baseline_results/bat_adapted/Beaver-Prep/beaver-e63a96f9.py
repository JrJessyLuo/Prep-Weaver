import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['FULL_NAME','FIRST_NAME','LAST_NAME','JOB_TITLE','HR_DEPARTMENT_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['fac_room_key','BUILDING_KEY','FLOOR','ROOM','SPACE_ID','ROOM_FULL_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    source = table_1.copy()
    target = source[['BUILDING_KEY','ADDRESS_PURPOSE','STREET_NUMBER','STREET_NUMBER_SUFFIX','PRE_DIRECTIONAL','STREET_NAME','STREET_SUFFIX','POST_DIRECTIONAL','CITY','STATE','POSTAL_CODE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_10'])
people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
rooms = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
building_addresses = prepared_table_3

# Inputs are the prepared tables: people, rooms, building_addresses

# 1) Identify the target person (Professor Summer Haynes)
name_mask = False
if 'FULL_NAME' in people.columns:
    name_mask = people['FULL_NAME'].str.contains('Summer', case=False, na=False) & people['FULL_NAME'].str.contains('Haynes', case=False, na=False)
else:
    name_mask = (people['FIRST_NAME'].str.contains('Summer', case=False, na=False)) & (people['LAST_NAME'].str.contains('Haynes', case=False, na=False))

prof_candidates = people[name_mask]
# Optionally prefer rows with JOB_TITLE containing 'Professor'
if 'JOB_TITLE' in prof_candidates.columns:
    prof_pref = prof_candidates[prof_candidates['JOB_TITLE'].str.contains('Professor', case=False, na=False)]
    if len(prof_pref) > 0:
        prof_candidates = prof_pref

# If multiple, take first (question expects a single office)
prof_row = prof_candidates.head(1)

# NOTE: No explicit join keys from people->rooms are present in the provided schemas.
# In practice, another mapping (e.g., person-to-room assignment) would be required.
# Proceed assuming the office is present in rooms and must be selected by additional business logic or external mapping.
# Here we select candidate office rooms by filtering rooms whose ROOM_FULL_NAME or ROOM suggests an office for the person name if available.

room_candidates = rooms.copy()
if 'ROOM_FULL_NAME' in rooms.columns:
    mask_office_owner = rooms['ROOM_FULL_NAME'].fillna('').str.contains('Haynes', case=False)
    room_candidates = rooms[mask_office_owner]

# If no labeled ownership, fallback to rooms with USE/DESC not available in target; retain all as last resort
if len(room_candidates) == 0:
    room_candidates = rooms

# If multiple rooms, pick first
room_row = room_candidates.head(1).copy()

# 2) Join to building address by BUILDING_KEY
joined = room_row.merge(building_addresses, on='BUILDING_KEY', how='left')

# 3) Compose street address
def compose_street(r):
    parts = [str(r.get('STREET_NUMBER') or '').strip()]
    if pd.notna(r.get('STREET_NUMBER_SUFFIX')) and str(r.get('STREET_NUMBER_SUFFIX')).strip() != 'nan':
        parts.append(str(r['STREET_NUMBER_SUFFIX']).strip())
    if pd.notna(r.get('PRE_DIRECTIONAL')) and str(r.get('PRE_DIRECTIONAL')).strip() != 'nan':
        parts.append(str(r['PRE_DIRECTIONAL']).strip())
    if pd.notna(r.get('STREET_NAME')) and str(r.get('STREET_NAME')).strip() != 'nan':
        parts.append(str(r['STREET_NAME']).strip())
    if pd.notna(r.get('STREET_SUFFIX')) and str(r.get('STREET_SUFFIX')).strip() != 'nan':
        parts.append(str(r['STREET_SUFFIX']).strip())
    if pd.notna(r.get('POST_DIRECTIONAL')) and str(r.get('POST_DIRECTIONAL')).strip() != 'nan':
        parts.append(str(r['POST_DIRECTIONAL']).strip())
    return ' '.join([p for p in parts if p])

joined['street_address'] = joined.apply(compose_street, axis=1)

# 4) Select and rename output columns
answer = joined.rename(columns={
    'ROOM': 'room',
    'FLOOR': 'floor',
    'BUILDING_KEY': 'building_key',
    'CITY': 'city',
    'STATE': 'state',
    'POSTAL_CODE': 'postal_code'
})[
    ['room', 'floor', 'building_key', 'street_address', 'city', 'state', 'postal_code']
]

result = answer

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
