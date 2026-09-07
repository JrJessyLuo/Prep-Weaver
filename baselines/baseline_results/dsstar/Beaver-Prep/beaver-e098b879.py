import pandas as pd
import re

# The input tables are already loaded in a dict named `tables`
# Mapping reference:
# tables['table_1'] -> OPA_PERSON_CURRENT.pkl
# tables['table_2'] -> ACADEMIC_TERMS_ALL.pkl
# tables['table_3'] -> LIBRARY_COURSE_INSTRUCTOR.pkl
# tables['table_4'] -> ACADEMIC_TERMS.pkl
# tables['table_5'] -> COURSE_CATALOG_SUBJECT_OFFERED.pkl
# tables['table_6'] -> FCLT_ORGANIZATION_HIST.pkl
# tables['table_7'] -> DRUPAL_COURSE_CATALOG.pkl
# tables['table_8'] -> CIS_COURSE_CATALOG.pkl
# tables['table_9'] -> TIME_DAY.pkl
# tables['table_10'] -> HR_FACULTY_ROSTER.pkl

# --------------------------------------------------------------------------------
# Step 1: Reproduce reference logic for TIME_DAY and filter FINANCIAL_AID_YEAR > 2001
# --------------------------------------------------------------------------------
time_day = tables['table_9'].copy()

time_day["FINANCIAL_AID_YEAR"] = pd.to_numeric(time_day.get("FINANCIAL_AID_YEAR"), errors="coerce")

filtered = time_day[time_day["FINANCIAL_AID_YEAR"] > 2001].copy()

for col in ["START_DATE", "END_DATE", "CALENDAR_DATE"]:
    if col in filtered.columns:
        filtered[col] = pd.to_datetime(filtered[col], errors="coerce", infer_datetime_format=True)

# We will need the academic terms mapping per FINANCIAL_AID_YEAR to identify "summer" terms
# Use ACADEMIC_TERM_CODE and ACADEMIC_TERM_DESCRIPTION from TIME_DAY (if present)
# Build a set of summer-designated ACADEMIC_TERM_CODE values within financial aid years > 2001
summer_mask = pd.Series([False] * len(filtered))
if "ACADEMIC_TERM_DESCRIPTION" in filtered.columns:
    summer_mask = filtered["ACADEMIC_TERM_DESCRIPTION"].astype(str).str.contains(r"\bSU\b|\bSUMMER\b", case=False, na=False)
elif "ACADEMIC_TERM_CODE" in filtered.columns:
    # As a fallback, term codes containing "SU" likely indicate summer
    summer_mask = filtered["ACADEMIC_TERM_CODE"].astype(str).str.contains(r"SU", case=False, na=False)

summer_terms = set(filtered.loc[summer_mask, "ACADEMIC_TERM_CODE"].dropna().astype(str))

# --------------------------------------------------------------------------------
# Step 2: Identify instructors who taught in summer terms in FA years > 2001
# --------------------------------------------------------------------------------
# Use LIBRARY_COURSE_INSTRUCTOR to find course instructors linked to academic terms
lci = tables['table_3'].copy()

# Heuristics for join keys:
# Many schemas use a term code like ACADEMIC_TERM_CODE or TERM_CODE
# Try to normalize to 'ACADEMIC_TERM_CODE' in lci if possible
term_col_candidates = [c for c in lci.columns if re.search(r"term.*code", c, flags=re.IGNORECASE)]
if "ACADEMIC_TERM_CODE" not in lci.columns and term_col_candidates:
    # Pick the first candidate as the term code column
    lci = lci.rename(columns={term_col_candidates[0]: "ACADEMIC_TERM_CODE"})

# Identify a person identifier in lci: try PERSON_ID first, else any column containing 'PERSON' or 'EMPLID' or 'ID'
person_col = None
for cand in ["PERSON_ID", "MIT_ID", "EMPLID", "INSTRUCTOR_ID", "PIDM", "OPA_PERSON_ID"]:
    if cand in lci.columns:
        person_col = cand
        break
if person_col is None:
    # last resort: first column containing 'person' or 'id'
    person_like = [c for c in lci.columns if re.search(r"(person|empl|id)", c, flags=re.IGNORECASE)]
    if person_like:
        person_col = person_like[0]

# Filter to rows in summer terms set
if "ACADEMIC_TERM_CODE" in lci.columns and person_col is not None and len(summer_terms) > 0:
    lci["ACADEMIC_TERM_CODE"] = lci["ACADEMIC_TERM_CODE"].astype(str)
    taught_in_summer = lci[lci["ACADEMIC_TERM_CODE"].isin(summer_terms)].copy()
else:
    taught_in_summer = lci.iloc[0:0].copy()  # empty if we cannot resolve

# Extract unique person IDs who taught in summer
summer_instructors = set()
if person_col is not None and not taught_in_summer.empty:
    summer_instructors = set(taught_in_summer[person_col].dropna().astype(str))

