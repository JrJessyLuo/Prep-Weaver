import pandas as pd

# --- Load tables ---
t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# --- Clean/standardize IDs ---
t1["ID_clean"] = pd.to_numeric(t1["ID"].astype(str).str.extract(r"(\d+)")[0], errors="coerce").astype("Int64")
t2["ID_clean"] = pd.to_numeric(t2["ID"], errors="coerce").astype("Int64")
t3["ID_clean"] = pd.to_numeric(t3["ID"], errors="coerce").astype("Int64")

# --- Identify MCTD patients (from any diagnosis table) ---
mctd_ids_1 = t1.loc[t1["Diagnosis"].astype(str).str.contains(r"\bMCTD\b", case=False, na=False), "ID_clean"]
mctd_ids_3 = t3.loc[t3["Diagnosis"].astype(str).str.contains(r"\bMCTD\b", case=False, na=False), "ID_clean"]

mctd_ids = pd.Index(
    pd.concat([mctd_ids_1, mctd_ids_3], ignore_index=True).dropna().unique()
)

# --- Filter platelet within normal range (assume 150-400) and diagnosed with MCTD ---
t2["PLT"] = pd.to_numeric(t2["PLT"], errors="coerce")
t2["Date"] = pd.to_datetime(t2["Date"], errors="coerce")

out = t2.loc[
    t2["ID_clean"].isin(mctd_ids) & t2["PLT"].between(150, 400, inclusive="both"),
    ["ID_clean", "Date", "PLT"]
].copy()

out = out.rename(columns={"ID_clean": "patient_id", "PLT": "platelet_level"})
out = out.sort_values(["patient_id", "Date"], na_position="last").reset_index(drop=True)

result = {"mctd_patients_normal_platelet_levels": out}
