import pandas as pd

# Tables already loaded in `tables`
accounts = tables["table_1"]
loans = tables["table_2"]

# Load loans and filter to 1997
loans = loans.copy()
loans["date"] = pd.to_datetime(loans["date"], errors="coerce")
loans_1997 = loans[loans["date"].dt.year == 1997].copy()

# Parse amount_duration_payments into separate numeric fields
parts = loans_1997["amount_duration_payments"].astype(str).str.split("-", n=2, expand=True)
loans_1997["approved_amount"] = pd.to_numeric(parts[0], errors="coerce")
loans_1997["duration_months"] = pd.to_numeric(parts[1], errors="coerce")
loans_1997["monthly_payments"] = pd.to_numeric(parts[2], errors="coerce")

# Compute minimum approved amount and filter rows matching it
min_approved_amount = loans_1997["approved_amount"].min(skipna=True)
loans_1997_min_amount = loans_1997[loans_1997["approved_amount"].eq(min_approved_amount)].copy()

# Join to accounts, keep weekly frequency, output account_id(s)
joined = loans_1997_min_amount.merge(accounts, on="account_id", how="inner")
weekly_account_ids = (
    joined.loc[joined["freq_part2"].eq("TYDNE"), ["account_id"]]
    .dropna()
    .drop_duplicates()
    .sort_values("account_id")
    .reset_index(drop=True)
)

# Final answer
result = {"weekly_account_ids": weekly_account_ids}