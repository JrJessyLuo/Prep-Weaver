import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['BUILDING_KEY','FLOOR','FLOOR_KEY','ASSIGNABLE_AREA','NON_ASSIGNABLE_AREA']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['FAC_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG','NUM_OF_ROOMS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    rooms = table_1[['BUILDING_KEY','FLOOR','FLOOR_KEY','ROOM']]
    rooms = rooms.dropna(subset=['BUILDING_KEY','FLOOR','FLOOR_KEY','ROOM'])
    target = rooms.drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_floors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_rooms = prepared_table_3

# Assume prepared_floors, prepared_buildings, prepared_rooms are dataframes created from the respective table_targets

# 1) Aggregate floor areas per building
floor_agg = (
    prepared_floors
    .groupby('BUILDING_KEY', as_index=False)
    .agg(total_assignable_area=('ASSIGNABLE_AREA', 'sum'),
         total_non_assignable_area=('NON_ASSIGNABLE_AREA', 'sum'))
)

# 2) Integrate with buildings on BUILDING_KEY == FAC_BUILDING_KEY
merged = floor_agg.merge(
    prepared_buildings,
    left_on='BUILDING_KEY',
    right_on='FAC_BUILDING_KEY',
    how='left'
)

# 3) Prefer BUILDING_NAME if present, else BUILDING_NAME_LONG
merged['building_name'] = merged['BUILDING_NAME'].where(merged['BUILDING_NAME'].notna(), merged['BUILDING_NAME_LONG'])

# 4) Select and rename columns; NUM_OF_ROOMS is already per building
result = (
    merged
    .assign(total_room_count=merged['NUM_OF_ROOMS'])
    [[
        'building_name',
        'BUILDING_NUMBER',
        'total_assignable_area',
        'total_non_assignable_area',
        'total_room_count'
    ]]
    .sort_values('total_assignable_area', ascending=False)
)

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
