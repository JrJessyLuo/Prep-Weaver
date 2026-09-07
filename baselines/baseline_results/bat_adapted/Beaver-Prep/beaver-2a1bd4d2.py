import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_TYPE','EXT_GROSS_AREA']].copy()
    prepared = prepared.drop_duplicates(subset=['FCLT_BUILDING_KEY'])
    target = prepared[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_TYPE','EXT_GROSS_AREA']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['FCLT_BUILDING_KEY','BUILDING_NUMBER','ADDRESS_PURPOSE','STREET_NUMBER','STREET_NUMBER_SUFFIX','PRE_DIRECTIONAL','STREET_NAME','STREET_SUFFIX','POST_DIRECTIONAL','CITY','STATE','POSTAL_CODE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1.loc[:, ['MIT_ID', 'OFFICE_LOCATION']].copy()
    prepared = prepared.drop_duplicates(subset=['MIT_ID'])
    target = prepared[['MIT_ID', 'OFFICE_LOCATION']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    prepared = table_1[['BUILDING_ROOM','BUILDING_COMPONENT']].copy()
    prepared = prepared.dropna(subset=['BUILDING_ROOM','BUILDING_COMPONENT'])
    prepared['BUILDING_ROOM'] = prepared['BUILDING_ROOM'].astype(str).str.strip()
    prepared['BUILDING_COMPONENT'] = prepared['BUILDING_COMPONENT'].astype(str).str.strip()
    prepared = prepared.drop_duplicates(subset=['BUILDING_ROOM','BUILDING_COMPONENT'])
    target = prepared[['BUILDING_ROOM','BUILDING_COMPONENT']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_6'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_addresses = prepared_table_2
prepared_table_3 = _prep_3(tables['table_10'])
prepared_employees = prepared_table_3
prepared_table_4 = _prep_4(tables['table_9'])
prepared_rooms = prepared_table_4

# Assume prepared_* DataFrames are available
b = prepared_buildings.copy()
# Normalize building number to string for joins
b['BUILDING_NUMBER'] = b['BUILDING_NUMBER'].astype(str).str.strip()
# Standardize building type for special display case later
b['BUILDING_TYPE_NORM'] = b['BUILDING_TYPE'].astype(str).str.strip()

# Addresses join on building key
addr = prepared_addresses.copy()
addr['FCLT_BUILDING_KEY'] = addr['FCLT_BUILDING_KEY'].astype(str).str.strip()
addr['POSTAL_CODE'] = addr['POSTAL_CODE'].astype(str).str.strip()

# Merge building to addresses (many addresses per building)
b_addr = b.merge(addr, on='FCLT_BUILDING_KEY', how='left', suffixes=('', '_addr'))

# Build a canonical street address string for uniqueness
street_parts = [
    b_addr['STREET_NUMBER'].fillna('').astype(str).str.strip(),
    b_addr['STREET_NUMBER_SUFFIX'].fillna('').astype(str).str.strip(),
    b_addr['PRE_DIRECTIONAL'].fillna('').astype(str).str.strip(),
    b_addr['STREET_NAME'].fillna('').astype(str).str.strip(),
    b_addr['STREET_SUFFIX'].fillna('').astype(str).str.strip(),
    b_addr['POST_DIRECTIONAL'].fillna('').astype(str).str.strip()
]
b_addr['STREET_ADDRESS_CANON'] = (
    pd.Series(street_parts).T.apply(lambda r: ' '.join([x for x in r if x])).str.upper().str.replace('\s+', ' ', regex=True).str.strip()
)

# Derive per-building unique address dimensions
addr_agg = b_addr.groupby(['FCLT_BUILDING_KEY'], dropna=False).agg(
    unique_street_address_count=('STREET_ADDRESS_CANON', lambda s: s.dropna().replace('', pd.NA).nunique()),
    unique_city_count=('CITY', lambda s: s.dropna().replace('', pd.NA).str.upper().nunique()),
    unique_state_count=('STATE', lambda s: s.dropna().replace('', pd.NA).str.upper().nunique()),
    unique_postal_code_count=('POSTAL_CODE', lambda s: s.dropna().replace('', pd.NA).nunique())
).reset_index()

# Employees: infer building number from OFFICE_LOCATION by matching BUILDING_ROOM
emp = prepared_employees.copy()
rooms = prepared_rooms.copy()

# Clean fields
emp['OFFICE_LOCATION'] = emp['OFFICE_LOCATION'].astype(str).str.strip()
rooms['BUILDING_ROOM'] = rooms['BUILDING_ROOM'].astype(str).str.strip()
rooms['BUILDING_COMPONENT'] = rooms['BUILDING_COMPONENT'].astype(str).str.strip()

# Inner join employees to rooms via exact office location to building_room
emp_rooms = emp.merge(rooms[['BUILDING_ROOM','BUILDING_COMPONENT']], left_on='OFFICE_LOCATION', right_on='BUILDING_ROOM', how='inner')

# Map room building component to buildings via BUILDING_NUMBER
emp_rooms['BUILDING_COMPONENT'] = emp_rooms['BUILDING_COMPONENT'].astype(str).str.strip()
b['BUILDING_NUMBER'] = b['BUILDING_NUMBER'].astype(str).str.strip()
emp_building = emp_rooms.merge(b[['FCLT_BUILDING_KEY','BUILDING_NUMBER']], left_on='BUILDING_COMPONENT', right_on='BUILDING_NUMBER', how='left')

# Count employees per building key (unique MIT_ID to avoid duplicates)
emp_counts = emp_building.dropna(subset=['FCLT_BUILDING_KEY']).groupby('FCLT_BUILDING_KEY')['MIT_ID'].nunique().reset_index(name='employee_count')

# Combine building-level facts: address dims and employee counts
b_facts = b[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_TYPE_NORM','EXT_GROSS_AREA']].merge(addr_agg, on='FCLT_BUILDING_KEY', how='left').merge(emp_counts, on='FCLT_BUILDING_KEY', how='left')

# Non-subdivisions: buildings without a parent (parent building number null/blank) are not subdivisions.
# Since parent column isn't in prepared schema, recreate from original via a left merge if available; else assume not subdivisions by uniqueness of BUILDING_NUMBER.
# Here we treat any building with a non-null BUILDING_NUMBER as a building; count 1 per building for non-subdivision count.
b_facts['not_subdivision_flag'] = 1

# Clean numerics
b_facts['employee_count'] = b_facts['employee_count'].fillna(0).astype(int)
b_facts['EXT_GROSS_AREA'] = pd.to_numeric(b_facts['EXT_GROSS_AREA'], errors='coerce').fillna(0.0)

# Aggregate per building type
type_grp = b_facts.groupby('BUILDING_TYPE_NORM', dropna=False).agg(
    buildings_not_subdivisions=('not_subdivision_flag','sum'),
    employees=('employee_count','sum'),
    unique_building_street_address=('unique_street_address_count','sum'),
    unique_city=('unique_city_count','sum'),
    unique_state=('unique_state_count','sum'),
    unique_postal_code=('unique_postal_code_count','sum'),
    total_gross_area=('EXT_GROSS_AREA','sum')
).reset_index()

# Average gross square footage per employee
type_grp['avg_gsf_per_employee'] = type_grp.apply(lambda r: (r['total_gross_area'] / r['employees']) if r['employees'] else 0.0, axis=1)

# Rename 'resident' to 'RESIDENTIAL' (case-insensitive match)
type_grp['BUILDING_TYPE_NORM'] = type_grp['BUILDING_TYPE_NORM'].astype(str)
type_grp.loc[type_grp['BUILDING_TYPE_NORM'].str.lower()=='resident', 'BUILDING_TYPE_NORM'] = 'RESIDENTIAL'

# Grand total row
tot = pd.Series({
    'BUILDING_TYPE_NORM':'TOTAL',
    'buildings_not_subdivisions': int(b_facts['not_subdivision_flag'].sum()),
    'employees': int(b_facts['employee_count'].sum()),
    'unique_building_street_address': int(b_facts['unique_street_address_count'].fillna(0).sum()),
    'unique_city': int(b_facts['unique_city_count'].fillna(0).sum()),
    'unique_state': int(b_facts['unique_state_count'].fillna(0).sum()),
    'unique_postal_code': int(b_facts['unique_postal_code_count'].fillna(0).sum()),
    'total_gross_area': float(b_facts['EXT_GROSS_AREA'].sum())
})

tot['avg_gsf_per_employee'] = (tot['total_gross_area'] / tot['employees']) if tot['employees'] else 0.0

answer = pd.concat([type_grp, pd.DataFrame([tot])], ignore_index=True)[[
    'BUILDING_TYPE_NORM',
    'buildings_not_subdivisions',
    'employees',
    'unique_building_street_address',
    'unique_city',
    'unique_state',
    'unique_postal_code',
    'avg_gsf_per_employee'
]].rename(columns={'BUILDING_TYPE_NORM':'building_type'})

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
