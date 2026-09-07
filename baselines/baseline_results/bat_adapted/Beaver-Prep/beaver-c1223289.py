import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['MOIRA_LIST_KEY','moira_list_member','MOIRA_LIST_MEMBER_FULL_NAME']].copy()
    df['moira_list_member'] = df['moira_list_member'].astype(str).str.strip()
    target = df[['MOIRA_LIST_KEY','moira_list_member','MOIRA_LIST_MEMBER_FULL_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['INSTRUCTOR_NAME','LIBRARY_COURSE_INSTRUCTOR_KEY','COURSE_NAME','DATE_FROM','DATE_TO']].copy()
    prepared['DATE_FROM'] = pd.to_datetime(prepared['DATE_FROM'], format='%d-%b-%y', errors='coerce')
    prepared['DATE_TO'] = pd.to_datetime(prepared['DATE_TO'], format='%d-%b-%y', errors='coerce')
    target = prepared[['INSTRUCTOR_NAME','LIBRARY_COURSE_INSTRUCTOR_KEY','COURSE_NAME','DATE_FROM','DATE_TO']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1.copy()
    df['LIBRARY_SUBJECT_OFFERED_KEY'] = df['LIBRARY_SUBJECT_OFFERED_KEY'].astype(str).str.strip()
    df['SUBJECT_ID'] = df['SUBJECT_ID'].astype(str).str.strip()
    df['term_code'] = df['term_code'].astype(str).str.strip()
    df['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(df['NUM_ENROLLED_STUDENTS'], errors='coerce')
    target = df[['LIBRARY_SUBJECT_OFFERED_KEY','term_code','SUBJECT_ID','NUM_ENROLLED_STUDENTS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_6'])
prepared_moira_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_course_instructors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_course_offerings_link = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_subject_offerings = prepared_table_4

# Assume prepared_* DataFrames exist per targets

# 1) Filter to the specified mailing list
ml = prepared_moira_members.copy()
ml['MOIRA_LIST_KEY_norm'] = ml['MOIRA_LIST_KEY'].str.strip().str.lower()
ml_f = ml[ml['MOIRA_LIST_KEY_norm'] == 'keeper-zephyr']

# 2) Normalize names for joining
left = ml_f.rename(columns={'MOIRA_LIST_MEMBER_FULL_NAME':'INSTRUCTOR_NAME'})
left['INSTRUCTOR_NAME'] = left['INSTRUCTOR_NAME'].astype(str).str.strip()
ci = prepared_course_instructors.copy()
ci['INSTRUCTOR_NAME'] = ci['INSTRUCTOR_NAME'].astype(str).str.strip()

# 3) Join mailing list members to instructor assignments by name
m1 = pd.merge(left, ci, on='INSTRUCTOR_NAME', how='inner')

# 4) Link to offerings via course-instructor key
b = prepared_course_offerings_link.copy()
m2 = pd.merge(m1, b, on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')

# 5) Join to subject offerings for enrollment
so = prepared_subject_offerings.copy()
m3 = pd.merge(m2, so, on='LIBRARY_SUBJECT_OFFERED_KEY', how='left')

# 6) Derive publication year from DATE_FROM/DATE_TO (take years)
def parse_year(s):
    # Expect formats like '04-JAN-10' -> 2010; handle 2- or 4-digit years
    if pd.isna(s):
        return pd.NA
    s = str(s)
    # simple extract last 2 or 4 digit year
    m4 = re.search(r'(19|20)\d{2}', s)
    if m4:
        return int(m4.group(0))
    m2d = re.search(r'(\d{2})(?!\d)', s)
    if m2d:
        y = int(m2d.group(1))
        return 2000 + y if y <= 49 else 1900 + y
    return pd.NA

m3['YEAR_FROM'] = m3['DATE_FROM'].apply(parse_year)
m3['YEAR_TO'] = m3['DATE_TO'].apply(parse_year)

# 7) Aggregate per instructor (list), instructor name, earliest/latest publication years, total enrolled students
# Treat NUM_ENROLLED_STUDENTS as numeric and sum over offerings linked to that instructor
m3['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(m3.get('NUM_ENROLLED_STUDENTS'), errors='coerce')

agg = (m3.groupby(['MOIRA_LIST_KEY', 'INSTRUCTOR_NAME'], dropna=False)
         .agg(earliest_publication_year=('YEAR_FROM', 'min'),
              latest_publication_year=('YEAR_TO', 'max'),
              total_enrolled_students=('NUM_ENROLLED_STUDENTS', 'sum'))
         .reset_index())

# 8) Prepare final columns as requested
result = agg.rename(columns={'MOIRA_LIST_KEY':'mailing_list',
                             'INSTRUCTOR_NAME':'instructor_name'})
# If multiple lists somehow present after filtering, keep as-is

output = result[['mailing_list','instructor_name','earliest_publication_year','latest_publication_year','total_enrolled_students']]

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
