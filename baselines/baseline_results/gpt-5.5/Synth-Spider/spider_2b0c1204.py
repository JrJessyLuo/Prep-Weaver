import pandas as pd

users = tables["table_2"]
addresses = tables["table_1"]

out = (
    users.loc[users["first_name"].astype(str).str.strip().str.lower() == "robbie", ["user_address_id"]]
    .merge(addresses[["address_id", "country"]], left_on="user_address_id", right_on="address_id", how="left")
    .loc[:, ["country"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"country": out}
