import pandas as pd

def clean_str(s):
    s = s.astype("string").str.strip()
    return s.mask(s.eq(""))

def fmt_int(x):
    if pd.isna(x):
        return ""
    return f"{int(round(float(x))):,}"

offers_raw = tables["table_2"].copy()

offers = pd.DataFrame(index=offers_raw.index)
offers["offer_key"] = clean_str(offers_raw["TIP_SUBJECT_OFFERED_KEY"])
offers["department_name"] = clean_str(offers_raw["OFFER_DEPT_NAME"]).fillna("Unknown")
offers["master_course_code"] = clean_str(offers_raw["MASTER_COURSE_NUMBER"]).fillna("Unknown")
offers["subject_id_clean"] = clean_str(offers_raw["SUBJECT_ID"])
offers["_dept_sort"] = offers["department_name"].astype("string").str.casefold().fillna("")

if "MASTER_COURSE_NUMBER_SORT" in offers_raw.columns:
    offers["_master_sort"] = clean_str(offers_raw["MASTER_COURSE_NUMBER_SORT"]).fillna(offers["master_course_code"])
else:
    offers["_master_sort"] = offers["master_course_code"]
offers["_master_sort"] = offers["_master_sort"].astype("string").fillna("")

offer_base = offers[
    ["offer_key", "department_name", "master_course_code", "subject_id_clean", "_dept_sort", "_master_sort"]
].drop_duplicates()

assoc_raw = tables["table_1"].copy()
assoc = pd.DataFrame(index=assoc_raw.index)
assoc["offer_key"] = clean_str(assoc_raw["TIP_SUBJECT_OFFERED_KEY"])
assoc["material_key"] = clean_str(assoc_raw["TIP_MATERIAL_KEY"])
assoc["status_key"] = clean_str(assoc_raw["TIP_MATERIAL_STATUS_KEY"]).fillna("").str.upper()

material_key_upper = assoc["material_key"].fillna("").str.upper()
real_material_mask = (
    assoc["offer_key"].notna()
    & assoc["material_key"].notna()
    & assoc["status_key"].ne("NM")
    & ~material_key_upper.str.contains("COURSE HAS NO MATERIAL", regex=False)
    & ~material_key_upper.str.startswith("N/A")
)

assoc_pairs = assoc.loc[real_material_mask, ["offer_key", "material_key"]].drop_duplicates()

materials_raw = tables["table_4"].copy()
materials = pd.DataFrame(index=materials_raw.index)
materials["material_key"] = clean_str(materials_raw["TIP_MATERIAL_KEY"])
materials["NEW_SHELF_PRICE"] = pd.to_numeric(materials_raw["NEW_SHELF_PRICE"], errors="coerce").fillna(0)

material_prices = (
    materials.dropna(subset=["material_key"])
    .groupby("material_key", as_index=False, sort=False)
    .agg(NEW_SHELF_PRICE=("NEW_SHELF_PRICE", "max"))
)

assoc_priced = assoc_pairs.merge(material_prices, on="material_key", how="left")
assoc_priced["NEW_SHELF_PRICE"] = assoc_priced["NEW_SHELF_PRICE"].fillna(0)

subject_counts = (
    offer_base.drop_duplicates(["department_name", "master_course_code", "subject_id_clean"])
    .groupby(["department_name", "master_course_code"], as_index=False, sort=False)
    .agg(
        number_subjects=("subject_id_clean", lambda s: s.dropna().nunique()),
        _dept_sort=("_dept_sort", "first"),
        _master_sort=("_master_sort", "min"),
    )
)

offer_course_map = offer_base[
    ["offer_key", "department_name", "master_course_code"]
].dropna(subset=["offer_key"]).drop_duplicates()

course_materials = offer_course_map.merge(assoc_priced, on="offer_key", how="left")
course_materials["NEW_SHELF_PRICE"] = course_materials["NEW_SHELF_PRICE"].fillna(0)

material_counts = (
    course_materials.groupby(["department_name", "master_course_code"], as_index=False, sort=False)
    .agg(
        total_new_shelf_price=("NEW_SHELF_PRICE", "sum"),
        unique_tip_materials=("material_key", lambda s: s.dropna().nunique()),
    )
)

