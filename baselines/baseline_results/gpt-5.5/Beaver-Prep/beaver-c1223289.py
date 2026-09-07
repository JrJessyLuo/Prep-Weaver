import pandas as pd

def _series(df, col, default=pd.NA):
    if col in df.columns:
        return df[col]
    return pd.Series(default, index=df.index)

def norm_text(s):
    return s.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)

def norm_name(s):
    return norm_text(s).str.casefold()

def norm_id(s):
    return pd.to_numeric(s, errors="coerce").astype("Int64").astype("string")

def norm_key(s):
    return s.astype("string").str.strip().str.upper()

def year_from_term(s):
    return pd.to_numeric(s.astype("string").str.extract(r"(\d{4})", expand=False), errors="coerce").astype("Int64")

def first_non_null(vals):
    vals = [str(v).strip() for v in vals if pd.notna(v) and str(v).strip()]
    return sorted(set(vals))[0] if vals else pd.NA

def unique_list(vals):
    vals = [str(v).strip() for v in vals if pd.notna(v) and str(v).strip()]
    return ", ".join(sorted(set(vals)))

final_cols = [
    "mailing_lists_subscribed_to",
    "instructor_name",
    "earliest_publication_year",
    "latest_publication_year",
    "total_number_of_enrolled_students",
]

moira = tables["table_6"].copy()
moira["MOIRA_LIST_KEY_clean"] = norm_text(_series(moira, "MOIRA_LIST_KEY"))
moira["list_norm"] = moira["MOIRA_LIST_KEY_clean"].str.casefold()
moira["name_norm"] = norm_name(_series(moira, "MOIRA_LIST_MEMBER_FULL_NAME"))
moira["mit_id_norm"] = norm_id(_series(moira, "MOIRA_LIST_MEMBER_MIT_ID"))

name_to_id = (
    moira.loc[moira["name_norm"].notna() & moira["mit_id_norm"].notna(), ["name_norm", "mit_id_norm"]]
    .drop_duplicates(["name_norm", "mit_id_norm"])
    .sort_values(["name_norm", "mit_id_norm"])
    .drop_duplicates("name_norm")
    .set_index("name_norm")["mit_id_norm"]
)

moira["mit_id_filled"] = moira["mit_id_norm"].fillna(moira["name_norm"].map(name_to_id))
moira["person_key"] = pd.Series(pd.NA, index=moira.index, dtype="string")
moira.loc[moira["mit_id_filled"].notna(), "person_key"] = "ID:" + moira.loc[moira["mit_id_filled"].notna(), "mit_id_filled"]
moira.loc[moira["person_key"].isna() & moira["name_norm"].notna(), "person_key"] = "NAME:" + moira.loc[moira["person_key"].isna() & moira["name_norm"].notna(), "name_norm"]

keeper_people = (
    moira.loc[
        moira["list_norm"].eq("keeper-zephyr") & moira["name_norm"].notna() & moira["person_key"].notna(),
        ["person_key", "name_norm", "mit_id_filled", "MOIRA_LIST_MEMBER_FULL_NAME"],
    ]
    .drop_duplicates()
)

if keeper_people.empty:
    answer = pd.DataFrame(columns=final_cols)
