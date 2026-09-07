import pandas as pd

# Source DataFrame from the provided tables dict
df = tables['table_6'].copy()

# Ensure TERM_CODE is string
df["TERM_CODE"] = df["TERM_CODE"].astype(str)

# Filter rows where TERM_CODE starts with "2022"
df_2022 = df[df["TERM_CODE"].str.startswith("2022", na=False)].copy()

# Determine course descriptor column
cols_available = df_2022.columns
course_col = "COURSE_NUMBER_DESC" if "COURSE_NUMBER_DESC" in cols_available else "SUBJECT_TITLE"

# Build selected columns list
select_cols = []
for c in ["ACADEMIC_YEAR", "RESPONSIBLE_FACULTY_NAME", course_col, "TERM_CODE"]:
    if c in cols_available:
        select_cols.append(c)

df_sel = df_2022[select_cols].copy()

# Clean instructor names: fill NaN and strip
if "RESPONSIBLE_FACULTY_NAME" in df_sel.columns:
    df_sel["RESPONSIBLE_FACULTY_NAME"] = df_sel["RESPONSIBLE_FACULTY_NAME"].fillna("").astype(str).str.strip()

# Drop rows without instructor or course descriptor
df_sel = df_sel[
    (df_sel.get("RESPONSIBLE_FACULTY_NAME", "") != "") &
    (df_sel[course_col].notna()) &
    (df_sel[course_col].astype(str).str.strip() != "")
].copy()

# If ACADEMIC_YEAR missing in dataset, derive from TERM_CODE's first 4 digits
if "ACADEMIC_YEAR" not in df_sel.columns and "TERM_CODE" in df_sel.columns:
    df_sel["ACADEMIC_YEAR"] = df_sel["TERM_CODE"].str[:4]

# Ensure ACADEMIC_YEAR is present
if "ACADEMIC_YEAR" not in df_sel.columns:
    raise KeyError("ACADEMIC_YEAR not found or derivable from the dataset.")

# Group and aggregate: number of unique course descriptors per instructor per academic year
answer_df = (
    df_sel
    .groupby(["ACADEMIC_YEAR", "RESPONSIBLE_FACULTY_NAME"], dropna=False)[course_col]
    .nunique()
    .reset_index(name="total_course_types")
    .sort_values(["ACADEMIC_YEAR", "RESPONSIBLE_FACULTY_NAME"])
)

# Package final answer
result = {
    "course_types_per_instructor_2022": answer_df
}