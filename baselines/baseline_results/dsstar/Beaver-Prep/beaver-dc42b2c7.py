import pandas as pd
import numpy as np

# ----------------------------
# Load dataframes from provided `tables` dict
# ----------------------------
cis_df = tables['table_1'].copy()
offered_df = tables['table_2'].copy()
drupal_df = tables['table_3'].copy()
hass_df = tables['table_4'].copy()
subj_attr_df = tables['table_5'].copy()
sis_code_df = tables['table_6'].copy()
offered_summary_df = tables['table_7'].copy()
sis_course_desc_df = tables['table_8'].copy()
student_degree_df = tables['table_9'].copy()

# ----------------------------
# Helpers
# ----------------------------
def std(s):
    return s.strip().upper() if isinstance(s, str) else s

for df in [cis_df, offered_df, drupal_df, sis_code_df, offered_summary_df, student_degree_df, hass_df, subj_attr_df]:
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(std)

# Identify Political Science codes from SIS_SUBJECT_CODE
pol_codes = sis_code_df.loc[
    sis_code_df["SUBJECT_CODE_DESC"].str.contains("POLITICAL SCIENCE", na=False)
    | sis_code_df["DEPARTMENT_NAME"].str.contains("POLITICAL SCIENCE", na=False)
    | sis_code_df["SUBJECT_CODE"].isin(["17"]),
    ["SUBJECT_CODE", "SUBJECT_CODE_DESC", "DEPARTMENT_CODE", "DEPARTMENT_NAME"]
].drop_duplicates()

if pol_codes.empty:
    pol_codes = pd.DataFrame(
        [{"SUBJECT_CODE": "17", "SUBJECT_CODE_DESC": "POLITICAL SCIENCE"}]
    )

pol_subject_codes = set(pol_codes["SUBJECT_CODE"].dropna().unique())
pol_dept_codes = set(pol_codes["DEPARTMENT_CODE"].dropna().unique())

# ----------------------------
# Implement plan (reproducing reference logic)
# ----------------------------
# 1) Filter SUBJECT_OFFERED_SUMMARY to Political Science
pol_filter = pd.Series(False, index=offered_summary_df.index)
if "COURSE_NUMBER" in offered_summary_df.columns:
    pol_filter = pol_filter | offered_summary_df["COURSE_NUMBER"].isin(pol_subject_codes)
if "OFFER_DEPT_NAME" in offered_summary_df.columns:
    pol_filter = pol_filter | offered_summary_df["OFFER_DEPT_NAME"].str.contains("POLITICAL SCIENCE", na=False)
if "OFFER_DEPT_CODE" in offered_summary_df.columns and len(pol_dept_codes) > 0:
    pol_filter = pol_filter | offered_summary_df["OFFER_DEPT_CODE"].isin(pol_dept_codes)

offered_summary_pol = offered_summary_df.loc[pol_filter].copy()

# 2) Join to CIS_HASS_ATTRIBUTE via HASS attribute codes present in SUBJECT_OFFERED_SUMMARY
hass_codes = set(hass_df["hass_attribute"].dropna().astype(str).str.upper().unique())
if "HGN_CODE" in offered_summary_pol.columns:
    offered_summary_pol["ATTR_CODE"] = offered_summary_pol["HGN_CODE"].where(
        offered_summary_pol["HGN_CODE"].isin(hass_codes), np.nan
    )
else:
    offered_summary_pol["ATTR_CODE"] = np.nan

# 3) Join to SIS_SUBJECT_CODE for SUBJECT_CODE_DESC (subject area description)
sis_map = sis_code_df[["SUBJECT_CODE", "SUBJECT_CODE_DESC", "DEPARTMENT_CODE", "DEPARTMENT_NAME"]].drop_duplicates()
offered_summary_pol = offered_summary_pol.merge(
    sis_map.rename(columns={"SUBJECT_CODE": "COURSE_NUMBER"}),
    on="COURSE_NUMBER",
    how="left"
)

# 4) Degree-granting departments indicator from STUDENT_DEGREE_PROGRAM
deg_dept_codes = set(student_degree_df["DEPARTMENT"].dropna().unique()) if "DEPARTMENT" in student_degree_df.columns else set()
offered_summary_pol["IS_DEGREE_DEPT"] = False
if "OFFER_DEPT_CODE" in offered_summary_pol.columns and len(deg_dept_codes) > 0:
    offered_summary_pol["IS_DEGREE_DEPT"] = offered_summary_pol["OFFER_DEPT_CODE"].isin(deg_dept_codes)

