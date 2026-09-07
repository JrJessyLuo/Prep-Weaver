import pandas as pd

# Tables are assumed to be preloaded in a dict named `tables`
card_df = tables["table_1"]  # bird_0ac39e90_input_0.pkl
disp_df = tables["table_2"]  # bird_0ac39e90_input_1.pkl

# Filter to gold cards and get unique disp_id
gold_disp_ids = (
    card_df.loc[card_df["type"] == "gold", "disp_id"]
    .dropna()
    .astype(int)
    .drop_duplicates()
)

# Join gold disp_id to disposition table to retrieve account_id, then distinct account_id
gold_account_ids_df = (
    disp_df.loc[disp_df["disp_id"].isin(gold_disp_ids), ["account_id"]]
    .dropna()
    .astype({"account_id": int})
    .drop_duplicates()
    .sort_values("account_id")
    .reset_index(drop=True)
)

result = {"gold_credit_card_accounts": gold_account_ids_df}