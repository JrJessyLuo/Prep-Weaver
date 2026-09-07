import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.copy()
    prepared['MOIRA_LIST_KEY'] = prepared['MOIRA_LIST_KEY'].astype(str).str.strip()
    target = prepared[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_PUBLIC','IS_HIDDEN','IS_MOIRA_MAILING_LIST','IS_ACTIVE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    source = table_1.copy()
    source['moira_list_member'] = source['moira_list_member'].astype(str).str.strip()
    target = source[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY','moira_list_member']]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_memberships = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_owners = prepared_table_3

# Start from prepared tables
lists = prepared_lists.copy()
memberships = prepared_memberships.copy()
owners = prepared_owners.copy()

# Filter to active Moira mailing lists
lists_f = lists[(lists['IS_MOIRA_MAILING_LIST'] == 'Y') & (lists['IS_ACTIVE'] == 'Y')]

# Join memberships to lists to scope members to valid lists
mem_lists = memberships.merge(lists_f, on='MOIRA_LIST_KEY', how='inner')

# Compute member counts per list (count distinct member ids to be robust)
member_counts = (mem_lists.dropna(subset=['moira_list_member'])
                          .groupby('MOIRA_LIST_KEY', as_index=False)
                          .agg(NUM_MEMBERS=('moira_list_member', 'nunique')))

# Join counts and list attributes back
list_with_counts = lists_f.merge(member_counts, on='MOIRA_LIST_KEY', how='left')
list_with_counts['NUM_MEMBERS'] = list_with_counts['NUM_MEMBERS'].fillna(0).astype(int)

# Find global min and max member counts
min_count = list_with_counts['NUM_MEMBERS'].min()
max_count = list_with_counts['NUM_MEMBERS'].max()

extreme_lists = list_with_counts[list_with_counts['NUM_MEMBERS'].isin([min_count, max_count])]

# Attach owners (multiple owners -> multiple rows)
extreme_with_owner = extreme_lists.merge(memberships[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY']].drop_duplicates(),
                                         on='MOIRA_LIST_KEY', how='left')\
                                  .merge(owners, on='MOIRA_LIST_OWNER_KEY', how='left')

# Prepare final output columns
result = extreme_with_owner[['MOIRA_LIST_NAME','OWNER','OWNER_TYPE','IS_PUBLIC','IS_HIDDEN','NUM_MEMBERS']].rename(columns={
    'MOIRA_LIST_NAME':'list_name',
    'OWNER':'owner',
    'OWNER_TYPE':'owner_type',
    'IS_PUBLIC':'is_public',
    'IS_HIDDEN':'is_hidden',
    'NUM_MEMBERS':'num_members'
}).sort_values(['num_members','list_name','owner'], ascending=[True, True, True])

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
