import pandas as pd

# --- Tables ---
acc_kv = tables["table_1"].copy()
district_wide = tables["table_3"].copy()
loans = tables["table_6"].copy()

# --- Pivot account key-value table to wide ---
acc = (
    acc_kv.pivot_table(index="account_id", columns="mt", values="vl", aggfunc="first")
    .reset_index()
)

# Clean/cast account_id and district_id
acc["account_id"] = (
    acc["account_id"].astype(str).str.strip().str.replace('"', "", regex=False)
)
acc["account_id"] = pd.to_numeric(acc["account_id"], errors="coerce").astype("Int64")
acc["district_id"] = pd.to_numeric(acc.get("district_id"), errors="coerce").astype("Int64")

# --- Find district_id for 'Tabor' from table_3 row 'A2' (district names by numeric id) ---
a2 = district_wide[district_wide["district_id"].astype(str).eq("A2")]
a2_long = a2.drop(columns=["district_id"]).melt(var_name="district_id_num", value_name="district_name")
tabor_ids = a2_long[a2_long["district_name"].astype(str).eq("Tabor")]["district_id_num"]
tabor_district_id = pd.to_numeric(tabor_ids, errors="coerce").dropna().astype(int).iloc[0] if len(tabor_ids) else 21

# --- Eligible loans: keep good-standing statuses (A, C) ---
eligible_accounts = loans[loans["status"].isin(["A", "C"])]["account_id"].dropna().unique()

# --- Filter accounts in Tabor and eligible for loans ---
out = (
    acc[acc["district_id"].eq(tabor_district_id) & acc["account_id"].isin(eligible_accounts)]
    [["account_id"]]
    .dropna()
    .drop_duplicates()
    .sort_values("account_id")
    .reset_index(drop=True)
)

result = {"tabor_eligible_loan_accounts": out}
