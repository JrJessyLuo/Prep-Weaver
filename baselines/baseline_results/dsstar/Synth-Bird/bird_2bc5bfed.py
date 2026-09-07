import pandas as pd

# Load tables from the provided in-scope dict
income = tables["table_1"]
members = tables["table_2"]

# Get Casey Mason's member_id (from base code result if available; otherwise derive from members)
if "casey_mason" in globals() and not casey_mason.empty:
    casey_member_id = casey_mason["member_id"].iloc[0]
else:
    casey_member_id = members.loc[
        (members["first_name"] == "Casey") & (members["last_name"] == "Mason"),
        "member_id"
    ].iloc[0]

# Filter income rows for Casey Mason and combine year/month/day into dates
casey_income = income.loc[income["link_to_member"] == casey_member_id].copy()
casey_income["income_date"] = pd.to_datetime(
    casey_income["year"].astype(str) + "-" +
    casey_income["month"].astype(str).str.zfill(2) + "-" +
    casey_income["day"].astype(str).str.zfill(2),
    errors="coerce"
)

answer = casey_income[["income_date"]].sort_values(["income_date"]).reset_index(drop=True)

# Final answer artifact
result = {"casey_mason_income_date": answer}