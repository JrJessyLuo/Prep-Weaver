import pandas as pd

# Source input tables from provided `tables` dict
td = tables['table_1'].copy()   # TIP_DETAIL.pkl
tm = tables['table_4'].copy()   # TIP_MATERIAL.pkl
tso = tables['table_7'].copy()  # TIP_SUBJECT_OFFERED.pkl

# Normalize join keys to string for safety
td["subject_id_norm"] = td["subject_id"].astype(str).str.strip()
td["TERM_CODE_norm"] = td["TERM_CODE"].astype(str).str.strip()

tso["SUBJECT_ID_norm"] = tso["SUBJECT_ID"].astype(str).str.strip()
tso["TERM_CODE_norm"] = tso["TERM_CODE"].astype(str).str.strip()

# Select needed columns from TSO for join
tso_sel = tso[
    ["SUBJECT_ID_norm", "TERM_CODE_norm", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME", "IS_NO_COURSE_MATERIAL"]
].drop_duplicates()

# Left join TIP_DETAIL -> TIP_SUBJECT_OFFERED on normalized keys
td_tso = td.merge(
    tso_sel,
    left_on=["subject_id_norm", "TERM_CODE_norm"],
    right_on=["SUBJECT_ID_norm", "TERM_CODE_norm"],
    how="left",
)

# Bring in material prices from TIP_MATERIAL
tm_sel = tm[["TIP_MATERIAL_KEY", "NEW_SHELF_PRICE", "USED_SHELF_PRICE"]].drop_duplicates()
td_tso_tm = td_tso.merge(tm_sel, on="TIP_MATERIAL_KEY", how="left")

# Apply filters:
# - Exclude where IS_NO_COURSE_MATERIAL == 'Y'
# - Exclude material key like 'N/ACourse has no materials%'
is_no_mat = td_tso_tm["IS_NO_COURSE_MATERIAL"].fillna("")
mask_no_course_mat_flag = is_no_mat.ne("Y")

tip_mat_key = td_tso_tm["TIP_MATERIAL_KEY"].astype(str)
mask_no_na_course_key = ~tip_mat_key.str.startswith("N/ACourse has no materials", na=False)

filtered = td_tso_tm[mask_no_course_mat_flag & mask_no_na_course_key].copy()

# Retain required columns
cols_out = [
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "TIP_MATERIAL_KEY",
    "TIP_MATERIAL_STATUS_KEY",
    "subject_id",
    "TERM_CODE",
    "NEW_SHELF_PRICE",
    "USED_SHELF_PRICE",
]
working_df = filtered[cols_out].copy()

# Aggregations per department and school
group_cols = ["OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME"]

agg_df = (
    working_df.groupby(group_cols, dropna=False)
    .agg(
        unique_course_materials=("TIP_MATERIAL_KEY", pd.Series.nunique),
        number_of_courses=("subject_id", pd.Series.nunique),
        avg_new_shelf_price=("NEW_SHELF_PRICE", "mean"),
        avg_used_shelf_price=("USED_SHELF_PRICE", "mean"),
        total_material_records=("TIP_MATERIAL_KEY", "size"),
        distinct_material_statuses=("TIP_MATERIAL_STATUS_KEY", pd.Series.nunique),
    )
    .reset_index()
)

# Grand total across all schools and departments (with null school/department)
grand_total = pd.DataFrame(
    {
        "OFFER_DEPT_NAME": [pd.NA],
        "OFFER_SCHOOL_NAME": [pd.NA],
        "unique_course_materials": [working_df["TIP_MATERIAL_KEY"].nunique()],
        "number_of_courses": [working_df["subject_id"].nunique()],
        "avg_new_shelf_price": [working_df["NEW_SHELF_PRICE"].mean()],
        "avg_used_shelf_price": [working_df["USED_SHELF_PRICE"].mean()],
        "total_material_records": [len(working_df)],
        "distinct_material_statuses": [working_df["TIP_MATERIAL_STATUS_KEY"].nunique()],
    }
)

final_df = pd.concat([agg_df, grand_total], ignore_index=True)

# Assign final answer to `result`
result = {
    "department_school_materials_summary": final_df
}