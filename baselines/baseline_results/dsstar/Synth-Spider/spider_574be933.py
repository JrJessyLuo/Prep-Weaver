import pandas as pd

# Access pre-loaded tables
artists_df = tables['table_1']  # corresponds to spider_574be933_input_0.pkl
sculptures_df = tables['table_2']  # corresponds to spider_574be933_input_1.pkl

# Filter sculptures before 1900
sculptures_pre1900 = sculptures_df[sculptures_df['year'] < 1900].copy()

# Inner join sculptures (pre-1900) with artists on sculptorID == artistID
merged = sculptures_pre1900.merge(
    artists_df,
    left_on="sculptorID",
    right_on="artistID",
    how="inner",
    suffixes=("_sculpture", "_artist")
)

# Select distinct artist first and last names
answer_df = merged[['fname', 'lname']].drop_duplicates().reset_index(drop=True)

# Prepare result as required
result = {
    "artists_with_sculptures_before_1900": answer_df
}