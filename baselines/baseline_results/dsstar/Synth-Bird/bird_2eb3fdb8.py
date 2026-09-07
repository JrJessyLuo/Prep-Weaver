import pandas as pd

# -----------------------------
# 1) Load + reshape demographics so each patient is a row with parsed Birthday
# -----------------------------
demo_raw = tables["table_1"]

demo_long = (
    demo_raw
    .set_index("ID")     # rows are fields like SEX, Birthday, etc.
    .T                   # rows become patients (IDs), columns become fields
    .reset_index()
    .rename(columns={"index": "PatientID_raw"})
)

# Patient IDs are quoted strings like '"4526214"' -> normalize to ID (int)
demo_long["ID"] = (
    demo_long["PatientID_raw"]
    .astype(str)
    .str.replace('"', "", regex=False)
    .str.strip()
)
demo_long["ID"] = pd.to_numeric(demo_long["ID"], errors="coerce").astype("Int64")

# Parse Birthday
if "Birthday" in demo_long.columns:
    demo_long["Birthday"] = pd.to_datetime(demo_long["Birthday"], errors="coerce")
else:
    demo_long["Birthday"] = pd.NaT

demo_patients = demo_long[["ID", "Birthday"]].dropna(subset=["ID"])

# -----------------------------
# 2) Load labs, filter to October 1991, get distinct patient IDs
# -----------------------------
lab = tables["table_2"].copy()
lab["Date"] = pd.to_datetime(lab["Date"], errors="coerce")

lab_oct_1991 = lab.loc[
    (lab["Date"].dt.year == 1991) & (lab["Date"].dt.month == 10)
].copy()

oct_1991_ids = (
    lab_oct_1991[["ID"]]
    .dropna(subset=["ID"])
    .assign(ID=lambda d: pd.to_numeric(d["ID"], errors="coerce"))
    .dropna(subset=["ID"])
    .assign(ID=lambda d: d["ID"].astype("Int64"))
    .drop_duplicates()
)

# -----------------------------
# 3) Inner-join demographics to Oct-1991 IDs; compute age at 1999-12-31; keep non-null birthdays
# -----------------------------
age_asof = pd.Timestamp("1999-12-31")

oct_1991_with_bday = (
    oct_1991_ids
    .merge(demo_patients, on="ID", how="inner")
    .dropna(subset=["Birthday"])
)

oct_1991_with_bday["AgeAsOf_1999_12_31"] = (
    (age_asof - oct_1991_with_bday["Birthday"]).dt.days / 365.25
)

avg_age = oct_1991_with_bday["AgeAsOf_1999_12_31"].mean()

answer_df = pd.DataFrame({"AverageAgeAsOf_1999_12_31": [avg_age]})

# Final output (as required by guidelines)
result = {"average_age": answer_df}

print(avg_age)