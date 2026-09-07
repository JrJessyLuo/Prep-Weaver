import pandas as pd

# --- Admission status from table_1 (transposed wide format) ---
t1 = tables["table_1"]

adm_row = t1.loc[t1["ID"].astype(str).str.strip().eq("Admission")]
adm_long = adm_row.drop(columns=["ID"]).T.reset_index()
adm_long.columns = ["patient_id", "admission_raw"]

adm_long["admission_raw"] = adm_long["admission_raw"].astype(str).str.strip()
adm_long["admitted"] = adm_long["admission_raw"].str.startswith("+")

# --- Normal RNP from table_2 ---
t2 = tables["table_2"].copy()
t2["patient_id"] = t2["ID"].astype(str)

rnp = t2[["patient_id", "RNP"]].copy()
rnp["RNP"] = rnp["RNP"].astype(str).str.strip()

# interpret "normal" as negative
rnp["normal_rnp"] = rnp["RNP"].isin(["-", "0", "NEG", "NEGATIVE", "N"]) | rnp["RNP"].str.fullmatch(r"-+").fillna(False)

normal_by_patient = (
    rnp[rnp["RNP"].notna() & (rnp["RNP"].str.lower() != "nan")]
    .groupby("patient_id", as_index=False)["normal_rnp"]
    .any()
)

# --- Combine and count ---
merged = adm_long.merge(normal_by_patient, on="patient_id", how="inner")
count_val = int((merged["admitted"] & merged["normal_rnp"]).sum())

result = {
    "normal_rnp_and_admitted_patient_count": pd.DataFrame(
        {"num_patients": [count_val]}
    )
}
