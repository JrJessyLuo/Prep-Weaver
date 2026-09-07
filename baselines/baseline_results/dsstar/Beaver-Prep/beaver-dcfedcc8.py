import pandas as pd
import re

# Source tables from provided mapping
detail = tables['table_1'].copy()
schedule = tables['table_2'].copy()
category = tables['table_3'].copy()
session = tables['table_4'].copy()
sponsor = tables['table_5'].copy()

# Helper: normalize keys
def normalize_key(s):
    if pd.isna(s):
        return pd.NA
    if not isinstance(s, str):
        s = str(s)
    return re.sub(r"\s+", "", s).upper().strip()

def norm_col(df, col, new_col):
    out = df[col].astype("string")
    out = out.map(lambda x: normalize_key(x))
    df[new_col] = out
    return df

# Prepare normalized category keys for robust join (reproduce reference logic)
if "IAP_SUBJECT_CATEGORY_KEY" not in detail.columns:
    raise KeyError("IAP_SUBJECT_CATEGORY_KEY not found in IAP_SUBJECT_DETAIL")
if "IAP_SUBJECT_CATEGORY_KEY" not in category.columns:
    raise KeyError("IAP_SUBJECT_CATEGORY_KEY not found in IAP_SUBJECT_CATEGORY")

detail = norm_col(detail, "IAP_SUBJECT_CATEGORY_KEY", "_cat_key_norm")
category = norm_col(category, "IAP_SUBJECT_CATEGORY_KEY", "_cat_key_norm")

# Exact normalized key join
cat_keep_cols = ["IAP_SUBJECT_CATEGORY_KEY", "IAP_CATEGORY_NAME", "IAP_CATEGORY_DESC", "_cat_key_norm"]
detail_1 = detail.merge(
    category[cat_keep_cols].drop_duplicates("_cat_key_norm"),
    on="_cat_key_norm",
    how="left",
    suffixes=("", "_cat"),
    indicator=True
)
detail_1.rename(columns={
    "IAP_SUBJECT_CATEGORY_KEY_cat": "IAP_SUBJECT_CATEGORY_KEY_from_cat"
}, inplace=True)

# Fallback using category name search in title/description (as per reference)
unmatched_mask = detail_1["_merge"] != "both"
unmatched = detail_1.loc[unmatched_mask].copy()

cat_name_map = category.dropna(subset=["IAP_CATEGORY_NAME"]).copy()
cat_name_map["IAP_CATEGORY_NAME_NORM"] = cat_name_map["IAP_CATEGORY_NAME"].astype("string").str.upper().str.strip()

cat_names_unique = cat_name_map["IAP_CATEGORY_NAME_NORM"].dropna().unique().tolist()
cat_names_unique = sorted(cat_names_unique, key=len, reverse=True)

def find_category_in_text(title, desc):
    text_parts = []
    if isinstance(title, str):
        text_parts.append(title)
    if isinstance(desc, str):
        text_parts.append(desc)
    if not text_parts:
        return pd.NA
    blob = " ".join(text_parts).upper()
    for cname in cat_names_unique:
        if cname and cname in blob:
            return cname
    return pd.NA

