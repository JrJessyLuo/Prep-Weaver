import pandas as pd
import numpy as np

def _prep_1(table_1):
    heroes_row = table_1.loc[table_1['id'].eq('superhero_name')]
    wide_names = heroes_row.drop(columns=['id'])
    long_names = wide_names.melt(value_name='superhero_name')
    target = long_names[['superhero_name']].astype({'superhero_name':'string'})
    target = target[target['superhero_name'].notna()]
    target = target[target['superhero_name'].str.strip().ne('')]
    target = target.drop_duplicates(subset=['superhero_name']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    split_cols = table_1['hero_power'].astype(str).str.split('-', n=1, expand=True)
    target = pd.DataFrame({'superhero_name': split_cols[0], 'power_name': split_cols[1]})
    target = target.dropna(subset=['superhero_name', 'power_name']).drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
hero_powers = prepared_table_2

# prepared tables assumed: heroes(superhero_name), hero_powers(superhero_name, power_name)

# 1) Join to align names (inner join keeps only heroes with listed powers)
joined = hero_powers.merge(heroes, on='superhero_name', how='inner')

# 2) Filter to the specific hero Amazo (case-sensitive match as in table_1 sample)
amazo_powers = joined[joined['superhero_name'] == 'Amazo']

# 3) Count distinct powers
answer = amazo_powers['power_name'].nunique()

result = int(answer)

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
