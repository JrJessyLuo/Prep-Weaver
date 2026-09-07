import pandas as pd
import numpy as np

def clean_str(s):
    return s.astype("string").str.strip().replace("", pd.NA)

def normalize_material_key(s):
    return (
        clean_str(s)
        .str.replace(r"(?:20\d{2}(?:FA|SP|JA|SU))$", "", regex=True)
        .str.strip()
        .replace("", pd.NA)
    )

# Fact table: TIP subject-material relationships
fact = tables["table_2"].copy()
fact["subject_offered_key_norm"] = clean_str(fact["TIP_SUBJECT_OFFERED_KEY"])
fact["material_key_norm"] = normalize_material_key(fact["TIP_MATERIAL_KEY"])
fact["status_key_norm"] = clean_str(fact["TIP_MATERIAL_STATUS_KEY"])
fact["term_code_norm"] = clean_str(fact["TERM_CODE"]).str.upper()
fact["subject_id_norm"] = clean_str(fact["subject_id"])
fact["RECORD_COUNT"] = pd.to_numeric(fact["RECORD_COUNT"], errors="coerce").fillna(1)

# TIP subject offered dimension
sub = tables["table_3"].copy()
sub["subject_offered_key_norm"] = clean_str(sub["TIP_SUBJECT_OFFERED_KEY"])
sub["term_code_norm"] = clean_str(sub["TERM_CODE"]).str.upper()
sub["subject_id_norm"] = clean_str(sub["SUBJECT_ID"])
sub["COURSE_NUMBER"] = clean_str(sub["COURSE_NUMBER"])
sub["SUBJECT_TITLE"] = clean_str(sub["SUBJECT_TITLE"])
sub["OFFER_SCHOOL_NAME"] = clean_str(sub["OFFER_SCHOOL_NAME"])

sub_sorted = sub.sort_values(["term_code_norm"], ascending=False, na_position="last")

sub_by_key = (
    sub_sorted.dropna(subset=["subject_offered_key_norm"])
    .drop_duplicates("subject_offered_key_norm")
    [["subject_offered_key_norm", "COURSE_NUMBER", "SUBJECT_TITLE", "OFFER_SCHOOL_NAME"]]
)

sub_by_subterm = (
    sub_sorted.dropna(subset=["subject_id_norm", "term_code_norm"])
    .drop_duplicates(["subject_id_norm", "term_code_norm"])
    [["subject_id_norm", "term_code_norm", "COURSE_NUMBER", "SUBJECT_TITLE", "OFFER_SCHOOL_NAME"]]
    .rename(columns={
        "COURSE_NUMBER": "COURSE_NUMBER_st",
        "SUBJECT_TITLE": "SUBJECT_TITLE_st",
        "OFFER_SCHOOL_NAME": "OFFER_SCHOOL_NAME_st"
    })
)

sub_by_sub = (
    sub_sorted.dropna(subset=["subject_id_norm"])
    .drop_duplicates("subject_id_norm")
    [["subject_id_norm", "COURSE_NUMBER", "SUBJECT_TITLE", "OFFER_SCHOOL_NAME"]]
    .rename(columns={
        "COURSE_NUMBER": "COURSE_NUMBER_ss",
        "SUBJECT_TITLE": "SUBJECT_TITLE_ss",
        "OFFER_SCHOOL_NAME": "OFFER_SCHOOL_NAME_ss"
    })
)

df = fact.merge(sub_by_key, on="subject_offered_key_norm", how="left")
df = df.merge(sub_by_subterm, on=["subject_id_norm", "term_code_norm"], how="left")
df = df.merge(sub_by_sub, on="subject_id_norm", how="left")

for col in ["COURSE_NUMBER", "SUBJECT_TITLE", "OFFER_SCHOOL_NAME"]:
    df[col] = df[col].combine_first(df[f"{col}_st"]).combine_first(df[f"{col}_ss"])

# Additional subject/catalog fallback
cat = tables["table_10"].copy()
cat["subject_id_norm"] = clean_str(cat["subject_id"])
cat["COURSE_NUMBER_cat"] = clean_str(cat["SUBJECT_CODE"])
cat["SUBJECT_TITLE_cat"] = clean_str(cat["SUBJECT_TITLE"])

cat_sort_cols = [c for c in ["ACADEMIC_YEAR", "EFFECTIVE_TERM_CODE"] if c in cat.columns]
cat = cat.sort_values(cat_sort_cols, ascending=False, na_position="last") if cat_sort_cols else cat

cat = (
    cat.dropna(subset=["subject_id_norm"])
    .drop_duplicates("subject_id_norm")
    [["subject_id_norm", "COURSE_NUMBER_cat", "SUBJECT_TITLE_cat"]]
)

school_map = tables["table_6"].copy()
school_map["COURSE_NUMBER_cat"] = clean_str(school_map["SUBJECT_CODE"]).str.upper()
school_map["OFFER_SCHOOL_NAME_cat"] = clean_str(school_map["SCHOOL_NAME"])
school_map = school_map.drop_duplicates("COURSE_NUMBER_cat")[["COURSE_NUMBER_cat", "OFFER_SCHOOL_NAME_cat"]]

cat = cat.merge(school_map, on="COURSE_NUMBER_cat", how="left")

