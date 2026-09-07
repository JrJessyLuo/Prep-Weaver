import pandas as pd

students = tables["table_1"].copy()
events = tables["table_2"].copy()

# Parse event_date with mixed formats
dt1 = pd.to_datetime(events["event_date"], errors="coerce", dayfirst=True)
dt2 = pd.to_datetime(events["event_date"], errors="coerce", dayfirst=False)
events["event_date"] = dt1.fillna(dt2)

out = (
    events.merge(students, on="student_id", how="inner")
    .loc[:, ["student_id", "bio_data", "residence_type", "residence_number", "event_date"]]
    .sort_values(["student_id", "event_date"], na_position="last")
    .reset_index(drop=True)
)

result = {"students_with_events": out}
