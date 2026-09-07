import pandas as pd

# Tables (already loaded in scope)
account_eav = tables["table_1"]   # bird_da11c438_input_0.pkl
district_df = tables["table_3"]   # bird_da11c438_input_2.pkl
loan_df = tables["table_6"]       # financial_loan.pkl

# ----------------------------
# 1) Recompute Tabor district_id from district table
# ----------------------------
matches = {}
for col in district_df.columns:
    s = district_df[col].astype(str).str.strip().str.lower()
    mask = s.eq("tabor")
    if mask.any():
        matches[col] = district_df.loc[mask, ["district_id", col]]

if not matches:
    raise ValueError('Could not find district name "Tabor" in the district table.')

tabor_match_df = pd.concat(matches.values(), ignore_index=True).drop_duplicates()

tabor_match_df["district_id_norm"] = pd.to_numeric(
    tabor_match_df["district_id"].astype(str).str.strip().str.strip('"'),
    errors="coerce"
)

tabor_ids = (
    tabor_match_df.loc[tabor_match_df["district_id_norm"].notna(), "district_id_norm"]
    .astype(int)
    .unique()
    .tolist()
)

if len(tabor_ids) != 1:
    raise ValueError(f"Expected exactly 1 district_id for 'Tabor', found: {tabor_ids}")

tabor_district_id = tabor_ids[0]

# ----------------------------
# 2) Filter/join after normalizing account_id types and verifying district_id match
# ----------------------------
district_rows = account_eav.loc[
    account_eav["mt"].astype(str).str.strip().str.lower().eq("district_id")
].copy()

district_rows["account_id_int"] = pd.to_numeric(
    district_rows["account_id"].astype(str).str.strip().str.strip('"'),
    errors="coerce"
).astype("Int64")

district_rows["district_id_int"] = pd.to_numeric(
    district_rows["vl"].astype(str).str.strip().str.strip('"'),
    errors="coerce"
).astype("Int64")

tabor_accounts = (
    district_rows.loc[district_rows["district_id_int"].eq(tabor_district_id), ["account_id_int"]]
    .dropna()
    .drop_duplicates()
    .rename(columns={"account_id_int": "account_id"})
)

loan_df = loan_df.copy()
loan_df["account_id"] = pd.to_numeric(loan_df["account_id"], errors="coerce").astype("Int64")

eligible_accounts_df = (
    tabor_accounts.merge(
        loan_df[["account_id"]].drop_duplicates(),
        on="account_id",
        how="inner"
    )
    .dropna()
    .drop_duplicates()
    .sort_values("account_id")
    .reset_index(drop=True)
)

result = {"tabor_loan_eligible_accounts": eligible_accounts_df}