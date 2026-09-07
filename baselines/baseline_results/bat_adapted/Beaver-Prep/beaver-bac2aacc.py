import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','RESPONSIBLE_FACULTY_NAME','responsible_faculty_mit_id','MEET_PLACE']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','RESPONSIBLE_FACULTY_NAME','responsible_faculty_mit_id','MEET_PLACE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','SUBJECT_DESCRIPTION','DEPARTMENT_CODE','DEPARTMENT_NAME']].copy()
    prepared = prepared.drop_duplicates(subset=['TERM_CODE','SUBJECT_ID'])
    target = prepared[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','SUBJECT_DESCRIPTION','DEPARTMENT_CODE','DEPARTMENT_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_subjects = prepared_table_2

# Merge offerings with subject metadata on SUBJECT_ID and TERM_CODE
merged = prepared_offerings.merge(prepared_subjects, on=["SUBJECT_ID", "TERM_CODE"], how="inner")

# Derive building, room, and floor from MEET_PLACE if possible (schema not provided; basic parsing example)
# Expected MEET_PLACE format examples could be like "Bldg 32-141 (1st Fl)"; adjust parsing rules as needed.
meet = merged["MEET_PLACE"].fillna("")
# Simple heuristics:
merged["BUILDING_NAME"] = meet.str.extract(r"^(.*?)(?=\s*\d|$)").fillna("").str.strip()
merged["ROOM_NAME"] = meet.str.extract(r"(\d[\w-]*)").fillna("")
merged["FLOOR_LEVEL"] = meet.str.extract(r"(\b\d+(?:st|nd|rd|th)\s*Fl\b|Floor\s*\d+)").fillna("")
merged["BUILDING_STREET_ADDRESS"] = ""  # Not present in selected tables; left blank.

# Compute total number of types of courses per department.
# Interpret "types of courses" as distinct SUBJECT_CODE (prefix before dot) or FORM_TYPE if available.
# Given available columns, use subject code prefix from SUBJECT_ID (e.g., '6' from '6.003').
merged["COURSE_TYPE"] = merged["SUBJECT_ID"].str.split(".").str[0]
course_type_counts = merged.groupby("DEPARTMENT_CODE")["COURSE_TYPE"].nunique().reset_index(name="TOTAL_COURSE_TYPES_PER_DEPT")

# Attach counts back to merged data (align by department code from prepared_subjects)
merged = merged.merge(course_type_counts, on="DEPARTMENT_CODE", how="left")

# Filter to summer term codes (assuming codes containing 'SU' denote summer, e.g., '2016SU')
summer = merged[merged["TERM_CODE"].str.contains("SU", na=False)]

# Select and rename final answer columns
answer = summer[[
    "SUBJECT_TITLE_x",            # from offerings (title as scheduled)
    "SUBJECT_DESCRIPTION",        # from subjects
    "RESPONSIBLE_FACULTY_NAME",
    "responsible_faculty_mit_id", # as proxy for email not present; email unavailable in selected tables
    "BUILDING_NAME",
    "ROOM_NAME",
    "FLOOR_LEVEL",
    "BUILDING_STREET_ADDRESS",
    "TOTAL_COURSE_TYPES_PER_DEPT"
]].rename(columns={
    "SUBJECT_TITLE_x": "subject_title",
    "SUBJECT_DESCRIPTION": "subject_description",
    "RESPONSIBLE_FACULTY_NAME": "responsible_faculty_name",
    "responsible_faculty_mit_id": "faculty_email_or_id",  # email not available; keep ID present
    "BUILDING_NAME": "building_name",
    "ROOM_NAME": "room_name",
    "FLOOR_LEVEL": "floor_level",
    "BUILDING_STREET_ADDRESS": "building_street_address",
    "TOTAL_COURSE_TYPES_PER_DEPT": "total_course_types_per_department"
})

# Drop duplicates to list each subject once per offering context
answer = answer.drop_duplicates()

target = answer

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
