import pandas as pd
import numpy as np

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# ---- Clean/join key (ID) ----
t1["ID_clean"] = (
    t1["ID"].astype(str)
    .str.replace('"', "", regex=False)
    .str.strip()
)
t1["ID_clean"] = pd.to_numeric(t1["ID_clean"], errors="coerce").astype("Int64")

t2["ID_clean"] = pd.to_numeric(t2["ID"], errors="coerce").astype("Int64")

# ---- Determine "came to hospital" date (earliest available of Description / First Date / Admission if date-like) ----
for col in ["Description", "First Date", "Admission"]:
    if col in t1.columns:
        t1[col + "_dt"] = pd.to_datetime(t1[col], errors="coerce")

t1["came_date"] = t1[[c for c in ["Description_dt", "First Date_dt", "Admission_dt"] if c in t1.columns]].min(axis=1)
t1_earliest = (
    t1.dropna(subset=["ID_clean"])
      .groupby("ID_clean", as_index=False)["came_date"].min()
)

early_ids = set(t1_earliest.loc[t1_earliest["came_date"] < pd.Timestamp("2000-01-01"), "ID_clean"])

# ---- Normal anti-SSA (negative/normal-like) ----
ssa = t2[["ID_clean", "SSA"]].copy()
ssa["SSA_str"] = ssa["SSA"].astype(str).str.strip().str.upper()

normal_tokens = {
    "-", "NEG", "NEGATIVE", "NORMAL", "N", "0", "0.0", "0.00", "(-)", "－"
}
ssa_normal_ids = set(
    ssa.loc[
        ssa["ID_clean"].notna()
        & ssa["SSA"].notna()
        & (ssa["SSA_str"].isin(normal_tokens)),
        "ID_clean"
    ]
)

count_patients = len(early_ids & ssa_normal_ids)

result = {
    "patients_with_normal_anti_SSA_before_2000": pd.DataFrame(
        {"patient_count": [count_patients]}
    )
}
