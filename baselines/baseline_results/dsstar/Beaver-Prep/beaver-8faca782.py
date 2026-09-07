import pandas as pd

# ----------------------------
# Source tables from provided `tables` dict
# ----------------------------
df_students = tables['table_2']  # MIT_STUDENT_DIRECTORY.pkl
moira_list_df = tables['table_9']  # MOIRA_LIST.pkl

# Attempt to locate a membership relation table within provided tables
# We don't have explicit membership files in the mapping, so infer if any table contains MOIRA membership-like structure.
# Common column hints for membership: a person identifier + MOIRA_LIST_KEY or MOIRA_LIST_NAME
candidate_keys = list(tables.keys())

membership_df = None
for k in candidate_keys:
    df = tables[k]
    cols_up = {c.upper(): c for c in df.columns}
    has_list = ('MOIRA_LIST_KEY' in cols_up) or ('MOIRA_LIST_NAME' in cols_up)
    has_person = any(c in cols_up for c in ["EMAIL_ADDRESS", "EMAIL", "KRB_NAME", "USER_KRB", "USERNAME", "MIT_ID"])
    # Exclude the moira list lookup table itself
    is_lookup_only = set([c.upper() for c in df.columns]).issuperset({"MOIRA_LIST_KEY", "MOIRA_LIST_NAME"}) and len(df.columns) <= 3
    if has_list and has_person and not is_lookup_only:
        membership_df = df
        break

# Filter students with LAST_NAME starting with "K" (case-insensitive)
mask = df_students["LAST_NAME"].astype(str).str.startswith("K", na=False, case=False)
student_subset = df_students.loc[mask].copy()

# Determine student key for joining
student_key_col = "EMAIL_ADDRESS" if "EMAIL_ADDRESS" in df_students.columns else ("krb_name" if "krb_name" in df_students.columns else None)

