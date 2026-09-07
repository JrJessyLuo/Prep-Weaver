import pandas as pd

# Access pre-loaded tables
df_univ = tables['table_1']
df_rank = tables['table_2']

# Construct University_ID from ID_Tens and ID_Units in ranking DF
rank_ids = (
    df_rank
    .assign(
        ID_Tens_num=pd.to_numeric(df_rank["ID_Tens"], errors="coerce").fillna(0).astype(int),
        ID_Units_num=pd.to_numeric(df_rank["ID_Units"], errors="coerce").fillna(0).astype(int),
    )
    .assign(University_ID=lambda d: d["ID_Tens_num"] * 10 + d["ID_Units_num"])
)

# Keep relevant fields including Research_point and constructed University_ID
rank_with_uid = rank_ids[["Rank", "Research_point", "University_ID"]]

# Merge to get university names with research points
merged = df_univ.merge(rank_with_uid, on="University_ID", how="left")

# Determine the university/universities with the maximum Research_point
max_rp = merged["Research_point"].max()
top_univ = merged.loc[merged["Research_point"] == max_rp].copy()

# Create a readable university name by combining prefix and suffix (strip to handle blanks)
top_univ["University_Name"] = (top_univ["Uni_Name_Prefix"].fillna("").str.strip() + " " + top_univ["Uni_Name_Suffix"].fillna("").str.strip()).str.strip()
top_univ.loc[top_univ["University_Name"] == "", "University_Name"] = top_univ["Uni_Name_Prefix"].fillna("").str.strip()

# Final answer: university name(s) with the most research points
answer_df = top_univ[["University_ID", "University_Name", "Research_point"]].drop_duplicates().sort_values(["Research_point", "University_ID"], ascending=[False, True]).reset_index(drop=True)

# Assign to result as required
result = {"top_research_university": answer_df}