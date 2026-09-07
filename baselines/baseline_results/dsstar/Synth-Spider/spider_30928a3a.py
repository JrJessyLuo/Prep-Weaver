import pandas as pd

# Input tables are provided in `tables` dict:
# tables['table_1'] -> spider_30928a3a_input_0.pkl (artists table with names)
# tables['table_2'] -> spider_30928a3a_input_1.pkl (paintings table)
# tables['table_3'] -> art_1_Sculptures.pkl (not used here)

# Reproduce reference logic using tables['table_2'] (paintings)
df_paintings = tables['table_2']

# Normalize medium column to handle casing/spacing variants
medium_norm = df_paintings["medium"].astype(str).str.strip().str.lower()

# Identify painterIDs with at least one 'oil' and at least one 'lithograph' (incl. variants)
painters_with_oil = set(df_paintings.loc[medium_norm.eq("oil"), "painterID"].unique())
litho_mask = medium_norm.isin({"lithograph", "lithography", "lithographic"})
painters_with_litho = set(df_paintings.loc[litho_mask, "painterID"].unique())

# Intersection: painters who have both
painters_both = sorted(painters_with_oil.intersection(painters_with_litho))

# Using the execution result of the reference code, the painterIDs are [222]
# Now map these painterIDs to first and last names using tables['table_1']
df_artists = tables['table_1']

# Ensure consistent dtypes for merge
df_artists = df_artists.copy()
df_artists["painterID"] = df_artists["painterID"].astype(df_paintings["painterID"].dtype)

# Filter artists for the identified painterIDs
artists_both = df_artists[df_artists["painterID"].isin(painters_both)]

# Select and order the desired columns
answer_df = artists_both.loc[:, ["first_name", "last_name"]].drop_duplicates().reset_index(drop=True)

# Package the final result as required
result = {"artists_with_oil_and_lithograph": answer_df}