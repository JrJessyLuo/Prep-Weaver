import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['organization_key','ORGANIZATION_ID','ORGANIZATION_NUMBER','ORGANIZATION_LEVEL','ORGANIZATION_NAME','ASSIGNABLE']].copy()
    prepared = prepared.drop_duplicates(subset=['organization_key'])
    target = prepared[['organization_key','ORGANIZATION_ID','ORGANIZATION_NUMBER','ORGANIZATION_LEVEL','ORGANIZATION_NAME','ASSIGNABLE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared_rooms = table_1[['ORGANIZATION_KEY','AREA']].copy()
    prepared_rooms['AREA'] = pd.to_numeric(prepared_rooms['AREA'], errors='coerce')
    prepared_rooms['ORGANIZATION_KEY'] = pd.to_numeric(prepared_rooms['ORGANIZATION_KEY'], errors='coerce')
    prepared_rooms = prepared_rooms.dropna(subset=['ORGANIZATION_KEY','AREA'])
    target = prepared_rooms[['ORGANIZATION_KEY','AREA']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_orgs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_rooms = prepared_table_2

# prepared_orgs and prepared_rooms are the synthesized tables per the targets above

# Ensure numeric types for join and calculations
prepared_orgs['organization_key'] = pd.to_numeric(prepared_orgs['organization_key'], errors='coerce')
prepared_orgs['ORGANIZATION_ID'] = pd.to_numeric(prepared_orgs['ORGANIZATION_ID'], errors='coerce')
prepared_orgs['ORGANIZATION_NUMBER'] = pd.to_numeric(prepared_orgs['ORGANIZATION_NUMBER'], errors='coerce')
prepared_orgs['ORGANIZATION_LEVEL'] = pd.to_numeric(prepared_orgs['ORGANIZATION_LEVEL'], errors='coerce')
prepared_orgs['ASSIGNABLE'] = pd.to_numeric(prepared_orgs['ASSIGNABLE'], errors='coerce')

prepared_rooms['ORGANIZATION_KEY'] = pd.to_numeric(prepared_rooms['ORGANIZATION_KEY'], errors='coerce')
prepared_rooms['AREA'] = pd.to_numeric(prepared_rooms['AREA'], errors='coerce')

# Aggregate room metrics per organization
room_agg = prepared_rooms.groupby('ORGANIZATION_KEY', dropna=True).agg(
    total_area=('AREA', 'sum'),
    room_count=('AREA', 'count'),
    avg_area=('AREA', 'mean')
).reset_index().rename(columns={'ORGANIZATION_KEY': 'organization_key'})

# Join orgs with room aggregates (left join to keep orgs with zero rooms)
merged = prepared_orgs.merge(room_agg, on='organization_key', how='left')

# Fill NaNs for orgs with no rooms
merged['total_area'] = merged['total_area'].fillna(0)
merged['room_count'] = merged['room_count'].fillna(0)
merged['avg_area'] = merged.apply(lambda r: (r['total_area'] / r['room_count']) if r['room_count'] > 0 else 0, axis=1)

# Exclude Cambridge-MIT Institute by name
mask_cmi = merged['ORGANIZATION_NAME'].str.strip().str.casefold() == 'cambridge-mit institute'
result = merged.loc[~mask_cmi].copy()

# Format name with leading spaces based on level (levels 2..6 -> 1..5 spaces)
def fmt_name(row):
    lvl = int(row['ORGANIZATION_LEVEL']) if pd.notna(row['ORGANIZATION_LEVEL']) else None
    spaces = max(0, min(6, lvl) - 1) if lvl is not None else 0
    return (' ' * spaces) + str(row['ORGANIZATION_NAME'])

result['Formatted Name'] = result.apply(fmt_name, axis=1)

# Assignable label
result['Assignable Label'] = result['ASSIGNABLE'].apply(lambda x: 'ASSIGNABLE' if pd.notna(x) and int(x) == 1 else 'NON-ASSIGNABLE')

# Round and format numbers with commas
def fmt_int(x):
    try:
        return f"{int(round(float(x))):,}"
    except Exception:
        return ''

result['Total Area'] = result['total_area'].apply(fmt_int)
result['Number of Rooms'] = result['room_count'].apply(fmt_int)
result['Average Room Area'] = result['avg_area'].apply(fmt_int)

# Select and rename output columns
output = result[[
    'ORGANIZATION_ID',
    'ORGANIZATION_NUMBER',
    'ORGANIZATION_LEVEL',
    'Formatted Name',
    'Assignable Label',
    'Total Area',
    'Number of Rooms',
    'Average Room Area'
]].rename(columns={
    'ORGANIZATION_ID': 'Organization ID',
    'ORGANIZATION_NUMBER': 'Organization Number',
    'ORGANIZATION_LEVEL': 'Level'
})

# Final answer dataframe
target = output

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
