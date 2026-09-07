import pandas as pd

# The input tables are provided in a dict named `tables`
term_df = tables['table_8'].copy()             # ACADEMIC_TERM_PARAMETER.pkl
sum_df = tables['table_4'].copy()              # SUBJECT_OFFERED_SUMMARY.pkl
emp_df = tables['table_9'].copy()              # EMPLOYEE_DIRECTORY.pkl

# Validate required columns for term parameter
required_cols = {"IS_CURRENT_TERM", "term_code"}
missing = required_cols - set(term_df.columns)
if missing:
    raise ValueError(f"Missing required columns in ACADEMIC_TERM_PARAMETER.pkl: {missing}")

# Filter current term
current_term_df = term_df[term_df["IS_CURRENT_TERM"].astype(str).str.upper().eq("Y")].copy()

# Determine the current term row
if not current_term_df.empty:
    if "TERM_START_DATE" in current_term_df.columns:
        current_term_df["TERM_START_DATE"] = pd.to_datetime(current_term_df["TERM_START_DATE"], errors="coerce")
        current_term_df = current_term_df.sort_values("TERM_START_DATE", ascending=False)
    current_row = current_term_df.iloc[0].to_dict()
    current_term_code = current_row.get("term_code")
    current_academic_year = current_row.get("TERM_DESCRIPTION") or current_row.get("TERM_PARAMETER")
else:
    current_term_code = None
    current_academic_year = None

# Ensure required columns exist in SUBJECT_OFFERED_SUMMARY
needed_sum_cols = {
    "TERM_CODE", "HGN_CODE", "TOTAL_UNITS", "OFFER_DEPT_NAME",
    "RESPONSIBLE_FACULTY_NAME", "RESPONSIBLE_FACULTY_MIT_ID", "CLUSTER_TYPE"
}
missing_sum = needed_sum_cols - set(sum_df.columns)
if missing_sum:
    raise ValueError(f"Missing required columns in SUBJECT_OFFERED_SUMMARY.pkl: {missing_sum}")

# If no current term code determined, derive it as latest by TERM_START_DATE if available
if current_term_code is None:
    # Fallback: pick the most recent by TERM_START_DATE; else pick the most frequent TERM_CODE in summary
    if "TERM_START_DATE" in term_df.columns:
        term_df["TERM_START_DATE"] = pd.to_datetime(term_df["TERM_START_DATE"], errors="coerce")
        term_df_sorted = term_df.sort_values("TERM_START_DATE", ascending=False)
        if not term_df_sorted.empty:
            current_term_code = str(term_df_sorted.iloc[0]["term_code"])
            current_academic_year = term_df_sorted.iloc[0].get("TERM_DESCRIPTION") or term_df_sorted.iloc[0].get("TERM_PARAMETER")
    if current_term_code is None and not sum_df.empty:
        current_term_code = str(sum_df["TERM_CODE"].astype(str).mode().iloc[0])

# Filter to the current term code
filtered = sum_df[sum_df["TERM_CODE"].astype(str).eq(str(current_term_code))].copy()

# Derive/attach ACADEMIC_YEAR:
if "ACADEMIC_YEAR" in filtered.columns:
    filtered["ACADEMIC_YEAR_DERIVED"] = filtered["ACADEMIC_YEAR"]
else:
    # Map from term_code to a descriptor
    term_map = {}
    key = "TERM_DESCRIPTION" if "TERM_DESCRIPTION" in term_df.columns else None
    if key is None:
        key = "TERM_PARAMETER" if "TERM_PARAMETER" in term_df.columns else None
    if key is not None:
        term_map = dict(zip(term_df["term_code"].astype(str), term_df[key].astype(str)))
    filtered["ACADEMIC_YEAR_DERIVED"] = filtered["TERM_CODE"].astype(str).map(term_map).fillna("")

# Select requested columns
selected_cols = [
    "ACADEMIC_YEAR_DERIVED",
    "TERM_CODE",
    "HGN_CODE",
    "TOTAL_UNITS",
    "OFFER_DEPT_NAME",
    "RESPONSIBLE_FACULTY_NAME",
    "RESPONSIBLE_FACULTY_MIT_ID"
]
filtered_sel = filtered[selected_cols].copy()

# Compute metrics per TERM_CODE:
metrics = filtered.groupby("TERM_CODE").agg(
    distinct_cluster_types=("CLUSTER_TYPE", lambda s: s.dropna().astype(str).nunique()),
    avg_total_units=("TOTAL_UNITS", "mean"),
    n_rows=("TERM_CODE", "size")
).reset_index()

# Validate EMPLOYEE_DIRECTORY columns
needed_emp_cols = {"MIT_ID", "EMAIL_ADDRESS", "FULL_NAME"}
missing_emp = needed_emp_cols - set(emp_df.columns)
if missing_emp:
    raise ValueError(f"Missing required columns in EMPLOYEE_DIRECTORY.pkl: {missing_emp}")

# Prepare key types for join
def clean_mit_id(series):
    s = pd.to_numeric(series, errors="coerce").astype("Int64")
    return s

filtered_sel["RESPONSIBLE_FACULTY_MIT_ID_JOIN"] = clean_mit_id(filtered_sel["RESPONSIBLE_FACULTY_MIT_ID"])
emp_df["MIT_ID_JOIN"] = clean_mit_id(emp_df["MIT_ID"])

# Columns for join from employee directory (include optional if present)
emp_join_cols = ["MIT_ID_JOIN", "EMAIL_ADDRESS"]
for opt_col in ["FULL_NAME", "KRB_NAME_UPPERCASE", "EMAIL_ADDRESS_UPPERCASE"]:
    if opt_col in emp_df.columns:
        emp_join_cols.append(opt_col)
emp_slim = emp_df[emp_join_cols].copy()

joined = filtered_sel.merge(
    emp_slim,
    left_on="RESPONSIBLE_FACULTY_MIT_ID_JOIN",
    right_on="MIT_ID_JOIN",
    how="left",
    suffixes=("", "_EMP")
)

# Build final detail table
final_cols = [
    "ACADEMIC_YEAR_DERIVED",
    "TERM_CODE",
    "HGN_CODE",
    "TOTAL_UNITS",
    "OFFER_DEPT_NAME",
    "RESPONSIBLE_FACULTY_NAME",
    "RESPONSIBLE_FACULTY_MIT_ID",
    "EMAIL_ADDRESS"
]
# Keep only columns that exist (in case EMAIL_ADDRESS missing)
final_cols_existing = [c for c in final_cols if c in joined.columns]
final_df = joined[final_cols_existing].copy()

# Prepare metrics table with friendly column names per the question
metrics_renamed = metrics.rename(columns={
    "TERM_CODE": "TERM_CODE",
    "distinct_cluster_types": "TOTAL_TYPES_OF_COURSES",
    "avg_total_units": "AVERAGE_TOTAL_UNITS",
    "n_rows": "ROW_COUNT"
})

# Compose result mapping
result = {
    "course_details_current_term": final_df,
    "per_term_metrics": metrics_renamed
}