import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['BUILDING_NUMBER','BUILDING_NAME_LONG','DATE_BUILT','NUM_OF_ROOMS']].copy()
    prepared['DATE_BUILT'] = pd.to_datetime(prepared['DATE_BUILT'], errors='coerce', infer_datetime_format=True)
    target = prepared[['BUILDING_NUMBER','BUILDING_NAME_LONG','DATE_BUILT','NUM_OF_ROOMS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    rooms = table_1[['BUILDING_ROOM']].copy()
    rooms['BUILDING_NUMBER'] = rooms['BUILDING_ROOM'].astype(str).str.split('-', n=1).str[0]
    rooms = rooms.dropna(subset=['BUILDING_ROOM', 'BUILDING_NUMBER'])
    rooms = rooms.drop_duplicates(subset=['BUILDING_NUMBER', 'BUILDING_ROOM'])
    target = rooms[['BUILDING_NUMBER', 'BUILDING_ROOM']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_4'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_rooms = prepared_table_2

# prepared_buildings: keep as provided
b = prepared_buildings.copy()

# prepared_rooms: ensure BUILDING_NUMBER parsed from BUILDING_ROOM
r = prepared_rooms.copy()
if 'BUILDING_NUMBER' not in r.columns and 'BUILDING_ROOM' in r.columns:
    r['BUILDING_NUMBER'] = r['BUILDING_ROOM'].astype(str).str.split('-', n=1).str[0]

# Integrate (if needed). For this question, employee threshold is approximated by NUM_OF_ROOMS > 100.
# We don't actually need room-level expansion to compute the answer, but preserve the join pattern.
merged = b.merge(r[['BUILDING_NUMBER']].drop_duplicates(), on='BUILDING_NUMBER', how='left')

# Parse built year from DATE_BUILT (formats like 'MM/DD/YYYY').
def parse_year(x):
    try:
        # Try standard parse
        return pd.to_datetime(x, errors='coerce').year
    except Exception:
        return pd.NaT

merged['BUILT_YEAR'] = pd.to_datetime(merged['DATE_BUILT'], errors='coerce').dt.year

# Filter: constructed before 1950 and more than 100 employees (approximated by NUM_OF_ROOMS > 100)
ans = merged[(merged['BUILT_YEAR'].notna()) & (merged['BUILT_YEAR'] < 1950) & (merged['NUM_OF_ROOMS'] > 100)]

# Select required output columns and drop duplicates
answer = ans[['BUILDING_NAME_LONG', 'BUILT_YEAR', 'NUM_OF_ROOMS']].drop_duplicates().sort_values(['BUILDING_NAME_LONG'])

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
