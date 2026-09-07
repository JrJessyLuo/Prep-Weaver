import pandas as pd
import numpy as np

# Source tables
sessions = tables["table_3"].copy()
iap_subjects = tables["table_2"].copy()
terms = tables["table_10"].copy()

# Standardize keys
sessions["iap_subject_session_key_std"] = sessions["iap_subject_session_key"].astype(str).str.strip().str.upper()
iap_subjects["iap_subject_session_key_std"] = iap_subjects["IAP_SUBJECT_SESSION_KEY"].astype(str).str.strip().str.upper()
iap_subjects["TERM_CODE_STD"] = iap_subjects["TERM_CODE"].astype(str).str.strip().str.upper()

# Deduplicate IAP subject metadata to avoid category/sponsor duplication
iap_subject_meta = (
    iap_subjects.sort_values(["iap_subject_session_key_std", "ACTIVITY_TITLE"])
    .drop_duplicates("iap_subject_session_key_std")
    [["iap_subject_session_key_std", "TERM_CODE_STD", "ACTIVITY_TITLE"]]
)

# Join session detail to IAP subject metadata
df = sessions.merge(iap_subject_meta, on="iap_subject_session_key_std", how="left")

# Build session name: prefer SESSION_TITLE, fall back to ACTIVITY_TITLE, then key
df["session_name"] = (
    df["SESSION_TITLE"]
    .where(df["SESSION_TITLE"].notna() & (df["SESSION_TITLE"].astype(str).str.strip() != ""), df["ACTIVITY_TITLE"])
    .fillna(df["iap_subject_session_key_std"])
    .astype(str)
    .str.strip()
)

# Parse session start/end datetimes and compute elapsed time in days
def _clean_time(s):
    s = s.astype("string").str.strip().str.upper()
    s = s.str.replace(r"\s+", "", regex=True)
    s = s.str.replace("NOON", "1200PM", regex=False)
    s = s.str.replace("MIDNIGHT", "1200AM", regex=False)
    return s

date_part = df["SESSION_DATE"].astype("string").str.strip().str.upper()
start_part = _clean_time(df["SESSION_START_TIME"])
end_part = _clean_time(df["SESSION_END_TIME"])

start_dt = pd.to_datetime(date_part + " " + start_part, format="%d-%b-%y %I%M%p", errors="coerce")
end_dt = pd.to_datetime(date_part + " " + end_part, format="%d-%b-%y %I%M%p", errors="coerce")

# If an end time falls before a start time, treat it as ending after midnight
end_dt = end_dt.where((end_dt.isna()) | (start_dt.isna()) | (end_dt >= start_dt), end_dt + pd.Timedelta(days=1))

df["iap_session_time_days"] = (end_dt - start_dt).dt.total_seconds() / 86400

# Current-term status
terms["TERM_CODE_STD"] = terms["term_code"].astype(str).str.strip().str.upper()
term_status = terms[["TERM_CODE_STD", "IS_CURRENT_TERM"]].drop_duplicates("TERM_CODE_STD")

df = df.merge(term_status, on="TERM_CODE_STD", how="left")
df["current_status"] = np.where(df["IS_CURRENT_TERM"].astype(str).str.strip().str.upper().eq("Y"), "CURRENT", "NOT CURRENT")

# Attach cluster type where an IAP activity title can be matched to an offered-subject title
df["title_norm"] = df["ACTIVITY_TITLE"].astype("string").str.strip().str.lower().str.replace(r"\s+", " ", regex=True)

cluster_type_col = None
if "table_8" in tables and {"TERM_CODE", "SUBJECT_TITLE", "CLUSTER_TYPE"}.issubset(tables["table_8"].columns):
    offered = tables["table_8"][["TERM_CODE", "SUBJECT_TITLE", "CLUSTER_TYPE"]].copy()
    cluster_type_col = "CLUSTER_TYPE"
