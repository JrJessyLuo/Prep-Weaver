import pandas as pd

# Tables (already loaded in scope)
client = tables["table_1"]   # bird_0cccdd02_input_0.pkl
demo = tables["table_2"]     # bird_0cccdd02_input_1.pkl
account = tables["table_3"]  # financial_account.pkl
disp = tables["table_5"]     # financial_disp.pkl

# -----------------------------
# 1) Identify districts with average salary (A11) > 10000
# -----------------------------
demo = demo.copy()
demo["district_number_int"] = pd.to_numeric(demo["district_number"], errors="coerce")
demo["value_num"] = pd.to_numeric(demo["value"], errors="coerce")

salary_dn = 11  # A11 = average salary

high_salary_districts = (
    demo.loc[
        (demo["district_number_int"] == salary_dn) & (demo["value_num"] > 10000),
        ["district_id", "district_number_int", "value_num"],
    ]
    .dropna(subset=["district_id", "value_num"])
    .sort_values("value_num", ascending=False)
    .reset_index(drop=True)
)

high_salary_district_ids = set(high_salary_districts["district_id"].astype(str).unique().tolist())

# -----------------------------
# 2) Join: accounts in those districts -> OWNER dispositions -> client gender
# -----------------------------
account = account.copy()
account["district_id_str"] = account["district_id"].astype(str)

account_hs = account.loc[
    account["district_id_str"].isin(high_salary_district_ids),
    ["account_id", "district_id"],
].copy()

disp_owner = disp.loc[disp["type"] == "OWNER", ["disp_id", "client_id", "account_id"]].copy()

acc_disp = account_hs.merge(disp_owner, on="account_id", how="inner")
acc_disp_client = acc_disp.merge(client[["client_id", "gender"]], on="client_id", how="inner")

# -----------------------------
# 3) Clean gender and compute % female among unique clients
# -----------------------------
def clean_gender(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).replace("'", "").strip().upper()
    return s if s != "" else pd.NA

acc_disp_client["gender_clean"] = acc_disp_client["gender"].map(clean_gender)

unique_clients = acc_disp_client.drop_duplicates(subset=["client_id"])

female_count = (unique_clients["gender_clean"] == "F").sum()
known_gender_count = unique_clients["gender_clean"].isin(["F", "M"]).sum()

female_pct = (female_count / known_gender_count * 100) if known_gender_count else float("nan")

# Final answer table
answer_df = pd.DataFrame(
    {"percentage_women": [female_pct]}
)

result = {"percentage_women_in_high_salary_district": answer_df}