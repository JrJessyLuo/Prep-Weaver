import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['FIRST_NAME','MIDDLE_NAME','LAST_NAME','FULL_NAME','DEPARTMENT','DEPARTMENT_NAME','EMAIL_ADDRESS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['MOIRA_LIST_KEY','moira_list_member','MOIRA_LIST_MEMBER_FULL_NAME','MOIRA_LIST_MEMBER_MIT_ID']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_NAME']].copy()
    df['MOIRA_LIST_KEY'] = df['MOIRA_LIST_KEY'].astype(str).str.strip()
    target = df[['MOIRA_LIST_KEY','MOIRA_LIST_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['DEPARTMENT_CODE','DEPARTMENT_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_students = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_mailing_list_members = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_mailing_lists = prepared_table_3
prepared_table_4 = _prep_4(tables['table_5'])
prepared_departments = prepared_table_4

# Assume prepared tables are provided as DataFrames: prepared_students, prepared_mailing_list_members, prepared_mailing_lists, prepared_departments

# Normalize keys and names for robust matching
ml = prepared_mailing_lists.copy()
ml['MOIRA_LIST_KEY_norm'] = ml['MOIRA_LIST_KEY'].astype(str).str.strip().str.lower()
ml['MOIRA_LIST_NAME_norm'] = ml['MOIRA_LIST_NAME'].astype(str).str.strip().str.lower()

mlm = prepared_mailing_list_members.copy()
mlm['MOIRA_LIST_KEY_norm'] = mlm['MOIRA_LIST_KEY'].astype(str).str.strip().str.lower()
mlm['MOIRA_LIST_MEMBER_FULL_NAME_norm'] = mlm['MOIRA_LIST_MEMBER_FULL_NAME'].astype(str).str.strip().str.upper()

stud = prepared_students.copy()
stud['FULL_NAME_UPPER_norm'] = stud['FULL_NAME'].astype(str).str.strip().str.upper()
stud['LAST_INITIAL'] = stud['LAST_NAME'].astype(str).str.strip().str[:1].str.upper()

# Filter to the target mailing list by name
target_list_name = 'beacon-date-date'
ml_target = ml[ml['MOIRA_LIST_NAME_norm'] == target_list_name]

# Join members with the target list via key
members_of_target = mlm.merge(ml_target[['MOIRA_LIST_KEY_norm','MOIRA_LIST_NAME_norm']], on='MOIRA_LIST_KEY_norm', how='inner')

# Compute list size (number of member rows) for the target list
list_size = len(members_of_target)

# Join students to members by normalized full name; also restrict to last names starting with 'H'
students_H = stud[stud['LAST_INITIAL'] == 'H']
joined = students_H.merge(
    members_of_target,
    left_on='FULL_NAME_UPPER_norm',
    right_on='MOIRA_LIST_MEMBER_FULL_NAME_norm',
    how='inner'
)

# Prepare department phone: table_1 contains OFFICE_PHONE but request asks for phone numbers of departments they belong to; no department phone exists in provided tables.
# Use OFFICE_PHONE as the available phone field associated with the student's department context.

# Build final output columns and attach list size
result = joined[['FIRST_NAME','MIDDLE_NAME','LAST_NAME','FULL_NAME','DEPARTMENT','DEPARTMENT_NAME']].copy()
# Use OFFICE_PHONE if present in original students table; if not available in prepared_students, attempt to fetch from original if accessible. Here we assume not included; thus no phone unless OFFICE_PHONE was preserved. If OFFICE_PHONE exists in prepared_students, include it.
if 'OFFICE_PHONE' in students_H.columns:
    result = joined[['FIRST_NAME','MIDDLE_NAME','LAST_NAME','FULL_NAME','DEPARTMENT','DEPARTMENT_NAME','OFFICE_PHONE']].copy()
    result = result.rename(columns={'OFFICE_PHONE':'DEPARTMENT_PHONE'})
else:
    result['DEPARTMENT_PHONE'] = pd.NA

result['MAILING_LIST_NAME'] = target_list_name
result['MAILING_LIST_SIZE'] = list_size

# Deduplicate in case of multiple matches per person
result = result.drop_duplicates(subset=['FULL_NAME'])

target = result

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
