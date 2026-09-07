import pandas as pd
import numpy as np

# -----------------------------
# Load input tables from `tables`
# -----------------------------
df_demo = tables["table_1"].copy()
df_labs = tables["table_2"].copy()

# -----------------------------
# Base code (previous plans)
# -----------------------------
# Parse Birthday to datetime
df_demo["Birthday"] = pd.to_datetime(df_demo["Birthday"], errors="coerce")

# Compute age (years) using today's date
today = pd.Timestamp.today().normalize()
df_demo["Age"] = (today - df_demo["Birthday"]).dt.days / 365.25

# Filter: female and age >= 50
df_filtered = df_demo[(df_demo["SEX"] == "F") & (df_demo["Age"] >= 50)].copy()

# -----------------------------
# Load lab results dataframe and find abnormal RBC
# -----------------------------
# Ensure merge keys are consistent
df_filtered["ID"] = pd.to_numeric(df_filtered["ID"], errors="coerce").astype("Int64")
df_labs["ID"] = pd.to_numeric(df_labs["ID"], errors="coerce").astype("Int64")

# Parse lab Date (optional but useful)
if "Date" in df_labs.columns:
    df_labs["Date"] = pd.to_datetime(df_labs["Date"], errors="coerce")

# Merge labs with filtered cohort
df_merged = df_filtered.merge(df_labs, on="ID", how="inner", suffixes=("_demo", "_lab"))

# Coerce RBC to numeric
if "RBC" not in df_merged.columns:
    raise KeyError("RBC column not found in lab results dataframe.")
df_merged["RBC"] = pd.to_numeric(df_merged["RBC"], errors="coerce")

# Define abnormal RBC using IQR-based bounds from merged cohort
rbc_series = df_merged["RBC"].dropna()
q1, q3 = rbc_series.quantile([0.25, 0.75])
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

df_abnormal_rbc = df_merged[
    df_merged["RBC"].notna()
    & ((df_merged["RBC"] < lower_bound) | (df_merged["RBC"] > upper_bound))
].copy()

# -----------------------------
# Current plan implementation
# -----------------------------
# Parse FirstDate_Admission and create Admitted flag:
# True if FirstDate_Admission is not missing and does not end with '|-'
fda = df_abnormal_rbc["FirstDate_Admission"].astype("string")
df_abnormal_rbc["Admitted"] = fda.notna() & (~fda.str.endswith("|-", na=False))

# Output: ID and Admitted
final_df = df_abnormal_rbc[["ID", "Admitted"]].drop_duplicates().reset_index(drop=True)

# Final answer as required by the evaluation convention
result = {"female_50plus_abnormal_rbc_admission_status": final_df}