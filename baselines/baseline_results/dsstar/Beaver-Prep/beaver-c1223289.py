import pandas as pd
from difflib import SequenceMatcher

# Assumptions:
# - Input DataFrames are provided in a dict named `tables`
#   tables['table_1'] -> LIBRARY_COURSE_INSTRUCTOR
#   tables['table_5'] -> SUBJECT_OFFERED_SUMMARY
#   tables['table_6'] -> MOIRA_LIST_DETAIL
#   tables['table_7'] -> LIBRARY_RESERVE_MATRL_DETAIL

# 1) Load dataframes from provided `tables` dict
lib_ci = tables['table_1'].copy()
sos = tables['table_5'].copy()
moira = tables['table_6'].copy()
lib_res = tables['table_7'].copy()

# 2) Basic normalize column names to consistent casing/strip
def normalize_cols(df):
    df.columns = [c.strip() for c in df.columns]
    return df

lib_ci = normalize_cols(lib_ci)
moira = normalize_cols(moira)
lib_res = normalize_cols(lib_res)
sos = normalize_cols(sos)

# 3) Filter MOIRA list to the requested list key
target_list_key = "keeper-zephyr"
moira_filtered = moira.loc[moira["MOIRA_LIST_KEY"] == target_list_key].copy()

# Helpers for name normalization and parsing
def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    return " ".join(name.replace(",", " ").split()).lower()

def split_last_first(full_name: str):
    if not isinstance(full_name, str) or not full_name.strip():
        return ("", "")
    s = full_name.strip()
    if "," in s:
        last, first = s.split(",", 1)
        return (last.strip().lower(), " ".join(first.split()).lower())
    parts = s.split()
    if len(parts) >= 2:
        return (parts[-1].lower(), " ".join(parts[:-1]).lower())
    return (s.lower(), "")

def simple_ratio(a: str, b: str) -> int:
    return int(round(100 * SequenceMatcher(None, a, b).ratio()))

# 4) Create standardized name columns and parsed names
moira_filtered["name_norm"] = moira_filtered["MOIRA_LIST_MEMBER_FULL_NAME"].astype(str).map(normalize_name)
lib_ci["name_norm"] = lib_ci["INSTRUCTOR_NAME"].astype(str).map(normalize_name)

moira_filtered[["last_name", "first_name"]] = moira_filtered["MOIRA_LIST_MEMBER_FULL_NAME"].astype(str).apply(
    lambda x: pd.Series(split_last_first(x))
)
lib_ci[["instr_last_name", "instr_first_name"]] = lib_ci["INSTRUCTOR_NAME"].astype(str).apply(
    lambda x: pd.Series(split_last_first(x))
)

# 5) Exact name match first (normalized)
exact_matches = moira_filtered.merge(
    lib_ci[[
        "LIBRARY_COURSE_INSTRUCTOR_KEY", "COURSE_NAME", "INSTRUCTOR_NAME",
        "DEPARTMENT", "DATE_FROM", "DATE_TO", "UNIT_CODE", "UNIT",
        "WAREHOUSE_LOAD_DATE", "name_norm", "instr_last_name", "instr_first_name"
    ]],
    how="left",
    on="name_norm",
    suffixes=("_MOIRA", "_LIB")
)

# 6) Fuzzy/alternate identifier matching for unmatched
unmatched_mask = exact_matches["LIBRARY_COURSE_INSTRUCTOR_KEY"].isna()
moira_unmatched = moira_filtered.loc[moira_filtered["name_norm"].isin(
    exact_matches.loc[unmatched_mask, "name_norm"]
)].copy()

lib_ci_by_last = lib_ci.copy()
moira_unmatched = moira_unmatched.rename(columns={"last_name": "moira_last_name", "first_name": "moira_first_name"})
lib_ci_by_last = lib_ci_by_last.rename(columns={"instr_last_name": "lib_last_name", "instr_first_name": "lib_first_name"})

cand = moira_unmatched.merge(
    lib_ci_by_last[[
        "LIBRARY_COURSE_INSTRUCTOR_KEY", "COURSE_NAME", "INSTRUCTOR_NAME",
        "DEPARTMENT", "DATE_FROM", "DATE_TO", "UNIT_CODE", "UNIT",
        "WAREHOUSE_LOAD_DATE", "name_norm", "lib_last_name", "lib_first_name"
    ]],
    how="left",
    left_on="moira_last_name",
    right_on="lib_last_name",
    suffixes=("_MOIRA", "_LIB")
)

cand["fuzzy_score"] = cand.apply(
    lambda r: simple_ratio(str(r.get("name_norm_MOIRA", "")), str(r.get("name_norm_LIB", ""))),
    axis=1
)

fuzzy_good = cand.loc[cand["fuzzy_score"] >= 90].copy()

cols_common = [
    "MOIRA_LIST_KEY", "MOIRA_LIST_OWNER_KEY", "moira_list_member", "MOIRA_LIST_MEMBER_FULL_NAME",
    "MOIRA_LIST_MEMBER_MIT_ID"
]
instr_cols = [
    "LIBRARY_COURSE_INSTRUCTOR_KEY", "COURSE_NAME", "INSTRUCTOR_NAME", "DEPARTMENT",
    "DATE_FROM", "DATE_TO", "UNIT_CODE", "UNIT", "WAREHOUSE_LOAD_DATE"
]

