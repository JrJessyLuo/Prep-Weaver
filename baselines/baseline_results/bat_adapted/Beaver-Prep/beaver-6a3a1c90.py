import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_ACTIVE','IS_MOIRA_MAILING_LIST']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['moira_list_member'] = df['moira_list_member'].astype(str).str.strip()
    target = df[['MOIRA_LIST_KEY','MOIRA_LIST_MEMBER_MIT_ID','MOIRA_LIST_MEMBER_FULL_NAME','moira_list_member']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['MIT_ID','IS_FACULTY','PERSONNEL_SUBAREA','PERSONNEL_SUBAREA_CODE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_members = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_people = prepared_table_3

# Assume prepared_lists, prepared_members, prepared_people are pre-synthesized per targets above

# Join members to people by MIT_ID to get role flags
m_with_people = prepared_members.merge(
    prepared_people, how='left', left_on='MOIRA_LIST_MEMBER_MIT_ID', right_on='MIT_ID'
)

# Define role flags
# Faculty: IS_FACULTY == 'Y'
# Support staff: treat non-faculty staff via personnel subarea fields when available
m_with_people['is_faculty'] = (m_with_people['IS_FACULTY'] == 'Y')
# Heuristic: support staff if not faculty and personnel subarea/code present (non-null/non-empty)
ps_present = m_with_people['PERSONNEL_SUBAREA'].notna() | m_with_people['PERSONNEL_SUBAREA_CODE'].notna()
m_with_people['is_support'] = (~m_with_people['is_faculty']) & ps_present

# Keep only members that are either support staff or faculty for list selection
eligible_lists = m_with_people.loc[m_with_people['is_faculty'] | m_with_people['is_support'], ['MOIRA_LIST_KEY']].drop_duplicates()

# Join lists to eligible list keys
lists_eligible = prepared_lists.merge(eligible_lists, on='MOIRA_LIST_KEY', how='inner')

# Now compute per-list counts of faculty and support staff using only members in those roles
role_counts = m_with_people.loc[m_with_people['MOIRA_LIST_KEY'].isin(lists_eligible['MOIRA_LIST_KEY'])]
agg = role_counts.groupby('MOIRA_LIST_KEY').agg(
    num_support_staff=('is_support', 'sum'),
    num_faculty=('is_faculty', 'sum')
).reset_index()

# Final join to get list name and active status
result = lists_eligible.merge(agg, on='MOIRA_LIST_KEY', how='left')

# Select and rename columns
result = result[['MOIRA_LIST_NAME', 'num_support_staff', 'num_faculty', 'IS_ACTIVE']].sort_values('MOIRA_LIST_NAME')

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
