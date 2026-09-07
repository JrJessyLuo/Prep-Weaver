import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['BUILDING_KEY','ROOM','ROOM_FULL_NAME','AREA','MAJOR_USE_DESC','ORGANIZATION_NAME','SPACE_ID','FLOOR']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['FAC_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG']].copy()
    prepared = prepared.drop_duplicates(subset=['FAC_BUILDING_KEY'])
    target = prepared[['FAC_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_buildings = prepared_table_2

# Assume prepared_rooms and prepared_buildings are provided per the target schemas
# 1) Identify building 45 and join to rooms
b45 = prepared_buildings[prepared_buildings['BUILDING_NUMBER'].astype(str).str.strip() == '45']
rooms_b45 = prepared_rooms.merge(b45[['FAC_BUILDING_KEY']], left_on='BUILDING_KEY', right_on='FAC_BUILDING_KEY', how='inner')

# 2) List all rooms with requested details
rooms_list = rooms_b45[['ROOM', 'ROOM_FULL_NAME', 'AREA', 'MAJOR_USE_DESC', 'ORGANIZATION_NAME']].copy()
# Ensure AREA is numeric for later aggregations
rooms_list['AREA'] = pd.to_numeric(rooms_list['AREA'], errors='coerce')

# 3) Count of rooms per major use
count_per_major_use = rooms_b45.groupby('MAJOR_USE_DESC', dropna=False)['ROOM'].nunique().reset_index(name='room_count')

# 4) Total area per organization
area_per_org = rooms_b45.assign(AREA=pd.to_numeric(rooms_b45['AREA'], errors='coerce')) \
    .groupby('ORGANIZATION_NAME', dropna=False)['AREA'].sum().reset_index(name='total_area')

# Package outputs
result = {
    'rooms': rooms_list.sort_values(['MAJOR_USE_DESC','ORGANIZATION_NAME','ROOM'], na_position='last').reset_index(drop=True),
    'rooms_per_major_use': count_per_major_use.sort_values('room_count', ascending=False).reset_index(drop=True),
    'total_area_per_organization': area_per_org.sort_values('total_area', ascending=False).reset_index(drop=True)
}

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
