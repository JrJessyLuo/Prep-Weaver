import pandas as pd

# --- Demographics (sex, birthday) from table_1 key-value style ---
t1 = tables["table_1"].copy()
parts = t1["Sample_ID_Value"].astype(str).str.split("|", n=1, expand=True)
t1["patient_id"] = parts[0].astype(str).str.strip()
t1["val"] = parts[1] if parts.shape[1] > 1 else pd.NA

demo_wide = (
    t1.pivot_table(index="patient_id", columns="ID", values="val", aggfunc="first")
      .reset_index()
)

cols_lower = {c: str(c).lower() for c in demo_wide.columns}

sex_col = next((c for c, lc in cols_lower.items() if ("sex" in lc) or ("gender" in lc)), None)
bday_col = next(
    (c for c, lc in cols_lower.items() if ("birthday" in lc) or ("birth" in lc) or (lc in {"dob", "date of birth"})),
    None
)

demo = demo_wide[["patient_id"] + ([sex_col] if sex_col else []) + ([bday_col] if bday_col else [])].copy()
demo = demo.rename(columns={"patient_id": "ID"})
if sex_col:
    demo = demo.rename(columns={sex_col: "sex"})
else:
    demo["sex"] = pd.NA
if bday_col:
    demo = demo.rename(columns={bday_col: "birthday"})
else:
    demo["birthday"] = pd.NA

# Cast ID for joining
demo["ID_num"] = pd.to_numeric(demo["ID"], errors="coerce")

# --- Borderline passing for UN (assume normal upper limit 20; borderline within 1 unit: 19-20) ---
t2 = tables["table_2"].copy()
borderline_ids = (
    t2.loc[t2["UN"].between(19, 20, inclusive="both"), "ID"]
      .dropna()
      .drop_duplicates()
      .to_frame(name="ID_num")
)

# --- Final output ---
out = borderline_ids.merge(demo, on="ID_num", how="left")
out["ID"] = out["ID_num"].astype("Int64").astype(str)

out = out[["ID", "sex", "birthday"]].drop_duplicates().reset_index(drop=True)

result = {"patients_borderline_passing_un": out}