else:
    subscriptions = (
        moira.loc[moira["person_key"].isin(keeper_people["person_key"])]
        .groupby("person_key", as_index=False)
        .agg(mailing_lists_subscribed_to=("MOIRA_LIST_KEY_clean", unique_list))
    )

    enroll_frames = []
    for tname in ["table_2", "table_3", "table_4", "table_5"]:
        if tname in tables:
            df = tables[tname].copy()
            term_col = "TERM_CODE" if "TERM_CODE" in df.columns else ("term_code" if "term_code" in df.columns else None)
            key_col = "LIBRARY_SUBJECT_OFFERED_KEY" if "LIBRARY_SUBJECT_OFFERED_KEY" in df.columns else None
            if term_col is not None and "SUBJECT_ID" in df.columns and "NUM_ENROLLED_STUDENTS" in df.columns:
                tmp = pd.DataFrame(index=df.index)
                tmp["library_key_norm"] = norm_key(_series(df, key_col)) if key_col is not None else pd.Series(pd.NA, index=df.index, dtype="string")
                tmp["subject_norm"] = norm_key(_series(df, "SUBJECT_ID"))
                tmp["term_norm"] = norm_key(_series(df, term_col))
                tmp["enrolled_students"] = pd.to_numeric(_series(df, "NUM_ENROLLED_STUDENTS"), errors="coerce")
                enroll_frames.append(tmp.reset_index(drop=True))

    if enroll_frames:
        enroll_all = pd.concat(enroll_frames, ignore_index=True)
    else:
        enroll_all = pd.DataFrame(columns=["library_key_norm", "subject_norm", "term_norm", "enrolled_students"])

    enroll_by_key = (
        enroll_all.loc[enroll_all["library_key_norm"].notna()]
        .groupby("library_key_norm", as_index=False)
        .agg(enrollment_by_key=("enrolled_students", "max"))
    )

    enroll_by_subject_term = (
        enroll_all.loc[enroll_all["subject_norm"].notna() & enroll_all["term_norm"].notna()]
        .groupby(["subject_norm", "term_norm"], as_index=False)
        .agg(enrollment_by_subject_term=("enrolled_students", "max"))
    )

    if "table_9" in tables:
        catalog = tables["table_9"].copy()
        catalog["subject_norm"] = norm_key(_series(catalog, "SO_SUBJECT_ID")).fillna(norm_key(_series(catalog, "SUBJECT_ID")))
        catalog["term_norm"] = norm_key(_series(catalog, "SO_TERM_CODE")).fillna(norm_key(_series(catalog, "EFFECTIVE_TERM_CODE")))
        catalog["catalog_publication_year"] = pd.to_numeric(_series(catalog, "ACADEMIC_YEAR"), errors="coerce").astype("Int64")
        catalog_years = (
            catalog.loc[
                catalog["subject_norm"].notna() & catalog["term_norm"].notna() & catalog["catalog_publication_year"].notna(),
                ["subject_norm", "term_norm", "catalog_publication_year"],
            ]
            .drop_duplicates()
            .groupby(["subject_norm", "term_norm"], as_index=False)
            .agg(catalog_publication_year=("catalog_publication_year", "min"))
        )
    else:
        catalog_years = pd.DataFrame(columns=["subject_norm", "term_norm", "catalog_publication_year"])

    ci = tables["table_1"].copy()
    ci["name_norm"] = norm_name(_series(ci, "INSTRUCTOR_NAME"))
    ci["instructor_name"] = norm_text(_series(ci, "INSTRUCTOR_NAME"))

    ci_keeper = ci.merge(
        keeper_people[["person_key", "name_norm"]].drop_duplicates(),
        on="name_norm",
        how="inner",
    )

    if ci_keeper.empty:
        answer = pd.DataFrame(columns=final_cols)
    else:
        course_key_text = _series(ci_keeper, "LIBRARY_COURSE_INSTRUCTOR_KEY").astype("string")
        ci_keeper["parsed_subject_norm"] = norm_key(course_key_text.str.extract(r":\s*([^:]+)\s*$", expand=False))
        ci_keeper["parsed_term_norm"] = norm_key(course_key_text.str.extract(r"(\d{4}[A-Za-z]{2})", expand=False))
        ci_keeper["date_year"] = pd.to_datetime(_series(ci_keeper, "DATE_FROM"), errors="coerce", format="%d-%b-%y").dt.year.astype("Int64")

        if "table_7" in tables:
            reserves = tables["table_7"].copy()
            lib_records = ci_keeper.merge(
                reserves,
                on="LIBRARY_COURSE_INSTRUCTOR_KEY",
                how="left",
                suffixes=("", "_reserve"),
            )
        else:
            lib_records = ci_keeper.copy()
            lib_records["LIBRARY_SUBJECT_OFFERED_KEY"] = pd.Series(pd.NA, index=lib_records.index, dtype="string")
            lib_records["TERM_CODE"] = pd.Series(pd.NA, index=lib_records.index, dtype="string")
            lib_records["SUBJECT_ID"] = pd.Series(pd.NA, index=lib_records.index, dtype="string")

        lib_records["library_key_norm"] = norm_key(_series(lib_records, "LIBRARY_SUBJECT_OFFERED_KEY"))
        lib_records["subject_norm"] = norm_key(_series(lib_records, "SUBJECT_ID")).fillna(lib_records["parsed_subject_norm"])
        lib_records["term_norm"] = norm_key(_series(lib_records, "TERM_CODE")).fillna(lib_records["parsed_term_norm"])

        offerings = lib_records[
            [
                "person_key",
                "instructor_name",
                "LIBRARY_COURSE_INSTRUCTOR_KEY",
                "library_key_norm",
                "subject_norm",
                "term_norm",
                "date_year",
            ]
        ].drop_duplicates()

        offerings = offerings.merge(enroll_by_key, on="library_key_norm", how="left")
        offerings = offerings.merge(enroll_by_subject_term, on=["subject_norm", "term_norm"], how="left")
        offerings = offerings.merge(catalog_years, on=["subject_norm", "term_norm"], how="left")

        offerings["publication_year"] = offerings["catalog_publication_year"].astype("Int64")
        offerings["publication_year"] = offerings["publication_year"].fillna(year_from_term(offerings["term_norm"]))
        offerings["publication_year"] = offerings["publication_year"].fillna(offerings["date_year"].astype("Int64"))

        offerings["enrolled_students"] = offerings["enrollment_by_key"].fillna(offerings["enrollment_by_subject_term"])
        offerings["enrolled_students"] = pd.to_numeric(offerings["enrolled_students"], errors="coerce").fillna(0)

        agg = (
            offerings.groupby(["person_key", "instructor_name"], as_index=False)
            .agg(
                earliest_publication_year=("publication_year", "min"),
                latest_publication_year=("publication_year", "max"),
                total_number_of_enrolled_students=("enrolled_students", "sum"),
            )
        )

        answer = (
            agg.merge(subscriptions, on="person_key", how="left")
            [
                [
                    "mailing_lists_subscribed_to",
                    "instructor_name",
                    "earliest_publication_year",
                    "latest_publication_year",
                    "total_number_of_enrolled_students",
                ]
            ]
            .sort_values(["instructor_name", "mailing_lists_subscribed_to"], kind="mergesort")
            .reset_index(drop=True)
        )

        answer["total_number_of_enrolled_students"] = (
            pd.to_numeric(answer["total_number_of_enrolled_students"], errors="coerce").fillna(0).astype("Int64")
        )
        answer["earliest_publication_year"] = answer["earliest_publication_year"].astype("Int64")
        answer["latest_publication_year"] = answer["latest_publication_year"].astype("Int64")

result = {"keeper_zephyr_course_instructors": answer}
