import pandas as pd

terms = tables["table_8"].copy()
terms["term_code_norm"] = terms["term_code"].astype(str).str.strip().str.upper()
terms["is_current_norm"] = terms["IS_CURRENT_TERM"].astype(str).str.strip().str.upper()

current_terms = terms.loc[terms["is_current_norm"].eq("Y"), "term_code_norm"].dropna().unique()

offered = tables["table_4"].copy()
offered["TERM_CODE"] = offered["TERM_CODE"].astype(str).str.strip().str.upper()
offered = offered[offered["TERM_CODE"].isin(current_terms)].copy()

offered["ACADEMIC_YEAR"] = pd.to_numeric(
    offered["TERM_CODE"].str.extract(r"^(\d{4})", expand=False),
    errors="coerce"
).astype("Int64")

offered["TOTAL_UNITS"] = pd.to_numeric(offered["TOTAL_UNITS"], errors="coerce")
offered["RESPONSIBLE_FACULTY_MIT_ID_INT"] = pd.to_numeric(
    offered["RESPONSIBLE_FACULTY_MIT_ID"], errors="coerce"
).round().astype("Int64")

dedup_cols = ["SUBJECT_OFFERED_SUMMARY_KEY"] if "SUBJECT_OFFERED_SUMMARY_KEY" in offered.columns else [
    "TERM_CODE", "SUBJECT_ID", "HGN_CODE", "OFFER_DEPT_NAME", "RESPONSIBLE_FACULTY_MIT_ID_INT"
]
offered = offered.drop_duplicates(subset=dedup_cols)

directory = tables["table_9"].copy()
directory["MIT_ID_INT"] = pd.to_numeric(directory["MIT_ID"], errors="coerce").astype("Int64")
directory = (
    directory[["MIT_ID_INT", "EMAIL_ADDRESS"]]
    .dropna(subset=["MIT_ID_INT"])
    .drop_duplicates(subset=["MIT_ID_INT"])
)

offered = offered.merge(
    directory,
    how="left",
    left_on="RESPONSIBLE_FACULTY_MIT_ID_INT",
    right_on="MIT_ID_INT"
)

result_df = (
    offered
    .groupby(
        [
            "ACADEMIC_YEAR",
            "TERM_CODE",
            "HGN_CODE",
            "OFFER_DEPT_NAME",
            "RESPONSIBLE_FACULTY_NAME",
            "EMAIL_ADDRESS",
        ],
        dropna=False,
        as_index=False
    )
    .agg(
        total_number_of_course_types=("SUBJECT_ID", lambda s: s.dropna().astype(str).nunique()),
        average_number_of_units=("TOTAL_UNITS", "mean")
    )
    .rename(columns={
        "ACADEMIC_YEAR": "academic_year",
        "TERM_CODE": "term_code",
        "HGN_CODE": "hgn_code",
        "OFFER_DEPT_NAME": "department_name",
        "RESPONSIBLE_FACULTY_NAME": "person_in_charge_name",
        "EMAIL_ADDRESS": "person_in_charge_email_address",
    })
)

result_df = result_df[
    [
        "academic_year",
        "term_code",
        "hgn_code",
        "total_number_of_course_types",
        "average_number_of_units",
        "department_name",
        "person_in_charge_name",
        "person_in_charge_email_address",
    ]
].sort_values(
    ["academic_year", "term_code", "hgn_code", "department_name", "person_in_charge_name"],
    na_position="last"
).reset_index(drop=True)

result = {"current_term_course_details": result_df}
