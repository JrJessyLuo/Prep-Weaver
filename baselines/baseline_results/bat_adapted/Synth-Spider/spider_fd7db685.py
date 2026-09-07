import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['artistID','fname']].copy()
    target = df.groupby('artistID', as_index=False).agg({'fname':'first'})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['painterID','paintingID']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_artists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_paintings = prepared_table_2

# Merge artists with paintings on artistID = painterID
merged = prepared_artists.merge(prepared_paintings, left_on='artistID', right_on='painterID', how='left')
# Count number of paintings per artist
counts = merged.groupby(['artistID','fname'], dropna=False)['paintingID'].nunique().reset_index(name='num_works')
# Filter artists with at least two paintings
result = counts[counts['num_works'] >= 2][['fname','num_works']]
# If needed, sort for presentation (not required)
# result = result.sort_values(['num_works','fname'], ascending=[False, True])
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
