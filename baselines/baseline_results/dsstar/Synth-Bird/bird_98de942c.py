import pandas as pd

# Tables are already loaded in-scope as `tables`
demo_df = tables["table_1"]
labs_df = tables["table_2"]

patient_id = 30609

# --- Diagnose diseases (same logic as reference code) ---
patient_demo = demo_df.loc[demo_df["ID"] == patient_id].copy()

def _clean_val(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    if s == "" or s.lower() in {"none", "nan"}:
        return None
    return s

diag_parts = []
for col in ["zd_part1", "zd_part2", "zd_part3", "zd_part4"]:
    if col in patient_demo.columns:
        vals = patient_demo[col].map(_clean_val).dropna().unique().tolist()
        diag_parts.extend(vals)

seen = set()
diagnosed_diseases = []
for d in diag_parts:
    if d not in seen:
        seen.add(d)
        diagnosed_diseases.append(d)

disease_df = pd.DataFrame(
    {"ID": [patient_id], "Diagnosed disease(s)": [", ".join(diagnosed_diseases) if diagnosed_diseases else None]}
)

# --- Laboratory test dates for this patient ---
patient_labs = labs_df.loc[labs_df["ID"] == patient_id].copy()

# Identify the most likely date column
date_col = None
for c in ["Date", "date", "EXAM_DATE", "exam_date", "test_date", "TEST_DATE", "Datetime", "datetime", "Time", "time"]:
    if c in patient_labs.columns:
        date_col = c
        break

if date_col is None:
    # Fallback: pick first datetime-like column if present
    datetime_cols = patient_labs.select_dtypes(include=["datetime64[ns]", "datetime64[ns, UTC]"]).columns.tolist()
    if len(datetime_cols) > 0:
        date_col = datetime_cols[0]

if date_col is None:
    lab_dates_df = pd.DataFrame({"ID": [patient_id], "Lab test dates": [None]})
else:
    dates = pd.to_datetime(patient_labs[date_col], errors="coerce")
    unique_dates = (
        pd.Series(dates.dropna().dt.date.unique())
        .sort_values()
        .astype(str)
        .tolist()
    )
    lab_dates_df = pd.DataFrame({"ID": [patient_id], "Lab test dates": [unique_dates]})

# Final answer tables
result = {
    "diagnosis": disease_df,
    "lab_test_dates": lab_dates_df,
}