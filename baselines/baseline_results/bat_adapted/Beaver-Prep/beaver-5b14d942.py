import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['term_code','TERM_DESCRIPTION','IS_CURRENT_TERM']].copy()
    df['IS_CURRENT_TERM'] = df['IS_CURRENT_TERM'].astype(str).str.strip().str.upper().replace({'TRUE':'Y','T':'Y','YES':'Y','1':'Y','FALSE':'N','F':'N','NO':'N','0':'N'})
    df = df.drop_duplicates(subset=['term_code','TERM_DESCRIPTION','IS_CURRENT_TERM'])
    target = df[['term_code','TERM_DESCRIPTION','IS_CURRENT_TERM']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    cols = ['TERM_CODE','SUBJECT_ID','COURSE_NUMBER','SUBJECT_TITLE','HGN_CODE','HGN_CODE_DESC','OFFER_DEPT_CODE','OFFER_DEPT_NAME','RESPONSIBLE_FACULTY_NAME','RESPONSIBLE_FACULTY_MIT_ID','TOTAL_UNITS']
    df = table_1[cols].copy()
    df['RESPONSIBLE_FACULTY_NAME'] = df['RESPONSIBLE_FACULTY_NAME'].replace('nan', pd.NA)
    df = df.groupby(['TERM_CODE','SUBJECT_ID','COURSE_NUMBER'], as_index=False).agg({'SUBJECT_TITLE':'first','HGN_CODE':'first','HGN_CODE_DESC':'first','OFFER_DEPT_CODE':'first','OFFER_DEPT_NAME':'first','RESPONSIBLE_FACULTY_NAME':'first','RESPONSIBLE_FACULTY_MIT_ID':'first','TOTAL_UNITS':'first'})
    target = df[['TERM_CODE','SUBJECT_ID','COURSE_NUMBER','SUBJECT_TITLE','HGN_CODE','HGN_CODE_DESC','OFFER_DEPT_CODE','OFFER_DEPT_NAME','RESPONSIBLE_FACULTY_NAME','RESPONSIBLE_FACULTY_MIT_ID','TOTAL_UNITS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.assign(MIT_ID=table_1['MIT_ID'].astype('string').str.strip(),FULL_NAME=table_1['FULL_NAME'].astype('string').str.strip(),EMAIL_ADDRESS=table_1['EMAIL_ADDRESS'].astype('string').str.strip())
    target = target.loc[target['MIT_ID'].notna() & (target['MIT_ID'] != ''), ['MIT_ID','FULL_NAME','EMAIL_ADDRESS']]
    target = target.drop_duplicates(subset=['MIT_ID'], keep='first').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_8'])
prepared_current_term = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_subject_offerings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_people_directory = prepared_table_3

# Assume prepared_current_term, prepared_subject_offerings, prepared_people_directory are DataFrames
cur_term = prepared_current_term[prepared_current_term['IS_CURRENT_TERM'].str.upper().eq('Y')]
# Join subjects to current term
cur_subjects = prepared_subject_offerings.merge(cur_term[['term_code','TERM_DESCRIPTION']], left_on='TERM_CODE', right_on='term_code', how='inner')
# Enrich with person directory (name/email may be missing if MIT_ID null or no match)
cur_subjects = cur_subjects.merge(prepared_people_directory[['MIT_ID','FULL_NAME','EMAIL_ADDRESS']], left_on='RESPONSIBLE_FACULTY_MIT_ID', right_on='MIT_ID', how='left')
# Compute per-course-type counts and average units as requested at the course/department/HGN granularity
# Coerce TOTAL_UNITS to numeric for averaging
cur_subjects['TOTAL_UNITS_NUM'] = pd.to_numeric(cur_subjects['TOTAL_UNITS'], errors='coerce')
# Prepare final details
result = cur_subjects.assign(
    academic_year=cur_subjects['TERM_DESCRIPTION'].str.extract(r'(\d{4}-\d{4})', expand=False),
    term_code=cur_subjects['TERM_CODE'],
    hgn_code=cur_subjects['HGN_CODE'],
    department_name=cur_subjects['OFFER_DEPT_NAME'],
    person_in_charge_name=cur_subjects['FULL_NAME'].fillna(cur_subjects['RESPONSIBLE_FACULTY_NAME']),
    person_in_charge_email=cur_subjects['EMAIL_ADDRESS']
)
# Aggregate total number of types of courses (distinct SUBJECT_ID) and average units by dept and HGN (and optionally course number)
aggr = result.groupby(['academic_year','term_code','hgn_code','department_name','person_in_charge_name','person_in_charge_email'], dropna=False).agg(
    total_number_of_types_of_courses=pd.NamedAgg(column='SUBJECT_ID', aggfunc=lambda s: s.nunique()),
    average_number_of_units=pd.NamedAgg(column='TOTAL_UNITS_NUM', aggfunc='mean')
).reset_index()
# Rename columns to match question phrasing
aggr = aggr[['academic_year','term_code','hgn_code','total_number_of_types_of_courses','average_number_of_units','department_name','person_in_charge_name','person_in_charge_email']]
# target output
target = aggr

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
