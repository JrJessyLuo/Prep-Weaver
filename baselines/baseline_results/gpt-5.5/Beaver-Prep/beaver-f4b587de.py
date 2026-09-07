import pandas as pd

# Base IAP/independent activities
activities = tables["table_1"].copy()

# Sessions provide activity locations
sessions = tables["table_3"].copy()
activities_sessions = activities.merge(
    sessions[["iap_subject_session_key", "SESSION_LOCATION"]].drop_duplicates(),
    left_on="IAP_SUBJECT_SESSION_KEY",
    right_on="iap_subject_session_key",
    how="left"
)

# Academic terms provide term start dates
term_frames = []
if "table_8" in tables:
    term_frames.append(tables["table_8"][["term_code", "TERM_START_DATE"]])
if "table_6" in tables:
    term_frames.append(tables["table_6"][["term_code", "TERM_START_DATE"]])

terms = (
    pd.concat(term_frames, ignore_index=True)
    .dropna(subset=["term_code"])
    .drop_duplicates(subset=["term_code"], keep="first")
)

df = activities_sessions.merge(
    terms,
    left_on="TERM_CODE",
    right_on="term_code",
    how="left"
)

# Try to obtain supervisor/responsible faculty names by exact title + term match
def _norm_text(s):
    return (
        s.astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
    )

supervisor_maps = []

for table_name in ["table_10", "table_4", "table_5"]:
    if table_name not in tables:
        continue

    t = tables[table_name].copy()
    cols = t.columns

    if "SUBJECT_TITLE" not in cols:
        continue

    term_col = None
    if "TERM_CODE" in cols:
        term_col = "TERM_CODE"
    elif "SO_TERM_CODE" in cols:
        term_col = "SO_TERM_CODE"

    name_col = None
    if "RESPONSIBLE_FACULTY_NAME" in cols:
        name_col = "RESPONSIBLE_FACULTY_NAME"
    elif "responsible_faculty_name" in cols:
        name_col = "responsible_faculty_name"

    if term_col is None or name_col is None:
        continue

    tmp = t[[term_col, "SUBJECT_TITLE", name_col]].dropna(subset=[name_col]).copy()
    tmp["_term_key"] = tmp[term_col].astype("string").str.strip()
    tmp["_title_key"] = _norm_text(tmp["SUBJECT_TITLE"])
    tmp[name_col] = tmp[name_col].astype("string").str.strip()

    tmp = (
        tmp.groupby(["_term_key", "_title_key"], as_index=False)[name_col]
        .agg(lambda x: ", ".join(sorted(set(v for v in x.dropna() if v))))
        .rename(columns={name_col: "SUPERVISOR_NAME"})
    )

    supervisor_maps.append(tmp)

if supervisor_maps:
    supervisors = (
        pd.concat(supervisor_maps, ignore_index=True)
        .dropna(subset=["SUPERVISOR_NAME"])
        .drop_duplicates(subset=["_term_key", "_title_key"], keep="first")
    )

    df["_term_key"] = df["TERM_CODE"].astype("string").str.strip()
    df["_title_key"] = _norm_text(df["ACTIVITY_TITLE"])

    df = df.merge(
        supervisors,
        on=["_term_key", "_title_key"],
        how="left"
    )
else:
    df["SUPERVISOR_NAME"] = pd.NA

# Final formatting
df["LOCATION"] = df["SESSION_LOCATION"].astype("string").str.strip()
df["_sort_start_date"] = pd.to_datetime(df["TERM_START_DATE"], format="%d-%b-%y", errors="coerce")

out = (
    df[["ACTIVITY_TITLE", "LOCATION", "TERM_START_DATE", "SUPERVISOR_NAME", "_sort_start_date"]]
    .drop_duplicates(subset=["ACTIVITY_TITLE", "LOCATION", "TERM_START_DATE", "SUPERVISOR_NAME"])
    .sort_values(["_sort_start_date", "ACTIVITY_TITLE", "LOCATION"], ascending=True, na_position="last")
    .drop(columns=["_sort_start_date"])
    .reset_index(drop=True)
)

result = {
    "independent_activities": out
}
