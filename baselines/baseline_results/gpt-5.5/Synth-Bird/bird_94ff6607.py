import pandas as pd

# Load tables
acct = tables["table_1"].copy()
loan = tables["table_2"].copy()

# Parse dates
loan["date"] = pd.to_datetime(loan["date"], errors="coerce")
acct["date"] = pd.to_datetime(acct["date"], errors="coerce")

# Extract approved amount from packed field "amount_duration_payments" (amount-duration-payments)
parts = loan["amount_duration_payments"].astype(str).str.split("-", n=2, expand=True)
loan["approved_amount"] = pd.to_numeric(parts[0], errors="coerce")

# Loans approved in 1997 (interpreting "approved" as status == 'A')
loan_1997_approved = loan[(loan["status"] == "A") & (loan["date"].dt.year == 1997)].copy()

# Find lowest approved amount among those loans
min_amt = loan_1997_approved["approved_amount"].min()

# Accounts with lowest approved amount
lowest_loans = loan_1997_approved[loan_1997_approved["approved_amount"] == min_amt].copy()

# Weekly issuance statement (account frequency)
acct["is_weekly_statement"] = acct["freq_part2"].astype(str).str.contains(r"TYD|WEEK", case=False, na=False)

# Join and keep only weekly statement accounts
out = (
    lowest_loans.merge(acct[["account_id", "freq_part1", "freq_part2", "is_weekly_statement"]], on="account_id", how="inner")
    .loc[lambda d: d["is_weekly_statement"]]
    .drop_duplicates(subset=["account_id"])
    .sort_values(["account_id"])
    .rename(columns={"date": "loan_date"})
    [["account_id", "loan_id", "loan_date", "approved_amount", "freq_part1", "freq_part2"]]
    .reset_index(drop=True)
)

result = {"lowest_approved_amount_weekly_accounts": out}
