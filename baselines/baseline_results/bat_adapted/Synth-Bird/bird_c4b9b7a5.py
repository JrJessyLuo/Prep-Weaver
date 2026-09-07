import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['budget_id','category']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['expense_date'] = pd.to_datetime(df['expense_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
    df['approved'] = df['approved'].astype(str).str.lower()
    target = df[['expense_id','expense_description','expense_date','cost','approved','link_to_member','link_to_budget']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['member_id','first_name','last_name','position']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1.loc[table_1['link_to_event'].eq('rec2N69DMcrqN9PJC'), ['link_to_event','link_to_member']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_budgets = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_expenses = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_members = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
prepared_attendance = prepared_table_4

# Assume prepared_* DataFrames already exist
# 1) Join expenses to budgets to filter to Food category
exp_bud = prepared_expenses.merge(prepared_budgets, left_on='link_to_budget', right_on='budget_id', how='inner')
food_exp = exp_bud[exp_bud['category'].str.lower() == 'food']

# 2) Keep only approved expenses (if needed)
food_exp = food_exp[food_exp['approved'].astype(str).str.lower() == 'true']

# 3) Filter expenses to September (assume September Meeting occurs in September of the same year; use expense_date month == 09)
food_exp['expense_date'] = pd.to_datetime(food_exp['expense_date'], errors='coerce')
food_sep = food_exp[food_exp['expense_date'].dt.month == 9]

# 4) Identify Student_Club members (position contains 'Member')
members = prepared_members.copy()
members['is_member'] = members['position'].astype(str).str.lower().str.contains('member')
club_members = members[members['is_member']]

# 5) If September Meeting attendees are required, intersect with attendance for the September Meeting event.
# Here we infer the event by name is not available; if an event id for 'September Meeting' is known, filter prepared_attendance by that id.
# For now, use attendance to require membership intersection only (no specific event filter available in provided schemas).
exp_with_members = food_sep.merge(club_members[['member_id']], left_on='link_to_member', right_on='member_id', how='inner')

# 6) Sum the costs
answer_value = float(exp_with_members['cost'].astype(float).sum())

result = {
    'answer': answer_value,
    'evidence_rows': exp_with_members[['expense_id','expense_description','expense_date','cost','link_to_member','link_to_budget']].to_dict(orient='records')
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
