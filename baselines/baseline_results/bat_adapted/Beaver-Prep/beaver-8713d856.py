import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['MOIRA_LIST_OWNER_KEY','MOIRA_LIST_KEY','moira_list_member']].copy()
    prepared['moira_list_member'] = prepared['moira_list_member'].astype(str).str.strip()
    target = prepared[['MOIRA_LIST_OWNER_KEY','MOIRA_LIST_KEY','moira_list_member']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['MOIRA_LIST_OWNER_KEY','OWNER','OWNER_TYPE']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_memberships = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_owners = prepared_table_2

target = prepared_memberships.merge(prepared_owners, on='MOIRA_LIST_OWNER_KEY', how='inner')
filtered = target[target['MOIRA_LIST_OWNER_KEY'] == 'LIST69.377-keeper-xenon']
owner_name = filtered['OWNER'].dropna().iloc[0] if not filtered.empty else None
total_lists = filtered['MOIRA_LIST_KEY'].nunique()
total_members = filtered.shape[0]
answer = {'owner': owner_name, 'total_mailing_lists': int(total_lists), 'total_members': int(total_members)}

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