# If no membership data or no person key available, construct a zeroed result
if (membership_df is None) or (student_key_col is None):
    # Build a basic result with department phone numbers if available
    out = student_subset.copy()
    # Attempt to bring in department phone from STUDENT_DEPARTMENT if present
    dept_df = tables.get('table_4', pd.DataFrame())
    dept_phone_col = None
    if isinstance(dept_df, pd.DataFrame) and not dept_df.empty:
        # Heuristic for department phone columns
        for cand in ["DEPARTMENT_PHONE", "DEPT_PHONE", "PHONE", "PHONE_NUMBER", "MAIN_PHONE"]:
            if cand in dept_df.columns:
                dept_phone_col = cand
                break
        # Keys to join on: try DEPARTMENT or DEPARTMENT_CODE
        join_key_students = None
        join_key_dept = None
        if "DEPARTMENT" in out.columns and "DEPARTMENT" in dept_df.columns:
            join_key_students, join_key_dept = "DEPARTMENT", "DEPARTMENT"
        elif "DEPARTMENT" in out.columns and "DEPARTMENT_CODE" in dept_df.columns:
            join_key_students, join_key_dept = "DEPARTMENT", "DEPARTMENT_CODE"
        elif "DEPARTMENT_CODE" in out.columns and "DEPARTMENT_CODE" in dept_df.columns:
            join_key_students, join_key_dept = "DEPARTMENT_CODE", "DEPARTMENT_CODE"
        if dept_phone_col and join_key_students and join_key_dept:
            out = out.merge(
                dept_df[[join_key_dept, dept_phone_col]].drop_duplicates(join_key_dept),
                left_on=join_key_students, right_on=join_key_dept, how="left"
            )
            if join_key_dept in out.columns and join_key_dept != join_key_students:
                out = out.drop(columns=[join_key_dept])
            out = out.rename(columns={dept_phone_col: "DEPARTMENT_PHONE"})
        else:
            out["DEPARTMENT_PHONE"] = pd.NA
    else:
        out["DEPARTMENT_PHONE"] = pd.NA

    # Prepare final columns
    cols = ["FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "FULL_NAME", "DEPARTMENT_PHONE"]
    cols = [c for c in cols if c in out.columns] + ["total_mailing_lists", "avg_mailing_list_size"]
    out["total_mailing_lists"] = 0
    out["avg_mailing_list_size"] = 0.0

    result = {"students_K_moira_stats": out[cols]}
else:
    # Identify list identifier column in membership
    mem_cols = {c.upper(): c for c in membership_df.columns}
    if "MOIRA_LIST_KEY" in mem_cols:
        list_key_col = mem_cols["MOIRA_LIST_KEY"]
        list_key_is_name = False
    elif "MOIRA_LIST_NAME" in mem_cols:
        list_key_col = mem_cols["MOIRA_LIST_NAME"]
        list_key_is_name = True
    else:
        # Fall back to zeroed result if not identifiable
        out = student_subset.copy()
        out["DEPARTMENT_PHONE"] = pd.NA
        out["total_mailing_lists"] = 0
        out["avg_mailing_list_size"] = 0.0
        result = {"students_K_moira_stats": out[["FIRST_NAME","MIDDLE_NAME","LAST_NAME","FULL_NAME","DEPARTMENT_PHONE","total_mailing_lists","avg_mailing_list_size"]]}
    
    # Determine person identifier column in membership
    person_key_col = None
    for cand in ["EMAIL_ADDRESS", "EMAIL", "KRB_NAME", "USER_KRB", "USERNAME", "MIT_ID"]:
        if cand in mem_cols:
            person_key_col = mem_cols[cand]
            break

    if person_key_col is None:
        # Fall back to zeroed result if not identifiable
        out = student_subset.copy()
        out["DEPARTMENT_PHONE"] = pd.NA
        out["total_mailing_lists"] = 0
        out["avg_mailing_list_size"] = 0.0
        result = {"students_K_moira_stats": out[["FIRST_NAME","MIDDLE_NAME","LAST_NAME","FULL_NAME","DEPARTMENT_PHONE","total_mailing_lists","avg_mailing_list_size"]]}
    else:
        # Normalize keys
        def norm_person_key(s: pd.Series) -> pd.Series:
            return s.astype(str).str.strip().str.lower()

        student_subset = student_subset.copy()
        student_subset["_PERSON_KEY"] = norm_person_key(student_subset[student_key_col])

        membership_slim = membership_df[[person_key_col, list_key_col]].dropna(subset=[person_key_col, list_key_col]).copy()

        # Map MOIRA_LIST_NAME -> MOIRA_LIST_KEY if needed
        if list_key_is_name:
            moira_list_map = moira_list_df[["MOIRA_LIST_KEY", "MOIRA_LIST_NAME"]].dropna(subset=["MOIRA_LIST_NAME"]).copy()
            membership_slim["_LIST_NAME_UP"] = membership_slim[list_key_col].astype(str).str.upper()
            moira_list_map["_LIST_NAME_UP"] = moira_list_map["MOIRA_LIST_NAME"].astype(str).str.upper()
            membership_slim = membership_slim.merge(
                moira_list_map[["_LIST_NAME_UP", "MOIRA_LIST_KEY"]],
                on="_LIST_NAME_UP", how="left"
            ).drop(columns=["_LIST_NAME_UP"])
            list_key_unified = "MOIRA_LIST_KEY"
        else:
            list_key_unified = list_key_col

        membership_slim["_PERSON_KEY"] = norm_person_key(membership_slim[person_key_col])

        # Filter for our students
        membership_for_students = membership_slim[
            membership_slim["_PERSON_KEY"].isin(student_subset["_PERSON_KEY"])
        ].copy()

        if membership_for_students.empty:
            per_student = pd.DataFrame({"_PERSON_KEY": student_subset["_PERSON_KEY"].unique()})
            per_student["total_mailing_lists"] = 0
            per_student["avg_mailing_list_size"] = 0.0
        else:
            # Deduplicate
            membership_for_students = membership_for_students.drop_duplicates(subset=["_PERSON_KEY", list_key_unified])

            # Compute list sizes from full membership universe
            full_membership = membership_df[[person_key_col, list_key_col]].dropna(subset=[person_key_col, list_key_col]).copy()
            if list_key_is_name:
                moira_list_map = moira_list_df[["MOIRA_LIST_KEY", "MOIRA_LIST_NAME"]].dropna(subset=["MOIRA_LIST_NAME"]).copy()
                full_membership["_LIST_NAME_UP"] = full_membership[list_key_col].astype(str).str.upper()
                moira_list_map["_LIST_NAME_UP"] = moira_list_map["MOIRA_LIST_NAME"].astype(str).str.upper()
                full_membership = full_membership.merge(
                    moira_list_map[["_LIST_NAME_UP", "MOIRA_LIST_KEY"]],
                    on="_LIST_NAME_UP", how="left"
                ).drop(columns=["_LIST_NAME_UP"])
                list_key_unified_full = "MOIRA_LIST_KEY"
            else:
                list_key_unified_full = list_key_col

            full_membership["_PERSON_KEY"] = norm_person_key(full_membership[person_key_col])
            full_membership = full_membership.drop_duplicates(subset=["_PERSON_KEY", list_key_unified_full])

            list_sizes = (
                full_membership.groupby(list_key_unified_full)["_PERSON_KEY"]
                .nunique()
                .rename("list_member_count")
                .reset_index()
            )

            mem_with_sizes = membership_for_students.merge(
                list_sizes, left_on=list_key_unified, right_on=list_key_unified_full, how="left"
            )

            per_student = (
                mem_with_sizes.groupby("_PERSON_KEY")
                .agg(
                    total_mailing_lists=(list_key_unified, "nunique"),
                    avg_mailing_list_size=("list_member_count", "mean"),
                )
                .reset_index()
            )

        # Join back to student info
        result_df = student_subset.merge(per_student, on="_PERSON_KEY", how="left")
        result_df["total_mailing_lists"] = result_df["total_mailing_lists"].fillna(0).astype(int)
        result_df["avg_mailing_list_size"] = result_df["avg_mailing_list_size"].fillna(0.0)

        # Bring in department phone numbers using STUDENT_DEPARTMENT if available
        dept_df = tables.get('table_4', pd.DataFrame())
        dept_phone_col = None
        if isinstance(dept_df, pd.DataFrame) and not dept_df.empty:
            for cand in ["DEPARTMENT_PHONE", "DEPT_PHONE", "PHONE", "PHONE_NUMBER", "MAIN_PHONE"]:
                if cand in dept_df.columns:
                    dept_phone_col = cand
                    break
            join_key_students = None
            join_key_dept = None
            if "DEPARTMENT" in result_df.columns and "DEPARTMENT" in dept_df.columns:
                join_key_students, join_key_dept = "DEPARTMENT", "DEPARTMENT"
            elif "DEPARTMENT" in result_df.columns and "DEPARTMENT_CODE" in dept_df.columns:
                join_key_students, join_key_dept = "DEPARTMENT", "DEPARTMENT_CODE"
            elif "DEPARTMENT_CODE" in result_df.columns and "DEPARTMENT_CODE" in dept_df.columns:
                join_key_students, join_key_dept = "DEPARTMENT_CODE", "DEPARTMENT_CODE"
            if dept_phone_col and join_key_students and join_key_dept:
                result_df = result_df.merge(
                    dept_df[[join_key_dept, dept_phone_col]].drop_duplicates(join_key_dept),
                    left_on=join_key_students, right_on=join_key_dept, how="left"
                )
                if join_key_dept in result_df.columns and join_key_dept != join_key_students:
                    result_df = result_df.drop(columns=[join_key_dept])
                result_df = result_df.rename(columns={dept_phone_col: "DEPARTMENT_PHONE"})
            else:
                result_df["DEPARTMENT_PHONE"] = pd.NA
        else:
            result_df["DEPARTMENT_PHONE"] = pd.NA

        # Final selection
        out_cols = [
            "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "FULL_NAME",
            "DEPARTMENT_PHONE", "total_mailing_lists", "avg_mailing_list_size"
        ]
        out_cols = [c for c in out_cols if c in result_df.columns]
        final_out = result_df[out_cols].copy()

        result = {"students_K_moira_stats": final_out}