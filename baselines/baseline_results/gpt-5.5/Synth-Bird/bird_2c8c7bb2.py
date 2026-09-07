import pandas as pd
import numpy as np

patients = tables["table_1"].copy()
labs = tables["table_2"].copy()

# Outpatients: Admission == "-"
patients["Admission"] = patients["Admission"].astype(str).str.strip()
outpatients = patients[patients["Admission"] == "-"][["ID", "xb"]].copy()
outpatients["xb"] = outpatients["xb"].astype(str).str.strip().str.upper()

# Join labs to outpatients and identify low hemoglobin (sex-specific thresholds)
df = outpatients.merge(labs[["ID", "HGB"]], on="ID", how="inner")
df["HGB"] = pd.to_numeric(df["HGB"], errors="coerce")

threshold = df["xb"].map({"M": 13.0, "F": 12.0}).fillna(12.0)
low = df[df["HGB"].notna() & (df["HGB"] < threshold)]

out = (
    low[["ID", "xb"]]
    .drop_duplicates()
    .rename(columns={"xb": "sex"})
    .sort_values(["ID", "sex"])
    .reset_index(drop=True)
)

result = {"outpatients_low_hemoglobin": out}
