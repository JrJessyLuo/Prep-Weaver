import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    name_col = 'name' if 'name' in df.columns else ('faceName' if 'faceName' in df.columns else ('asciiName' if 'asciiName' in df.columns else None))
    setcode_col = 'setCode' if 'setCode' in df.columns else ('set' if 'set' in df.columns else ('set_code' if 'set_code' in df.columns else None))
    setname_col = 'setName' if 'setName' in df.columns else ('set_name' if 'set_name' in df.columns else ('setName' if 'setName' in df.columns else None))
    df = df.rename(columns={c: n for c, n in [(name_col, 'name'), (setcode_col, 'setCode'), (setname_col, 'setName')] if c is not None})
    for col in ['id','artist','setCode','setName','name']: df[col] = df[col] if col in df.columns else pd.NA
    target = df[['id','artist','setCode','setName','name']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1.loc[:, ['code', 'name']]
    prepared = prepared.drop_duplicates(subset=['code', 'name']).reset_index(drop=True)
    target = prepared
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_sets = prepared_table_2

# prepared_cards must include a set code column; infer likely column names
cards = prepared_cards.copy()
# Normalize potential set code/name columns in cards
if 'setCode' not in cards.columns:
    if 'set' in cards.columns:
        cards = cards.rename(columns={'set': 'setCode'})
    elif 'code' in cards.columns:
        cards = cards.rename(columns={'code': 'setCode'})

if 'setName' not in cards.columns:
    if 'set_name' in cards.columns:
        cards = cards.rename(columns={'set_name': 'setName'})
    elif 'setName' in cards.columns:
        pass
    else:
        # if no setName exists, it will be obtained from prepared_sets on join
        pass

sets = prepared_sets.rename(columns={'code': 'code', 'name': 'setName'})

# Join cards to sets on set code
merged = cards.merge(sets, left_on='setCode', right_on='code', how='left')

# Filter to the target set by (localized) name and artist
mask_set = merged['setName'].str.strip().str.casefold() == 'hauptset zehnte edition'
mask_artist = merged['artist'].str.strip().str.casefold() == 'adam rex'
result_count = merged[mask_set & mask_artist].shape[0]

answer = result_count

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
