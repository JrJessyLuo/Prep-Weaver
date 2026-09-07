import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['artistID','birthYear','fname','prefix','last_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['paintingID','title','w_mm','painterID']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_artists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_paintings = prepared_table_2

# prepared_artists and prepared_paintings are the synthesized per-table targets
merged = prepared_paintings.merge(prepared_artists, left_on='painterID', right_on='artistID', how='inner')
# Filter artists born prior to 1850
merged = merged[pd.to_numeric(merged['birthYear'], errors='coerce') < 1850]
# Select painting widths (and optional identifiers/evidence)
result = merged[['paintingID', 'title', 'w_mm']]
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
