import pandas as pd
import numpy as np

def _prep_1(table_1):
    codes_row = table_1.loc[table_1['city1_code'].eq('city2_code'), 'city_data_combined'].iloc[0]
    dists_row = table_1.loc[table_1['city1_code'].eq('distance'), 'city_data_combined'].iloc[0]
    codes_by_city = codes_row.split('|')
    dists_by_city = dists_row.split('|')
    n = min(len(codes_by_city), len(dists_by_city))
    codes_by_city = codes_by_city[:n]
    dists_by_city = dists_by_city[:n]
    city_codes = [s.split(',')[0].strip() if isinstance(s, str) and len(s) else None for s in codes_by_city]
    other_codes_lists = [s.split(',') if isinstance(s, str) and len(s) else [] for s in codes_by_city]
    dist_lists = [s.split(',') if isinstance(s, str) and len(s) else [] for s in dists_by_city]
    df = pd.DataFrame({'city_code': city_codes, 'other_city_code': other_codes_lists, 'distance': dist_lists})
    df = df.explode(['other_city_code', 'distance'], ignore_index=True)
    df['other_city_code'] = df['other_city_code'].astype(str).str.strip()
    df['distance'] = pd.to_numeric(df['distance'].astype(str).str.replace('"', '', regex=False).str.strip(), errors='coerce')
    target = df.loc[df['city_code'].notna() & df['other_city_code'].ne('') & df['distance'].notna(), ['city_code', 'other_city_code', 'distance']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['city_code','city_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_city_distances = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_city_directory = prepared_table_2

# prepared_city_distances columns: city_code, other_city_code, distance (numeric)
# prepared_city_directory columns: city_code, city_name

# 1) Join distances with city names for the base city
base_named = prepared_city_distances.merge(prepared_city_directory, how='left', on='city_code')
# 2) Optionally drop self-distances if present (distance to self should be excluded from average to 'all other cities')
base_named = base_named[base_named['city_code'] != base_named['other_city_code']]
# 3) Compute average distance to all other cities per base city
avg_dist = (base_named
            .groupby(['city_code', 'city_name'], as_index=False)['distance']
            .mean()
            .rename(columns={'distance': 'avg_distance_to_others'}))
# 4) Select required output columns: city name and the computed average
target = avg_dist[['city_name', 'avg_distance_to_others']]

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
