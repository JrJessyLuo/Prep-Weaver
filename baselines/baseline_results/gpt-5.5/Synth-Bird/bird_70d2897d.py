import pandas as pd
import numpy as np
import re

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# ---- Parse table_1 packed field: "\"<ID>\"|<value>" ----
parts = t1["observation_id_value"].astype(str).str.split("|", n=1, expand=True)
t1["_id_str"] = parts[0].astype(str).str.replace('"', "", regex=False).str.replace(r"\D", "", regex=True)
t1["ID"] = pd.to_numeric(t1["_id_str"], errors="coerce").astype("Int64")
t1["value"] = np.where(parts.shape[1] > 1, parts[1], np.nan)
t1["value"] = pd.Series(t1["value"]).astype("string").str.strip().str.replace('"', "", regex=False)

t1_long = t1.dropna(subset=["ID"])[["ID", "feat_id", "value"]].copy()

# Pivot to patient-level features (if applicable)
wide = (
    t1_long.pivot_table(index="ID", columns="feat_id", values="value", aggfunc="first")
    .reset_index()
)

# Helper to find first matching column by regex
def _find_col(cols, pattern):
    rgx = re.compile(pattern, flags=re.IGNORECASE)
    hits = [c for c in cols if rgx.search(str(c))]
    return hits[0] if hits else None

alt_col = _find_col(wide.columns, r"\b(ALT|GPT)\b|glutamic\s*pylvic|alanine\s*aminotransferase|transaminase")
dob_col = _find_col(wide.columns, r"\b(dob|date\s*of\s*birth|birth\s*date|birthday)\b")
dx_col = _find_col(wide.columns, r"\bdiagnos")

# ---- Determine "ALT (GPT) beyond normal range" patient set ----
patients_flag = None

if alt_col is not None:
    s = wide[alt_col].astype("string").str.strip()
    # if encoded as + / - flags
    flag = s.str.upper().isin(["+", "-", "H", "L", "HIGH", "LOW"])
    if flag.any():
        patients_flag = wide.loc[flag, ["ID"]].copy()
    else:
        # else numeric threshold (use common upper limit 40)
        alt_num = pd.to_numeric(s, errors="coerce")
        patients_flag = wide.loc[alt_num > 40, ["ID"]].copy()

if patients_flag is None:
    # fallback: use table_2 GPT numeric > 40
    t2_gpt = t2.copy()
    t2_gpt["ID"] = pd.to_numeric(t2_gpt["ID"], errors="coerce").astype("Int64")
    t2_gpt["GPT"] = pd.to_numeric(t2_gpt["GPT"], errors="coerce")
    max_gpt = t2_gpt.groupby("ID", as_index=False)["GPT"].max()
    patients_flag = max_gpt.loc[max_gpt["GPT"] > 40, ["ID"]].copy()

# ---- Build patient info: DOB + Diagnosis ----
out = patients_flag.drop_duplicates().copy()

# DOB from wide if present
if dob_col is not None:
    tmp = wide[["ID", dob_col]].copy()
    tmp = tmp.rename(columns={dob_col: "Date_of_birth"})
    tmp["Date_of_birth"] = pd.to_datetime(tmp["Date_of_birth"], errors="coerce")
    out = out.merge(tmp, on="ID", how="left")
else:
    out["Date_of_birth"] = pd.NaT

# Diagnosis from wide if present, else from table_3
if dx_col is not None:
    tmp = wide[["ID", dx_col]].copy().rename(columns={dx_col: "Diagnosis"})
    out = out.merge(tmp, on="ID", how="left")
else:
    t3_tmp = t3.copy()
    t3_tmp["ID"] = pd.to_numeric(t3_tmp["ID"], errors="coerce").astype("Int64")
    t3_tmp = t3_tmp[["ID", "Diagnosis"]].drop_duplicates()
    out = out.merge(t3_tmp, on="ID", how="left")

# Sort by DOB ascending (NaT last), then ID for stability
out = out.sort_values(["Date_of_birth", "ID"], ascending=[True, True], na_position="last")

# Final selection
out = out[["ID", "Date_of_birth", "Diagnosis"]].reset_index(drop=True)

result = {"diagnosis_patients_alt_beyond_normal_sorted_by_dob": out}
