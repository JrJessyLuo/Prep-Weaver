import pandas as pd

# Tables are preloaded in `tables`
demo_df = tables["table_1"].copy()  # demographics (Birthday, Diagnosis parts)
lab_df = tables["table_2"].copy()   # lab results (contains HGB)

# Ensure HGB is numeric
lab_df["HGB"] = pd.to_numeric(lab_df["HGB"], errors="coerce")

# Find maximum HGB (ignoring NaNs)
max_hgb = lab_df["HGB"].max()

# Get row(s) achieving the maximum HGB, capture ID and Date
max_hgb_rows = lab_df.loc[lab_df["HGB"] == max_hgb, ["ID", "Date", "HGB"]].copy()

# Parse dates
max_hgb_rows["Date"] = pd.to_datetime(max_hgb_rows["Date"], errors="coerce")
demo_df["Birthday"] = pd.to_datetime(demo_df["Birthday"], errors="coerce")

# Join on ID to bring in Birthday + diagnoses
joined = max_hgb_rows.merge(
    demo_df[["ID", "Birthday", "Diagnosis_Part1", "Diagnosis_Part2"]],
    on="ID",
    how="left"
)

# Compute age at examination (years)
joined["Age_at_Examination_years"] = (joined["Date"] - joined["Birthday"]).dt.days / 365.25

# Prepare final answer table
answer_df = joined[[
    "ID", "Date", "HGB",
    "Age_at_Examination_years",
    "Diagnosis_Part1", "Diagnosis_Part2"
]].copy()

# If desired, you can concatenate diagnosis parts into one column
answer_df["Doctor_Diagnosis"] = (
    answer_df["Diagnosis_Part1"].fillna("") + " " + answer_df["Diagnosis_Part2"].fillna("")
).str.strip().replace("", pd.NA)

answer_df = answer_df[[
    "ID", "Date", "HGB",
    "Age_at_Examination_years",
    "Doctor_Diagnosis"
]]

# Final result as required
result = {"highest_hgb_patient_age_and_diagnosis": answer_df}