import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME','DLC_KEY']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME','DLC_KEY']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','SUBJECT_CODE','COURSE_NUMBER']].copy()
    target['COURSE_NUMBER'] = target['COURSE_NUMBER'].astype(str).str.strip()
    target = target.drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['COURSE_NUMBER','HGN_CODE']].copy()
    df = df.dropna(subset=['COURSE_NUMBER','HGN_CODE'])
    df['HGN_CODE'] = df['HGN_CODE'].astype(str).str.strip()
    df = df[df['HGN_CODE'].ne('') & df['COURSE_NUMBER'].astype(str).str.strip().ne('')]
    agg = df.groupby('COURSE_NUMBER', as_index=False).agg(HGN_CODE=('HGN_CODE', lambda s: 'G' if (s == 'G').any() else s.iloc[0]))
    target = agg[['COURSE_NUMBER','HGN_CODE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_departments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_subject_codes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_subject_offerings = prepared_table_3

# Assume prepared tables are provided as dataframes: prepared_departments, prepared_subject_codes, prepared_subject_offerings

# 1) Derive graduate level per course number using offerings (G present => Graduate, else if N only => Not for grad credit, else other codes retained). 
# Normalize COURSE_NUMBER whitespace/case across tables
psc = prepared_subject_codes.copy()
pso = prepared_subject_offerings.copy()
pdpt = prepared_departments.copy()

for df in (psc, pso):
    if 'COURSE_NUMBER' in df.columns:
        df['COURSE_NUMBER'] = df['COURSE_NUMBER'].astype(str).str.strip().str.upper()

# Deduplicate offerings by COURSE_NUMBER and compute graduate flag
pso_g = (
    pso.assign(
        COURSE_NUMBER=lambda d: d['COURSE_NUMBER'].astype(str).str.strip().str.upper(),
        HGN_CODE=lambda d: d['HGN_CODE'].astype(str).str.upper()
    )
)
# For each COURSE_NUMBER, determine grad_level: 'Graduate' if any HGN_CODE == 'G', else 'Not for graduate credit' if all 'N', else 'Mixed/Other'
agg = (
    pso_g.groupby('COURSE_NUMBER')['HGN_CODE']
         .agg(lambda s: ('Graduate' if (s == 'G').any() else ('Not for graduate credit' if (s.replace({'N': 'N'}).isin(['N'])).all() else 'Mixed/Other')))
         .reset_index()
         .rename(columns={'HGN_CODE': 'GRADUATE_LEVEL'})
)

# 2) Attach graduate level to subject codes via COURSE_NUMBER (left join, some course numbers may lack offerings)
psc_gl = psc.merge(agg, on='COURSE_NUMBER', how='left')

# 3) Compute school-level aggregates from subject codes
# Total number of SIS subjects per school: count distinct SUBJECT_CODE per SCHOOL_CODE
subjects_per_school = (
    psc[['SCHOOL_CODE','SUBJECT_CODE']]
      .dropna()
      .drop_duplicates()
      .groupby('SCHOOL_CODE')
      .size()
      .rename('TOTAL_SIS_SUBJECTS')
      .reset_index()
)

# 4) Min/Max course numbers per school (based on normalized COURSE_NUMBER strings)
course_minmax = (
    psc[['SCHOOL_CODE','COURSE_NUMBER']]
      .dropna()
      .assign(COURSE_NUMBER=lambda d: d['COURSE_NUMBER'].astype(str).str.strip().str.upper())
      .drop_duplicates()
      .groupby('SCHOOL_CODE')
      .agg(MIN_COURSE_NUMBER=('COURSE_NUMBER','min'), MAX_COURSE_NUMBER=('COURSE_NUMBER','max'))
      .reset_index()
)

# 5) Total number of departments offering subjects per school
depts_per_school = (
    pdpt[['SCHOOL_CODE','DEPARTMENT_CODE']]
        .dropna()
        .drop_duplicates()
        .merge(psc[['DEPARTMENT_CODE']].drop_duplicates(), on='DEPARTMENT_CODE', how='inner')
        .groupby('SCHOOL_CODE')
        .size()
        .rename('TOTAL_DEPARTMENTS_OFFERING_SUBJECTS')
        .reset_index()
)

# 6) Determine school-level graduate level from course numbers present in that school (priority: Graduate if any Graduate; else Not for graduate credit if all are that; else Mixed/Other)
school_grad = (
    psc_gl[['SCHOOL_CODE','GRADUATE_LEVEL']]
      .dropna(subset=['SCHOOL_CODE'])
)
# If a school has no GRADUATE_LEVEL values (no offerings matched), treat as Mixed/Other
logic = (
    school_grad.groupby('SCHOOL_CODE')['GRADUATE_LEVEL']
      .agg(lambda s: ('Graduate' if (s == 'Graduate').any() else ('Not for graduate credit' if len(s)>0 and (s.replace({'Not for graduate credit':'NFG'}).isin(['Not for graduate credit'])).all() else 'Mixed/Other')))
      .reset_index()
      .rename(columns={'GRADUATE_LEVEL':'SCHOOL_GRADUATE_LEVEL'})
)

# 7) One row per school with school name and DLC key: DLC_KEY is department-level; preserve but cannot aggregate meaningfully across multiple depts.
# We will present DLC_KEY as null at school level unless there is a unique DLC per school (rare); collect none/ambiguous as null.
# Build school dimension from departments, choosing a canonical SCHOOL_NAME per SCHOOL_CODE.
school_dim = (
    pdpt[['SCHOOL_CODE','SCHOOL_NAME']]
        .dropna(subset=['SCHOOL_CODE'])
        .drop_duplicates()
)

# 8) Combine all school-level pieces
result = (
    school_dim
      .merge(subjects_per_school, on='SCHOOL_CODE', how='left')
      .merge(course_minmax, on='SCHOOL_CODE', how='left')
      .merge(depts_per_school, on='SCHOOL_CODE', how='left')
      .merge(logic, on='SCHOOL_CODE', how='left')
)

# 9) Add DLC_KEY: if a school has exactly one unique DLC_KEY across its departments, keep it; else set to None.
dlc_by_school = (
    pdpt[['SCHOOL_CODE','DLC_KEY']].dropna()
        .drop_duplicates()
        .groupby('SCHOOL_CODE')['DLC_KEY']
        .agg(lambda s: s.iloc[0] if s.nunique()==1 else None)
        .reset_index()
)
result = result.merge(dlc_by_school, on='SCHOOL_CODE', how='left')

# Final columns in requested order
final = result[['SCHOOL_CODE','SCHOOL_NAME','DLC_KEY','SCHOOL_GRADUATE_LEVEL','TOTAL_SIS_SUBJECTS','MIN_COURSE_NUMBER','MAX_COURSE_NUMBER','TOTAL_DEPARTMENTS_OFFERING_SUBJECTS']].sort_values('SCHOOL_CODE')

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
