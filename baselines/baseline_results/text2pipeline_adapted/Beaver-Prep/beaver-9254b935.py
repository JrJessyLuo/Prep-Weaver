import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'IS_NO_COURSE_MATERIAL', 'NUM_ENROLLED_STUDENTS', 'OFFER_SCHOOL_NAME']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'subject_id', 'new_name': 'SUBJECT_ID'}, {'old_name': 'TERM_CODE', 'new_name': 'TERM_CODE'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RECORD_COUNT', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'TIP_MATERIAL_STATUS_KEY', 'TIP_MATERIAL_KEY', 'RECORD_COUNT']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_6', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_0['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'IS_NO_COURSE_MATERIAL', 'NUM_ENROLLED_STUDENTS', 'OFFER_SCHOOL_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'subject_id': 'SUBJECT_ID', 'TERM_CODE': 'TERM_CODE'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['RECORD_COUNT'] = pd.to_numeric(tmp_1['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'TIP_MATERIAL_STATUS_KEY', 'TIP_MATERIAL_KEY', 'RECORD_COUNT']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t12 = prepared_table_2.merge(prepared_table_1, on=['TERM_CODE','SUBJECT_ID'], how='left')
# Bring in materials info by TIP_SUBJECT_OFFERED_KEY; keep left rows
t123 = t12.merge(prepared_table_3[['TIP_SUBJECT_OFFERED_KEY','TIP_MATERIAL_STATUS_KEY']], on='TIP_SUBJECT_OFFERED_KEY', how='left')
# Derive flags
# materials_needed: True if IS_NO_COURSE_MATERIAL not explicitly indicates no materials and/or TIP_MATERIAL_STATUS_KEY not NM
materials_flag = (~t123['IS_NO_COURSE_MATERIAL'].fillna('').str.strip().str.upper().isin(['Y','YES','TRUE','1','T'])) & (~t123['TIP_MATERIAL_STATUS_KEY'].fillna('').str.upper().eq('NM'))
t123 = t123.assign(materials_needed=materials_flag)
# Group by term to compute requested metrics
agg = t123.groupby('TERM_CODE').agg(
    total_tip_subject_types=('TIP_SUBJECT_OFFERED_KEY', 'nunique'),
    total_materials_needed=('materials_needed', 'sum'),
    min_enrolled=('NUM_ENROLLED_STUDENTS', 'min'),
    max_enrolled=('NUM_ENROLLED_STUDENTS', 'max'),
    total_schools_offering_subjects=('OFFER_SCHOOL_NAME', 'nunique'),
    total_records=('TIP_SUBJECT_OFFERED_KEY', 'count')
).reset_index()
# Derive term description and whether current: infer from TERM_CODE pattern (e.g., 2024SP -> Spring 2024). 'Current' cannot be reliably known from these tables; set to unknown.
term_map = {'FA':'Fall','SP':'Spring','JA':'IAP','SU':'Summer'}
season = agg['TERM_CODE'].str[-2:]
year = agg['TERM_CODE'].str[:4]
term_desc = season.map(term_map).fillna(season) + ' ' + year
agg['TERM_DESCRIPTION'] = term_desc
agg['IS_CURRENT_TERM'] = 'Unknown'
# Final projection and ordering
cols = ['TERM_CODE','TERM_DESCRIPTION','IS_CURRENT_TERM','total_tip_subject_types','total_materials_needed','min_enrolled','max_enrolled','total_schools_offering_subjects','total_records']
target = agg[cols].sort_values('TERM_CODE')

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
