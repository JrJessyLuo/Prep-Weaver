import pandas as pd

u = tables["table_1"].copy()
maj = tables["table_2"].copy()
um = tables["table_3"].copy()

# Normalize IDs for joining/filtering
maj["Major_ID_num"] = (
    maj["Major_ID"].astype(str).str.replace('"', '', regex=False).str.strip()
)
maj["Major_ID_num"] = pd.to_numeric(maj["Major_ID_num"], errors="coerce")

target_major_ids = maj.loc[
    maj["Major_Name"].isin(["Accounting", "Urban Education"]),
    "Major_ID_num"
].dropna().astype(int).unique().tolist()

# Universities that have both target majors
uids = (
    um[um["m_id"].isin(target_major_ids)]
    .groupby("u_id")["m_id"]
    .nunique()
)
uids = uids[uids == len(set(target_major_ids))].index.tolist()

out = (
    u[u["University_ID"].isin(uids)][["yxmc"]]
    .rename(columns={"yxmc": "university_name"})
)
out["university_name"] = out["university_name"].astype(str).str.strip()
out = out.drop_duplicates().sort_values("university_name").reset_index(drop=True)

result = {"universities_with_accounting_and_urban_education": out}
