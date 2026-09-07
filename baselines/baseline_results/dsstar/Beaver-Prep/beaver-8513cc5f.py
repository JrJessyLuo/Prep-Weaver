import pandas as pd
import numpy as np

# Source tables from the provided dict `tables`
fac = tables['table_1'].copy()
fclt = tables['table_2'].copy()
fclt_hist = tables['table_3'].copy()
hr_fac_roster = tables['table_4'].copy()
mdh = tables['table_5'].copy()
se_person = tables['table_6'].copy()
# tables['table_7'] HR_ORG_UNIT not used in reference logic
hr_org_unit_new = tables['table_8'].copy()
fclt_org_dlc = tables['table_9'].copy()
mdh_links = tables['table_10'].copy()

# Build unified base (from reference plan)
fac_sel = fac.rename(columns={
    "ORGANIZATION_ID": "organization_id",
    "ORGANIZATION": "organization",
    "ORGANIZATION_NAME": "organization_name",
    "ORGANIZATION_LEVEL": "organization_level",
    "ORGANIZATION_NUMBER": "organization_number",
}).loc[:, ["organization_id", "organization", "organization_name", "organization_level", "organization_number"]]

fclt_sel = fclt.rename(columns={
    "ORGANIZATION_ID": "organization_id",
    "ORGANIZATION": "organization",
    "ORGANIZATION_NAME": "organization_name",
    "ORGANIZATION_LEVEL": "organization_level",
    "ORGANIZATION_NUMBER": "organization_number",
}).loc[:, ["organization_id", "organization", "organization_name", "organization_level", "organization_number"]]

base = pd.concat([fac_sel, fclt_sel], ignore_index=True)
base = base[~base["organization_id"].astype(str).isin(['139', '250'])].drop_duplicates().reset_index(drop=True)

# Step 1: Append DLC_KEY where available to help join to MASTER_DEPT_HIERARCHY
fclt_dlc_cols = fclt.rename(columns={
    "ORGANIZATION_ID": "organization_id",
    "DLC_KEY": "dlc_key"
})[["organization_id", "dlc_key"]].drop_duplicates()

# Fallback mapping via FCLT_ORG_DLC_KEY (ORG_KEY -> DLC_KEY), need to map ORG_KEY to ORG_ID from FCLT_ORGANIZATION
fclt_org_id_key = fclt.rename(columns={
    "FCLT_ORGANIZATION_KEY": "fclt_organization_key",
    "ORGANIZATION_ID": "organization_id"
})[["fclt_organization_key", "organization_id"]].drop_duplicates()

fclt_org_dlc_mapped = fclt_org_dlc.rename(columns={
    "FCLT_ORGANIZATION_KEY": "fclt_organization_key",
    "DLC_KEY": "dlc_key"
}).merge(fclt_org_id_key, on="fclt_organization_key", how="left")[["organization_id", "dlc_key"]].dropna().drop_duplicates()

# Use FCLT_ORGANIZATION_HIST to map ORG_ID -> DLC_KEY
fclt_hist_map = fclt_hist.rename(columns={
    "ORGANIZATION_ID": "organization_id",
    "DLC_KEY": "dlc_key"
})[["organization_id", "dlc_key"]].dropna().drop_duplicates()

# Consolidate DLC mappings
dlc_map = pd.concat([fclt_dlc_cols, fclt_org_dlc_mapped, fclt_hist_map], ignore_index=True)\
    .dropna().drop_duplicates()

# Attach DLC to base
base_with_dlc = base.merge(dlc_map, on="organization_id", how="left")

# Step 2: Join to MASTER_DEPT_HIERARCHY to get HIERARCHY_TYPE (and keep DLC fields for reference)
mdh_keep = mdh.rename(columns={
    "DLC_KEY": "dlc_key",
    "DLC_NAME": "dlc_name",
    "DLC_CODE": "dlc_code",
    "HIERARCHY_TYPE": "hierarchy_type"
})[["hierarchy_type", "dlc_key", "dlc_code", "dlc_name"]].drop_duplicates()

base_hier = base_with_dlc.merge(mdh_keep, on="dlc_key", how="left")

# Step 3: Compute employee counts per organization
se_person_org = se_person.rename(columns={"ORGANIZATION": "organization"})[["MIT_ID", "organization", "EMPLOYEE_TYPE", "IS_ACTIVE"]]
se_person_org["is_active_flag"] = (se_person_org["IS_ACTIVE"].astype(str).str.upper() == "Y").astype(int)

emp_counts_by_org = se_person_org.groupby("organization", dropna=False).agg(
    active_employees=("is_active_flag", "sum"),
    all_employees=("MIT_ID", "nunique")
).reset_index()

