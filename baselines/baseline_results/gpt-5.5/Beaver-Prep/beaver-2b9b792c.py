import pandas as pd
import numpy as np
import re

# -----------------------------
# Courses: one row per course/location/date, with previous/next course names
# -----------------------------
courses = tables["table_2"].copy()

courses["start_date"] = pd.to_datetime(courses["DATE_FROM"], format="%d-%b-%y", errors="coerce")

courses = (
    courses[["COURSE_NAME", "DATE_FROM", "start_date", "UNIT_CODE", "UNIT"]]
    .drop_duplicates()
    .sort_values(["start_date", "COURSE_NAME"], ascending=[True, True], kind="mergesort")
    .reset_index(drop=True)
)

courses["course_before"] = courses["COURSE_NAME"].shift(1)
courses["course_after"] = courses["COURSE_NAME"].shift(-1)

# -----------------------------
# Current room and building data
# -----------------------------
rooms = tables["table_3"].copy()
rooms = rooms.rename(columns={
    "fac_room_key": "FCLT_ROOM_KEY",
    "BUILDING_KEY": "FCLT_BUILDING_KEY"
})

buildings = tables["table_9"].copy()

room_cols = [
    "FCLT_ROOM_KEY", "FCLT_BUILDING_KEY", "ROOM", "SPACE_ID",
    "ROOM_FULL_NAME", "ORGANIZATION_NAME", "AREA"
]
room_cols = [c for c in room_cols if c in rooms.columns]

building_cols = [
    "FCLT_BUILDING_KEY", "BUILDING_NAME", "BUILDING_NAME_LONG",
    "ACCESS_LEVEL_CODE", "ACCESS_LEVEL_NAME"
]
building_cols = [c for c in building_cols if c in buildings.columns]

room_building = rooms[room_cols].merge(
    buildings[building_cols],
    on="FCLT_BUILDING_KEY",
    how="left"
)

# -----------------------------
# Helper functions for fuzzy location matching
# -----------------------------
def norm_text(x):
    if pd.isna(x):
        return ""
    x = str(x).upper()
    x = re.sub(r"[^A-Z0-9]+", " ", x)
    return re.sub(r"\s+", " ", x).strip()

library_aliases = {
    "ENG": "BARKER",
    "BARKER": "BARKER",
    "DEW": "DEWEY",
    "DEWEY": "DEWEY",
    "HAYDEN": "HAYDEN",
    "ROTCH": "ROTCH",
    "MUSIC": "LEWIS MUSIC",
    "LEWIS": "LEWIS MUSIC",
    "AERO": "AERONAUTICS ASTRONAUTICS",
    "GIS": "GIS",
    "SCI": "SCIENCE",
}

for col in ["ROOM_FULL_NAME", "ORGANIZATION_NAME", "BUILDING_NAME", "BUILDING_NAME_LONG", "FCLT_ROOM_KEY"]:
    if col in room_building.columns:
        room_building[f"_{col}_norm"] = room_building[col].map(norm_text)
    else:
        room_building[f"_{col}_norm"] = ""

room_building["_search_text"] = (
    room_building["_ROOM_FULL_NAME_norm"] + " " +
    room_building["_ORGANIZATION_NAME_norm"] + " " +
    room_building["_BUILDING_NAME_norm"] + " " +
    room_building["_BUILDING_NAME_LONG_norm"] + " " +
    room_building["_FCLT_ROOM_KEY_norm"]
).str.strip()

def best_location_match(unit_code, unit):
    terms = []
    for value in [unit, unit_code]:
        n = norm_text(value)
        if n:
            terms.append(n)
            if n in library_aliases:
                terms.append(norm_text(library_aliases[n]))
    terms = list(dict.fromkeys([t for t in terms if t]))

    if not terms:
        return pd.Series({
            "building_name": np.nan,
            "building_access_level": np.nan,
            "room_assignable_area": np.nan
        })

    candidates = room_building.iloc[0:0].copy()

    for term in terms:
        mask = room_building["_search_text"].str.contains(re.escape(term), na=False)
        tmp = room_building.loc[mask].copy()
        if tmp.empty:
            continue

        tmp["_match_score"] = 0
        tmp.loc[tmp["_ROOM_FULL_NAME_norm"].eq(term), "_match_score"] += 100
        tmp.loc[tmp["_ROOM_FULL_NAME_norm"].str.contains(re.escape(term), na=False), "_match_score"] += 80
        tmp.loc[tmp["_BUILDING_NAME_LONG_norm"].str.contains(re.escape(term), na=False), "_match_score"] += 60
        tmp.loc[tmp["_BUILDING_NAME_norm"].str.contains(re.escape(term), na=False), "_match_score"] += 60
        tmp.loc[tmp["_ORGANIZATION_NAME_norm"].str.contains(re.escape(term), na=False), "_match_score"] += 40
        tmp.loc[tmp["_FCLT_ROOM_KEY_norm"].str.contains(re.escape(term), na=False), "_match_score"] += 20

        candidates = pd.concat([candidates, tmp], ignore_index=True)

    if candidates.empty:
        return pd.Series({
            "building_name": np.nan,
            "building_access_level": np.nan,
            "room_assignable_area": np.nan
        })

    candidates = candidates.drop_duplicates(subset=["FCLT_ROOM_KEY", "FCLT_BUILDING_KEY"])
    candidates["_area_sort"] = pd.to_numeric(candidates["AREA"], errors="coerce").fillna(-1)

    best = candidates.sort_values(
        ["_match_score", "_area_sort"],
        ascending=[False, False],
        kind="mergesort"
    ).iloc[0]

    building_name = best.get("BUILDING_NAME_LONG")
    if pd.isna(building_name) or building_name == "":
        building_name = best.get("BUILDING_NAME")

    access_level = best.get("ACCESS_LEVEL_NAME")
    if pd.isna(access_level):
        access_level = best.get("ACCESS_LEVEL_CODE")

    return pd.Series({
        "building_name": building_name,
        "building_access_level": access_level,
        "room_assignable_area": best.get("AREA")
    })

# -----------------------------
# Build one location lookup per course UNIT/UNIT_CODE
# -----------------------------
location_keys = courses[["UNIT_CODE", "UNIT"]].drop_duplicates().reset_index(drop=True)

location_info = location_keys.apply(
    lambda r: best_location_match(r["UNIT_CODE"], r["UNIT"]),
    axis=1
)

location_lookup = pd.concat([location_keys, location_info], axis=1)

# -----------------------------
# Final result
# -----------------------------
out = courses.merge(location_lookup, on=["UNIT_CODE", "UNIT"], how="left")

out = out.sort_values(
    ["start_date", "COURSE_NAME"],
    ascending=[True, True],
    kind="mergesort"
).reset_index(drop=True)

out = out[[
    "COURSE_NAME",
    "building_name",
    "DATE_FROM",
    "course_before",
    "course_after",
    "building_access_level",
    "room_assignable_area"
]].rename(columns={
    "COURSE_NAME": "course_name",
    "DATE_FROM": "start_date"
})

result = {
    "course_location_sequence": out
}
