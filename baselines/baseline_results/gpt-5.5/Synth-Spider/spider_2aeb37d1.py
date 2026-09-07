import pandas as pd

users = tables["table_1"]
properties = tables["table_2"]

owner_counts = (
    properties.groupby("owner_user_id", as_index=False)
    .agg(property_count=("property_id", "count"))
)

top_owner_id = (
    owner_counts.sort_values(["property_count", "owner_user_id"], ascending=[False, True])
    .iloc[0]["owner_user_id"]
)

out = (
    users.loc[users["user_id"].eq(top_owner_id), ["first_name"]]
    .head(1)
    .reset_index(drop=True)
)

result = {"user_with_most_properties": out}
