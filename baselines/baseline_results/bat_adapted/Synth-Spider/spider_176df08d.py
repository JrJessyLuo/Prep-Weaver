import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['Title'] = df['Title_Part1'].astype(str) + ' ' + df['Title_Part2'].astype(str)
    target = df[['Code','Title']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    names = table_1[table_1['Code'].eq('Name')].drop(columns=['Code']).melt(var_name='key', value_name='TheaterName')
    movies = table_1[table_1['Code'].eq('Movie')].drop(columns=['Code']).melt(var_name='key', value_name='MovieCode')
    merged = pd.merge(names, movies, on='key', how='inner')
    merged['MovieCode'] = pd.to_numeric(merged['MovieCode'], errors='coerce')
    merged = merged.dropna(subset=['MovieCode'])
    merged['MovieCode'] = merged['MovieCode'].astype(int)
    target = merged[['TheaterName', 'MovieCode']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
movies = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
theater_movie_map = prepared_table_2

# movies: from table_1
# - keep Code
# - Title = Title_Part1 + ' ' + Title_Part2 (handle missing parts gracefully)
movies = table_1.copy()
movies['Title_Part1'] = movies['Title_Part1'].fillna('')
movies['Title_Part2'] = movies['Title_Part2'].fillna('')
movies['Title'] = (movies['Title_Part1'] + ' ' + movies['Title_Part2']).str.strip()
movies = movies[['Code', 'Title']]

# theater_movie_map: from table_2
# Unpivot columns 1..n into rows using the 'Name' and 'Movie' entries
wide = table_2.copy()
# Identify theater columns (exclude the first 'Code' column)
theater_cols = [c for c in wide.columns if c != 'Code']
# Create mapping from column -> (theater name, movie code)
name_row = wide[wide['Code'] == 'Name'][theater_cols].iloc[0]
movie_row = wide[wide['Code'] == 'Movie'][theater_cols].iloc[0]
long_df = pd.DataFrame({
    'TheaterName': name_row.values,
    'MovieCode_raw': movie_row.values
})
# Clean and cast movie codes, drop NaNs
long_df['MovieCode'] = pd.to_numeric(long_df['MovieCode_raw'], errors='coerce').dropna().astype(int)
# Align TheaterName with non-null MovieCode
theater_movie_map = long_df.loc[long_df['MovieCode_raw'].notna(), ['TheaterName', 'MovieCode']].copy()

# Integrate: join on MovieCode (theater_movie_map) == Code (movies)
merged = theater_movie_map.merge(movies, left_on='MovieCode', right_on='Code', how='inner')

# Question-specific filtering: theaters named 'Odeon'
result = merged[merged['TheaterName'].str.strip().str.casefold() == 'odeon']

# Final answer: movie titles for ones that are played in the Odeon theater
answer = result['Title'].dropna().drop_duplicates().tolist()

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
