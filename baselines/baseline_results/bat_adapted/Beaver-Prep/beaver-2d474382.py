import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','FLOOR']].copy()
    prepared = prepared.dropna(subset=['FCLT_BUILDING_KEY','FLOOR'])
    prepared['FCLT_BUILDING_KEY'] = prepared['FCLT_BUILDING_KEY'].astype(str)
    prepared['FLOOR'] = prepared['FLOOR'].astype(str)
    target = prepared.drop_duplicates(subset=['FCLT_BUILDING_KEY','FLOOR']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','BUILDING_NAME','BUILDING_NAME_LONG','BUILDING_NUMBER']].copy()
    prepared = prepared.drop_duplicates(subset=['FCLT_BUILDING_KEY'])
    target = prepared[['FCLT_BUILDING_KEY','BUILDING_NAME','BUILDING_NAME_LONG','BUILDING_NUMBER']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['MIT_ID','krb_name','KRB_NAME_UPPERCASE','OFFICE_LOCATION']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1.copy()
    df['MOIRA_LIST_KEY'] = df['MOIRA_LIST_KEY'].astype(str).str.strip()
    target = df[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_ACTIVE','IS_MOIRA_MAILING_LIST']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_9'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_people = prepared_table_3
prepared_table_4 = _prep_4(tables['table_6'])
prepared_moira_lists = prepared_table_4

# Inputs: prepared_rooms, prepared_buildings, prepared_people, prepared_moira_lists, and a memberships bridge table (people-to-lists)
# Assumptions for integration:
# - A memberships table named prepared_memberships exists with columns: MIT_ID, MOIRA_LIST_KEY (or MOIRA_LIST_NAME) linking people to lists.
#   If the bridge uses kerberos instead of MIT_ID, rename to MIT_ID via lookup on prepared_people.
# - OFFICE_LOCATION pattern like 'E94-1573D' -> building key 'E94' (substring before first '-')

# 1) Compute building with most distinct floors from rooms
rooms = prepared_rooms.copy()
rooms['FLOOR_NORM'] = rooms['FLOOR'].astype(str).str.strip().str.lower()
floors_per_bldg = rooms.dropna(subset=['FCLT_BUILDING_KEY', 'FLOOR_NORM']).groupby('FCLT_BUILDING_KEY')['FLOOR_NORM'].nunique().reset_index(name='num_floors')
max_bldg_key = floors_per_bldg.sort_values(['num_floors','FCLT_BUILDING_KEY'], ascending=[False, True]).head(1)['FCLT_BUILDING_KEY'].iloc[0]

# 2) Get building names
bldg_row = prepared_buildings[prepared_buildings['FCLT_BUILDING_KEY'] == max_bldg_key].head(1)
building_name = (bldg_row['BUILDING_NAME'].iloc[0]
                 if ('BUILDING_NAME' in bldg_row and pd.notna(bldg_row['BUILDING_NAME'].iloc[0]))
                 else (bldg_row['BUILDING_NAME_LONG'].iloc[0] if 'BUILDING_NAME_LONG' in bldg_row else max_bldg_key))

# 3) Identify employees in that building (by office location)
people = prepared_people.copy()
people['OFFICE_LOCATION'] = people['OFFICE_LOCATION'].astype(str)
people['OFFICE_BLDG_KEY'] = people['OFFICE_LOCATION'].str.split('-', n=1).str[0].str.strip()
# Some office locations may be lowercase like 'w98-299a'; normalize case to match building keys' case
people['OFFICE_BLDG_KEY_UP'] = people['OFFICE_BLDG_KEY'].str.upper()
max_bldg_key_up = str(max_bldg_key).upper()
people_in_bldg = people[people['OFFICE_BLDG_KEY_UP'] == max_bldg_key_up]

# 4) Filter people by kerberos starting with 'c' (case-insensitive)
people_in_bldg = people_in_bldg[people_in_bldg['krb_name'].astype(str).str.startswith(('c','C'))]

# 5) Memberships join to get lists they subscribe to
# Expect prepared_memberships with at least columns: MIT_ID and MOIRA_LIST_KEY (preferred) or MOIRA_LIST_NAME
m = prepared_memberships.copy()
# If memberships contain MOIRA_LIST_NAME instead of key, join on name; otherwise join on key
lists = prepared_moira_lists.copy()
# standardize list name case
lists['MOIRA_LIST_NAME_UP'] = lists['MOIRA_LIST_NAME'].astype(str).str.strip().str.upper()

if 'MOIRA_LIST_KEY' in m.columns and 'MOIRA_LIST_KEY' in lists.columns:
    merged = m.merge(lists[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_ACTIVE','IS_MOIRA_MAILING_LIST']], on='MOIRA_LIST_KEY', how='inner')
else:
    m['MOIRA_LIST_NAME_UP'] = m['MOIRA_LIST_NAME'].astype(str).str.strip().str.upper()
    merged = m.merge(lists[['MOIRA_LIST_NAME','MOIRA_LIST_NAME_UP','IS_ACTIVE','IS_MOIRA_MAILING_LIST']], on='MOIRA_LIST_NAME_UP', how='inner')

# 6) Filter to active Moira mailing lists whose names start with 'a' (case-insensitive)
merged = merged[(merged['IS_MOIRA_MAILING_LIST'] == 'Y') & (merged['IS_ACTIVE'] == 'Y')]
merged['MOIRA_LIST_NAME_LOW'] = merged['MOIRA_LIST_NAME'].astype(str).str.strip().str.lower()
merged = merged[merged['MOIRA_LIST_NAME_LOW'].str.startswith('a')]

# 7) Join people filter with memberships
people_cols = people_in_bldg[['MIT_ID','krb_name']].drop_duplicates()
subscribed = people_cols.merge(merged, on='MIT_ID', how='inner')

# 8) Prepare final answer: building name and list names (distinct)
result = subscribed[['MOIRA_LIST_NAME']].drop_duplicates().assign(BUILDING_NAME=building_name)
# Reorder columns
result = result[['BUILDING_NAME','MOIRA_LIST_NAME']]

answer = result

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
