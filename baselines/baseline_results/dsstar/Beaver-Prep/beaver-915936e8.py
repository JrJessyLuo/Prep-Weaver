import pandas as pd
import numpy as np

# Input tables already loaded in a dict named `tables`
# Mapping:
# tables['table_5'] -> ACADEMIC_TERMS.pkl
# tables['table_6'] -> COURSE_CATALOG_SUBJECT_OFFERED.pkl

# 1) Load Data from provided tables dict
df = tables['table_6'].copy()
terms = tables['table_5'].copy()

# 2) Construct course_name (SUBJECT_CODE.SUBJECT_NUMBER) matching reference logic
for col in ["SUBJECT_CODE", "SUBJECT_NUMBER"]:
    if col not in df.columns:
        df[col] = np.nan
df["SUBJECT_CODE"] = df["SUBJECT_CODE"].astype(str).str.strip()
df["SUBJECT_NUMBER"] = df["SUBJECT_NUMBER"].astype(str).str.strip()
df["course_name"] = np.where(
    df["SUBJECT_CODE"].notna() & df["SUBJECT_CODE"].ne("nan") & df["SUBJECT_NUMBER"].notna() & df["SUBJECT_NUMBER"].ne("nan"),
    df["SUBJECT_CODE"] + "." + df["SUBJECT_NUMBER"],
    df.get("COURSE_NAME", pd.Series(index=df.index, dtype="object"))
)

# 3) Parse MEET_PLACE to extract a building code/name (first token or left of hyphen)
if "MEET_PLACE" not in df.columns:
    df["MEET_PLACE"] = np.nan

def extract_building(meet_place: str):
    if pd.isna(meet_place):
        return np.nan
    s = str(meet_place).strip()
    if not s:
        return np.nan
    if "-" in s:
        return s.split("-")[0].strip()
    return s.split()[0].strip()

df["building_code"] = df["MEET_PLACE"].apply(extract_building)

# 4) Prepare ACADEMIC_TERMS join for FIRST_DAY_OF_CLASSES
term_key_offered = "TERM_CODE" if "TERM_CODE" in df.columns else None
if term_key_offered is None:
    if "EFFECTIVE_TERM_CODE" in df.columns:
        term_key_offered = "EFFECTIVE_TERM_CODE"
    else:
        df["TERM_CODE"] = np.nan
        term_key_offered = "TERM_CODE"

term_cols_needed = ["term_code", "FIRST_DAY_OF_CLASSES", "ACADEMIC_YEAR"]
available_term_cols = [c for c in term_cols_needed if c in terms.columns]
terms_sel = terms[available_term_cols].drop_duplicates(subset=["term_code"]) if "term_code" in terms.columns else pd.DataFrame(columns=["term_code"])

# 5) Join offerings with FIRST_DAY_OF_CLASSES via TERM_CODE
df = df.copy()
df["_term_code_key"] = df[term_key_offered].astype(str)
if "term_code" in terms_sel.columns:
    terms_sel = terms_sel.copy()
    terms_sel["_term_code_key"] = terms_sel["term_code"].astype(str)
else:
    terms_sel["_term_code_key"] = pd.Series(dtype="object")

df_merged = df.merge(
    terms_sel[["_term_code_key"] + [c for c in ["FIRST_DAY_OF_CLASSES", "ACADEMIC_YEAR"] if c in terms_sel.columns]],
    on="_term_code_key",
    how="left",
    suffixes=("", "_from_terms")
)

# Prefer ACADEMIC_YEAR from offerings if present; else from terms
if "ACADEMIC_YEAR" in df_merged.columns and "ACADEMIC_YEAR_from_terms" in df_merged.columns:
    df_merged["ACADEMIC_YEAR_final"] = df_merged["ACADEMIC_YEAR"].fillna(df_merged["ACADEMIC_YEAR_from_terms"])
elif "ACADEMIC_YEAR" in df_merged.columns:
    df_merged["ACADEMIC_YEAR_final"] = df_merged["ACADEMIC_YEAR"]
else:
    df_merged["ACADEMIC_YEAR_final"] = df_merged.get("ACADEMIC_YEAR_from_terms", pd.Series(index=df_merged.index, dtype="float"))

