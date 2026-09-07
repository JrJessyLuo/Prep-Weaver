import pandas as pd

lists = tables["table_1"].copy()
members = tables["table_2"].copy()
owners = tables["table_3"].copy()

lists["list_key_norm"] = lists["MOIRA_LIST_KEY"].astype("string").str.strip().str.lower()
lists["list_name_clean"] = lists["MOIRA_LIST_NAME"].astype("string").str.strip()
lists["is_mailing_list_clean"] = lists["IS_MOIRA_MAILING_LIST"].astype("string").str.strip().str.upper()

members["list_key_norm"] = members["MOIRA_LIST_KEY"].astype("string").str.strip().str.lower()
members["member_norm"] = members["moira_list_member"].astype("string").str.strip().str.upper()
members["owner_key_norm"] = members["MOIRA_LIST_OWNER_KEY"].astype("string").str.strip()

owners["owner_key_norm"] = owners["MOIRA_LIST_OWNER_KEY"].astype("string").str.strip()

valid_members = members[
    members["member_norm"].notna()
    & members["member_norm"].ne("")
    & members["member_norm"].ne("NAN")
]

member_counts = (
    valid_members.groupby("list_key_norm", as_index=False)
    .agg(
        number_of_people=("member_norm", "nunique"),
        owner_key_norm=("owner_key_norm", lambda s: s.dropna().mode().iloc[0] if not s.dropna().mode().empty else pd.NA),
    )
)

owner_lookup = owners[["owner_key_norm", "OWNER"]].drop_duplicates("owner_key_norm")

eligible_lists = lists[
    lists["list_name_clean"].str[:1].str.lower().eq("a")
    & lists["is_mailing_list_clean"].eq("Y")
].drop_duplicates("list_key_norm")

out = eligible_lists.merge(member_counts, on="list_key_norm", how="inner")
out = out[out["number_of_people"] > 1000]
out = out.merge(owner_lookup, on="owner_key_norm", how="left")

out = (
    out[
        [
            "list_name_clean",
            "IS_MOIRA_MAILING_LIST",
            "IS_MOIRA_GROUP",
            "IS_NFS_GROUP",
            "OWNER",
            "number_of_people",
        ]
    ]
    .rename(
        columns={
            "list_name_clean": "mailing_list_name",
            "IS_MOIRA_MAILING_LIST": "is_mailing_list",
            "IS_MOIRA_GROUP": "is_moira_group",
            "IS_NFS_GROUP": "is_nfs_group",
            "OWNER": "owner",
        }
    )
    .sort_values("mailing_list_name", kind="stable")
    .reset_index(drop=True)
)

result = {"mailing_lists_over_1000_starting_with_a": out}
