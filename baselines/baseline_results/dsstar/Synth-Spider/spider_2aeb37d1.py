import pandas as pd

# Source DataFrames from provided tables dict
df_users = tables['table_1']
df_properties = tables['table_2']

# Reproduce the same logic as the reference code
properties_per_owner = (
    df_properties
    .groupby("owner_user_id")
    .size()
    .reset_index(name="property_count")
    .sort_values(by=["property_count", "owner_user_id"], ascending=[False, True])
    .reset_index(drop=True)
)

result_df = properties_per_owner.merge(
    df_users[["user_id", "first_name", "middle_name", "last_name", "login_name"]],
    left_on="owner_user_id",
    right_on="user_id",
    how="left"
).drop(columns=["user_id"])

# Extract the first name of the user who owns the greatest number of properties
top_first_name = result_df.iloc[0]["first_name"]
answer_df = pd.DataFrame({"first_name": [top_first_name]})

# Package final answer in the required dict format
result = {
    "top_owner_first_name": answer_df
}