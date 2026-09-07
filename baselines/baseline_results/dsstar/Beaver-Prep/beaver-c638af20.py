import pandas as pd

# Input tables are provided in `tables` dict:
# tables['table_1'] -> TIP_DETAIL.pkl
# tables['table_2'] -> TIP_MATERIAL_STATUS.pkl
# tables['table_3'] -> LIBRARY_MATERIAL_STATUS.pkl
# tables['table_4'] -> LIBRARY_RESERVE_MATRL_DETAIL.pkl
# tables['table_5'] -> TIP_MATERIAL.pkl
# tables['table_6'] -> TIP_SUBJECT_OFFERED.pkl
# tables['table_7'] -> SIS_DEPARTMENT.pkl
# tables['table_8'] -> LIBRARY_RESERVE_CATALOG.pkl
# tables['table_9'] -> HR_ORG_UNIT.pkl

# Load dataframes from provided `tables` dict
TIP_DETAIL = tables['table_1'].copy()
TIP_MATERIAL_STATUS = tables['table_2'].copy()
LIBRARY_MATERIAL_STATUS = tables['table_3'].copy()
LIBRARY_RESERVE_MATRL_DETAIL = tables['table_4'].copy()
TIP_MATERIAL = tables['table_5'].copy() if 'table_5' in tables else pd.DataFrame()
TIP_SUBJECT_OFFERED = tables['table_6'].copy() if 'table_6' in tables else pd.DataFrame()
SIS_DEPARTMENT = tables['table_7'].copy() if 'table_7' in tables else pd.DataFrame()
LIBRARY_RESERVE_CATALOG = tables['table_8'].copy() if 'table_8' in tables else pd.DataFrame()
HR_ORG_UNIT = tables['table_9'].copy() if 'table_9' in tables else pd.DataFrame()

