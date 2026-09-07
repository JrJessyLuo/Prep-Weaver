import pandas as pd

owner_key = "LIST69.377-keeper-xenon"

members = tables["table_1"].copy()
owners = tables["table_2"].copy()
lists = tables["table_3"].copy()

members["owner_key_norm"] = members["MOIRA_LIST_OWNER_KEY"].astype(str).str.strip()
members["list_key_norm"] = members["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()

owners["owner_key_norm"] = owners["MOIRA_LIST_OWNER_KEY"].astype(str).str.strip()

lists["list_key_norm"] = lists["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()
mailing_lists = lists.loc[
    lists["IS_MOIRA_MAILING_LIST"].astype(str).str.strip().str.upper().eq("Y"),
    ["list_key_norm"]
].drop_duplicates()

filtered = members.loc[members["owner_key_norm"].eq(owner_key)].merge(
    mailing_lists,
    on="list_key_norm",
    how="inner"
)

summary = pd.DataFrame({
    "MOIRA_LIST_OWNER_KEY": [owner_key],
    "total_number_of_mailing_lists": [filtered["list_key_norm"].nunique()],
    "total_number_of_members": [filtered["COUNTER"].sum() if "COUNTER" in filtered.columns else len(filtered)]
})

summary = summary.merge(
    owners[["owner_key_norm", "OWNER"]].drop_duplicates(),
    left_on="MOIRA_LIST_OWNER_KEY",
    right_on="owner_key_norm",
    how="left"
)

summary["OWNER"] = summary["OWNER"].fillna(
    summary["MOIRA_LIST_OWNER_KEY"].str.replace(r"^LIST", "", regex=True)
)

summary = summary[[
    "OWNER",
    "total_number_of_mailing_lists",
    "total_number_of_members"
]]

result = {"mailing_list_owner_summary": summary}
