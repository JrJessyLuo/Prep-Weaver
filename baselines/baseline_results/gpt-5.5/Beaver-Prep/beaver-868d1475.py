import pandas as pd

target_list = "kangaroo-inspire-yearn"

students = tables["table_2"].copy()
students["_email_norm"] = students["EMAIL_ADDRESS"].astype("string").str.strip().str.lower()
students["_krb_norm"] = students["_email_norm"].str.split("@", n=1).str[0]

# Fill department names from department reference table if needed
if "table_1" in tables:
    dept_ref = tables["table_1"][["DEPARTMENT_CODE", "DEPARTMENT_NAME"]].drop_duplicates()
    dept_ref["_dept_code_norm"] = dept_ref["DEPARTMENT_CODE"].astype("string").str.strip().str.upper()
    students["_dept_code_norm"] = students["DEPARTMENT"].astype("string").str.strip().str.upper()
    students = students.merge(
        dept_ref[["_dept_code_norm", "DEPARTMENT_NAME"]].rename(columns={"DEPARTMENT_NAME": "_dept_name_ref"}),
        on="_dept_code_norm",
        how="left",
    )
    students["DEPARTMENT_NAME"] = students["DEPARTMENT_NAME"].fillna(students["_dept_name_ref"])

def norm_series(s):
    return s.astype("string").str.strip().str.lower()

member_parts = []

# Look for a table containing Moira/list membership rows
for _, df in tables.items():
    cols_upper = {c: str(c).strip().upper() for c in df.columns}

    list_cols = [
        c for c, u in cols_upper.items()
        if (
            u in {"MOIRA_LIST_NAME", "MOIRA_LIST_KEY", "LIST_NAME", "LIST_KEY"}
            or ("MOIRA" in u and "LIST" in u and ("NAME" in u or "KEY" in u))
        )
    ]

    if not list_cols:
        continue

    mask = pd.Series(False, index=df.index)
    for c in list_cols:
        mask |= norm_series(df[c]).eq(target_list)

    if not mask.any():
        continue

    member_cols = [
        c for c, u in cols_upper.items()
        if c not in list_cols
        and (
            "MEMBER" in u
            or "EMAIL" in u
            or "KRB" in u
            or "KERBEROS" in u
            or u in {"USERNAME", "USER_NAME", "LOGIN", "ATHENA_USERNAME", "MIT_ID"}
        )
        and not u.startswith("IS_")
    ]

    for c in member_cols:
        vals = df.loc[mask, c].dropna().astype("string").str.strip()
        vals = vals[vals.ne("")]
        if not vals.empty:
            member_parts.append(vals.rename("member"))

if member_parts:
    members = pd.concat(member_parts, ignore_index=True).drop_duplicates()
else:
    members = pd.Series([], dtype="string", name="member")

members_norm = members.astype("string").str.strip().str.lower()
member_emails = set(members_norm[members_norm.str.contains("@", na=False)])
member_krbs = set(members_norm[~members_norm.str.contains("@", na=False)])

# If list members are MIT IDs, map them through the directory table when available
if "table_4" in tables and not members_norm.empty:
    numeric_members = set(members_norm[members_norm.str.fullmatch(r"\d+", na=False)])
    if numeric_members:
        directory = tables["table_4"].copy()
        directory["_mit_id_norm"] = directory["MIT_ID"].astype("string").str.strip()
        directory["_email_norm"] = directory["EMAIL_ADDRESS"].astype("string").str.strip().str.lower()
        mapped_emails = directory.loc[
            directory["_mit_id_norm"].isin(numeric_members),
            "_email_norm"
        ].dropna()
        member_emails.update(mapped_emails.tolist())

list_students = students[
    students["_email_norm"].isin(member_emails) | students["_krb_norm"].isin(member_krbs)
].drop_duplicates(subset=["_email_norm"])

total_students = len(list_students)

if total_students == 0:
    final = pd.DataFrame(columns=["department_name", "number_of_students", "percentage"])
else:
    final = (
        list_students
        .dropna(subset=["DEPARTMENT_NAME"])
        .groupby("DEPARTMENT_NAME", as_index=False)
        .agg(number_of_students=("_email_norm", "nunique"))
        .rename(columns={"DEPARTMENT_NAME": "department_name"})
    )
    final["percentage"] = final["number_of_students"] / total_students * 100
    final = final.sort_values(
        ["number_of_students", "department_name"],
        ascending=[False, True]
    ).reset_index(drop=True)

result = {"department_student_percentages": final}
