import pandas as pd
import numpy as np

# Source input DataFrames from provided `tables` dict
df_session = tables['table_1'].copy()
df_detail = tables['table_3'].copy()

# Normalize column names helper
def standardize_cols(df):
    lower_to_orig = {c.lower(): c for c in df.columns}
    return df, lower_to_orig

df_session, sess_map = standardize_cols(df_session)
df_detail, det_map = standardize_cols(df_detail)

# Determine join keys (case-insensitive, matching reference logic)
join_key_session = None
join_key_detail = None
for k in ["iap_subject_session_key", "IAP_SUBJECT_SESSION_KEY"]:
    if k in df_session.columns:
        join_key_session = k
        break
    if k.lower() in sess_map:
        join_key_session = sess_map[k.lower()]
        break

for k in ["iap_subject_session_key", "IAP_SUBJECT_SESSION_KEY"]:
    if k in df_detail.columns:
        join_key_detail = k
        break
    if k.lower() in det_map:
        join_key_detail = det_map[k.lower()]
        break

# Identify session fields as in reference
def find_cols(df, keywords, prefer=None):
    cols = [c for c in df.columns if any(k in c.lower() for k in keywords)]
    if prefer:
        pref = [c for c in cols if c.lower() in [p.lower() for p in prefer]]
        rest = [c for c in cols if c not in pref]
        cols = pref + rest
    return cols

location_cols = find_cols(df_session, ["place", "location", "room", "building", "meet_place", "meet loc"], prefer=["session_location", "meet_place"])
start_cols = find_cols(df_session, ["start_time", "begin", "from", "meet_start"], prefer=["meet_start_time", "start_time"])
end_cols = find_cols(df_session, ["end_time", "finish", "to", "meet_end"], prefer=["meet_end_time", "end_time"])
title_cols = find_cols(df_session, ["title"], prefer=["session_title"])

session_location_col = location_cols[0] if location_cols else None
session_start_col = start_cols[0] if start_cols else None
session_end_col = end_cols[0] if end_cols else None
session_title_col = title_cols[0] if title_cols else None

# Detail fields: fee and a subject identifier (if any)
detail_fee_col = None
for c in df_detail.columns:
    if c.lower() == "fee":
        detail_fee_col = c
        break

detail_subject_cols = [c for c in df_detail.columns if "subject" in c.lower() and "key" not in c.lower() and "session" not in c.lower()]
detail_keep_cols = list({join_key_detail, detail_fee_col} - {None})
if detail_subject_cols:
    preferred = [c for c in detail_subject_cols if c.lower() == "subject_id"]
    if preferred:
        detail_keep_cols.append(preferred[0])
    else:
        detail_keep_cols.append(detail_subject_cols[0])

# Perform left join session with detail
df_joined = df_session.merge(
    df_detail[detail_keep_cols],
    how="left",
    left_on=join_key_session,
    right_on=join_key_detail,
    suffixes=("", "_detail")
)

# Filter to physical locations per reference logic
exclude_keywords = ["zoom", "online", "virtual", "remote", "web", "webinar"]
if session_location_col is None:
    df_joined["_SESSION_LOCATION"] = np.nan
    session_location_col = "_SESSION_LOCATION"

loc_series = df_joined[session_location_col].astype(str).str.strip()
mask_notnull = df_joined[session_location_col].notna() & (loc_series != "") & (loc_series.str.lower() != "nan")
mask_exclude = loc_series.str.lower().str.contains("|".join(exclude_keywords), na=False)
mask_physical = mask_notnull & (~mask_exclude)
df_physical = df_joined.loc[mask_physical].copy()

# Parse session durations (in minutes) using SESSION_DATE + start/end times if present
# Fallback to time-only parsing if date missing; if either time missing, duration = NaN
def parse_time(t):
    if pd.isna(t):
        return None
    s = str(t).strip()
    if s == "" or s.lower() == "nan":
        return None
    return s

date_col_candidates = [c for c in df_session.columns if c.lower() in ["session_date", "date"] or "date" in c.lower()]
session_date_col = date_col_candidates[0] if date_col_candidates else None

