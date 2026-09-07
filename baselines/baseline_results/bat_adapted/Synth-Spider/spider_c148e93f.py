import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df = df.loc[:, ~df.columns.duplicated()]
    long = df.melt(id_vars=['city1_code'], var_name='city2_code', value_name='value')
    wide = long.pivot(index='city2_code', columns='city1_code', values='value').reset_index()
    wide = wide.rename(columns={'city2_code': 'city1_code', 'distance': 'distance'})
    wide['distance'] = pd.to_numeric(wide['distance'], errors='coerce')
    target = wide[['city1_code', 'city2_code', 'distance']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['city_code'] = df['city_code'].astype(str).str.strip()
    df['city_name'] = df['city_name'].astype(str).str.strip()
    df['state'] = df['state'].astype(str).str.strip()
    df['country'] = df['country'].astype(str).str.strip().str.upper()
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    target = df[['city_code','city_name','state','country','latitude','longitude']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_city_distances = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_cities = prepared_table_2

# prepared_city_distances: columns [city1_code, city2_code, distance]
# prepared_cities: columns [city_code, city_name, state, country, latitude, longitude]

# Normalize city_name for matching user input
cities = prepared_cities.copy()
cities['city_name_norm'] = cities['city_name'].str.strip().str.lower()

# Map user cities to codes
user_city_a = 'Boston'
user_city_b = 'Newark'
code_a = cities.loc[cities['city_name_norm'] == user_city_a.strip().lower(), 'city_code'].iloc[0]
code_b = cities.loc[cities['city_name_norm'] == user_city_b.strip().lower(), 'city_code'].iloc[0]

# Filter the distance for the unordered pair (either direction)
mask = ((prepared_city_distances['city1_code'] == code_a) & (prepared_city_distances['city2_code'] == code_b)) | \
       ((prepared_city_distances['city1_code'] == code_b) & (prepared_city_distances['city2_code'] == code_a))
result = prepared_city_distances.loc[mask, ['city1_code','city2_code','distance']].copy()

# Optionally attach names for readability (not required for computation)
result = result.merge(prepared_cities[['city_code','city_name']], left_on='city1_code', right_on='city_code', how='left') \
               .rename(columns={'city_name':'city1_name'}).drop(columns=['city_code'])
result = result.merge(prepared_cities[['city_code','city_name']], left_on='city2_code', right_on='city_code', how='left') \
               .rename(columns={'city_name':'city2_name'}).drop(columns=['city_code'])

# Final answer frame
answer = result[['city1_name','city2_name','distance']]

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
