import pandas as pd

# tables are assumed to be already loaded in scope as a dict of DataFrames:
# tables['table_2'] -> dispositions (bird_a3f180fc_input_1.pkl)
# tables['table_5'] -> client (financial_client.pkl)

disp = tables["table_2"]
client = tables["table_5"]

# Identify clients who have a DISPONENT row (attribute == "type" and value == "DISPONENT")
disponent_clients = set(
    disp.loc[(disp["attribute"] == "type") & (disp["value"] == "DISPONENT"), "client_id"]
    .dropna()
    .unique()
)

# Filter to OWNER dispositions and exclude clients who also appear as DISPONENT anywhere
owners_only = (
    disp.loc[(disp["attribute"] == "type") & (disp["value"] == "OWNER"), ["client_id", "account_id"]]
    .drop_duplicates()
)
owners_only = owners_only.loc[~owners_only["client_id"].isin(disponent_clients)].reset_index(drop=True)

# Join OWNER-only dispositions to client on client_id, then select distinct client_id and district_id
answer_df = (
    owners_only.merge(client[["client_id", "district_id"]], on="client_id", how="inner")
    .loc[:, ["client_id", "district_id"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Final answer assigned per guidelines
result = {"owner_only_client_district": answer_df}