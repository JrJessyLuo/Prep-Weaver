import pandas as pd
import numpy as np

# Tables are preloaded in `tables`
# tables['table_1'] = bird_70d2897d_input_0.pkl
# tables['table_2'] = bird_70d2897d_input_1.pkl (lab)
# tables['table_3'] = thrombosis_prediction_Examination.pkl (exam)

lab_df = tables["table_2"]
exam_df = tables["table_3"]
extra_df = tables["table_1"]

DOB_KEYWORDS = ("dob", "date of birth", "birth", "birthday", "born", "bday")

def find_dob_candidates(
    df: pd.DataFrame,
    df_name: str,
    id_col_candidates=("ID", "Id", "id", "patient_id", "PatientID", "PATIENT_ID"),
):
    cols = list(df.columns)
    id_cols = [c for c in cols if c in id_col_candidates]
    dob_cols = []
    for c in cols:
        cl = str(c).strip().lower()
        if any(k in cl for k in DOB_KEYWORDS):
            dob_cols.append(c)
    date_like_cols = [c for c in cols if "date" in str(c).strip().lower()]
    return {
        "df_name": df_name,
        "id_cols": id_cols,
        "dob_cols": dob_cols,
        "date_like_cols": date_like_cols,
        "all_cols": cols,
    }

lab_info = find_dob_candidates(lab_df, "lab_df")
exam_info = find_dob_candidates(exam_df, "exam_df")
extra_info = find_dob_candidates(extra_df, "extra_df")

# 1) Determine GPT cutoff (ALT ULN)
GPT_ULN = 40.0

# 2) Filter lab rows with GPT > cutoff
lab_filtered = lab_df.copy()
lab_filtered["ID"] = pd.to_numeric(lab_filtered["ID"], errors="coerce")
lab_filtered["Date"] = pd.to_datetime(lab_filtered["Date"], errors="coerce")
lab_filtered["GPT"] = pd.to_numeric(lab_filtered["GPT"], errors="coerce")

gpt_high_df = lab_filtered[lab_filtered["GPT"].notna() & (lab_filtered["GPT"] > GPT_ULN)].copy()

# Keep a single row per patient ID for joining (earliest lab date for that ID)
gpt_high_by_id = (
    gpt_high_df.sort_values(["ID", "Date"], ascending=[True, True])
    .drop_duplicates(subset=["ID"], keep="first")
    .copy()
)

# 3) Inspect for true DOB; join if present, otherwise confirm none and fall back
exam = exam_df.copy()
exam["ID"] = pd.to_numeric(exam["ID"], errors="coerce")

if "Examination Date" in exam.columns:
    exam["Examination Date"] = pd.to_datetime(exam["Examination Date"], errors="coerce")

dob_source_df = None
dob_col = None

for info, df in [(exam_info, exam), (lab_info, lab_filtered), (extra_info, extra_df)]:
    if len(info.get("id_cols", [])) == 0:
        continue
    if len(info.get("dob_cols", [])) > 0:
        dob_col = info["dob_cols"][0]
        dob_source_df = df
        break

exam_join_cols = ["ID"]
if "Diagnosis" in exam.columns:
    exam_join_cols.append("Diagnosis")
if "Examination Date" in exam.columns:
    exam_join_cols.append("Examination Date")

joined = gpt_high_by_id.merge(
    exam[exam_join_cols].drop_duplicates(subset=["ID"]),
    on="ID",
    how="left",
    suffixes=("", "_exam"),
)

if dob_source_df is not None and dob_col is not None and dob_col in dob_source_df.columns:
    dob_map = dob_source_df[["ID", dob_col]].copy()
    dob_map["ID"] = pd.to_numeric(dob_map["ID"], errors="coerce")
    dob_map[dob_col] = pd.to_datetime(dob_map[dob_col], errors="coerce")
    dob_map = dob_map.dropna(subset=["ID"]).drop_duplicates(subset=["ID"], keep="first")
    joined = joined.merge(dob_map, on="ID", how="left")
    joined["DOB"] = joined[dob_col]
else:
    joined["DOB"] = joined["Date"]
    if "Examination Date" in joined.columns:
        joined["DOB"] = joined["DOB"].fillna(joined["Examination Date"])

# 4) Sort by DOB ascending and select useful output columns
result_df = joined.sort_values(["DOB", "ID"], ascending=[True, True]).reset_index(drop=True)

out_cols = ["ID", "DOB"]
if "Diagnosis" in result_df.columns:
    out_cols.append("Diagnosis")
out_cols += ["GPT", "Date"]
if "Examination Date" in result_df.columns:
    out_cols.append("Examination Date")
if dob_col is not None and dob_col in result_df.columns and dob_col not in out_cols:
    out_cols.append(dob_col)

result_df = result_df[out_cols]

# Final answer as required
result = {"alt_gpt_high_patients_sorted_by_dob": result_df}