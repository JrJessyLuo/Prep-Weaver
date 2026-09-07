import pandas as pd
import re

# The input tables are provided in the `tables` dict
df_moira = tables['table_1'].copy()       # MOIRA_LIST_DETAIL.pkl
df_users = tables['table_10'].copy()      # WAREHOUSE_USERS.pkl

# Ensure OFFICE_LOCATION is string for pattern checks
loc = df_users["OFFICE_LOCATION"].astype(str).str.strip()

# Define patterns that indicate Building 24 (same logic as reference)
patterns = [
    r"^\s*24\s*[-–]\s*\w+",                  # e.g., "24-123", "24 – 123"
    r"^\s*24\s+\w+",                         # e.g., "24 123"
    r"\b(BLDG|BLDG\.|BUILDING|BLD)\s*24\b",  # e.g., "BLDG 24", "Building 24"
    r"^\s*24\s*$"                            # exactly "24"
]
regex = re.compile("|".join(patterns), flags=re.IGNORECASE)

# Identify Building 24 users
mask_bldg24 = loc.str.match(regex) | loc.str.contains(regex, na=False)
mit_ids_bldg24 = (
    df_users.loc[mask_bldg24, "MIT_ID"]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

# Prepare MOIRA_LIST_DETAIL MIT IDs and filter for Building 24 members
moira_member_ids = pd.to_numeric(df_moira["MOIRA_LIST_MEMBER_MIT_ID"], errors="coerce")
df_moira_b24 = df_moira.loc[moira_member_ids.isin(mit_ids_bldg24)].copy()

# Among the mailing lists subscribed by Building 24 users, find the most subscribed list
# Assume the mailing list name column is MOIRA_LIST_NAME (common in MOIRA exports).
# If different, adjust accordingly.
list_name_col_candidates = [
    "MOIRA_LIST_NAME",
    "LIST_NAME",
    "MOIRA_LIST",
    "LIST"
]
for col in list_name_col_candidates:
    if col in df_moira_b24.columns:
        list_col = col
        break
else:
    # If no expected column is found, create an empty result
    top_list_df = pd.DataFrame(columns=["mailing_list", "subscriber_count"])
    result = {"most_subscribed_mailing_list_for_building_24": top_list_df}
    # No print as per guideline; just assign result
    pass

if 'list_col' in locals():
    counts = (
        df_moira_b24
        .dropna(subset=[list_col])
        .groupby(list_col)
        .size()
        .reset_index(name="subscriber_count")
        .sort_values(["subscriber_count", list_col], ascending=[False, True])
        .head(1)
        .rename(columns={list_col: "mailing_list"})
    )

    # Assign final answer table to result as required
    result = {"most_subscribed_mailing_list_for_building_24": counts}