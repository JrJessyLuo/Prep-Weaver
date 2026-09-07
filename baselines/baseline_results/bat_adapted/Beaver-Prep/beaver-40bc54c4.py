import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(df['ROOM_SQUARE_FOOTAGE'], errors='coerce')
    target = df[['BUILDING_KEY','FLOOR_KEY','BUILDING_COMPONENT','BUILDING_ROOM','BUILDING_ROOM_NAME','ROOM_NUMBER','ROOM_SQUARE_FOOTAGE','ROOM_COUNTER']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BLDG_GROSS_SQUARE_FOOTAGE','BLDG_ASSIGNABLE_SQUARE_FOOTAGE','BUILDING_COUNTER']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','NUM_OF_ROOMS']].copy()
    df['NUM_OF_ROOMS'] = pd.to_numeric(df['NUM_OF_ROOMS'], errors='coerce').fillna(0).astype(int)
    target = df.groupby(['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME'], as_index=False)['NUM_OF_ROOMS'].sum()
    target = target[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','NUM_OF_ROOMS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['FCLT_BUILDING_KEY','BUILDING_ROOM','FCLT_FLOOR_KEY','FCLT_ORGANIZATION_KEY','ORGANIZATION_NAME','FCLT_ROOM_KEY']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
rooms_by_component = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
building_directory = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
building_summary = prepared_table_3
prepared_table_4 = _prep_4(tables['table_5'])
room_orgs = prepared_table_4

# Assume prepared DataFrames: rooms_by_component, building_directory, building_summary, room_orgs

# 1) Enrich building_directory with total rooms (building level)
bldg_dir_enriched = building_directory.merge(
    building_summary[['BUILDING_NUMBER', 'NUM_OF_ROOMS']],
    on='BUILDING_NUMBER', how='left'
)

# 2) Join room/component facts to building directory on BUILDING_KEY to get building name
rooms_enriched = rooms_by_component.merge(
    bldg_dir_enriched[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','NUM_OF_ROOMS']],
    on='BUILDING_KEY', how='left'
)

# 3) Link room_orgs to rooms via BUILDING_ROOM to attribute organizations to components
room_orgs_linked = room_orgs.merge(
    rooms_enriched[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_COMPONENT','BUILDING_ROOM']],
    on='BUILDING_ROOM', how='inner'
)

# 4) Compute per-building-component metrics
# - Square footage for all rooms: sum ROOM_SQUARE_FOOTAGE per component
# - Total number of floors: count distinct FLOOR_KEY per component
# - Total number of rooms: count distinct BUILDING_ROOM (or sum ROOM_COUNTER if unique)
# - Total number of facility organizations: count distinct FCLT_ORGANIZATION_KEY per component
# Note: Supervisors/supervisees not present in selected tables; will return nulls

# Ensure numeric
rooms_enriched['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(rooms_enriched['ROOM_SQUARE_FOOTAGE'], errors='coerce')

component_agg = (
    rooms_enriched.groupby(['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_COMPONENT'])
    .agg(
        total_room_sqft = ('ROOM_SQUARE_FOOTAGE','sum'),
        total_floors = ('FLOOR_KEY', pd.Series.nunique),
        total_rooms = ('BUILDING_ROOM', pd.Series.nunique)
    )
    .reset_index()
)

org_agg = (
    room_orgs_linked.groupby(['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_COMPONENT'])
    .agg(total_facility_organizations = ('FCLT_ORGANIZATION_KEY', pd.Series.nunique))
    .reset_index()
)

result = component_agg.merge(org_agg,
                             on=['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_COMPONENT'],
                             how='left')

# Supervisors and supervisees placeholders (no data available in provided tables)
result['total_supervisors'] = pd.NA
result['total_supervisees'] = pd.NA

# Select and rename columns to match the question
answer = result[[
    'BUILDING_COMPONENT',
    'BUILDING_NAME',
    'total_room_sqft',
    'total_floors',
    'total_rooms',
    'total_facility_organizations',
    'total_supervisors',
    'total_supervisees'
]].sort_values(['BUILDING_NAME','BUILDING_COMPONENT'])

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
