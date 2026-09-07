import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['fac_room_key','BUILDING_KEY','FLOOR','FLOOR_KEY','ROOM','SPACE_ID','ROOM_FULL_NAME','ORGANIZATION_KEY','ORGANIZATION_NAME','DEPT_CODE','AREA']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['FAC_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG','ASSIGNABLE_AREA']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['BUILDING_KEY','FLOOR_KEY','ROOM_NUMBER','ROOM_SQUARE_FOOTAGE']].copy()
    df['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(df['ROOM_SQUARE_FOOTAGE'], errors='coerce')
    target = df.drop_duplicates(subset=['BUILDING_KEY','FLOOR_KEY','ROOM_NUMBER','ROOM_SQUARE_FOOTAGE']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_floors = prepared_table_3

# Assume prepared_* DataFrames exist as specified.
rooms = prepared_rooms.copy()
bldgs = prepared_buildings.copy()
floors = prepared_floors.copy()

# Coerce numeric fields
rooms['AREA'] = pd.to_numeric(rooms['AREA'], errors='coerce')
bldgs['ASSIGNABLE_AREA'] = pd.to_numeric(bldgs['ASSIGNABLE_AREA'], errors='coerce')

# Join buildings to get building names and assignable area
rooms_b = rooms.merge(
    bldgs.rename(columns={'FAC_BUILDING_KEY':'BUILDING_KEY'}),
    on='BUILDING_KEY', how='left'
)

# Compute floor total area per building-floor using floors table
# First, ensure join keys align for per-room mapping (ROOM matches ROOM_NUMBER)
floors_subset = floors[['BUILDING_KEY','FLOOR_KEY','ROOM_NUMBER','ROOM_SQUARE_FOOTAGE']].copy()
floors_subset['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(floors_subset['ROOM_SQUARE_FOOTAGE'], errors='coerce')

# Floor totals
floor_totals = floors_subset.groupby(['BUILDING_KEY','FLOOR_KEY'], as_index=False)['ROOM_SQUARE_FOOTAGE'].sum()
floor_totals = floor_totals.rename(columns={'ROOM_SQUARE_FOOTAGE':'FLOOR_TOTAL_AREA'})

# Attach floor totals to each room via BUILDING_KEY and FLOOR_KEY
rooms_b = rooms_b.merge(floor_totals, on=['BUILDING_KEY','FLOOR_KEY'], how='left')

# Percentages: room over floor total and over building assignable area
rooms_b['pct_room_over_floor'] = rooms_b['AREA'] / rooms_b['FLOOR_TOTAL_AREA']
rooms_b['pct_room_over_building'] = rooms_b['AREA'] / rooms_b['ASSIGNABLE_AREA']

# Select requested output columns
target = rooms_b[[
    'ROOM_FULL_NAME',            # full room name
    'BUILDING_NAME',             # building name (short)
    'BUILDING_NAME_LONG',        # building name (long)
    'FLOOR',                     # floor number
    'ORGANIZATION_NAME',         # occupying organization name
    'DEPT_CODE',                 # department code (name not available in provided tables)
    'AREA',                      # room area (evidence for percentages)
    'FLOOR_TOTAL_AREA',          # floor total area (evidence)
    'ASSIGNABLE_AREA',           # building assignable area (evidence)
    'pct_room_over_floor',
    'pct_room_over_building'
]].copy()

# Optionally format percentages
# target['pct_room_over_floor'] = (target['pct_room_over_floor']*100).round(2)
# target['pct_room_over_building'] = (target['pct_room_over_building']*100).round(2)

result = target

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
