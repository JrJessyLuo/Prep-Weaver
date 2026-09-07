import pandas as pd
import numpy as np
import re

df = tables["table_2"].copy()

# Keep MIT-offered subjects where possible
if "OFFER_SCHOOL_NAME" in df.columns:
    df = df[df["OFFER_SCHOOL_NAME"].isna() | (df["OFFER_SCHOOL_NAME"].astype(str).str.strip() != "Non-MIT")]

# Course level: map MIT HGN codes to requested labels
hgn = df["HGN_CODE"].astype("string").str.strip().str.upper()
df["course_level"] = pd.NA
df.loc[hgn.isin(["G", "H"]), "course_level"] = "Graduate"
df.loc[hgn.isin(["U", "N"]), "course_level"] = "Undergraduate"

# Fallback from descriptions if needed
desc = df["HGN_CODE_DESC"].astype("string").str.lower()
missing_level = df["course_level"].isna()
df.loc[missing_level & desc.str.contains("not for graduate|undergraduate", na=False), "course_level"] = "Undergraduate"
df.loc[
    missing_level
    & desc.str.contains("graduate", na=False)
    & ~desc.str.contains("not for graduate", na=False),
    "course_level"
] = "Graduate"

# Extract MIT building identifiers from MEET_PLACE, e.g. "26-100" -> "26", "E51-350" -> "E51"
building_pattern = re.compile(r"(?<![A-Z0-9])([A-Z]{0,3}\d{1,3}[A-Z]?)-[A-Z0-9]", flags=re.I)

def extract_buildings(x):
    if pd.isna(x):
        return []
    return sorted(set(m.group(1).upper() for m in building_pattern.finditer(str(x))))

df["building_name"] = df["MEET_PLACE"].apply(extract_buildings)
df = df.explode("building_name")

# Standardize course and instructor identifiers
df["course_key"] = df["SUBJECT_ID"].astype("string").str.strip()

mit_id = pd.to_numeric(df["responsible_faculty_mit_id"], errors="coerce")
df["instructor_key"] = pd.NA
has_id = mit_id.notna()
df.loc[has_id, "instructor_key"] = "MIT_ID:" + mit_id.loc[has_id].astype("int64").astype(str)

name = df["RESPONSIBLE_FACULTY_NAME"].astype("string").str.strip()
has_name_only = ~has_id & name.notna() & (name != "")
df.loc[has_name_only, "instructor_key"] = "NAME:" + name.loc[has_name_only]

base = (
    df.dropna(subset=["building_name", "course_level", "course_key"])
      [["building_name", "course_level", "course_key", "instructor_key"]]
      .drop_duplicates()
)

def summarize(data, group_cols):
    if group_cols:
        out = (
            data.groupby(group_cols, dropna=False)
                .agg(
                    total_unique_courses=("course_key", "nunique"),
                    total_instructors=("instructor_key", lambda s: s.dropna().nunique())
                )
                .reset_index()
        )
    else:
        out = pd.DataFrame([{
            "total_unique_courses": data["course_key"].nunique(),
            "total_instructors": data["instructor_key"].dropna().nunique()
        }])
    return out

detail = summarize(base, ["building_name", "course_level"])
detail["_section_order"] = 0

building_subtotals = summarize(base, ["building_name"])
building_subtotals["course_level"] = "All Levels"
building_subtotals["_section_order"] = 1

level_subtotals = summarize(base, ["course_level"])
level_subtotals["building_name"] = "All Buildings"
level_subtotals["_section_order"] = 2

grand_total = summarize(base, [])
grand_total["building_name"] = "All Buildings"
grand_total["course_level"] = "All Levels"
grand_total["_section_order"] = 3

out = pd.concat(
    [
        detail,
        building_subtotals[detail.columns],
        level_subtotals[detail.columns],
        grand_total[detail.columns],
    ],
    ignore_index=True
)

level_order = {"Undergraduate": 0, "Graduate": 1, "All Levels": 2}
out["_building_sort"] = np.where(out["building_name"].eq("All Buildings"), "ZZZZZZ", out["building_name"])
out["_level_sort"] = out["course_level"].map(level_order).fillna(99)

out = (
    out.sort_values(["_section_order", "_building_sort", "_level_sort", "course_level"])
       .drop(columns=["_section_order", "_building_sort", "_level_sort"])
       .reset_index(drop=True)
)

result = {
    "building_course_level_summary": out[
        ["building_name", "course_level", "total_unique_courses", "total_instructors"]
    ]
}
