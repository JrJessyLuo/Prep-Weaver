import pandas as pd
import numpy as np

df0 = tables["table_1"]
df2 = tables["table_3"]

# --- Re-parse APTT to numeric (strip non-numeric symbols, coerce errors) ---
aptt_raw = df2["APTT"] if "APTT" in df2.columns else pd.Series([np.nan] * len(df2), index=df2.index)
aptt_str = aptt_raw.astype(str).str.strip()

# Keep digits/decimal/sign only; remove units/symbols and other artifacts.
aptt_clean = (
    aptt_str
    .str.replace(",", ".", regex=False)
    .str.replace(r"[^0-9\.\-\+]", "", regex=True)
)
aptt_num = pd.to_numeric(aptt_clean, errors="coerce")

# --- Define abnormal APTT outside standard reference range (<25 or >35 seconds) ---
low_ref, high_ref = 25.0, 35.0
abn_mask = aptt_num.notna() & ((aptt_num < low_ref) | (aptt_num > high_ref))

abn_aptt = df2.loc[abn_mask, ["ID", "Date", "APTT"]].copy()
abn_aptt["APTT_num"] = aptt_num.loc[abn_aptt.index]

# --- Prepare IDs for joining (robust to float/int/object differences) ---
def normalize_id(series: pd.Series) -> pd.Series:
    s = series.copy()
    s = s.replace({'"': ""}, regex=True)

    num = pd.to_numeric(s, errors="coerce")
    out = np.where(
        pd.notna(num),
        num.astype("Int64").astype(str),
        s.astype(str)
    )
    out = pd.Series(out, index=series.index).str.strip()
    out = out.replace({"<NA>": np.nan, "nan": np.nan, "None": np.nan})
    return out

df0_join = df0.copy()
df0_join["ID_norm"] = normalize_id(df0_join["ID"])

abn_aptt_join = abn_aptt.copy()
abn_aptt_join["ID_norm"] = normalize_id(abn_aptt_join["ID"])
abn_aptt_join = abn_aptt_join.dropna(subset=["ID_norm"])

# Distinct abnormal-APTT patient set
abn_patients = abn_aptt_join[["ID_norm"]].drop_duplicates()

# --- Join to thrombosis and count distinct patients with Thrombosis == "0" ---
merged = df0_join.merge(abn_patients, on="ID_norm", how="inner")

thrombosis_clean = merged["Thrombosis"].astype(str).str.strip().str.replace('"', '', regex=False)
mask_th0 = thrombosis_clean == "0"
distinct_patients_th0 = merged.loc[mask_th0, "ID_norm"].nunique(dropna=True)

answer_df = pd.DataFrame({"patients_without_thrombosis": [int(distinct_patients_th0)]})

result = {"answer": answer_df}