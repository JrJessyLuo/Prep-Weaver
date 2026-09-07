import pandas as pd
import numpy as np

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Parse dates
t1["Birthday"] = pd.to_datetime(t1["Birthday"], errors="coerce")
t2["Date"] = pd.to_datetime(t2["Date"], errors="coerce")

# Admission flag from "FirstDate_Admission" (e.g., "1996-01-25|+")
adm_str = t1["FirstDate_Admission"].astype(str)
t1["admitted_to_hospital"] = adm_str.str.contains(r"\|\+", regex=True, na=False)

# Join demographics + labs
df = t2.merge(
    t1[["ID", "SEX", "Birthday", "admitted_to_hospital"]],
    on="ID",
    how="inner"
)

# Age at lab date
df["age"] = np.floor((df["Date"] - df["Birthday"]).dt.days / 365.25)

# Abnormal RBC definition (adult female typical range approx. 3.8–5.2)
df["abnormal_rbc"] = df["RBC"].notna() & ((df["RBC"] < 3.8) | (df["RBC"] > 5.2))

# Filter: female, age >= 50, abnormal RBC
df_filt = df[(df["SEX"].eq("F")) & (df["age"] >= 50) & (df["abnormal_rbc"])].copy()

# Keep earliest abnormal record per patient
df_filt = df_filt.sort_values(["ID", "Date"], ascending=[True, True])
out = df_filt.drop_duplicates(subset=["ID"], keep="first")[
    ["ID", "Date", "age", "RBC", "admitted_to_hospital"]
].rename(columns={"Date": "lab_date", "RBC": "rbc"})

result = {"female_50plus_abnormal_rbc_admission_status": out.reset_index(drop=True)}
