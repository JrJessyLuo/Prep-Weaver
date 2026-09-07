import pandas as pd

# Source tables from the provided `tables` dict
df_users = tables['table_1']  # spider_ed292888_input_0.pkl
df_properties = tables['table_2']  # spider_ed292888_input_1.pkl

# Identify join keys
join_key_users = "user_id"
join_key_properties = "owner_user_id"

# Confirm presence of keys
assert join_key_users in df_users.columns, f"Missing {join_key_users} in users"
assert join_key_properties in df_properties.columns, f"Missing {join_key_properties} in properties"

# Perform join to link property with its owner user row
df_properties_with_owner = df_properties.merge(
    df_users.add_prefix("owner_"),
    left_on=join_key_properties,
    right_on=f"owner_{join_key_users}",
    how="left",
    validate="m:1"
)

# Create owner full name as "first_name + middle_name + last_name" with proper spacing and handling NaNs/empties
def safe_str(x):
    return "" if pd.isna(x) else str(x).strip()

owner_first = df_properties_with_owner.get("owner_first_name", "")
owner_middle = df_properties_with_owner.get("owner_middle_name", "")
owner_last = df_properties_with_owner.get("owner_last_name", "")

df_properties_with_owner["owner_full_name"] = (
    owner_first.map(safe_str) + " " + owner_middle.map(safe_str) + " " + owner_last.map(safe_str)
).str.split().str.join(" ")

# Deduplicate and drop empty names if any
unique_full_names = (
    df_properties_with_owner["owner_full_name"]
    .dropna()
    .map(str.strip)
    .replace("", pd.NA)
    .dropna()
    .drop_duplicates()
    .sort_values()
)

# Prepare final answer DataFrame
answer_df = unique_full_names.to_frame(name="full_name").reset_index(drop=True)

# Assign to result as required
result = {"owners_living_in_owned_properties_full_names": answer_df}