if not unmatched.empty:
    unmatched["CATEGORY_NAME_HIT"] = unmatched.apply(
        lambda r: find_category_in_text(r.get("ACTIVITY_TITLE", None), r.get("ACTIVITY_DESCRIPTION", None)),
        axis=1
    )
    fallback = unmatched.dropna(subset=["CATEGORY_NAME_HIT"]).copy()
    if not fallback.empty:
        fallback = fallback.merge(
            cat_name_map[["IAP_CATEGORY_NAME_NORM", "IAP_CATEGORY_NAME", "IAP_SUBJECT_CATEGORY_KEY"]].drop_duplicates("IAP_CATEGORY_NAME_NORM"),
            left_on="CATEGORY_NAME_HIT",
            right_on="IAP_CATEGORY_NAME_NORM",
            how="left"
        )
        fallback_cols = ["_cat_key_norm", "IAP_CATEGORY_NAME", "IAP_SUBJECT_CATEGORY_KEY"]
        fallback_small = fallback[fallback_cols].rename(
            columns={
                "IAP_CATEGORY_NAME": "IAP_CATEGORY_NAME_fallback",
                "IAP_SUBJECT_CATEGORY_KEY": "IAP_SUBJECT_CATEGORY_KEY_fallback"
            }
        )
        unmatched = unmatched.merge(
            fallback_small.drop_duplicates("_cat_key_norm"),
            on="_cat_key_norm",
            how="left"
        )
    matched = detail_1.loc[~unmatched_mask].copy()
    combined = pd.concat([matched, unmatched], ignore_index=True, sort=False)
    combined["category_key_final"] = combined["IAP_SUBJECT_CATEGORY_KEY_from_cat"].combine_first(combined["IAP_SUBJECT_CATEGORY_KEY_fallback"])
    combined["category_name_final"] = combined["IAP_CATEGORY_NAME"].combine_first(combined["IAP_CATEGORY_NAME_fallback"])
else:
    combined = detail_1.copy()
    combined["category_key_final"] = combined["IAP_SUBJECT_CATEGORY_KEY_from_cat"]
    combined["category_name_final"] = combined["IAP_CATEGORY_NAME"]

# Prepare intermediate with fields needed for downstream aggregations
combined.rename(columns={"category_key_final": "category_key",
                         "category_name_final": "category_name"}, inplace=True)

# Ensure presence of keys/fields referenced downstream
if "IAP_SUBJECT_SESSION_KEY" not in combined.columns:
    combined["IAP_SUBJECT_SESSION_KEY"] = pd.NA
if "TERM_CODE" not in combined.columns:
    combined["TERM_CODE"] = pd.NA
if "ATTENDANCE" not in combined.columns:
    combined["ATTENDANCE"] = pd.NA
if "IAP_SUBJECT_SPONSOR_KEY" not in combined.columns:
    combined["IAP_SUBJECT_SPONSOR_KEY"] = pd.NA

intermediate = combined[[
    "category_key", "category_name",
    "IAP_SUBJECT_SESSION_KEY",
    "TERM_CODE",
    "ATTENDANCE",
    "IAP_SUBJECT_SPONSOR_KEY"
]].copy()

# Map sponsor name (most common sponsor name required)
# Join sponsor table on sponsor key
if "IAP_SUBJECT_SPONSOR_KEY" in sponsor.columns:
    sponsor_small = sponsor[["IAP_SUBJECT_SPONSOR_KEY", "SPONSOR_NAME"]].copy()
    intermediate = intermediate.merge(
        sponsor_small.drop_duplicates("IAP_SUBJECT_SPONSOR_KEY"),
        on="IAP_SUBJECT_SPONSOR_KEY",
        how="left"
    )
else:
    intermediate["SPONSOR_NAME"] = pd.NA

# Map session start time (most common session start time required)
# Expect schedule has session key and start time fields
sess_key_col = "IAP_SUBJECT_SESSION_KEY"
sched_keep = schedule.copy()
if sess_key_col not in sched_keep.columns:
    # create for safe join
    sched_keep[sess_key_col] = pd.NA

# Identify a start time column heuristically
start_cols = [c for c in sched_keep.columns if re.search(r"START", c, re.IGNORECASE)]
start_time_col = start_cols[0] if start_cols else None
if start_time_col is None:
    # no start column; create null
    sched_keep["SESSION_START_TIME"] = pd.NA
    start_time_col = "SESSION_START_TIME"

sched_map = sched_keep[[sess_key_col, start_time_col]].copy().rename(columns={start_time_col: "SESSION_START_TIME"})
intermediate = intermediate.merge(
    sched_map, on="IAP_SUBJECT_SESSION_KEY", how="left"
)

