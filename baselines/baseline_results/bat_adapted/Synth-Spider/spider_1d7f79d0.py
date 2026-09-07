import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['artistID','fname','lname_part1','lname_part2']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['painterID', 'paintingID', 'title']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['sculptorID','sculptureID','title']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
artists_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
paintings_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
sculptures_prepared = prepared_table_3

# Assume artists_prepared, paintings_prepared, sculptures_prepared are dataframes synthesized per targets.
# 1) Artists who have at least one painting
artists_with_paint = (artists_prepared
    .merge(paintings_prepared[['painterID']], left_on='artistID', right_on='painterID', how='inner')
    .drop_duplicates(subset=['artistID'])
)

# 2) Artists who have at least one sculpture
artists_with_sculp = (artists_prepared
    .merge(sculptures_prepared[['sculptorID']], left_on='artistID', right_on='sculptorID', how='inner')
    .drop_duplicates(subset=['artistID'])
)

# 3) Artists with painting but no sculpture
sculpt_ids = set(artists_with_sculp['artistID'])
result = artists_with_paint[~artists_with_paint['artistID'].isin(sculpt_ids)].copy()

# 4) Prepare output: first and last name (concatenate last name parts, trimming empties)
def join_last(parts):
    parts = [p for p in parts if isinstance(p, str) and p.strip() != '']
    return ' '.join(parts)

result['lname'] = [join_last([p1, p2]) for p1, p2 in zip(result.get('lname_part1', ''), result.get('lname_part2', ''))]
answer = result[['fname', 'lname']].drop_duplicates().reset_index(drop=True)

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
