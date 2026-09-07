import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['EMAIL_ADDRESS','DEPARTMENT_NAME']].copy()
    prepared['EMAIL_ADDRESS'] = prepared['EMAIL_ADDRESS'].astype(str).str.strip()
    prepared['DEPARTMENT_NAME'] = prepared['DEPARTMENT_NAME'].astype(object)
    prepared = prepared[prepared['EMAIL_ADDRESS'].notna() & (prepared['EMAIL_ADDRESS'] != '')]
    target = prepared.groupby('EMAIL_ADDRESS', as_index=False)['DEPARTMENT_NAME'].first()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['DEPARTMENT_NAME','DEPARTMENT_FULL_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_departments = prepared_table_2

# Inputs: prepared_people, prepared_departments, and an emails table representing lists (not among selected tables).
# Since only people and departments are provided, assume another process selects people by list name 'date-destiny'.
# Here, demonstrate logic assuming a DataFrame `emails_in_list` with EMAIL_ADDRESS for the list.

# 1) Filter people to those in the email list 'date-destiny'
# emails_in_list should have a column EMAIL_ADDRESS for members of the list
people_in_list = prepared_people.merge(emails_in_list[["EMAIL_ADDRESS"]].drop_duplicates(), on="EMAIL_ADDRESS", how="inner")

# 2) Optionally integrate department reference (kept simple here)
people_in_list = people_in_list.merge(prepared_departments, on="DEPARTMENT_NAME", how="left")

# 3) Compute counts
total_students = len(people_in_list)
mgmt_count = (people_in_list["DEPARTMENT_NAME"].str.strip().str.lower() == "management").sum()
percentage = round((mgmt_count / total_students) * 100, 2) if total_students > 0 else 0.0

# 4) Produce final answer row
answer = pd.DataFrame([
    {
        "list_name": "date-destiny",
        "department_name": "Management",
        "management_student_count": int(mgmt_count),
        "management_percentage": percentage
    }
])

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