# Step 4: Flag emeritus vs non-emeritus from HR_FACULTY_ROSTER
emer = hr_fac_roster.rename(columns={"EMERITUS_STATUS": "emeritus_status", "MIT_ID": "MIT_ID"})[["MIT_ID", "emeritus_status"]]
emer["is_emeritus"] = emer["emeritus_status"].fillna("").str.strip().str.upper().isin(["Y", "YES", "EMERITUS"]).astype(int)
emer_by_person = emer.groupby("MIT_ID", as_index=False).agg(is_emeritus=("is_emeritus", "max"))

# Map emeritus to organizations using SE_PERSON
se_person_with_emer = se_person_org.merge(emer_by_person, on="MIT_ID", how="left")
se_person_with_emer["is_emeritus"] = se_person_with_emer["is_emeritus"].fillna(0).astype(int)
se_person_with_emer["is_non_emeritus"] = np.where(se_person_with_emer["is_emeritus"] == 1, 0, 1)

emer_counts_by_org = se_person_with_emer.groupby("organization", dropna=False).agg(
    emeritus_count=("is_emeritus", "sum"),
    non_emeritus_count=("is_non_emeritus", "sum")
).reset_index()

# Combine employee counts
org_person_counts = emp_counts_by_org.merge(emer_counts_by_org, on="organization", how="outer").fillna(0)
for c in ["active_employees", "all_employees", "emeritus_count", "non_emeritus_count"]:
    org_person_counts[c] = org_person_counts[c].astype(int)

# Step 5: Join counts back to base by organization name
result_df = base_hier.merge(org_person_counts, on="organization", how="left")

# Step 6: Derive break group by organization and level (same heuristic as reference)
result_df["break_group"] = result_df["organization_level"]

# Step 7: Prepare fields and formatting
result_df["organization_id"] = result_df["organization_id"].astype(int)
result_df["name"] = result_df["organization_name"].fillna(result_df["organization"])
result_df["formatted_name"] = result_df["organization"].fillna("").str.strip() + " - " + result_df["name"].fillna("").str.strip()
result_df["formatted_name"] = result_df["formatted_name"].str.strip(" -")

# Select and sort as requested
final_cols = [
    "break_group",
    "organization_id",
    "name",
    "formatted_name",
    "organization_number",
    "organization_level",
    "hierarchy_type",
    "all_employees",
    "active_employees",
    "emeritus_count",
    "non_emeritus_count",
]
final_table = result_df.loc[:, final_cols].drop_duplicates()

# Ensure integer columns are proper dtype (fill NaN with 0 before casting)
for c in ["all_employees", "active_employees", "emeritus_count", "non_emeritus_count"]:
    final_table[c] = final_table[c].fillna(0).astype(int)

# Sort by hierarchy type as requested, and then by name for stability
final_table = final_table.sort_values(by=["hierarchy_type", "name"], kind="mergesort").reset_index(drop=True)

# Add totals for employer counts (grand total row)
totals = pd.DataFrame([{
    "break_group": "TOTAL",
    "organization_id": np.nan,
    "name": "TOTAL",
    "formatted_name": "TOTAL",
    "organization_number": np.nan,
    "organization_level": np.nan,
    "hierarchy_type": "TOTAL",
    "all_employees": final_table["all_employees"].sum(),
    "active_employees": final_table["active_employees"].sum(),
    "emeritus_count": final_table["emeritus_count"].sum(),
    "non_emeritus_count": final_table["non_emeritus_count"].sum(),
}])

# Optional: also add hierarchy_type-level subtotals
subtotals = (
    final_table.groupby("hierarchy_type", dropna=False)[["all_employees", "active_employees", "emeritus_count", "non_emeritus_count"]]
    .sum()
    .reset_index()
)
subtotals["break_group"] = "SUBTOTAL"
subtotals["organization_id"] = np.nan
subtotals["name"] = subtotals["hierarchy_type"].astype(str) + " SUBTOTAL"
subtotals["formatted_name"] = subtotals["name"]
subtotals["organization_number"] = np.nan
subtotals["organization_level"] = np.nan
subtotals = subtotals.loc[:, final_cols]

# Append subtotals after each hierarchy_type block
# We'll interleave by concatenating and resorting so that subtotals appear after their group
final_with_sub = pd.concat([final_table, subtotals], ignore_index=True)
# Create an order key to ensure subtotal appears after the group
final_with_sub["_is_subtotal"] = (final_with_sub["break_group"] == "SUBTOTAL").astype(int)
final_with_sub = final_with_sub.sort_values(
    by=["hierarchy_type", "_is_subtotal", "name"],
    ascending=[True, True, True],
    kind="mergesort"
).drop(columns=["_is_subtotal"]).reset_index(drop=True)

# Append grand total at the end
final_with_totals = pd.concat([final_with_sub, totals.loc[:, final_cols]], ignore_index=True)

# Prepare result mapping
result = {
    "organization_summary": final_with_totals
}