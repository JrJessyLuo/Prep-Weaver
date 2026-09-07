import pandas as pd

# Tables are already loaded in `tables`
majors = tables["table_1"]
members = tables["table_2"]

# Join members to majors on members.link_to_major = majors.major_id
joined = members.merge(
    majors,
    how="left",
    left_on="link_to_major",
    right_on="major_id",
    suffixes=("_member", "_major"),
)

# Filter to the target major and select last names
target_major = "Law and Constitutional Studies"
answer_df = joined.loc[joined["major_name"].eq(target_major), ["last_name"]].sort_values(
    ["last_name"], kind="stable"
)

# Final answer as required
result = {"law_and_constitutional_studies_last_names": answer_df}