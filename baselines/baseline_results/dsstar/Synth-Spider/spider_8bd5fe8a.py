import pandas as pd

# Source DataFrames from provided tables dict
df_students = tables['table_1']
df_events = tables['table_2']

# Inner join on student_id to get students with at least one event
df_joined = df_students.merge(df_events, on="student_id", how="inner")

# Select desired columns
answer_df = df_joined[["bio_data", "student_id", "event_date"]]

# Package final result as specified
result = {
    "students_with_events": answer_df
}