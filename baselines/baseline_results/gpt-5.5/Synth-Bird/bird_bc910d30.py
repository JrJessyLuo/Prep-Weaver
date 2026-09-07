import pandas as pd

# --- Patients with ALP in normal range (using common reference range 44–147 U/L) ---
labs = tables["table_2"].copy()
alp_low, alp_high = 44.0, 147.0

normal_ids = (
    labs.loc[labs["ALP"].between(alp_low, alp_high, inclusive="both"), "ID"]
    .dropna()
    .astype(int)
    .unique()
)

# --- Get Admission (+/-) from table_1 (denormalized: first row=attribute, second row=value) ---
t1 = tables["table_1"].copy()
t1_wide = t1.set_index("ID").T  # index: patient IDs, columns: ['attribute','value']

admission = (
    t1_wide.loc[t1_wide["attribute"].eq("Admission"), ["value"]]
    .rename(columns={"value": "Admission"})
    .copy()
)
admission["CareSetting"] = admission["Admission"].map({"+": "Inpatient", "-": "Outpatient"})

admission = admission.reset_index().rename(columns={"index": "patient_id"})
admission["patient_id_num"] = pd.to_numeric(admission["patient_id"], errors="coerce")

normal_admission = admission.loc[
    admission["patient_id_num"].isin(normal_ids), ["patient_id_num", "CareSetting"]
].drop_duplicates()

out = (
    normal_admission.groupby("CareSetting", dropna=False)
    .agg(num_patients=("patient_id_num", "nunique"))
    .reset_index()
)

result = {"alp_normal_inpatient_outpatient": out}
