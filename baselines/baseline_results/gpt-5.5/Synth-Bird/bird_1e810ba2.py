import pandas as pd

majors = tables["table_1"]
kv = tables["table_2"]

# Pivot key-value member attributes to wide format
members_wide = (
    kv.pivot_table(index="member_id", columns="shuxing", values="zhi", aggfunc="first")
      .reset_index()
)

# Extract major_id(s) from link_to_major (handles possible packed strings / lists)
member_major = members_wide[["member_id", "link_to_major"]].dropna(subset=["link_to_major"]).copy()
member_major["major_id"] = member_major["link_to_major"].astype(str).str.findall(r"rec[A-Za-z0-9]+")
member_major = member_major.explode("major_id").dropna(subset=["major_id"])

# Join to majors and count distinct members with major "Environmental Engineering"
mm = member_major.merge(majors[["major_id", "major_name"]], on="major_id", how="left")
count_env = mm.loc[mm["major_name"].str.casefold().eq("environmental engineering"), "member_id"].nunique()

result = {
    "environmental_engineering_major_members_count": pd.DataFrame(
        {"number_of_members": [count_env]}
    )
}
