import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['BUILDING_KEY','BUILDING_NAME','BLDG_GROSS_SQUARE_FOOTAGE','BLDG_ASSIGNABLE_SQUARE_FOOTAGE','BUILDING_NUMBER']].copy()
    df['BLDG_GROSS_SQUARE_FOOTAGE'] = pd.to_numeric(df['BLDG_GROSS_SQUARE_FOOTAGE'], errors='coerce')
    df['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = pd.to_numeric(df['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'], errors='coerce')
    target = df.groupby('BUILDING_KEY', as_index=False).agg({'BUILDING_NAME':'first','BLDG_GROSS_SQUARE_FOOTAGE':'max','BLDG_ASSIGNABLE_SQUARE_FOOTAGE':'max','BUILDING_NUMBER':'first'})[['BUILDING_KEY','BUILDING_NAME','BLDG_GROSS_SQUARE_FOOTAGE','BLDG_ASSIGNABLE_SQUARE_FOOTAGE','BUILDING_NUMBER']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['BUILDING_COMPONENT','BUILDING_ROOM','HR_ORG_UNIT_ID','SPACE_USAGE','FLOOR']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['HR_ORG_UNIT_ID','HR_ORG_UNIT_TITLE','HR_DEPARTMENT_NAME']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['HR_ORG_UNIT_ID','HR_ORG_UNIT_TITLE','HR_DEPARTMENT_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_rooms = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_hr_orgs = prepared_table_3

# Start from prepared tables
rooms_hr = prepared_rooms.merge(prepared_hr_orgs, on='HR_ORG_UNIT_ID', how='left')

# Join rooms to buildings by mapping building component/number
bldg_rooms = prepared_buildings.merge(rooms_hr, left_on='BUILDING_NUMBER', right_on='BUILDING_COMPONENT', how='left')

# Identify HR departments occupying each building (distinct names per building)
hr_names_per_building = (
    bldg_rooms.groupby('BUILDING_KEY')['HR_DEPARTMENT_NAME']
    .apply(lambda s: sorted(set([x for x in s.dropna() if str(x).strip() != ''])))
    .reset_index(name='HR_DEPARTMENTS')
)

# Aggregate assignable square footage metrics per building
sqft_agg = (
    prepared_buildings
    .groupby(['BUILDING_KEY', 'BUILDING_NAME', 'BLDG_GROSS_SQUARE_FOOTAGE'], as_index=False)
    .agg(total_assignable_sqft=('BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'sum'),
         avg_assignable_sqft=('BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'mean'))
)

# Combine HR department lists back to building aggregates
result = sqft_agg.merge(hr_names_per_building, on='BUILDING_KEY', how='left')

# Add built year if available (not present in provided schemas). If a built year column exists in buildings, select it in prepared_buildings and include it here.
if 'BUILT_YEAR' in prepared_buildings.columns:
    built_year = prepared_buildings[['BUILDING_KEY', 'BUILT_YEAR']].drop_duplicates()
    result = result.merge(built_year, on='BUILDING_KEY', how='left')
else:
    result['BUILT_YEAR'] = pd.NA

# Final projection per building key
target = result[['BUILDING_KEY', 'BUILDING_NAME', 'HR_DEPARTMENTS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'total_assignable_sqft', 'avg_assignable_sqft', 'BUILT_YEAR']].sort_values('BUILDING_KEY')

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