# Normalize key columns for robust joins
def _to_str_strip(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

_to_str_strip(TIP_DETAIL, ["TIP_MATERIAL_STATUS_KEY", "TERM_CODE", "subject_id", "DEPT_ID", "DEPARTMENT_ID"])
_to_str_strip(TIP_MATERIAL_STATUS, ["tip_material_status_key"])
_to_str_strip(LIBRARY_RESERVE_MATRL_DETAIL, ["LIBRARY_MATERIAL_STATUS_KEY", "TERM_CODE", "SUBJECT_ID", "DEPT_ID", "DEPARTMENT_ID"])
_to_str_strip(LIBRARY_MATERIAL_STATUS, ["LIBRARY_MATERIAL_STATUS_KEY"])
_to_str_strip(SIS_DEPARTMENT, ["DEPARTMENT_ID", "DEPT_ID"])
_to_str_strip(TIP_SUBJECT_OFFERED, ["DEPARTMENT_ID", "DEPT_ID"])
_to_str_strip(LIBRARY_RESERVE_CATALOG, ["DEPARTMENT_ID", "DEPT_ID"])
_to_str_strip(HR_ORG_UNIT, ["ORG_UNIT_ID"])

# Resolve department name dimension
# Prefer SIS_DEPARTMENT if available; otherwise try HR_ORG_UNIT name if linked
dept_dim = pd.DataFrame()

if not SIS_DEPARTMENT.empty:
    # Common columns in SIS_DEPARTMENT are assumed: DEPARTMENT_ID (or DEPT_ID) and DEPARTMENT_NAME (or similar)
    # Standardize to DEPARTMENT_ID and DEPARTMENT_NAME
    cols = SIS_DEPARTMENT.columns
    dept_id_col = "DEPARTMENT_ID" if "DEPARTMENT_ID" in cols else ("DEPT_ID" if "DEPT_ID" in cols else None)
    dept_name_col = "DEPARTMENT_NAME" if "DEPARTMENT_NAME" in cols else (
        "DEPARTMENT_DESC" if "DEPARTMENT_DESC" in cols else (
            "DEPARTMENT" if "DEPARTMENT" in cols else None
        )
    )
    if dept_id_col is not None:
        dept_dim = SIS_DEPARTMENT[[dept_id_col] + ([dept_name_col] if dept_name_col else [])].drop_duplicates().rename(
            columns={dept_id_col: "DEPARTMENT_ID", (dept_name_col or "DEPARTMENT_ID"): "DEPARTMENT_NAME"}
        )
        if "DEPARTMENT_NAME" not in dept_dim.columns:
            dept_dim["DEPARTMENT_NAME"] = dept_dim["DEPARTMENT_ID"]
else:
    dept_dim = pd.DataFrame(columns=["DEPARTMENT_ID", "DEPARTMENT_NAME"])

# Helper to attach DEPARTMENT_ID to TIP_DETAIL via subject table if direct is missing
def attach_department(df, subj_df, subj_key="subject_id"):
    # If TIP_DETAIL already has DEPARTMENT_ID or DEPT_ID, prefer that
    if "DEPARTMENT_ID" in df.columns or "DEPT_ID" in df.columns:
        if "DEPARTMENT_ID" not in df.columns and "DEPT_ID" in df.columns:
            df = df.rename(columns={"DEPT_ID": "DEPARTMENT_ID"})
        return df
    # Else try to merge from TIP_SUBJECT_OFFERED
    if subj_df is not None and not subj_df.empty and subj_key in df.columns:
        # Standardize subject key/name
        _to_str_strip(subj_df, [subj_key, "DEPARTMENT_ID", "DEPT_ID"])
        subj = subj_df.copy()
        if "DEPARTMENT_ID" not in subj.columns and "DEPT_ID" in subj.columns:
            subj = subj.rename(columns={"DEPT_ID": "DEPARTMENT_ID"})
        keep_cols = [c for c in [subj_key, "DEPARTMENT_ID"] if c in subj.columns]
        subj = subj[keep_cols].drop_duplicates()
        df = df.merge(subj, how="left", on=subj_key)
    return df

# Helper to attach DEPARTMENT_ID to LIBRARY_RESERVE_MATRL_DETAIL via catalog if direct is missing
def attach_department_lib(df, catalog_df):
    if "DEPARTMENT_ID" in df.columns or "DEPT_ID" in df.columns:
        if "DEPARTMENT_ID" not in df.columns and "DEPT_ID" in df.columns:
            df = df.rename(columns={"DEPT_ID": "DEPARTMENT_ID"})
        return df
    if catalog_df is not None and not catalog_df.empty:
        cat = catalog_df.copy()
        # Find a common join key (e.g., COURSE_ID / SUBJECT_ID / CATALOG_KEY). We will try SUBJECT_ID then TERM_CODE+SUBJECT_ID
        join_cols = []
        if "SUBJECT_ID" in df.columns and "SUBJECT_ID" in cat.columns:
            join_cols = ["SUBJECT_ID"]
        elif all(c in df.columns for c in ["TERM_CODE", "SUBJECT_ID"]) and all(c in cat.columns for c in ["TERM_CODE", "SUBJECT_ID"]):
            join_cols = ["TERM_CODE", "SUBJECT_ID"]
        if join_cols:
            _to_str_strip(cat, join_cols + ["DEPARTMENT_ID", "DEPT_ID"])
            if "DEPARTMENT_ID" not in cat.columns and "DEPT_ID" in cat.columns:
                cat = cat.rename(columns={"DEPT_ID": "DEPARTMENT_ID"})
            keep_cols = [c for c in join_cols + ["DEPARTMENT_ID"] if c in cat.columns]
            cat = cat[keep_cols].drop_duplicates()
            df = df.merge(cat, how="left", on=join_cols)
    return df

# Build TIP side with status labels and department
tip_merged = TIP_DETAIL.copy()
# Attach department if needed
tip_merged = attach_department(tip_merged, TIP_SUBJECT_OFFERED, subj_key="subject_id")
if "DEPARTMENT_ID" not in tip_merged.columns:
    tip_merged["DEPARTMENT_ID"] = None

# Join status labels
if "TIP_MATERIAL_STATUS_KEY" in tip_merged.columns:
    tip_merged = tip_merged.merge(
        TIP_MATERIAL_STATUS[["tip_material_status_key", "TIP_MATERIAL_STATUS_CODE", "TIP_MATERIAL_STATUS"]],
        how="left",
        left_on="TIP_MATERIAL_STATUS_KEY",
        right_on="tip_material_status_key"
    )
else:
    # If no key, carry NaN status
    tip_merged["TIP_MATERIAL_STATUS"] = pd.NA

# Aggregate TIP counts by (DEPARTMENT_ID, TIP_MATERIAL_STATUS)
if "RECORD_COUNT" in tip_merged.columns:
    tip_counts = (
        tip_merged
        .groupby(["DEPARTMENT_ID", "TIP_MATERIAL_STATUS"], dropna=False, as_index=False)["RECORD_COUNT"]
        .sum()
        .rename(columns={"RECORD_COUNT": "TIP_COUNT"})
    )
else:
    tip_counts = (
        tip_merged
        .groupby(["DEPARTMENT_ID", "TIP_MATERIAL_STATUS"], dropna=False)
        .size()
        .reset_index(name="TIP_COUNT")
    )

# Build Library side with status labels and department
lib_merged = LIBRARY_RESERVE_MATRL_DETAIL.copy()
lib_merged = attach_department_lib(lib_merged, LIBRARY_RESERVE_CATALOG)
if "DEPARTMENT_ID" not in lib_merged.columns:
    lib_merged["DEPARTMENT_ID"] = None

lib_merged = lib_merged.merge(
    LIBRARY_MATERIAL_STATUS[["LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS_CODE", "LIBRARY_MATERIAL_STATUS"]],
    how="left",
    on="LIBRARY_MATERIAL_STATUS_KEY"
)

lib_counts = (
    lib_merged
    .groupby(["DEPARTMENT_ID", "LIBRARY_MATERIAL_STATUS"], dropna=False)
    .size()
    .reset_index(name="LIB_COUNT")
)

# Harmonize status values between TIP and Library
# We'll create a unified 'MATERIAL_STATUS' by taking the status string from each side and later outer-joining
tip_counts = tip_counts.rename(columns={"TIP_MATERIAL_STATUS": "MATERIAL_STATUS"})
lib_counts = lib_counts.rename(columns={"LIBRARY_MATERIAL_STATUS": "MATERIAL_STATUS"})

# Outer join on (DEPARTMENT_ID, MATERIAL_STATUS)
dept_status = pd.merge(
    tip_counts, lib_counts,
    how="outer",
    on=["DEPARTMENT_ID", "MATERIAL_STATUS"]
)

# Fill missing counts with 0
for c in ["TIP_COUNT", "LIB_COUNT"]:
    if c not in dept_status.columns:
        dept_status[c] = 0
dept_status["TIP_COUNT"] = dept_status["TIP_COUNT"].fillna(0).astype(int)
dept_status["LIB_COUNT"] = dept_status["LIB_COUNT"].fillna(0).astype(int)

# Attach department name
if not dept_dim.empty:
    dept_status = dept_status.merge(dept_dim[["DEPARTMENT_ID", "DEPARTMENT_NAME"]].drop_duplicates(), how="left", on="DEPARTMENT_ID")
else:
    dept_status["DEPARTMENT_NAME"] = dept_status["DEPARTMENT_ID"]

# Compute totals per row
dept_status["TOTAL_COUNT"] = dept_status["TIP_COUNT"] + dept_status["LIB_COUNT"]

# Prepare detail rows
detail_cols = ["DEPARTMENT_NAME", "MATERIAL_STATUS", "TIP_COUNT", "LIB_COUNT", "TOTAL_COUNT"]
detail = dept_status.copy()
# Ensure clean department names
detail["DEPARTMENT_NAME"] = detail["DEPARTMENT_NAME"].fillna("Unknown Department")
detail["MATERIAL_STATUS"] = detail["MATERIAL_STATUS"].fillna("Unknown Status")
detail = detail[detail_cols].sort_values(["DEPARTMENT_NAME", "MATERIAL_STATUS"]).reset_index(drop=True)

# Subtotals per department
dept_subtot = (
    detail
    .groupby("DEPARTMENT_NAME", as_index=False)[["TIP_COUNT", "LIB_COUNT", "TOTAL_COUNT"]]
    .sum()
)
dept_subtot["MATERIAL_STATUS"] = "Subtotal"
dept_subtot = dept_subtot[detail_cols]

# Grand total
grand_total = pd.DataFrame({
    "DEPARTMENT_NAME": ["Grand Total"],
    "MATERIAL_STATUS": ["Grand Total"],
    "TIP_COUNT": [detail["TIP_COUNT"].sum()],
    "LIB_COUNT": [detail["LIB_COUNT"].sum()],
    "TOTAL_COUNT": [detail["TOTAL_COUNT"].sum()],
})

# Concatenate detail + subtotal per department + grand total
# Interleave subtotals after each department's details
final_rows = []
for dept_name, grp in detail.groupby("DEPARTMENT_NAME", sort=True):
    final_rows.append(grp)
    st = dept_subtot[dept_subtot["DEPARTMENT_NAME"] == dept_name]
    final_rows.append(st)

final = pd.concat(final_rows + [grand_total], ignore_index=True)

# Assign to result dict as required
result = {
    "department_material_status_counts": final
}