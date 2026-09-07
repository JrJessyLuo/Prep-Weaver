import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['Theater_Name'] = df['Name_Part1'].astype(str).fillna('') + df['Name_Part2'].astype(str).fillna('')
    df['Movie'] = pd.to_numeric(df['Movie'], errors='coerce')
    target = df[['Code', 'Movie', 'Theater_Name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Code','movie_title']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_theaters = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_movies = prepared_table_2

# Assume prepared_theaters and prepared_movies are already synthesized per targets
# Filter for Odeon or Imperial theaters, then join to get movie titles and select unique titles
filtered = prepared_theaters[prepared_theaters['Theater_Name'].str.strip().str.lower().isin(['odeon','imperial'])]
merged = filtered.merge(prepared_movies, left_on='Movie', right_on='Code', how='inner')
# Extract distinct movie titles
answer = merged['movie_title'].dropna().drop_duplicates().sort_values().reset_index(drop=True)

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
