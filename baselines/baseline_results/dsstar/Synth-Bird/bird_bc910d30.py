import pandas as pd
import numpy as np

# ------------------------------------------------------------
# Tables already loaded in-scope as `tables`
#   table_1: bird_bc910d30_input_0.pkl (encounter-like, but appears to be a data dictionary)
#   table_2: bird_bc910d30_input_1.pkl (labs)
#   table_3: thrombosis_prediction_Examination.pkl (exam)
# ------------------------------------------------------------
df_enc = tables["table_1"]
df_labs = tables["table_2"]

# Helper: make encounter columns unique (matches reference logic)
def make_unique_columns(columns):
    seen = {}
    new_cols = []
    for c in columns:
        if c not in seen:
            seen[c] = 0
            new_cols.append(c)
        else:
            seen[c] += 1
            new_cols.append(f"{c}__dup{seen[c]}")
    return new_cols

df_enc_u = df_enc.copy()
df_enc_u.columns = make_unique_columns(df_enc_u.columns)

# ------------------------------------------------------------
# Identify patients with ALP within "normal range"
# The dataset does not provide explicit normal-range bounds, so we use the
# common adult reference interval: 38–126 U/L.
# ------------------------------------------------------------
alp = pd.to_numeric(df_labs["ALP"], errors="coerce")
labs_normal_alp = df_labs.loc[alp.between(38, 126, inclusive="both"), ["ID", "ALP"]].copy()
normal_ids = labs_normal_alp["ID"].dropna().unique()

# ------------------------------------------------------------
# Determine inpatient vs outpatient from encounter table.
# From reference execution, encounter DF has 2 rows and appears to be metadata/dictionary,
# with ID having 0 non-null unique values; thus we cannot map IDs to patient encounters.
# Also, no encounter-type field could be inferred.
# Therefore, treatment setting cannot be determined from available tables.
# ------------------------------------------------------------
answer_df = pd.DataFrame(
    {
        "question": ["For patients with ALP within normal range, were they treated as inpatient or outpatient?"],
        "status": ["Unknown (encounter table lacks patient encounter records / encounter-type indicator)"],
        "n_patients_with_normal_alp": [int(pd.Series(normal_ids).nunique())],
        "encounter_rows": [int(df_enc_u.shape[0])],
        "encounter_non_null_ids": [int(df_enc_u["ID"].notna().sum()) if "ID" in df_enc_u.columns else 0],
    }
)

result = {"alp_normal_inpatient_outpatient": answer_df}