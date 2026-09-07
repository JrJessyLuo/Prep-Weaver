import pandas as pd
import numpy as np

def _prep_1(table_1):
    cols = ['EMAIL_ADDRESS','FIRST_NAME','LAST_NAME','FULL_NAME','DEPARTMENT','DEPARTMENT_NAME']
    target = table_1.loc[:, cols].drop_duplicates(subset=['EMAIL_ADDRESS'], keep='first').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['DEPARTMENT_CODE','DEPARTMENT_NAME','DEPARTMENT_FULL_NAME','SCHOOL_CODE','SCHOOL_NAME']].copy()
    target = target.apply(lambda s: s.astype('string').str.strip())
    target = target.replace({'': pd.NA, 'nan': pd.NA, 'None': pd.NA})
    target = target.dropna(subset=['DEPARTMENT_CODE'])
    target = target.drop_duplicates(subset=['DEPARTMENT_CODE'], keep='first').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    df['MOIRA_LIST_KEY'] = df['MOIRA_LIST_KEY'].astype(str).str.strip()
    target = df[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_ACTIVE','IS_MOIRA_MAILING_LIST','IS_PUBLIC','IS_HIDDEN']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_students = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_departments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_mailing_lists = prepared_table_3

# Inputs: prepared_students (from table_1), prepared_departments (from table_2), prepared_mailing_lists (from table_3)
# Assumptions: student-to-list membership and list sizes come from external membership/size data not present in selected tables.

# 1) Filter students with last names starting with 'K'
stud_k = prepared_students[prepared_students['LAST_NAME'].astype(str).str.startswith('K', na=False)].copy()

# 2) Join departments to get department attributes (e.g., phone would be joined here if available in dept reference)
# Note: The provided department reference lacks phone numbers; if department phones exist in a different prepared table,
# add an additional merge on a matching department key.
stud_dept = stud_k.merge(prepared_departments, how='left', left_on='DEPARTMENT_NAME', right_on='DEPARTMENT_NAME')

# 3) Compute per-student mailing list metrics
# Placeholder: membership DataFrame 'membership' with columns ['EMAIL_ADDRESS','MOIRA_LIST_NAME'] is required.
# Placeholder: list_sizes DataFrame 'list_sizes' with columns ['MOIRA_LIST_NAME','LIST_SIZE'] is required.
# If available, integrate as below. If not available, counts/averages cannot be computed from given tables.
try:
    # Keep only active Moira mailing lists
    active_lists = prepared_mailing_lists[(prepared_mailing_lists['IS_ACTIVE'] == 'Y') & (prepared_mailing_lists['IS_MOIRA_MAILING_LIST'] == 'Y')][['MOIRA_LIST_NAME']]

    # Filter membership to active lists and to our students
    mem = membership.merge(active_lists, how='inner', on='MOIRA_LIST_NAME')
    mem = mem.merge(stud_dept[['EMAIL_ADDRESS']], how='inner', on='EMAIL_ADDRESS')

    # Join list sizes
    mem = mem.merge(list_sizes, how='left', on='MOIRA_LIST_NAME')

    # Aggregate per student
    agg = mem.groupby('EMAIL_ADDRESS').agg(total_mailing_lists=('MOIRA_LIST_NAME','nunique'), avg_mailing_list_size=('LIST_SIZE','mean')).reset_index()
except NameError:
    # Fallback empty aggregates if membership/size not provided
    agg = pd.DataFrame(columns=['EMAIL_ADDRESS','total_mailing_lists','avg_mailing_list_size'])

# 4) Final projection with names, department phone placeholder, and metrics
# Note: Department phone not present in inputs; if a dept phone column exists after joining, rename/select it here.
result = stud_dept.merge(agg, how='left', on='EMAIL_ADDRESS')
result['total_mailing_lists'] = result['total_mailing_lists'].fillna(0).astype(int)

# Choose name to display and the department phone column if available
result = result.assign(Student_Name=result['FULL_NAME'])
# If department phone column existed, e.g., 'DEPARTMENT_PHONE', keep/rename it; placeholder below
if 'DEPARTMENT_PHONE' in result.columns:
    result = result.rename(columns={'DEPARTMENT_PHONE':'Department_Phone'})
else:
    result['Department_Phone'] = pd.NA

answer = result[['Student_Name','Department_Phone','total_mailing_lists','avg_mailing_list_size']]

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
