import pandas as pd

# 0) Source input tables from `tables` dict (already provided in scope)
df_offered = tables['table_7'].copy()
df_drupal = tables['table_5'].copy()
df_cis = tables['table_2'].copy()

# 1) Helper: heuristic identification (same as reference)
def infer_cols(df):
    cols = df.columns
    title = [c for c in cols if any(k in c.upper() for k in ["TITLE", "SUBJECT_TITLE", "COURSE_TITLE", "DESCR", "DESCRIPTION"]) and "LONG" not in c.upper()]
    start = [c for c in cols if any(k in c.upper() for k in ["START", "BEGIN", "FROM"]) and "DATE" in c.upper()]
    end = [c for c in cols if any(k in c.upper() for k in ["END", "THRU", "TO"]) and "DATE" in c.upper()]
    acad_year = [c for c in cols if "ACADEMIC_YEAR" in c.upper() or c.upper() == "YEAR"]
    location = [c for c in cols if any(k in c.upper() for k in ["LOCATION", "ROOM", "PLACE", "BUILD", "MEET_PLACE", "MEETING_PLACE", "BUILDING"])]
    term = [c for c in cols if "TERM_CODE" in c.upper() or c.upper() in ["TERM", "TERMID", "TERM_ID", "TERM CODE"]]
    subject_id = [c for c in cols if c.upper() in ["SUBJECT_ID", "SUBJECTID", "SOURCE_SUBJECT_ID", "PRINT_SUBJECT_ID", "COURSE_ID"]]
    section_id = [c for c in cols if any(k in c.upper() for k in ["SECTION", "CLASS_SECTION", "SECTION_ID"])]
    return {
        "title": title,
        "start": start,
        "end": end,
        "acad_year": acad_year,
        "location": location,
        "term": term,
        "subject_id": subject_id,
        "section_id": section_id,
    }

offered_infer = infer_cols(df_offered)
drupal_infer = infer_cols(df_drupal)
cis_infer = infer_cols(df_cis)

# 2) Standardize keys (same as reference)
def standardize_keys(df, mapping):
    for std, cands in mapping.items():
        for c in cands:
            if c in df.columns and std not in df.columns:
                df = df.rename(columns={c: std})
                break
    return df

offered_key_map = {
    "SUBJECT_ID": ["SUBJECT_ID", "SOURCE_SUBJECT_ID", "PRINT_SUBJECT_ID", "SUBJECTID"],
    "TERM_CODE": ["TERM_CODE", "TERM", "TERMID", "TERM_ID"],
}
df_offered_std = standardize_keys(df_offered.copy(), offered_key_map)

drupal_key_map = {
    "SUBJECT_ID": ["SUBJECT_ID", "SOURCE_SUBJECT_ID", "PRINT_SUBJECT_ID", "SUBJECTID"],
    "TERM_CODE": ["TERM_CODE", "TERM", "TERMID", "TERM_ID", "EFFECTIVE_TERM_CODE"],
}
df_drupal_std = standardize_keys(df_drupal.copy(), drupal_key_map)

cis_key_map = {
    "SUBJECT_ID": ["subject_id", "SOURCE_SUBJECT_ID", "PRINT_SUBJECT_ID", "SUBJECT_ID"],
    "TERM_CODE": ["EFFECTIVE_TERM_CODE", "TERM_CODE", "TERM"],
}
df_cis_std = standardize_keys(df_cis.copy(), cis_key_map)

# 3) Choose candidate columns (same approach as reference)
def pick_first(cols, prefer=None):
    if prefer:
        for p in prefer:
            if p in cols:
                return p
    return cols[0] if cols else None

# Determine offered-side equivalents
offered_start = None  # reference scan showed none
offered_end = None
offered_loc = pick_first(offered_infer["location"], prefer=["MEET_PLACE", "MEETING_PLACE", "LOCATION", "ROOM", "BUILDING"])
offered_title = pick_first(offered_infer["title"], prefer=["COURSE_TITLE", "SUBJECT_TITLE", "TITLE", "DESCRIPTION"])

