import pandas as pd

# The input tables are already loaded in a dict named `tables`
lib_subj = tables['table_1'].copy()  # LIBRARY_SUBJECT_OFFERED.pkl
lib_res = tables['table_6'].copy()   # LIBRARY_RESERVE_MATRL_DETAIL.pkl

def _std_str_series(s: pd.Series) -> pd.Series:
    s = s.astype(str)
    s = s.str.strip()
    s = s.str.replace(r"\s+", " ", regex=True)
    return s.str.upper()

# Preserve originals for diagnostics (not printed)
lib_subj_raw = lib_subj.copy()
lib_res_raw = lib_res.copy()

# Standardize keys and fields as in reference
lib_subj["LIBRARY_SUBJECT_OFFERED_KEY_STD"] = _std_str_series(lib_subj["LIBRARY_SUBJECT_OFFERED_KEY"])
lib_res["LIBRARY_SUBJECT_OFFERED_KEY_STD"] = _std_str_series(lib_res["LIBRARY_SUBJECT_OFFERED_KEY"])

if "term_code" in lib_subj.columns:
    lib_subj["TERM_CODE_STD"] = _std_str_series(lib_subj["term_code"])
else:
    lib_subj["TERM_CODE_STD"] = pd.NA

if "TERM_CODE" in lib_res.columns:
    lib_res["TERM_CODE_STD"] = _std_str_series(lib_res["TERM_CODE"])
else:
    lib_res["TERM_CODE_STD"] = pd.NA

if "SUBJECT_ID" in lib_subj.columns:
    lib_subj["SUBJECT_ID_STD"] = _std_str_series(lib_subj["SUBJECT_ID"])
else:
    lib_subj["SUBJECT_ID_STD"] = pd.NA

if "SUBJECT_ID" in lib_res.columns:
    lib_res["SUBJECT_ID_STD"] = _std_str_series(lib_res["SUBJECT_ID"])
else:
    lib_res["SUBJECT_ID_STD"] = pd.NA

# Attempt 1 merge by standardized key (reference shows this succeeds and is used)
merged_key = lib_res.merge(
    lib_subj,
    how="inner",
    left_on="LIBRARY_SUBJECT_OFFERED_KEY_STD",
    right_on="LIBRARY_SUBJECT_OFFERED_KEY_STD",
    suffixes=("_RES", "_LIB")
)

if merged_key.empty:
    lhs = lib_res[lib_res["TERM_CODE_STD"].notna() & lib_res["SUBJECT_ID_STD"].notna()].copy()
    rhs = lib_subj[lib_subj["TERM_CODE_STD"].notna() & lib_subj["SUBJECT_ID_STD"].notna()].copy()
    lhs = lhs.drop_duplicates(subset=["TERM_CODE_STD", "SUBJECT_ID_STD"])
    rhs = rhs.drop_duplicates(subset=["TERM_CODE_STD", "SUBJECT_ID_STD"])
    merged = lhs.merge(
        rhs,
        how="inner",
        on=["TERM_CODE_STD", "SUBJECT_ID_STD"],
        suffixes=("_RES", "_LIB"),
    )
else:
    merged = merged_key

# Compute required metrics per department
# - Department name column per reference preview: OFFER_DEPT_NAME
# - Courses using library materials: count distinct LIBRARY_SUBJECT_OFFERED_KEY (from LIB side)
# - Number of catalog items: count distinct LIBRARY_RESERVE_CATALOG_KEY (from RES side)
# - Average enrollment per course: average of NUM_ENROLLED_STUDENTS at course level,
#   where course level is defined by unique LIBRARY_SUBJECT_OFFERED_KEY (LIB side).
dept_col = "OFFER_DEPT_NAME"

# Ensure columns exist
cols_needed = [
    dept_col,
    "LIBRARY_SUBJECT_OFFERED_KEY_LIB",
    "LIBRARY_RESERVE_CATALOG_KEY",
    "NUM_ENROLLED_STUDENTS"
]
existing = [c for c in cols_needed if c in merged.columns]
# We proceed assuming the reference columns exist as shown in the sample output

# Build course-level table (one row per course per department) to compute enrollment per course
course_level = merged[
    [dept_col, "LIBRARY_SUBJECT_OFFERED_KEY_LIB", "NUM_ENROLLED_STUDENTS"]
].drop_duplicates(subset=[dept_col, "LIBRARY_SUBJECT_OFFERED_KEY_LIB"])

# Aggregations
dept_courses = course_level.groupby(dept_col, dropna=False).agg(
    total_courses=("LIBRARY_SUBJECT_OFFERED_KEY_LIB", "nunique"),
    avg_enrollment_per_course=("NUM_ENROLLED_STUDENTS", "mean"),
).reset_index()

dept_items = merged.groupby(dept_col, dropna=False).agg(
    num_catalog_items=("LIBRARY_RESERVE_CATALOG_KEY", "nunique")
).reset_index()

dept_summary = dept_courses.merge(dept_items, on=dept_col, how="left")

# Grand total row
grand_courses = course_level["LIBRARY_SUBJECT_OFFERED_KEY_LIB"].nunique()
grand_items = merged["LIBRARY_RESERVE_CATALOG_KEY"].nunique()
grand_avg_enroll = course_level["NUM_ENROLLED_STUDENTS"].mean()

grand_row = pd.DataFrame({
    dept_col: ["Grand Total"],
    "total_courses": [grand_courses],
    "avg_enrollment_per_course": [grand_avg_enroll],
    "num_catalog_items": [grand_items],
})

final_df = pd.concat([dept_summary, grand_row], ignore_index=True)

# Order and types
final_df = final_df[[dept_col, "total_courses", "num_catalog_items", "avg_enrollment_per_course"]]
final_df["total_courses"] = final_df["total_courses"].astype("Int64")
final_df["num_catalog_items"] = final_df["num_catalog_items"].astype("Int64")

# Assign to result dict as required
result = {"department_library_usage_summary": final_df}