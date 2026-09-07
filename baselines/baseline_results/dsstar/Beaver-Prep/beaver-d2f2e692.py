import pandas as pd
import numpy as np

# tables dict is preloaded with DataFrames
# Mapping reminder:
# tables['table_1'] -> TIP_DETAIL.pkl
# tables['table_2'] -> TIP_SUBJECT_OFFERED.pkl
# tables['table_3'] -> TIP_MATERIAL_STATUS.pkl
# tables['table_4'] -> TIP_MATERIAL.pkl
# others not needed for this task

# Load from provided tables dict
tip_detail = tables['table_1'].copy()
tip_so = tables['table_2'].copy()
tip_status = tables['table_3'].copy()
tip_material = tables['table_4'].copy()

# Standardize column names for status key to match and trim whitespace
tip_status = tip_status.rename(columns={"tip_material_status_key": "TIP_MATERIAL_STATUS_KEY"})

def trim_object_cols(df):
    obj_cols = df.select_dtypes(include="object").columns
    if len(obj_cols) > 0:
        df[obj_cols] = df[obj_cols].apply(lambda s: s.str.strip())
    return df

tip_so = trim_object_cols(tip_so)
tip_detail = trim_object_cols(tip_detail)
tip_material = trim_object_cols(tip_material)
tip_status = trim_object_cols(tip_status)

# 1) TIP_DETAIL -> TIP_SUBJECT_OFFERED on TIP_SUBJECT_OFFERED_KEY
joined_1 = tip_detail.merge(
    tip_so[[
        "TIP_SUBJECT_OFFERED_KEY",
        "TERM_CODE",
        "MASTER_COURSE_NUMBER",
        "OFFER_DEPT_NAME"
    ]].rename(columns={"TERM_CODE": "TERM_CODE_SO"}),
    on="TIP_SUBJECT_OFFERED_KEY",
    how="left",
    validate="m:1"
)

# 2) Join materials
joined_2 = joined_1.merge(
    tip_material,
    on="TIP_MATERIAL_KEY",
    how="left",
    validate="m:1"
)

# 3) Join status
joined_final = joined_2.merge(
    tip_status[["TIP_MATERIAL_STATUS_KEY", "TIP_MATERIAL_STATUS_CODE", "TIP_MATERIAL_STATUS"]],
    on="TIP_MATERIAL_STATUS_KEY",
    how="left",
    validate="m:1"
)

# Filter to valid course/department and exclude "Course has no materials"
mask_valid_course = (
    joined_final["MASTER_COURSE_NUMBER"].notna() &
    joined_final["OFFER_DEPT_NAME"].notna()
)

title_series = joined_final.get("TITLE")
tmk_series = joined_final.get("TIP_MATERIAL_KEY")

no_materials_mask = pd.Series(False, index=joined_final.index)
if title_series is not None:
    no_materials_mask = no_materials_mask | title_series.str.casefold().eq("course has no materials").fillna(False)
if tmk_series is not None:
    no_materials_mask = no_materials_mask | tmk_series.str.startswith("N/ACourse has no materials", na=False)

filtered = joined_final.loc[mask_valid_course & (~no_materials_mask)].copy()

# Ensure NEW_SHELF_PRICE exists; fillna(0) for sum
if "NEW_SHELF_PRICE" not in filtered.columns:
    filtered["NEW_SHELF_PRICE"] = 0.0
else:
    filtered["NEW_SHELF_PRICE"] = pd.to_numeric(filtered["NEW_SHELF_PRICE"], errors="coerce").fillna(0.0)

# Group and aggregate per (OFFER_DEPT_NAME, MASTER_COURSE_NUMBER)
agg_df = (
    filtered
    .groupby(["OFFER_DEPT_NAME", "MASTER_COURSE_NUMBER"], dropna=False)
    .agg(
        subject_count=("TIP_SUBJECT_OFFERED_KEY", "nunique"),
        total_new_shelf_price=("NEW_SHELF_PRICE", "sum"),
        unique_materials=("TIP_MATERIAL_KEY", "nunique"),
    )
    .reset_index()
    .sort_values(["OFFER_DEPT_NAME", "MASTER_COURSE_NUMBER"], kind="mergesort")
)

