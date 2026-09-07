import pandas as pd

users = tables["table_1"].copy()
props = tables["table_2"].copy()

# Users who live at an address that is also the address of a property they own
owned_and_lived = users.merge(
    props,
    left_on=["user_id", "user_address_id"],
    right_on=["owner_user_id", "property_address_id"],
    how="inner"
)

# Build full name (skip missing/blank middle names)
name_parts = owned_and_lived[["first_name", "middle_name", "last_name"]].fillna("").astype(str)
owned_and_lived["full_name"] = (
    name_parts["first_name"].str.strip() + " " +
    name_parts["middle_name"].str.strip() + " " +
    name_parts["last_name"].str.strip()
).str.replace(r"\s+", " ", regex=True).str.strip()

out = owned_and_lived[["full_name"]].drop_duplicates().reset_index(drop=True)

result = {"users_living_in_owned_properties": out}
