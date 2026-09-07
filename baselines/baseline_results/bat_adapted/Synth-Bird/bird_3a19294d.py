import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['event_id','event_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['expense_id','expense_description','expense_date','cost','approved','link_to_budget']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    source = table_1.copy()
    target_cols = ['budget_id','rec0QmEc3cSQFQ6V2','rec1bG6HSft7XIvTP','rec1z6ISJU2HdIsVm','rec33PFqxLtnp80RJ','rec4DYUKBHMPZXWB2','rec4yM47hEjVVsCuq','rec59vErJo51glQRb','rec5V70sIuIgpOzDT','recFZ47e0eVqcQD9O','recHzdM40gk9a6AdY','recJOc7f9KgpgJm5q','recKZxqNPPZgtnR0P','recKjd7dcURsmP0KY','recM0BC3bOG33jG4X','recMc8TbR76rmUSHG','recN9yY7okNrFps0Y','recQf86wBWXvebEBO','recRQdaiKCxFAlPCy','recTUGXxhTaFZ2qkg','recTxecmwIhCdIKvl','recUmDNVie8sfU6UR','recW1Nf8JDbUhtxkc','recXGXXRruuAY1JNN','recXZUYlYNiRmeoxX','recXaqLgIlsJ4eppc','recZAjcliIUo4BCKW','recZdw5TjWrRTj4kp','recZuCiQzCDAs4zDQ','recca5tkvdQgoLKZz','recdGqhxapehMT00E','recexNBMuCY9emh6y','recfbLRzfFbWypDEs','recjcVh1VW33HXFFf','recjpAeh0324DqHtB','reckyFmOuPIIya9hY','recl41vHHNtegoZFY','recmdREMTVnyW11OD','recpyBgyiqxFEFCI3','recqSlOPFX5FlrMqw']
    target = source[target_cols]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
events_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
expenses_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
budgets_pivoted = prepared_table_3

# Assume events_prepared, expenses_prepared, budgets_pivoted are available DataFrames

# 1) Reshape budgets to long form so each budget column key becomes a row
value_vars = [c for c in budgets_pivoted.columns if c != 'budget_id']
budgets_long = budgets_pivoted.melt(id_vars=['budget_id'], value_vars=value_vars, var_name='column_key', value_name='value')
# Split into category and spent for easy filtering
budget_category = budgets_long[budgets_long['budget_id'] == 'category'][['column_key', 'value']].rename(columns={'value':'category'})
budget_spent    = budgets_long[budgets_long['budget_id'] == 'spent'][['column_key', 'value']].rename(columns={'value':'spent'})
# Merge category and spent
budget_detail = budget_category.merge(budget_spent, on='column_key', how='left')
# Keep only Advertisement budget items
budget_ads = budget_detail[budget_detail['category'] == 'Advertisement'].copy()
# 2) Map expenses to these budget items via link_to_budget
expenses_ads = expenses_prepared.merge(budget_ads[['column_key']], left_on='link_to_budget', right_on='column_key', how='inner')
# 3) Sum advertisement spend per event by using the budget column_key as the event_id, then join to event names
ads_by_event = expenses_ads.groupby('link_to_budget', as_index=False)['cost'].sum().rename(columns={'link_to_budget':'event_id', 'cost':'total_ad_spend'})
result = ads_by_event.merge(events_prepared, on='event_id', how='left')
# 4) Pick the event with the highest total advertisement spend
result_sorted = result.sort_values('total_ad_spend', ascending=False)
final_answer = result_sorted.iloc[0][['event_name', 'total_ad_spend']]

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
