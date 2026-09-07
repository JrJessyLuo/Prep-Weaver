import pandas as pd
import re

def _find_col(df, candidates):
    lower_to_col = {str(c).lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lower_to_col:
            return lower_to_col[cand.lower()]
    return None

def _norm_id_series(s):
    out = s.astype("string").str.strip()
    out = out.str.replace(r"\.0$", "", regex=True)
    out = out.mask(out.str.lower().isin(["", "nan", "none", "null", "<na>"]))
    return out

def _norm_text_series(s):
    out = s.astype("string").str.strip()
    out = out.mask(out.str.lower().isin(["", "nan", "none", "null", "<na>"]))
    return out

def _norm_name_series(s):
    return _norm_text_series(s).str.lower().str.replace(r"\s+", " ", regex=True)

# --- Courses/faculty responsible in Fall 2023 ---
course_source_order = ["table_4", "table_3", "table_5", "table_6", "table_1", "table_2"]
courses_2023fa = pd.DataFrame(columns=["faculty_id", "faculty_name_norm", "subject_id"])

for tname in course_source_order:
    if tname not in tables:
        continue
    df = tables[tname].copy()
    term_col = _find_col(df, ["TERM_CODE", "term_code", "SO_TERM_CODE"])
    fac_id_col = _find_col(df, ["RESPONSIBLE_FACULTY_MIT_ID", "responsible_faculty_mit_id"])
    fac_name_col = _find_col(df, ["RESPONSIBLE_FACULTY_NAME"])
    subj_col = _find_col(df, ["SUBJECT_ID", "subject_id", "SO_SUBJECT_ID", "SUBJECT_OFFERED_SUMMARY_KEY"])
    if term_col is None or fac_id_col is None or subj_col is None:
        continue

    tmp = df[df[term_col].astype("string").str.upper().eq("2023FA")].copy()
    if tmp.empty:
        continue

    tmp = tmp[[fac_id_col, subj_col] + ([fac_name_col] if fac_name_col is not None else [])].copy()
    tmp[fac_id_col] = tmp[fac_id_col].astype("string").str.split(r"\s*,\s*")
    tmp = tmp.explode(fac_id_col)

    tmp["faculty_id"] = _norm_id_series(tmp[fac_id_col])
    tmp["subject_id"] = _norm_text_series(tmp[subj_col])
    tmp["faculty_name_norm"] = (
        _norm_name_series(tmp[fac_name_col]) if fac_name_col is not None else pd.NA
    )

    tmp = tmp.dropna(subset=["faculty_id", "subject_id"])
    if not tmp.empty:
        courses_2023fa = tmp[["faculty_id", "faculty_name_norm", "subject_id"]].drop_duplicates()
        break

faculty_ids = set(courses_2023fa["faculty_id"].dropna())
faculty_names = set(courses_2023fa["faculty_name_norm"].dropna())

# --- Discover mailing-list membership tables and aggregate ---
def _candidate_list_cols(df):
    cols = []
    for c in df.columns:
        lc = str(c).lower()
        if any(x in lc for x in ["cluster_list", "joint_subject", "school_wide", "equivalent_subject", "meets_with"]):
            continue
        if lc in {
            "mailing_list_name", "mail_list_name", "email_list_name", "moira_list_name",
            "list_name", "listname", "mailing_list", "mailinglist", "mail_list",
            "group_name", "groupname"
        }:
            cols.append(c)
        elif ("mail" in lc or "moira" in lc or "list" in lc) and ("name" in lc or lc.endswith("list")):
            cols.append(c)
    return cols

def _candidate_member_id_cols(df):
    cols = []
    for c in df.columns:
        lc = str(c).lower()
        if lc in {
            "mit_id", "member_mit_id", "subscriber_mit_id", "person_mit_id",
            "member_id", "subscriber_id", "person_id", "user_id"
        }:
            cols.append(c)
        elif ("mit_id" in lc) or (("member" in lc or "subscriber" in lc or "person" in lc) and lc.endswith("id")):
            cols.append(c)
    return cols

def _candidate_member_name_cols(df):
    cols = []
    for c in df.columns:
        lc = str(c).lower()
        if lc in {"member_name", "subscriber_name", "person_name", "full_name"}:
            cols.append(c)
        elif ("member" in lc or "subscriber" in lc or "person" in lc) and "name" in lc:
            cols.append(c)
    return cols

def _candidate_count_cols(df):
    cols = []
    for c in df.columns:
        lc = str(c).lower()
        if ("member" in lc or "subscriber" in lc) and any(x in lc for x in ["count", "number", "num", "cnt"]):
            cols.append(c)
    return cols

outputs = []

for _, df in tables.items():
    list_cols = _candidate_list_cols(df)
    if not list_cols:
        continue

    member_id_cols = _candidate_member_id_cols(df)
    member_name_cols = _candidate_member_name_cols(df)
    count_cols = _candidate_count_cols(df)

    for list_col in list_cols:
        # ID-based membership
        for member_col in member_id_cols:
            pairs = df[[list_col, member_col] + count_cols].copy()
            pairs[list_col] = _norm_text_series(pairs[list_col])
            pairs[member_col] = pairs[member_col].astype("string").str.split(r"\s*,\s*")
            pairs = pairs.explode(member_col)
            pairs["member_key"] = _norm_id_series(pairs[member_col])
            pairs = pairs.dropna(subset=[list_col, "member_key"]).drop_duplicates([list_col, "member_key"])

            if pairs.empty:
                continue

            row_counts = pairs.groupby(list_col)["member_key"].nunique()
            ten_lists = set(row_counts[row_counts.eq(10)].index)

            for cnt_col in count_cols:
                cnt_vals = pd.to_numeric(df[cnt_col], errors="coerce")
                ten_lists.update(df.loc[cnt_vals.eq(10), list_col].dropna().astype("string").str.strip())

            qualifying = pairs[pairs[list_col].isin(ten_lists) & pairs["member_key"].isin(faculty_ids)]
            if qualifying.empty:
                continue

            list_faculty = qualifying[[list_col, "member_key"]].drop_duplicates()
            merged = list_faculty.merge(
                courses_2023fa[["faculty_id", "subject_id"]],
                left_on="member_key",
                right_on="faculty_id",
                how="left"
            )

            agg = merged.groupby(list_col, as_index=False).agg(
                number_of_faculty=("member_key", "nunique"),
                number_of_courses=("subject_id", "nunique")
            ).rename(columns={list_col: "mailing_list_name"})

            outputs.append(agg)

        # Name-based membership fallback
        for member_col in member_name_cols:
            pairs = df[[list_col, member_col] + count_cols].copy()
            pairs[list_col] = _norm_text_series(pairs[list_col])
            pairs["member_key"] = _norm_name_series(pairs[member_col])
            pairs = pairs.dropna(subset=[list_col, "member_key"]).drop_duplicates([list_col, "member_key"])

            if pairs.empty:
                continue

            row_counts = pairs.groupby(list_col)["member_key"].nunique()
            ten_lists = set(row_counts[row_counts.eq(10)].index)

            for cnt_col in count_cols:
                cnt_vals = pd.to_numeric(df[cnt_col], errors="coerce")
                ten_lists.update(df.loc[cnt_vals.eq(10), list_col].dropna().astype("string").str.strip())

            qualifying = pairs[pairs[list_col].isin(ten_lists) & pairs["member_key"].isin(faculty_names)]
            if qualifying.empty:
                continue

            list_faculty = qualifying[[list_col, "member_key"]].drop_duplicates()
            merged = list_faculty.merge(
                courses_2023fa[["faculty_name_norm", "subject_id"]].dropna(subset=["faculty_name_norm"]),
                left_on="member_key",
                right_on="faculty_name_norm",
                how="left"
            )

            agg = merged.groupby(list_col, as_index=False).agg(
                number_of_faculty=("member_key", "nunique"),
                number_of_courses=("subject_id", "nunique")
            ).rename(columns={list_col: "mailing_list_name"})

            outputs.append(agg)

if outputs:
    final = pd.concat(outputs, ignore_index=True)
    final = (
        final.groupby("mailing_list_name", as_index=False)
        .agg(number_of_faculty=("number_of_faculty", "max"),
             number_of_courses=("number_of_courses", "max"))
        .sort_values("mailing_list_name")
        .reset_index(drop=True)
    )
else:
    final = pd.DataFrame(columns=["mailing_list_name", "number_of_faculty", "number_of_courses"])

result = {"mailing_lists_for_2023_fall_responsible_faculty": final}
