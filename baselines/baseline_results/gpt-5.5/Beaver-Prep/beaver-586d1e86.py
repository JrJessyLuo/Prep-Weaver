import pandas as pd
import numpy as np

# Source tables
members = tables["table_1"].copy()
students = tables["table_2"].copy()
owners = tables["table_3"].copy()
lists = tables["table_10"].copy()

# Normalize list keys/names and keep eligible email lists whose names start with "e"
lists["list_key_norm"] = lists["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()
lists["list_name_norm"] = lists["MOIRA_LIST_NAME"].astype(str).str.strip()

eligible_lists = lists[
    (lists["IS_MOIRA_MAILING_LIST"].astype(str).str.strip().str.upper() == "Y") &
    (lists["list_name_norm"].str.lower().str.startswith("e", na=False))
][["list_key_norm", "list_name_norm"]].drop_duplicates()

# Normalize members and join to eligible lists
members["list_key_norm"] = members["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()
members["member_kerb_norm"] = members["moira_list_member"].astype(str).str.strip().str.upper()
members["owner_key_norm"] = members["MOIRA_LIST_OWNER_KEY"].astype(str).str.strip()

m = members.merge(eligible_lists, on="list_key_norm", how="inner")

# Identify computer science students from student table
students["member_kerb_norm"] = (
    students["EMAIL_ADDRESS"]
    .astype(str)
    .str.strip()
    .str.split("@", n=1)
    .str[0]
    .str.upper()
)

dept_code = students["DEPARTMENT"].astype(str).str.strip().str.upper()
dept_name = students["DEPARTMENT_NAME"].astype(str).str.strip().str.lower()

students["is_cs_student"] = (
    dept_code.eq("6") |
    dept_name.str.contains("computer sci|computer science", na=False)
)

student_cs = (
    students.dropna(subset=["member_kerb_norm"])
    .groupby("member_kerb_norm", as_index=False)["is_cs_student"]
    .max()
)

# Mark each list member as CS student or not
m = m.merge(student_cs, on="member_kerb_norm", how="left")
m["is_cs_student"] = m["is_cs_student"].fillna(False)

# Aggregate by list
agg = (
    m.groupby(["list_key_norm", "list_name_norm"], as_index=False)
    .agg(
        owner_key_norm=("owner_key_norm", "first"),
        member_count=("member_kerb_norm", "nunique"),
        cs_student_count=("is_cs_student", "sum")
    )
)

agg["cs_student_pct"] = agg["cs_student_count"] / agg["member_count"]

# Owner lookup
owners["owner_key_norm"] = owners["MOIRA_LIST_OWNER_KEY"].astype(str).str.strip()
owner_lookup = owners[["owner_key_norm", "OWNER"]].drop_duplicates()

out = agg.merge(owner_lookup, on="owner_key_norm", how="left")
out["owner"] = out["OWNER"].fillna(
    out["owner_key_norm"].str.replace(r"^(USER|LIST)", "", regex=True)
)

# Final filter and output
final = out[
    out["member_count"].between(10, 20, inclusive="both") &
    (out["cs_student_pct"] > 0.75)
].copy()

final = (
    final[["list_name_norm", "owner", "member_count"]]
    .rename(columns={"list_name_norm": "list_name"})
    .sort_values(["list_name", "owner"])
    .reset_index(drop=True)
)

result = {"email_lists": final}