# Attendance: convert to numeric if possible, else treat non-numeric as NaN
def to_numeric_safe(x):
    try:
        return pd.to_numeric(x)
    except Exception:
        return pd.NA

intermediate["ATTENDANCE_NUM"] = pd.to_numeric(intermediate["ATTENDANCE"], errors="coerce")

# Active period per category: beginning term - end term
# Compute min and max TERM_CODE per category
term_minmax = (
    intermediate.groupby(["category_key", "category_name"], dropna=False)["TERM_CODE"]
    .agg(begin_term=lambda s: s.dropna().min() if s.notna().any() else pd.NA,
         end_term=lambda s: s.dropna().max() if s.notna().any() else pd.NA)
    .reset_index()
)
term_minmax["active_period"] = term_minmax.apply(
    lambda r: (str(r["begin_term"]) + "-" + str(r["end_term"])) if pd.notna(r["begin_term"]) and pd.notna(r["end_term"]) else pd.NA,
    axis=1
)

# Number of unique sessions per category
sessions_per_cat = (
    intermediate.groupby(["category_key", "category_name"], dropna=False)["IAP_SUBJECT_SESSION_KEY"]
    .nunique(dropna=True)
    .reset_index(name="num_sessions")
)

# Total attendees per category (sum over rows; if multiple rows per session exist, we assume attendance is recorded per row and summable)
attendees_per_cat = (
    intermediate.groupby(["category_key", "category_name"], dropna=False)["ATTENDANCE_NUM"]
    .sum(min_count=1)
    .reset_index(name="total_attendees")
)

# Most common sponsor name per category
def mode_or_na(s):
    s2 = s.dropna()
    if s2.empty:
        return pd.NA
    counts = s2.value_counts(dropna=True)
    return counts.idxmax()

sponsor_mode = (
    intermediate.groupby(["category_key", "category_name"], dropna=False)["SPONSOR_NAME"]
    .agg(most_common_sponsor=lambda s: mode_or_na(s))
    .reset_index()
)

# Most common session start time per category
start_mode = (
    intermediate.groupby(["category_key", "category_name"], dropna=False)["SESSION_START_TIME"]
    .agg(most_common_start_time=lambda s: mode_or_na(s))
    .reset_index()
)

# Assemble category-level result
cat_result = (
    sessions_per_cat
    .merge(attendees_per_cat, on=["category_key", "category_name"], how="left")
    .merge(term_minmax[["category_key", "category_name", "active_period"]], on=["category_key", "category_name"], how="left")
    .merge(sponsor_mode, on=["category_key", "category_name"], how="left")
    .merge(start_mode, on=["category_key", "category_name"], how="left")
)

# Select and order columns as specified: name, number of unique sessions, total attendees, active period, most common sponsor name, most common session start time
# The question asks "For each IAP category, list its name, number of unique sessions, total number of attendees, active period (begin-end), the most common sponsor name, and the most common session start time."
final_cols = [
    "category_name",
    "num_sessions",
    "total_attendees",
    "active_period",
    "most_common_sponsor",
    "most_common_start_time"
]
cat_result_final = cat_result[final_cols].copy()

# Grand total row: ('TOTAL', number of sessions, number of attendees, null, null, null)
total_sessions = intermediate["IAP_SUBJECT_SESSION_KEY"].nunique(dropna=True)
total_attendees = intermediate["ATTENDANCE_NUM"].sum(min_count=1)

grand_total = pd.DataFrame([{
    "category_name": "TOTAL",
    "num_sessions": int(total_sessions) if pd.notna(total_sessions) else 0,
    "total_attendees": float(total_attendees) if pd.notna(total_attendees) else pd.NA,
    "active_period": pd.NA,
    "most_common_sponsor": pd.NA,
    "most_common_start_time": pd.NA
}])

# Append grand total row
answer_df = pd.concat([cat_result_final, grand_total], ignore_index=True)

# Assign to result mapping
result = {
    "iap_category_summary": answer_df
}