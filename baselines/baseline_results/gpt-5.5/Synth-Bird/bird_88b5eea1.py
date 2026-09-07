import pandas as pd
import numpy as np

# --- Load tables ---
t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# --- Clean/join keys ---
t1["patient_id_clean"] = (
    t1["patient_id"]
    .astype(str)
    .str.strip()
    .str.strip('"')
    .str.replace(r'^"|"$', "", regex=True)
)

t2["patient_id_clean"] = t2["ID"].astype(str)

# --- Extract sex from key-value table (table_1) ---
sex_rows = t1[t1["ID"].astype(str).str.contains(r"sex|gender", case=False, na=False)].copy()
sex_rows["sex_raw"] = sex_rows["value"].astype(str).str.strip()

sex_per_patient = (
    sex_rows.sort_values(["patient_id_clean"])
    .groupby("patient_id_clean", as_index=False)["sex_raw"]
    .agg(lambda s: s.dropna().iloc[0] if (s.dropna().shape[0] > 0) else np.nan)
)

def _is_male(x):
    s = str(x).strip().lower()
    if s in {"nan", "none", ""}:
        return False
    return (
        s.startswith("m")
        or "male" in s
        or s in {"1", "男", "男性", "ｍ", "m"}
    )

sex_per_patient["is_male"] = sex_per_patient["sex_raw"].map(_is_male)

# --- Determine normal/abnormal thresholds ---
# WBC normal range (common clinical): 4.0 - 10.0
wbc_low, wbc_high = 4.0, 10.0

# FG normal range depends on units; infer by magnitude if possible
fg_nonnull = t2["FG"].dropna()
if fg_nonnull.shape[0] > 0 and fg_nonnull.median() > 20:
    fg_low, fg_high = 200.0, 400.0  # mg/dL-like
else:
    fg_low, fg_high = 2.0, 4.0      # g/L-like

# --- Compute per-row flags on lab table and count distinct patients ---
labs = t2.merge(sex_per_patient[["patient_id_clean", "is_male"]], on="patient_id_clean", how="left")

labs["wbc_normal"] = labs["WBC"].between(wbc_low, wbc_high, inclusive="both")
labs["fg_abnormal"] = labs["FG"].notna() & ~labs["FG"].between(fg_low, fg_high, inclusive="both")

count_patients = (
    labs.loc[(labs["is_male"] == True) & (labs["wbc_normal"] == True) & (labs["fg_abnormal"] == True), "patient_id_clean"]
    .nunique()
)

result = {
    "male_patients_with_normal_wbc_and_abnormal_fibrinogen_count": pd.DataFrame(
        {"count": [int(count_patients)]}
    )
}
