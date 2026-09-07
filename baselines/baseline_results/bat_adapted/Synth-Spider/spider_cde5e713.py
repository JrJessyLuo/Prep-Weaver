import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['sid','name','age']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['xh','bh','day']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    melted = table_1.melt(id_vars=['bid'], value_vars=['Legacy', 'Mars', 'Melon'], var_name='boat_type', value_name='boat_name')
    melted = melted.dropna(subset=['boat_name'])
    target = melted[['bid', 'boat_name']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_bookings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_boats = prepared_table_3

# prepared_people: select needed columns
prepared_people = table_1[['sid','name','age']].copy()

# prepared_bookings: select needed columns
prepared_bookings = table_2[['xh','bh','day']].copy()

# prepared_boats: unpivot wide boat-name columns into a single 'boat_name'
boat_name_cols = [c for c in table_3.columns if c != 'bid']
long = table_3.melt(id_vars=['bid'], value_vars=boat_name_cols, var_name='name_col', value_name='boat_name')
prepared_boats = long.dropna(subset=['boat_name'])[['bid','boat_name']].drop_duplicates()

# Integration
people_bookings = prepared_people.merge(prepared_bookings, left_on='sid', right_on='xh', how='inner')
people_bookings_boats = people_bookings.merge(prepared_boats, left_on='bh', right_on='bid', how='inner')

# Apply question-specific filtering: age between 20 and 30 inclusive
people_bookings_boats['age'] = pd.to_numeric(people_bookings_boats['age'], errors='coerce')
filtered = people_bookings_boats[(people_bookings_boats['age'] >= 20) & (people_bookings_boats['age'] <= 30)]

# Get the names of the boats booked
answer = filtered['boat_name'].dropna().drop_duplicates().tolist()
answer

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
