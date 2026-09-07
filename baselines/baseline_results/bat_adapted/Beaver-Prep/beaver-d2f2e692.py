import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','MASTER_COURSE_NUMBER','MASTER_COURSE_NUMBER_DESC','MASTER_SUBJECT_ID','SUBJECT_ID','OFFER_DEPT_CODE','OFFER_DEPT_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','subject_id','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY']].copy()
    df = df.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','subject_id','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY'])
    target = df[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','subject_id','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['TIP_MATERIAL_KEY','NEW_SHELF_PRICE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
subject_material_links = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
material_details = prepared_table_3

# Assume prepared DataFrames: subjects, subject_material_links, material_details
# 1) Join subjects to material links primarily on SUBJECT_ID <> subject_id
links = subject_material_links.merge(subjects[["SUBJECT_ID","OFFER_DEPT_NAME","OFFER_DEPT_CODE","MASTER_COURSE_NUMBER"]], left_on="subject_id", right_on="SUBJECT_ID", how="left")

# 2) Attach material prices
links = links.merge(material_details, on="TIP_MATERIAL_KEY", how="left")

# Treat missing prices as 0 for totals
links["NEW_SHELF_PRICE"] = pd.to_numeric(links["NEW_SHELF_PRICE"], errors="coerce").fillna(0.0)

# Exclude explicit no-material placeholders if present
no_mat_keys = {"N/ACourse has no materials"}
links = links[~links["TIP_MATERIAL_KEY"].isin(no_mat_keys)]

# 3) Compute per (dept, master course) aggregates
agg = links.groupby(["OFFER_DEPT_NAME","OFFER_DEPT_CODE","MASTER_COURSE_NUMBER"], dropna=False).agg(
    subjects=("SUBJECT_ID", pd.Series.nunique),
    total_new_shelf_price=("NEW_SHELF_PRICE", "sum"),
    unique_tip_materials=("TIP_MATERIAL_KEY", pd.Series.nunique)
).reset_index()

# 4) Formatting and ordering
agg = agg.sort_values(["OFFER_DEPT_NAME","MASTER_COURSE_NUMBER"], kind="mergesort")
for col in ["subjects","total_new_shelf_price","unique_tip_materials"]:
    if col != "total_new_shelf_price":
        agg[col] = agg[col].round(0).astype(int)
    else:
        agg[col] = agg[col].round(0).astype(int)
agg["subjects_fmt"] = agg["subjects"].map(lambda x: f"{x:,}")
agg["total_new_shelf_price_fmt"] = agg["total_new_shelf_price"].map(lambda x: f"{x:,}")
agg["unique_tip_materials_fmt"] = agg["unique_tip_materials"].map(lambda x: f"{x:,}")

# 5) Build display with department/master course shown only at first occurrence within department, with subtotals and grand total
rows = []
current_dept = None
for _, r in agg.iterrows():
    dept = r["OFFER_DEPT_NAME"]
    mc = r["MASTER_COURSE_NUMBER"]
    # If new department, optionally insert nothing; will add subtotal after block
    show_dept = dept if dept != current_dept else ""
    show_mc = mc if dept != current_dept else mc  # show master course on every row within dept per spec states display dept and master course only if it differs from previous entry
    # However, we blank dept when same as previous; master course keeps full value but could also be repeated; if identical consecutive, blank it too
    if dept == current_dept:
        # Check previous row's master course in built rows
        prev_mc = rows[-1]["MASTER_COURSE_NUMBER"] if rows else None
        show_mc = "" if prev_mc == mc else mc
    rows.append({
        "OFFER_DEPT_NAME": show_dept,
        "MASTER_COURSE_NUMBER": show_mc,
        "subjects": r["subjects_fmt"],
        "total_new_shelf_price": r["total_new_shelf_price_fmt"],
        "unique_tip_materials": r["unique_tip_materials_fmt"],
        "_dept_key": dept
    })
    # Update current dept
    if dept != current_dept:
        current_dept = dept
    
# 6) Insert department subtotals
out_rows = []
for dept, grp in groupby(rows, key=lambda x: x["_dept_key"]):
    grp = list(grp)
    out_rows.extend([{k:v for k,v in g.items() if k != "_dept_key"} for g in grp])
    # Compute subtotal from agg for this dept
    sub = agg[agg["OFFER_DEPT_NAME"]==dept].agg({
        "subjects":"sum",
        "total_new_shelf_price":"sum",
        "unique_tip_materials":"sum"
    })
    out_rows.append({
        "OFFER_DEPT_NAME": f"Subtotal - {dept}",
        "MASTER_COURSE_NUMBER": "",
        "subjects": f"{int(round(sub['subjects'])):,}",
        "total_new_shelf_price": f"{int(round(sub['total_new_shelf_price'])):,}",
        "unique_tip_materials": f"{int(round(sub['unique_tip_materials'])):,}"
    })

# 7) Grand total
grand = agg.agg({
    "subjects":"sum",
    "total_new_shelf_price":"sum",
    "unique_tip_materials":"sum"
})
out_rows.append({
    "OFFER_DEPT_NAME": "Grand Total",
    "MASTER_COURSE_NUMBER": "",
    "subjects": f"{int(round(grand['subjects'])):,}",
    "total_new_shelf_price": f"{int(round(grand['total_new_shelf_price'])):,}",
    "unique_tip_materials": f"{int(round(grand['unique_tip_materials'])):,}"
})

result = pd.DataFrame(out_rows)
# Columns in final output
result = result[["OFFER_DEPT_NAME","MASTER_COURSE_NUMBER","subjects","total_new_shelf_price","unique_tip_materials"]]

target = result

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
