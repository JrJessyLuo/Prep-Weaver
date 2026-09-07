import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_MEMBER_MIT_ID','moira_list_member','MOIRA_LIST_MEMBER_FULL_NAME']].copy()
    target['moira_list_member'] = target['moira_list_member'].astype('string').str.strip()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['MIT_ID','KRB_NAME','KRB_NAME_UPPERCASE','OFFICE_LOCATION']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['BUILDING_NUMBER','BUILDING_NAME']].copy()
    prepared['BUILDING_NUMBER'] = prepared['BUILDING_NUMBER'].astype(str)
    prepared['BUILDING_NAME'] = prepared['BUILDING_NAME'].astype(str)
    prepared = prepared.drop_duplicates(subset=['BUILDING_NUMBER','BUILDING_NAME']).reset_index(drop=True)
    target = prepared[['BUILDING_NUMBER','BUILDING_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_mailing_list_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_people_offices = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_buildings = prepared_table_3

ml = prepared_mailing_list_members.copy()
people = prepared_people_offices.copy()

# Normalize keys
# MIT IDs
ml['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(ml['MOIRA_LIST_MEMBER_MIT_ID'], errors='coerce').astype('Int64')
people['MIT_ID'] = pd.to_numeric(people['MIT_ID'], errors='coerce').astype('Int64')

# Kerberos usernames: strip and uppercase in ml; ensure people has uppercase variant
ml['KRB_FROM_MEMBER'] = ml['moira_list_member'].astype(str).str.strip().str.upper()
people['KRB_NAME_UPPERCASE'] = people['KRB_NAME_UPPERCASE'].astype(str).str.strip()

# Build two linkage paths and union them to maximize matches
join_on_mit = ml.merge(people[['MIT_ID','OFFICE_LOCATION']], left_on='MOIRA_LIST_MEMBER_MIT_ID', right_on='MIT_ID', how='inner')
join_on_krb = ml.merge(people[['KRB_NAME_UPPERCASE','OFFICE_LOCATION']], left_on='KRB_FROM_MEMBER', right_on='KRB_NAME_UPPERCASE', how='inner')

# Standardize columns
join_on_mit = join_on_mit[['MOIRA_LIST_KEY','OFFICE_LOCATION']]
join_on_krb = join_on_krb[['MOIRA_LIST_KEY','OFFICE_LOCATION']]

joined = pd.concat([join_on_mit, join_on_krb], ignore_index=True).drop_duplicates()

# Filter to people with physical offices in building 24
# Assume office codes like '24-xxx' or '24xxx'; match starting with '24' followed by '-' or a digit
mask_b24 = joined['OFFICE_LOCATION'].astype(str).str.match(r'^\s*24(\-|\d)')
joined_b24 = joined[mask_b24]

# Count subscribers per mailing list among building 24 occupants
counts = joined_b24.groupby('MOIRA_LIST_KEY', as_index=False).size().rename(columns={'size':'subscriber_count'})

# Identify the most subscribed list and its count
if counts.empty:
    result = pd.DataFrame([{'mailing_list': None, 'subscriber_count': 0}])
else:
    top = counts.sort_values(['subscriber_count','MOIRA_LIST_KEY'], ascending=[False, True]).head(1)
    result = top.rename(columns={'MOIRA_LIST_KEY':'mailing_list'})[['mailing_list','subscriber_count']]

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
