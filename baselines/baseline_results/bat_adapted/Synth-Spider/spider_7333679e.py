import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['transcript_id','student_id','date_of_transcript']].copy()
    target['date_of_transcript'] = pd.to_datetime(target['date_of_transcript'], errors='coerce')
    target = target[['transcript_id','student_id','date_of_transcript']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['student_id','tid','class_id','cd']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.loc[(table_1['prefix'] == 'teacher') & (table_1['suffix'] == 'details'), ['teacher_id','detail_value','prefix','suffix']].drop_duplicates(subset=['teacher_id'], keep='first').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_transcripts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_enrollments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_teachers = prepared_table_3

# Assume prepared_transcripts, prepared_enrollments, prepared_teachers are dataframes
# 1) Find student(s) with earliest transcript issuance
earliest_date = prepared_transcripts['date_of_transcript']
if not pd.api.types.is_datetime64_any_dtype(earliest_date):
    prepared_transcripts = prepared_transcripts.assign(date_of_transcript=pd.to_datetime(prepared_transcripts['date_of_transcript'], errors='coerce'))
earliest_dt = prepared_transcripts['date_of_transcript'].min()
earliest_students = prepared_transcripts.loc[prepared_transcripts['date_of_transcript'] == earliest_dt, ['student_id']].drop_duplicates()

# 2) Join to enrollments to get teacher ids for those students
stu_enroll = earliest_students.merge(prepared_enrollments, on='student_id', how='inner')

# 3) Join to teachers on teacher_id (tid)
stu_teachers = stu_enroll.merge(prepared_teachers, left_on='tid', right_on='teacher_id', how='inner')

# 4) Deduplicate teachers and select teacher details
target = stu_teachers[['teacher_id', 'detail_value', 'prefix', 'suffix']].drop_duplicates().reset_index(drop=True)

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
