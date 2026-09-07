import pandas as pd

# Source tables from the provided `tables` dict
owner = tables['table_1']          # MOIRA_LIST_OWNER.pkl
mlist = tables['table_2']          # MOIRA_LIST.pkl
detail = tables['table_3']         # MOIRA_LIST_DETAIL.pkl

# Select only needed columns
owner_sel = owner[["MOIRA_LIST_OWNER_KEY", "OWNER", "OWNER_TYPE"]].copy()
mlist_sel = mlist[["MOIRA_LIST_KEY", "IS_PUBLIC", "IS_HIDDEN"]].copy()

# Join detail -> owner (inner, as in reference)
detail_owner = detail.merge(owner_sel, on="MOIRA_LIST_OWNER_KEY", how="inner")

# Join to list to bring visibility flags (left, as in reference)
detail_owner_list = detail_owner.merge(mlist_sel, on="MOIRA_LIST_KEY", how="left")

# Create member_visibility
detail_owner_list["member_visibility"] = detail_owner_list["IS_PUBLIC"].apply(
    lambda x: "Public Members" if str(x) == "Y" else "Hidden Members"
)

# Counts per (OWNER, OWNER_TYPE, member_visibility) — reproduces reference logic
counts_by_visibility = (
    detail_owner_list
    .groupby(["OWNER", "OWNER_TYPE", "member_visibility"], dropna=False)
    .size()
    .reset_index(name="member_count")
)

# Add mailing list dimension per question: counts per (OWNER, OWNER_TYPE, member_visibility, MOIRA_LIST_KEY)
counts_by_list = (
    detail_owner_list
    .groupby(["MOIRA_LIST_KEY", "OWNER", "OWNER_TYPE", "member_visibility"], dropna=False)
    .size()
    .reset_index(name="member_count")
)

# Grand totals per (OWNER, OWNER_TYPE) with member_visibility set to null (NaN)
grand_totals = (
    detail_owner_list
    .groupby(["OWNER", "OWNER_TYPE"], dropna=False)
    .size()
    .reset_index(name="member_count")
)
grand_totals["member_visibility"] = pd.NA
grand_totals["MOIRA_LIST_KEY"] = pd.NA
grand_totals = grand_totals[["MOIRA_LIST_KEY", "OWNER", "OWNER_TYPE", "member_visibility", "member_count"]]

# Align columns for the per-list result
counts_by_list = counts_by_list[["MOIRA_LIST_KEY", "OWNER", "OWNER_TYPE", "member_visibility", "member_count"]]

# Final result for the question:
# - For each mailing list: owner, owner type, member visibility, and number of members
# - Include grand total per owner/owner type with (owner, owner type, null, total members)
final_df = pd.concat([counts_by_list, grand_totals], ignore_index=True)

# Package final answer
result = {
    "mailing_list_member_visibility_counts": final_df
}