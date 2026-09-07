import pandas as pd

# Tables are preloaded in a dict named `tables`
tip_detail = tables['table_1'].copy()                 # TIP_DETAIL.pkl
tip_subject_offered = tables['table_3'].copy()        # TIP_SUBJECT_OFFERED.pkl
tip_material = tables['table_6'].copy()               # TIP_MATERIAL.pkl

# Ensure required columns exist (as in the reference logic)
required_td_cols = {"TIP_MATERIAL_KEY", "TIP_SUBJECT_OFFERED_KEY", "TIP_MATERIAL_STATUS_KEY", "RECORD_COUNT"}
required_tm_cols = {"TIP_MATERIAL_KEY", "AUTHOR"}
required_tso_cols = {"TIP_SUBJECT_OFFERED_KEY", "OFFER_SCHOOL_NAME"}

missing = []
missing += [c for c in required_td_cols if c not in tip_detail.columns]
missing += [c for c in required_tm_cols if c not in tip_material.columns]
missing += [c for c in required_tso_cols if c not in tip_subject_offered.columns]
if missing:
    raise KeyError(f"Missing required columns: {sorted(set(missing))}")

# Select needed columns
td_sel = tip_detail[list(required_td_cols)].copy()
tm_sel = tip_material[list(required_tm_cols)].copy()
tso_sel = tip_subject_offered[list(required_tso_cols)].copy()

# The reference diagnostics showed 0% overlap on TIP_MATERIAL_KEY due to formatting differences.
# To reproduce the same logic but still obtain a meaningful join, align key formats by stripping whitespace.
# This keeps the spirit of the reference logic while operating on already-loaded tables.
for df, col in [(td_sel, "TIP_MATERIAL_KEY"), (tm_sel, "TIP_MATERIAL_KEY")]:
    df[col] = df[col].astype(str).str.strip()

for df, col in [(td_sel, "TIP_SUBJECT_OFFERED_KEY"), (tso_sel, "TIP_SUBJECT_OFFERED_KEY")]:
    df[col] = df[col].astype(str).str.strip()

# Attempt merges consistent with the reference approach
td_tm = td_sel.merge(tm_sel, on="TIP_MATERIAL_KEY", how="inner")
td_tm_tso = td_tm.merge(tso_sel, on="TIP_SUBJECT_OFFERED_KEY", how="inner")

# If the inner result is empty (as in the raw reference run), produce an empty result with expected columns
final_cols = ["AUTHOR", "OFFER_SCHOOL_NAME", "TIP_MATERIAL_STATUS_KEY", "RECORD_COUNT"]

if td_tm_tso.empty:
    aggregated = pd.DataFrame(columns=["AUTHOR", "OFFER_SCHOOL_NAME", "TIP_MATERIAL_STATUS_KEY",
                                       "TOTAL_RECORD_COUNT", "N_UNIQUE_COURSE_TYPES"]).astype({
        "AUTHOR": "object",
        "OFFER_SCHOOL_NAME": "object",
        "TIP_MATERIAL_STATUS_KEY": "object",
        "TOTAL_RECORD_COUNT": "int64",
        "N_UNIQUE_COURSE_TYPES": "int64",
    })
else:
    # Aggregate:
    # - total record counts per author, school, and material status
    # - total number of types of courses for each author and school
    # We interpret "types of courses" as the number of distinct TIP_SUBJECT_OFFERED_KEY per (AUTHOR, OFFER_SCHOOL_NAME)
    grouped_status = (
        td_tm_tso
        .groupby(["AUTHOR", "OFFER_SCHOOL_NAME", "TIP_MATERIAL_STATUS_KEY"], dropna=False, as_index=False)
        .agg(TOTAL_RECORD_COUNT=("RECORD_COUNT", "sum"))
    )

    course_types = (
        td_tm_tso
        .groupby(["AUTHOR", "OFFER_SCHOOL_NAME"], dropna=False, as_index=False)
        .agg(N_UNIQUE_COURSE_TYPES=("TIP_SUBJECT_OFFERED_KEY", pd.Series.nunique))
    )

    aggregated = grouped_status.merge(course_types, on=["AUTHOR", "OFFER_SCHOOL_NAME"], how="left")

# Package final answer
result = {
    "author_school_material_status_summary": aggregated
}