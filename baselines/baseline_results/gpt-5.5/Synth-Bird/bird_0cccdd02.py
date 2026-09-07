import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()
t5 = tables["table_5"].copy()

# Districts with average salary > 10000 (A11 = average salary in the classic dataset)
salary = t2.loc[t2["district_id"].astype(str).str.strip().str.upper() == "A11", ["district_number", "value"]].copy()
salary["district_number"] = pd.to_numeric(salary["district_number"], errors="coerce")
salary["value"] = pd.to_numeric(salary["value"], errors="coerce")
high_salary_districts = set(salary.loc[salary["value"] > 10000, "district_number"].dropna().astype(int))

# Accounts opened in those districts
accounts_hsd = t3.loc[t3["district_id"].isin(high_salary_districts), ["account_id"]].drop_duplicates()

# Clients who opened (OWNERS of) those accounts
owners = t5.loc[t5["type"].astype(str).str.strip().str.upper() == "OWNER", ["client_id", "account_id"]]
clients_hsd = owners.merge(accounts_hsd, on="account_id", how="inner")[["client_id"]].drop_duplicates()

# Join to client table to get gender, normalize gender values
t1["gender_clean"] = (
    t1["gender"]
    .astype(str)
    .str.replace("'", "", regex=False)
    .str.strip()
    .str.upper()
)

clients_gender = clients_hsd.merge(t1[["client_id", "gender_clean"]], on="client_id", how="left")

total_clients = len(clients_gender)
female_clients = (clients_gender["gender_clean"] == "F").sum()
pct_women = (female_clients / total_clients * 100) if total_clients else 0.0

result = {
    "percentage_women_clients_high_salary_district": pd.DataFrame(
        {"percentage_women": [pct_women]}
    )
}
