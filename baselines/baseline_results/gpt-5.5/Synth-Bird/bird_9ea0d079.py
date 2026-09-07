import pandas as pd
import numpy as np

# --- Patient sex table (table_1 is key-value style) ---
t1 = tables["table_1"].copy()

# Reconstruct an ID from prefix + id_core + suffix by extracting digits
def _digits(x):
    if pd.isna(x):
        return ""
    return "".join(pd.Series([str(x)]).str.findall(r"\d+").iloc[0])

t1["patient_id"] = (
    t1["prefix"].map(_digits).astype(str)
    + t1["id_core"].map(_digits).astype(str)
    + t1["suffix"].map(_digits).astype(str)
)
t1["patient_id"] = t1["patient_id"].replace("", np.nan)

patients = (
    t1.dropna(subset=["patient_id"])
      .pivot_table(index="patient_id", columns="attr", values="val", aggfunc="first")
      .reset_index()
)

patients["ID"] = pd.to_numeric(patients["patient_id"], errors="coerce").astype("Int64")
patients["SEX"] = (
    patients.get("SEX", pd.Series([pd.NA] * len(patients)))
    .astype(str).str.strip().str.upper()
    .replace({"MALE": "M", "FEMALE": "F"})
)
patients = patients.dropna(subset=["ID"])[["ID", "SEX"]].drop_duplicates("ID")

# --- Lab table with UA (table_2) ---
labs = tables["table_2"].copy()
labs["ID"] = pd.to_numeric(labs["ID"], errors="coerce").astype("Int64")
labs["UA"] = pd.to_numeric(labs["UA"], errors="coerce")

labs = labs.merge(patients, on="ID", how="left")

# Sex-specific normal ranges (mg/dL), mark abnormal if outside range
lower = np.select([labs["SEX"].eq("M"), labs["SEX"].eq("F")], [3.6, 2.6], default=2.6)
upper = np.select([labs["SEX"].eq("M"), labs["SEX"].eq("F")], [7.2, 6.0], default=7.2)

labs["ua_abnormal"] = labs["UA"].notna() & ((labs["UA"] < lower) | (labs["UA"] > upper))

abnormal_patients = (
    labs.groupby("ID", as_index=False)
        .agg(ua_abnormal=("ua_abnormal", "any"), SEX=("SEX", "first"))
)
abnormal_patients = abnormal_patients[abnormal_patients["ua_abnormal"]]

sex_counts = abnormal_patients["SEX"].value_counts(dropna=False)
male_cnt = int(sex_counts.get("M", 0))
female_cnt = int(sex_counts.get("F", 0))
ratio = (male_cnt / female_cnt) if female_cnt != 0 else np.nan

out = pd.DataFrame(
    [{
        "male_patients": male_cnt,
        "female_patients": female_cnt,
        "male_to_female_ratio": ratio
    }]
)

result = {"male_female_ratio_abnormal_uric_acid": out}
