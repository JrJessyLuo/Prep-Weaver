import pandas as pd

materials = tables["table_1"].copy()
statuses = tables["table_2"].copy()
offerings = tables["table_5"].copy()

# Normalize keys
materials["_status_key"] = materials["TIP_MATERIAL_STATUS_KEY"].astype("string").str.strip().str.upper()
statuses["_status_key"] = statuses["tip_material_status_key"].astype("string").str.strip().str.upper()

# Join TIP material status descriptions
status_dim = statuses[["_status_key", "TIP_MATERIAL_STATUS"]].drop_duplicates("_status_key")
df = materials.merge(status_dim, on="_status_key", how="left")

# Display null/blank material statuses as requested
df["TIP_MATERIAL_STATUS"] = (
    df["TIP_MATERIAL_STATUS"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
    .fillna("No material status")
)

# Normalize material key for distinct counts
df["_material_key"] = (
    df["TIP_MATERIAL_KEY"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
)

# Normalize record count
df["_record_count"] = pd.to_numeric(df["RECORD_COUNT"], errors="coerce").fillna(0)

# Join enrollment from TIP subject offerings
df["_offered_key"] = df["TIP_SUBJECT_OFFERED_KEY"].astype("string").str.strip().str.upper()
offerings["_offered_key"] = offerings["TIP_SUBJECT_OFFERED_KEY"].astype("string").str.strip().str.upper()

enrollment_by_key = (
    offerings.dropna(subset=["_offered_key"])
    .groupby("_offered_key")["NUM_ENROLLED_STUDENTS"]
    .max()
)

df["_enrollment"] = df["_offered_key"].map(enrollment_by_key)

# Fallback enrollment lookup by term + subject when subject offered key is unavailable
df["_term_code"] = df["TERM_CODE"].astype("string").str.strip().str.upper()
df["_subject_id"] = df["subject_id"].astype("string").str.strip().str.upper()

term_subject_sources = []

offerings["_term_code"] = offerings["TERM_CODE"].astype("string").str.strip().str.upper()
offerings["_subject_id"] = offerings["SUBJECT_ID"].astype("string").str.strip().str.upper()
term_subject_sources.append(
    offerings[["_term_code", "_subject_id", "NUM_ENROLLED_STUDENTS"]]
)

if "table_9" in tables:
    subject_summary = tables["table_9"].copy()
    subject_summary["_term_code"] = subject_summary["TERM_CODE"].astype("string").str.strip().str.upper()
    subject_summary["_subject_id"] = subject_summary["SUBJECT_ID"].astype("string").str.strip().str.upper()
    term_subject_sources.append(
        subject_summary[["_term_code", "_subject_id", "NUM_ENROLLED_STUDENTS"]]
    )

term_subject_enrollment = pd.concat(term_subject_sources, ignore_index=True)
enrollment_by_term_subject = (
    term_subject_enrollment.dropna(subset=["_term_code", "_subject_id"])
    .groupby(["_term_code", "_subject_id"])["NUM_ENROLLED_STUDENTS"]
    .max()
)

missing_enrollment = df["_enrollment"].isna()
if missing_enrollment.any():
    lookup_index = pd.MultiIndex.from_frame(df.loc[missing_enrollment, ["_term_code", "_subject_id"]])
    df.loc[missing_enrollment, "_enrollment"] = enrollment_by_term_subject.reindex(lookup_index).to_numpy()

df["_enrollment"] = pd.to_numeric(df["_enrollment"], errors="coerce").fillna(0)

# Aggregate by material status
summary = (
    df.groupby("TIP_MATERIAL_STATUS", as_index=False)
    .agg(
        TOTAL_UNIQUE_MATERIALS=("_material_key", lambda s: s.nunique(dropna=True)),
        TOTAL_RECORDS=("_record_count", "sum"),
        TOTAL_STUDENT_ENROLLMENT=("_enrollment", "sum"),
    )
    .sort_values("TIP_MATERIAL_STATUS")
    .reset_index(drop=True)
)

# Add grand total row
grand_total = pd.DataFrame([{
    "TIP_MATERIAL_STATUS": "Grand Total",
    "TOTAL_UNIQUE_MATERIALS": df["_material_key"].nunique(dropna=True),
    "TOTAL_RECORDS": df["_record_count"].sum(),
    "TOTAL_STUDENT_ENROLLMENT": df["_enrollment"].sum(),
}])

final = pd.concat([summary, grand_total], ignore_index=True)

# Clean numeric output types
final["TOTAL_UNIQUE_MATERIALS"] = final["TOTAL_UNIQUE_MATERIALS"].astype("int64")
final["TOTAL_RECORDS"] = final["TOTAL_RECORDS"].astype("int64")
final["TOTAL_STUDENT_ENROLLMENT"] = final["TOTAL_STUDENT_ENROLLMENT"].astype("int64")

result = {
    "tip_material_status_summary": final
}
