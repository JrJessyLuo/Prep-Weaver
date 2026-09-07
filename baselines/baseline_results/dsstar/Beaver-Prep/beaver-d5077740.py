import pandas as pd

# Source tables from the provided 'tables' dict
df = tables['table_1'].copy()         # SUBJECT_OFFERED_SUMMARY.pkl
dept = tables['table_7'].copy()       # SIS_DEPARTMENT.pkl

# Prepare department subset to avoid column collisions
dept_small = dept[[
    "DEPARTMENT_CODE",
    "DEPARTMENT_NAME",
    "SCHOOL_CODE",
    "SCHOOL_NAME",
    "IS_DEGREE_GRANTING"
]].copy()

# Left join on OFFER_DEPT_CODE == DEPARTMENT_CODE
df_joined = df.merge(
    dept_small,
    how="left",
    left_on="OFFER_DEPT_CODE",
    right_on="DEPARTMENT_CODE",
    suffixes=("", "_DEPT")
)

# Ensure enrollment numeric and filter rows:
# - NUM_ENROLLED_STUDENTS not null and > 0
# - CLUSTER_TYPE not null
# - OFFER_SCHOOL_NAME not null
filtered = df_joined[
    (df_joined["NUM_ENROLLED_STUDENTS"].notna()) &
    (df_joined["NUM_ENROLLED_STUDENTS"] > 0) &
    (df_joined["CLUSTER_TYPE"].notna()) &
    (df_joined["OFFER_SCHOOL_NAME"].notna())
].copy()

# Normalize IS_DEGREE_GRANTING to Y/N/None
def _normalize_deg(x):
    if pd.isna(x):
        return None
    s = str(x).strip().upper()
    if s in ("Y", "YES", "1", "TRUE", "T"):
        return "Y"
    if s in ("N", "NO", "0", "FALSE", "F"):
        return "N"
    return s

filtered["IS_DEGREE_GRANTING"] = filtered["IS_DEGREE_GRANTING"].map(_normalize_deg)

# Helper to compute mode (first non-null)
def mode_first_non_null(series: pd.Series):
    s = series.dropna()
    if s.empty:
        return None
    vc = s.value_counts()
    return vc.index[0] if not vc.empty else None

# Group by cluster type, department name, and school name
group_cols = ["CLUSTER_TYPE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME"]

agg_df = (
    filtered
    .groupby(group_cols, dropna=False)
    .agg(
        subjects_count=("SUBJECT_OFFERED_SUMMARY_KEY", "nunique"),
        total_enrollment=("NUM_ENROLLED_STUDENTS", "sum"),
        avg_enrollment=("NUM_ENROLLED_STUDENTS", "mean"),
        IS_DEGREE_GRANTING=("IS_DEGREE_GRANTING", mode_first_non_null),
    )
    .reset_index()
)

# Cast numeric columns
agg_df["subjects_count"] = agg_df["subjects_count"].astype(int)
agg_df["total_enrollment"] = agg_df["total_enrollment"].astype(int)
agg_df["avg_enrollment"] = agg_df["avg_enrollment"].astype(float)

# Reorder and rename columns to match the question phrasing
final_cols = [
    "CLUSTER_TYPE",
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "IS_DEGREE_GRANTING",
    "subjects_count",
    "total_enrollment",
    "avg_enrollment",
]
final_df = agg_df[final_cols].sort_values(
    ["total_enrollment", "subjects_count"], ascending=[False, False]
).reset_index(drop=True)

# Package result
result = {
    "subjects_grouped_by_cluster_dept_school": final_df
}