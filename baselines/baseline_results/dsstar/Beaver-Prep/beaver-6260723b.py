import pandas as pd

# ---------------------------
# Access already-loaded tables
# ---------------------------
academic_terms_all = tables['table_5'].copy()
tip_subject_offered = tables['table_6'].copy()
subject_enrollable = tables['table_2'].copy()
cis = tables['table_3'].copy()
drupal = tables['table_4'].copy()

# Standardize column names to string
academic_terms_all.columns = [str(c) for c in academic_terms_all.columns]
tip_subject_offered.columns = [str(c) for c in tip_subject_offered.columns]
subject_enrollable.columns = [str(c) for c in subject_enrollable.columns]
cis.columns = [str(c) for c in cis.columns]
drupal.columns = [str(c) for c in drupal.columns]

# ---------------------------
# Determine 2023 Fall term code (replicate reference logic)
# ---------------------------
df = academic_terms_all.copy()
candidate_mask = df["term_code"].astype(str).str.contains("2023", na=False)
candidates = df.loc[candidate_mask, ["term_code", "TERM_DESCRIPTION"]].drop_duplicates().sort_values("term_code")

preferred_codes = ["2023FA", "2023FALL", "2023-FALL", "2023 Fall", "2023SEP", "2023-FA"]
fall_mask = df["TERM_DESCRIPTION"].astype(str).str.contains("Fall", case=False, na=False) & df["ACADEMIC_YEAR"].astype(str).str.contains("2023", na=False)
filtered_exact = df[df["term_code"].isin(preferred_codes)]
filtered_fall = df[fall_mask]

if not filtered_exact.empty:
    result_term = filtered_exact[["term_code", "TERM_DESCRIPTION", "TERM_START_DATE", "TERM_END_DATE"]].drop_duplicates()
else:
    tmp = filtered_fall.copy()
    for col in ["TERM_START_DATE", "TERM_END_DATE"]:
        if col in tmp.columns:
            tmp[col] = pd.to_datetime(tmp[col], errors="coerce")
    mask_2023_by_date = tmp["TERM_START_DATE"].dt.year.eq(2023)
    if mask_2023_by_date.any():
        tmp = tmp[mask_2023_by_date]
    elif "ACADEMIC_YEAR" in tmp.columns:
        tmp = tmp[tmp["ACADEMIC_YEAR"].astype(str).str.contains("2023", na=False)]
    if "TERM_START_DATE" in tmp.columns and tmp["TERM_START_DATE"].notna().any():
        tmp = tmp.sort_values("TERM_START_DATE")
    result_term = tmp[["term_code", "TERM_DESCRIPTION", "TERM_START_DATE", "TERM_END_DATE"]].drop_duplicates()

if result_term.empty:
    raise ValueError("Could not determine 2023 Fall term code from ACADEMIC_TERMS_ALL")

term_code_2023_fall = result_term.iloc[0]["term_code"]

# ---------------------------
# Part 1: Filter TIP_SUBJECT_OFFERED for Fall 2023 and aggregate
# ---------------------------
tip = tip_subject_offered.copy()
needed_cols = ["TERM_CODE", "SUBJECT_TITLE", "RESPONSIBLE_FACULTY_NAME", "COURSE_NUMBER_DESC", "SUBJECT_ID"]
missing = [c for c in needed_cols if c not in tip.columns]
if missing:
    raise KeyError(f"TIP_SUBJECT_OFFERED missing expected columns: {missing}")

tip_fall = tip[tip["TERM_CODE"].astype(str) == str(term_code_2023_fall)].copy()

agg_per_term = tip_fall.groupby("TERM_CODE").agg(
    unique_subject_titles=("SUBJECT_TITLE", lambda s: sorted(set([x for x in s.dropna().astype(str).unique()]))),
    unique_instructors=("RESPONSIBLE_FACULTY_NAME", lambda s: sorted(set([x for x in s.dropna().astype(str).unique()]))),
    distinct_course_number_desc_count=("COURSE_NUMBER_DESC", lambda s: s.dropna().astype(str).nunique()),
    subjects_count=("SUBJECT_ID", "nunique")
).reset_index()

# ---------------------------
# Part 2: Join prerequisites from DRUPAL or CIS
# ---------------------------
def find_prereq_column(columns):
    cands = [c for c in columns if "PREREQ" in c.upper() or "PREREQUISITE" in c.upper()]
    cands_sorted = sorted(cands, key=lambda x: (len(x), x))
    return cands_sorted[0] if cands_sorted else None

drupal_prereq_col = find_prereq_column(drupal.columns)
cis_prereq_col = find_prereq_column(cis.columns)