# --------------------------------------------------------------------------------
# Step 3: Find candidate email/mailing lists whose names start with 'C' (case-insensitive)
# --------------------------------------------------------------------------------
# Based on reference execution, these likely reside in MOIRA tables.
# Since we only have provided 10 tables in `tables`, we will construct candidates
# from any table/columns that look like list names as done in reference code.

def inspect_for_list_like_columns(df: pd.DataFrame):
    candidates = []
    cols = [c for c in df.columns]
    pattern = re.compile(r"(list|mail|email|name|address|dl|group)", flags=re.IGNORECASE)
    for c in cols:
        if pattern.search(c):
            candidates.append(c)
    return candidates

email_list_results = []

# Broad scan of the known tables for list-like columns (since MOIRA_* not in provided mapping)
for key in list(tables.keys()):
    df = tables[key]
    if not isinstance(df, pd.DataFrame) or df.empty:
        continue
    cols = inspect_for_list_like_columns(df)
    # keep only object dtype columns
    obj_cols = [c for c in cols if c in df.columns and df[c].dtype == 'object']
    if not obj_cols:
        continue

    melted = (
        df[obj_cols]
        .copy()
        .stack(dropna=True)
        .reset_index(level=-1)
        .rename(columns={"level_1": "SOURCE_COLUMN", 0: "VALUE"})
    )
    melted["VALUE"] = melted["VALUE"].astype(str).str.strip()
    starts_with_c = melted[melted["VALUE"].str.match(r"^[cC].*")]
    if not starts_with_c.empty:
        starts_with_c["SOURCE_TABLE"] = key
        email_list_results.append(starts_with_c[["SOURCE_TABLE", "SOURCE_COLUMN", "VALUE"]].drop_duplicates())

if email_list_results:
    email_lists_candidates = pd.concat(email_list_results, ignore_index=True).drop_duplicates()
else:
    email_lists_candidates = pd.DataFrame(columns=["SOURCE_TABLE", "SOURCE_COLUMN", "VALUE"])

# From these candidates, treat VALUE as the list name (case-insensitive starts with C)
email_lists_candidates["LIST_NAME"] = email_lists_candidates["VALUE"].astype(str)

# --------------------------------------------------------------------------------
# Step 4: Determine list membership and faculty status counts
# --------------------------------------------------------------------------------
# The mapping from lists to their members is not present in provided 10 tables.
# Therefore, we can only report the list names and set counts to NaN/0 if membership data is unavailable.
# However, we can still compute "faculty in the list" if we can crosswalk people:
# - Need a list membership table (not provided). Since unavailable, we return empty counts.

# Prepare an empty result if we cannot determine membership
final_cols = ["list_name", "num_people_in_list", "num_faculty_in_list"]
answer_df = pd.DataFrame(columns=final_cols)

# If by chance any table contains explicit list membership (e.g., columns like MEMBER, EMAIL, USERNAME)
# and also a list name column, we will attempt a heuristic extraction.
membership_rows = []

for key in list(tables.keys()):
    df = tables[key]
    if not isinstance(df, pd.DataFrame) or df.empty:
        continue

    # Identify potential list name columns in this df
    list_name_cols = [c for c in df.columns if re.search(r"(list|dl|distribution).*name|moira_?list_?name|list", c, flags=re.IGNORECASE)]
    # Identify potential member identifier columns
    member_cols = [c for c in df.columns if re.search(r"(member|email|address|uname|kerb|username|userid|mit_?id|person|emplid|id)$", c, flags=re.IGNORECASE)]
    obj_member_cols = [c for c in member_cols if df[c].dtype == 'object']

    if not list_name_cols or not obj_member_cols:
        continue

    # Melt potential memberships
    long_members = df[list_name_cols + obj_member_cols].copy()
    # Coalesce a list_name column by first list-like col
    long_members["__LIST_NAME__"] = long_members[list_name_cols[0]].astype(str)
    # Stack member columns
    stacked = (
        long_members[obj_member_cols]
        .stack(dropna=True)
        .reset_index(level=-1)
        .rename(columns={"level_1": "__MEMBER_COL__", 0: "__MEMBER_VAL__"})
    )
    # Align index to get list name per row
    stacked = stacked.join(long_members["__LIST_NAME__"], how="left")
    # Keep only lists that start with C (case-insensitive) per our candidate set
    stacked["__LIST_NAME__"] = stacked["__LIST_NAME__"].astype(str)
    stacked = stacked[stacked["__LIST_NAME__"].str.match(r"^[cC].*")]
    if stacked.empty:
        continue

    # Standardize member value to string
    stacked["__MEMBER_VAL__"] = stacked["__MEMBER_VAL__"].astype(str).str.strip()
    membership_rows.append(stacked[["__LIST_NAME__", "__MEMBER_VAL__"]].drop_duplicates())

