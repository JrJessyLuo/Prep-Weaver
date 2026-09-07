import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# Earliest transcript issuance date -> student(s)
t1["date_of_transcript"] = pd.to_datetime(t1["date_of_transcript"], errors="coerce")
earliest_date = t1["date_of_transcript"].min()
earliest_students = (
    t1.loc[t1["date_of_transcript"].eq(earliest_date), ["student_id"]]
    .dropna()
    .drop_duplicates()
)

# Teacher ids (tid) who taught those student(s)
student_teachers = (
    t3.merge(earliest_students, on="student_id", how="inner")[["tid"]]
    .dropna()
    .drop_duplicates()
    .rename(columns={"tid": "teacher_id"})
)

# Pivot teacher details from key-value format into wide format
t2["detail_col"] = (
    t2["prefix"].fillna("").astype(str).str.strip() + "_" + t2["suffix"].fillna("").astype(str).str.strip()
).str.strip("_")
teacher_details = (
    t2.pivot_table(index="teacher_id", columns="detail_col", values="detail_value", aggfunc="first")
    .reset_index()
)

# Final result
out = (
    student_teachers.merge(teacher_details, on="teacher_id", how="left")
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"teachers_who_taught_earliest_transcript_student": out}
