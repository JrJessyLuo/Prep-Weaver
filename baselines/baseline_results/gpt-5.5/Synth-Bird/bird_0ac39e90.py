import pandas as pd

# Cards
cards = tables["table_1"].copy()
cards["disp_id"] = pd.to_numeric(cards["disp_id"], errors="coerce")
cards["type"] = cards["type"].astype(str).str.lower()

# Dispositions (table_2 is a transposed/wide representation)
disp_raw = tables["table_2"].copy()
disp_long = disp_raw.melt(id_vars=["fp"], var_name="disp_id", value_name="val")
disp_long["disp_id"] = pd.to_numeric(disp_long["disp_id"], errors="coerce")

disp = (
    disp_long.pivot_table(index="disp_id", columns="fp", values="val", aggfunc="first")
    .reset_index()
)
disp["account_id"] = pd.to_numeric(disp.get("account_id"), errors="coerce")

# Accounts that have gold credit cards
gold_accounts = (
    cards.loc[cards["type"].eq("gold"), ["disp_id"]]
    .merge(disp[["disp_id", "account_id"]], on="disp_id", how="left")
    .dropna(subset=["account_id"])
    .drop_duplicates(subset=["account_id"])
    .sort_values("account_id")[["account_id"]]
    .reset_index(drop=True)
)
gold_accounts["account_id"] = gold_accounts["account_id"].astype(int)

result = {"gold_card_accounts": gold_accounts}
