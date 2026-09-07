import pandas as pd

# Access pre-loaded tables
moira_df = tables['table_7'].copy()
student_df = tables['table_2'].copy()

# Target MOIRA list name
target_list_name = "kangaroo-inspire-yearn"

# Find the MOIRA list row(s) matching the target list name (case-insensitive)
moira_match = moira_df.loc[moira_df["MOIRA_LIST_NAME"].astype(str).str.lower() == target_list_name.lower()].copy()

# Prepare output placeholder
final_df = pd.DataFrame(columns=["DEPARTMENT", "DEPARTMENT_NAME", "STUDENTS_IN_DEPT", "PCT_OF_LIST"])

# Attempt to locate a membership table among columns present in tables
# Reproduce the same intent as reference: seek a membership frame and map to student directory via email
possible_membership_keys = [
    # Try common membership table names that might be embedded in MOIRA_LIST (unlikely, but check)
    "MOIRA_LIST_MEMBERS", "MOIRA_LIST_MEMBER", "MOIRA_MEMBER", "MOIRA_LIST_PEOPLE", "MOIRA_LIST_ENTRIES"
]

# Since we only have the predefined 9 tables, inspect each for plausible membership columns
membership_df = None
for key in tables.keys():
    df = tables[key]
    cols_lower = {c.lower(): c for c in df.columns}
    has_list_ref = any(k in cols_lower for k in ["moira_list_key", "list_key", "moira_listname", "moira_list_name"])
    has_member_ref = any(k in cols_lower for k in ["email_address", "email", "member_email", "krb_name", "username", "kerberos", "moira_member"])
    if has_list_ref and has_member_ref:
        membership_df = df.copy()
        break

if (membership_df is not None) and (not moira_match.empty):
    # Heuristically determine key columns
    cols_lower = {c.lower(): c for c in membership_df.columns}
    moira_key_col = cols_lower.get("moira_list_key") or cols_lower.get("list_key") or cols_lower.get("moira_listname") or cols_lower.get("moira_list_name")
    email_col = cols_lower.get("email_address") or cols_lower.get("email") or cols_lower.get("member_email")
    krb_col = cols_lower.get("krb_name") or cols_lower.get("username") or cols_lower.get("kerberos") or cols_lower.get("moira_member")

    # Extract list keys or names from moira_match
    if "MOIRA_LIST_KEY" in moira_match.columns and not moira_match["MOIRA_LIST_KEY"].isna().all():
        list_keys = moira_match["MOIRA_LIST_KEY"].dropna().astype(str).unique().tolist()
    else:
        list_keys = []

    if moira_key_col is None and ("MOIRA_LIST_NAME" in moira_df.columns):
        target_list_names = moira_match["MOIRA_LIST_NAME"].astype(str).unique().tolist()
    else:
        target_list_names = []

    # Filter membership to the target list
    if (moira_key_col is not None) and (len(list_keys) > 0):
        mem_filtered = membership_df.loc[membership_df[moira_key_col].astype(str).isin(list_keys)].copy()
    elif (moira_key_col in ({k.lower(): k for k in membership_df.columns}.get("moira_list_name"), {k.lower(): k for k in membership_df.columns}.get("moira_listname"))) and len(target_list_names) > 0:
        mem_filtered = membership_df.loc[membership_df[moira_key_col].astype(str).str.lower().isin([n.lower() for n in target_list_names])].copy()
    else:
        mem_filtered = pd.DataFrame()

    if not mem_filtered.empty:
        # Create EMAIL_ADDRESS for mapping to student directory
        if email_col and email_col in mem_filtered.columns:
            mem_filtered["EMAIL_ADDRESS"] = mem_filtered[email_col].astype(str).str.strip()
        elif krb_col and krb_col in mem_filtered.columns:
            mem_filtered["EMAIL_ADDRESS"] = mem_filtered[krb_col].astype(str).str.strip().str.split("@").str[0] + "@mit.edu"
        else:
            mem_filtered["EMAIL_ADDRESS"] = pd.NA

        # Clean and deduplicate emails
        emails = (
            mem_filtered["EMAIL_ADDRESS"]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace({"nan": pd.NA})
            .dropna()
            .unique()
            .tolist()
        )

        if len(emails) > 0:
            # Prepare student directory for join (case-insensitive on email)
            student_df = student_df.copy()
            student_df["_EMAIL_LOWER"] = student_df["EMAIL_ADDRESS"].astype(str).str.strip().str.lower()
            emails_df = pd.DataFrame({"_EMAIL_LOWER": emails})

            joined = emails_df.merge(student_df, on="_EMAIL_LOWER", how="left")

            # Keep only matched students (rows with non-null EMAIL_ADDRESS from student directory)
            matched = joined.dropna(subset=["EMAIL_ADDRESS"]).copy()

            if not matched.empty:
                # Compute counts and percentages by department
                dept_cols = [c for c in ["DEPARTMENT", "DEPARTMENT_NAME"] if c in matched.columns]
                if len(dept_cols) == 0:
                    # If department columns missing, keep empty final_df
                    pass
                else:
                    group_cols = []
                    if "DEPARTMENT" in dept_cols:
                        group_cols.append("DEPARTMENT")
                    if "DEPARTMENT_NAME" in dept_cols:
                        group_cols.append("DEPARTMENT_NAME")

                    counts = (
                        matched.groupby(group_cols, dropna=False)
                        .size()
                        .reset_index(name="STUDENTS_IN_DEPT")
                    )

                    total_students = counts["STUDENTS_IN_DEPT"].sum()
                    counts["PCT_OF_LIST"] = (counts["STUDENTS_IN_DEPT"] / total_students * 100).round(2)

                    # Ensure both DEPARTMENT and DEPARTMENT_NAME present in final output
                    if "DEPARTMENT" not in counts.columns:
                        counts["DEPARTMENT"] = pd.NA
                    if "DEPARTMENT_NAME" not in counts.columns:
                        counts["DEPARTMENT_NAME"] = pd.NA

                    # Order columns
                    final_df = counts[["DEPARTMENT", "DEPARTMENT_NAME", "STUDENTS_IN_DEPT", "PCT_OF_LIST"]].sort_values(
                        by=["STUDENTS_IN_DEPT", "DEPARTMENT_NAME"], ascending=[False, True]
                    )

# Package final result
result = {"dept_breakdown": final_df}