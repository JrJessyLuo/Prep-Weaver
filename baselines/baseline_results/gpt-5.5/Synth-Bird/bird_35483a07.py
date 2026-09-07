import pandas as pd

# Accounts with monthly statement issuance
accounts = tables["table_1"].copy()
monthly_accounts = accounts.loc[accounts["frequency"].eq("POPLATEK MESICNE"), ["account_id"]].drop_duplicates()

# Loans: take only the "amount" metric rows to get one row per loan
loans_kv = tables["table_2"].copy()
loans_amount = loans_kv.loc[loans_kv["metric"].eq("amount"), ["loan_id", "account_id", "date", "status", "value"]].copy()
loans_amount = loans_amount.rename(columns={"value": "amount"})
loans_amount["date"] = pd.to_datetime(loans_amount["date"], errors="coerce")

# Filter date range, amount threshold, and approved status
start = pd.Timestamp("1995-01-01")
end = pd.Timestamp("1997-12-31")

filtered = loans_amount[
    loans_amount["date"].between(start, end, inclusive="both")
    & (loans_amount["amount"] >= 250000)
    & loans_amount["status"].eq("A")
]

# Keep only loans belonging to monthly-statement accounts
filtered = filtered.merge(monthly_accounts, on="account_id", how="inner")

result = {
    "approved_loans_count": pd.DataFrame(
        {"approved_loans_count": [filtered["loan_id"].nunique()]}
    )
}
