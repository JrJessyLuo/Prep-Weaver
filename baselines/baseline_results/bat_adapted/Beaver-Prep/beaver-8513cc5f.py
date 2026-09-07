import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['FCLT_ORGANIZATION_KEY','ORGANIZATION_ID','ORGANIZATION','ORGANIZATION_NAME','ORGANIZATION_LEVEL','ORGANIZATION_NUMBER','DLC_KEY']].copy()
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
    prepared = table_1[['dlc_key','HIERARCHY_TYPE']].copy()
    prepared = prepared.drop_duplicates(subset=['dlc_key','HIERARCHY_TYPE'])
    target = prepared[['dlc_key','HIERARCHY_TYPE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    source = table_1.copy()
    source = source.replace({'nan': pd.NA, 'NaN': pd.NA, 'NAN': pd.NA})
    target = source[['DIRECTORY_ORG_UNIT_TITLE','EMERITUS_STATUS']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_orgs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_table_3 = _prep_3(tables['table_5'])
prepared_hierarchy = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
prepared_people = prepared_table_4

# Start from prepared tables
orgs = prepared_orgs.copy()
hier = prepared_hierarchy.copy()
people = prepared_people.copy()

# Join orgs to hierarchy via DLC key
merged = orgs.merge(hier, left_on='DLC_KEY', right_on='dlc_key', how='left')

# Derive emeritus membership per organization by matching people.DIRECTORY_ORG_UNIT_TITLE to org ORGANIZATION_NAME
# Flag people as emeritus/non-emeritus
people_flags = people.dropna(subset=['DIRECTORY_ORG_UNIT_TITLE']).copy()
people_flags['is_emeritus'] = people_flags['EMERITUS_STATUS'].fillna('').str.strip().str.lower().isin(['emeritus','emerita','emeritus/emerita','emeritus status'])

# Map directory titles to organization names using case-insensitive equality
# Build normalization for join
merged['_org_name_norm'] = merged['ORGANIZATION_NAME'].astype(str).str.strip().str.lower()
people_flags['_dir_name_norm'] = people_flags['DIRECTORY_ORG_UNIT_TITLE'].astype(str).str.strip().str.lower()

# Count members per org by emeritus flag
member_counts = (
    people_flags
    .groupby('_dir_name_norm')['is_emeritus']
    .value_counts(dropna=False)
    .unstack(fill_value=0)
    .reset_index()
)
# Ensure both columns exist
if True not in member_counts.columns:
    member_counts[True] = 0
if False not in member_counts.columns:
    member_counts[False] = 0
member_counts = member_counts.rename(columns={True: 'emeritus_count', False: 'non_emeritus_count'})

merged = merged.merge(member_counts, left_on='_org_name_norm', right_on='_dir_name_norm', how='left')
merged['emeritus_count'] = merged['emeritus_count'].fillna(0).astype(int)
merged['non_emeritus_count'] = merged['non_emeritus_count'].fillna(0).astype(int)

# Exclude organizations '139' and '250' (compare to ORGANIZATION_ID as strings)
result = merged[~merged['ORGANIZATION_ID'].astype(str).isin(['139','250'])].copy()

# Compute employer count totals per hierarchy type
result['EMPLOYER_COUNT'] = result['emeritus_count'] + result['non_emeritus_count']

totals = (
    result.groupby('HIERARCHY_TYPE', dropna=False)['EMPLOYER_COUNT']
    .sum()
    .reset_index()
    .rename(columns={'EMPLOYER_COUNT':'EMPLOYER_COUNT_TOTAL'})
)

result = result.merge(totals, on='HIERARCHY_TYPE', how='left')

# Prepare final projection and sorting by hierarchy type
final_cols = [
    'ORGANIZATION',            # break group (short code)
    'ORGANIZATION_ID',
    'ORGANIZATION_NAME',       # name
    'ORGANIZATION_NAME',       # formatted name according to its level (no special formatting available; using name)
    'HIERARCHY_TYPE',
    'ORGANIZATION_NUMBER',
    'ORGANIZATION_LEVEL',
    'emeritus_count',
    'non_emeritus_count',
    'EMPLOYER_COUNT',
    'EMPLOYER_COUNT_TOTAL'
]
final = result.sort_values(['HIERARCHY_TYPE', 'ORGANIZATION_NAME'], kind='mergesort')[final_cols].copy()

# Rename for clarity
final = final.rename(columns={
    'ORGANIZATION': 'BREAK_GROUP',
    'ORGANIZATION_NAME': 'ORGANIZATION_NAME',
    'ORGANIZATION_NUMBER': 'ORGANIZATION_NUMBER',
    'ORGANIZATION_LEVEL': 'ORGANIZATION_LEVEL'
})

target = final

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
