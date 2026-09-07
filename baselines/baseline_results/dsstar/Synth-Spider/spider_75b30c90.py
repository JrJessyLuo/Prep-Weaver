import pandas as pd

# 1) Load the two relevant dataframes from the provided `tables` dict
df_subset_defs = tables['table_1']  # spider_75b30c90_input_0.pkl
df_subset_members = tables['table_2']  # spider_75b30c90_input_1.pkl

# 2) Join memberships with subset definitions
joined = df_subset_members.merge(
    df_subset_defs,
    left_on="subset_id",
    right_on="Collection_Subset_ID",
    how="left",
    validate="m:1"
)

# 3) Group to count unique collections per subset (mirrors reference logic)
grouped = (
    joined.groupby(['subset_id', 'Collection_Subset_Name'])['Collection_ID']
    .nunique()
    .reset_index(name='num_collections')
    .sort_values(['num_collections', 'subset_id'], ascending=[False, True])
)

# 4) Prepare final answer DataFrame with requested columns
answer = grouped[['subset_id', 'Collection_Subset_Name', 'num_collections']]

# 5) Package into result dict as required
result = {
    "collections_per_subset": answer
}