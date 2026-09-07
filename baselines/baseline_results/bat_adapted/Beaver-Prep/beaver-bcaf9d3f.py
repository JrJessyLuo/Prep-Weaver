import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['dlc_key','DLC_CODE','DLC_NAME']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['dlc_key','DLC_CODE','DLC_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['FCLT_ORGANIZATION_KEY','DLC_KEY']].copy()
    df = df.dropna(subset=['FCLT_ORGANIZATION_KEY','DLC_KEY'])
    df['FCLT_ORGANIZATION_KEY'] = df['FCLT_ORGANIZATION_KEY'].astype('int64')
    df['DLC_KEY'] = df['DLC_KEY'].astype(str)
    target = df.drop_duplicates(subset=['FCLT_ORGANIZATION_KEY','DLC_KEY']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['FCLT_ORGANIZATION_KEY','DLC_KEY']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['fclt_organization_key','DLC_KEY','SPACE_UNIT_KEY']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_dlc_master = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_orgs_by_dlc = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_org_dlc_lookup = prepared_table_3
prepared_table_4 = _prep_4(tables['table_9'])
prepared_space_units_by_dlc = prepared_table_4

# Assume prepared_dlc_master, prepared_orgs_by_dlc, prepared_org_dlc_lookup, prepared_space_units_by_dlc exist

# 1) Build organization-to-DLC mapping, preferring explicit DLC_KEYs from either source
org_dlc_from_t2 = prepared_orgs_by_dlc[['FCLT_ORGANIZATION_KEY','DLC_KEY']].dropna()
org_dlc_from_t3 = prepared_org_dlc_lookup[['FCLT_ORGANIZATION_KEY','DLC_KEY']].dropna()
org_dlc = pd.concat([org_dlc_from_t2, org_dlc_from_t3], ignore_index=True).drop_duplicates()

# 2) Count distinct facility organizations per DLC
org_counts = org_dlc.groupby('DLC_KEY', as_index=False).agg(total_facility_organizations=('FCLT_ORGANIZATION_KEY','nunique'))

# 3) Derive space-related aggregates if available (floors, sqft, heights not present in provided tables -> set to NaN/0 as placeholders)
# Link space units to DLC via organizations
su_link = prepared_space_units_by_dlc.merge(org_dlc, left_on='fclt_organization_key', right_on='FCLT_ORGANIZATION_KEY', how='left')
space_counts = su_link.groupby('DLC_KEY', as_index=False).agg(
    total_floors=('SPACE_UNIT_KEY', lambda s: pd.NA),
    total_square_footage=('SPACE_UNIT_KEY', lambda s: pd.NA),
    total_building_heights=('SPACE_UNIT_KEY', lambda s: pd.NA)
)

# 4) Supervisor/supervisee counts not present -> placeholders
people_counts = org_dlc[['DLC_KEY']].drop_duplicates().assign(
    total_supervisors=pd.NA,
    total_supervisees=pd.NA
)

# 5) Combine all per-DLC metrics
metrics = prepared_dlc_master.rename(columns={'dlc_key':'DLC_KEY'})[['DLC_KEY','DLC_NAME']].drop_duplicates() \
    .merge(org_counts, on='DLC_KEY', how='left') \
    .merge(space_counts, on='DLC_KEY', how='left') \
    .merge(people_counts, on='DLC_KEY', how='left')

# 6) Final selection/rename per question
answer = metrics.rename(columns={
    'DLC_KEY':'dlc_key',
    'DLC_NAME':'dlc_name'
})[['dlc_key','dlc_name','total_floors','total_square_footage','total_facility_organizations','total_supervisors','total_supervisees','total_building_heights']]

target = answer

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
