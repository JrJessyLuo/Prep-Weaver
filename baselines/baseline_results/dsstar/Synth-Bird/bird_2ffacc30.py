import pandas as pd

# Tables already loaded in scope as `tables`
mapping_df = tables["table_1"]  # bird_2ffacc30_input_0.pkl
loan_df = tables["table_2"]     # bird_2ffacc30_input_1.pkl

# --- Find the loan(s) approved on 1994-08-25 and get associated account id(s) (zh_id) ---
target_date = "1994-08-25"
matches = loan_df.loc[loan_df["date"] == target_date, ["loan_id", "zh_id", "date", "duration", "payments", "flz"]]
account_ids = sorted(matches["zh_id"].dropna().unique().tolist())

# --- For each account_id, find district_id(s) where the account was opened (same logic as reference) ---
m = mapping_df.copy()
m["acc_id"] = m["acc_id"].astype(str)

rows = []
for account_id in account_ids:
    row = m.loc[m["acc_id"] == str(account_id)]
    if row.empty:
        raise ValueError(f"acc_id {account_id} not found in mapping table.")

    district_cols = [c for c in row.columns if c != "acc_id"]
    memberships = row[district_cols].iloc[0]
    hits = [
        int(col) for col, val in memberships.items()
        if pd.notna(val) and str(val).strip().lower() in {"1", "true", "t", "yes", "y"}
    ]
    for district_id in sorted(hits):
        rows.append({"account_id": account_id, "district_id": district_id})

answer_df = pd.DataFrame(rows).sort_values(["account_id", "district_id"]).reset_index(drop=True)

# Final required output container
result = {"account_opened_district": answer_df}