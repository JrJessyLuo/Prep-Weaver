import pandas as pd
import numpy as np

# The input DataFrames are provided in a dict named `tables`
# Mapping:
# tables['table_1'] -> SIS_DEPARTMENT.pkl
# tables['table_3'] -> SIS_SUBJECT_CODE.pkl

# Load required tables from the provided `tables` dict
df_department = tables['table_1'].copy()
df_subject_code = tables['table_3'].copy()

# Helper to standardize strings safely (kept for parity with reference, though not heavily used)
def std_str(s):
    if s is None:
        return s
    return str(s).strip().lower()

# Validate required columns presence as in reference logic
required_subj_cols = {"SCHOOL_CODE", "SCHOOL_NAME", "SUBJECT_CODE", "COURSE_NUMBER"}
missing_subj = required_subj_cols - set(df_subject_code.columns)
if missing_subj:
    raise ValueError(f"Missing required columns in SIS_SUBJECT_CODE: {missing_subj}")

required_dept_cols = {"SCHOOL_CODE", "SCHOOL_NAME", "DEPARTMENT_CODE"}
missing_dept = required_dept_cols - set(df_department.columns)
if missing_dept:
    raise ValueError(f"Missing required columns in SIS_DEPARTMENT: {missing_dept}")

# Prepare subject code data (reproduce reference logic)
df_sc = df_subject_code.copy()

# Normalize COURSE_NUMBER for robust min/max (string-wise per reference instructions)
df_sc["COURSE_NUMBER_NORM"] = (
    df_sc["COURSE_NUMBER"]
    .astype(str)
    .str.strip()
    .str.lower()
)

# Keep only rows with non-null SUBJECT_CODE
df_sc_nonnull = df_sc.dropna(subset=["SUBJECT_CODE"]).copy()

# Build per-school summary from SIS_SUBJECT_CODE (reference logic)
subjects_by_school = (
    df_sc_nonnull
    .groupby(["SCHOOL_CODE", "SCHOOL_NAME"], dropna=False)
    .agg(
        total_SIS_subjects=("SUBJECT_CODE", "nunique"),
        min_course=("COURSE_NUMBER_NORM", lambda s: s.dropna().min() if len(s.dropna()) else np.nan),
        max_course=("COURSE_NUMBER_NORM", lambda s: s.dropna().max() if len(s.dropna()) else np.nan),
    )
    .reset_index()
)

# Concatenate unique DLC_KEYs per school as representative sample (exclude NaNs); cap to avoid extreme length
def concat_unique(values, max_items=10):
    uniq = pd.Series(values).dropna().astype(str).unique().tolist()
    if len(uniq) == 0:
        return np.nan
    if len(uniq) > max_items:
        shown = ", ".join(uniq[:max_items])
        return f"{shown} ...(+{len(uniq)-max_items} more)"
    return ", ".join(uniq)

# Build per-school summary from SIS_DEPARTMENT (reference logic)
departments_by_school = (
    df_department
    .dropna(subset=["DEPARTMENT_CODE"])
    .groupby(["SCHOOL_CODE", "SCHOOL_NAME"], dropna=False)
    .agg(
        total_departments=("DEPARTMENT_CODE", "nunique"),
        representative_DLC_KEY=("DLC_KEY", concat_unique),
    )
    .reset_index()
)

# Merge summaries to create the final table (reference logic)
final_table = (
    subjects_by_school
    .merge(
        departments_by_school,
        on=["SCHOOL_CODE", "SCHOOL_NAME"],
        how="left",
        validate="m:1"
    )
    .sort_values(["SCHOOL_CODE", "SCHOOL_NAME"])
    .reset_index(drop=True)
)

# The question asks for school code, school name, DLC key, the graduate level,
# total number of SIS subjects, min & max course numbers, and total number of departments.
# The reference code does not produce graduate level; it is not available in the given
# reference logic/tables. We will include a Graduate_Level column set to NaN to keep schema.
final_columns = [
    "SCHOOL_CODE",
    "SCHOOL_NAME",
    "representative_DLC_KEY",
    "total_SIS_subjects",
    "min_course",
    "max_course",
    "total_departments",
]
answer_df = final_table.copy()

# Insert a placeholder column for Graduate Level as it isn't computed in the reference
answer_df.insert(3, "Graduate_Level", np.nan)

# Reorder to match the requested output order
answer_df = answer_df[[
    "SCHOOL_CODE",
    "SCHOOL_NAME",
    "representative_DLC_KEY",
    "Graduate_Level",
    "total_SIS_subjects",
    "min_course",
    "max_course",
    "total_departments",
]]

# Assign the final answer to `result` as required
result = {"per_school_subjects_departments": answer_df}