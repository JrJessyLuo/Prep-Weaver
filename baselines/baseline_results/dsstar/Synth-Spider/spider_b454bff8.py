import pandas as pd

# Access preloaded tables
df1 = tables['table_1']
df2 = tables['table_2']

# Reproduce the same logic as the reference: left join df1 with df2 on Institution_ID == iid
merged = df1.merge(df2, left_on="Institution_ID", right_on="iid", how="left")

# Select required columns: institution names and their nicknames
answer_df = merged[["Name", "Nickname"]]

# Package final answer
result = {"institutions_and_nicknames": answer_df}