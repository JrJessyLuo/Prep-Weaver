import pandas as pd

# ------------------------------------------------------------------------------
# Source input tables from `tables` dict (already provided in the environment)
# ------------------------------------------------------------------------------
scd = tables["table_1"].copy()  # SIS_COURSE_DESCRIPTION
sdp = tables.get("table_2", pd.DataFrame()).copy()  # STUDENT_DEGREE_PROGRAM
cip = tables["table_4"].copy()  # CIP
dept = tables.get("table_6", pd.DataFrame()).copy()  # SIS_DEPARTMENT

# ------------------------------------------------------------------------------
# Try to locate a CIP program code field in SIS_COURSE_DESCRIPTION
# Common candidates: CIP_PROGRAM_CODE, CIP_CODE, PROGRAM_CODE
# ------------------------------------------------------------------------------
candidate_cols = [c for c in scd.columns if c.upper() in {"CIP_PROGRAM_CODE", "CIP_CODE", "PROGRAM_CODE"}]
if len(candidate_cols) == 0:
    # If no explicit CIP code is present in SIS_COURSE_DESCRIPTION, try to bridge via STUDENT_DEGREE_PROGRAM by COURSE
    left_key = "COURSE" if "COURSE" in scd.columns else None
    right_key = "COURSE" if not sdp.empty and "COURSE" in sdp.columns else None
    if left_key and right_key and not sdp.empty:
        sdp_cols = sdp.columns.tolist()
        sdp_prog_col = "PROGRAM_CODE" if "PROGRAM_CODE" in sdp_cols else None
        if sdp_prog_col is None and "DEGREE_CODE" in sdp_cols:
            sample = sdp["DEGREE_CODE"].dropna().astype(str).str.replace(r"\D", "", regex=True).str.len()
            if (sample == 6).mean() > 0.3:
                sdp_prog_col = "DEGREE_CODE"

        if sdp_prog_col:
            course_to_prog = (
                sdp[[right_key, sdp_prog_col]]
                .dropna()
                .rename(columns={right_key: "COURSE", sdp_prog_col: "PROGRAM_CODE"})
                .drop_duplicates(subset=["COURSE", "PROGRAM_CODE"])
            )
            scd = scd.merge(course_to_prog, on="COURSE", how="left")
            candidate_cols = ["PROGRAM_CODE"]

# Standardize chosen CIP program code column name to PROGRAM_CODE for join
if "PROGRAM_CODE" not in candidate_cols:
    if len(candidate_cols) == 1:
        scd = scd.rename(columns={candidate_cols[0]: "PROGRAM_CODE"})
    else:
        scd["PROGRAM_CODE"] = pd.NA

# Ensure both join keys are strings for safe merging
scd["PROGRAM_CODE"] = scd["PROGRAM_CODE"].astype(str).str.strip()
cip["PROGRAM_CODE"] = cip["PROGRAM_CODE"].astype(str).str.strip()

# ------------------------------------------------------------------------------
# Select and prepare columns from SIS_COURSE_DESCRIPTION for downstream use
# ------------------------------------------------------------------------------
keep_from_scd = []
for col in ["COURSE", "COURSE_LEVEL", "DEPARTMENT", "DEPARTMENT_NAME", "SCHOOL_NAME", "FROM_TERM", "THRU_TERM", "PROGRAM_CODE"]:
    if col in scd.columns:
        keep_from_scd.append(col)
scd_narrow = scd[keep_from_scd].copy()

# ------------------------------------------------------------------------------
# Join SIS_COURSE_DESCRIPTION to CIP on PROGRAM_CODE to bring in CATEGORY and VERSION
# ------------------------------------------------------------------------------
cip_keep = ["PROGRAM_CODE", "CATEGORY_CODE", "CATEGORY_TITLE", "VERSION"]
cip_narrow = cip[cip_keep].drop_duplicates(subset=["PROGRAM_CODE", "VERSION"], keep="last")
merged = scd_narrow.merge(cip_narrow, on="PROGRAM_CODE", how="left")

# ------------------------------------------------------------------------------
# Optionally bring IS_DEGREE_GRANTING via department code (if available)
# ------------------------------------------------------------------------------
if not dept.empty and "DEPARTMENT" in merged.columns and "DEPARTMENT_CODE" in dept.columns:
    tmp_dept = dept[["DEPARTMENT_CODE", "IS_DEGREE_GRANTING"]].drop_duplicates("DEPARTMENT_CODE")
    tmp_dept["DEPARTMENT_CODE"] = tmp_dept["DEPARTMENT_CODE"].astype(str).str.strip()
    merged["DEPARTMENT"] = merged["DEPARTMENT"].astype(str).str.strip()
    merged = merged.merge(tmp_dept, left_on="DEPARTMENT", right_on="DEPARTMENT_CODE", how="left")
    if "DEPARTMENT_CODE" in merged.columns:
        merged = merged.drop(columns=["DEPARTMENT_CODE"])

# ------------------------------------------------------------------------------
# Compute final answers required by the question:
# - category title
# - version
# - department name
# - school name
# - total number of courses for each course level
# - total number of degree-granting courses for each CIP category code
# ------------------------------------------------------------------------------
# Clean up fields
if "COURSE_LEVEL" in merged.columns:
    merged["COURSE_LEVEL"] = merged["COURSE_LEVEL"].astype(str).str.strip()
if "CATEGORY_CODE" in merged.columns:
    merged["CATEGORY_CODE"] = merged["CATEGORY_CODE"].astype(str).str.strip()
if "IS_DEGREE_GRANTING" in merged.columns:
    merged["IS_DEGREE_GRANTING"] = merged["IS_DEGREE_GRANTING"].astype(str).str.strip()

# 1) Total number of courses for each COURSE_LEVEL by CIP attributes and org info
group_cols_courses = []
for c in ["CATEGORY_CODE", "CATEGORY_TITLE", "VERSION", "DEPARTMENT_NAME", "SCHOOL_NAME", "COURSE_LEVEL"]:
    if c in merged.columns:
        group_cols_courses.append(c)

courses_by_level = (
    merged.groupby(group_cols_courses, dropna=False)
    .agg(total_courses=("COURSE", "nunique"))
    .reset_index()
)

# 2) Total number of degree-granting courses for each CIP CATEGORY_CODE
# Define a flag for degree-granting = 'Y'
if "IS_DEGREE_GRANTING" in merged.columns:
    dg_flag = merged["IS_DEGREE_GRANTING"].fillna("").str.upper().eq("Y")
else:
    # If not available, create a False flag so counts are zero
    dg_flag = pd.Series(False, index=merged.index)

merged["IS_DG_FLAG"] = dg_flag

dg_group_cols = []
for c in ["CATEGORY_CODE", "CATEGORY_TITLE", "VERSION"]:
    if c in merged.columns:
        dg_group_cols.append(c)

degree_granting_by_cip = (
    merged.loc[merged["IS_DG_FLAG"]]
    .groupby(dg_group_cols, dropna=False)
    .agg(total_degree_granting_courses=("COURSE", "nunique"))
    .reset_index()
)

# ------------------------------------------------------------------------------
# Package final result(s) into dict[str, DataFrame] as required
# ------------------------------------------------------------------------------
result = {
    "courses_by_level": courses_by_level,
    "degree_granting_by_cip": degree_granting_by_cip,
}