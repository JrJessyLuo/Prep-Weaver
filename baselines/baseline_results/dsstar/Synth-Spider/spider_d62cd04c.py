import pandas as pd

# Use pre-loaded tables
df_accounts = tables['table_1']  # corresponds to spider_d62cd04c_input_0.pkl
df_shipments = tables['table_2']  # corresponds to spider_d62cd04c_input_1.pkl

# Find sender ID(s) for "John Zoidfarb"
sender_ids = df_accounts.loc[df_accounts["xingming"] == "John Zoidfarb", "zhanghao"].unique()

# Filter shipments where FaSongRen is among the identified sender IDs and select Contents
answer_df = df_shipments.loc[df_shipments["FaSongRen"].isin(sender_ids), ["Contents"]].reset_index(drop=True)

# Package final result as required
result = {
    "package_contents_by_john_zoidfarb": answer_df
}