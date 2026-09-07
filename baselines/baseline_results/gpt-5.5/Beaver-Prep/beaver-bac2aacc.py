import pandas as pd
import numpy as np
import re

def get_col(df, col):
    if col in df.columns:
        x = df.loc[:, col]
        if isinstance(x, pd.DataFrame):
            return x.iloc[:, 0]
        return x
    return pd.Series(pd.NA, index=df.index, dtype="object")

def coalesce_cols(df, candidates):
    out = pd.Series(pd.NA, index=df.index, dtype="object")
    for c in candidates:
        if c in df.columns:
            out = out.combine_first(get_col(df, c))
    return out

def yes_like(s):
    return s.astype("string").str.strip().str.upper().eq("Y").fillna(False)

def contains_yes(s):
    return s.astype("string").str.upper().str.contains(r"(^|,)\s*Y\s*(,|$)|\bY\b", regex=True, na=False)

def clean_string_cols(df):
    out = df.copy()
    for c in out.columns:
        if pd.api.types.is_object_dtype(out[c]) or pd.api.types.is_string_dtype(out[c]):
            out[c] = out[c].astype("string").str.strip()
    return out

frames = []

for table_name, df in tables.items():
    if not isinstance(df, pd.DataFrame):
        continue

    has_subject = ("SUBJECT_ID" in df.columns) or ("subject_id" in df.columns)
    useful_cols = {
        "SUBJECT_DESCRIPTION",
        "IS_OFFERED_SUMMER_TERM",
        "MEET_PLACE",
        "RESPONSIBLE_FACULTY_NAME",
        "SUBJECT_TITLE",
        "SUBJECT_SHORT_TITLE",
    }
    if has_subject and any(c in df.columns for c in useful_cols):
        tmp = pd.DataFrame(index=df.index)

        tmp["academic_year"] = coalesce_cols(df, ["ACADEMIC_YEAR"])
        tmp["term_code"] = coalesce_cols(df, ["SO_TERM_CODE", "TERM_CODE", "term_code"])
        tmp["term_description"] = coalesce_cols(df, ["SO_TERM_DESCRIPTION", "TERM_DESCRIPTION"])
        tmp["subject_id"] = coalesce_cols(df, ["SUBJECT_ID", "subject_id", "SO_SUBJECT_ID"])
        tmp["subject_title"] = coalesce_cols(df, ["SUBJECT_TITLE", "SUBJECT_SHORT_TITLE", "SUBJECT_TITLE_LONG"])
        tmp["subject_description"] = coalesce_cols(df, ["SUBJECT_DESCRIPTION"])
        tmp["department_code"] = coalesce_cols(df, ["DEPARTMENT_CODE", "OFFER_DEPT_CODE"])
        tmp["department_name"] = coalesce_cols(df, ["DEPARTMENT_NAME", "OFFER_DEPT_NAME"])
        tmp["responsible_faculty_name"] = coalesce_cols(df, ["RESPONSIBLE_FACULTY_NAME"])
        tmp["responsible_faculty_mit_id"] = coalesce_cols(
            df, ["RESPONSIBLE_FACULTY_MIT_ID", "responsible_faculty_mit_id"]
        )
        tmp["meet_place"] = coalesce_cols(df, ["MEET_PLACE"])
        tmp["is_offered_summer_term"] = coalesce_cols(df, ["IS_OFFERED_SUMMER_TERM"])
        tmp["course_type_base"] = coalesce_cols(
            df, ["FORM_TYPE_DESC", "FORM_TYPE", "HGN_DESC", "HGN_CODE_DESC", "HGN_CODE", "GRADE_TYPE_DESC", "GRADE_TYPE", "TERM_DURATION"]
        )

        email_cols = [c for c in df.columns if "EMAIL" in str(c).upper()]
        tmp["email_address"] = get_col(df, email_cols[0]) if email_cols else pd.Series(pd.NA, index=df.index, dtype="object")

        tmp["building_name_source"] = coalesce_cols(
            df, ["BUILDING_NAME", "BLDG_NAME", "BUILDING", "BUILDING_DESC"]
        )
        tmp["room_name_source"] = coalesce_cols(
            df, ["ROOM_NAME", "ROOM", "ROOM_NUMBER", "CLASSROOM"]
        )
        tmp["floor_level_source"] = coalesce_cols(
            df, ["FLOOR_LEVEL", "FLOOR", "BUILDING_FLOOR"]
        )
        tmp["building_street_address"] = coalesce_cols(
            df, ["BUILDING_STREET_ADDRESS", "STREET_ADDRESS", "BUILDING_ADDRESS", "ADDRESS"]
        )

        for flag in [
            "IS_LECTURE_SECTION",
            "IS_LAB_SECTION",
            "IS_RECITATION_SECTION",
            "IS_DESIGN_SECTION",
            "IS_MASTER_SECTION",
        ]:
            tmp[flag] = get_col(df, flag) if flag in df.columns else pd.Series(pd.NA, index=df.index, dtype="object")

        frames.append(tmp)

