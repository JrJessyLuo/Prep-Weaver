import pandas as pd
import numpy as np

# Input tables (already loaded)
patients = tables["table_1"]
lab = tables["table_2"]

# --- Reproduce reference-code logic to determine GOT (AST) normal range ---
ref_keywords = (
    "ref", "range", "normal", "lower", "upper", "min", "max", "low", "high", "lln", "uln",
    "reference", "interval", "limit", "bounds"
)
ref_cols = [c for c in lab.columns if any(k in str(c).lower() for k in ref_keywords)]

normal_got_low = np.nan
normal_got_high = np.nan
used_external_reference_range = False
got_range_source = None

if ref_cols:
    cols_lower = [c for c in ref_cols if any(k in str(c).lower() for k in ("lower", "low", "min", "lln"))]
    cols_upper = [c for c in ref_cols if any(k in str(c).lower() for k in ("upper", "high", "max", "uln"))]

    got_like = ("got", "ast")
    cols_lower_got = [c for c in cols_lower if any(k in str(c).lower() for k in got_like)]
    cols_upper_got = [c for c in cols_upper if any(k in str(c).lower() for k in got_like)]

    lower_col = cols_lower_got[0] if cols_lower_got else (cols_lower[0] if cols_lower else None)
    upper_col = cols_upper_got[0] if cols_upper_got else (cols_upper[0] if cols_upper else None)

    if lower_col is not None and upper_col is not None:
        low_vals = pd.to_numeric(lab[lower_col], errors="coerce")
        high_vals = pd.to_numeric(lab[upper_col], errors="coerce")
        if low_vals.notna().any() and high_vals.notna().any():
            normal_got_low = float(low_vals.dropna().median())
            normal_got_high = float(high_vals.dropna().median())
            got_range_source = {"type": "dataset_columns", "lower_col": lower_col, "upper_col": upper_col}
        else:
            used_external_reference_range = True
    else:
        used_external_reference_range = True
else:
    used_external_reference_range = True

if used_external_reference_range or not np.isfinite(normal_got_low) or not np.isfinite(normal_got_high):
    normal_got_low = 10.0
    normal_got_high = 40.0
    got_range_source = {"type": "external_fixed_reference", "note": "Common adult AST(GOT) reference interval"}

# --- Identify likely columns for AST/GOT values and exam date, plus patient ID link ---
lab_cols_lower = {c: str(c).lower() for c in lab.columns}

# Patient ID column in lab
pid_candidates = [c for c, cl in lab_cols_lower.items() if cl in ("patient_id", "pat_id", "pid", "subject_id", "id")]
if not pid_candidates:
    pid_candidates = [c for c, cl in lab_cols_lower.items() if "patient" in cl and "id" in cl]
lab_pid_col = pid_candidates[0] if pid_candidates else lab.columns[0]

# Exam date column in lab
date_candidates = [c for c, cl in lab_cols_lower.items() if "date" in cl or "time" in cl]
lab_date_col = date_candidates[0] if date_candidates else None

# GOT/AST value column in lab
got_candidates = [c for c, cl in lab_cols_lower.items() if ("got" in cl or "ast" in cl) and any(k in cl for k in ("value", "result", "index", "val"))]
if not got_candidates:
    got_candidates = [c for c, cl in lab_cols_lower.items() if ("got" in cl or "ast" in cl)]
lab_got_col = got_candidates[0] if got_candidates else None

# --- Filter lab records to year 1994 and normal GOT range ---
lab_filt = lab.copy()

if lab_date_col is not None:
    lab_filt["_exam_date"] = pd.to_datetime(lab_filt[lab_date_col], errors="coerce")
    lab_filt = lab_filt[lab_filt["_exam_date"].dt.year == 1994]
else:
    # If no date column exists, can't apply "in 1994"; produce empty set
    lab_filt = lab_filt.iloc[0:0].copy()
    lab_filt["_exam_date"] = pd.NaT

if lab_got_col is not None:
    lab_filt["_got"] = pd.to_numeric(lab_filt[lab_got_col], errors="coerce")
    lab_filt = lab_filt[lab_filt["_got"].between(normal_got_low, normal_got_high, inclusive="both")]
else:
    lab_filt = lab_filt.iloc[0:0].copy()
    lab_filt["_got"] = np.nan

# Distinct patients meeting criteria
eligible_ids = (
    lab_filt[[lab_pid_col]]
    .dropna()
    .drop_duplicates()
    .rename(columns={lab_pid_col: "_patient_id"})
)

# --- Select patient columns: sex + date of birth ---
pat_cols_lower = {c: str(c).lower() for c in patients.columns}

# patient id in patients
pat_id_candidates = [c for c, cl in pat_cols_lower.items() if cl in ("patient_id", "pat_id", "pid", "subject_id", "id")]
if not pat_id_candidates:
    pat_id_candidates = [c for c, cl in pat_cols_lower.items() if "patient" in cl and "id" in cl]
pat_pid_col = pat_id_candidates[0] if pat_id_candidates else patients.columns[0]

# sex column
sex_candidates = [c for c, cl in pat_cols_lower.items() if cl in ("sex", "gender") or "sex" in cl or "gender" in cl]
pat_sex_col = sex_candidates[0] if sex_candidates else None

# dob column
dob_candidates = [c for c, cl in pat_cols_lower.items() if cl in ("dob", "date_of_birth", "birth_date", "birthday") or ("birth" in cl and "date" in cl)]
pat_dob_col = dob_candidates[0] if dob_candidates else None

patients_sel = patients.copy()
patients_sel["_patient_id"] = patients_sel[pat_pid_col]

out = eligible_ids.merge(patients_sel, on="_patient_id", how="inner")

# Build final answer table
cols_out = ["_patient_id"]
rename_map = {"_patient_id": "patient_id"}

if pat_sex_col is not None:
    cols_out.append(pat_sex_col)
    rename_map[pat_sex_col] = "sex"
if pat_dob_col is not None:
    cols_out.append(pat_dob_col)
    rename_map[pat_dob_col] = "date_of_birthday"

answer_df = out.loc[:, cols_out].rename(columns=rename_map).drop_duplicates()

# Standardize DOB to datetime if present
if "date_of_birthday" in answer_df.columns:
    answer_df["date_of_birthday"] = pd.to_datetime(answer_df["date_of_birthday"], errors="coerce").dt.date

answer_df = answer_df.sort_values(by=["patient_id"]).reset_index(drop=True)

# Final result (per guideline)
result = {"patients_normal_ast_got_1994": answer_df}