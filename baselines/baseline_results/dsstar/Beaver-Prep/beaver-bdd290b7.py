import pandas as pd
import numpy as np

# Source input tables from the provided `tables` dict
df_detail = tables['table_1'].copy()
df_person = tables['table_2'].copy()

# Standardize key column names for merge (same logic as reference)
left_key = "IAP_SUBJECT_PERSON_KEY"
right_key = "iap_subject_person_key"

if left_key not in df_detail.columns:
    raise KeyError(f"Expected column '{left_key}' not found in IAP_SUBJECT_DETAIL")
if right_key not in df_person.columns:
    raise KeyError(f"Expected column '{right_key}' not found in IAP_SUBJECT_PERSON")

# Select only needed columns from person dataframe
person_cols = [right_key, "PERSON_NAME", "PERSON_EMAIL"]
missing = [c for c in person_cols if c not in df_person.columns]
if missing:
    raise KeyError(f"Missing expected columns in IAP_SUBJECT_PERSON: {missing}")

df_person_slim = df_person[person_cols].copy()

# Perform left merge
df_merged = df_detail.merge(
    df_person_slim,
    how="left",
    left_on=left_key,
    right_on=right_key,
    validate="m:1"
)

# Drop duplicate right_key column after merge
if right_key in df_merged.columns:
    df_merged = df_merged.drop(columns=[right_key])

# Derive academic year from TERM_CODE
def derive_academic_year(term):
    if pd.isna(term):
        return np.nan
    term_str = str(term)
    if len(term_str) >= 4 and term_str[:4].isdigit():
        return int(term_str[:4])
    import re
    m = re.search(r'(\d{4})', term_str)
    if m:
        return int(m.group(1))
    return np.nan

if "TERM_CODE" not in df_merged.columns:
    df_merged["TERM_CODE"] = np.nan

df_merged["ACADEMIC_YEAR_DERIVED"] = df_merged["TERM_CODE"].apply(derive_academic_year)

# Prepare fields for aggregation
for col in ["FEE", "MAX_ENROLLMENT"]:
    if col in df_merged.columns:
        df_merged[col] = pd.to_numeric(df_merged[col], errors="coerce")

# Identify a subject/session key for unique counting.
possible_session_keys = [
    "IAP_SUBJECT_SESSION_KEY",
    "IAP_SUBJECT_PERSON_KEY",
    "IAP_SUBJECT_CATEGORY_KEY",
]
session_key = None
for c in possible_session_keys:
    if c in df_merged.columns:
        session_key = c
        break
if session_key is None:
    session_key = "_row_id_"
    df_merged[session_key] = df_merged.reset_index().index

# Group by PERSON_EMAIL, PERSON_NAME, TERM_CODE, and academic year
group_keys = ["PERSON_EMAIL", "PERSON_NAME", "TERM_CODE", "ACADEMIC_YEAR_DERIVED"]

agg_dict = {
    session_key: pd.Series.nunique,
}
if "FEE" in df_merged.columns:
    agg_dict.update({
        "FEE": ["min", "max"]
    })
if "MAX_ENROLLMENT" in df_merged.columns:
    agg_dict.update({
        "MAX_ENROLLMENT": "sum"
    })

grouped = df_merged.groupby(group_keys, dropna=False).agg(agg_dict)

# Flatten columns after multiple aggregations
grouped.columns = [
    (f"total_iap_subjects" if col[0] == session_key else f"{col[0]}_{col[1]}")
    if isinstance(col, tuple) else col
    for col in grouped.columns
]
grouped = grouped.reset_index()

# Ensure expected output columns exist even if source cols missing
if "FEE_min" not in grouped.columns:
    grouped["FEE_min"] = np.nan
if "FEE_max" not in grouped.columns:
    grouped["FEE_max"] = np.nan
if "MAX_ENROLLMENT_sum" not in grouped.columns:
    grouped["MAX_ENROLLMENT_sum"] = np.nan

# Reorder columns for readability, focusing on the question's requested fields
final_cols_order = [
    "PERSON_EMAIL",
    "PERSON_NAME",
    "ACADEMIC_YEAR_DERIVED",
    "total_iap_subjects",
    "FEE_min",
    "FEE_max",
    "MAX_ENROLLMENT_sum",
    "TERM_CODE",
]
final_cols_order = [c for c in final_cols_order if c in grouped.columns] + \
                   [c for c in grouped.columns if c not in final_cols_order]
df_summary = grouped[final_cols_order].copy()

# Prepare final result mapping as required
result = {
    "iap_person_year_summary": df_summary
}