elif "table_7" in tables and {"TERM_CODE", "SUBJECT_TITLE", "CLUSTER_TYPE"}.issubset(tables["table_7"].columns):
    offered = tables["table_7"][["TERM_CODE", "SUBJECT_TITLE", "CLUSTER_TYPE"]].copy()
    cluster_type_col = "CLUSTER_TYPE"
else:
    offered = pd.DataFrame(columns=["TERM_CODE", "SUBJECT_TITLE", "CLUSTER_TYPE"])

if not offered.empty:
    offered["TERM_CODE_STD"] = offered["TERM_CODE"].astype(str).str.strip().str.upper()
    offered["title_norm"] = offered["SUBJECT_TITLE"].astype("string").str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    offered["cluster_type"] = offered["CLUSTER_TYPE"].astype("string").str.strip()
    offered = (
        offered.dropna(subset=["TERM_CODE_STD", "title_norm"])
        .sort_values(["TERM_CODE_STD", "title_norm", "cluster_type"])
        .drop_duplicates(["TERM_CODE_STD", "title_norm"])
        [["TERM_CODE_STD", "title_norm", "cluster_type"]]
    )
    df = df.merge(offered, on=["TERM_CODE_STD", "title_norm"], how="left")
else:
    df["cluster_type"] = pd.NA

df["cluster_type"] = df["cluster_type"].fillna("UNKNOWN").astype(str).str.strip()

# Helper aggregation
def summarize(data, group_cols):
    return (
        data.groupby(group_cols, dropna=False, as_index=False)
        .agg(
            number_of_iap_sessions=("iap_subject_session_key_std", "size"),
            total_iap_session_time_days=("iap_session_time_days", lambda x: x.sum(min_count=1)),
            average_iap_session_time_days=("iap_session_time_days", "mean"),
        )
    )

# Detail rows
detail = summarize(df, ["current_status", "cluster_type", "session_name"])
detail["row_type"] = "DETAIL"

# Subtotals by current status
subtotals = summarize(df, ["current_status"])
subtotals["cluster_type"] = ""
subtotals["session_name"] = "Subtotal"
subtotals["row_type"] = "SUBTOTAL"

# Grand total
grand_total = pd.DataFrame(
    {
        "current_status": ["GRAND TOTAL"],
        "cluster_type": [""],
        "session_name": ["Grand Total"],
        "number_of_iap_sessions": [len(df)],
        "total_iap_session_time_days": [df["iap_session_time_days"].sum(min_count=1)],
        "average_iap_session_time_days": [df["iap_session_time_days"].mean()],
        "row_type": ["GRAND TOTAL"],
    }
)

# Combine and order
status_order = {"CURRENT": 0, "NOT CURRENT": 1, "GRAND TOTAL": 2}
row_order = {"DETAIL": 0, "SUBTOTAL": 1, "GRAND TOTAL": 2}

out = pd.concat([detail, subtotals, grand_total], ignore_index=True)
out["status_sort"] = out["current_status"].map(status_order).fillna(9)
out["row_sort"] = out["row_type"].map(row_order).fillna(9)

out = out.sort_values(
    ["status_sort", "row_sort", "cluster_type", "session_name"],
    kind="mergesort",
).reset_index(drop=True)

# Display current status only when it differs from previous displayed entry
out["display_current_status"] = out["current_status"].where(out["current_status"].ne(out["current_status"].shift()), "")

# Final report columns
final = out[
    [
        "display_current_status",
        "cluster_type",
        "session_name",
        "number_of_iap_sessions",
        "total_iap_session_time_days",
        "average_iap_session_time_days",
    ]
].rename(
    columns={
        "display_current_status": "current_status",
        "cluster_type": "cluster_type",
        "session_name": "session_name",
        "number_of_iap_sessions": "number_of_iap_sessions",
        "total_iap_session_time_days": "total_iap_session_time_days",
        "average_iap_session_time_days": "average_iap_session_time_days",
    }
)

result = {"iap_sessions_by_current_status": final}
