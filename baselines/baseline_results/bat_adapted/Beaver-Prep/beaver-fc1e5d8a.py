import pandas as pd
import numpy as np

def _prep_1(table_1):
    buildings = table_1[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME']].copy()
    buildings = buildings.drop_duplicates(subset=['BUILDING_KEY'])
    target = buildings[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    rooms = table_1[['BUILDING_KEY','FLOOR','ROOM','ORGANIZATION_NAME','DEPT_CODE']].copy()
    rooms = rooms.replace({'nan': pd.NA, 'NaN': pd.NA, '': pd.NA})
    rooms['ORGANIZATION_NAME'] = rooms['ORGANIZATION_NAME'].astype('string')
    rooms['DEPT_CODE'] = rooms['DEPT_CODE'].astype('string')
    rooms = rooms.groupby(['BUILDING_KEY','FLOOR','ROOM'], as_index=False).agg(ORGANIZATION_NAME=('ORGANIZATION_NAME', lambda s: s.dropna().iloc[0] if s.dropna().size else pd.NA), DEPT_CODE=('DEPT_CODE', lambda s: s.dropna().iloc[0] if s.dropna().size else pd.NA))
    target = rooms[['BUILDING_KEY','FLOOR','ROOM','ORGANIZATION_NAME','DEPT_CODE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_5'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_rooms = prepared_table_2

# Merge buildings with rooms on BUILDING_KEY
merged = prepared_buildings.merge(prepared_rooms, on='BUILDING_KEY', how='left')

# Coerce floor to numeric when possible to compute min/max, keeping NaN for non-numeric
floors_num = pd.to_numeric(merged['FLOOR'], errors='coerce')
merged = merged.assign(_FLOOR_NUM=floors_num)

# Aggregate per building
agg = (
    merged.groupby(['BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NUMBER'], dropna=False)
          .agg(
              highest_floor=('._FLOOR_NUM'.strip('.'), 'max'),
              lowest_floor=('._FLOOR_NUM'.strip('.'), 'min'),
              total_rooms=('ROOM', lambda s: s.notna().sum()),
              organizations=('ORGANIZATION_NAME', lambda s: ', '.join(sorted({str(x) for x in s.dropna()})) if s.notna().any() else None),
              departments=('DEPT_CODE', lambda s: ', '.join(sorted({str(x) for x in s.dropna()})) if s.notna().any() else None)
          )
          .reset_index()
)

# Final selection/rename
target = agg.rename(columns={
    'BUILDING_KEY': 'building_key',
    'BUILDING_NAME': 'building_name',
    'BUILDING_NUMBER': 'building_number',
    'highest_floor': 'highest_floor_number',
    'lowest_floor': 'lowest_floor_number',
    'total_rooms': 'total_number_of_rooms',
    'organizations': 'organizations',
    'departments': 'department_names'
})

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
