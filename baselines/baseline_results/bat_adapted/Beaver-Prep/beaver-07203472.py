import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['FCLT_BUILDING_KEY','BUILDING_NUMBER','PARENT_BUILDING_NUMBER','BUILDING_USE','EXT_GROSS_AREA']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','FCLT_ORGANIZATION_KEY','ORGANIZATION_NAME']].copy()
    prepared['FCLT_BUILDING_KEY'] = prepared['FCLT_BUILDING_KEY'].astype(str)
    prepared['FCLT_ORGANIZATION_KEY'] = prepared['FCLT_ORGANIZATION_KEY'].astype('Int64')
    prepared['ORGANIZATION_NAME'] = prepared['ORGANIZATION_NAME'].astype(str)
    target = prepared.drop_duplicates(subset=['FCLT_BUILDING_KEY','FCLT_ORGANIZATION_KEY','ORGANIZATION_NAME']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_6'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_rooms = prepared_table_2

# Assume prepared_buildings and prepared_rooms are available DataFrames from the per-table targets
bld = prepared_buildings.copy()
rooms = prepared_rooms.drop_duplicates()

# Exclude subdivisions: keep only buildings without a parent (null/NaN or empty)
bld_main = bld[bld['PARENT_BUILDING_NUMBER'].isna() | (bld['PARENT_BUILDING_NUMBER'].astype(str).str.strip() == 'nan') | (bld['PARENT_BUILDING_NUMBER'].astype(str).str.strip() == '')]

# Normalize numeric
bld_main['EXT_GROSS_AREA'] = pd.to_numeric(bld_main['EXT_GROSS_AREA'], errors='coerce').fillna(0)

# Join rooms to buildings to get orgs per building
br = bld_main[['FCLT_BUILDING_KEY','BUILDING_USE','EXT_GROSS_AREA']].merge(
    rooms[['FCLT_BUILDING_KEY','FCLT_ORGANIZATION_KEY']].dropna(subset=['FCLT_ORGANIZATION_KEY']).astype({'FCLT_ORGANIZATION_KEY': str}),
    on='FCLT_BUILDING_KEY', how='left'
)

# Compute per-building org counts
orgs_per_bld = br.groupby('FCLT_BUILDING_KEY')['FCLT_ORGANIZATION_KEY'].nunique(dropna=True).reset_index(name='unique_orgs')

bld_with_orgs = bld_main.merge(orgs_per_bld, on='FCLT_BUILDING_KEY', how='left')
bld_with_orgs['unique_orgs'] = bld_with_orgs['unique_orgs'].fillna(0).astype(int)

# Map building use type label: if use indicates residence, label as RESIDENTIAL
# Treat codes starting with 'RES' or equal to 'RES' (case-insensitive) as residential
use_series = bld_with_orgs['BUILDING_USE'].astype(str).str.upper().fillna('')
bld_with_orgs['USE_TYPE'] = use_series.where(~use_series.str.startswith('RES'), 'RESIDENTIAL')

# Aggregate by use type
agg = bld_with_orgs.groupby('USE_TYPE').agg(
    buildings=('FCLT_BUILDING_KEY','nunique'),
    gross_sqft=('EXT_GROSS_AREA','sum'),
    unique_orgs=('unique_orgs','sum')
).reset_index()

# Totals row across all types
total_row = pd.DataFrame({
    'USE_TYPE': ['TOTAL'],
    'buildings': [bld_with_orgs['FCLT_BUILDING_KEY'].nunique()],
    'gross_sqft': [bld_with_orgs['EXT_GROSS_AREA'].sum()],
    'unique_orgs': [bld_with_orgs['unique_orgs'].sum()]
})

result = pd.concat([agg, total_row], ignore_index=True)

# Round to integers and format with commas
for col in ['buildings','gross_sqft','unique_orgs']:
    result[col] = result[col].round(0).astype(int).map(lambda x: f"{x:,}")

# Final output
target = result[['USE_TYPE','buildings','gross_sqft','unique_orgs']].rename(columns={
    'USE_TYPE':'use_type',
    'buildings':'number_of_buildings',
    'gross_sqft':'total_gross_sqft',
    'unique_orgs':'number_of_organizations'
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
