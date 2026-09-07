import pandas as pd

owners = tables["table_1"].copy()
members = tables["table_2"].copy()
lists = tables["table_4"].copy()
employees = tables["table_8"].copy()

# Normalize keys used for joins
members["_list_key_norm"] = members["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()
members["_owner_key_norm"] = members["MOIRA_LIST_OWNER_KEY"].astype(str).str.strip().str.upper()
members["_member_login_norm"] = members["moira_list_member"].astype(str).str.strip().str.upper()

lists["_list_key_norm"] = lists["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()

owners["_owner_key_norm"] = owners["MOIRA_LIST_OWNER_KEY"].astype(str).str.strip().str.upper()
owners["_owner_norm"] = owners["OWNER"].astype(str).str.strip().str.upper()

employees["_member_login_norm"] = employees["KRB_NAME_UPPERCASE"].astype(str).str.strip().str.upper()
employees["_dept_name_norm"] = employees["HR_DEPARTMENT_NAME"].astype(str).str.strip()

# Subscribers who work in departments whose names start with "Computer Science"
cs_employees = employees[
    employees["_dept_name_norm"].str.startswith("Computer Science", na=False)
][["_member_login_norm"]].drop_duplicates()

# Mailing lists only
mailing_lists = lists[
    lists["IS_MOIRA_MAILING_LIST"].astype(str).str.strip().str.upper().eq("Y")
][["_list_key_norm", "MOIRA_LIST_NAME"]].drop_duplicates()

# Keep memberships for CS subscribers on mailing lists
qualified = (
    members.merge(cs_employees, on="_member_login_norm", how="inner")
           .merge(mailing_lists, on="_list_key_norm", how="inner")
           .merge(
               owners[["_owner_key_norm", "OWNER", "OWNER_TYPE", "_owner_norm"]].drop_duplicates(),
               on="_owner_key_norm",
               how="left"
           )
)

# Detail rows: one row per ownership type and mailing list
detail = (
    qualified.groupby(["OWNER_TYPE", "MOIRA_LIST_NAME"], dropna=False)
    .agg(
        NUMBER_OF_OWNERS=("_owner_norm", "nunique"),
        NUMBER_OF_SUBSCRIBERS=("_member_login_norm", "nunique")
    )
    .reset_index()
    .rename(columns={
        "OWNER_TYPE": "_OWNER_TYPE",
        "MOIRA_LIST_NAME": "LIST_NAME"
    })
)

detail["_OWNER_TYPE"] = detail["_OWNER_TYPE"].fillna("")
detail = detail.sort_values(["_OWNER_TYPE", "LIST_NAME"], kind="mergesort").reset_index(drop=True)

rows = []
for owner_type, group in detail.groupby("_OWNER_TYPE", sort=False):
    first = True
    for _, r in group.iterrows():
        rows.append({
            "OWNERSHIP_TYPE": owner_type if first else "",
            "LIST_NAME": r["LIST_NAME"],
            "NUMBER_OF_OWNERS": int(r["NUMBER_OF_OWNERS"]),
            "NUMBER_OF_SUBSCRIBERS": int(r["NUMBER_OF_SUBSCRIBERS"])
        })
        first = False

    rows.append({
        "OWNERSHIP_TYPE": "SUBTOTAL",
        "LIST_NAME": owner_type,
        "NUMBER_OF_OWNERS": int(group["NUMBER_OF_OWNERS"].sum()),
        "NUMBER_OF_SUBSCRIBERS": int(group["NUMBER_OF_SUBSCRIBERS"].sum())
    })

rows.append({
    "OWNERSHIP_TYPE": "TOTAL",
    "LIST_NAME": "",
    "NUMBER_OF_OWNERS": int(detail["NUMBER_OF_OWNERS"].sum()) if not detail.empty else 0,
    "NUMBER_OF_SUBSCRIBERS": int(detail["NUMBER_OF_SUBSCRIBERS"].sum()) if not detail.empty else 0
})

answer = pd.DataFrame(
    rows,
    columns=["OWNERSHIP_TYPE", "LIST_NAME", "NUMBER_OF_OWNERS", "NUMBER_OF_SUBSCRIBERS"]
)

result = {"mailing_list_ownership_summary": answer}
