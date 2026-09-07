import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['BUILDING_KEY','MAJOR_USE_DESC','USE_DESC','ROOM','ROOM_FULL_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['BUILDING_KEY','BUILDING_NAME','BUILDING_NUMBER']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['BUILDING_KEY','BUILDING_NAME','BUILDING_NUMBER']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_9'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_7'])
prepared_buildings = prepared_table_2

# Assume prepared_rooms and prepared_buildings are already synthesized from their respective sources
# Join rooms to buildings
rooms_bldg = prepared_rooms.merge(prepared_buildings, on='BUILDING_KEY', how='left')

# Heuristic: identify rooms that accommodate students. Adjust the keyword set as needed based on data dictionary.
# We consider MAJOR_USE_DESC/USE_DESC/ROOM_FULL_NAME text for hints like 'DORM', 'RESIDENCE', 'HOUSING', 'STUDENT', 'BED', 'ROOM', 'SUITE'.
text_cols = ['MAJOR_USE_DESC', 'USE_DESC', 'ROOM_FULL_NAME']
for c in text_cols:
    if c not in rooms_bldg.columns:
        rooms_bldg[c] = None

def contains_student_hint(s):
    if pd.isna(s):
        return False
    s = str(s).upper()
    hints = ['DORM', 'RESIDENCE', 'HOUS', 'STUDENT', 'BED', 'SUITE']
    return any(h in s for h in hints)

rooms_bldg['is_student_accom'] = rooms_bldg[text_cols].apply(lambda r: any(contains_student_hint(v) for v in r.values), axis=1)

# Count student-accommodating rooms per building as a proxy for capacity (actual bed counts not provided).
building_counts = (
    rooms_bldg[rooms_bldg['is_student_accom']]
    .groupby(['BUILDING_KEY', 'BUILDING_NAME'], dropna=False, as_index=False)
    .size()
    .rename(columns={'size': 'student_room_count'})
)

# Find building with maximum count
if not building_counts.empty:
    top = building_counts.sort_values(['student_room_count', 'BUILDING_NAME'], ascending=[False, True]).head(1)
    answer_building = top['BUILDING_NAME'].iloc[0]
    answer_count = int(top['student_room_count'].iloc[0])
else:
    answer_building = None
    answer_count = 0

result = {'building_name': answer_building, 'students_accommodated_proxy': answer_count}

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
