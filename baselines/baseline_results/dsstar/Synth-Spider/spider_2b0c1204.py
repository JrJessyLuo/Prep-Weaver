import pandas as pd

# Source tables from the provided `tables` dict
addresses_df = tables['table_1']
users_df = tables['table_2']

# Reproduce the same logic as the reference code
robbie_users = users_df.loc[users_df["first_name"] == "Robbie", ["user_id", "first_name", "user_address_id"]]
merged = robbie_users.merge(
    addresses_df[["address_id", "country"]],
    left_on="user_address_id",
    right_on="address_id",
    how="left"
)
final_df = merged[["user_id", "first_name", "user_address_id", "country"]]

# Assign final answer as required
result = {"robbie_country": final_df}