exact_keep = exact_matches[
    cols_common + [c for c in instr_cols] + ["name_norm"]
].copy()

fuzzy_keep = fuzzy_good[
    [*cols_common,
     "LIBRARY_COURSE_INSTRUCTOR_KEY", "COURSE_NAME", "INSTRUCTOR_NAME", "DEPARTMENT",
     "DATE_FROM", "DATE_TO", "UNIT_CODE", "UNIT", "WAREHOUSE_LOAD_DATE",
     "name_norm_MOIRA"]
].copy()
fuzzy_keep = fuzzy_keep.rename(columns={"name_norm_MOIRA": "name_norm"})

has_exact = exact_keep.groupby("MOIRA_LIST_MEMBER_FULL_NAME")["LIBRARY_COURSE_INSTRUCTOR_KEY"].apply(lambda s: s.notna().any())
members_with_exact = set(has_exact[has_exact].index)

fuzzy_subset = fuzzy_keep[~fuzzy_keep["MOIRA_LIST_MEMBER_FULL_NAME"].isin(members_with_exact)].copy()

moira_instructors = pd.concat([exact_keep, fuzzy_subset], ignore_index=True)

# 7) Enrichment: connect matched instructor-course rows to reserve materials and enrollment info
moira_instr_with_reserves = moira_instructors.merge(
    lib_res[["LIBRARY_COURSE_INSTRUCTOR_KEY", "LIBRARY_RESERVE_CATALOG_KEY", "LIBRARY_SUBJECT_OFFERED_KEY", "TERM_CODE", "SUBJECT_ID"]],
    how="left",
    on="LIBRARY_COURSE_INSTRUCTOR_KEY"
)

sos_slim = sos[[
    "SUBJECT_OFFERED_SUMMARY_KEY", "TERM_CODE", "SUBJECT_ID", "SUBJECT_TITLE", "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME", "RESPONSIBLE_FACULTY_NAME", "RESPONSIBLE_FACULTY_MIT_ID", "NUM_ENROLLED_STUDENTS"
]].copy()

moira_full = moira_instr_with_reserves.merge(
    sos_slim,
    how="left",
    on=["TERM_CODE", "SUBJECT_ID"],
    suffixes=("", "_SOS")
)

# 8) Build final answer per the question:
# "For each course instructor in the 'keeper-zephyr' mailing list, provide:
#  - the name of mailing lists they subscribe to,
#  - instructor name,
#  - earliest and latest publication years,
#  - total number of enrolled students."
#
# Interpretation aligned to available data:
# - Mailing list name(s): from MOIRA_LIST_KEY for the matched rows (all 'keeper-zephyr' here).
# - Instructor name: INSTRUCTOR_NAME from library course instructor matches.
# - Publication years: interpret as year extracted from DATE_FROM / DATE_TO in LIBRARY_COURSE_INSTRUCTOR,
#   taking min(DATE_FROM.year) as earliest, max(DATE_TO.year) as latest among matched rows.
# - Total enrolled students: sum of NUM_ENROLLED_STUDENTS from SUBJECT_OFFERED_SUMMARY across matched subjects/terms.

def to_year(s):
    # Handle datetime, date, string-like years; return pandas.NA for missing
    if pd.isna(s):
        return pd.NA
    # If already datetime-like
    if isinstance(s, (pd.Timestamp, )):
        return s.year
    # Try to parse
    try:
        ts = pd.to_datetime(s, errors="coerce")
        if pd.isna(ts):
            # maybe it's already a year number
            try:
                return int(str(s)[:4])
            except Exception:
                return pd.NA
        return ts.year
    except Exception:
        return pd.NA

agg_df = moira_full.copy()

# Extract years from DATE_FROM / DATE_TO (these are on the instructor-course rows)
agg_df["YEAR_FROM"] = agg_df["DATE_FROM"].apply(to_year) if "DATE_FROM" in agg_df.columns else pd.NA
agg_df["YEAR_TO"] = agg_df["DATE_TO"].apply(to_year) if "DATE_TO" in agg_df.columns else pd.NA

# Group by mailing list and instructor
group_cols = ["MOIRA_LIST_KEY", "INSTRUCTOR_NAME"]

# Compute aggregations
final_agg = (
    agg_df.groupby(group_cols, dropna=False)
    .agg(
        earliest_publication_year=("YEAR_FROM", lambda s: pd.to_numeric(s, errors="coerce").min()),
        latest_publication_year=("YEAR_TO", lambda s: pd.to_numeric(s, errors="coerce").max()),
        total_enrolled_students=("NUM_ENROLLED_STUDENTS", lambda s: pd.to_numeric(s, errors="coerce").fillna(0).sum())
    )
    .reset_index()
)

# Keep only rows for the target mailing list (safety filter)
final_agg = final_agg[final_agg["MOIRA_LIST_KEY"] == target_list_key].copy()

# Sort for readability
final_agg = final_agg.sort_values(["INSTRUCTOR_NAME"]).reset_index(drop=True)

# Assemble result as required
result = {
    "keeper_zephyr_instructor_summary": final_agg.rename(columns={
        "MOIRA_LIST_KEY": "mailing_list",
        "INSTRUCTOR_NAME": "instructor_name"
    })[["mailing_list", "instructor_name", "earliest_publication_year", "latest_publication_year", "total_enrolled_students"]]
}