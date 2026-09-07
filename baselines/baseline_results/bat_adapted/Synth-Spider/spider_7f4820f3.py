import pandas as pd
import numpy as np

def _prep_1(table_1):
    import re
    target = table_1.rename(columns={'b':'boat_id','name':'boat_name','clr':'color_norm'})
    target['boat_id'] = target['boat_id'].astype(int)
    target['color_norm'] = target['color_norm'].astype(str).str.lower().str.strip().str.replace(r"[^a-z_ ]+","",regex=True).str.strip(" _")
    target = target[['boat_id','boat_name','color_norm']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['date_value_pairs'] = df['date_value_pairs'].fillna('')
    df['pair'] = df['date_value_pairs'].str.split(',')
    df = df.explode('pair')
    df['pair'] = df['pair'].astype(str).str.strip()
    df = df[df['pair'].ne('') & df['pair'].ne('nan')]
    df['boat_id'] = df['pair'].str.split(':').str[1].astype(float).astype(int)
    target = df[['sid','boat_id']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_boats = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_reservations = prepared_table_2

# prepared_boats creation
pb = table_1.copy()
pb = pb.rename(columns={'b':'boat_id','name':'boat_name','clr':'color_raw'})
# normalize color: lowercase, strip spaces, remove non-letters except spaces/underscore, then map common variants
pb['color_norm'] = (pb['color_raw']
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(r'[^a-z_ ]','', regex=True)
    .str.replace(r'\s+',' ', regex=True)
    .str.strip())
# optional simple canonicalization of variants
pb['color_norm'] = pb['color_norm'].replace({'_red_':'red', ' red ':'red', ' blue ':'blue'})
pb['boat_id'] = pd.to_numeric(pb['boat_id'], errors='coerce').astype('Int64')
prepared_boats = pb[['boat_id','boat_name','color_norm']]

# prepared_reservations creation: explode date_value_pairs to rows
pr = table_2.copy()
pr = pr.rename(columns={'sid':'sid','date_value_pairs':'date_value_pairs'})
# split into list of pairs
pairs = pr['date_value_pairs'].astype(str).str.split(',')
pr = pr.loc[pr.index.repeat(pairs.str.len())].assign(pair=sum(pairs.tolist(), []))
# split 'date:boat' and cast boat to int
pr[['date','boat_str']] = pr['pair'].str.split(':', n=1, expand=True)
pr['boat_id'] = pd.to_numeric(pr['boat_str'], errors='coerce').astype('Int64')
prepared_reservations = pr[['sid','boat_id']].dropna(subset=['boat_id']).drop_duplicates()

# Integration
merged = prepared_reservations.merge(prepared_boats, on='boat_id', how='inner')

# Question-specific filter: boats that are red or blue
mask = merged['color_norm'].isin(['red','blue'])
result_sids = merged.loc[mask, 'sid'].drop_duplicates().sort_values()

answer = result_sids.tolist()
answer

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