final_columns = [
    "term_code",
    "subject_id",
    "subject_title",
    "subject_description",
    "department_code",
    "department_name",
    "responsible_faculty_name",
    "email_address",
    "building_name",
    "room_name",
    "floor_level",
    "building_street_address",
    "total_number_of_course_types_per_department",
]

if frames:
    subjects = pd.concat(frames, ignore_index=True)
    subjects = clean_string_cols(subjects)

    term_upper = subjects["term_code"].astype("string").str.upper()
    term_desc_upper = subjects["term_description"].astype("string").str.upper()

    actual_summer_mask = (
        term_upper.str.contains(r"(SU|SUM|SUMMER)$|SUMMER", regex=True, na=False)
        | term_desc_upper.str.contains("SUMMER", na=False)
    )

    if actual_summer_mask.any():
        summer = subjects.loc[actual_summer_mask].copy()
    else:
        summer = subjects.loc[yes_like(subjects["is_offered_summer_term"])].copy()

    section_type_defs = [
        ("Lecture", "IS_LECTURE_SECTION"),
        ("Lab", "IS_LAB_SECTION"),
        ("Recitation", "IS_RECITATION_SECTION"),
        ("Design", "IS_DESIGN_SECTION"),
        ("Master", "IS_MASTER_SECTION"),
    ]

    type_parts = []
    for label, flag_col in section_type_defs:
        m = contains_yes(summer[flag_col]) if flag_col in summer.columns else pd.Series(False, index=summer.index)
        if m.any():
            type_parts.append(
                summer.loc[m, ["department_code", "department_name"]].assign(course_type=label)
            )

    if type_parts:
        course_types_long = pd.concat(type_parts, ignore_index=True)
    else:
        course_types_long = (
            summer[["department_code", "department_name", "course_type_base"]]
            .rename(columns={"course_type_base": "course_type"})
            .copy()
        )

    course_types_long["course_type"] = course_types_long["course_type"].astype("string").str.strip()
    course_types_long = course_types_long[
        course_types_long["course_type"].notna() & course_types_long["course_type"].ne("")
    ]

    if len(course_types_long) > 0:
        type_counts = (
            course_types_long
            .groupby(["department_code", "department_name"], dropna=False)["course_type"]
            .nunique()
            .reset_index(name="total_number_of_course_types_per_department")
        )
    else:
        type_counts = pd.DataFrame(
            columns=["department_code", "department_name", "total_number_of_course_types_per_department"]
        )

    summer["meet_place_part"] = (
        summer["meet_place"]
        .astype("string")
        .fillna("")
        .str.split(r"\s*,\s*", regex=True)
    )
    summer = summer.explode("meet_place_part", ignore_index=True)
    summer["meet_place_part"] = summer["meet_place_part"].astype("string").str.strip()

    invalid_place = (
        summer["meet_place_part"].eq("")
        | summer["meet_place_part"].str.contains(
            r"TO BE ARRANGED|TBA|REMOTE|ONLINE|VIRTUAL", case=False, regex=True, na=False
        )
    )

    parsed_place = summer["meet_place_part"].where(~invalid_place).str.extract(
        r"^\s*([A-Za-z]*\d+[A-Za-z]*|\d+[A-Za-z]*|[A-Za-z]+\d*)-([A-Za-z0-9]+)",
        expand=True,
    )

    building_id = parsed_place[0].astype("string")
    room_id = parsed_place[1].astype("string")

    parsed_building_name = ("Building " + building_id).where(building_id.notna(), pd.NA)

    room_upper = room_id.astype("string").str.upper()
    floor_digit = room_upper.str.extract(r"^([0-9])", expand=False)
    floor_special = room_upper.str.extract(r"^([BGL])", expand=False)
    floor_level = floor_digit.combine_first(
        floor_special.map({"B": "Basement", "G": "Ground", "L": "Lower"})
    )

    summer["building_name"] = summer["building_name_source"].combine_first(parsed_building_name)
    summer["room_name"] = summer["room_name_source"].combine_first(room_id)
    summer["floor_level"] = summer["floor_level_source"].combine_first(floor_level)

    out = summer.merge(
        type_counts,
        on=["department_code", "department_name"],
        how="left",
    )

    out["total_number_of_course_types_per_department"] = (
        out["total_number_of_course_types_per_department"].fillna(0).astype(int)
    )

    out = out[final_columns].drop_duplicates().reset_index(drop=True)
else:
    out = pd.DataFrame(columns=final_columns)

result = {"summer_subject_details": out}
