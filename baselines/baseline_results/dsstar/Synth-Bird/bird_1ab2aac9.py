import pandas as pd

# Input tables (already loaded in `tables`)
account = tables["table_1"]
loan = tables["table_2"]

# ---------- Infer duration/amount columns in loan (reuse base-code logic) ----------
cols = list(loan.columns)
duration_candidates = [
    c for c in cols
    if any(k in str(c).lower() for k in ["dur", "valid", "term", "months"])
]
amount_candidates = [
    c for c in cols
    if any(k in str(c).lower() for k in ["amount", "approved", "credit"])
]

def to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")

dur_col = None
if duration_candidates:
    scores = [(to_num(loan[c]).notna().sum(), c) for c in duration_candidates]
    scores.sort(reverse=True)
    dur_col = scores[0][1]

amt_col = None
if amount_candidates:
    scores = [(to_num(loan[c]).notna().sum(), c) for c in amount_candidates]
    scores.sort(reverse=True)
    amt_col = scores[0][1]

if dur_col is None or amt_col is None:
    raise ValueError("Could not infer duration and/or approved amount columns from the loan table.")

# ---------- Clean keys / types ----------
acc = account.copy()
acc["_account_id_num"] = pd.to_numeric(
    acc["account_id"].astype(str).str.replace('"', "", regex=False).str.strip(),
    errors="coerce"
)
acc["_date_dt"] = pd.to_datetime(acc["date"], errors="coerce")

loan_tmp = loan.copy()
# try to find an account_id column (common in this dataset but may be named differently)
loan_account_col = None
for c in loan_tmp.columns:
    if str(c).lower() in {"account_id", "accountid", "account"}:
        loan_account_col = c
        break
if loan_account_col is None:
    raise ValueError("Could not find an account_id-like column in the loan table.")

loan_tmp["_account_id_num"] = pd.to_numeric(loan_tmp[loan_account_col], errors="coerce")
loan_tmp["_duration_num"] = to_num(loan_tmp[dur_col])
loan_tmp["_amount_num"] = to_num(loan_tmp[amt_col])

# ---------- Current plan: join, filter, max, return all accounts with that max ----------
joined = loan_tmp.merge(
    acc[["_account_id_num", "_date_dt", "district_id", "frequency", "date", "account_id"]],
    on="_account_id_num",
    how="inner"
)

subset = joined[
    (joined["_date_dt"].dt.year == 1993) &
    (joined["_duration_num"] > 12)
].copy()

max_amt = subset["_amount_num"].max()

out = subset[subset["_amount_num"] == max_amt].copy()
out["max_approved_amount_1993_opened_duration_gt_12"] = max_amt

# Prefer numeric account_id, but keep original account_id string from account table for traceability
final_df = out[[
    "_account_id_num",
    "account_id",
    "max_approved_amount_1993_opened_duration_gt_12",
    "date",
    "district_id",
    "frequency"
]].drop_duplicates().sort_values(["_account_id_num", "account_id"])

# Final answer (as required)
result = {"accounts_highest_approved_amount_1993_opened_duration_gt_12": final_df}