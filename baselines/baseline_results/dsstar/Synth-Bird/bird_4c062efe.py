import pandas as pd

# Tables are already loaded in a dict named `tables`
majors_df = tables["table_1"]   # bird_4c062efe_input_0.pkl
members_df = tables["table_2"]  # bird_4c062efe_input_1.pkl

# Join members to majors
joined = members_df.merge(
    majors_df,
    how="inner",
    left_on="link_to_major",
    right_on="major_id",
    suffixes=("_member", "_major"),
)

# Filter for majors in the Art and Design Department
mask = joined["major_info"].astype(str).str.contains("Art and Design Department", case=False, na=False)
filtered = joined.loc[mask, ["first_name", "last_name"]].copy()

# Build full names (and de-duplicate)
filtered["full_name"] = filtered["first_name"].astype(str).str.strip() + " " + filtered["last_name"].astype(str).str.strip()
full_names = (
    filtered["full_name"]
    .dropna()
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
    .to_frame(name="full_name")
)

# Final answer
result = {"art_and_design_students": full_names}

# Print answer
print(result["art_and_design_students"].to_string(index=False))