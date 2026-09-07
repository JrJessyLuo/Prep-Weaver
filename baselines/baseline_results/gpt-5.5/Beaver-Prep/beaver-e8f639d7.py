import pandas as pd

members = tables["table_1"].copy()
lists = tables["table_2"].copy()
owners = tables["table_3"].copy()

# Normalize keys and flags
members["list_key_norm"] = members["MOIRA_LIST_KEY"].astype("string").str.strip().str.lower()
members["member_norm"] = members["moira_list_member"].astype("string").str.strip().str.lower()
members["owner_key_norm"] = members["MOIRA_LIST_OWNER_KEY"].astype("string").str.strip()

lists["list_key_norm"] = lists["MOIRA_LIST_KEY"].astype("string").str.strip().str.lower()
lists["is_mailing_norm"] = lists["IS_MOIRA_MAILING_LIST"].astype("string").str.strip().str.upper()
lists["public_status"] = lists["IS_PUBLIC"].astype("string").str.strip().str.upper()
lists["hidden_status"] = lists["IS_HIDDEN"].astype("string").str.strip().str.upper()

mailing_lists = (
    lists.loc[lists["is_mailing_norm"].eq("Y"),
              ["list_key_norm", "MOIRA_LIST_NAME", "public_status", "hidden_status"]]
    .drop_duplicates(subset=["list_key_norm"])
)

# Count distinct members per mailing list
members_for_mailing = members[members["list_key_norm"].isin(mailing_lists["list_key_norm"])].copy()

member_counts = (
    members_for_mailing
    .dropna(subset=["list_key_norm", "member_norm"])
    .drop_duplicates(subset=["list_key_norm", "member_norm"])
    .groupby("list_key_norm", as_index=False)
    .size()
    .rename(columns={"size": "number_of_members"})
)

list_counts = mailing_lists.merge(member_counts, on="list_key_norm", how="inner")

final_columns = [
    "mailing_list_name",
    "owner",
    "public_status",
    "hidden_status",
    "number_of_members"
]

if list_counts.empty:
    out = pd.DataFrame(columns=final_columns)
else:
    min_members = list_counts["number_of_members"].min()
    max_members = list_counts["number_of_members"].max()

    extrema_lists = list_counts[
        list_counts["number_of_members"].isin([min_members, max_members])
    ].copy()

    # Resolve owner names; keep one final row per owner
    owners["owner_key_norm"] = owners["MOIRA_LIST_OWNER_KEY"].astype("string").str.strip()
    owner_lookup = owners[["owner_key_norm", "OWNER"]].drop_duplicates()

    list_owners = (
        members_for_mailing[["list_key_norm", "owner_key_norm"]]
        .dropna(subset=["list_key_norm", "owner_key_norm"])
        .drop_duplicates()
        .merge(owner_lookup, on="owner_key_norm", how="left")
    )

    fallback_owner = list_owners["owner_key_norm"].str.replace(r"^(USER|LIST)", "", regex=True)
    list_owners["owner"] = list_owners["OWNER"].combine_first(fallback_owner)

    out = (
        extrema_lists
        .merge(list_owners[["list_key_norm", "owner"]].drop_duplicates(),
               on="list_key_norm", how="left")
        .rename(columns={"MOIRA_LIST_NAME": "mailing_list_name"})
        [final_columns]
        .sort_values(
            by=["number_of_members", "mailing_list_name", "owner"],
            ascending=[False, True, True],
            na_position="last"
        )
        .reset_index(drop=True)
    )

result = {
    "mailing_lists_with_largest_and_least_members": out
}
