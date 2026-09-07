import pandas as pd

def first_valid(s):
    s = s.dropna()
    return s.iloc[0] if len(s) else pd.NA

def clean_str_series(s):
    return s.astype("string").str.strip()

def split_clean(x, drop_tba=False):
    if pd.isna(x):
        return []
    vals = [v.strip() for v in str(x).split(",")]
    vals = [v for v in vals if v and v.lower() not in {"nan", "none", "null"}]
    if drop_tba:
        vals = [
            v for v in vals
            if "TO BE ARRANGED" not in v.upper() and v.upper() != "TBA"
        ]
    return vals

def make_place_time_pairs(row):
    places = split_clean(row["MEET_PLACE"], drop_tba=True)
    times = split_clean(row["MEET_TIME"], drop_tba=True)
    if not places or not times:
        return []
    if len(places) == len(times):
        return list(zip(places, times))
    if len(places) == 1:
        return [(places[0], t) for t in times]
    if len(times) == 1:
        return [(p, times[0]) for p in places]
    n = min(len(places), len(times))
    return list(zip(places[:n], times[:n]))

course_cols = [
    "SUBJECT_CODE", "SUBJECT_ID", "TERM_CODE", "HGN_DESC",
    "TOTAL_UNITS", "MEET_TIME", "MEET_PLACE"
]
course_frames = []

if "table_1" in tables:
    t1 = tables["table_1"].copy()
    if "SO_TERM_CODE" in t1.columns and "TERM_CODE" not in t1.columns:
        t1 = t1.rename(columns={"SO_TERM_CODE": "TERM_CODE"})
    available = [c for c in course_cols if c in t1.columns]
    tmp = t1.loc[:, available].copy()
    for c in course_cols:
        if c not in tmp.columns:
            tmp[c] = pd.NA
    course_frames.append(tmp.loc[:, course_cols])

if "table_2" in tables:
    t2 = tables["table_2"].copy()
    available = [c for c in course_cols if c in t2.columns]
    tmp = t2.loc[:, available].copy()
    for c in course_cols:
        if c not in tmp.columns:
            tmp[c] = pd.NA
    course_frames.append(tmp.loc[:, course_cols])

if course_frames:
    courses = pd.concat(course_frames, ignore_index=True)
else:
    courses = pd.DataFrame(columns=course_cols)

courses = courses.rename(columns={
    "SUBJECT_CODE": "COURSE_NUMBER",
    "HGN_DESC": "COURSE_LEVEL"
})

courses = courses[
    courses["MEET_PLACE"].notna()
    & courses["MEET_TIME"].notna()
    & clean_str_series(courses["MEET_PLACE"]).ne("")
    & clean_str_series(courses["MEET_TIME"]).ne("")
].copy()

if not courses.empty:
    courses["place_time_pairs"] = courses.apply(make_place_time_pairs, axis=1)
    courses = courses.explode("place_time_pairs").reset_index(drop=True)
    courses = courses[courses["place_time_pairs"].notna()].reset_index(drop=True)

    if not courses.empty:
        pair_df = pd.DataFrame(
            courses["place_time_pairs"].tolist(),
            columns=["MEET_PLACE_CLEAN", "MEET_TIME_CLEAN"]
        )
        courses["MEET_PLACE_CLEAN"] = pair_df["MEET_PLACE_CLEAN"].to_numpy()
        courses["MEET_TIME_CLEAN"] = pair_df["MEET_TIME_CLEAN"].to_numpy()
    else:
        courses["MEET_PLACE_CLEAN"] = pd.Series(dtype="string")
        courses["MEET_TIME_CLEAN"] = pd.Series(dtype="string")
else:
    courses["place_time_pairs"] = pd.Series(dtype="object")
    courses["MEET_PLACE_CLEAN"] = pd.Series(dtype="string")
    courses["MEET_TIME_CLEAN"] = pd.Series(dtype="string")

courses["MEET_PLACE_CLEAN"] = clean_str_series(courses["MEET_PLACE_CLEAN"]).str.upper()
courses["MEET_TIME_CLEAN"] = clean_str_series(courses["MEET_TIME_CLEAN"])

parsed = courses["MEET_PLACE_CLEAN"].str.extract(r"^\s*([A-Z]*\d+[A-Z]*)-(.+?)\s*$")
courses["BUILDING_NUMBER_PARSED"] = parsed[0].reset_index(drop=True)
courses["ROOM_NUMBER_PARSED"] = parsed[1].reset_index(drop=True)
courses["BUILDING_ROOM"] = courses["MEET_PLACE_CLEAN"]
courses["TOTAL_UNITS"] = pd.to_numeric(courses["TOTAL_UNITS"], errors="coerce")

