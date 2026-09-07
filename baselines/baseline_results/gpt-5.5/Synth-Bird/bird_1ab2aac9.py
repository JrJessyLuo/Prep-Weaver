import pandas as pd

# --- Accounts table (opening date in 1993) ---
acc = tables["table_1"].copy()
acc["account_id"] = (
    acc["account_id"].astype(str)
    .str.strip()
    .str.replace('"', "", regex=False)
    .str.replace("'", "", regex=False)
)
acc["account_id"] = pd.to_numeric(acc["account_id"], errors="coerce").astype("Int64")
acc["account_opening_date"] = pd.to_datetime(acc["date"], errors="coerce")
acc_1993 = acc.loc[acc["account_opening_date"].dt.year.eq(1993), ["account_id", "account_opening_date"]].dropna()

# --- Loans table (repair from transposed/wide to normal) ---
loans_raw = tables["table_2"].copy()
loans = (
    loans_raw.set_index("loan_id")
    .T.reset_index()
    .rename(columns={"index": "loan_id"})
)
# keep only expected columns if present
expected_cols = ["loan_id", "account_id", "date", "amount", "duration", "payments"]
loans = loans[[c for c in expected_cols if c in loans.columns]]

loans["loan_id"] = pd.to_numeric(loans["loan_id"], errors="coerce").astype("Int64")
loans["account_id"] = pd.to_numeric(loans["account_id"], errors="coerce").astype("Int64")
loans["amount"] = pd.to_numeric(loans["amount"], errors="coerce")
loans["duration"] = pd.to_numeric(loans["duration"], errors="coerce")
if "date" in loans.columns:
    loans["loan_date"] = pd.to_datetime(loans["date"], errors="coerce")

# --- Filter: loan validity (duration) > 12 months, opening date in 1993 ---
loans_gt12 = loans.loc[loans["duration"] > 12, ["account_id", "amount"]].dropna()
m = loans_gt12.merge(acc_1993, on="account_id", how="inner")

# --- Highest approved amount among these accounts ---
max_amt = m["amount"].max()
out = (
    m.loc[m["amount"].eq(max_amt), ["account_id", "amount", "account_opening_date"]]
    .drop_duplicates()
    .rename(columns={"amount": "approved_amount"})
    .sort_values(["approved_amount", "account_id"], ascending=[False, True])
    .reset_index(drop=True)
)

result = {"highest_approved_amount_accounts_1993": out}