# Determine DRUPAL/CIS equivalents (as in reference execution)
drupal_date_start_cols = [c for c in df_drupal_std.columns if ("START" in c.upper() or "BEGIN" in c.upper() or "FROM" in c.upper()) and "DATE" in c.upper()]
drupal_date_end_cols = [c for c in df_drupal_std.columns if ("END" in c.upper() or "THRU" in c.upper() or "TO" in c.upper()) and "DATE" in c.upper()]
drupal_location_cols = [c for c in df_drupal_std.columns if any(k in c.upper() for k in ["LOCATION", "ROOM", "PLACE", "BUILD", "MEET_PLACE", "MEETING_PLACE", "BUILDING"])]
drupal_title_cols = [c for c in df_drupal_std.columns if any(k in c.upper() for k in ["TITLE", "SUBJECT_TITLE", "COURSE_TITLE", "DESCR"]) and "LONG" not in c.upper()]

cis_date_start_cols = [c for c in df_cis_std.columns if ("START" in c.upper() or "BEGIN" in c.upper() or "FROM" in c.upper()) and "DATE" in c.upper()]
cis_date_end_cols = [c for c in df_cis_std.columns if ("END" in c.upper() or "THRU" in c.upper() or "TO" in c.upper()) and "DATE" in c.upper()]
cis_location_cols = [c for c in df_cis_std.columns if any(k in c.upper() for k in ["LOCATION", "ROOM", "PLACE", "BUILD", "MEET_PLACE", "MEETING_PLACE", "BUILDING"])]
cis_title_cols = [c for c in df_cis_std.columns if any(k in c.upper() for k in ["TITLE", "SUBJECT_TITLE", "COURSE_TITLE", "DESCR"]) and "LONG" not in c.upper()]

drupal_start = pick_first(drupal_date_start_cols, prefer=["START_DATE", "COURSE_START_DATE"])
drupal_end = pick_first(drupal_date_end_cols, prefer=["END_DATE", "COURSE_END_DATE"])
drupal_loc = pick_first(drupal_location_cols, prefer=["MEET_PLACE", "MEETING_PLACE", "LOCATION", "ROOM", "BUILDING"])
drupal_title = pick_first(drupal_title_cols, prefer=["COURSE_TITLE", "SUBJECT_TITLE", "TITLE", "DESCRIPTION"])

cis_start = pick_first(cis_date_start_cols, prefer=["START_DATE", "COURSE_START_DATE", "FROM_DATE"])
cis_end = pick_first(cis_date_end_cols, prefer=["END_DATE", "COURSE_END_DATE", "THRU_DATE"])
cis_loc = pick_first(cis_location_cols, prefer=["MEET_PLACE", "MEETING_PLACE", "LOCATION", "ROOM", "BUILDING"])
cis_title = pick_first(cis_title_cols, prefer=["COURSE_TITLE", "SUBJECT_TITLE", "TITLE", "DESCRIPTION"])

# 4) Reduce frames for join (same as reference)
def reduce_for_join(df, keep_cols, key_cols=("SUBJECT_ID", "TERM_CODE")):
    keep_cols = [c for c in keep_cols if c in df.columns]
    red = df[keep_cols].copy()
    if all(k in red.columns for k in key_cols):
        red = red.sort_values(by=list(keep_cols)).drop_duplicates(subset=list(key_cols), keep="last")
    else:
        red = red.drop_duplicates()
    return red

drupal_keep = ["SUBJECT_ID", "TERM_CODE"] + [c for c in [drupal_start, drupal_end, drupal_loc, drupal_title] if c]
cis_keep = ["SUBJECT_ID", "TERM_CODE"] + [c for c in [cis_start, cis_end, cis_loc, cis_title] if c]

df_drupal_red = reduce_for_join(df_drupal_std, drupal_keep)
df_cis_red = reduce_for_join(df_cis_std, cis_keep)

# 5) Merge OFFERED <- DRUPAL <- CIS (same logic and priority)
merge_keys = [k for k in ["SUBJECT_ID", "TERM_CODE"] if k in df_offered_std.columns]
if not merge_keys:
    alt_subject_cols = [c for c in ["SOURCE_SUBJECT_ID", "PRINT_SUBJECT_ID", "SUBJECT_ID"] if c in df_offered.columns]
    if alt_subject_cols:
        df_offered_std["SUBJECT_ID"] = df_offered_std[alt_subject_cols[0]]
        merge_keys = [k for k in ["SUBJECT_ID", "TERM_CODE"] if k in df_offered_std.columns]

