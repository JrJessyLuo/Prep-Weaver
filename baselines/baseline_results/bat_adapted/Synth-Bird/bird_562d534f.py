import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['event_id','event_name']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['budget_id','link_to_event']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['expense_id','link_to_budget','link_to_member']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['member_id','first_name','last_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
events = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
budgets = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
expenses = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
members = prepared_table_4

events_f = events[['event_id','event_name']]
budgets_f = budgets[['budget_id','link_to_event']]
expenses_f = expenses[['expense_id','link_to_budget','link_to_member']]
members_f = members[['member_id','first_name','last_name']]

# Join budgets to events to get event context
be = budgets_f.merge(events_f, left_on='link_to_event', right_on='event_id', how='inner')
# Filter to the specific event name
be_lol = be[be['event_name'] == 'Laugh Out Loud']
# Join expenses to the filtered budgets (proxy for attendance via member involvement)
exp_for_event = expenses_f.merge(be_lol[['budget_id']], left_on='link_to_budget', right_on='budget_id', how='inner')
# Map to members and construct full names
member_hits = exp_for_event.merge(members_f, left_on='link_to_member', right_on='member_id', how='inner')
member_hits['full_name'] = member_hits['first_name'] + ' ' + member_hits['last_name']
# Deduplicate names
answer = sorted(member_hits['full_name'].dropna().unique().tolist())
print(answer)

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