def to_datetime(date_str, time_str):
    if time_str is None:
        return None
    # Try formats like 0100PM or 01:00 PM
    t = time_str
    # Insert colon if like 0100PM
    if len(t) in (6,7) and t[-2:].upper() in ("AM","PM") and ":" not in t:
        core = t[:-2]
        ampm = t[-2:]
        if len(core) == 3:
            core = "0" + core
        t = core[:2] + ":" + core[2:] + " " + ampm
    elif "AM" in t.upper() or "PM" in t.upper():
        # Ensure space before AM/PM
        t = t.upper().replace("AM"," AM").replace("PM"," PM")
        t = " ".join(t.split())
    # Compose datetime string
    if date_str is not None:
        ds = str(date_str).strip()
        if ds != "" and ds.lower() != "nan":
            # Try multiple date formats
            for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"]:
                try:
                    dt = pd.to_datetime(ds + " " + t, format=fmt + " %I:%M %p", errors="raise")
                    return dt
                except Exception:
                    continue
    # Fallback: parse time only today (arbitrary date), sufficient for duration diffs within same day
    try:
        dt = pd.to_datetime(t, format="%I:%M %p", errors="raise")
        return dt
    except Exception:
        try:
            # Last resort generic
            return pd.to_datetime(t, errors="coerce")
        except Exception:
            return None

start_parsed = []
end_parsed = []
for _, row in df_physical.iterrows():
    ds = row[session_date_col] if session_date_col in df_physical.columns else None
    st = parse_time(row[session_start_col]) if session_start_col in df_physical.columns else None
    et = parse_time(row[session_end_col]) if session_end_col in df_physical.columns else None
    dt_s = to_datetime(ds, st) if st is not None else None
    dt_e = to_datetime(ds, et) if et is not None else None
    start_parsed.append(dt_s)
    end_parsed.append(dt_e)

df_physical["_start_dt"] = pd.to_datetime(start_parsed)
df_physical["_end_dt"] = pd.to_datetime(end_parsed)

# Compute duration in minutes, guard negatives or cross-midnight by taking absolute diff if both present
dur = (df_physical["_end_dt"] - df_physical["_start_dt"]).dt.total_seconds() / 60.0
df_physical["_duration_min"] = dur

# Aggregate per physical location:
# - building name (use SESSION_LOCATION as-is)
# - total number of subjects: count distinct session keys present in detail per location
#   Since join is session->detail, count distinct IAP_SUBJECT_SESSION_KEY from detail rows per location.
# - total fee: sum of FEE over joined rows (NaN treated as 0)
# - shortest and longest sessions: min/max duration in minutes (ignoring NaN)
group_cols = [session_location_col]

# Prepare subject/session counts: if there is at least one detail row per session, count unique session keys observed in detail
session_key_in_detail = join_key_detail if join_key_detail in df_physical.columns else None

agg_dict = {}

# total number of subjects: use number of detail rows per location if subject granularity is per-detail row.
# Safer: count unique session keys from detail where available, else count unique session keys overall.
if session_key_in_detail is not None:
    subj_count_series = df_physical.groupby(group_cols)[session_key_in_detail].nunique()
else:
    subj_count_series = df_physical.groupby(group_cols)[join_key_session].nunique()

# total fee
fee_col = detail_fee_col if detail_fee_col in df_physical.columns else None
if fee_col is not None:
    fee_sum_series = df_physical.groupby(group_cols)[fee_col].sum(min_count=1)
else:
    fee_sum_series = df_physical.groupby(group_cols)[join_key_session].size().astype(float)
    fee_sum_series[:] = np.nan  # no fee data

# durations
duration_min = df_physical.groupby(group_cols)["_duration_min"].min()
duration_max = df_physical.groupby(group_cols)["_duration_min"].max()

# Build final DataFrame
out = pd.DataFrame({
    "building_name": [idx for idx in subj_count_series.index],
    "total_subjects": subj_count_series.values,
})

out = out.set_index("building_name").sort_index()

# Align and add fee and durations
out["total_fee"] = fee_sum_series.reindex(out.index)
out["shortest_session_min"] = duration_min.reindex(out.index)
out["longest_session_min"] = duration_max.reindex(out.index)

# Reset index and finalize columns
out = out.reset_index()

# Assign final result
result = {"iap_physical_location_summary": out}