import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['TERM_CODE','SUBJECT_ID','OFFER_SCHOOL_NAME','NUM_ENROLLED_STUDENTS','TIP_SUBJECT_OFFERED_KEY']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['TERM_CODE','TIP_SUBJECT_OFFERED_KEY','TIP_MATERIAL_STATUS_KEY','TIP_MATERIAL_KEY','RECORD_COUNT']].copy()
    df['RECORD_COUNT'] = pd.to_numeric(df['RECORD_COUNT'], errors='coerce').fillna(0).astype('int64')
    target = df.groupby(['TERM_CODE','TIP_SUBJECT_OFFERED_KEY','TIP_MATERIAL_STATUS_KEY','TIP_MATERIAL_KEY'], dropna=False, as_index=False)['RECORD_COUNT'].sum()
    target = target[['TERM_CODE','TIP_SUBJECT_OFFERED_KEY','TIP_MATERIAL_STATUS_KEY','TIP_MATERIAL_KEY','RECORD_COUNT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_6'])
prepared_subject_catalog = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_tip_offered = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_tip_materials = prepared_table_3

# Assume the three prepared tables already exist as dataframes with the specified columns
# prepared_subject_catalog: TERM_CODE, SUBJECT_ID, SUBJECT_TITLE
# prepared_tip_offered: TERM_CODE, SUBJECT_ID, OFFER_SCHOOL_NAME, NUM_ENROLLED_STUDENTS, TIP_SUBJECT_OFFERED_KEY
# prepared_tip_materials: TERM_CODE, TIP_SUBJECT_OFFERED_KEY, TIP_MATERIAL_STATUS_KEY, TIP_MATERIAL_KEY, RECORD_COUNT

# Join offerings to materials (left join to keep offerings with or without materials)
off_mat = prepared_tip_offered.merge(
    prepared_tip_materials.drop(columns=["TERM_CODE"]),
    on="TIP_SUBJECT_OFFERED_KEY",
    how="left"
)

# Join to catalog to bring in term description (subject title used here)
off_mat_cat = off_mat.merge(
    prepared_subject_catalog,
    on=["TERM_CODE", "SUBJECT_ID"],
    how="left"
)

# Define helpers
# Current term flag: treat most recent TERM_CODE as current
term_order = off_mat_cat["TERM_CODE"].dropna().unique()
# If available, sort lexicographically which matches format like 2024SP/2016FA; adjust if custom order needed
current_term = pd.Series(term_order).sort_values().iloc[-1] if len(term_order) > 0 else None
off_mat_cat["IS_CURRENT_TERM"] = off_mat_cat["TERM_CODE"].eq(current_term)

# Aggregate per TERM_CODE
# - term description: choose the most frequent SUBJECT_TITLE in that term as a proxy
term_desc = (off_mat_cat
             .groupby(["TERM_CODE", "SUBJECT_TITLE"], dropna=False)
             .size()
             .reset_index(name="cnt"))
term_desc = term_desc.sort_values(["TERM_CODE", "cnt"], ascending=[True, False]).drop_duplicates(["TERM_CODE"])
term_desc = term_desc.rename(columns={"SUBJECT_TITLE": "TERM_DESCRIPTION"})[["TERM_CODE", "TERM_DESCRIPTION"]]

# Count distinct types of TIP subjects offered per term (distinct SUBJECT_ID)
subj_types = off_mat_cat.groupby("TERM_CODE")["SUBJECT_ID"].nunique().reset_index(name="TOTAL_TIP_SUBJECT_TYPES")

# Materials needed: count of offered subjects that have any material record not marked as NM (No Materials)
# If TIP_MATERIAL_STATUS_KEY == 'NM' means no materials; otherwise materials needed/present
materials_needed = (off_mat_cat.assign(has_material=lambda d: d["TIP_MATERIAL_STATUS_KEY"].notna() & d["TIP_MATERIAL_STATUS_KEY"].ne("NM"))
                    .groupby(["TERM_CODE", "SUBJECT_ID"], dropna=False)["has_material"].max()
                    .reset_index()
                    .groupby("TERM_CODE")["has_material"].sum()
                    .reset_index(name="MATERIALS_NEEDED_SUBJECTS"))

# Enrollment min/max per term
enroll_agg = off_mat_cat.groupby("TERM_CODE")["NUM_ENROLLED_STUDENTS"].agg(MIN_ENROLLED="min", MAX_ENROLLED="max").reset_index()

# Total number of schools offering subjects per term (distinct OFFER_SCHOOL_NAME)
schools = off_mat_cat.groupby("TERM_CODE")["OFFER_SCHOOL_NAME"].nunique().reset_index(name="TOTAL_SCHOOLS_OFFERING")

# Total number of records per term (row count in offerings table for that term)
# Use offered records (before exploding by materials) by counting distinct TIP_SUBJECT_OFFERED_KEY per term
offer_counts = prepared_tip_offered.groupby("TERM_CODE")["TIP_SUBJECT_OFFERED_KEY"].nunique().reset_index(name="TOTAL_RECORDS")

# Current term flag per term
current_flag = (off_mat_cat.groupby("TERM_CODE")["IS_CURRENT_TERM"].max().reset_index())

# Combine all pieces
result = (term_desc
          .merge(current_flag, on="TERM_CODE", how="left")
          .merge(subj_types, on="TERM_CODE", how="left")
          .merge(materials_needed, on="TERM_CODE", how="left")
          .merge(enroll_agg, on="TERM_CODE", how="left")
          .merge(schools, on="TERM_CODE", how="left")
          .merge(offer_counts, on="TERM_CODE", how="left")
         )

# Final columns as requested per term code
result = result[[
    "TERM_CODE",
    "TERM_DESCRIPTION",
    "IS_CURRENT_TERM",
    "TOTAL_TIP_SUBJECT_TYPES",
    "MATERIALS_NEEDED_SUBJECTS",
    "MIN_ENROLLED",
    "MAX_ENROLLED",
    "TOTAL_SCHOOLS_OFFERING",
    "TOTAL_RECORDS"
]].sort_values("TERM_CODE")

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