drupal_key = "SUBJECT_ID" if "SUBJECT_ID" in drupal.columns else None
cis_key = "subject_id" if "subject_id" in cis.columns else None

prereq_lookup = None
if drupal_prereq_col and drupal_key:
    if "TERM_CODE" in drupal.columns:
        drupal_subset = drupal[[drupal_key, "TERM_CODE", drupal_prereq_col]].copy()
        drupal_subset = drupal_subset[drupal_subset["TERM_CODE"].astype(str) == str(term_code_2023_fall)]
    else:
        drupal_subset = drupal[[drupal_key, drupal_prereq_col]].copy()
    drupal_subset = drupal_subset.sort_values(by=[drupal_key]).drop_duplicates(subset=[drupal_key], keep="first")
    prereq_lookup = drupal_subset.rename(columns={drupal_key: "SUBJECT_ID", drupal_prereq_col: "PREREQUISITES"})
elif cis_prereq_col and cis_key:
    if "EFFECTIVE_TERM_CODE" in cis.columns:
        cis_subset = cis[[cis_key, "EFFECTIVE_TERM_CODE", cis_prereq_col]].copy()
        cis_subset["EFFECTIVE_TERM_CODE_STR"] = cis_subset["EFFECTIVE_TERM_CODE"].astype(str)
        cis_subset = cis_subset.sort_values(by=[cis_key, "EFFECTIVE_TERM_CODE_STR"]).drop_duplicates(subset=[cis_key], keep="last")
        cis_subset = cis_subset.drop(columns=["EFFECTIVE_TERM_CODE_STR"])
    else:
        cis_subset = cis[[cis_key, cis_prereq_col]].copy()
    prereq_lookup = cis_subset.rename(columns={cis_key: "SUBJECT_ID", cis_prereq_col: "PREREQUISITES"})

tip_with_prereq = tip_fall.copy()
if prereq_lookup is not None:
    tip_with_prereq = tip_with_prereq.merge(
        prereq_lookup[["SUBJECT_ID", "PREREQUISITES"]],
        on="SUBJECT_ID",
        how="left"
    )
else:
    tip_with_prereq["PREREQUISITES"] = pd.NA

# ---------------------------
# Part 3: Instructor distinct COURSE_NUMBER_DESC across all terms
# ---------------------------
instructor_counts_all_terms = (
    tip_subject_offered
    .dropna(subset=["RESPONSIBLE_FACULTY_NAME"])
    .assign(
        RESPONSIBLE_FACULTY_NAME=lambda d: d["RESPONSIBLE_FACULTY_NAME"].astype(str).str.strip(),
        COURSE_NUMBER_DESC=lambda d: d["COURSE_NUMBER_DESC"].astype(str)
    )
    .groupby("RESPONSIBLE_FACULTY_NAME")["COURSE_NUMBER_DESC"]
    .nunique(dropna=True)
    .reset_index(name="distinct_course_number_desc_across_all_terms")
)

# ---------------------------
# Build final answer tables per the question
# ---------------------------
# 1) Unique term descriptions for Fall 2023
unique_term_descriptions = (
    academic_terms_all.loc[academic_terms_all["term_code"].astype(str) == str(term_code_2023_fall), ["term_code", "TERM_DESCRIPTION"]]
    .drop_duplicates()
    .rename(columns={"term_code": "TERM_CODE"})
)

# 2) Subject titles with prerequisites and instructor (Fall 2023)
subjects_with_prereq_and_instructor = tip_with_prereq[[
    "TERM_CODE", "SUBJECT_ID", "SUBJECT_TITLE", "COURSE_NUMBER_DESC", "RESPONSIBLE_FACULTY_NAME", "PREREQUISITES"
]].copy()

# 3) Total number of types of subjects per term code (distinct COURSE_NUMBER_DESC) for Fall 2023
types_per_term = agg_per_term[["TERM_CODE", "distinct_course_number_desc_count"]].copy()

# 4) Instructor and number of types of courses ever taught by the instructor (join onto Fall 2023 subjects)
instructor_course_types = (
    subjects_with_prereq_and_instructor[["RESPONSIBLE_FACULTY_NAME"]]
    .drop_duplicates()
    .merge(instructor_counts_all_terms, on="RESPONSIBLE_FACULTY_NAME", how="left")
)

# Package final results
result = {
    "unique_term_descriptions_fall_2023": unique_term_descriptions.reset_index(drop=True),
    "subjects_with_prerequisites_fall_2023": subjects_with_prereq_and_instructor.reset_index(drop=True),
    "types_of_subjects_count_per_term_fall_2023": types_per_term.reset_index(drop=True),
    "instructor_course_type_counts_all_terms": instructor_course_types.reset_index(drop=True),
}