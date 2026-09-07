import pandas as pd

def clean_text(s):
    return s.astype("string").str.strip().replace("", pd.NA)

def clean_code(s):
    return clean_text(s).str.upper()

def most_common_value(s):
    s = s.dropna()
    if s.empty:
        return pd.NA
    counts = s.astype(str).value_counts()
    max_count = counts.max()
    return sorted(counts[counts == max_count].index)[0]

# SIS course descriptions
sis = tables["table_1"].copy()
sis = sis.assign(
    department_code=clean_code(sis["DEPARTMENT"]),
    department_name_sis=clean_text(sis["DEPARTMENT_NAME"]),
    school_name_sis=clean_text(sis["SCHOOL_NAME"]),
    course_level=clean_code(sis["COURSE_LEVEL"])
)

# Build department/school lookup candidates
candidate_frames = []

if "table_3" in tables:
    d = tables["table_3"].copy()
    candidate_frames.append(pd.DataFrame({
        "key": clean_code(d["DEPARTMENT_CODE"]),
        "school_code_dim": clean_code(d["SCHOOL_CODE"]),
        "school_name_dim": clean_text(d["SCHOOL_NAME"]),
        "department_name_dim": clean_text(d["DEPARTMENT_NAME"]),
        "priority": 1
    }))

if "table_5" in tables:
    d = tables["table_5"].copy()
    candidate_frames.append(pd.DataFrame({
        "key": clean_code(d["DEPARTMENT_CODE"]),
        "school_code_dim": clean_code(d["SCHOOL_CODE"]),
        "school_name_dim": clean_text(d["SCHOOL_NAME"]),
        "department_name_dim": clean_text(d["DEPARTMENT_NAME"]),
        "priority": 2
    }))

if "table_2" in tables:
    d = tables["table_2"].copy()
    for col, priority in [
        ("DEPARTMENT_CODE", 3),
        ("SUBJECT_CODE", 4),
        ("COURSE_NUMBER", 5),
    ]:
        candidate_frames.append(pd.DataFrame({
            "key": clean_code(d[col]),
            "school_code_dim": clean_code(d["SCHOOL_CODE"]),
            "school_name_dim": clean_text(d["SCHOOL_NAME"]),
            "department_name_dim": clean_text(d["DEPARTMENT_NAME"]),
            "priority": priority
        }))

dept_dim = (
    pd.concat(candidate_frames, ignore_index=True)
    .dropna(subset=["key"])
    .sort_values(["priority", "key"])
    .drop_duplicates("key", keep="first")
    .drop(columns="priority")
)

# Build school-name-to-code lookup as a fallback
school_frames = []

if "table_3" in tables:
    d = tables["table_3"].copy()
    school_frames.append(pd.DataFrame({
        "school_name_key": clean_text(d["SCHOOL_NAME"]).str.upper(),
        "school_code": clean_code(d["SCHOOL_CODE"])
    }))
    if "SCHOOL_NAME_IN_COMMENCEMENT_BK" in d.columns:
        school_frames.append(pd.DataFrame({
            "school_name_key": clean_text(d["SCHOOL_NAME_IN_COMMENCEMENT_BK"]).str.upper(),
            "school_code": clean_code(d["SCHOOL_CODE"])
        }))

if "table_5" in tables:
    d = tables["table_5"].copy()
    school_frames.append(pd.DataFrame({
        "school_name_key": clean_text(d["SCHOOL_NAME"]).str.upper(),
        "school_code": clean_code(d["SCHOOL_CODE"])
    }))

if "table_2" in tables:
    d = tables["table_2"].copy()
    school_frames.append(pd.DataFrame({
        "school_name_key": clean_text(d["SCHOOL_NAME"]).str.upper(),
        "school_code": clean_code(d["SCHOOL_CODE"])
    }))

school_lookup = (
    pd.concat(school_frames, ignore_index=True)
    .dropna(subset=["school_name_key", "school_code"])
    .drop_duplicates("school_name_key", keep="first")
)

school_code_map = dict(zip(school_lookup["school_name_key"], school_lookup["school_code"]))

# Enrich SIS rows with school code/name
sis = sis.merge(
    dept_dim,
    left_on="department_code",
    right_on="key",
    how="left"
)

sis["school_code"] = sis["school_code_dim"]
missing_school_code = sis["school_code"].isna()
sis.loc[missing_school_code, "school_code"] = (
    sis.loc[missing_school_code, "school_name_sis"]
    .astype("string")
    .str.strip()
    .str.upper()
    .map(school_code_map)
)

sis["school_name"] = sis["school_name_dim"].combine_first(sis["school_name_sis"])
sis["department_name"] = sis["department_name_sis"].combine_first(sis["department_name_dim"])

# Count phone numbers by SIS admin department code
phones = tables["table_6"].copy()
phones["department_code"] = clean_code(phones["SIS_ADMIN_DEPARTMENT_CODE"])

phone_counts = (
    phones.dropna(subset=["department_phone_number"])
    .groupby("department_code", as_index=False)["department_phone_number"]
    .nunique()
    .rename(columns={"department_phone_number": "total_number_of_phone_numbers"})
)

# Aggregate to the requested school/department level
answer = (
    sis.dropna(subset=["department_code"])
    .groupby(["school_code", "school_name", "department_code"], dropna=False, as_index=False)
    .agg(
        department_name=("department_name", most_common_value),
        most_common_course_level=("course_level", most_common_value)
    )
    .merge(phone_counts, on="department_code", how="left")
)

answer["total_number_of_phone_numbers"] = (
    answer["total_number_of_phone_numbers"]
    .fillna(0)
    .astype(int)
)

answer = answer[
    [
        "school_code",
        "school_name",
        "department_code",
        "department_name",
        "total_number_of_phone_numbers",
        "most_common_course_level",
    ]
].sort_values(
    ["school_code", "school_name", "department_code"],
    na_position="last"
).reset_index(drop=True)

result = {
    "sis_course_schools_departments": answer
}
