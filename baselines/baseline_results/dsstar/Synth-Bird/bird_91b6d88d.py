import pandas as pd
import numpy as np

# Tables (already loaded in-scope)
map_df = tables["table_1"].copy()  # bird_91b6d88d_input_0.pkl
lab_df = tables["table_2"].copy()  # bird_91b6d88d_input_1.pkl

# -----------------------------
# Load lab DataFrame (TP lives here)
# -----------------------------
lab_df["ID"] = pd.to_numeric(lab_df["ID"], errors="coerce").astype("Int64")

# TP normal range (g/dL)
TP_LOW, TP_HIGH = 6.6, 8.2

# -----------------------------
# Load diagnosis/description mapping and find which ID category has diagnosis codes
# -----------------------------
map_df["ID_norm"] = map_df["ID"].astype(str).str.strip()

# Split "patient_id|value"
parts_all = map_df["column_id_value"].astype(str).str.split("|", n=1, expand=True)
map_df["patient_id"] = pd.to_numeric(parts_all[0], errors="coerce")
map_df["value_raw"] = parts_all[1] if parts_all.shape[1] > 1 else np.nan

# Normalize value strings
map_df["value_norm"] = (
    map_df["value_raw"]
    .astype(str)
    .str.strip()
    .replace({"nan": np.nan, "None": np.nan, "": np.nan, "NaN": np.nan})
)

# Diagnosis-like text heuristic:
val = map_df["value_norm"].astype("string")
has_letters = val.str.contains(r"[A-Za-z]", na=False)
is_date_like = val.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)
is_numeric_like = val.str.match(r"^\s*[-+]?\d+(\.\d+)?\s*$", na=False)

diag_like = map_df.loc[val.notna() & has_letters & ~is_date_like & ~is_numeric_like].copy()

# Pick the most likely diagnosis-code category: the ID category with the highest count of diagnosis-like values
id_diag_counts = diag_like.groupby("ID_norm").size().sort_values(ascending=False)
diag_id_category = None if id_diag_counts.empty else id_diag_counts.index[0]

# -----------------------------
# Re-parse that category and search for SJS including variants: SJS, SjS, Sjögren/Sjogren
# -----------------------------
if diag_id_category is None:
    sjs_patients = pd.Series([], dtype="Int64")
else:
    diag_df = map_df.loc[map_df["ID_norm"] == diag_id_category, ["patient_id", "value_norm"]].copy()

    sjs_pattern = r"(\bSJS\b|\bSjS\b|S[ji]ö?g?ren|Sjögren|Sjogren)"
    sjs_patients = (
        diag_df.loc[
            diag_df["patient_id"].notna()
            & diag_df["value_norm"].notna()
            & diag_df["value_norm"].astype(str).str.contains(sjs_pattern, case=False, regex=True),
            "patient_id",
        ]
        .dropna()
        .astype("Int64")
        .drop_duplicates()
    )

# -----------------------------
# Join to lab data and count distinct SJS patients with TP in normal range
# -----------------------------
sjs_lab = lab_df[lab_df["ID"].isin(sjs_patients)].copy()
tp_in_normal = sjs_lab["TP"].between(TP_LOW, TP_HIGH, inclusive="both")

distinct_sjs_patients_with_normal_tp = (
    sjs_lab.loc[tp_in_normal, "ID"].dropna().drop_duplicates().shape[0]
)

# Final answer table
answer_df = pd.DataFrame(
    {"distinct_sjs_patients_with_normal_total_protein": [int(distinct_sjs_patients_with_normal_tp)]}
)

result = {"answer": answer_df}