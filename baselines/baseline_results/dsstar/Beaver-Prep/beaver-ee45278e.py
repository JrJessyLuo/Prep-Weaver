import pandas as pd

# Source tables from provided `tables` dict
iap_subject_detail = tables['table_1'].copy()
subject_iap_schedule = tables['table_2'].copy()
iap_session = tables['table_3'].copy()
iap_category = tables['table_4'].copy()
iap_sponsor = tables['table_5'].copy()

# Standardize key dtypes to string to ensure consistent joins (mirror reference logic)
for df, cols in [
    (iap_subject_detail, ["IAP_SUBJECT_CATEGORY_KEY", "IAP_SUBJECT_SPONSOR_KEY", "IAP_SUBJECT_SESSION_KEY"]),
    (iap_category, ["IAP_SUBJECT_CATEGORY_KEY"]),
    (iap_sponsor, ["IAP_SUBJECT_SPONSOR_KEY"]),
    (iap_session, ["iap_subject_session_key"]),
    (subject_iap_schedule, ["IAP_SUBJECT_SESSION_KEY"]),
]:
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str)

# Join to category (mimic reference)
if "IAP_SUBJECT_CATEGORY_KEY" in iap_subject_detail.columns and "IAP_SUBJECT_CATEGORY_KEY" in iap_category.columns:
    merged = iap_subject_detail.merge(
        iap_category[[c for c in ["IAP_SUBJECT_CATEGORY_KEY", "IAP_CATEGORY_NAME", "IAP_CATEGORY_DESC"] if c in iap_category.columns]],
        on="IAP_SUBJECT_CATEGORY_KEY",
        how="left",
        validate="m:1"
    )
else:
    merged = iap_subject_detail.copy()

# Join to sponsor (mimic reference)
if "IAP_SUBJECT_SPONSOR_KEY" in merged.columns and "IAP_SUBJECT_SPONSOR_KEY" in iap_sponsor.columns:
    merged = merged.merge(
        iap_sponsor[[c for c in ["IAP_SUBJECT_SPONSOR_KEY", "SPONSOR_NAME", "SPONSOR_TYPE"] if c in iap_sponsor.columns]],
        on="IAP_SUBJECT_SPONSOR_KEY",
        how="left",
        validate="m:1"
    )

# Join to session (reference uses right key 'iap_subject_session_key')
session_cols = [c for c in iap_session.columns if c in ["iap_subject_session_key", "SESSION_TITLE", "SESSION_SEQUENCE", "SESSION_DESCRIPTION", "WAREHOUSE_LOAD_DATE"]]
if "IAP_SUBJECT_SESSION_KEY" in merged.columns and "iap_subject_session_key" in iap_session.columns:
    merged = merged.merge(
        iap_session[session_cols],
        left_on="IAP_SUBJECT_SESSION_KEY",
        right_on="iap_subject_session_key",
        how="left",
        validate="m:1"
    )

# Bring in schedule info to get session start/end times
# SUBJECT_IAP_SCHEDULE expected to have IAP_SUBJECT_SESSION_KEY and time fields
sched_cols = [c for c in subject_iap_schedule.columns if c.upper() in {
    "IAP_SUBJECT_SESSION_KEY",
    "SESSION_START_TIME", "SESSION_END_TIME",
    "START_TIME", "END_TIME",
    "SESSION_START_DATE", "SESSION_END_DATE",
    "START_DATE", "END_DATE"
}]
if "IAP_SUBJECT_SESSION_KEY" in merged.columns and "IAP_SUBJECT_SESSION_KEY" in subject_iap_schedule.columns and sched_cols:
    merged = merged.merge(
        subject_iap_schedule[sched_cols],
        on="IAP_SUBJECT_SESSION_KEY",
        how="left",
        validate="m:m"  # schedules can have multiple rows per session
    )

# Determine grouping key as in reference:
subject_id_cols = [c for c in ["SUBJECT_ID", "SOURCE_SUBJECT_ID", "PRINT_SUBJECT_ID"] if c in merged.columns]
if subject_id_cols:
    grp_cols = [subject_id_cols[0]]
else:
    proxy_cols = [c for c in ["TERM_CODE", "ACTIVITY_TITLE"] if c in merged.columns]
    grp_cols = proxy_cols if len(proxy_cols) == 2 else ["IAP_SUBJECT_SESSION_KEY"]

# Session counts (mirror reference preference order)
if "SESSION_SEQUENCE" in merged.columns:
    session_count = (merged
                     .dropna(subset=["SESSION_SEQUENCE"])
                     .groupby(grp_cols)["SESSION_SEQUENCE"]
                     .nunique()
                     .reset_index(name="SESSION_COUNT"))
elif "SESSION_TITLE" in merged.columns:
    session_count = (merged
                     .dropna(subset=["SESSION_TITLE"])
                     .groupby(grp_cols)["SESSION_TITLE"]
                     .nunique()
                     .reset_index(name="SESSION_COUNT"))
else:
    session_count = merged.groupby(grp_cols).size().reset_index(name="SESSION_COUNT")

merged = merged.merge(session_count, on=grp_cols, how="left", validate="m:1")

# Try to provide canonical session start/end column names
# Prefer SESSION_START_TIME/SESSION_END_TIME; fall back to START_TIME/END_TIME if necessary
start_time_col = "SESSION_START_TIME" if "SESSION_START_TIME" in merged.columns else ("START_TIME" if "START_TIME" in merged.columns else None)
end_time_col = "SESSION_END_TIME" if "SESSION_END_TIME" in merged.columns else ("END_TIME" if "END_TIME" in merged.columns else None)

# Build final answer columns
final_cols = []
# Core subject identity and requested fields
for c in (grp_cols + [c for c in [
    "ACTIVITY_TITLE",
    "IAP_CATEGORY_NAME",
    "SESSION_TITLE",
    start_time_col,
    end_time_col,
    "SPONSOR_NAME",
    "SESSION_COUNT"
] if (c is not None)]):
    if c in merged.columns and c not in final_cols:
        final_cols.append(c)

final = merged[final_cols].copy()

# Make column names user-friendly
rename_map = {}
if start_time_col in final.columns:
    rename_map[start_time_col] = "SESSION_START_TIME"
if end_time_col in final.columns:
    rename_map[end_time_col] = "SESSION_END_TIME"
final = final.rename(columns=rename_map)

# Provide a concise, deduplicated view per session row (subject x session), keeping session times
dedupe_keys = [c for c in ["IAP_SUBJECT_SESSION_KEY"] if c in merged.columns]
if dedupe_keys:
    # Keep one row per subject-session-title-time combo
    dedupe_cols = [c for c in ["IAP_SUBJECT_SESSION_KEY", "SESSION_TITLE", "SESSION_START_TIME", "SESSION_END_TIME"] if c in final.columns]
    keep_cols = list(dict.fromkeys(grp_cols + [c for c in ["ACTIVITY_TITLE", "IAP_CATEGORY_NAME", "SPONSOR_NAME", "SESSION_COUNT"] if c in final.columns] + dedupe_cols))
    final = final[keep_cols].drop_duplicates()

# Assemble result mapping as required
result = {
    "iap_subjects_with_sessions": final
}