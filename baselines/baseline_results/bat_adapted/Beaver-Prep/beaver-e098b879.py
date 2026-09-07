import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['MIT_ID','FULL_NAME','EMAIL_ADDRESS','IS_FACULTY','IS_SUMMER_SESSION_APPT']].drop_duplicates(subset=['MIT_ID']).reset_index(drop=True)
    target = target.reindex(columns=['MIT_ID','FULL_NAME','EMAIL_ADDRESS','IS_FACULTY','IS_SUMMER_SESSION_APPT'])
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    academic_terms = table_1[['term_code','TERM_DESCRIPTION','FINANCIAL_AID_YEAR']].copy()
    academic_terms['FINANCIAL_AID_YEAR'] = pd.to_numeric(academic_terms['FINANCIAL_AID_YEAR'], errors='coerce')
    academic_terms = academic_terms.drop_duplicates(subset=['term_code'], keep='first')
    target = academic_terms[['term_code','TERM_DESCRIPTION','FINANCIAL_AID_YEAR']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['ACADEMIC_TERM_CODE','ACADEMIC_TERM_DESCRIPTION','FINANCIAL_AID_YEAR']].copy()
    df = df[df['ACADEMIC_TERM_CODE'].notna()]
    df = df.drop_duplicates(subset=['ACADEMIC_TERM_CODE','ACADEMIC_TERM_DESCRIPTION','FINANCIAL_AID_YEAR'], keep='first')
    target = df[['ACADEMIC_TERM_CODE','ACADEMIC_TERM_DESCRIPTION','FINANCIAL_AID_YEAR']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
people_directory = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
academic_terms = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
calendar_terms = prepared_table_3

# Inputs: prepared tables
people = people_directory.copy()
terms = academic_terms.copy()
cal_terms = calendar_terms.copy()

# 1) Identify summer terms in FA years > 2001 using either terms table (primary) or calendar_terms (backup)
terms_summer = terms[terms['TERM_DESCRIPTION'].str.contains('Summer', case=False, na=False)].copy()
terms_summer = terms_summer[pd.to_numeric(terms_summer['FINANCIAL_AID_YEAR'], errors='coerce') > 2001]

cal_terms_summer = cal_terms[cal_terms['ACADEMIC_TERM_DESCRIPTION'].str.contains('Summer', case=False, na=False)].copy()
cal_terms_summer = cal_terms_summer[pd.to_numeric(cal_terms_summer['FINANCIAL_AID_YEAR'], errors='coerce') > 2001]

# Merge to unify term codes considered summer after 2001
summer_codes = pd.Series(dtype=object)
if not terms_summer.empty:
    summer_codes = pd.concat([summer_codes, terms_summer['term_code']])
if not cal_terms_summer.empty:
    summer_codes = pd.concat([summer_codes, cal_terms_summer['ACADEMIC_TERM_CODE']])
summer_codes = summer_codes.dropna().drop_duplicates()

# 2) Identify faculty who teach in summer: we only have a summer-session appointment flag in people
faculty_summer = people.copy()
faculty_summer['is_fac'] = people['IS_FACULTY'].astype(str).str.upper().isin(['Y', 'YES', 'TRUE', '1'])
faculty_summer['is_summer'] = people['IS_SUMMER_SESSION_APPT'].astype(str).str.upper().isin(['Y', 'YES', 'TRUE', '1'])
faculty_summer = faculty_summer[faculty_summer['is_fac'] & faculty_summer['is_summer']]

# 3) Email lists starting with C: Not present in selected tables. We cannot compute list membership counts without a mailing list table and a membership bridge.
# Return an empty result with the expected columns to indicate no data available from provided tables.

result = pd.DataFrame(columns=['list_name', 'num_people_in_list', 'num_faculty_in_list'])

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
