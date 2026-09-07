import pandas as pd

lists = tables["table_1"].copy()
members = tables["table_9"].copy()
employees = tables["table_6"].copy()
faculty = tables["table_2"].copy()

# Normalize list keys for joining
lists["list_key_norm"] = lists["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()
members["list_key_norm"] = members["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()

# Keep Moira mailing lists and their active status
mailing_lists = lists.loc[
    lists["IS_MOIRA_MAILING_LIST"].astype(str).str.strip().str.upper().eq("Y"),
    ["list_key_norm", "MOIRA_LIST_NAME", "IS_ACTIVE"]
].drop_duplicates("list_key_norm")

# Normalize member MIT IDs
members = members.dropna(subset=["MOIRA_LIST_MEMBER_MIT_ID"]).copy()
members["MIT_ID"] = members["MOIRA_LIST_MEMBER_MIT_ID"].astype("int64")

# Identify support staff and faculty MIT IDs
support_staff_ids = set(
    employees.loc[
        employees["EMPLOYEE_TYPE"].astype(str).str.strip().str.lower().eq("support staff"),
        "MIT_ID"
    ].dropna().astype("int64")
)

faculty_ids = set(faculty["MIT_ID"].dropna().astype("int64"))

# Flag subscriber type
member_people = members[["list_key_norm", "MIT_ID"]].drop_duplicates()
member_people["is_support_staff"] = member_people["MIT_ID"].isin(support_staff_ids)
member_people["is_faculty"] = member_people["MIT_ID"].isin(faculty_ids)

# Count subscribers by list
counts = (
    member_people.groupby("list_key_norm", as_index=False)
    .agg(
        number_of_support_staff_subscribers=("is_support_staff", "sum"),
        number_of_faculty_subscribers=("is_faculty", "sum")
    )
)

# Keep lists subscribed by either support staff or faculty
counts = counts[
    (counts["number_of_support_staff_subscribers"] > 0) |
    (counts["number_of_faculty_subscribers"] > 0)
]

out = (
    counts.merge(mailing_lists, on="list_key_norm", how="inner")
    .rename(columns={
        "MOIRA_LIST_NAME": "email_list_name",
        "IS_ACTIVE": "active_status"
    })
    [[
        "email_list_name",
        "number_of_support_staff_subscribers",
        "number_of_faculty_subscribers",
        "active_status"
    ]]
    .sort_values("email_list_name")
    .reset_index(drop=True)
)

result = {
    "email_lists_by_support_staff_or_faculty_subscribers": out
}
