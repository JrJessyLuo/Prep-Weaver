import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['moira_list_member'] = df['moira_list_member'].astype('string').str.strip()
    df = df[df['MOIRA_LIST_KEY'].astype('string').str.upper().str.startswith('B')]
    target = df[['MOIRA_LIST_KEY','moira_list_member','MOIRA_LIST_MEMBER_MIT_ID']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['MIT_ID','DEPARTMENT_NAME','krb_name','KRB_NAME_UPPERCASE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_mailing_list_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_people_directory = prepared_table_2

# Start from prepared tables
ml = prepared_mailing_list_members.copy()
dir = prepared_people_directory.copy()

# Normalize keys for joining
# MIT IDs in ml are float-like strings (e.g., '984301411.0'); convert to string ints
ml_id = ml['MOIRA_LIST_MEMBER_MIT_ID'].astype(str).str.replace('.0$', '', regex=True).str.strip()
dir_id = dir['MIT_ID'].astype(str).str.strip()

# Normalize kerberos names: strip and uppercase
ml_krb = ml['moira_list_member'].astype(str).str.strip().str.upper()
dir_krb = dir['KRB_NAME_UPPERCASE'].astype(str).str.strip()

ml_norm = ml.assign(_MIT_ID_NORM=ml_id, _KRB_NORM=ml_krb)
dir_norm = dir.assign(_MIT_ID_NORM=dir_id, _KRB_NORM=dir_krb)

# Left join by MIT_ID first
joined_id = ml_norm.merge(
    dir_norm[['MIT_ID','DEPARTMENT_NAME','_MIT_ID_NORM']],
    how='left', left_on='_MIT_ID_NORM', right_on='_MIT_ID_NORM', suffixes=('', '_dir')
)

# Rows not matched on MIT_ID
unmatched = joined_id[joined_id['DEPARTMENT_NAME'].isna()].copy()
matched = joined_id[~joined_id['DEPARTMENT_NAME'].isna()].copy()

# Attempt secondary join on kerberos for the unmatched subset
if not unmatched.empty:
    unmatched2 = unmatched.drop(columns=['DEPARTMENT_NAME'], errors='ignore').merge(
        dir_norm[['KRB_NAME_UPPERCASE','DEPARTMENT_NAME','_KRB_NORM']],
        how='left', left_on='_KRB_NORM', right_on='_KRB_NORM', suffixes=('', '_krb')
    )
    rejoined = pd.concat([matched, unmatched2], ignore_index=True)
else:
    rejoined = matched

# Filter to EECS department members
eecs_mask = rejoined['DEPARTMENT_NAME'].astype(str).str.contains('Electrical Engineering and Computer Science', case=False, na=False)
eecs_members = rejoined[eecs_mask].copy()

# Consider only lists whose names start with 'B' (case-insensitive)
b_mask = eecs_members['MOIRA_LIST_KEY'].astype(str).str.startswith(('B','b'), na=False)
eecs_b = eecs_members[b_mask].copy()

# Compute outputs
# 1) Count of distinct mailing lists with at least one EECS member
count_lists = eecs_b['MOIRA_LIST_KEY'].nunique()

# 2) List starting with B that has the highest number of EECS members and that count
list_counts = eecs_b.groupby('MOIRA_LIST_KEY', dropna=False).size().reset_index(name='eecs_member_count')
if list_counts.empty:
    top_list_name = None
    top_member_count = 0
else:
    top_row = list_counts.sort_values(['eecs_member_count','MOIRA_LIST_KEY'], ascending=[False, True]).iloc[0]
    top_list_name = top_row['MOIRA_LIST_KEY']
    top_member_count = int(top_row['eecs_member_count'])

answer = {
    'count_mailing_lists_starting_B_with_EECS_members': int(count_lists),
    'list_with_max_EECS_members_starting_B': top_list_name,
    'max_EECS_member_count_in_that_list': top_member_count
}

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
