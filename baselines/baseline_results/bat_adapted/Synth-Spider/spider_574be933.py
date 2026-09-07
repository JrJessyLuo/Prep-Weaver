import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['artistID','fname','lname','birth_year','deathYear']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['sculptureID','title','year','medium','sculptorID','location']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_artists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_sculptures = prepared_table_2

# prepared_artists and prepared_sculptures are assumed to be synthesized per the target schemas
merged = prepared_sculptures.merge(prepared_artists, left_on='sculptorID', right_on='artistID', how='inner')
# Filter to sculptures made before 1900
merged['year'] = pd.to_numeric(merged['year'], errors='coerce')
pre1900 = merged[merged['year'] < 1900]
# Get distinct artists who made such sculptures
result = pre1900[['fname', 'lname', 'artistID']].dropna(subset=['fname','lname']).drop_duplicates(subset=['artistID'])
# Final projection: first and last names of each distinct artist
answer = result[['fname', 'lname']]

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
