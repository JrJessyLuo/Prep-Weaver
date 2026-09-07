import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['MOIRA_LIST_OWNER_KEY','OWNER','OWNER_TYPE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_MOIRA_MAILING_LIST','IS_PUBLIC','IS_HIDDEN']].copy()
    df['MOIRA_LIST_KEY'] = df['MOIRA_LIST_KEY'].astype(str).str.strip()
    target = df[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_MOIRA_MAILING_LIST','IS_PUBLIC','IS_HIDDEN']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY','moira_list_member']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_list_owners = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_lists = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_memberships = prepared_table_3

# Assume prepared_* DataFrames already exist as per target schemas
# Normalize keys (e.g., strip spaces) for robust joins
prepared_lists = prepared_lists.assign(MOIRA_LIST_KEY=prepared_lists['MOIRA_LIST_KEY'].astype(str).str.strip())
prepared_memberships = prepared_memberships.assign(MOIRA_LIST_KEY=prepared_memberships['MOIRA_LIST_KEY'].astype(str).str.strip())

# Join memberships to owners
m_with_owner = prepared_memberships.merge(
    prepared_list_owners, how='left', on='MOIRA_LIST_OWNER_KEY'
)

# Join list visibility
m_full = m_with_owner.merge(
    prepared_lists[['MOIRA_LIST_KEY','IS_MOIRA_MAILING_LIST','IS_PUBLIC','IS_HIDDEN']],
    how='left', on='MOIRA_LIST_KEY'
)

# Keep only mailing lists
m_full = m_full[m_full['IS_MOIRA_MAILING_LIST'] == 'Y'].copy()

# Derive member visibility label per list
m_full['member_visibility'] = pd.Series(
    ['Public Members' if x == 'Y' else 'Hidden Members' for x in m_full['IS_PUBLIC']]
)

# Count members per list and visibility
per_list = (
    m_full.groupby(['MOIRA_LIST_KEY','OWNER','OWNER_TYPE','member_visibility'], dropna=False)['moira_list_member']
    .nunique()
    .reset_index(name='member_count')
)

# Build grand totals per (owner, owner type) across all their lists/members
grand_totals = (
    m_full.groupby(['OWNER','OWNER_TYPE'], dropna=False)['moira_list_member']
    .nunique()
    .reset_index(name='member_count')
)
grand_totals['MOIRA_LIST_KEY'] = pd.NA
grand_totals['member_visibility'] = pd.NA

# Align columns and concatenate
per_list_out = per_list[['MOIRA_LIST_KEY','OWNER','OWNER_TYPE','member_visibility','member_count']]
grand_out = grand_totals[['MOIRA_LIST_KEY','OWNER','OWNER_TYPE','member_visibility','member_count']]

result = pd.concat([per_list_out, grand_out], ignore_index=True)

# Final columns per question
target = result.rename(columns={
    'MOIRA_LIST_KEY': 'mailing_list',
    'OWNER': 'owner',
    'OWNER_TYPE': 'owner_type',
    'member_visibility': 'member_visibility',
    'member_count': 'members'
})

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
