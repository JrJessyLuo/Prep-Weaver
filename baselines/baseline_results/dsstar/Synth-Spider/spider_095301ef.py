import pandas as pd

# Access pre-loaded DataFrames from the provided `tables` dict
df0 = tables['table_1']  # corresponds to spider_095301ef_input_0.pkl
df1 = tables['table_2']  # corresponds to spider_095301ef_input_1.pkl

# Reproduce the same logic as the reference code: merge and aggregate
merged = df1.merge(df0, left_on='conf_id', right_on='Conference_ID', how='inner')
answer_df = merged.groupby(['Conference_Name', 'Year']).size().reset_index(name='num_participants')

# Prepare final result mapping
result = {
    'participants_per_conference_year': answer_df
}