# 5) Attach HASS attribute descriptions (name/description) from CIS_HASS_ATTRIBUTE
hass_lookup = hass_df.rename(columns={
    "hass_attribute": "ATTR_CODE",
    "DESCRIPTION_IN_BULLETIN": "HASS_DESCRIPTION",
    "CIS_ATTRIBUTE_GROUP": "HASS_GROUP",
    "CIS_ATTRIBUTE_GROUP_NOTE": "HASS_GROUP_NOTE"
})[["ATTR_CODE", "HASS_DESCRIPTION", "HASS_GROUP", "HASS_GROUP_NOTE"]].drop_duplicates()

offered_summary_pol = offered_summary_pol.merge(hass_lookup, on="ATTR_CODE", how="left")

# 6) Group by HASS attribute to compute required metrics
group_key = "ATTR_CODE"
subject_id_cols = [c for c in ["SUBJECT_ID", "MASTER_SUBJECT_ID", "SUBJECT_SUMMARY_KEY", "COMPOSITE_SUBJECT_KEY"] if c in offered_summary_pol.columns]
if subject_id_cols:
    subj_id_col = subject_id_cols[0]
else:
    subj_id_col = "SUBJECT_TITLE" if "SUBJECT_TITLE" in offered_summary_pol.columns else None

agg_dict = {
    "TOTAL_UNITS": "mean",
    "NUM_ENROLLED_STUDENTS": "sum",
}
group_cols = [group_key]
agg_df = offered_summary_pol.groupby(group_cols).agg(agg_dict).reset_index()

# Unique subject count
if subj_id_col is not None:
    uniq_subj = offered_summary_pol.groupby(group_cols)[subj_id_col].nunique(dropna=True).reset_index().rename(columns={subj_id_col: "NUM_UNIQUE_SUBJECTS"})
    agg_df = agg_df.merge(uniq_subj, on=group_cols, how="left")
else:
    agg_df["NUM_UNIQUE_SUBJECTS"] = np.nan

# Distinct OFFER_DEPT_CODE granting degrees
if "OFFER_DEPT_CODE" in offered_summary_pol.columns:
    deg_dept_counts = (
        offered_summary_pol.loc[offered_summary_pol["IS_DEGREE_DEPT"]]
        .groupby(group_cols)["OFFER_DEPT_CODE"]
        .nunique(dropna=True)
        .reset_index()
        .rename(columns={"OFFER_DEPT_CODE": "NUM_DISTINCT_DEGREE_DEPTS"})
    )
    agg_df = agg_df.merge(deg_dept_counts, on=group_cols, how="left")
else:
    agg_df["NUM_DISTINCT_DEGREE_DEPTS"] = np.nan

# Attach attribute descriptions (from hass_lookup)
agg_df = agg_df.merge(hass_lookup, left_on="ATTR_CODE", right_on="ATTR_CODE", how="left")

# Subject code description (from SIS_SUBJECT_CODE): aggregate distinct descriptions appearing under each attribute
if "SUBJECT_CODE_DESC" in offered_summary_pol.columns:
    subj_desc_per_attr = (
        offered_summary_pol.groupby("ATTR_CODE")["SUBJECT_CODE_DESC"]
        .apply(lambda x: ", ".join(sorted(set([s for s in x.dropna().unique() if isinstance(s, str)]))) if x.notna().any() else np.nan)
        .reset_index()
        .rename(columns={"SUBJECT_CODE_DESC": "SUBJECT_CODE_DESC_LIST"})
    )
    agg_df = agg_df.merge(subj_desc_per_attr, on="ATTR_CODE", how="left")
else:
    agg_df["SUBJECT_CODE_DESC_LIST"] = np.nan

# For readability, fill attribute label: prefer HASS_DESCRIPTION, else HASS_GROUP, else ATTR_CODE
agg_df["HASS_ATTRIBUTE_LABEL"] = agg_df["HASS_DESCRIPTION"].where(agg_df["HASS_DESCRIPTION"].notna(), agg_df["HASS_GROUP"])
agg_df["HASS_ATTRIBUTE_LABEL"] = agg_df["HASS_ATTRIBUTE_LABEL"].where(agg_df["HASS_ATTRIBUTE_LABEL"].notna(), agg_df["ATTR_CODE"])

# Order columns per question
cols_order = [
    "ATTR_CODE",
    "HASS_ATTRIBUTE_LABEL",        # attribute name
    "HASS_DESCRIPTION",            # attribute description
    "NUM_UNIQUE_SUBJECTS",
    "TOTAL_UNITS",                 # average units
    "NUM_ENROLLED_STUDENTS",       # total enrollment
    "NUM_DISTINCT_DEGREE_DEPTS",   # number of departments that grant degrees
    "SUBJECT_CODE_DESC_LIST"       # subject code description(s)
]
cols_order = [c for c in cols_order if c in agg_df.columns]
final_df = agg_df[cols_order].sort_values(["ATTR_CODE"]).reset_index(drop=True)

# Assign final answer
result = {
    "political_science_by_hass_attribute": final_df
}