import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','publisher_id','superhero_name','full_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    row = table_1.loc[table_1['id'].eq('publisher_name')].copy()
    long = row.drop(columns=['id']).melt(var_name='publisher_id', value_name='publisher_name')
    long['publisher_id'] = pd.to_numeric(long['publisher_id'], errors='coerce').astype('Int64')
    long['publisher_name'] = long['publisher_name'].replace('nan', pd.NA)
    long = long.dropna(subset=['publisher_id', 'publisher_name'])
    long['publisher_id'] = long['publisher_id'].astype(int)
    target = long[['publisher_id', 'publisher_name']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_superheroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_publishers = prepared_table_2

prepared_superheroes['publisher_id'] = prepared_superheroes['publisher_id'].astype('Int64')
prepared_superheroes['id'] = prepared_superheroes['id'].astype('Int64')
# Unpivot table_2-style wide row into long mapping
pp = prepared_publishers.copy()
# If prepared_publishers isn't yet constructed: build from raw table_2
# Example construction (assumes raw table_2 is df2):
# row = df2.iloc[0]
# prepared_publishers = (
#     pd.DataFrame({'publisher_id': [int(c) for c in df2.columns[1:]],
#                   'publisher_name': [row[c] for c in df2.columns[1:]]})
# )
prepared_publishers['publisher_id'] = prepared_publishers['publisher_id'].astype('Int64')
# Join to get publisher names
joined = prepared_superheroes.merge(prepared_publishers, on='publisher_id', how='left')
# Question-specific filter: superhero with ID 38
answer = joined.loc[joined['id'] == 38, ['publisher_name']]
# If multiple rows, take unique non-null names
answer = answer['publisher_name'].dropna().unique().tolist()
result = answer[0] if len(answer) > 0 else None

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
