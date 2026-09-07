import pandas as pd

# Use the historical subject catalog; normalize the subject id column name.
subjects = tables["table_2"].copy()
subjects = subjects.rename(columns={"subject_id": "SUBJECT_ID"})

# Count each subject only once, in the first effective term in which it appears.
introduced = (
    subjects[["SUBJECT_ID", "EFFECTIVE_TERM_CODE"]]
    .dropna(subset=["SUBJECT_ID", "EFFECTIVE_TERM_CODE"])
    .drop_duplicates()
    .sort_values(["SUBJECT_ID", "EFFECTIVE_TERM_CODE"])
    .drop_duplicates(subset=["SUBJECT_ID"], keep="first")
    .rename(columns={"EFFECTIVE_TERM_CODE": "TERM_CODE"})
)

# Map term codes to academic years.
terms = tables["table_5"][["term_code", "ACADEMIC_YEAR"]].drop_duplicates()
terms = terms.rename(columns={"term_code": "TERM_CODE"})

summary = (
    introduced.merge(terms, on="TERM_CODE", how="left")
    .dropna(subset=["ACADEMIC_YEAR"])
    .groupby(["ACADEMIC_YEAR", "TERM_CODE"], as_index=False)
    .agg(NUM_NEWLY_INTRODUCED_SUBJECTS=("SUBJECT_ID", "nunique"))
)

summary["ACADEMIC_YEAR"] = summary["ACADEMIC_YEAR"].astype(int)
summary = summary.sort_values(["ACADEMIC_YEAR", "TERM_CODE"]).reset_index(drop=True)

# Display the academic year only when it differs from the previous row.
display_summary = summary.copy()
display_summary["ACADEMIC_YEAR"] = display_summary["ACADEMIC_YEAR"].astype(object)
display_summary.loc[
    display_summary["ACADEMIC_YEAR"].eq(display_summary["ACADEMIC_YEAR"].shift()),
    "ACADEMIC_YEAR"
] = ""

# Add grand total row.
total_row = pd.DataFrame([{
    "ACADEMIC_YEAR": "TOTAL",
    "TERM_CODE": "",
    "NUM_NEWLY_INTRODUCED_SUBJECTS": summary["NUM_NEWLY_INTRODUCED_SUBJECTS"].sum()
}])

final_df = pd.concat([display_summary, total_row], ignore_index=True)

result = {
    "newly_introduced_subjects_by_term": final_df
}
