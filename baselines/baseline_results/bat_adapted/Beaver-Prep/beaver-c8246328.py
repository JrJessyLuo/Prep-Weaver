import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME','SUBJECT_ID','JOINT_SUBJECTS']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME','SUBJECT_ID','JOINT_SUBJECTS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME']].copy()
    df['SCHOOL_NAME'] = df['SCHOOL_NAME'].replace('', pd.NA)
    target = df.groupby(['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME'], as_index=False)['SCHOOL_NAME'].first()[['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_table_3 = _prep_3(tables['table_1'])
prepared_dept_school = prepared_table_3
prepared_table_4 = _prep_4(tables['table_6'])

def count_equivalents(joints):
    if pd.isna(joints) or str(joints).strip()=='' or str(joints).strip().lower()=='nan':
        return 0
    # assume JOINT_SUBJECTS is a delimiter-separated list (e.g., comma); count non-empty tokens
    parts = [p.strip() for p in str(joints).replace(';', ',').split(',')]
    parts = [p for p in parts if p]
    return len(parts)

# 1) Aggregate per term x department
subjects = prepared_subjects.copy()
subjects['equiv_cnt'] = subjects['JOINT_SUBJECTS'].apply(count_equivalents)
per_td = (
    subjects.groupby(['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME'], as_index=False)
            .agg(num_courses=('SUBJECT_ID','nunique'), avg_equiv=('equiv_cnt','mean'))
)

# 2) Attach SCHOOL_NAME
per_td = per_td.merge(prepared_dept_school[['TERM_CODE','DEPARTMENT_CODE','SCHOOL_NAME']].drop_duplicates(),
                      on=['TERM_CODE','DEPARTMENT_CODE'], how='left')

# 3) Build subtotals per term
term_sub = (
    per_td.groupby(['TERM_CODE'], as_index=False)
          .agg(num_courses=('num_courses','sum'), avg_equiv=('avg_equiv','mean'))
)
term_sub['DEPARTMENT_CODE'] = ''
term_sub['DEPARTMENT_NAME'] = 'SUBTOTAL'
# For subtotals, if multiple schools exist per term, leave SCHOOL_NAME blank
term_schools = per_td.groupby('TERM_CODE')['SCHOOL_NAME'].nunique().reset_index(name='n')
term_single = term_sub.merge(term_schools, on='TERM_CODE', how='left')
term_single['SCHOOL_NAME'] = ''
term_sub = term_single[['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME','num_courses','avg_equiv','SCHOOL_NAME']]

# 4) Grand total across all terms
grand = pd.DataFrame([{
    'TERM_CODE': 'TOTAL',
    'DEPARTMENT_CODE': '',
    'DEPARTMENT_NAME': 'TOTAL',
    'num_courses': per_td['num_courses'].sum(),
    'avg_equiv': per_td['avg_equiv'].mean(),
    'SCHOOL_NAME': ''
}])

# 5) Union detail + subtotals + grand total
result = pd.concat([per_td, term_sub, grand], ignore_index=True, sort=False)

# 6) Sort by term then department; suppress repeating term labels
result = result.sort_values(by=['TERM_CODE','DEPARTMENT_NAME'], kind='mergesort').reset_index(drop=True)
# Create display column for term that blanks repeated values except for SUBTOTAL rows which already carry term
result['TERM_DISPLAY'] = result['TERM_CODE']
mask = (result['DEPARTMENT_NAME']!='SUBTOTAL') & (result['TERM_CODE']!='TOTAL')
result.loc[mask, 'TERM_DISPLAY'] = result.loc[mask, 'TERM_CODE'].where(result['TERM_CODE'].ne(result['TERM_CODE'].shift()), '')

# Final selected columns for output
final = result[['TERM_DISPLAY','DEPARTMENT_NAME','num_courses','avg_equiv','SCHOOL_NAME']]
final = final.rename(columns={'TERM_DISPLAY':'TERM','DEPARTMENT_NAME':'DEPARTMENT','num_courses':'NUMBER_OF_COURSES','avg_equiv':'AVERAGE_EQUIVALENT_SUBJECTS','SCHOOL_NAME':'SCHOOL_NAME'})

target = final

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
