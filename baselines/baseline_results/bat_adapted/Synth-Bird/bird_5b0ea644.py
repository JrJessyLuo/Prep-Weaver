import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['id', 'artist']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['id','language']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_translations = prepared_table_2

target = prepared_cards.merge(prepared_translations, on='id', how='inner')
# Filter to cards illustrated by Volkan BaÇa (handle possible variations/diacritics)
name_variants = ['Volkan Baça', 'Volkan BaÃ§a', 'Volkan BaÇa', 'Volkan Baca']
mask_artist = prepared_cards['artist'].fillna('').str.strip().str.lower().isin([n.lower() for n in name_variants])
# Filter to French language
mask_lang = prepared_translations['language'].fillna('').str.strip().str.lower() == 'french'
filtered = target[mask_artist & mask_lang]
answer = len(filtered['id'].drop_duplicates())

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
