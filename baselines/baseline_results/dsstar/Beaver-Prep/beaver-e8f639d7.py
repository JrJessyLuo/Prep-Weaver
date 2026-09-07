import pandas as pd

# 1) Load from provided in-scope `tables` dict
df_detail = tables["table_1"].copy()
df_list = tables["table_2"].copy()
df_owner = tables["table_3"].copy()

# 2) Normalize key dtypes for reliable joins
for c in ["MOIRA_LIST_KEY"]:
    if c in df_detail.columns:
        df_detail[c] = df_detail[c].astype("object")
    if c in df_list.columns:
        df_list[c] = df_list[c].astype("object")

if "MOIRA_LIST_OWNER_KEY" in df_detail.columns:
    df_detail["MOIRA_LIST_OWNER_KEY"] = df_detail["MOIRA_LIST_OWNER_KEY"].astype("object")
if "MOIRA_LIST_OWNER_KEY" in df_owner.columns:
    df_owner["MOIRA_LIST_OWNER_KEY"] = df_owner["MOIRA_LIST_OWNER_KEY"].astype("object")

# 3) Filter MOIRA_LIST to mailing lists only (IS_MOIRA_MAILING_LIST == 'Y')
mailing_lists = df_list.loc[df_list.get("IS_MOIRA_MAILING_LIST", pd.Series([], dtype=object)) == "Y"].copy()

# 4) Inner join detail to mailing_lists on MOIRA_LIST_KEY
detail_joined = df_detail.merge(
    mailing_lists,
    on="MOIRA_LIST_KEY",
    how="inner",
    suffixes=("", "_LIST")
)

# 5) Count members per list using MOIRA_LIST_KEY in detail_joined
# Each row in detail is a membership; count rows per list key.
if not detail_joined.empty:
    members_per_list = (
        detail_joined.groupby("MOIRA_LIST_KEY", as_index=False)
        .size()
        .rename(columns={"size": "member_count"})
    )
else:
    members_per_list = pd.DataFrame(columns=["MOIRA_LIST_KEY", "member_count"])

# 6) Merge counts back to list-level attributes and owners
#    Keep only mailing lists with observed membership counts
list_with_counts = mailing_lists.merge(members_per_list, on="MOIRA_LIST_KEY", how="inner")

# 7) Attach owners: detail -> owner key -> owner table
#    Owners are stored in MOIRA_LIST_OWNER keyed table; lists can have multiple owners.
#    Use df_detail to link list to owner_key(s), then distinct pairs to owner table.
if not df_detail.empty and "MOIRA_LIST_OWNER_KEY" in df_detail.columns:
    list_owner_keys = (
        df_detail[["MOIRA_LIST_KEY", "MOIRA_LIST_OWNER_KEY"]]
        .dropna()
        .drop_duplicates()
    )
else:
    list_owner_keys = pd.DataFrame(columns=["MOIRA_LIST_KEY", "MOIRA_LIST_OWNER_KEY"])

owners_mapped = list_owner_keys.merge(
    df_owner[["MOIRA_LIST_OWNER_KEY", "OWNER", "OWNER_TYPE"]] if not df_owner.empty else pd.DataFrame(columns=["MOIRA_LIST_OWNER_KEY", "OWNER", "OWNER_TYPE"]),
    on="MOIRA_LIST_OWNER_KEY",
    how="left"
)

# 8) Combine list attributes/counts with owners (one row per list-owner)
final = list_with_counts.merge(
    owners_mapped,
    on="MOIRA_LIST_KEY",
    how="left"
)

# 9) Determine min and max member_count across lists
if not final.empty:
    max_count = final["member_count"].max()
    min_count = final["member_count"].min()
    max_lists = final.loc[final["member_count"] == max_count].copy()
    min_lists = final.loc[final["member_count"] == min_count].copy()
else:
    max_lists = final.copy()
    min_lists = final.copy()

# 10) Select and order output columns
def select_cols(df):
    cols = []
    for c in [
        "MOIRA_LIST_KEY",
        "MOIRA_LIST_NAME",
        "OWNER",
        "OWNER_TYPE",
        "IS_PUBLIC",
        "IS_HIDDEN",
        "member_count"
    ]:
        if c in df.columns:
            cols.append(c)
    return df[cols].sort_values(["member_count", "MOIRA_LIST_NAME" if "MOIRA_LIST_NAME" in df.columns else "MOIRA_LIST_KEY"], ascending=[False, True])

max_lists_out = select_cols(max_lists)
min_lists_out = select_cols(min_lists).sort_values(["member_count", "MOIRA_LIST_NAME" if "MOIRA_LIST_NAME" in min_lists.columns else "MOIRA_LIST_KEY"], ascending=[True, True])

# 11) Package final results
result = {
    "mailing_lists_with_max_members": max_lists_out.reset_index(drop=True),
    "mailing_lists_with_min_members": min_lists_out.reset_index(drop=True),
}