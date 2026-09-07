import pandas as pd

# Access input tables from provided `tables` dict
df_sis_subject_code = tables['table_1']  # SIS_SUBJECT_CODE.pkl
cis = tables['table_3']                  # CIS_COURSE_CATALOG.pkl

# Select and standardize key columns from SIS_SUBJECT_CODE
sis_cols_needed = ["SUBJECT_CODE", "SUBJECT_CODE_DESC", "DEPARTMENT_NAME", "COURSE_NUMBER"]
sis_present_cols = [c for c in sis_cols_needed if c in df_sis_subject_code.columns]
sis = df_sis_subject_code[sis_present_cols].copy()

# Prepare CIS course catalog core mapping columns
cis_map_cols = [c for c in [
    "SUBJECT_CODE", "SUBJECT_NUMBER", "DEPARTMENT_CODE", "DEPARTMENT_NAME",
    "ACADEMIC_YEAR", "EFFECTIVE_TERM_CODE",
    # potential level indicators discovered in reference exploration
    "GRADE_TYPE", "GRADE_TYPE_DESC", "GRADE_RULE", "GRADE_RULE_DESC"
] if c in cis.columns]
cis_sub = cis[cis_map_cols].copy()

# Heuristic for "graduate level":
# The reference exploration did not reveal an explicit graduate-level flag.
# Common MIT heuristic: courses numbered 100+ are graduate-level.
# SUBJECT_NUMBER is alphanumeric; extract leading integer where possible.
def to_int_prefix(s):
    if pd.isna(s):
        return pd.NA
    s = str(s).strip()
    num = ""
    for ch in s:
        if ch.isdigit():
            num += ch
        else:
            break
    return int(num) if num != "" else pd.NA

cis_sub["SUBJECT_NUM_INT"] = cis_sub["SUBJECT_NUMBER"].map(to_int_prefix)

# Determine graduate level flag
cis_sub["GRAD_LEVEL"] = pd.NA
cis_sub.loc[cis_sub["SUBJECT_NUM_INT"].notna(), "GRAD_LEVEL"] = (
    cis_sub.loc[cis_sub["SUBJECT_NUM_INT"].notna(), "SUBJECT_NUM_INT"] >= 100
)

# Aggregate total number of courses per department and grad level
dept_level_counts = (
    cis_sub
    .dropna(subset=["DEPARTMENT_NAME"])  # ensure department present
    .groupby(["DEPARTMENT_NAME", "GRAD_LEVEL"], dropna=False)
    .agg(total_courses=("SUBJECT_NUMBER", "nunique"))
    .reset_index()
)

# Join SIS subject code and description to departments via SUBJECT_CODE mapping
# We will get the SIS subject code(s) that appear in CIS per department.
dept_subject_map = (
    cis_sub[["DEPARTMENT_NAME", "SUBJECT_CODE"]]
    .dropna()
    .drop_duplicates()
)

# Attach SIS subject code descriptions from SIS table
sis_map_small = sis[["SUBJECT_CODE", "SUBJECT_CODE_DESC"]].drop_duplicates()
dept_subject_with_desc = dept_subject_map.merge(sis_map_small, on="SUBJECT_CODE", how="left")

# Combine counts with SIS mappings:
# Some departments may map to multiple SUBJECT_CODEs; we will keep all combinations.
final_df = (
    dept_level_counts
    .merge(dept_subject_with_desc, on="DEPARTMENT_NAME", how="left")
    .loc[:, ["DEPARTMENT_NAME", "SUBJECT_CODE", "SUBJECT_CODE_DESC", "GRAD_LEVEL", "total_courses"]]
    .sort_values(["DEPARTMENT_NAME", "GRAD_LEVEL", "SUBJECT_CODE"], kind="mergesort")
    .reset_index(drop=True)
)

# Present GRAD_LEVEL as human-friendly labels
def grad_label(x):
    if pd.isna(x):
        return "Unknown"
    return "Graduate" if bool(x) else "Undergraduate"

final_df["GRAD_LEVEL"] = final_df["GRAD_LEVEL"].map(grad_label)

# Assign to result as required
result = {
    "dept_sis_subject_grad_counts": final_df
}