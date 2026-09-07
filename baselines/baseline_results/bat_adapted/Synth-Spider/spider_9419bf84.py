import pandas as pd
import numpy as np

def _prep_1(table_1):
    split_cols = table_1['trc'].str.split('###', n=1, expand=True)
    target = table_1.assign(MovieName=split_cols[0], Rating=split_cols[1])[['Code', 'MovieName', 'Rating']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    names = table_1.loc[table_1['Code'].eq('Name')].drop(columns=['Code']).melt(var_name='key', value_name='CinemaName')
    codes = table_1.loc[table_1['Code'].eq('Movie')].drop(columns=['Code']).melt(var_name='key', value_name='MovieCode')
    merged = pd.merge(names, codes, on='key', how='inner')
    merged['MovieCode'] = merged['MovieCode'].replace('nan', pd.NA)
    target = merged.dropna(subset=['MovieCode'])[['CinemaName','MovieCode']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
movies = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
cinema_movie_map = prepared_table_2

# Assume prepared tables are provided as DataFrames: movies, cinema_movie_map
# Filter to the target cinemas
target_cinemas = ['Odeon', 'Imperial']
cm_filt = cinema_movie_map[cinema_movie_map['CinemaName'].isin(target_cinemas)].copy()

# Normalize types for join
cm_filt['MovieCode'] = cm_filt['MovieCode'].astype(str).str.replace('.0', '', regex=False)
movies_norm = movies.copy()
movies_norm['Code'] = movies_norm['Code'].astype(str)

# Join to get movie names
joined = cm_filt.merge(movies_norm, left_on='MovieCode', right_on='Code', how='inner')

# Select unique movie names played in either cinema
result = joined['MovieName'].dropna().drop_duplicates().sort_values().tolist()

# If a DataFrame is expected as final output
answer = pd.DataFrame({'MovieName': result})

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
