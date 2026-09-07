import pandas as pd

loan = tables["table_2"].copy()
acc_wide = tables["table_1"].copy()

# Loans approved on 1994/8/25
loan["date_dt"] = pd.to_datetime(loan["date"], errors="coerce")
loans_on_date = loan[loan["date_dt"].eq(pd.Timestamp(1994, 8, 25))].copy()

# account_id -> district_id mapping from the transposed account table
district_map = (
    acc_wide[acc_wide["acc_id"].astype(str).str.lower().eq("district_id")]
    .melt(id_vars=["acc_id"], var_name="account_id", value_name="district_id")
    .drop(columns=["acc_id"])
)
district_map["account_id"] = pd.to_numeric(district_map["account_id"], errors="coerce").astype("Int64")
district_map["district_id"] = pd.to_numeric(district_map["district_id"], errors="coerce").astype("Int64")

# Join to get the branch district_id for that loan's account
out = loans_on_date.merge(district_map, left_on="zh_id", right_on="account_id", how="left")

out = out.rename(columns={"zh_id": "account_id"})[["loan_id", "account_id", "district_id"]].reset_index(drop=True)

result = {"loan_account_branch_district": out}