detail = subject_counts.merge(
    material_counts,
    on=["department_name", "master_course_code"],
    how="left",
)
detail["total_new_shelf_price"] = detail["total_new_shelf_price"].fillna(0)
detail["unique_tip_materials"] = detail["unique_tip_materials"].fillna(0)

dept_subjects = (
    offer_base.drop_duplicates(["department_name", "subject_id_clean"])
    .groupby("department_name", as_index=False, sort=False)
    .agg(
        number_subjects=("subject_id_clean", lambda s: s.dropna().nunique()),
        _dept_sort=("_dept_sort", "first"),
    )
)

offer_dept_map = offer_base[
    ["offer_key", "department_name"]
].dropna(subset=["offer_key"]).drop_duplicates()

dept_materials = offer_dept_map.merge(assoc_priced, on="offer_key", how="left")
dept_materials["NEW_SHELF_PRICE"] = dept_materials["NEW_SHELF_PRICE"].fillna(0)

dept_material_counts = (
    dept_materials.groupby("department_name", as_index=False, sort=False)
    .agg(
        total_new_shelf_price=("NEW_SHELF_PRICE", "sum"),
        unique_tip_materials=("material_key", lambda s: s.dropna().nunique()),
    )
)

dept_subtotals = dept_subjects.merge(dept_material_counts, on="department_name", how="left")
dept_subtotals["total_new_shelf_price"] = dept_subtotals["total_new_shelf_price"].fillna(0)
dept_subtotals["unique_tip_materials"] = dept_subtotals["unique_tip_materials"].fillna(0)

detail = detail.sort_values(["_dept_sort", "_master_sort", "department_name", "master_course_code"], kind="mergesort")
dept_subtotals = dept_subtotals.sort_values(["_dept_sort", "department_name"], kind="mergesort")

rows = []
for dept_name in dept_subtotals["department_name"].tolist():
    dept_detail = detail.loc[detail["department_name"].eq(dept_name)].copy()
    if not dept_detail.empty:
        dept_rows = dept_detail.rename(
            columns={
                "department_name": "Department",
                "master_course_code": "Master Course",
                "number_subjects": "Number of Subjects",
                "total_new_shelf_price": "Total New Shelf Price",
                "unique_tip_materials": "Unique TIP Materials",
            }
        )[
            ["Department", "Master Course", "Number of Subjects", "Total New Shelf Price", "Unique TIP Materials"]
        ]
        rows.append(dept_rows)

    subtotal_row = dept_subtotals.loc[dept_subtotals["department_name"].eq(dept_name)].head(1)
    if not subtotal_row.empty:
        subtotal_out = pd.DataFrame(
            {
                "Department": subtotal_row["department_name"].to_list(),
                "Master Course": ["Subtotal"],
                "Number of Subjects": subtotal_row["number_subjects"].to_list(),
                "Total New Shelf Price": subtotal_row["total_new_shelf_price"].to_list(),
                "Unique TIP Materials": subtotal_row["unique_tip_materials"].to_list(),
            }
        )
        rows.append(subtotal_out)

all_offer_map = offer_base[["offer_key"]].dropna(subset=["offer_key"]).drop_duplicates()
grand_materials = all_offer_map.merge(assoc_priced, on="offer_key", how="left")
grand_materials["NEW_SHELF_PRICE"] = grand_materials["NEW_SHELF_PRICE"].fillna(0)

grand_row = pd.DataFrame(
    {
        "Department": ["Grand Total"],
        "Master Course": [""],
        "Number of Subjects": [offer_base["subject_id_clean"].dropna().nunique()],
        "Total New Shelf Price": [grand_materials["NEW_SHELF_PRICE"].sum()],
        "Unique TIP Materials": [grand_materials["material_key"].dropna().nunique()],
    }
)
rows.append(grand_row)

final = pd.concat(rows, ignore_index=True) if rows else grand_row.copy()

final["Department"] = final["Department"].where(final["Department"].ne(final["Department"].shift()), "")
final["Master Course"] = final["Master Course"].where(final["Master Course"].ne(final["Master Course"].shift()), "")

for col in ["Number of Subjects", "Total New Shelf Price", "Unique TIP Materials"]:
    final[col] = final[col].map(fmt_int)

result = {"master_courses_by_department": final}
