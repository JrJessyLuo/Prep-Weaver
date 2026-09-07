import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_MOIRA_MAILING_LIST','IS_ACTIVE']].copy()
    prepared['MOIRA_LIST_KEY'] = prepared['MOIRA_LIST_KEY'].astype(str).str.strip()
    target = prepared[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_MOIRA_MAILING_LIST','IS_ACTIVE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY','moira_list_member','MOIRA_LIST_MEMBER_FULL_NAME','MOIRA_LIST_MEMBER_MIT_ID']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['MOIRA_LIST_OWNER_KEY','OWNER','OWNER_TYPE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['FULL_NAME','FULL_NAME_UPPERCASE','EMAIL_ADDRESS','DEPARTMENT_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_10'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_memberships = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_owners = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_people = prepared_table_4

# Assume prepared_* DataFrames already created per table_targets
lists = prepared_lists.copy()
members = prepared_memberships.copy()
owners = prepared_owners.copy()
people = prepared_people.copy()

# Normalize keys/identifiers
for df,col in [(lists,'MOIRA_LIST_NAME'), (lists,'MOIRA_LIST_KEY'), (members,'MOIRA_LIST_KEY'), (members,'MOIRA_LIST_OWNER_KEY'), (members,'moira_list_member')]:
    df[col] = df[col].astype(str).str.strip()
people['EMAIL_ADDRESS'] = people['EMAIL_ADDRESS'].astype(str).str.strip().str.lower()
people['FULL_NAME_UPPERCASE'] = people['FULL_NAME_UPPERCASE'].astype(str).str.strip()

# Filter to active mailing lists whose names start with 'e' (case-insensitive)
lists_f = lists[(lists['IS_ACTIVE'].str.upper() == 'Y') & (lists['IS_MOIRA_MAILING_LIST'].str.upper() == 'Y')]
lists_f = lists_f[lists_f['MOIRA_LIST_NAME'].str.lower().str.startswith('e')]

# Join members to those lists
lm = members.merge(lists_f[['MOIRA_LIST_KEY','MOIRA_LIST_NAME']], on='MOIRA_LIST_KEY', how='inner')

# Try to map members to people by email address first (moira_list_member often stores login/email). Normalize member as email-like
lm['member_norm'] = lm['moira_list_member'].astype(str).str.strip().str.lower()
# Left join to people on email
lm_people = lm.merge(people[['EMAIL_ADDRESS','DEPARTMENT_NAME']], left_on='member_norm', right_on='EMAIL_ADDRESS', how='left')

# If email match missing, optionally try a heuristic name match using FULL_NAME vs MOIRA_LIST_MEMBER_FULL_NAME uppercase
# Prepare name keys
people_name = people[['FULL_NAME_UPPERCASE','DEPARTMENT_NAME']].dropna().copy()
people_name.rename(columns={'FULL_NAME_UPPERCASE':'NAME_KEY','DEPARTMENT_NAME':'DEPT_FROM_NAME'}, inplace=True)
name_key = lm['MOIRA_LIST_MEMBER_FULL_NAME'].astype(str).str.strip().str.upper()
lm_people['NAME_KEY'] = name_key
# Name-based enrichment
lm_people = lm_people.merge(people_name, on='NAME_KEY', how='left')

# Determine if member is CS/EECS student: treat DEPARTMENT_NAME containing 'Computer Sci' or 'Electrical Eng & Computer Sci' as CS
def is_cs(dept):
    if not isinstance(dept, str):
        return False
    d = dept.lower()
    return ('computer sci' in d) or ('electrical eng & computer sci' in d) or ('electrical eng and computer sci' in d) or ('eecs' in d)

cs_flag_email = lm_people['DEPARTMENT_NAME'].apply(is_cs)
cs_flag_name = lm_people['DEPT_FROM_NAME'].apply(is_cs)
lm_people['is_cs'] = cs_flag_email | cs_flag_name

# Aggregate per list: member count and cs count
agg = lm_people.groupby(['MOIRA_LIST_KEY','MOIRA_LIST_NAME'], as_index=False).agg(
    member_count=('moira_list_member','count'),
    cs_count=('is_cs','sum')
)
agg['cs_ratio'] = agg['cs_count'] / agg['member_count']

# Keep lists with member count between 10 and 20 inclusive and cs_ratio > 0.75
eligible = agg[(agg['member_count'].between(10,20, inclusive='both')) & (agg['cs_ratio'] > 0.75)]

# Attach owner
owners_f = owners[['MOIRA_LIST_OWNER_KEY','OWNER']].drop_duplicates()
# Need one owner per list: take the most common owner per list in memberships subset
list_owner = members[members['MOIRA_LIST_KEY'].isin(eligible['MOIRA_LIST_KEY'])]
list_owner = list_owner[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY']].dropna()
# Select first owner per list (or mode if desired)
list_owner = list_owner.groupby('MOIRA_LIST_KEY', as_index=False).agg(MOIRA_LIST_OWNER_KEY=('MOIRA_LIST_OWNER_KEY','first'))
list_owner = list_owner.merge(owners_f, on='MOIRA_LIST_OWNER_KEY', how='left')

result = eligible.merge(list_owner[['MOIRA_LIST_KEY','OWNER']], on='MOIRA_LIST_KEY', how='left')

# Final output: list name, owner, member count
answer = result[['MOIRA_LIST_NAME','OWNER','member_count']].rename(columns={
    'MOIRA_LIST_NAME':'list_name',
    'OWNER':'owner',
    'member_count':'member_count'
}).sort_values(['list_name'])

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
