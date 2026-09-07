import pandas as pd

# Input tables already loaded in `tables`
tip_detail = tables['table_1']
subject_offered = tables['table_2'] if 'table_2' in tables else pd.DataFrame()
tip_subject_offered = tables['table_3']
subject_offered_summary = tables['table_4'] if 'table_4' in tables else pd.DataFrame()
library_subject_offered = tables['table_5'] if 'table_5' in tables else pd.DataFrame()
course_catalog_so = tables['table_6']
subject_enrollable = tables['table_7'] if 'table_7' in tables else pd.DataFrame()
library_reserve_matrl_detail = tables['table_8'] if 'table_8' in tables else pd.DataFrame()
iap_subject_detail = tables['table_9'] if 'table_9' in tables else pd.DataFrame()

# Validate required columns analogous to the reference logic
required_tso_cols = {"TERM_CODE", "NUM_ENROLLED_STUDENTS", "OFFER_SCHOOL_NAME"}
missing_tso = required_tso_cols - set(tip_subject_offered.columns)
if missing_tso:
    raise ValueError(f"TIP_SUBJECT_OFFERED missing required columns: {missing_tso}")

required_tipd_cols = {"TERM_CODE", "RECORD_COUNT"}
missing_tipd = required_tipd_cols - set(tip_detail.columns)
if missing_tipd:
    raise ValueError(f"TIP_DETAIL missing required columns: {missing_tipd}")

required_cc_cols = {"TERM_CODE", "ACADEMIC_YEAR"}
missing_cc = required_cc_cols - set(course_catalog_so.columns)
if missing_cc:
    raise ValueError(f"COURSE_CATALOG_SUBJECT_OFFERED missing required columns: {missing_cc}")

# Create term-level aggregates from TIP_SUBJECT_OFFERED
tso_term_agg = (
    tip_subject_offered.groupby("TERM_CODE", dropna=False).agg(
        min_num_enrolled_students=("NUM_ENROLLED_STUDENTS", "min"),
        max_num_enrolled_students=("NUM_ENROLLED_STUDENTS", "max"),
        distinct_offer_school_name_count=("OFFER_SCHOOL_NAME", pd.Series.nunique),
        tso_row_count=("TERM_CODE", "size"),
    )
    .reset_index()
)

# Create term-level aggregates from TIP_DETAIL
tipd_term_agg = (
    tip_detail.groupby("TERM_CODE", dropna=False).agg(
        tip_detail_total_record_count=("RECORD_COUNT", "sum"),
        tip_detail_row_count=("TERM_CODE", "size"),
    )
    .reset_index()
)

# Join the two term-level aggregates
term_level_base = tso_term_agg.merge(tipd_term_agg, on="TERM_CODE", how="outer")

# Helper: derive season text from TERM_CODE suffix if possible
def derive_season(term_code: str) -> str:
    if not isinstance(term_code, str) or len(term_code) < 2:
        return ""
    suffix = term_code[-2:].upper()
    mapping = {
        "FA": "Fall",
        "SP": "Spring",
        "SU": "Summer",
        "JA": "IAP",
        "WI": "Winter",
    }
    return mapping.get(suffix, suffix)

# Build TERM_DESC lookup
candidate_desc_cols = [c for c in ["TERM_DESC", "TERM_DESCRIPTION", "TERM_NAME"] if c in course_catalog_so.columns]
if candidate_desc_cols:
    desc_col = candidate_desc_cols[0]
    term_lookup = (
        course_catalog_so.sort_values([desc_col])
        .groupby("TERM_CODE", as_index=False, dropna=False)
        .agg(
            ACADEMIC_YEAR=("ACADEMIC_YEAR", "max"),
            TERM_DESC=(desc_col, "first"),
        )
    )
else:
    tmp = course_catalog_so[["TERM_CODE", "ACADEMIC_YEAR"]].copy()
    tmp["SEASON"] = tmp["TERM_CODE"].astype(str).map(derive_season)
    def _mk_desc(row):
        ay = row["ACADEMIC_YEAR"]
        season = row["SEASON"]
        if pd.notna(ay):
            try:
                return f"{int(ay)} {season}".strip()
            except Exception:
                return f"{ay} {season}".strip()
        return f"{season}".strip()
    tmp["TERM_DESC"] = tmp.apply(_mk_desc, axis=1)
    term_lookup = (
        tmp.groupby("TERM_CODE", as_index=False, dropna=False)
        .agg(
            ACADEMIC_YEAR=("ACADEMIC_YEAR", "max"),
            TERM_DESC=("TERM_DESC", "first"),
        )
    )

# Determine current term as max TERM_CODE in COURSE_CATALOG_SUBJECT_OFFERED
max_term_code = (
    course_catalog_so["TERM_CODE"].dropna().astype(str).max()
    if not course_catalog_so["TERM_CODE"].dropna().empty
    else None
)
term_lookup["IS_CURRENT_TERM"] = term_lookup["TERM_CODE"].astype(str).eq(str(max_term_code)).astype("boolean")

# Merge term metadata
term_level_base = term_level_base.merge(term_lookup, on="TERM_CODE", how="left")

# Prepare final answer columns per question:
# - term description (TERM_DESC)
# - whether the term is current (IS_CURRENT_TERM)
# - total number of types of TIP subjects offered (we interpret as distinct OFFER_SCHOOL_NAME already computed, plus also include tso_row_count for completeness)
# - materials needed (tip_detail_total_record_count)
# - min and max enrolled students
# - total number of schools offering subjects (distinct_offer_school_name_count)
# - total number of records for each term code (tip_detail_total_record_count)
final_cols = [
    "TERM_CODE",
    "TERM_DESC",
    "IS_CURRENT_TERM",
    "tso_row_count",  # total number of types of TIP subjects offered (rows)
    "distinct_offer_school_name_count",  # total number of schools offering subjects
    "min_num_enrolled_students",
    "max_num_enrolled_students",
    "tip_detail_total_record_count",  # materials needed / total records
]

final_df = term_level_base[final_cols].sort_values(by="TERM_CODE", kind="stable").reset_index(drop=True)

# Package result
result = {
    "term_level_summary": final_df
}