room_output_cols = [
    "BUILDING_ROOM", "BUILDING_NUMBER", "ROOM_NUMBER",
    "AREA", "ORGANIZATION_NAME", "MAJOR_USE_DESC"
]
room_frames = []

if "table_5" in tables:
    r5 = tables["table_5"].copy()
    tmp = pd.DataFrame(index=r5.index)
    tmp["BUILDING_ROOM"] = r5["fac_room_key"] if "fac_room_key" in r5.columns else pd.NA
    tmp["BUILDING_NUMBER"] = r5["BUILDING_KEY"] if "BUILDING_KEY" in r5.columns else pd.NA
    tmp["ROOM_NUMBER"] = r5["ROOM"] if "ROOM" in r5.columns else pd.NA
    tmp["AREA"] = r5["AREA"] if "AREA" in r5.columns else pd.NA
    tmp["ORGANIZATION_NAME"] = r5["ORGANIZATION_NAME"] if "ORGANIZATION_NAME" in r5.columns else pd.NA
    tmp["MAJOR_USE_DESC"] = r5["MAJOR_USE_DESC"] if "MAJOR_USE_DESC" in r5.columns else pd.NA
    room_frames.append(tmp.reset_index(drop=True).loc[:, room_output_cols])

if "table_3" in tables:
    r3 = tables["table_3"].copy()
    room_key_col = "BUILDING_ROOM" if "BUILDING_ROOM" in r3.columns else "FCLT_ROOM_KEY"
    tmp = pd.DataFrame(index=r3.index)
    tmp["BUILDING_ROOM"] = r3[room_key_col] if room_key_col in r3.columns else pd.NA
    tmp["BUILDING_NUMBER"] = r3["FCLT_BUILDING_KEY"] if "FCLT_BUILDING_KEY" in r3.columns else pd.NA
    tmp["ROOM_NUMBER"] = r3["ROOM"] if "ROOM" in r3.columns else pd.NA
    tmp["AREA"] = r3["AREA"] if "AREA" in r3.columns else pd.NA
    tmp["ORGANIZATION_NAME"] = r3["ORGANIZATION_NAME"] if "ORGANIZATION_NAME" in r3.columns else pd.NA
    tmp["MAJOR_USE_DESC"] = r3["MAJOR_USE_DESC"] if "MAJOR_USE_DESC" in r3.columns else pd.NA
    room_frames.append(tmp.reset_index(drop=True).loc[:, room_output_cols])

if room_frames:
    rooms = pd.concat(room_frames, ignore_index=True).drop_duplicates().reset_index(drop=True)
else:
    rooms = pd.DataFrame(columns=room_output_cols)

rooms["BUILDING_ROOM"] = clean_str_series(rooms["BUILDING_ROOM"]).str.upper()
rooms["BUILDING_NUMBER"] = clean_str_series(rooms["BUILDING_NUMBER"])
rooms["ROOM_NUMBER"] = clean_str_series(rooms["ROOM_NUMBER"])

if "table_7" in tables and {"BUILDING_ROOM", "SPACE_USAGE"}.issubset(tables["table_7"].columns):
    usage = tables["table_7"].loc[:, ["BUILDING_ROOM", "SPACE_USAGE"]].copy()
    usage["BUILDING_ROOM"] = clean_str_series(usage["BUILDING_ROOM"]).str.upper()
    usage = usage.groupby("BUILDING_ROOM", as_index=False, dropna=False).agg(
        SPACE_USAGE=("SPACE_USAGE", first_valid)
    )
    rooms = rooms.merge(usage, on="BUILDING_ROOM", how="left")
else:
    rooms["SPACE_USAGE"] = pd.NA

rooms["ROOM_USAGE"] = rooms["SPACE_USAGE"].combine_first(rooms["MAJOR_USE_DESC"])

rooms = rooms.groupby("BUILDING_ROOM", as_index=False, dropna=False).agg(
    BUILDING_NUMBER=("BUILDING_NUMBER", first_valid),
    ROOM_NUMBER=("ROOM_NUMBER", first_valid),
    AREA=("AREA", first_valid),
    ORGANIZATION_NAME=("ORGANIZATION_NAME", first_valid),
    ROOM_USAGE=("ROOM_USAGE", first_valid)
)