# Parse FIRST_DAY_OF_CLASSES to datetime
if "FIRST_DAY_OF_CLASSES" in df_merged.columns:
    df_merged["FIRST_DAY_OF_CLASSES_dt"] = pd.to_datetime(df_merged["FIRST_DAY_OF_CLASSES"], errors="coerce")
else:
    df_merged["FIRST_DAY_OF_CLASSES_dt"] = pd.NaT

# 6) Sort within each ACADEMIC_YEAR then by FIRST_DAY_OF_CLASSES_dt then course_name
sort_keys = ["ACADEMIC_YEAR_final", "FIRST_DAY_OF_CLASSES_dt", "course_name"]
existing_sort_keys = [k for k in sort_keys if k in df_merged.columns]
df_merged = df_merged.sort_values(existing_sort_keys).reset_index(drop=True)

# 6b) Compute cumulative number of courses within the same or preceding academic years (partitioned by academic year)
# Interpretation: for each academic year y, count all rows whose ACADEMIC_YEAR_final <= y up to and including the current row,
# ordered by FIRST_DAY_OF_CLASSES within year, and then accumulate across years for each building.
# We will first compute per-year cumulative count within each building, then cumulative sum across years for each building.

# Ensure ACADEMIC_YEAR_final is numeric or comparable for ordering
df_merged["ACADEMIC_YEAR_final_ord"] = pd.to_numeric(df_merged["ACADEMIC_YEAR_final"], errors="coerce")

# Per-year ordering within building by date then course_name for stability
group_keys_year_build = []
if "building_code" in df_merged.columns:
    group_keys_year_build.append("building_code")
if "ACADEMIC_YEAR_final_ord" in df_merged.columns:
    group_keys_year_build.append("ACADEMIC_YEAR_final_ord")

if group_keys_year_build:
    df_merged["per_year_seq"] = df_merged.groupby(group_keys_year_build, dropna=False).cumcount() + 1
else:
    df_merged["per_year_seq"] = np.nan

# Compute total counts per (building, year) to allow cumulative sum across years
counts_per_year = (
    df_merged.groupby(group_keys_year_build, dropna=False)["course_name"]
    .count()
    .reset_index()
    .rename(columns={"course_name": "year_total_count"})
)

# Sort year buckets and compute cumulative totals across years for each building
counts_per_year = counts_per_year.sort_values(group_keys_year_build)
if "building_code" in counts_per_year.columns and "ACADEMIC_YEAR_final_ord" in counts_per_year.columns:
    counts_per_year["cum_count_upto_year"] = counts_per_year.groupby("building_code", dropna=False)["year_total_count"].cumsum()
else:
    counts_per_year["cum_count_upto_year"] = counts_per_year["year_total_count"]

# Merge back to get the cumulative total up to the current academic year for each row
df_merged = df_merged.merge(
    counts_per_year[["building_code", "ACADEMIC_YEAR_final_ord", "cum_count_upto_year"]],
    on=["building_code", "ACADEMIC_YEAR_final_ord"],
    how="left"
)

# The desired cumulative number including the course itself, held in the same year or preceding years,
# ordered within the year by start date, is:
# cumulative up to previous years + position within the current year (per_year_seq)
df_merged["cumulative_courses_upto_and_in_year"] = (
    df_merged["cum_count_upto_year"] - df_merged["per_year_seq"] + 1
)

# 7) Select useful output columns: course name, building name/code, cumulative number
out_cols = []
candidate_cols = [
    "course_name",
    "building_code",
    "ACADEMIC_YEAR_final",
    "FIRST_DAY_OF_CLASSES_dt",
    "cumulative_courses_upto_and_in_year",
]
for c in candidate_cols:
    if c in df_merged.columns:
        out_cols.append(c)

final_df = df_merged[out_cols].rename(columns={
    "course_name": "course_name",
    "building_code": "building_name_or_code",
    "ACADEMIC_YEAR_final": "academic_year",
    "FIRST_DAY_OF_CLASSES_dt": "course_start_date",
    "cumulative_courses_upto_and_in_year": "cumulative_course_count_through_year"
})

# Sort output as described: partitioned by academic year and sorted by course start date ascending
sort_out = [c for c in ["academic_year", "course_start_date", "course_name"] if c in final_df.columns]
final_df = final_df.sort_values(sort_out).reset_index(drop=True)

# Assign to `result` dict as required
result = {
    "courses_building_cumulative_counts": final_df
}