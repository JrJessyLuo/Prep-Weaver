import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['code','name','block','baseSetSize','totalSetSize','type']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    tmp = table_1.copy()
    tmp[['language','setCode']] = tmp['language_setCode'].str.split('|', n=1, expand=True)
    target = tmp[['language','setCode','translation']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_sets = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_translations = prepared_table_2

# prepared_sets has columns: code, name, block, baseSetSize, totalSetSize, type
# prepared_translations has columns: language, setCode, translation

merged = prepared_sets.merge(prepared_translations, left_on='code', right_on='setCode', how='inner')

# Identify the set: "the set of 180 cards that belongs to the Ravnica block"
# Use totalSetSize (or baseSetSize if total not present); prefer totalSetSize when available.
merged['size'] = merged['totalSetSize'].fillna(merged['baseSetSize'])

candidate = merged[(merged['block'] == 'Ravnica') & (merged['size'] == 180)]

# The question asks: What language is the set translated into?
# Return the distinct language(s) corresponding to that set's translation entries.
answer = candidate['language'].dropna().drop_duplicates().tolist()

# If multiple, keep unique values; if single, return that value/string.
result = answer if len(answer) != 1 else answer[0]

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
