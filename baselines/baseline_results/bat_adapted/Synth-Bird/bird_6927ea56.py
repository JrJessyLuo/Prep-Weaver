import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['setCode','convertedManaCost','id']].copy()
    prepared = prepared.rename(columns={'id':'card_id'})
    prepared = prepared.drop_duplicates(subset=['card_id','setCode'], keep='first')
    target = prepared[['setCode','convertedManaCost','card_id']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1.loc[:, ['code', 'name', 'totalSetSize']]
    prepared = prepared.drop_duplicates(subset=['code'], keep='first')
    target = prepared.reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_sets = prepared_table_2

# Assume prepared_cards and prepared_sets are available DataFrames
# 1) Join cards to sets by set code
cards_sets = prepared_cards.merge(prepared_sets, left_on='setCode', right_on='code', how='inner')

# 2) Filter to the Coldsnap set (name == 'Coldsnap' or code == its code 'CSP')
cs = cards_sets[(cards_sets['name'] == 'Coldsnap') | (cards_sets['code'] == 'CSP')]

# 3) Compute counts
total_cards = len(cs)
num_cmc7 = (cs['convertedManaCost'] == 7).sum()

# 4) Percentage of cards with CMC 7 within the set
percentage = (num_cmc7 / total_cards * 100.0) if total_cards > 0 else 0.0

result = pd.DataFrame({
    'set': ['Coldsnap'],
    'total_cards': [total_cards],
    'cmc7_cards': [int(num_cmc7)],
    'percentage_cmc7': [percentage]
})

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
