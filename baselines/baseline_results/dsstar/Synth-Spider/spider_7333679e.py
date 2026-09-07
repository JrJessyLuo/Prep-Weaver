import pandas as pd

# Tables are provided in a dict named `tables`
# Map inputs
transcripts_df = tables['table_1'].copy()
teachers_df = tables['table_2'].copy()   # columns: teacher_id, detail_value, prefix, suffix
classes_df = tables['table_3'].copy()    # columns: class_id, student_id, tid, cd

# Ensure date_of_transcript is datetime and get earliest student_id
transcripts_df['date_of_transcript'] = pd.to_datetime(transcripts_df['date_of_transcript'])
earliest_student_id = transcripts_df.sort_values('date_of_transcript', ascending=True).iloc[0]['student_id']

# Filter classes to the earliest student_id
classes_earliest = classes_df[classes_df['student_id'] == earliest_student_id].copy()

# Join classes with teachers on tid = teacher_id
joined = classes_earliest.merge(
    teachers_df,
    left_on='tid',
    right_on='teacher_id',
    how='left'
)

# Select and format unique teacher details
teacher_details = (
    joined[['teacher_id', 'detail_value', 'prefix', 'suffix']]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Assign to result as required
result = {
    "teacher_details_for_earliest_transcript_student": teacher_details
}