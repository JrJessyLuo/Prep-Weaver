import pandas as pd
import numpy as np

def _prep_1(table_1):
    core = table_1[['BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG','BUILDING_HEIGHT','ASSIGNABLE_AREA','EXT_GROSS_AREA']].copy()
    core = core.drop_duplicates(subset=['BUILDING_NUMBER'], keep='first')
    target = core[['BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG','BUILDING_HEIGHT','ASSIGNABLE_AREA','EXT_GROSS_AREA']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['BUILDING_NUMBER','BUILDING_NAME','BUILDING_STREET_ADDRESS']].copy()
    prepared = prepared.drop_duplicates(subset=['BUILDING_NUMBER'], keep='first')
    target = prepared[['BUILDING_NUMBER','BUILDING_NAME','BUILDING_STREET_ADDRESS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1[['HR_DEPARTMENT_NAME']].copy()
    df['HR_DEPARTMENT_NAME'] = df['HR_DEPARTMENT_NAME'].astype('string').str.strip()
    df = df[df['HR_DEPARTMENT_NAME'].notna() & (df['HR_DEPARTMENT_NAME'] != '')]
    target = df.drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_4'])
prepared_buildings_core = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_table_3 = _prep_3(tables['table_1'])
prepared_building_addresses = prepared_table_3
prepared_table_4 = _prep_4(tables['table_8'])
prepared_hr_departments = prepared_table_4

# Merge core building data with addresses on BUILDING_NUMBER
b = merge(prepared_buildings_core, prepared_building_addresses, on='BUILDING_NUMBER', how='left')

# Choose a building name preference order: use BUILDING_NAME from core if present, else from addresses, else BUILDING_NAME_LONG
b['BUILDING_NAME_FINAL'] = b['BUILDING_NAME_x'].fillna(b['BUILDING_NAME_y']).fillna(b['BUILDING_NAME_LONG'])

# Derive required outputs
result = b.rename(columns={
    'BUILDING_NUMBER': 'building_number',
    'BUILDING_NAME_FINAL': 'building_name',
    'BUILDING_HEIGHT': 'building_height',
    'BUILDING_STREET_ADDRESS': 'street_address',
    'ASSIGNABLE_AREA': 'assignable_square_footage',
    'EXT_GROSS_AREA': 'total_square_footage'
})

# Average square footage (assignable) as requested context; if intended as per-room or per-building average not defined in data, compute assignable avg per building = assignable/1
# Here interpret as average of assignable and non-assignable not available; fall back to average per building using total/1. If both present, compute average of assignable and total.
result['average_square_footage'] = np.where(
    result['assignable_square_footage'].notna() & result['total_square_footage'].notna(),
    (result['assignable_square_footage'] + result['total_square_footage']) / 2.0,
    result['assignable_square_footage'].fillna(result['total_square_footage'])
)

# No city/state columns exist in selected tables; set as MIT default placeholders if required
result['city'] = np.nan
result['state'] = np.nan

# HR department name not linkable from provided schemas; leave null
result['HR_department_name'] = np.nan

# Select and order columns
result = result[[
    'building_name',
    'building_number',
    'building_height',
    'street_address',
    'city',
    'state',
    'HR_department_name',
    'assignable_square_footage',
    'total_square_footage',
    'average_square_footage'
]]

# Order descending by assignable, then total, then average square footage
result = result.sort_values(by=['assignable_square_footage','total_square_footage','average_square_footage'], ascending=[False, False, False])

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
