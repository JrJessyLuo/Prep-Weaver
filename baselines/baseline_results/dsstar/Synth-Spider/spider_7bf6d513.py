import pandas as pd

# Source dataframes from provided 'tables' dict
df0 = tables['table_1']  # pilots and planes
df1 = tables['table_2']  # plane locations wide format

# Reshape df1 to long format: plane -> location
df1_long = df1.melt(id_vars=['plane_name'], var_name='pln', value_name='location')
if df1_long['plane_name'].nunique() == 1:
    df1_long = df1_long.drop(columns=['plane_name'])

# Join pilots with their plane locations
df_joined = df0.merge(df1_long, on='pln', how='left')

# Find pilots who have planes in both Austin and Boston
locs = df_joined.dropna(subset=['location']).groupby('pn')['location'].apply(set).reset_index()
pilots_both = locs[locs['location'].apply(lambda s: {'Austin', 'Boston'}.issubset(s))]['pn']

answer_df = pd.DataFrame({'pn': sorted(pilots_both.unique())})

# Package final answer
result = {'pilots_in_austin_and_boston': answer_df}