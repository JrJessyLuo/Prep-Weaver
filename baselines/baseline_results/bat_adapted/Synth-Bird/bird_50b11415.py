import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','asciiName','faceName','duelDeck','convertedManaCost']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])

cards = prepared_cards.copy()
# Filter to duel-related cards (interpretation: rows where 'duelDeck' is not null indicate Duel Decks)
duels = cards[~cards['duelDeck'].isna()]
# Choose a display name preferring faceName then asciiName
duels['card_name'] = duels['faceName'].fillna(duels['asciiName'])
# Rank by converted mana cost descending and take top 10
result = duels.sort_values(by='convertedManaCost', ascending=False).head(10)[['card_name','convertedManaCost']]
answer = result

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
