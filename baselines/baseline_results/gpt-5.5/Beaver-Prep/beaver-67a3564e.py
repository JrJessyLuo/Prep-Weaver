import pandas as pd
import numpy as np

def norm_text(s):
    return s.astype("string").str.strip().str.upper()

def mit_id_to_str(s):
    return pd.to_numeric(s, errors="coerce").astype("Int64").astype("string")

def email_local_upper(s):
    return norm_text(s).str.split("@", n=1).str[0]

def eecs_mask_from_name(s):
    x = norm_text(s)
    return x.str.contains("ELECTRICAL", na=False) & x.str.contains("COMPUTER", na=False)

eecs_mit_ids = set()
eecs_kerbs = set()
eecs_full_names = set()

# Department codes corresponding to EECS, if available
dept_codes = set()
if "table_2" in tables:
    dept = tables["table_2"]
    dept_name_cols = [c for c in ["DEPARTMENT_NAME", "DEPARTMENT_FULL_NAME"] if c in dept.columns]
    if dept_name_cols:
        mask = pd.Series(False, index=dept.index)
        for c in dept_name_cols:
            mask |= eecs_mask_from_name(dept[c])
        if "DEPARTMENT_CODE" in dept.columns:
            dept_codes |= set(norm_text(dept.loc[mask, "DEPARTMENT_CODE"]).dropna())

# Student/person table with department and email login
if "table_3" in tables:
    t3 = tables["table_3"]
    mask = pd.Series(False, index=t3.index)
    if "DEPARTMENT" in t3.columns:
        mask |= norm_text(t3["DEPARTMENT"]).isin(dept_codes | {"6"})
    if "DEPARTMENT_NAME" in t3.columns:
        mask |= eecs_mask_from_name(t3["DEPARTMENT_NAME"])
    if "EMAIL_ADDRESS" in t3.columns:
        eecs_kerbs |= set(email_local_upper(t3.loc[mask, "EMAIL_ADDRESS"]).dropna())
    for c in ["FULL_NAME_UPPERCASE", "FULL_NAME"]:
        if c in t3.columns:
            eecs_full_names |= set(norm_text(t3.loc[mask, c]).dropna())

# Faculty table
if "table_5" in tables:
    t5 = tables["table_5"]
    mask = pd.Series(False, index=t5.index)
    for c in ["HR_ORG_UNIT_TITLE", "DIRECTORY_ORG_UNIT_TITLE"]:
        if c in t5.columns:
            mask |= eecs_mask_from_name(t5[c])
    if "MIT_ID" in t5.columns:
        eecs_mit_ids |= set(mit_id_to_str(t5.loc[mask, "MIT_ID"]).dropna())

# Directory/person table
if "table_9" in tables:
    t9 = tables["table_9"]
    mask = pd.Series(False, index=t9.index)
    if "DEPARTMENT_NAME" in t9.columns:
        mask |= eecs_mask_from_name(t9["DEPARTMENT_NAME"])
    if "MIT_ID" in t9.columns:
        eecs_mit_ids |= set(mit_id_to_str(t9.loc[mask, "MIT_ID"]).dropna())
    for c in ["KRB_NAME_UPPERCASE", "krb_name"]:
        if c in t9.columns:
            eecs_kerbs |= set(norm_text(t9.loc[mask, c]).dropna())
    if "EMAIL_ADDRESS" in t9.columns:
        eecs_kerbs |= set(email_local_upper(t9.loc[mask, "EMAIL_ADDRESS"]).dropna())
    for c in ["FULL_NAME_UPPERCASE", "FULL_NAME"]:
        if c in t9.columns:
            eecs_full_names |= set(norm_text(t9.loc[mask, c]).dropna())

ml = tables["table_1"].copy()

ml["list_name"] = ml["MOIRA_LIST_KEY"].astype("string").str.strip()
ml["member_kerb"] = norm_text(ml["moira_list_member"])
ml["member_mit_id"] = mit_id_to_str(ml["MOIRA_LIST_MEMBER_MIT_ID"])
ml["member_full_name_norm"] = norm_text(ml["MOIRA_LIST_MEMBER_FULL_NAME"])

starts_with_b = ml["list_name"].str.upper().str.startswith("B", na=False)
is_eecs_member = (
    ml["member_mit_id"].isin(eecs_mit_ids)
    | ml["member_kerb"].isin(eecs_kerbs)
    | ml["member_full_name_norm"].isin(eecs_full_names)
)

eecs_b_lists = ml.loc[starts_with_b & is_eecs_member].copy()
eecs_b_lists["member_identity"] = eecs_b_lists["member_mit_id"].fillna(eecs_b_lists["member_kerb"])

member_counts = (
    eecs_b_lists
    .dropna(subset=["list_name", "member_identity"])
    .drop_duplicates(["list_name", "member_identity"])
    .groupby("list_name", as_index=False)
    .size()
    .rename(columns={"size": "eecs_member_count"})
)

mailing_lists_count = int(member_counts["list_name"].nunique())

if member_counts.empty:
    final_answer = pd.DataFrame({
        "mailing_lists_count": [0],
        "top_mailing_list_name": [pd.NA],
        "top_eecs_member_count": [0]
    })
else:
    top_row = member_counts.sort_values(
        ["eecs_member_count", "list_name"],
        ascending=[False, True]
    ).iloc[0]
    
    final_answer = pd.DataFrame({
        "mailing_lists_count": [mailing_lists_count],
        "top_mailing_list_name": [top_row["list_name"]],
        "top_eecs_member_count": [int(top_row["eecs_member_count"])]
    })

result = {"mailing_list_eecs_b_summary": final_answer}
