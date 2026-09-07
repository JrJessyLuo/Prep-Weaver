import pandas as pd

# Source DataFrames from the provided `tables` dict
artists_df = tables['table_1']
paintings_df = tables['table_2']

# Merge paintings with artists to associate painter info (artistID ↔ painterID)
merged_df = paintings_df.merge(
    artists_df[['artistID', 'fname', 'last_name', 'birthYear', 'deathYear']],
    left_on='painterID',
    right_on='artistID',
    how='left'
)

# Apply the same filter logic: artists with birthYear < 1850
filtered = merged_df[merged_df['birthYear'] < 1850]

# Select columns for output and sort as in the reference
result_cols = ['w_mm', 'title', 'fname', 'last_name', 'birthYear', 'year', 'paintingID']
final_df = filtered[result_cols].sort_values(by=['birthYear', 'year', 'paintingID']).reset_index(drop=True)

# Prepare final answer mapping
result = {"widths_by_artists_born_before_1850": final_df}