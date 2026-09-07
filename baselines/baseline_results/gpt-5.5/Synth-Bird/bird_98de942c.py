import pandas as pd

patient_id = 30609

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# --- Diagnosis (prefer table_1 zd_part1-4; fallback to table_3 Diagnosis) ---
t1["ID"] = pd.to_numeric(t1["ID"], errors="coerce").astype("Int64")
zd_cols = [c for c in ["zd_part1", "zd_part2", "zd_part3", "zd_part4"] if c in t1.columns]

diag_vals = []
if zd_cols:
    t1_pid = t1.loc[t1["ID"] == patient_id, zd_cols]
    if not t1_pid.empty:
        diag_vals = (
            pd.unique(t1_pid.stack(dropna=True).astype(str).str.strip())
            .tolist()
        )
        diag_vals = [d for d in diag_vals if d and d.lower() not in ("nan", "none", "null", "-")]

if not diag_vals and "ID" in t3.columns and "Diagnosis" in t3.columns:
    t3["ID"] = pd.to_numeric(t3["ID"], errors="coerce")
    t3_pid = t3.loc[t3["ID"] == float(patient_id), "Diagnosis"].dropna().astype(str)
    if not t3_pid.empty:
        diag_vals = (
            pd.Series(t3_pid.str.split(r"\s*,\s*").sum())
            .astype(str).str.strip()
            .loc[lambda s: s.ne("") & ~s.str.lower().isin(["nan", "none", "null", "-"])]
            .drop_duplicates()
            .tolist()
        )

diagnosis_str = ", ".join(diag_vals) if diag_vals else pd.NA

# --- Lab test dates from table_2 ---
t2["ID"] = pd.to_numeric(t2["ID"], errors="coerce").astype("Int64")
t2["Date"] = pd.to_datetime(t2["Date"], errors="coerce")

lab_dates = (
    t2.loc[t2["ID"] == patient_id, "Date"]
      .dropna()
      .drop_duplicates()
      .sort_values()
      .dt.strftime("%Y-%m-%d")
      .tolist()
)

out = pd.DataFrame(
    [{
        "patient_id": str(patient_id),
        "diagnosis": diagnosis_str,
        "laboratory_test_dates": lab_dates
    }]
)

result = {"patient_30609_diagnosis_and_lab_dates": out}
