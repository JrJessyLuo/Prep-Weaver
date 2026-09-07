import pandas as pd

# Input tables already loaded in `tables`
df_instr = tables['table_1']
df_detail = tables['table_2']

# Ensure key columns exist
key_col = "LIBRARY_COURSE_INSTRUCTOR_KEY"
assert key_col in df_instr.columns, f"Missing {key_col} in LIBRARY_COURSE_INSTRUCTOR"
assert key_col in df_detail.columns, f"Missing {key_col} in LIBRARY_RESERVE_MATRL_DETAIL"

# Inner merge on LIBRARY_COURSE_INSTRUCTOR_KEY
merged = df_instr.merge(df_detail, on=key_col, how="inner", suffixes=("_INSTR", "_DETAIL"))

# Filter to relevant columns
cols_needed = [
    "LIBRARY_COURSE_INSTRUCTOR_KEY",
    "INSTRUCTOR_NAME",
    "COURSE_NAME",
    "LIBRARY_SUBJECT_OFFERED_KEY",
]
missing_cols = [c for c in cols_needed if c not in merged.columns]
assert not missing_cols, f"Missing columns after merge: {missing_cols}"

filtered = merged[cols_needed].copy()

# Group and compute material_count
agg = (
    filtered.groupby(
        ["LIBRARY_COURSE_INSTRUCTOR_KEY", "LIBRARY_SUBJECT_OFFERED_KEY", "INSTRUCTOR_NAME", "COURSE_NAME"],
        dropna=False
    )
    .size()
    .rename("material_count")
    .reset_index()
)

# Assign final answer
result = {
    "course_instructor_materials": agg
}