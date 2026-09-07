import pandas as pd
import numpy as np

def _prep_1(table_1):
    import pandas as pd
    target = table_1.loc[:, ['MIT_ID','FULL_NAME','FIRST_NAME','LAST_NAME','EMAIL_ADDRESS','IS_FACULTY']].copy()
    target = target.replace({'': pd.NA, 'NULL': pd.NA, 'null': pd.NA, 'None': pd.NA})
    target = target.dropna(subset=['MIT_ID'])
    target = target.drop_duplicates(subset=['MIT_ID'], keep='first').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    source = table_1.copy()
    source['moira_list_member'] = source['moira_list_member'].astype(str).str.strip()
    target = source[['MOIRA_LIST_KEY','moira_list_member','MOIRA_LIST_MEMBER_FULL_NAME','MOIRA_LIST_MEMBER_MIT_ID']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['RESPONSIBLE_FACULTY_MIT_ID','SUBJECT_ID','SUBJECT_TITLE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_moira_members = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_subjects = prepared_table_3

# Assume prepared_people, prepared_moira_members, prepared_subjects are the synthesized per-table targets

# Normalize ID types
prepared_people = prepared_people.copy()
prepared_people['MIT_ID'] = pd.to_numeric(prepared_people['MIT_ID'], errors='coerce')

prepared_moira_members = prepared_moira_members.copy()
prepared_moira_members['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(prepared_moira_members['MOIRA_LIST_MEMBER_MIT_ID'], errors='coerce')

prepared_subjects = prepared_subjects.copy()
prepared_subjects['RESPONSIBLE_FACULTY_MIT_ID'] = pd.to_numeric(prepared_subjects['RESPONSIBLE_FACULTY_MIT_ID'], errors='coerce')

# Join list memberships to people
m = prepared_moira_members.merge(
    prepared_people,
    left_on='MOIRA_LIST_MEMBER_MIT_ID',
    right_on='MIT_ID',
    how='inner'
)

# Filter to faculty and last names starting with 'Y'
m = m[(m['IS_FACULTY'].astype(str).str.upper().isin(['Y', 'YES', 'TRUE', '1'])) &
      (m['LAST_NAME'].astype(str).str.upper().str.startswith('Y'))]

# Join to subjects managed by those faculty
ms = m.merge(
    prepared_subjects,
    left_on='MIT_ID',
    right_on='RESPONSIBLE_FACULTY_MIT_ID',
    how='left'
)

# Aggregate: for each list, count unique faculty and total subjects managed by those faculty
# Total subjects: count distinct SUBJECT_ID across all matched faculty within the list
agg = ms.groupby('MOIRA_LIST_KEY').agg(
    num_faculty_in_list=('MIT_ID', 'nunique'),
    total_subjects_managed=('SUBJECT_ID', pd.Series.nunique)
).reset_index()

# If a list has faculty but none manage subjects in data, ensure total_subjects_managed is 0
agg['total_subjects_managed'] = agg['total_subjects_managed'].fillna(0).astype(int)

# Prepare final output columns
result = agg.rename(columns={'MOIRA_LIST_KEY': 'list_name'})

# Sort for presentation (optional)
result = result.sort_values(['num_faculty_in_list', 'total_subjects_managed', 'list_name'], ascending=[False, False, True])

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
