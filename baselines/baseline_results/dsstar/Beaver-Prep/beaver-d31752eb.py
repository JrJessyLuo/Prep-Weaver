import pandas as pd

# The input DataFrames are provided in scope as a dict named `tables`
# Mapping per guideline:
# tables['table_3'] -> IAP_SUBJECT_SESSION.pkl
# tables['table_7'] -> SUBJECT_OFFERED_SUMMARY.pkl
# tables['table_10'] -> ACADEMIC_TERMS.pkl

# 1) Load dataframes from provided tables dict
iap_sess = tables['table_3'].copy()
subj_offered_sum = tables['table_7'].copy()
acad_terms = tables['table_10'].copy()

# 2) Sanity checks for required columns per current plan
required_iap_cols = {"TERM_CODE"}
required_offered_sum_cols = {"TERM_CODE", "SUBJECT_ID", "CLUSTER_TYPE", "SUBJECT_TITLE"}
required_terms_cols = {"term_code", "TERM_DESCRIPTION", "IS_CURRENT_TERM"}

missing_iap = required_iap_cols - set(iap_sess.columns)
missing_offered_sum = required_offered_sum_cols - set(subj_offered_sum.columns)
missing_terms = required_terms_cols - set(acad_terms.columns)
if missing_iap:
    raise ValueError(f"Missing columns in IAP_SUBJECT_SESSION: {missing_iap}")
if missing_offered_sum:
    raise ValueError(f"Missing columns in SUBJECT_OFFERED_SUMMARY: {missing_offered_sum}")
if missing_terms:
    raise ValueError(f"Missing columns in ACADEMIC_TERMS: {missing_terms}")

# 3) Identify SUBJECT_ID in IAP sessions for the join.
possible_subject_id_cols = [c for c in iap_sess.columns if c.upper() in {"SUBJECT_ID", "IAP_SUBJECT_ID", "MASTER_SUBJECT_ID"}]
iap_has_subject_id = len(possible_subject_id_cols) > 0
iap_subject_id_col = possible_subject_id_cols[0] if iap_has_subject_id else None

# 4) Prepare terms current flag
terms_cur = acad_terms.loc[:, ["term_code", "TERM_DESCRIPTION", "IS_CURRENT_TERM"]].rename(columns={"term_code": "TERM_CODE"})

# 5) If SUBJECT_ID exists in IAP session, do the requested join on (TERM_CODE, SUBJECT_ID)
if iap_has_subject_id:
    # Normalize types to string for safe merging
    iap_sess["_TERM_CODE_"] = iap_sess["TERM_CODE"].astype(str)
    iap_sess["_SUBJECT_ID_"] = iap_sess[iap_subject_id_col].astype(str)

    subj_offered_sum["_TERM_CODE_"] = subj_offered_sum["TERM_CODE"].astype(str)
    subj_offered_sum["_SUBJECT_ID_"] = subj_offered_sum["SUBJECT_ID"].astype(str)

    # Select minimal columns from offered summary
    offered_min = subj_offered_sum.loc[:, [
        "_TERM_CODE_", "_SUBJECT_ID_", "CLUSTER_TYPE", "SUBJECT_TITLE"
    ]].drop_duplicates()

    # Merge
    merged = (
        iap_sess.merge(
            offered_min,
            on=["_TERM_CODE_", "_SUBJECT_ID_"],
            how="left",
            validate="m:1"
        )
        .drop(columns=["_TERM_CODE_", "_SUBJECT_ID_"])
    )
else:
    # Fallback: no SUBJECT_ID in IAP session; attach the most common CLUSTER_TYPE by TERM_CODE.
    offered_min = subj_offered_sum.loc[:, ["TERM_CODE", "CLUSTER_TYPE"]].copy()
    cluster_by_term = (
        offered_min.groupby("TERM_CODE")["CLUSTER_TYPE"]
        .agg(lambda s: s.mode().iat[0] if not s.mode().empty else pd.NA)
        .reset_index()
    )
    merged = iap_sess.merge(cluster_by_term, on="TERM_CODE", how="left")
    # SUBJECT_TITLE cannot be accurately joined without SUBJECT_ID; leave it absent.

# 6) Tag current term info
merged = merged.merge(terms_cur, on="TERM_CODE", how="left")

# 7) Build base fields for reporting
# Session name: prefer SESSION_TITLE if present, else SUBJECT_TITLE if available, else fallback to iap_subject_session_key
session_name_col = None
if "SESSION_TITLE" in merged.columns:
    session_name_col = "SESSION_TITLE"
elif "SUBJECT_TITLE" in merged.columns:
    session_name_col = "SUBJECT_TITLE"
elif "iap_subject_session_key" in merged.columns:
    session_name_col = "iap_subject_session_key"

# Current status label
merged["IS_CURRENT_TERM_BOOL"] = merged["IS_CURRENT_TERM"].astype(str).str.upper().isin(["Y", "YES", "TRUE", "1"])
merged["CURRENT_STATUS"] = merged["IS_CURRENT_TERM_BOOL"].map({True: "CURRENT", False: "NOT CURRENT"})

# Ensure cluster type exists for ordering/grouping even if missing
if "CLUSTER_TYPE" not in merged.columns:
    merged["CLUSTER_TYPE"] = pd.NA

# Session duration in days: use SESSION_TIME_DAYS if present; else infer from start/end timestamps if available
if "SESSION_TIME_DAYS" in merged.columns:
    dur_days = pd.to_numeric(merged["SESSION_TIME_DAYS"], errors="coerce")