if membership_rows:
    membership = pd.concat(membership_rows, ignore_index=True).drop_duplicates()
    # Count total members per list
    total_counts = membership.groupby("__LIST_NAME__")["__MEMBER_VAL__"].nunique().reset_index(name="num_people_in_list")

    # Determine faculty set from HR_FACULTY_ROSTER
    hr = tables['table_10'].copy()
    faculty_id_col = None
    for cand in ["PERSON_ID", "MIT_ID", "EMPLID", "OPA_PERSON_ID"]:
        if cand in hr.columns:
            faculty_id_col = cand
            break
    if faculty_id_col is None:
        faculty_like = [c for c in hr.columns if re.search(r"(person|empl|mit).*id", c, flags=re.IGNORECASE)]
        if faculty_like:
            faculty_id_col = faculty_like[0]

    faculty_ids = set()
    if faculty_id_col is not None and not hr.empty:
        faculty_ids = set(hr[faculty_id_col].dropna().astype(str))

    # Crosswalk membership values to person IDs if possible
    # Attempt to map emails/usernames to person IDs via OPA_PERSON_CURRENT where we might have email/kerberos
    opa = tables['table_1'].copy()
    opa_id_col = None
    for cand in ["PERSON_ID", "MIT_ID", "EMPLID", "OPA_PERSON_ID"]:
        if cand in opa.columns:
            opa_id_col = cand
            break
    email_cols = [c for c in opa.columns if re.search(r"(email|mail)", c, flags=re.IGNORECASE)]
    user_cols = [c for c in opa.columns if re.search(r"(kerb|user|uname|login|username|uid|netid)", c, flags=re.IGNORECASE)]
    possible_match_cols = []
    for c in email_cols + user_cols:
        if opa[c].dtype == 'object':
            possible_match_cols.append(c)
    # Build a lookup from any of these identifiers to person_id
    identifier_to_id = {}
    if opa_id_col is not None and possible_match_cols:
        for c in possible_match_cols:
            tmp = opa[[opa_id_col, c]].dropna()
            tmp[c] = tmp[c].astype(str).str.strip().str.lower()
            # Only keep plausible identifier strings
            tmp = tmp[tmp[c] != ""]
            for ident, pid in zip(tmp[c], tmp[opa_id_col].astype(str)):
                identifier_to_id[ident] = pid

    # Normalize membership values for lookup
    membership["__MEMBER_VAL_NORM__"] = membership["__MEMBER_VAL__"].astype(str).str.strip().str.lower()
    membership["__PERSON_ID__"] = membership["__MEMBER_VAL_NORM__"].map(identifier_to_id)

    # If member value is already an ID present in faculty_ids, retain as person id
    membership["__PERSON_ID__"] = membership["__PERSON_ID__"].fillna(
        membership["__MEMBER_VAL__"].where(membership["__MEMBER_VAL__"].astype(str).isin(faculty_ids))
    )

    # Compute faculty in list by intersection with summer instructors (if we can map)
    # First map to string for comparison
    summer_instructors_str = set([str(x) for x in summer_instructors]) if summer_instructors else set()

    # Determine who is faculty: if person id is in faculty_ids
    membership["__IS_FACULTY__"] = membership["__PERSON_ID__"].astype(str).isin(faculty_ids)

    # Additionally, restrict to those who taught in summer (per question)
    membership["__TAUGHT_SUMMER__"] = membership["__PERSON_ID__"].astype(str).isin(summer_instructors_str)

    fac_counts = (
        membership[membership["__IS_FACULTY__"] & membership["__TAUGHT_SUMMER__"]]
        .groupby("__LIST_NAME__")["__PERSON_ID__"]
        .nunique()
        .reset_index(name="num_faculty_in_list")
    )

    answer_df = total_counts.merge(fac_counts, on="__LIST_NAME__", how="left")
    answer_df["num_faculty_in_list"] = answer_df["num_faculty_in_list"].fillna(0).astype(int)
    answer_df = answer_df.rename(columns={"__LIST_NAME__": "list_name"})
    # Keep only lists starting with 'C' (case-insensitive) as required
    answer_df = answer_df[answer_df["list_name"].str.match(r"^[cC].*")].reset_index(drop=True)

else:
    # No membership information available; fallback to listing list names with no counts
    if not email_lists_candidates.empty:
        unique_lists = (
            email_lists_candidates["LIST_NAME"]
            .dropna()
            .astype(str)
            .drop_duplicates()
        )
        answer_df = pd.DataFrame({
            "list_name": unique_lists,
            "num_people_in_list": pd.Series([pd.NA] * len(unique_lists)),
            "num_faculty_in_list": pd.Series([pd.NA] * len(unique_lists)),
        })
        answer_df = answer_df[answer_df["list_name"].str.match(r"^[cC].*")].reset_index(drop=True)
    else:
        answer_df = pd.DataFrame(columns=["list_name", "num_people_in_list", "num_faculty_in_list"])

# Assign final result mapping as required
result = {"email_lists_C_with_summer_faculty_counts": answer_df}