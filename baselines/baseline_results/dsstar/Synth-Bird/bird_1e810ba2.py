import pandas as pd

# tables['table_1'] = majors lookup
# tables['table_2'] = Student_Club members EAV table
df_majors = tables["table_1"]
df_members_eav = tables["table_2"]

# Filter member-major links
df_member_major = df_members_eav[df_members_eav["shuxing"] == "link_to_major"].copy()
df_member_major = df_member_major.rename(columns={"zhi": "major_id"})

# Count members per major_id
major_counts = df_member_major["major_id"].value_counts(dropna=False)

# Join with majors to get major_name
df_major_counts_named = (
    major_counts.rename_axis("major_id").reset_index(name="member_count")
    .merge(df_majors, on="major_id", how="left")
)

# Filter Environmental Engineering and return count
env_mask = df_major_counts_named["major_name"].str.fullmatch("Environmental Engineering", na=False)
answer_df = df_major_counts_named.loc[env_mask, ["member_count"]].copy()

if answer_df.empty:
    answer_df = pd.DataFrame({"member_count": [0]})

result = {"environmental_engineering_member_count": answer_df}