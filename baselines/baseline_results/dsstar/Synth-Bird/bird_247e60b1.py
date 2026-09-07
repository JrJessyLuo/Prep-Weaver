import pandas as pd
import numpy as np

# --- Load cohort ---
df0 = tables["table_1"]

sle_patients = (
    df0[df0["Diagnosis"].astype(str).str.contains("SLE", case=False, na=False)]
    .loc[:, ["ID", "SEX", "combined_dates"]]
    .drop_duplicates(subset=["ID"])
    .reset_index(drop=True)
)

# --- Load labs ---
df1 = tables["table_2"].copy()

# --- Parse birthdate from earliest non-NA in combined_dates ---
def earliest_non_na_date(s):
    if pd.isna(s):
        return pd.NaT
    parts = [p.strip() for p in str(s).split("|")]
    parts = [p for p in parts if p and p.upper() != "NA"]
    if not parts:
        return pd.NaT
    dt = pd.to_datetime(parts, errors="coerce")
    if isinstance(dt, pd.DatetimeIndex):
        dt = dt.dropna()
        return dt.min() if len(dt) else pd.NaT
    return dt

sle_patients["birthdate"] = sle_patients["combined_dates"].apply(earliest_non_na_date)

# --- Merge SLE cohort with labs, compute age at lab date ---
df1["Date"] = pd.to_datetime(df1["Date"], errors="coerce")
labs_sle = df1.merge(sle_patients[["ID", "SEX", "birthdate"]], on="ID", how="inner")

labs_sle["SEX"] = labs_sle["SEX"].astype(str).str.upper().str.strip()
labs_sle = labs_sle.dropna(subset=["Date", "birthdate", "HGB", "SEX"]).copy()
labs_sle["age_years"] = (labs_sle["Date"] - labs_sle["birthdate"]).dt.days / 365.25

# --- Keep records with normal HGB (sex-specific) ---
normal_hgb = (
    ((labs_sle["SEX"] == "F") & (labs_sle["HGB"].between(12.0, 16.0, inclusive="both")))
    | ((labs_sle["SEX"] == "M") & (labs_sle["HGB"].between(13.5, 17.5, inclusive="both")))
)

labs_sle_norm = labs_sle.loc[normal_hgb].copy()

# --- Select patient with maximum age and return ID and SEX ---
answer_df = (
    labs_sle_norm.sort_values(["age_years", "ID"], ascending=[False, True])
    .loc[:, ["ID", "SEX"]]
    .head(1)
    .reset_index(drop=True)
)

result = {"oldest_sle_with_normal_hgb": answer_df}