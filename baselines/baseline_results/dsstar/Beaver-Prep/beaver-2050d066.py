import pandas as pd

# Load input tables from the provided 'tables' dict
df_list = tables['table_1']          # MOIRA_LIST.pkl
df_detail = tables['table_2']        # MOIRA_LIST_DETAIL.pkl
df_owner = tables['table_3']         # MOIRA_LIST_OWNER.pkl

# Filter MOIRA_LIST to active lists (IS_ACTIVE == 'Y'),
# mailing lists (IS_MOIRA_MAILING_LIST == 'Y'),
# names starting with 'A' (case-insensitive)
df_list_filtered = df_list[
    (df_list["IS_ACTIVE"] == "Y")
    & (df_list["IS_MOIRA_MAILING_LIST"] == "Y")
    & (df_list["MOIRA_LIST_NAME"].str.startswith("A", na=False, case=False))
].copy()

# Compute member counts per MOIRA_LIST_KEY from MOIRA_LIST_DETAIL
member_counts = (
    df_detail.groupby("MOIRA_LIST_KEY", dropna=False)
    .size()
    .reset_index(name="member_count")
)

# Keep only those with counts > 1000
member_counts_gt_1000 = member_counts[member_counts["member_count"] > 1000]

# Join filtered lists with counts > 1000
lists_over_1000 = df_list_filtered.merge(
    member_counts_gt_1000, on="MOIRA_LIST_KEY", how="inner", validate="one_to_one"
)

# Bring in owner information: join MOIRA_LIST_DETAIL -> MOIRA_LIST_OWNER on MOIRA_LIST_OWNER_KEY
detail_owner = df_detail.merge(
    df_owner, on="MOIRA_LIST_OWNER_KEY", how="left", validate="many_to_one"
)

# Determine a single owner per list:
# Prefer OWNER where available; if multiple owners exist, pick the first non-null OWNER per list.
owners_per_list = (
    detail_owner[["MOIRA_LIST_KEY", "OWNER"]]
    .drop_duplicates()
    .sort_values(["MOIRA_LIST_KEY"])
    .groupby("MOIRA_LIST_KEY", as_index=False)
    .agg(OWNER=("OWNER", "first"))
)

# Final join to attach owner and select requested fields
final_df = (
    lists_over_1000.merge(owners_per_list, on="MOIRA_LIST_KEY", how="left", validate="one_to_one")
    .sort_values(["member_count", "MOIRA_LIST_NAME"], ascending=[False, True])
)

# Prepare the final answer with required columns:
# - name (MOIRA_LIST_NAME)
# - whether it is a mailing list (IS_MOIRA_MAILING_LIST)
# - whether it is a moira group (IS_MOIRA_GROUP)  [assumed column in MOIRA_LIST]
# - whether it is a NFS group (IS_NFS_GROUP)      [assumed column in MOIRA_LIST]
# - the owner of the mailing list (OWNER)
# - the number of people in the list (member_count)
columns_available = [c for c in [
    "MOIRA_LIST_NAME",
    "IS_MOIRA_MAILING_LIST",
    "IS_MOIRA_GROUP",
    "IS_NFS_GROUP",
    "OWNER",
    "member_count",
] if c in final_df.columns]

answer_df = final_df[columns_available].copy()

# Package final result as required
result = {
    "mailing_lists_A_over_1000": answer_df
}