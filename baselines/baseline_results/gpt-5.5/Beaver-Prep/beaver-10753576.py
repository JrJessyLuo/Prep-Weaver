import pandas as pd
import numpy as np

owners = tables["table_1"].copy()
lists = tables["table_2"].copy()
members = tables["table_3"].copy()

owners["MOIRA_LIST_OWNER_KEY_NORM"] = owners["MOIRA_LIST_OWNER_KEY"].astype(str).str.strip()
lists["MOIRA_LIST_KEY_NORM"] = lists["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()
members["MOIRA_LIST_KEY_NORM"] = members["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()
members["MOIRA_LIST_OWNER_KEY_NORM"] = members["MOIRA_LIST_OWNER_KEY"].astype(str).str.strip()

mailing_lists = lists[lists["IS_MOIRA_MAILING_LIST"].astype(str).str.strip().str.upper().eq("Y")].copy()
mailing_lists["member_visibility"] = np.where(
    mailing_lists["IS_PUBLIC"].astype(str).str.strip().str.upper().eq("Y"),
    "Public Members",
    "Hidden Members"
)

df = (
    members.merge(
        mailing_lists[["MOIRA_LIST_KEY_NORM", "member_visibility"]],
        on="MOIRA_LIST_KEY_NORM",
        how="inner"
    )
    .merge(
        owners[["MOIRA_LIST_OWNER_KEY_NORM", "OWNER", "OWNER_TYPE"]],
        on="MOIRA_LIST_OWNER_KEY_NORM",
        how="left"
    )
)

count_col = "COUNTER" if "COUNTER" in df.columns else None

if count_col:
    detail = (
        df.groupby(["OWNER", "OWNER_TYPE", "member_visibility"], dropna=False, as_index=False)[count_col]
        .sum()
        .rename(columns={count_col: "number_of_members"})
    )
    totals = (
        df.groupby(["OWNER", "OWNER_TYPE"], dropna=False, as_index=False)[count_col]
        .sum()
        .rename(columns={count_col: "number_of_members"})
    )
else:
    detail = (
        df.groupby(["OWNER", "OWNER_TYPE", "member_visibility"], dropna=False)
        .size()
        .reset_index(name="number_of_members")
    )
    totals = (
        df.groupby(["OWNER", "OWNER_TYPE"], dropna=False)
        .size()
        .reset_index(name="number_of_members")
    )

totals["member_visibility"] = pd.NA
totals = totals[["OWNER", "OWNER_TYPE", "member_visibility", "number_of_members"]]

answer = pd.concat(
    [detail[["OWNER", "OWNER_TYPE", "member_visibility", "number_of_members"]], totals],
    ignore_index=True
).sort_values(
    ["OWNER", "OWNER_TYPE", "member_visibility"],
    na_position="last"
).reset_index(drop=True)

result = {"mailing_list_member_visibility_counts": answer}
