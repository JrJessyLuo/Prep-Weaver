import pandas as pd
import numpy as np

# --- Load input dataframes from in-scope `tables` dict ---
df_0 = tables["table_1"]
lab_df = tables["table_2"]

# --- Parse merged_ID_Attribute_Value into structured fields (demographics) ---
col = "merged_ID_Attribute_Value"
s = df_0[col].astype("string")

parts = s.str.split(r"\|\|\|", n=2, expand=True)
parts.columns = ["ID_raw", "Attribute", "Value"]

parts["ID"] = (
    parts["ID_raw"]
    .astype("string")
    .str.strip()
    .str.strip('"')
    .str.strip("'")
)
parts["Attribute"] = parts["Attribute"].astype("string").str.strip()
parts["Value"] = parts["Value"].astype("string").str.strip()

demog_long = parts.loc[
    parts["Attribute"].isin(["SEX", "Birthday"]),
    ["ID", "Attribute", "Value"]
].copy()

demog_wide = (
    demog_long
    .pivot_table(index="ID", columns="Attribute", values="Value", aggfunc="first")
    .reset_index()
)

for c in ["SEX", "Birthday"]:
    if c not in demog_wide.columns:
        demog_wide[c] = pd.NA

demog_wide["Birthday"] = pd.to_datetime(demog_wide["Birthday"], errors="coerce")
demog_wide["ID_int"] = pd.to_numeric(demog_wide["ID"], errors="coerce").astype("Int64")

patient_demographics = (
    demog_wide[["ID", "ID_int", "SEX", "Birthday"]]
    .sort_values(["ID_int", "ID"], na_position="last")
    .reset_index(drop=True)
)

# --- Join demographics to labs ---
lab = lab_df.copy()
lab["ID_int"] = pd.to_numeric(lab["ID"], errors="coerce").astype("Int64")

lab_with_demog = lab.merge(
    patient_demographics[["ID_int", "SEX", "Birthday"]],
    on="ID_int",
    how="left",
)

# --- Determine ALB normal reference range by inferring from the data distribution ---
alb = pd.to_numeric(lab_with_demog["ALB"], errors="coerce")
alb_valid = alb.dropna()

if alb_valid.empty:
    ALB_LOW, ALB_HIGH = np.nan, np.nan
else:
    q025, q975 = alb_valid.quantile([0.025, 0.975]).astype(float).tolist()
    span = q975 - q025
    pad = 0.05 * span if np.isfinite(span) and span > 0 else 0.0
    ALB_LOW = q025 - pad
    ALB_HIGH = q975 + pad

    if not (np.isfinite(ALB_LOW) and np.isfinite(ALB_HIGH)) or ALB_LOW >= ALB_HIGH:
        ALB_LOW, ALB_HIGH = alb_valid.min(), alb_valid.max()

# --- Apply out-of-range filter and deduplicate to one row per male patient ---
filtered = lab_with_demog.loc[
    (lab_with_demog["SEX"] == "M")
    & alb.notna()
    & ((alb < ALB_LOW) | (alb > ALB_HIGH))
].copy()

result_patient_ids = (
    filtered[["ID_int", "Birthday", "SEX"]]
    .drop_duplicates(subset=["ID_int"])
    .sort_values(["Birthday", "ID_int"], ascending=[False, True], na_position="last")
    .reset_index(drop=True)
)

# --- Final result ---
result = {"male_patients_alb_out_of_range_sorted_by_birthday_desc": result_patient_ids}