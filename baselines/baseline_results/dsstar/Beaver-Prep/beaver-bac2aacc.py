import pandas as pd
import numpy as np

# Helper functions (adapted to in-memory tables dict)
def normalize_term_code(col: pd.Series) -> pd.Series:
    return col.astype(str).str.strip()

def is_summer_term(term_codes: pd.Series) -> pd.Series:
    s = term_codes.astype(str).str.strip()
    return s.str.endswith("SU")

def safe_select(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    present = [c for c in cols if c in df.columns]
    return df[present].copy()

# Source dataframes from provided `tables` dict
df_summary = tables['table_1'].copy()
df_offered = tables['table_2'].copy()
df_drupal = tables['table_6'].copy()

# Normalize TERM_CODE
if "TERM_CODE" in df_offered.columns:
    df_offered["TERM_CODE"] = normalize_term_code(df_offered["TERM_CODE"])
if "TERM_CODE" in df_summary.columns:
    df_summary["TERM_CODE"] = normalize_term_code(df_summary["TERM_CODE"])

# Filter SUBJECT_OFFERED to summer terms
mask_summer_offered = is_summer_term(df_offered["TERM_CODE"]) if "TERM_CODE" in df_offered.columns else pd.Series(False, index=df_offered.index)
df_offered_summer = df_offered.loc[mask_summer_offered].copy()

# Select needed columns from SUBJECT_OFFERED
cols_needed_offered = [
    "SUBJECT_KEY",
    "SUBJECT_OFFERED_SUMMARY_KEY",
    "COMPOSITE_SUBJECT_KEY",
    "TERM_CODE",
    "COURSE_NUMBER",
    "SUBJECT_ID",
    "SUBJECT_TITLE",
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "RESPONSIBLE_FACULTY_NAME",
    "responsible_faculty_mit_id",
    "CLUSTER_TYPE"
]
df_offered_summer_sel = safe_select(df_offered_summer, cols_needed_offered)

# Prepare DRUPAL_COURSE_CATALOG fields
drupal_cols_possible = [
    "ACADEMIC_YEAR",
    "SUBJECT_ID",
    "SUBJECT_CODE",
    "SUBJECT_NUMBER",
    "PRINT_SUBJECT_ID",
    "SUBJECT_TITLE",
    "SUBJECT_TITLE_LONG",
    "SUBJECT_DESCRIPTION",
    "DESCRIPTION",
    "INSTRUCTOR_EMAIL",
    "INSTRUCTOR_NAME",
    "DEPARTMENT_CODE",
    "DEPARTMENT_NAME",
    "BUILDING",
    "ROOM",
    "FLOOR",
    "STREET",
    "ADDRESS",
    "LOCATION",
]
drupal_cols_present = [c for c in drupal_cols_possible if c in df_drupal.columns]
df_drupal_sel = df_drupal[drupal_cols_present].copy()

# Derive academic year from TERM_CODE
if "TERM_CODE" in df_offered_summer_sel.columns:
    df_offered_summer_sel["ACADEMIC_YEAR_FROM_TERM"] = pd.to_numeric(df_offered_summer_sel["TERM_CODE"].str[:4], errors="coerce").astype("Int64")

# Ensure ACADEMIC_YEAR is numeric Int64
if "ACADEMIC_YEAR" in df_drupal_sel.columns:
    df_drupal_sel["ACADEMIC_YEAR"] = pd.to_numeric(df_drupal_sel["ACADEMIC_YEAR"], errors="coerce").astype("Int64")

# Merge on SUBJECT_ID + ACADEMIC_YEAR when possible
can_merge_on_year = ("SUBJECT_ID" in df_offered_summer_sel.columns and
                     "ACADEMIC_YEAR_FROM_TERM" in df_offered_summer_sel.columns and
                     "SUBJECT_ID" in df_drupal_sel.columns and
                     "ACADEMIC_YEAR" in df_drupal_sel.columns)

if can_merge_on_year:
    df_offered_summer_sel["SUBJECT_ID"] = df_offered_summer_sel["SUBJECT_ID"].astype(str)
    df_drupal_sel["SUBJECT_ID"] = df_drupal_sel["SUBJECT_ID"].astype(str)

    left_for_year = df_offered_summer_sel.rename(columns={"ACADEMIC_YEAR_FROM_TERM": "ACADEMIC_YEAR"})
    df_merge_year = pd.merge(
        left_for_year,
        df_drupal_sel,
        on=["SUBJECT_ID", "ACADEMIC_YEAR"],
        how="left",
        suffixes=("", "_DRUPAL")
    )
else:
    df_merge_year = df_offered_summer_sel.copy()

# Fallback merge for rows missing description fields: SUBJECT_ID-only to most recent year in Drupal
if "SUBJECT_ID" in df_merge_year.columns and "SUBJECT_ID" in df_drupal_sel.columns:
    if "ACADEMIC_YEAR" in df_drupal_sel.columns:
        drupal_recent = (
            df_drupal_sel.sort_values(["SUBJECT_ID", "ACADEMIC_YEAR"], ascending=[True, False])
            .drop_duplicates(subset=["SUBJECT_ID"], keep="first")
        )
    else:
        drupal_recent = df_drupal_sel.drop_duplicates(subset=["SUBJECT_ID"], keep="first").copy()

    desc_cols = [c for c in ["SUBJECT_TITLE_LONG", "SUBJECT_DESCRIPTION", "DESCRIPTION"] if c in df_merge_year.columns] or []
    need_backfill_mask = pd.Series(False, index=df_merge_year.index)
    for dc in desc_cols:
        need_backfill_mask |= df_merge_year[dc].isna()

    if need_backfill_mask.any():
        df_to_fill = df_merge_year.loc[need_backfill_mask].copy()
        cols_to_drop = [c for c in drupal_cols_present if c in df_to_fill.columns and c not in ["SUBJECT_ID"]]
        df_filled = pd.merge(
            df_to_fill.drop(columns=cols_to_drop, errors="ignore"),
            drupal_recent,
            on="SUBJECT_ID",
            how="left",
            suffixes=("", "_DRUPAL2"),
        )
        df_merge_year.loc[need_backfill_mask, df_filled.columns] = df_filled.values

df_summer_with_drupal = df_merge_year

# Compute per-department counts of distinct CLUSTER_TYPE from SUBJECT_OFFERED_SUMMARY filtered to summer
mask_summer_summary = is_summer_term(df_summary["TERM_CODE"]) if "TERM_CODE" in df_summary.columns else pd.Series(False, index=df_summary.index)
df_summary_summer = df_summary.loc[mask_summer_summary].copy()

dept_col = "OFFER_DEPT_CODE" if "OFFER_DEPT_CODE" in df_summary_summer.columns else None
cluster_col = "CLUSTER_TYPE" if "CLUSTER_TYPE" in df_summary_summer.columns else None

if dept_col and cluster_col:
    df_summary_summer[dept_col] = df_summary_summer[dept_col].astype(str)
    df_cluster_agg = (
        df_summary_summer.groupby(dept_col)[cluster_col]
        .nunique(dropna=True)
        .reset_index(name="DISTINCT_CLUSTER_TYPE_COUNT")
    )
else:
    df_cluster_agg = pd.DataFrame(columns=["OFFER_DEPT_CODE", "DISTINCT_CLUSTER_TYPE_COUNT"])

# Merge aggregate back to the summer subject rows by OFFER_DEPT_CODE
if "OFFER_DEPT_CODE" in df_summer_with_drupal.columns:
    df_summer_with_drupal["OFFER_DEPT_CODE"] = df_summer_with_drupal["OFFER_DEPT_CODE"].astype(str)
    df_final = pd.merge(
        df_summer_with_drupal,
        df_cluster_agg,
        left_on="OFFER_DEPT_CODE",
        right_on="OFFER_DEPT_CODE",
        how="left",
    )
else:
    df_final = df_summer_with_drupal.copy()

# Build output with requested fields:
# titles of subjects offered in the summer term along with their descriptions,
# responsible faculty names, email address, building name, room name, floor level, building street address,
# and the total number of types of courses per department.
output_cols_priority = [
    "TERM_CODE",
    "SUBJECT_ID",
    "SUBJECT_TITLE",
    "SUBJECT_TITLE_LONG" if "SUBJECT_TITLE_LONG" in df_final.columns else None,
    "SUBJECT_DESCRIPTION" if "SUBJECT_DESCRIPTION" in df_final.columns else None,
    "DESCRIPTION" if "DESCRIPTION" in df_final.columns else None,
    "RESPONSIBLE_FACULTY_NAME",
    "INSTRUCTOR_EMAIL" if "INSTRUCTOR_EMAIL" in df_final.columns else None,
    "BUILDING" if "BUILDING" in df_final.columns else None,
    "ROOM" if "ROOM" in df_final.columns else None,
    "FLOOR" if "FLOOR" in df_final.columns else None,
    "STREET" if "STREET" in df_final.columns else None,
    "ADDRESS" if "ADDRESS" in df_final.columns else None,
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME" if "OFFER_DEPT_NAME" in df_final.columns else None,
    "DISTINCT_CLUSTER_TYPE_COUNT",
]
output_cols = [c for c in output_cols_priority if c is not None and c in df_final.columns]
df_output = df_final[output_cols].copy()

# Assign final result as required
result = {
    "summer_subjects_with_details_and_dept_cluster_counts": df_output
}