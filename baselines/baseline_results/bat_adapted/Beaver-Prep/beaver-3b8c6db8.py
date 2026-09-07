import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG','DATE_BUILT','BUILDING_TYPE','EXT_GROSS_AREA','NUM_OF_ROOMS']].copy()
    prepared['DATE_BUILT'] = pd.to_datetime(prepared['DATE_BUILT'], errors='coerce', infer_datetime_format=True)
    prepared = prepared.drop_duplicates(subset=['FCLT_BUILDING_KEY'])
    target = prepared[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG','DATE_BUILT','BUILDING_TYPE','EXT_GROSS_AREA','NUM_OF_ROOMS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['FCLT_BUILDING_KEY','BUILDING_NUMBER','FCLT_BUILDING_ADDRESS_KEY']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['BUILDING_KEY','ROOM_COUNTER']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_4'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_8'])
prepared_building_addresses = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_rooms = prepared_table_3

# Assume prepared_buildings, prepared_building_addresses, prepared_rooms are dataframes created per target schemas

# Count addresses per building
addr_counts = prepared_building_addresses.groupby('FCLT_BUILDING_KEY', dropna=False)['FCLT_BUILDING_ADDRESS_KEY'].nunique().reset_index(name='address_count')

# Sum rooms per building from room-level table (fallback if NUM_OF_ROOMS is missing or to corroborate)
room_sums = prepared_rooms.groupby('BUILDING_KEY', dropna=False)['ROOM_COUNTER'].sum(min_count=1).reset_index()
room_sums = room_sums.rename(columns={'BUILDING_KEY':'FCLT_BUILDING_KEY', 'ROOM_COUNTER':'rooms_from_rooms'})

# Merge counts into buildings
merged = prepared_buildings.merge(addr_counts, on='FCLT_BUILDING_KEY', how='left')\
                     .merge(room_sums, on='FCLT_BUILDING_KEY', how='left')

# Choose total rooms: prefer building-level NUM_OF_ROOMS if available; otherwise use summed rooms
def choose_rooms(row):
    if pd.notna(row.get('NUM_OF_ROOMS')):
        return row['NUM_OF_ROOMS']
    return row.get('rooms_from_rooms')

merged['total_rooms'] = merged.apply(choose_rooms, axis=1)

# Prepare final columns: name, number, construction date, type, address count, avg gross area (per building this is just its value)
# Use BUILDING_NAME if present else fallback to BUILDING_NAME_LONG
merged['building_name_out'] = merged['BUILDING_NAME'].where(merged['BUILDING_NAME'].notna() & (merged['BUILDING_NAME'] != ''), merged['BUILDING_NAME_LONG'])

result = merged[['building_name_out', 'BUILDING_NUMBER', 'DATE_BUILT', 'BUILDING_TYPE', 'address_count', 'EXT_GROSS_AREA', 'total_rooms']].copy()
result = result.rename(columns={
    'building_name_out':'building_name',
    'BUILDING_NUMBER':'building_number',
    'DATE_BUILT':'construction_date',
    'BUILDING_TYPE':'building_type',
    'address_count':'address_count',
    'EXT_GROSS_AREA':'average_gross_area',
    'total_rooms':'total_rooms'
})

# Sort by building name
result = result.sort_values(by='building_name', kind='stable')

# 'result' is the final answer dataframe
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
