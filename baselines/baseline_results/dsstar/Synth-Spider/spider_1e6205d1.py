import pandas as pd

# Access pre-loaded tables
df_unis = tables['table_1']
df_rank = tables['table_2']

# Prepare university id -> name mapping
df_unis_reset = df_unis.reset_index(drop=False)
uni_id_cols = [c for c in df_unis_reset.columns if str(c).isdigit()]

long_unis = df_unis_reset.melt(
    id_vars=['University_ID'],
    value_vars=uni_id_cols,
    var_name='uni_id_str',
    value_name='University_Name'
).dropna(subset=['University_Name'])

long_unis['uni_id'] = long_unis['uni_id_str'].astype(int)
uni_lookup = long_unis[['uni_id', 'University_Name']].drop_duplicates()

# Merge rankings with university names
merged = df_rank.merge(uni_lookup, on='uni_id', how='left')

# Aggregate per university
agg = (
    merged
    .groupby('University_Name', as_index=False)
    .agg({
        'Reputation_point': 'max',
        'cit_p': 'max',
        'Total': 'max',
        'Rank': 'min'
    })
)

# Sort and get top 3 by Reputation_point, then cit_p, then Rank
top3 = agg.sort_values(
    by=['Reputation_point', 'cit_p', 'Rank'],
    ascending=[False, False, True]
).head(3)

# Select only the required columns: University_Name and cit_p
final_df = top3[['University_Name', 'cit_p']].reset_index(drop=True)

# Package result as required
result = {
    'top3_universities_name_and_citation_point': final_df
}