building_frames = []
for df_src in tables.values():
    df_src = df_src.copy()
    colmap = {}
    for c in df_src.columns:
        cu = str(c).upper()
        if cu not in colmap:
            colmap[cu] = c

    key_col = None
    for cand in ["BUILDING_KEY", "FCLT_BUILDING_KEY", "BUILDING_NUMBER", "BUILDING_COMPONENT"]:
        if cand in colmap:
            key_col = colmap[cand]
            break
    if key_col is None:
        continue

    name_col = next((colmap[c] for c in ["BUILDING_NAME", "NAME"] if c in colmap), None)
    city_col = next((colmap[c] for c in ["BUILDING_CITY", "CITY"] if c in colmap), None)
    state_col = next((colmap[c] for c in ["BUILDING_STATE", "STATE"] if c in colmap), None)
    if not (name_col or city_col or state_col):
        continue

    tmp = pd.DataFrame(index=df_src.index)
    tmp["BUILDING_NUMBER"] = clean_str_series(df_src[key_col])
    tmp["BUILDING_NAME"] = df_src[name_col] if name_col else pd.NA
    tmp["BUILDING_CITY"] = df_src[city_col] if city_col else pd.NA
    tmp["BUILDING_STATE"] = df_src[state_col] if state_col else pd.NA
    building_frames.append(tmp.reset_index(drop=True))

if building_frames:
    building_dim = pd.concat(building_frames, ignore_index=True)
    building_dim = building_dim.groupby("BUILDING_NUMBER", as_index=False, dropna=False).agg(
        BUILDING_NAME=("BUILDING_NAME", first_valid),
        BUILDING_CITY=("BUILDING_CITY", first_valid),
        BUILDING_STATE=("BUILDING_STATE", first_valid)
    )
else:
    building_dim = pd.DataFrame(columns=[
        "BUILDING_NUMBER", "BUILDING_NAME", "BUILDING_CITY", "BUILDING_STATE"
    ])

df = courses.merge(rooms, on="BUILDING_ROOM", how="left")
df["ROOM_NUMBER"] = df["ROOM_NUMBER"].combine_first(df["ROOM_NUMBER_PARSED"])
df["BUILDING_NUMBER"] = df["BUILDING_NUMBER"].combine_first(df["BUILDING_NUMBER_PARSED"])
df["BUILDING_NUMBER"] = clean_str_series(df["BUILDING_NUMBER"])

df = df.merge(building_dim, on="BUILDING_NUMBER", how="left")

group_cols = [
    "COURSE_NUMBER",
    "ROOM_NUMBER",
    "BUILDING_NAME",
    "BUILDING_NUMBER",
    "BUILDING_CITY",
    "BUILDING_STATE",
    "AREA",
    "ORGANIZATION_NAME",
    "ROOM_USAGE",
    "TERM_CODE",
    "COURSE_LEVEL"
]

for c in group_cols + ["SUBJECT_ID", "MEET_TIME_CLEAN", "TOTAL_UNITS"]:
    if c not in df.columns:
        df[c] = pd.NA

base_agg = df.groupby(group_cols, as_index=False, dropna=False).agg(
    TOTAL_NUMBER_OF_SUBJECTS=("SUBJECT_ID", "nunique"),
    UNIQUE_MEETING_TIMES=("MEET_TIME_CLEAN", "nunique")
)

units_agg = (
    df.drop_duplicates(group_cols + ["SUBJECT_ID"])
      .groupby(group_cols, as_index=False, dropna=False)
      .agg(TOTAL_UNITS=("TOTAL_UNITS", "sum"))
)

final = base_agg.merge(units_agg, on=group_cols, how="left")

final_cols = [
    "COURSE_NUMBER",
    "ROOM_NUMBER",
    "BUILDING_NAME",
    "BUILDING_NUMBER",
    "BUILDING_CITY",
    "BUILDING_STATE",
    "AREA",
    "ORGANIZATION_NAME",
    "ROOM_USAGE",
    "TERM_CODE",
    "COURSE_LEVEL",
    "TOTAL_NUMBER_OF_SUBJECTS",
    "UNIQUE_MEETING_TIMES",
    "TOTAL_UNITS"
]

final = final.loc[:, final_cols].sort_values(
    ["COURSE_NUMBER", "TERM_CODE", "BUILDING_NUMBER", "ROOM_NUMBER", "COURSE_LEVEL"],
    na_position="last"
).reset_index(drop=True)

result = {
    "course_location_summary": final
}
