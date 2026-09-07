import pandas as pd

# Input tables are provided in `tables` dict:
# tables['table_1'] -> ACADEMIC_TERM_PARAMETER.pkl
# tables['table_4'] -> CIS_COURSE_CATALOG.pkl

# 1) Load dataframes from provided tables dict
term_param_df = tables['table_1'].copy()
cis_df = tables['table_4'].copy()

# 2) Safety checks for required columns
required_term_col = "term_code"
required_cis_cols = ["EFFECTIVE_TERM_CODE", "SUBJECT_CODE"]

missing = []
if required_term_col not in term_param_df.columns:
    missing.append(f"ACADEMIC_TERM_PARAMETER missing {required_term_col}")
for col in required_cis_cols:
    if col not in cis_df.columns:
        missing.append(f"CIS_COURSE_CATALOG missing {col}")
if missing:
    raise KeyError(" | ".join(missing))

# 3) Prepare valid terms from ACADEMIC_TERM_PARAMETER
valid_terms = (
    term_param_df[required_term_col]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

# 4) Normalize key columns in CIS
cis_filtered = cis_df.copy()
cis_filtered["EFFECTIVE_TERM_CODE"] = cis_filtered["EFFECTIVE_TERM_CODE"].astype(str).str.strip()
cis_filtered["SUBJECT_CODE"] = cis_filtered["SUBJECT_CODE"].astype(str).str.strip()

# 5) Keep CIS rows whose EFFECTIVE_TERM_CODE appears in valid_terms
cis_in_terms = cis_filtered[cis_filtered["EFFECTIVE_TERM_CODE"].isin(valid_terms)]

# 6) Count distinct SUBJECT_CODE per EFFECTIVE_TERM_CODE
summary = (
    cis_in_terms.groupby("EFFECTIVE_TERM_CODE", as_index=False)
    .agg(distinct_subject_code_count=("SUBJECT_CODE", "nunique"))
    .sort_values(["EFFECTIVE_TERM_CODE"])
)

# 7) Attach human-readable term description if available
attach_cols = ["term_code", "TERM_DESCRIPTION"]
attach_cols = [c for c in attach_cols if c in term_param_df.columns]
if len(attach_cols) == 2:
    term_lookup = term_param_df[attach_cols].drop_duplicates()
    summary = summary.merge(
        term_lookup,
        left_on="EFFECTIVE_TERM_CODE",
        right_on="term_code",
        how="left"
    ).drop(columns=["term_code"])

# 8) Determine current term flag if available
# Common columns to infer "current" status: IS_CURRENT_TERM, CURRENT_TERM_IND, or a boolean/flag in ACADEMIC_TERM_PARAMETER
current_flag_col = None
for cand in ["IS_CURRENT_TERM", "CURRENT_TERM_IND", "CURRENT_IND", "IS_CURRENT"]:
    if cand in term_param_df.columns:
        current_flag_col = cand
        break

if current_flag_col is not None:
    term_current_lookup = (
        term_param_df[[required_term_col, current_flag_col]]
        .drop_duplicates()
        .rename(columns={required_term_col: "term_code"})
    )
    # Normalize to boolean where possible
    def to_bool(x):
        if isinstance(x, str):
            xs = x.strip().upper()
            if xs in {"Y", "YES", "TRUE", "T", "1"}:
                return True
            if xs in {"N", "NO", "FALSE", "F", "0"}:
                return False
        if isinstance(x, (int, float)):
            return bool(x)
        return bool(x)
    term_current_lookup["is_current_term"] = term_current_lookup[current_flag_col].map(to_bool)
    term_current_lookup = term_current_lookup[["term_code", "is_current_term"]]

    summary = summary.merge(
        term_current_lookup,
        left_on="EFFECTIVE_TERM_CODE",
        right_on="term_code",
        how="left"
    ).drop(columns=["term_code"])
else:
    # If no explicit flag, attempt to infer current from ACADEMIC_TERM_PARAMETER if it has a single row flagged by max/min or similar
    # Fallback: mark all as None
    summary["is_current_term"] = None

# 9) Final formatting to match the question:
# For each term, list: term code, term description, whether current, and total number of types of CIS courses.
final_cols = []
# Term code
summary = summary.rename(columns={"EFFECTIVE_TERM_CODE": "term_code",
                                  "TERM_DESCRIPTION": "term_description",
                                  "distinct_subject_code_count": "total_cis_course_types"})
final_cols.append("term_code")
# Description if available
if "term_description" in summary.columns:
    final_cols.append("term_description")
else:
    summary["term_description"] = None
    final_cols.append("term_description")
# Current flag
final_cols.append("is_current_term")
# Count
final_cols.append("total_cis_course_types")

final_answer = summary[final_cols].drop_duplicates().sort_values(["term_code"]).reset_index(drop=True)

# 10) Assign to result dict as required
result = {"term_cis_course_types": final_answer}