merged = df_offered_std.copy()
if merge_keys:
    merged = merged.merge(df_drupal_red, on=merge_keys, how="left", suffixes=("", "_DRUPAL"))
    merged = merged.merge(df_cis_red, on=merge_keys, how="left", suffixes=("", "_CIS"))

# 6) Coalesce unified fields (priority: OFFERED -> DRUPAL -> CIS)
def coalesce_cols(df, targets, new_name):
    cols = [c for c in targets if c and c in df.columns]
    if not cols:
        return pd.Series([pd.NA] * len(df), index=df.index, name=new_name)
    s = df[cols[0]]
    for c in cols[1:]:
        s = s.fillna(df[c])
    s.name = new_name
    return s

merged["COURSE_START_DATE"] = coalesce_cols(merged, [offered_start, drupal_start, cis_start], "COURSE_START_DATE")
merged["COURSE_END_DATE"] = coalesce_cols(merged, [offered_end, drupal_end, cis_end], "COURSE_END_DATE")
merged["COURSE_LOCATION"] = coalesce_cols(merged, [offered_loc, drupal_loc, cis_loc], "COURSE_LOCATION")
merged["COURSE_TITLE_UNIFIED"] = coalesce_cols(merged, [offered_title, drupal_title, cis_title], "COURSE_TITLE_UNIFIED")

# 7) Parse building from COURSE_LOCATION (building assumed to be prefix before '-' in MIT-style room like '26-247D')
def extract_building(place):
    if pd.isna(place):
        return pd.NA
    s = str(place).strip()
    if not s:
        return pd.NA
    # If contains '-', take the part before '-'; else take first token (up to whitespace)
    if '-' in s:
        return s.split('-')[0].strip()
    return s.split()[0].strip()

merged["BUILDING_NAME"] = merged["COURSE_LOCATION"].apply(extract_building)

# 8) Compute duration in days (inclusive) if dates available
def to_dt(s):
    return pd.to_datetime(s, errors="coerce")

start_dt = to_dt(merged["COURSE_START_DATE"])
end_dt = to_dt(merged["COURSE_END_DATE"])

# Inclusive days if both present; else NaN
duration_days = (end_dt - start_dt).dt.days.add(1)
duration_days = duration_days.where(~(start_dt.isna() | end_dt.isna()))

merged["DURATION_DAYS"] = duration_days

# 9) Running average over window 2 preceding and 2 following, partitioned by ACADEMIC_YEAR and ordered by COURSE_START_DATE
# If start date missing, use a fallback for ordering: keep NaT; pandas rolling on sorted values with NaT still positions rows; we'll sort with NaT at end.
merged["_order_dt"] = start_dt
merged = merged.sort_values(by=["ACADEMIC_YEAR", "_order_dt"])

# Group by ACADEMIC_YEAR and apply fixed window with center=True to include preceding and following
def rolling_mean_fixed(g):
    # Create a simple rolling mean over window=5 centered on the row
    return g.rolling(window=5, min_periods=1, center=True).mean()

merged["RUNNING_AVG_DURATION_DAYS"] = merged.groupby("ACADEMIC_YEAR", dropna=False)["DURATION_DAYS"].apply(rolling_mean_fixed).reset_index(level=0, drop=True)

# 10) Assemble final answer: title, building name, duration, running average, plus sort for readability
final_cols = ["ACADEMIC_YEAR", "COURSE_TITLE_UNIFIED", "BUILDING_NAME", "DURATION_DAYS", "RUNNING_AVG_DURATION_DAYS", "COURSE_START_DATE", "COURSE_END_DATE"]
answer = merged[final_cols].copy()

# Optional: sort by academic year then start date for determinism
answer = answer.sort_values(by=["ACADEMIC_YEAR", "COURSE_START_DATE"]).reset_index(drop=True)

# 11) Package result
result = {
    "course_duration_with_running_avg": answer.rename(columns={
        "COURSE_TITLE_UNIFIED": "course_title",
        "BUILDING_NAME": "building_name",
        "DURATION_DAYS": "duration_days",
        "RUNNING_AVG_DURATION_DAYS": "running_avg_duration_days",
        "COURSE_START_DATE": "course_start_date",
        "COURSE_END_DATE": "course_end_date",
    })
}