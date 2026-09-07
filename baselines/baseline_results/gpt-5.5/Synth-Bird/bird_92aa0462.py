import pandas as pd
import numpy as np

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Find the examination (lab) record with the highest hemoglobin (HGB)
t2["Date"] = pd.to_datetime(t2["Date"], errors="coerce")
t2["HGB"] = pd.to_numeric(t2["HGB"], errors="coerce")
top_hgb_row = (
    t2.dropna(subset=["HGB"])
      .sort_values(["HGB", "Date"], ascending=[False, True])
      .head(1)
      .loc[:, ["ID", "Date", "HGB"]]
)

# Prepare demographics + diagnosis
t1["Birthday"] = pd.to_datetime(t1["Birthday"], errors="coerce")
t1["Diagnosis_Part1"] = t1["Diagnosis_Part1"].astype("string")
t1["Diagnosis_Part2"] = t1["Diagnosis_Part2"].astype("string")

t1["doctor_diagnosis"] = (
    t1["Diagnosis_Part1"].fillna("").str.strip()
    + np.where(t1["Diagnosis_Part2"].fillna("").str.strip().ne(""),
               ", " + t1["Diagnosis_Part2"].fillna("").str.strip(),
               "")
).str.strip().replace({"": pd.NA})

demo = t1[["ID", "Birthday", "doctor_diagnosis"]].drop_duplicates(subset=["ID"], keep="first")

# Join and compute age at examination date
merged = top_hgb_row.merge(demo, on="ID", how="left")
merged["age_at_examination"] = np.floor(
    (merged["Date"] - merged["Birthday"]).dt.days / 365.25
).astype("Int64")

out = merged[["age_at_examination", "doctor_diagnosis"]].rename(
    columns={"doctor_diagnosis": "doctor_diagnosis"}
).reset_index(drop=True)

result = {"patient_age_and_diagnosis": out}
