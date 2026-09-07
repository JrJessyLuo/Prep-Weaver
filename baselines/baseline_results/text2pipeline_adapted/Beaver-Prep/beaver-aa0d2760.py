import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TIP_MATERIAL_STATUS_KEY', 'new_name': 'tip_material_status_key'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RECORD_COUNT', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status_key', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    s = s.strip()\n    return None if s == "" or s.lower() == "nan" else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['tip_material_status_key', 'TIP_MATERIAL_KEY', 'RECORD_COUNT']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status_key', 'func': "def transform(s):\n    s = None if s is None else str(s)\n    if s is None:\n        return None\n    s = s.strip()\n    if s == '' or s.lower() in {'nan', 'none', 'null'}:\n        return None\n    return s.lower()\n"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS', 'func': "def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    if s == '' or s.lower() in {'nan', 'none', 'null'}:\n        return None\n    return s\n"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['tip_material_status_key', 'TIP_MATERIAL_STATUS']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'NUM_ENROLLED_STUDENTS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'TIP_MATERIAL_STATUS_KEY': 'tip_material_status_key'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['RECORD_COUNT'] = pd.to_numeric(tmp_1['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    s = s.strip()\n    return None if s == "" or s.lower() == "nan" else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['tip_material_status_key'] = tmp_2['tip_material_status_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['tip_material_status_key', 'TIP_MATERIAL_KEY', 'RECORD_COUNT']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = None if s is None else str(s)\n    if s is None:\n        return None\n    s = s.strip()\n    if s == '' or s.lower() in {'nan', 'none', 'null'}:\n        return None\n    return s.lower()\n", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['tip_material_status_key'] = tmp_0['tip_material_status_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    if s == '' or s.lower() in {'nan', 'none', 'null'}:\n        return None\n    return s\n", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TIP_MATERIAL_STATUS'] = tmp_1['TIP_MATERIAL_STATUS'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['tip_material_status_key', 'TIP_MATERIAL_STATUS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_0['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'NUM_ENROLLED_STUDENTS']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
m1 = prepared_table_1.copy()
# Bring in status labels
m1_labeled = m1.merge(prepared_table_2, on='tip_material_status_key', how='left')

# Normalize display label: null key or null label -> 'No material status'
m1_labeled['material_status_display'] = m1_labeled['TIP_MATERIAL_STATUS']
m1_labeled.loc[m1_labeled['material_status_display'].isna(), 'material_status_display'] = 'No material status'

# Prepare enrollment by TIP_SUBJECT_OFFERED_KEY from table_3
# Aggregate enrollment at the subject offering level to avoid double counting when joining
enr = prepared_table_3.groupby('TIP_SUBJECT_OFFERED_KEY', as_index=False)['NUM_ENROLLED_STUDENTS'].sum().rename(columns={'NUM_ENROLLED_STUDENTS':'ENROLLMENT'})

# Join enrollment to materials by TIP_SUBJECT_OFFERED_KEY if present; rows without a matching key will have NaN enrollment which we treat as 0 in sums
m_full = m1_labeled.merge(enr, on='TIP_SUBJECT_OFFERED_KEY', how='left') if 'TIP_SUBJECT_OFFERED_KEY' in m1_labeled.columns else m1_labeled.assign(ENROLLMENT=None)

# Compute per-status aggregates
agg = m_full.groupby('material_status_display', as_index=False).agg(
    total_unique_materials=('TIP_MATERIAL_KEY', 'nunique'),
    total_records=('RECORD_COUNT', 'sum'),
    total_student_enrollment=('ENROLLMENT', 'sum')
)
# Replace NaN enrollments with 0
agg['total_student_enrollment'] = agg['total_student_enrollment'].fillna(0).astype(int)
agg['total_records'] = agg['total_records'].fillna(0).astype(int)

# Grand total row
grand = agg.agg({
    'total_unique_materials': 'sum',
    'total_records': 'sum',
    'total_student_enrollment': 'sum'
}).to_frame().T
grand.insert(0, 'material_status_display', 'Grand Total')

# Concatenate and final projection
target = (
    pd.concat([agg, grand], ignore_index=True)[[
        'material_status_display', 'total_unique_materials', 'total_records', 'total_student_enrollment'
    ]]
)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
