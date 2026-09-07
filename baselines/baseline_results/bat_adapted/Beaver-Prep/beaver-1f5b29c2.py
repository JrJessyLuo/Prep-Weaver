import pandas as pd
import numpy as np

def _prep_1(table_1):
    rooms = table_1[['FCLT_ROOM_KEY','FCLT_BUILDING_KEY','FCLT_FLOOR_KEY','FLOOR','ROOM','SPACE_ID','ORGANIZATION_NAME','AREA']].copy()
    rooms['AREA'] = pd.to_numeric(rooms['AREA'], errors='coerce')
    rooms = rooms.drop_duplicates(subset=['FCLT_ROOM_KEY'], keep='first')
    target = rooms[['FCLT_ROOM_KEY','FCLT_BUILDING_KEY','FCLT_FLOOR_KEY','FLOOR','ROOM','SPACE_ID','ORGANIZATION_NAME','AREA']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG','OWNERSHIP_TYPE','NUM_OF_ROOMS','ASSIGNABLE_AREA']].copy()
    prepared['NUM_OF_ROOMS'] = pd.to_numeric(prepared['NUM_OF_ROOMS'], errors='coerce')
    prepared['ASSIGNABLE_AREA'] = pd.to_numeric(prepared['ASSIGNABLE_AREA'], errors='coerce')
    target = prepared[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG','OWNERSHIP_TYPE','NUM_OF_ROOMS','ASSIGNABLE_AREA']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_buildings = prepared_table_2

# Merge rooms with buildings
rooms_bldg = prepared_rooms.merge(prepared_buildings, on='FCLT_BUILDING_KEY', how='left')

# Ensure numeric types
rooms_bldg['AREA'] = pd.to_numeric(rooms_bldg['AREA'], errors='coerce')
rooms_bldg['ASSIGNABLE_AREA'] = pd.to_numeric(rooms_bldg['ASSIGNABLE_AREA'], errors='coerce')
rooms_bldg['NUM_OF_ROOMS'] = pd.to_numeric(rooms_bldg['NUM_OF_ROOMS'], errors='coerce')

# Derive display building name (prefer BUILDING_NAME, fallback to BUILDING_NAME_LONG)
rooms_bldg['BUILDING_NAME_DISPLAY'] = rooms_bldg['BUILDING_NAME'].where(rooms_bldg['BUILDING_NAME'].notna() & (rooms_bldg['BUILDING_NAME']!=''), rooms_bldg['BUILDING_NAME_LONG'])

# Compute building total area for room-relative percentage (sum of room AREA per building) and campus total area for grand-relative percentage
building_room_area = rooms_bldg.groupby('FCLT_BUILDING_KEY', dropna=False)['AREA'].sum().rename('BUILDING_ROOM_AREA')
rooms_bldg = rooms_bldg.merge(building_room_area, on='FCLT_BUILDING_KEY', how='left')

grand_total_area = rooms_bldg['AREA'].sum(min_count=1)

# Base room-level rows
room_rows = rooms_bldg.copy()
room_rows['LEVEL'] = 'Room'
room_rows['FLOOR_NUMBER'] = room_rows['FLOOR']
room_rows['ROOM_NUMBER'] = room_rows['ROOM']
room_rows['ORGANIZATION'] = room_rows['ORGANIZATION_NAME']
room_rows['OWNERSHIP'] = room_rows['OWNERSHIP_TYPE']
room_rows['NUM_ROOMS_BUILDING'] = room_rows['NUM_OF_ROOMS']
# Percent of area relative to building (using sum of room areas per building)
room_rows['PCT_AREA_REL_BUILDING'] = (room_rows['AREA'] / room_rows['BUILDING_ROOM_AREA']) * 100
# Percent of area relative to all buildings (for display consistency; used for building and grand totals per requirement)
room_rows['PCT_AREA_REL_ALL'] = (room_rows['AREA'] / grand_total_area) * 100

# Floor subtotals within each building
floor_agg = rooms_bldg.groupby(['FCLT_BUILDING_KEY','BUILDING_NAME_DISPLAY','OWNERSHIP_TYPE','FLOOR'], dropna=False).agg(
    AREA=('AREA','sum'),
    NUM_ROOMS=('FCLT_ROOM_KEY','count')
).reset_index()
floor_agg = floor_agg.merge(building_room_area.reset_index(), on='FCLT_BUILDING_KEY', how='left')
floor_agg['LEVEL'] = 'Subtotal: Floor'
floor_agg['FLOOR_NUMBER'] = floor_agg['FLOOR']
floor_agg['ROOM_NUMBER'] = pd.NA
floor_agg['ORGANIZATION'] = pd.NA
floor_agg['OWNERSHIP'] = floor_agg['OWNERSHIP_TYPE']
# For floor subtotals, percentage relative to building
floor_agg['PCT_AREA_REL_BUILDING'] = (floor_agg['AREA'] / floor_agg['BUILDING_ROOM_AREA']) * 100
floor_agg['PCT_AREA_REL_ALL'] = (floor_agg['AREA'] / grand_total_area) * 100
# Carry NUM_ROOMS per floor and building metadata
floor_agg = floor_agg.merge(prepared_buildings[['FCLT_BUILDING_KEY','NUM_OF_ROOMS']], on='FCLT_BUILDING_KEY', how='left')
floor_agg = floor_agg.rename(columns={'BUILDING_NAME_DISPLAY':'BUILDING_NAME_DISPLAY'})

# Building subtotals (across all floors in each building)
bldg_agg = rooms_bldg.groupby(['FCLT_BUILDING_KEY','BUILDING_NAME_DISPLAY','OWNERSHIP_TYPE'], dropna=False).agg(
    AREA=('AREA','sum'),
    NUM_ROOMS_CALC=('FCLT_ROOM_KEY','count')
).reset_index()
# Use official NUM_OF_ROOMS if available, else fallback to calc
bldg_agg = bldg_agg.merge(prepared_buildings[['FCLT_BUILDING_KEY','NUM_OF_ROOMS']], on='FCLT_BUILDING_KEY', how='left')
bldg_agg['NUM_ROOMS_FINAL'] = bldg_agg['NUM_OF_ROOMS'].where(bldg_agg['NUM_OF_ROOMS'].notna(), bldg_agg['NUM_ROOMS_CALC'])
# Percent relative to all buildings per requirement for building subtotal
bldg_agg['PCT_AREA_REL_ALL'] = (bldg_agg['AREA'] / grand_total_area) * 100
bldg_agg['LEVEL'] = 'Subtotal: Building'
bldg_agg['FLOOR_NUMBER'] = pd.NA
bldg_agg['ROOM_NUMBER'] = pd.NA
bldg_agg['ORGANIZATION'] = pd.NA
bldg_agg['PCT_AREA_REL_BUILDING'] = pd.NA

# Grand total across all buildings
grand = pd.DataFrame({
    'LEVEL':['Grand Total'],
    'BUILDING_NAME_DISPLAY':[pd.NA],
    'OWNERSHIP_TYPE':[pd.NA],
    'FLOOR_NUMBER':[pd.NA],
    'ROOM_NUMBER':[pd.NA],
    'ORGANIZATION':[pd.NA],
    'AREA':[grand_total_area],
    'NUM_ROOMS_CALC':[rooms_bldg['FCLT_ROOM_KEY'].count()],
    'PCT_AREA_REL_ALL':[100.0],
    'PCT_AREA_REL_BUILDING':[pd.NA]
})

# Select and align columns for each block
room_out = room_rows[['LEVEL','BUILDING_NAME_DISPLAY','FLOOR_NUMBER','ROOM_NUMBER','OWNERSHIP','ORGANIZATION','NUM_ROOMS_BUILDING','AREA','PCT_AREA_REL_BUILDING']].copy()
room_out['PCT_AREA_REL_ALL'] = pd.NA
room_out = room_out.rename(columns={'OWNERSHIP':'OWNERSHIP_TYPE', 'NUM_ROOMS_BUILDING':'NUM_ROOMS'})

floor_out = floor_agg[['LEVEL','BUILDING_NAME_DISPLAY','FLOOR_NUMBER','ROOM_NUMBER','OWNERSHIP','ORGANIZATION','NUM_OF_ROOMS','AREA','PCT_AREA_REL_BUILDING','PCT_AREA_REL_ALL']].copy()
floor_out = floor_out.rename(columns={'OWNERSHIP':'OWNERSHIP_TYPE','NUM_OF_ROOMS':'NUM_ROOMS'})

bldg_out = bldg_agg[['LEVEL','BUILDING_NAME_DISPLAY','OWNERSHIP_TYPE','AREA','PCT_AREA_REL_ALL','NUM_ROOMS_FINAL']].copy()
bldg_out['FLOOR_NUMBER'] = pd.NA
bldg_out['ROOM_NUMBER'] = pd.NA
bldg_out['ORGANIZATION'] = pd.NA
bldg_out['PCT_AREA_REL_BUILDING'] = pd.NA
bldg_out = bldg_out[['LEVEL','BUILDING_NAME_DISPLAY','FLOOR_NUMBER','ROOM_NUMBER','OWNERSHIP_TYPE','ORGANIZATION','NUM_ROOMS_FINAL','AREA','PCT_AREA_REL_BUILDING','PCT_AREA_REL_ALL']]
bldg_out = bldg_out.rename(columns={'NUM_ROOMS_FINAL':'NUM_ROOMS'})

grand_out = grand[['LEVEL','BUILDING_NAME_DISPLAY','FLOOR_NUMBER','ROOM_NUMBER','OWNERSHIP_TYPE','ORGANIZATION','NUM_ROOMS_CALC','AREA','PCT_AREA_REL_BUILDING','PCT_AREA_REL_ALL']].copy()
grand_out = grand_out.rename(columns={'NUM_ROOMS_CALC':'NUM_ROOMS'})

# Concatenate all sections
result = pd.concat([room_out, floor_out, bldg_out, grand_out], ignore_index=True)

# Rounding and formatting
def fmt_int_with_commas(x):
    if pd.isna(x):
        return x
    try:
        return f"{int(round(float(x))):,}"
    except Exception:
        return x

def fmt_pct_2(x):
    if pd.isna(x):
        return x
    try:
        return f"{round(float(x), 2):.2f}%"
    except Exception:
        return x

# Round numeric fields
result['AREA'] = result['AREA'].round(0)
# Format integers with commas: AREA and NUM_ROOMS
result['AREA'] = result['AREA'].apply(fmt_int_with_commas)
result['NUM_ROOMS'] = result['NUM_ROOMS'].apply(fmt_int_with_commas)
# Percentages formatting
result['PCT_AREA_REL_BUILDING'] = result['PCT_AREA_REL_BUILDING'].apply(fmt_pct_2)
result['PCT_AREA_REL_ALL'] = result['PCT_AREA_REL_ALL'].apply(fmt_pct_2)

# Final column names per question
result = result.rename(columns={
    'BUILDING_NAME_DISPLAY':'Building Name',
    'FLOOR_NUMBER':'Floor Number',
    'ROOM_NUMBER':'Room Number',
    'OWNERSHIP_TYPE':'Ownership Type',
    'ORGANIZATION':'Organization Name',
    'NUM_ROOMS':'Number of Rooms',
    'AREA':'Area',
    'PCT_AREA_REL_BUILDING':'% Area Rel Building',
    'PCT_AREA_REL_ALL':'% Area Rel All Buildings',
    'LEVEL':'Row Type'
})

answer = result

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
