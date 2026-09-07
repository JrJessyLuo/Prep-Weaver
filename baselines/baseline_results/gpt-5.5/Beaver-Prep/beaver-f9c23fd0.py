import pandas as pd
import numpy as np

def clean_text(s):
    return s.astype("string").str.strip()

# Materials
materials = tables["table_1"].copy()
materials["_mk_clean"] = clean_text(materials["TIP_MATERIAL_KEY"])
materials["ISBN_clean"] = clean_text(materials["ISBN"])
materials["MATERIAL_TITLE"] = clean_text(materials["TITLE"])
materials["NEW_SHELF_PRICE"] = pd.to_numeric(materials["NEW_SHELF_PRICE"], errors="coerce")

is_no_material = materials["MATERIAL_TITLE"].str.casefold().eq("course has no materials").fillna(False)
valid_materials = materials.loc[~is_no_material].copy()

# Material lookup by material key
material_by_key = (
    valid_materials.loc[valid_materials["_mk_clean"].notna()]
    .sort_values(["_mk_clean", "NEW_SHELF_PRICE"], na_position="first")
    .drop_duplicates("_mk_clean", keep="last")
    [["_mk_clean", "ISBN_clean", "MATERIAL_TITLE", "NEW_SHELF_PRICE"]]
    .rename(columns={
        "ISBN_clean": "KEY_ISBN",
        "MATERIAL_TITLE": "KEY_MATERIAL_TITLE",
        "NEW_SHELF_PRICE": "KEY_NEW_SHELF_PRICE"
    })
)

# Material lookup by ISBN
material_by_isbn = (
    valid_materials.loc[valid_materials["ISBN_clean"].notna()]
    .sort_values(["ISBN_clean", "NEW_SHELF_PRICE"], na_position="first")
    .drop_duplicates("ISBN_clean", keep="last")
    [["ISBN_clean", "MATERIAL_TITLE", "NEW_SHELF_PRICE"]]
    .rename(columns={
        "ISBN_clean": "_isbn_join",
        "MATERIAL_TITLE": "ISBN_MATERIAL_TITLE",
        "NEW_SHELF_PRICE": "ISBN_NEW_SHELF_PRICE"
    })
)

# Subject-material links
links = tables["table_2"].copy()
links["_offer_key"] = clean_text(links["TIP_SUBJECT_OFFERED_KEY"])
links["_mk_clean"] = clean_text(links["TIP_MATERIAL_KEY"])
links["ISBN_clean"] = clean_text(links["ISBN"])
links["_subject_id"] = clean_text(links["subject_id"])
links["_term_code"] = clean_text(links["TERM_CODE"])

# Subject titles from subject offerings
offerings = tables["table_4"].copy()
offerings["_offer_key"] = clean_text(offerings["TIP_SUBJECT_OFFERED_KEY"])
offerings["_subject_id"] = clean_text(offerings["SUBJECT_ID"])
offerings["_term_code"] = clean_text(offerings["TERM_CODE"])
offerings["SUBJECT_TITLE_clean"] = clean_text(offerings["SUBJECT_TITLE"])

subject_by_key = (
    offerings.loc[offerings["_offer_key"].notna(), ["_offer_key", "SUBJECT_TITLE_clean"]]
    .drop_duplicates("_offer_key")
    .rename(columns={"SUBJECT_TITLE_clean": "SUBJECT_TITLE_by_key"})
)

subject_by_subterm = (
    offerings.loc[
        offerings["_subject_id"].notna() & offerings["_term_code"].notna(),
        ["_subject_id", "_term_code", "SUBJECT_TITLE_clean"]
    ]
    .drop_duplicates(["_subject_id", "_term_code"])
    .rename(columns={"SUBJECT_TITLE_clean": "SUBJECT_TITLE_by_subterm"})
)

df = links.merge(subject_by_key, on="_offer_key", how="left")
df = df.merge(subject_by_subterm, on=["_subject_id", "_term_code"], how="left")

df["SUBJECT_TITLE"] = df["SUBJECT_TITLE_by_key"].combine_first(df["SUBJECT_TITLE_by_subterm"])

# Fallback subject titles from catalog by latest academic year
catalog = tables["table_3"].copy()
catalog["_subject_id"] = clean_text(catalog["subject_id"])
catalog["SUBJECT_TITLE_catalog"] = clean_text(catalog["SUBJECT_TITLE"])
catalog["ACADEMIC_YEAR"] = pd.to_numeric(catalog["ACADEMIC_YEAR"], errors="coerce")

catalog_latest = (
    catalog.loc[catalog["_subject_id"].notna(), ["_subject_id", "ACADEMIC_YEAR", "SUBJECT_TITLE_catalog"]]
    .sort_values("ACADEMIC_YEAR")
    .drop_duplicates("_subject_id", keep="last")
    [["_subject_id", "SUBJECT_TITLE_catalog"]]
)

df = df.merge(catalog_latest, on="_subject_id", how="left")
df["SUBJECT_TITLE"] = df["SUBJECT_TITLE"].combine_first(df["SUBJECT_TITLE_catalog"])

# Attach material details, first by material key, then by ISBN
df = df.merge(material_by_key, on="_mk_clean", how="left")
df["ISBN_FOR_JOIN"] = df["ISBN_clean"].combine_first(df["KEY_ISBN"])

df = df.merge(material_by_isbn, left_on="ISBN_FOR_JOIN", right_on="_isbn_join", how="left")

df["ISBN"] = df["ISBN_FOR_JOIN"].combine_first(df["KEY_ISBN"])
df["MATERIAL_TITLE"] = df["KEY_MATERIAL_TITLE"].combine_first(df["ISBN_MATERIAL_TITLE"])
df["NEW_SHELF_PRICE"] = df["KEY_NEW_SHELF_PRICE"].combine_first(df["ISBN_NEW_SHELF_PRICE"])

# Final item-level table with subject-level total new-material cost
items = df[["SUBJECT_TITLE", "MATERIAL_TITLE", "ISBN", "NEW_SHELF_PRICE"]].copy()
items = items.loc[
    items["SUBJECT_TITLE"].notna()
    & items["MATERIAL_TITLE"].notna()
    & items["NEW_SHELF_PRICE"].notna()
]

items = items.loc[
    ~items["MATERIAL_TITLE"].str.casefold().eq("course has no materials").fillna(False)
]

items = items.drop_duplicates(
    ["SUBJECT_TITLE", "MATERIAL_TITLE", "ISBN", "NEW_SHELF_PRICE"]
)

totals = (
    items.groupby("SUBJECT_TITLE", as_index=False)["NEW_SHELF_PRICE"]
    .sum()
    .rename(columns={"NEW_SHELF_PRICE": "TOTAL_COST_OF_NEW_MATERIALS"})
)

final_df = (
    items.merge(totals, on="SUBJECT_TITLE", how="left")
    .sort_values(["NEW_SHELF_PRICE", "SUBJECT_TITLE", "MATERIAL_TITLE"], ascending=[True, True, True])
    .reset_index(drop=True)
)

result = {
    "subject_material_new_costs": final_df
}
