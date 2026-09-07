import pandas as pd

members = tables["table_2"].copy()
majors_kv = tables["table_1"].copy()

# Find Garrett Gerke (case-insensitive)
m = members[
    members["first_name"].astype(str).str.strip().str.lower().eq("garrett")
    & members["last_name"].astype(str).str.strip().str.lower().eq("gerke")
].copy()

# Pivot majors key-value table to wide format
majors_wide = (
    majors_kv.pivot_table(index="major_id", columns="attribute", values="value", aggfunc="first")
    .reset_index()
)

if m.empty or m["ltm"].dropna().empty:
    out = pd.DataFrame(columns=["major_name", "department"])
else:
    m = m.dropna(subset=["ltm"]).drop_duplicates(subset=["ltm"])
    out = (
        m[["ltm"]]
        .rename(columns={"ltm": "major_id"})
        .merge(majors_wide, on="major_id", how="left")
        [["major_name", "department"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

result = {"garrett_gerke_major_and_department": out}
