import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Examination Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Diagnosis', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Examination Date', 'new_name': 'exam_date'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'exam_date', 'Diagnosis']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Date', 'new_name': 'lab_date'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'lab_date']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ID'] = tmp_1['ID'].astype(str)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Examination Date'] = pd.to_datetime(tmp_2['Examination Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['Diagnosis'] = tmp_3['Diagnosis'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'Examination Date': 'exam_date'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['ID', 'exam_date', 'Diagnosis']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = tmp_0['ID'].astype(str)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Date'] = pd.to_datetime(tmp_1['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'Date': 'lab_date'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ID', 'lab_date']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
patient_id = '30609'
# Join prepared tables on patient ID to combine diagnosis context with lab dates
integrated = prepared_table_1.merge(prepared_table_2, on='ID', how='inner')
# Filter for the requested patient ID using robust matching on the string ID
subset = integrated[integrated['ID'].str.strip() == patient_id]
# If no rows due to absence of lab records after join, fall back to diagnosis-only rows and then left join to lab dates
if subset.empty:
    diag_only = prepared_table_1[prepared_table_1['ID'].str.strip() == patient_id]
    integrated_fallback = diag_only.merge(prepared_table_2, on='ID', how='left')
    subset = integrated_fallback
# Aggregate: list unique lab dates for the patient while preserving diagnosis text (assume single diagnosis row or consistent text)
if not subset.empty:
    diagnosis_vals = subset['Diagnosis'].dropna().unique()
    diagnosis = diagnosis_vals[0] if len(diagnosis_vals) > 0 else None
    dates = subset['lab_date'].dropna().astype(str).sort_values().unique().tolist()
    target = subset.head(0).assign(ID=patient_id, Diagnosis=diagnosis, lab_date_list=[dates])
else:
    # As a last resort, return the patient ID with empty results
    target = prepared_table_1.head(0).assign(ID=patient_id, Diagnosis=None, lab_date_list=[[]])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