# Prepare display with department and master course only when changed from previous row
out = agg_df.copy()

# Round numeric values to integers
out["subject_count"] = out["subject_count"].astype("Int64")
out["total_new_shelf_price"] = out["total_new_shelf_price"].round(0).astype("Int64")
out["unique_materials"] = out["unique_materials"].astype("Int64")

# Build department subtotals
dept_subtotals = (
    out.groupby("OFFER_DEPT_NAME", as_index=False)
      .agg(
          subject_count=("subject_count", "sum"),
          total_new_shelf_price=("total_new_shelf_price", "sum"),
          unique_materials=("unique_materials", "sum")
      )
)
dept_subtotals["MASTER_COURSE_NUMBER"] = "Subtotal"
dept_subtotals["__is_subtotal__"] = True

# Mark detail rows
out["__is_subtotal__"] = False

# Combine detail rows and subtotals, ordered with subtotal after each department block
combined = []
for dept, g in out.groupby("OFFER_DEPT_NAME", sort=True):
    g_sorted = g.sort_values(["OFFER_DEPT_NAME", "MASTER_COURSE_NUMBER"], kind="mergesort")
    combined.append(g_sorted)
    subtotal_row = dept_subtotals.loc[dept_subtotals["OFFER_DEPT_NAME"] == dept]
    combined.append(subtotal_row)

final_df = pd.concat(combined, ignore_index=True)

# Append grand total
grand_total = pd.DataFrame({
    "OFFER_DEPT_NAME": ["Grand total"],
    "MASTER_COURSE_NUMBER": ["Grand total"],
    "subject_count": [final_df.loc[~final_df["__is_subtotal__"], "subject_count"].sum()],
    "total_new_shelf_price": [final_df.loc[~final_df["__is_subtotal__"], "total_new_shelf_price"].sum()],
    "unique_materials": [final_df.loc[~final_df["__is_subtotal__"], "unique_materials"].sum()],
    "__is_subtotal__": [True]
})
final_df = pd.concat([final_df, grand_total], ignore_index=True)

# After inserting subtotals, hide repeated department/master values on consecutive detail rows.
# For subtotals and grand total, keep the department label; master shows "Subtotal"/"Grand total".
display_df = final_df.copy()

# For detail rows, blank out repeated dept/master when same as previous non-subtotal row
dept_col = "OFFER_DEPT_NAME"
mc_col = "MASTER_COURSE_NUMBER"

# Create helper columns for previous values among all rows
prev_dept = display_df[dept_col].shift(1)
prev_mc = display_df[mc_col].shift(1)
prev_is_sub = display_df["__is_subtotal__"].shift(1).fillna(False)

# For detail rows only
detail_mask = ~display_df["__is_subtotal__"]

# Blank department if same as previous row's department and previous row is not a subtotal
same_dept_as_prev = (display_df[dept_col] == prev_dept) & (~prev_is_sub)
display_df.loc[detail_mask & same_dept_as_prev, dept_col] = ""

# For master course, blank if same as previous row (and previous not subtotal)
same_mc_as_prev = (display_df[mc_col] == prev_mc) & (~prev_is_sub)
display_df.loc[detail_mask & same_mc_as_prev, mc_col] = ""

# Format numbers with commas
for c in ["subject_count", "total_new_shelf_price", "unique_materials"]:
    display_df[c] = display_df[c].astype("Int64").map(lambda x: f"{int(x):,}" if pd.notna(x) else "")

# Keep only required columns and friendly headers
answer = display_df[[dept_col, mc_col, "subject_count", "total_new_shelf_price", "unique_materials"]].rename(columns={
    dept_col: "Department",
    mc_col: "Master Course",
    "subject_count": "Subjects",
    "total_new_shelf_price": "Total New Shelf Price",
    "unique_materials": "Unique TIP Materials"
})

# Assign to result dict as required
result = {"Dept-Master Course Aggregates with Subtotals": answer}