else:
    # Try to compute from START/END if exist; otherwise default to NaN
    start_cols = [c for c in merged.columns if c.upper() in {"SESSION_START", "START_TIME", "START_DATETIME"}]
    end_cols = [c for c in merged.columns if c.upper() in {"SESSION_END", "END_TIME", "END_DATETIME"}]
    if start_cols and end_cols:
        s_col, e_col = start_cols[0], end_cols[0]
        s_dt = pd.to_datetime(merged[s_col], errors="coerce")
        e_dt = pd.to_datetime(merged[e_col], errors="coerce")
        dur_days = (e_dt - s_dt).dt.total_seconds() / (24*3600)
    else:
        dur_days = pd.Series(pd.NA, index=merged.index, dtype="float")

merged["_SESSION_DAYS_"] = pd.to_numeric(dur_days, errors="coerce")

# Establish final grouping keys: CURRENT_STATUS and CLUSTER_TYPE
group_keys = ["CURRENT_STATUS", "CLUSTER_TYPE"]

# Aggregate per group and session name
# Count sessions, sum and average durations
name_col = session_name_col if session_name_col is not None else "SESSION_NAME_FALLBACK"
if session_name_col is None:
    merged[name_col] = "SESSION"

agg_detail = (
    merged.groupby(group_keys + [name_col], dropna=False)
    .agg(
        IAP_SESSIONS=("iap_subject_session_key" if "iap_subject_session_key" in merged.columns else name_col, "count"),
        TOTAL_DAYS=("_SESSION_DAYS_", "sum"),
        AVG_DAYS=("_SESSION_DAYS_", "mean"),
    )
    .reset_index()
)

# Order by CURRENT_STATUS and CLUSTER_TYPE as requested
# Define order: CURRENT first then NOT CURRENT
status_cat = pd.CategoricalDtype(categories=["CURRENT", "NOT CURRENT"], ordered=True)
agg_detail["CURRENT_STATUS"] = agg_detail["CURRENT_STATUS"].astype(status_cat)
agg_detail = agg_detail.sort_values(["CURRENT_STATUS", "CLUSTER_TYPE", name_col], kind="mergesort")

# Subtotals per CURRENT_STATUS
subtotals = (
    agg_detail.groupby(["CURRENT_STATUS"], dropna=False)
    .agg(
        IAP_SESSIONS=("IAP_SESSIONS", "sum"),
        TOTAL_DAYS=("TOTAL_DAYS", "sum"),
        AVG_DAYS=("TOTAL_DAYS", lambda s: s.sum() / agg_detail.loc[agg_detail["CURRENT_STATUS"] == s.name, "IAP_SESSIONS"].sum() if agg_detail.loc[agg_detail["CURRENT_STATUS"] == s.name, "IAP_SESSIONS"].sum() else pd.NA),
    )
    .reset_index()
)
subtotals["CLUSTER_TYPE"] = "Subtotal"
subtotals[name_col] = ""
# Ensure column order alignment
subtotals = subtotals[agg_detail.columns]

# Grand total
grand_total_sessions = agg_detail["IAP_SESSIONS"].sum()
grand_total_days = agg_detail["TOTAL_DAYS"].sum()
grand_avg_days = (grand_total_days / grand_total_sessions) if grand_total_sessions else pd.NA
grand = pd.DataFrame([{
    "CURRENT_STATUS": "Grand Total",
    "CLUSTER_TYPE": "",
    name_col: "",
    "IAP_SESSIONS": grand_total_sessions,
    "TOTAL_DAYS": grand_total_days,
    "AVG_DAYS": grand_avg_days
}])

# Combine detail + subtotals per status inserted after each status block
combined_parts = []
for status in ["CURRENT", "NOT CURRENT"]:
    part = agg_detail[agg_detail["CURRENT_STATUS"] == status]
    if not part.empty:
        combined_parts.append(part)
        sub = subtotals[subtotals["CURRENT_STATUS"] == status]
        if not sub.empty:
            combined_parts.append(sub)

final_df = pd.concat(combined_parts + [grand], ignore_index=True)

# Display current status only when it differs from previous entry
final_df["CURRENT_STATUS_DISPLAY"] = final_df["CURRENT_STATUS"]
final_df["CURRENT_STATUS_DISPLAY"] = final_df["CURRENT_STATUS_DISPLAY"].where(
    final_df["CURRENT_STATUS_DISPLAY"].ne(final_df["CURRENT_STATUS_DISPLAY"].shift(1)),
    ""
)

# Friendly column names
final_display = final_df.rename(columns={
    "CURRENT_STATUS_DISPLAY": "CURRENT STATUS",
    name_col: "SESSION NAME",
    "IAP_SESSIONS": "NUMBER OF IAP SESSIONS",
    "TOTAL_DAYS": "TOTAL IAP SESSION TIME (DAYS)",
    "AVG_DAYS": "AVERAGE IAP SESSION TIME (DAYS)"
})[[
    "CURRENT STATUS",
    "CLUSTER_TYPE",
    "SESSION NAME",
    "NUMBER OF IAP SESSIONS",
    "TOTAL IAP SESSION TIME (DAYS)",
    "AVERAGE IAP SESSION TIME (DAYS)"
]]

# Assign final result as required
result = {"sessions_by_current_status": final_display}