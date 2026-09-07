import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['BUILDING_KEY','FLOOR_KEY','SPACE_UNIT_KEY','SPACE_USAGE_KEY','BUILDING_ROOM','BUILDING_ROOM_NAME','ROOM_NUMBER']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['BUILDING_KEY','FLOOR_KEY','SPACE_UNIT_KEY','SPACE_USAGE_KEY','BUILDING_ROOM','BUILDING_ROOM_NAME','ROOM_NUMBER']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_STREET_ADDRESS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    df['FLOOR_KEY'] = df['FLOOR_KEY'].astype(str).str.strip()
    df['FLOOR'] = df['FLOOR'].astype(str).str.strip()
    df['FLOOR_NAME'] = df['FLOOR_NAME'].astype(str).str.strip()
    df = df.drop_duplicates(subset=['FLOOR_KEY'], keep='first')
    target = df[['FLOOR_KEY','FLOOR','FLOOR_NAME']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1[['space_usage_key','SPACE_USAGE']].copy()
    df = df[df['SPACE_USAGE'].notna()]
    df['space_usage_key'] = pd.to_numeric(df['space_usage_key'], errors='coerce').astype('Int64')
    df = df[df['space_usage_key'].notna()]
    df['space_usage_key'] = df['space_usage_key'].astype('int64')
    target = df[['space_usage_key','SPACE_USAGE']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_5(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_6(table_1):
    prepared = table_1[['BUILDING_KEY','FLOOR_KEY','ROOM','ORGANIZATION_KEY','ORGANIZATION_NAME']].copy()
    prepared = prepared.dropna(subset=['BUILDING_KEY','FLOOR_KEY','ROOM','ORGANIZATION_KEY','ORGANIZATION_NAME'])
    prepared = prepared.drop_duplicates(subset=['BUILDING_KEY','FLOOR_KEY','ROOM','ORGANIZATION_KEY','ORGANIZATION_NAME'])
    target = prepared[['BUILDING_KEY','FLOOR_KEY','ROOM','ORGANIZATION_KEY','ORGANIZATION_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_space_units = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_floors = prepared_table_3
prepared_table_4 = _prep_4(tables['table_10'])
prepared_space_usage = prepared_table_4
prepared_table_5 = _prep_5(tables['table_6'])
prepared_table_6 = _prep_6(tables['table_5'])
prepared_org_rooms = prepared_table_6

# Assume prepared_* dataframes exist per targets.
sp = prepared_space_units.copy()
# Normalize key types/whitespace for robust joins
sp['BUILDING_KEY'] = sp['BUILDING_KEY'].astype(str).str.strip()
sp['FLOOR_KEY'] = sp['FLOOR_KEY'].astype(str).str.strip()
sp['SPACE_USAGE_KEY'] = sp['SPACE_USAGE_KEY'].astype(str).str.strip()

bldg = prepared_buildings.copy()
bldg['BUILDING_KEY'] = bldg['BUILDING_KEY'].astype(str).str.strip()

fl = prepared_floors.copy()
fl['FLOOR_KEY'] = fl['FLOOR_KEY'].astype(str).str.strip()

su = prepared_space_usage.copy()
su['space_usage_key'] = su['space_usage_key'].astype(str).str.strip()

org = prepared_org_rooms.copy()
org['BUILDING_KEY'] = org['BUILDING_KEY'].astype(str).str.strip()
org['FLOOR_KEY'] = org['FLOOR_KEY'].astype(str).str.strip()
org['ROOM'] = org['ROOM'].astype(str).str.strip()

# Filter to building 36 using building number/name from buildings table, joining first to find BUILDING_KEY of number '36'
# If BUILDING_NUMBER holds the canonical building identifier like '36', match on that; otherwise assume BUILDING_KEY equals that identifier.
# Create a building selector for '36' in either key or number.
bldg_sel_keys = set(bldg.loc[(bldg['BUILDING_NUMBER'].astype(str).str.strip()=='36') | (bldg['BUILDING_KEY'].astype(str).str.strip()=='36'), 'BUILDING_KEY'].astype(str).str.strip())
if len(bldg_sel_keys)==0:
    # Fallback: use raw '36'
    bldg_sel_keys = {'36'}

sp36 = sp[sp['BUILDING_KEY'].isin(bldg_sel_keys)].copy()

# Join building info
sp36 = sp36.merge(bldg[['BUILDING_KEY','BUILDING_NAME','BUILDING_STREET_ADDRESS']], on='BUILDING_KEY', how='left')

# Join floor info
sp36 = sp36.merge(fl[['FLOOR_KEY','FLOOR','FLOOR_NAME']], on='FLOOR_KEY', how='left')

# Join space usage
sp36 = sp36.merge(su.rename(columns={'space_usage_key':'SPACE_USAGE_KEY'}), on='SPACE_USAGE_KEY', how='left')

# Prepare org aggregation by building+floor
org_bf = org[org['BUILDING_KEY'].isin(bldg_sel_keys)].copy()
# Distinct organizations per building-floor
org_counts = (org_bf.dropna(subset=['ORGANIZATION_KEY'])
                 .groupby(['BUILDING_KEY','FLOOR_KEY'])['ORGANIZATION_KEY']
                 .nunique()
                 .reset_index(name='num_organizations_on_floor'))

# Space unit counts per building-floor from sp table
su_counts = (sp36.groupby(['BUILDING_KEY','FLOOR_KEY'])['SPACE_UNIT_KEY']
                 .nunique()
                 .reset_index(name='num_space_units_on_floor'))

# Attach counts to each space unit row
sp36 = sp36.merge(org_counts, on=['BUILDING_KEY','FLOOR_KEY'], how='left')
sp36 = sp36.merge(su_counts, on=['BUILDING_KEY','FLOOR_KEY'], how='left')

# Final selection of columns
target = sp36[['SPACE_UNIT_KEY', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER', 'FLOOR', 'FLOOR_NAME', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'SPACE_USAGE', 'num_organizations_on_floor', 'num_space_units_on_floor']]

# target now contains all space units in building 36 with required fields and counts

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
