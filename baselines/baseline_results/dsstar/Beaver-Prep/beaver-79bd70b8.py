import pandas as pd
import numpy as np

# Source tables from `tables` dict
iap_subject_detail = tables['table_1'].copy()
iap_subject_sponsor = tables['table_2'].copy()

# Merge sponsor name onto detail
merged = iap_subject_detail.merge(
    iap_subject_sponsor[["IAP_SUBJECT_SPONSOR_KEY", "SPONSOR_NAME"]],
    on="IAP_SUBJECT_SPONSOR_KEY",
    how="left",
    validate="m:1"
)

# Helper: coerce fee-like strings to numeric (strip $, commas, whitespace)
def to_numeric_fee(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float, np.number)):
        return pd.to_numeric(x, errors="coerce")
    s = str(x).strip()
    s = s.replace("$", "").replace(",", "").replace("USD", "").strip()
    if "-" in s:
        parts = [p.strip() for p in s.split("-") if p.strip() != ""]
        vals = pd.to_numeric(parts, errors="coerce")
        if len(vals) >= 2 and not np.isnan(vals[0]) and not np.isnan(vals[1]):
            return float(np.nanmean(vals[:2]))
    if "to" in s.lower():
        parts = [p.strip() for p in s.lower().split("to") if p.strip() != ""]
        vals = pd.to_numeric(parts, errors="coerce")
        if len(vals) >= 2 and not np.isnan(vals[0]) and not np.isnan(vals[1]):
            return float(np.nanmean(vals[:2]))
    return pd.to_numeric(s, errors="coerce")

# Normalize FEE
fee_col = "FEE" if "FEE" in merged.columns else None
if fee_col:
    merged["_FEE_NUM"] = merged[fee_col].apply(to_numeric_fee)
else:
    merged["_FEE_NUM"] = np.nan

# Normalize ATTENDANCE / enrollment
att_cols_preference = ["ATTENDANCE", "MAX_ENROLLMENT", "ENROLLMENT", "ENROLLMENT_TYPE"]
att_col = next((c for c in att_cols_preference if c in merged.columns), None)

def to_numeric_att(x):
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float, np.number)):
        return pd.to_numeric(x, errors="coerce")
    s = str(x).strip()
    s = s.replace(",", "")
    tokens = "".join(ch if (ch.isdigit() or ch == "." or ch == " ") else " " for ch in s).split()
    num = pd.to_numeric(tokens[0], errors="coerce") if tokens else np.nan
    return num

if att_col:
    merged["_ATT_NUM"] = merged[att_col].apply(to_numeric_att)
else:
    merged["_ATT_NUM"] = np.nan

# Determine info presence based on ACTIVITY_DESCRIPTION not null/empty (after stripping)
def has_info(x):
    if pd.isna(x):
        return False
    return str(x).strip() != ""

info_col = "ACTIVITY_DESCRIPTION" if "ACTIVITY_DESCRIPTION" in merged.columns else None
merged["_HAS_INFO"] = merged[info_col].apply(has_info) if info_col else False

# Use SPONSOR_NAME; fill missing sponsor with "Unknown Sponsor" for grouping clarity
merged["SPONSOR_NAME"] = merged["SPONSOR_NAME"].fillna("Unknown Sponsor")

# sessions_held: count of distinct IAP_SUBJECT_SESSION_KEY per sponsor
session_key_col = "IAP_SUBJECT_SESSION_KEY" if "IAP_SUBJECT_SESSION_KEY" in merged.columns else None
if session_key_col is None:
    merged["_SESSION_KEY_FALLBACK"] = np.arange(len(merged))
    session_key_col = "_SESSION_KEY_FALLBACK"

# Build aggregates
grouped = merged.groupby("SPONSOR_NAME", dropna=False)

sessions_held = grouped[session_key_col].nunique().rename("sessions_held")
total_enrollment = grouped["_ATT_NUM"].sum(min_count=1).fillna(0).astype(float).rename("total_enrollment")
min_fee = grouped["_FEE_NUM"].min().rename("min_fee")
max_fee = grouped["_FEE_NUM"].max().rename("max_fee")
sessions_with_info = grouped["_HAS_INFO"].sum().astype(int).rename("sessions_with_info")

summary = pd.concat(
    [sessions_held, total_enrollment, min_fee, max_fee, sessions_with_info],
    axis=1
).reset_index()

summary["sessions_without_info"] = summary["sessions_held"] - summary["sessions_with_info"]

# Sort for readability
summary = summary.sort_values(["sessions_held", "SPONSOR_NAME"], ascending=[False, True]).reset_index(drop=True)

# Package final result
result = {
    "iap_sponsor_summary": summary
}