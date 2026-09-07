import pandas as pd

# Source dataframes from provided tables dict
df = tables['table_7']  # SUBJECT_OFFERED_SUMMARY

# 1) Inspect distinct HGN_CODE and HGN_CODE_DESC values to verify the label(s)
distinct_hgn = (
    df[['HGN_CODE', 'HGN_CODE_DESC']]
    .drop_duplicates()
    .sort_values(['HGN_CODE_DESC', 'HGN_CODE'])
    .reset_index(drop=True)
)

# Attempt to find the humanities/arts/social sciences label candidates programmatically
candidate_mask = (
    df['HGN_CODE_DESC']
    .astype(str)
    .str.contains('Humanit|Arts|Social', case=False, na=False)
)
candidate_labels = (
    df.loc[candidate_mask, ['HGN_CODE', 'HGN_CODE_DESC']]
    .drop_duplicates()
    .sort_values(['HGN_CODE_DESC', 'HGN_CODE'])
    .reset_index(drop=True)
)

# 2) Choose verified value(s) for filtering.
verified_hass_labels = candidate_labels['HGN_CODE_DESC'].dropna().unique().tolist()
if not verified_hass_labels:
    verified_hass_labels = ["Humanities, Arts, and Social Sciences"]

# 3) Re-filter using the verified value(s)
hass_df = df[df["HGN_CODE_DESC"].isin(verified_hass_labels)]

# Keep only relevant columns; attempt to include requested descriptive fields if present
cols_present = hass_df.columns.tolist()

# Determine best-effort column names for requested outputs
term_code_col = "TERM_CODE" if "TERM_CODE" in cols_present else None
term_desc_col = "TERM_DESC" if "TERM_DESC" in cols_present else None
attr_desc_col = "HGN_CODE_DESC" if "HGN_CODE_DESC" in cols_present else None
dept_name_col = None
school_name_col = None

# Common possible aliases for department and school names
dept_candidates = [c for c in cols_present if c.upper() in {"DEPARTMENT_NAME", "DEPT_NAME", "DEPARTMENT_DESC", "DEPARTMENT"}]
school_candidates = [c for c in cols_present if c.upper() in {"SCHOOL_NAME", "SCHOOL_DESC", "SCHOOL"}]
if dept_candidates:
    dept_name_col = dept_candidates[0]
if school_candidates:
    school_name_col = school_candidates[0]

# Fall back to group-by keys available
group_keys = []
if term_code_col: group_keys.append(term_code_col)
if term_desc_col: group_keys.append(term_desc_col)
if attr_desc_col: group_keys.append(attr_desc_col)
if dept_name_col: group_keys.append(dept_name_col)
if school_name_col: group_keys.append(school_name_col)

# Subject identifier columns (prefer SUBJECT_ID; fallback to SUBJECT)
subject_id_col = "SUBJECT_ID" if "SUBJECT_ID" in cols_present else ("SUBJECT" if "SUBJECT" in cols_present else None)

# If no subject identifier available, create a synthetic one from SUBJECT_GROUPING_KEY + SUBJECT_ID if possible
if subject_id_col is None:
    if "SUBJECT_GROUPING_KEY" in cols_present and "SUBJECT_ID" in cols_present:
        hass_df = hass_df.assign(_SUBJECT_SYN=hass_df["SUBJECT_GROUPING_KEY"].astype(str) + "|" + hass_df["SUBJECT_ID"].astype(str))
        subject_id_col = "_SUBJECT_SYN"

# If still not available, count rows as proxy
agg_spec = {}
if subject_id_col is not None:
    hass_df = hass_df.dropna(subset=[subject_id_col])
    agg_spec = {"unique_subjects": (subject_id_col, "nunique")}
else:
    agg_spec = {"unique_subjects": (hass_df.columns[0], "size")}  # size of group

# Ensure we have at least TERM_CODE and attribute description in output grouping
if term_code_col is None:
    # Create placeholder to allow grouping and provide an output
    hass_df = hass_df.assign(TERM_CODE_PLACEHOLDER="")
    term_code_col = "TERM_CODE_PLACEHOLDER"
if attr_desc_col is None:
    hass_df = hass_df.assign(HGN_CODE_DESC_PLACEHOLDER="Humanities, Arts, and Social Sciences")
    attr_desc_col = "HGN_CODE_DESC_PLACEHOLDER"

# Rebuild group keys with ensured fallbacks
group_keys = []
if term_code_col: group_keys.append(term_code_col)
if term_desc_col: group_keys.append(term_desc_col)
if attr_desc_col: group_keys.append(attr_desc_col)
if dept_name_col: group_keys.append(dept_name_col)
if school_name_col: group_keys.append(school_name_col)

subset = hass_df[group_keys + ([subject_id_col] if subject_id_col else [])]

counts = (
    subset.groupby(group_keys)
    .agg(**agg_spec)
    .reset_index()
    .sort_values(group_keys)
)

# Rename columns to match the question phrasing where possible
rename_map = {}
if term_code_col != "TERM_CODE":
    rename_map[term_code_col] = "TERM_CODE"
if term_desc_col:
    rename_map[term_desc_col] = "TERM_DESC"
if attr_desc_col != "HGN_CODE_DESC":
    rename_map[attr_desc_col] = "HGN_CODE_DESC"
if dept_name_col:
    rename_map[dept_name_col] = "DEPARTMENT_NAME"
if school_name_col:
    rename_map[school_name_col] = "SCHOOL_NAME"

final_cols_order = []
# Required: term code
final_cols_order.append("TERM_CODE")
# Optional: term description
if term_desc_col:
    final_cols_order.append("TERM_DESC")
# Attribute description
final_cols_order.append("HGN_CODE_DESC")
# Department and School if available
if dept_name_col:
    final_cols_order.append("DEPARTMENT_NAME")
if school_name_col:
    final_cols_order.append("SCHOOL_NAME")
# Count
final_cols_order.append("unique_subjects")

final = counts.rename(columns=rename_map)
# Ensure all expected columns exist; if missing, add with empty values to satisfy schema
for c in final_cols_order:
    if c not in final.columns:
        if c == "unique_subjects":
            final[c] = 0
        else:
            final[c] = ""

final = final[final_cols_order]

# Assign to result dict as required
result = {"subjects_in_hass_by_term_dept_school": final}