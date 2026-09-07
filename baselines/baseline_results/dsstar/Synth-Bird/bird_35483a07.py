import pandas as pd

# Source tables from the provided `tables` dict
accounts = tables["table_1"]       # bird_35483a07_input_0.pkl
loan_metrics = tables["table_2"]   # bird_35483a07_input_1.pkl

# Large loan amounts (for downstream join)
large_loan_amounts = (
    loan_metrics.loc[
        (loan_metrics["metric"] == "amount") & (loan_metrics["value"] >= 250000),
        ["loan_id", "account_id", "date"],
    ]
    .copy()
)

# 1) Filter loan table to date range and approved status ("A")
loan_filtered = loan_metrics.copy()
loan_filtered["date"] = pd.to_datetime(loan_filtered["date"], errors="coerce")
loan_filtered = loan_filtered.loc[
    loan_filtered["date"].between("1995-01-01", "1997-12-31") & (loan_filtered["status"] == "A")
].copy()

# 2) Join to account table on account_id
loan_with_accounts = loan_filtered.merge(
    accounts[["account_id", "frequency"]],
    on="account_id",
    how="inner",
)

# 3) Keep only accounts with monthly fee frequency
loan_with_accounts = loan_with_accounts.loc[
    loan_with_accounts["frequency"] == "POPLATEK MESICNE"
].copy()

# 4) Join to the large amount subset on loan_id, then count distinct loan_id
joined = loan_with_accounts.merge(
    large_loan_amounts[["loan_id"]].drop_duplicates(),
    on="loan_id",
    how="inner",
)
distinct_loan_id_count = joined["loan_id"].nunique()

# Final answer as required: dict[str, pd.DataFrame]
answer_df = pd.DataFrame({"approved_large_loans_count": [distinct_loan_id_count]})
result = {"answer": answer_df}