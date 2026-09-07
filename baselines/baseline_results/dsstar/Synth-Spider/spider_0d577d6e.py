import pandas as pd

# Access pre-loaded tables
df0 = tables['table_1']
df1 = tables['table_2']

# Create a combined Theater_Name from Name_Part1 and Name_Part2 if both exist
if {'Name_Part1', 'Name_Part2'}.issubset(df1.columns):
    df1 = df1.copy()
    df1['Theater_Name'] = (
        df1['Name_Part1'].fillna('') + ' ' + df1['Name_Part2'].fillna('')
    ).str.strip().replace('', pd.NA)

# Merge via Code
merged = df0.merge(df1, on='Code', how='left', suffixes=('_movie', '_theater'))

# Filter for the specified Theater_Name values and get unique movie titles
target_names = {"Od eon", "Im perial"}
filtered = merged[merged['Theater_Name'].isin(target_names)]
unique_titles = sorted(filtered['movie_title'].dropna().unique().tolist())

# Prepare final answer DataFrame
answer_df = pd.DataFrame({'movie_title': unique_titles})

# Package result as specified
result = {"movies_at_odeon_or_imperial": answer_df}