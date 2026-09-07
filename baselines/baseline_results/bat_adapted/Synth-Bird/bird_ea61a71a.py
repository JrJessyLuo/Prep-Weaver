import pandas as pd
import numpy as np

def _prep_1(table_1):
    import numpy as np
    df = table_1.copy()
    df = df.drop_duplicates(subset=['id'], keep='first')
    name_candidates = [c for c in ['name','asciiName','faceName','flavorName','artist'] if c in df.columns]
    df['name'] = np.nan
    df['name'] = df[name_candidates].bfill(axis=1).iloc[:, 0] if len(name_candidates) > 0 else df['name']
    df['rarity'] = df['rarity'] if 'rarity' in df.columns else np.nan
    df['uuid'] = df['uuid'] if 'uuid' in df.columns else np.nan
    uuid_parts = df['uuid'].astype('string').str.split('-', n=4, expand=True)
    uuid_parts = uuid_parts.reindex(columns=range(5))
    uuid_parts.columns = ['uuid_part1','uuid_part2','uuid_part3','uuid_part4','uuid_part5']
    df = pd.concat([df, uuid_parts], axis=1)
    target = df[['id','name','rarity','uuid_part1','uuid_part2','uuid_part3','uuid_part4','uuid_part5']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['uuid_part1','uuid_part2','uuid_part3','uuid_part4','uuid_part5','date','text']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_rulings = prepared_table_2

# Join cards to rulings using composite uuid parts
cards_rulings = prepared_cards.merge(
    prepared_rulings,
    how='inner',
    on=['uuid_part1','uuid_part2','uuid_part3','uuid_part4','uuid_part5']
)

# Filter to uncommon rarity
uncommons = cards_rulings[cards_rulings['rarity'].str.lower() == 'uncommon']

# For each card, find the earliest ruling date
uncommons['date'] = pd.to_datetime(uncommons['date'], errors='coerce')
earliest = (
    uncommons.sort_values('date')
             .groupby(['uuid_part1','uuid_part2','uuid_part3','uuid_part4','uuid_part5','name','rarity'], as_index=False)
             .agg(first_ruling_date=('date','first'))
)

# Sort by earliest ruling date ascending and pick first 3
result = earliest.sort_values('first_ruling_date', ascending=True).head(3)[['name']]

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
