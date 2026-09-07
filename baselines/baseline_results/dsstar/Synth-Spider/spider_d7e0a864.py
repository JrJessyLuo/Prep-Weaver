import pandas as pd

# Access pre-loaded tables
df_uni = tables['table_1']   # Universities
df_major = tables['table_2'] # Majors
df_map = tables['table_3']   # University-Major Mapping
df_rank = tables['table_4']  # Overall Ranking (not used for this query)

# Reproduce cleaning and joins per reference logic
df_major_clean = df_major.copy()
df_major_clean["Major_ID"] = pd.to_numeric(df_major_clean["Major_ID"], errors="coerce").astype("Int64")

df_map_major = df_map.merge(
    df_major_clean[["Major_ID", "Major_Name", "Major_Code"]],
    left_on="m_id",
    right_on="Major_ID",
    how="left"
)

df_u_mj = df_map_major.merge(
    df_uni,
    left_on="u_id",
    right_on="University_ID",
    how="left"
)

# Find universities that have both Accounting and Urban Education majors
majors_needed = {"Accounting", "Urban Education"}
uni_majors = df_u_mj.groupby("University_ID")["Major_Name"].apply(lambda s: set(s.dropna()))
eligible_unis = uni_majors[uni_majors.apply(lambda s: majors_needed.issubset(s))].index

answer_df = df_uni[df_uni["University_ID"].isin(eligible_unis)][["University_ID", "yxmc"]].rename(columns={"yxmc": "University_Name"}).sort_values("University_ID").reset_index(drop=True)

# Package final result
result = {"universities_with_accounting_and_urban_education": answer_df}