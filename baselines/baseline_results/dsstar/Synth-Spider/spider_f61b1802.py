import pandas as pd

# Access pre-loaded tables
df1 = tables['table_1']
df2 = tables['table_2']

# Optional: Ensure Institution_ID is int64 in both for consistent merging
if df1['Institution_ID'].dtype != 'int64':
    df1['Institution_ID'] = df1['Institution_ID'].astype('int64', errors='ignore')
if df2['Institution_ID'].dtype != 'int64':
    df2['Institution_ID'] = df2['Institution_ID'].astype('int64', errors='ignore')

# Merge on Institution_ID, bringing Nickname from df2
merged = pd.merge(df1, df2[['Institution_ID', 'Nickname']], on='Institution_ID', how='left')

# Prepare final answer: Names and Nicknames of institutions (as per merged preview logic)
final_df = merged[['Institution_ID', 'Name', 'Nickname']]

# Package result as required
result = {
    "institution_names_and_nicknames": final_df
}