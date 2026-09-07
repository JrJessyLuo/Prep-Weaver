import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['expense_id','expense_date','cost','items','link_to_budget']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['link_to_event','budget_id_prefix','budget_id_suffix']]
    df = df.dropna(subset=['link_to_event','budget_id_prefix','budget_id_suffix'])
    df = df.drop_duplicates()
    target = df[['link_to_event','budget_id_prefix','budget_id_suffix']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_expenses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_event_budgets = prepared_table_2

# Join prepared tables by reconstructing the budget id on the right side
prepared_event_budgets = prepared_event_budgets.assign(budget_id=lambda df: df['budget_id_prefix'].astype(str) + df['budget_id_suffix'].astype(str))
merged = prepared_expenses.merge(prepared_event_budgets[['link_to_event','budget_id']], left_on='link_to_budget', right_on='budget_id', how='inner')

# Filter to pizza expenses with cost in (50, 100)
mask = (
    merged['items'].str.contains('pizza', case=False, na=False) &
    (merged['cost'].astype(float) > 50) &
    (merged['cost'].astype(float) < 100)
)
result = merged.loc[mask, ['link_to_event', 'expense_date']].drop_duplicates()

# Rename for clarity
result = result.rename(columns={'link_to_event': 'event_name_or_id', 'expense_date': 'date'})

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