df = df.merge(cat, on="subject_id_norm", how="left")
df["COURSE_NUMBER"] = df["COURSE_NUMBER"].combine_first(df["COURSE_NUMBER_cat"])
df["SUBJECT_TITLE"] = df["SUBJECT_TITLE"].combine_first(df["SUBJECT_TITLE_cat"])
df["OFFER_SCHOOL_NAME"] = df["OFFER_SCHOOL_NAME"].combine_first(df["OFFER_SCHOOL_NAME_cat"])

# Material status dimension
status = tables["table_4"].copy()
status["status_key_norm"] = clean_str(status["tip_material_status_key"])
status["TIP_MATERIAL_STATUS"] = clean_str(status["TIP_MATERIAL_STATUS"])
status["TIP_MATERIAL_STATUS_CODE"] = clean_str(status["TIP_MATERIAL_STATUS_CODE"])
status["MATERIAL_STATUS"] = status["TIP_MATERIAL_STATUS"].combine_first(status["TIP_MATERIAL_STATUS_CODE"])
status = status.drop_duplicates("status_key_norm")[["status_key_norm", "MATERIAL_STATUS"]]

df = df.merge(status, on="status_key_norm", how="left")
df["MATERIAL_STATUS"] = df["MATERIAL_STATUS"].combine_first(df["status_key_norm"])

# Material price dimension
mat = tables["table_1"].copy()
mat["material_key_norm"] = normalize_material_key(mat["TIP_MATERIAL_KEY"])
mat["isbn_norm"] = clean_str(mat["ISBN"])

for price_col in ["NEW_SHELF_PRICE", "USED_SHELF_PRICE"]:
    mat[price_col] = pd.to_numeric(mat[price_col], errors="coerce")

mat_by_key = (
    mat.dropna(subset=["material_key_norm"])
    .drop_duplicates("material_key_norm")
    [["material_key_norm", "NEW_SHELF_PRICE", "USED_SHELF_PRICE"]]
)

mat_by_isbn = (
    mat.dropna(subset=["isbn_norm"])
    .drop_duplicates("isbn_norm")
    [["isbn_norm", "NEW_SHELF_PRICE", "USED_SHELF_PRICE"]]
    .rename(columns={
        "NEW_SHELF_PRICE": "NEW_SHELF_PRICE_isbn",
        "USED_SHELF_PRICE": "USED_SHELF_PRICE_isbn"
    })
)

df["isbn_norm"] = clean_str(df["ISBN"])
df = df.merge(mat_by_key, on="material_key_norm", how="left")
df = df.merge(mat_by_isbn, on="isbn_norm", how="left")

df["NEW_SHELF_PRICE"] = df["NEW_SHELF_PRICE"].combine_first(df["NEW_SHELF_PRICE_isbn"])
df["USED_SHELF_PRICE"] = df["USED_SHELF_PRICE"].combine_first(df["USED_SHELF_PRICE_isbn"])

no_material_mask = (
    df["material_key_norm"].astype("string").str.lower().str.contains("course has no materials", na=False)
    | df["MATERIAL_STATUS"].astype("string").str.lower().str.contains("course has no materials", na=False)
)
df.loc[no_material_mask, ["NEW_SHELF_PRICE", "USED_SHELF_PRICE"]] = (
    df.loc[no_material_mask, ["NEW_SHELF_PRICE", "USED_SHELF_PRICE"]].fillna(0)
)

df["NEW_SHELF_PRICE"] = pd.to_numeric(df["NEW_SHELF_PRICE"], errors="coerce").fillna(0)
df["USED_SHELF_PRICE"] = pd.to_numeric(df["USED_SHELF_PRICE"], errors="coerce").fillna(0)

df["NEW_SHELF_PRICE_TOTAL_COMPONENT"] = df["NEW_SHELF_PRICE"] * df["RECORD_COUNT"]
df["USED_SHELF_PRICE_TOTAL_COMPONENT"] = df["USED_SHELF_PRICE"] * df["RECORD_COUNT"]

final = (
    df.groupby(["COURSE_NUMBER", "SUBJECT_TITLE", "MATERIAL_STATUS"], dropna=False, as_index=False)
    .agg(
        TOTAL_NEW_SHELF_PRICE=("NEW_SHELF_PRICE_TOTAL_COMPONENT", "sum"),
        MIN_NEW_SHELF_PRICE=("NEW_SHELF_PRICE", "min"),
        MAX_NEW_SHELF_PRICE=("NEW_SHELF_PRICE", "max"),
        TOTAL_USED_SHELF_PRICE=("USED_SHELF_PRICE_TOTAL_COMPONENT", "sum"),
        MIN_USED_SHELF_PRICE=("USED_SHELF_PRICE", "min"),
        MAX_USED_SHELF_PRICE=("USED_SHELF_PRICE", "max"),
        TOTAL_NUMBER_OF_SCHOOLS=("OFFER_SCHOOL_NAME", lambda x: x.dropna().nunique()),
        TOTAL_NUMBER_OF_MATERIALS=("RECORD_COUNT", "sum")
    )
    .sort_values(["COURSE_NUMBER", "SUBJECT_TITLE", "MATERIAL_STATUS"], na_position="last")
    .reset_index(drop=True)
)

result = {
    "tip_subject_material_status_summary": final
}
