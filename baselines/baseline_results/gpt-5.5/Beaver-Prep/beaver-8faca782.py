import pandas as pd
import numpy as np
import re

# --- Students with last names starting with K ---
students = tables["table_2"].copy()

students_k = students[
    students["LAST_NAME"].astype(str).str.startswith("K", na=False)
].copy()

students_k["student_name"] = students_k["FULL_NAME"].fillna(
    students_k["LAST_NAME"].fillna("") + ", " + students_k["FIRST_NAME"].fillna("")
)

students_k["email_key"] = students_k["EMAIL_ADDRESS"].astype(str).str.strip().str.lower()
students_k["krb_key"] = students_k["email_key"].str.split("@").str[0]
students_k["department_key"] = students_k["DEPARTMENT_NAME"].astype(str).str.strip().str.lower()

# --- Department phone numbers ---
dept_phone_frames = []

dept_sources = [
    ("table_1", "DEPARTMENT_NAME"),
    ("table_2", "DEPARTMENT_NAME"),
    ("table_3", "UNIT_NAME"),
    ("table_5", "HR_ORG_UNIT_TITLE"),
]

for tname, dept_col in dept_sources:
    if tname in tables:
        df = tables[tname]
        if dept_col in df.columns and "OFFICE_PHONE" in df.columns:
            tmp = df[[dept_col, "OFFICE_PHONE"]].copy()
            tmp = tmp.dropna(subset=[dept_col, "OFFICE_PHONE"])
            tmp["department_key"] = tmp[dept_col].astype(str).str.strip().str.lower()
            tmp["department_phone"] = tmp["OFFICE_PHONE"].apply(
                lambda x: str(int(x)) if pd.notna(x) and float(x).is_integer() else str(x)
            )
            dept_phone_frames.append(tmp[["department_key", "department_phone"]])

if dept_phone_frames:
    dept_phones = pd.concat(dept_phone_frames, ignore_index=True).drop_duplicates()
    dept_phones = (
        dept_phones.groupby("department_key", as_index=False)["department_phone"]
        .agg(lambda s: sorted(set(s)))
    )
else:
    dept_phones = pd.DataFrame(columns=["department_key", "department_phone"])

students_k = students_k.merge(dept_phones, on="department_key", how="left")
students_k["department_phone"] = students_k["department_phone"].apply(
    lambda x: x if isinstance(x, list) else []
)

# --- Mailing list membership statistics ---
lists = tables["table_9"].copy()

for col in ["MOIRA_LIST_KEY", "MOIRA_LIST_NAME"]:
    if col in lists.columns:
        lists[col + "_clean"] = lists[col].astype(str).str.strip().str.lower()

active_mailing_lists = lists.copy()
if "IS_ACTIVE" in active_mailing_lists.columns:
    active_mailing_lists = active_mailing_lists[
        active_mailing_lists["IS_ACTIVE"].astype(str).str.upper().eq("Y")
    ]
if "IS_MOIRA_MAILING_LIST" in active_mailing_lists.columns:
    active_mailing_lists = active_mailing_lists[
        active_mailing_lists["IS_MOIRA_MAILING_LIST"].astype(str).str.upper().eq("Y")
    ]

valid_list_names = set()
if "MOIRA_LIST_NAME_clean" in active_mailing_lists.columns:
    valid_list_names |= set(active_mailing_lists["MOIRA_LIST_NAME_clean"].dropna())
if "MOIRA_LIST_KEY_clean" in active_mailing_lists.columns:
    valid_list_names |= set(active_mailing_lists["MOIRA_LIST_KEY_clean"].dropna())

membership_tables = []

for tname, df in tables.items():
    cols_lower = {c: c.lower() for c in df.columns}
    possible_list_cols = [
        c for c in df.columns
        if (
            ("list" in c.lower() or "moira" in c.lower())
            and c.lower() not in {
                "moira_list_description",
                "is_moira_mailing_list",
                "is_moira_group",
                "is_nfs_group",
                "is_public",
                "is_hidden",
                "is_active",
            }
        )
    ]
    possible_member_cols = [
        c for c in df.columns
        if (
            re.search(r"(member|krb|email|username|login|user)", c.lower())
            and "list" not in c.lower()
            and c.lower() not in {"is_active"}
        )
    ]

    for list_col in possible_list_cols:
        for member_col in possible_member_cols:
            if list_col == member_col:
                continue
            tmp = df[[list_col, member_col]].copy().dropna()
            if tmp.empty:
                continue
            tmp["list_key"] = tmp[list_col].astype(str).str.strip().str.lower()
            tmp["member_key"] = tmp[member_col].astype(str).str.strip().str.lower()

            if valid_list_names:
                tmp = tmp[tmp["list_key"].isin(valid_list_names)]

            if not tmp.empty:
                membership_tables.append(tmp[["list_key", "member_key"]])

if membership_tables:
    memberships = pd.concat(membership_tables, ignore_index=True).drop_duplicates()

    list_sizes = (
        memberships.groupby("list_key", as_index=False)["member_key"]
        .nunique()
        .rename(columns={"member_key": "mailing_list_size"})
    )

    student_keys = students_k[["email_key", "krb_key"]].copy()
    student_keys = student_keys.melt(
        value_vars=["email_key", "krb_key"],
        value_name="member_key"
    )[["member_key"]].dropna().drop_duplicates()

    student_memberships = memberships.merge(student_keys, on="member_key", how="inner")
    student_memberships = student_memberships.merge(list_sizes, on="list_key", how="left")

    mail_stats = (
        student_memberships.groupby("member_key", as_index=False)
        .agg(
            total_mailing_lists=("list_key", "nunique"),
            average_mailing_list_size=("mailing_list_size", "mean"),
        )
    )

    stats_by_email = mail_stats.rename(columns={"member_key": "email_key"})
    stats_by_krb = mail_stats.rename(columns={"member_key": "krb_key"})

    students_k = students_k.merge(
        stats_by_email[["email_key", "total_mailing_lists", "average_mailing_list_size"]],
        on="email_key",
        how="left"
    )

    students_k = students_k.merge(
        stats_by_krb[["krb_key", "total_mailing_lists", "average_mailing_list_size"]],
        on="krb_key",
        how="left",
        suffixes=("_email", "_krb")
    )

    students_k["total_mailing_lists"] = students_k[
        ["total_mailing_lists_email", "total_mailing_lists_krb"]
    ].max(axis=1).fillna(0).astype(int)

    students_k["average_mailing_list_size"] = students_k[
        ["average_mailing_list_size_email", "average_mailing_list_size_krb"]
    ].mean(axis=1)

else:
    students_k["total_mailing_lists"] = 0
    students_k["average_mailing_list_size"] = np.nan

# --- Final answer ---
answer = students_k[
    [
        "student_name",
        "department_phone",
        "total_mailing_lists",
        "average_mailing_list_size",
    ]
].copy()

answer = answer.rename(columns={"department_phone": "department_phone_numbers"})
answer = answer.sort_values("student_name").reset_index(drop=True)

result = {"students_k_mailing_lists": answer}
