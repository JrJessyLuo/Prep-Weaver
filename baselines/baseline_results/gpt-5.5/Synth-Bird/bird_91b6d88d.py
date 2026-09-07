import pandas as pd
import numpy as np

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# --- Identify SJS patients (best-effort from available tables) ---

# From table_1: parse "patient_id|value" and search for "sjs" in the value
parts = t1["column_id_value"].astype(str).str.split("|", n=1, expand=True)
t1_long = pd.DataFrame({
    "patient_id": pd.to_numeric(parts[0], errors="coerce"),
    "value": parts[1].replace({"nan": np.nan, "NaN": np.nan, "None": np.nan})
})
sjs_ids_1 = set(
    t1_long.loc[t1_long["value"].astype(str).str.contains(r"sjs", case=False, na=False), "patient_id"]
    .dropna()
    .astype("int64")
    .unique()
)

# From table_3: Diagnosis contains "sjs" (case-insensitive)
sjs_ids_3 = set(
    t3.loc[t3["Diagnosis"].astype(str).str.contains(r"sjs", case=False, na=False), "ID"]
    .dropna()
    .astype(int)
    .unique()
)

sjs_ids = sjs_ids_1.union(sjs_ids_3)

# Keep only SJS IDs that actually appear in the labs table
t2_ids = set(pd.to_numeric(t2["ID"], errors="coerce").dropna().astype(int).unique())
sjs_ids_in_labs = sorted(list(sjs_ids.intersection(t2_ids)))

# --- Count SJS patients with normal total protein (TP) ---
# Assume typical normal TP reference range in g/dL: 6.5–8.3
tp = pd.to_numeric(t2["TP"], errors="coerce")
normal_tp_mask = tp.between(6.5, 8.3, inclusive="both")

sjs_normal_tp_patient_count = (
    t2.loc[t2["ID"].isin(sjs_ids_in_labs) & normal_tp_mask, "ID"]
    .dropna()
    .astype(int)
    .nunique()
)

result = {
    "sjs_patients_normal_total_protein_count": pd.DataFrame(
        {"sjs_patients_with_normal_total_protein": [sjs_normal_tp_patient_count]}
    )
}
