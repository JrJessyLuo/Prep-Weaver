import pandas as pd

income = tables["table_1"].copy()
members = tables["table_2"].copy()

# Find Casey Mason's member_id (case-insensitive match)
casey_ids = members.loc[
    members["first_name"].astype(str).str.strip().str.lower().eq("casey")
    & members["last_name"].astype(str).str.strip().str.lower().eq("mason"),
    "member_id"
].dropna().unique()

# Filter income records for Casey Mason
casey_income = income[income["link_to_member"].isin(casey_ids)].copy()

# Build a proper date column
casey_income["income_date"] = pd.to_datetime(
    casey_income["year"].astype(str).str.zfill(4) + "-"
    + casey_income["month"].astype(str).str.zfill(2) + "-"
    + casey_income["day"].astype(str).str.zfill(2),
    errors="coerce"
)

out = (casey_income[["income_date"]]
       .dropna()
       .drop_duplicates()
       .sort_values("income_date")
       .reset_index(drop=True))

result = {"casey_mason_income_dates": out}
