import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['account_id','district_id','frequency','date']].copy()
    target['date'] = pd.to_datetime(target['date'], errors='coerce')
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['card_id','disp_id','type','year','month','day']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_accounts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_cards = prepared_table_2

gold_cards = prepared_cards[prepared_cards['type'].str.lower() == 'gold']
# Join cards -> dispositions to get account_id
cards_with_accounts = gold_cards.merge(prepared_dispositions[['disp_id','account_id']], on='disp_id', how='inner')
# Join to accounts to get account details (optional for evidence)
result = cards_with_accounts.merge(prepared_accounts[['account_id']], on='account_id', how='inner').drop_duplicates(subset=['account_id'])
# Final answer: accounts that have gold credit cards
answer = result[['account_id']]

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
