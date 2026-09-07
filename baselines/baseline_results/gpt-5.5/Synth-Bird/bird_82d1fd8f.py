import pandas as pd
import numpy as np

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Normalize key fields
t1["Admission"] = t1["Admission"].astype(str).str.strip()
t1["SEX"] = t1["SEX"].astype(str).str.upper().str.strip()

t2["RBC"] = pd.to_numeric(t2["RBC"], errors="coerce")

# Join labs to patient table to get SEX / outpatient status
m = t2[["ID", "RBC"]].merge(t1[["ID", "SEX", "Admission"]], on="ID", how="inner")
m = m.dropna(subset=["RBC"])

# Sex-specific RBC reference ranges (adult, typical; units as in data)
low = np.select(
    [m["SEX"].eq("M"), m["SEX"].eq("F")],
    [4.2, 3.8],
    default=4.0
)
high = np.select(
    [m["SEX"].eq("M"), m["SEX"].eq("F")],
    [5.7, 5.2],
    default=5.5
)

m["abnormal_rbc"] = (m["RBC"] < low) | (m["RBC"] > high)
m["outpatient"] = m["Admission"].eq("-")

out = (
    m.loc[m["abnormal_rbc"] & m["outpatient"], ["ID"]]
    .drop_duplicates()
    .sort_values("ID")
    .reset_index(drop=True)
)

result = {"patients_with_abnormal_rbc_outpatient": out}
