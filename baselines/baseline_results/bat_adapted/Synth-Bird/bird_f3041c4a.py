import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['id', 'asciiName']]
    prepared = prepared.drop_duplicates(subset=['id'], keep='first')
    target = prepared.reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['id','translation','language_setCode']].dropna(subset=['id','translation','language_setCode']).drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_translations = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])

angel_cards = prepared_cards[prepared_cards['asciiName'].fillna('').str.contains('Angel of Mercy', case=False, na=False)]
merged = angel_cards.merge(prepared_translations, on='id', how='inner')
# Count distinct translations for those cards (by language and set code entry)
answer = merged['language_setCode'].nunique()

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
