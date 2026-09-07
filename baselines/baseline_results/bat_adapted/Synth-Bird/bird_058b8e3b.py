import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['language','set_info']].copy()
    parsed = df['set_info'].astype(str).str.split('|', n=1, expand=True)
    df['set_code'] = parsed[0]
    df['set_name_local'] = parsed[1]
    target = df[['set_code','set_name_local','language']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import numpy as np
    import pandas as pd
    df = table_1.copy()
    df['set_code_from_name'] = df['name'].astype('string').str.extract(r'(?i)(?:\[\s*([A-Z0-9]{2,10})\s*\]|\b([A-Z0-9]{2,10})\s*\|)', expand=True).bfill(axis=1).iloc[:, 0]
    df['set_code_from_text'] = df['text'].astype('string').str.extract(r'(?i)(?:\[\s*([A-Z0-9]{2,10})\s*\]|\b([A-Z0-9]{2,10})\s*\|)', expand=True).bfill(axis=1).iloc[:, 0]
    df['set_code'] = df['set_code_from_name'].fillna(df['set_code_from_text'])
    df['set_code'] = df['set_code'].where(df['set_code'].notna(), pd.NA)
    target = df[['uuid', 'name', 'language', 'set_code']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_table_sets_by_language = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_table_cards_by_language = prepared_table_2

sets = prepared_table_sets_by_language.copy()
cards = prepared_table_cards_by_language.copy()

# Normalize language labels
norm = {
    'Japanese': 'Japanese',
    'Korean': 'Korean'
}
sets['language_norm'] = sets['language']
cards['language_norm'] = cards['language']

# Determine which set_codes have any Korean card translations and which have any Japanese card translations
cards_kor_sets = set(cards.loc[cards['language_norm'].eq('Korean'), 'set_code'].dropna().unique())
cards_jpn_sets = set(cards.loc[cards['language_norm'].eq('Japanese'), 'set_code'].dropna().unique())

# Consider only known sets (from table_1) and find those lacking Japanese but having Korean
all_set_codes = sets['set_code'].dropna().unique()
eligible_codes = [c for c in all_set_codes if (c in cards_kor_sets) and (c not in cards_jpn_sets)]

# Output the set names (deduplicate per set_code)
result = (
    sets[sets['set_code'].isin(eligible_codes)]
    .sort_values(['set_code', 'language_norm'])
    .groupby('set_code', as_index=False)
    .agg(set_name_local=('set_name_local', 'first'))
)

target = result[['set_name_local']].rename(columns={'set_name_local': 'set_name'})

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
