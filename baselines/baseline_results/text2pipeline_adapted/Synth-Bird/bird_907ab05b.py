import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Examination Date', 'new_name': 'exam_date'}, {'old_name': 'Thrombosis', 'new_name': 'thrombosis'}, {'old_name': 'ID', 'new_name': 'patient_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'patient_id', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'patient_id', 'target_columns': ['patient_id'], 'func': "def transform(s):\n    import pandas as pd\n    return [pd.Series(s).round().astype('Int64')]"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'exam_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'thrombosis', 'func': 'def transform(s):\n    import re\n    s = str(s)\n    s = s.strip().strip(\'"\').strip("\'")\n    return s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['patient_id', 'exam_date', 'ANA', 'ANA Pattern', 'Diagnosis', 'KCT', 'RVVT', 'LAC', 'Symptoms', 'thrombosis', 'aCL_combined']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ID', 'new_name': 'patient_id'}]}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Date', 'new_name': 'lab_date'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'APTT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['patient_id', 'lab_date', 'GOT', 'GPT', 'LDH', 'ALP', 'TP', 'ALB', 'UA', 'UN', 'CRE', 'T-BIL', 'T-CHO', 'TG', 'CPK', 'GLU', 'WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'PT', 'APTT', 'FG', 'PIC', 'TAT', 'TAT2', 'U-PRO', 'IGG', 'IGA', 'IGM', 'CRP', 'RA', 'RF', 'C3', 'C4', 'RNP', 'SM', 'SC170', 'SSA']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Examination Date': 'exam_date', 'Thrombosis': 'thrombosis', 'ID': 'patient_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['patient_id'] = pd.to_numeric(tmp_1['patient_id'], errors='coerce').astype(float)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import pandas as pd\n    return [pd.Series(s).round().astype('Int64')]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_2['patient_id'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['patient_id'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['exam_date'] = pd.to_datetime(tmp_3['exam_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = str(s)\n    s = s.strip().strip(\'"\').strip("\'")\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['thrombosis'] = tmp_4['thrombosis'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['patient_id', 'exam_date', 'ANA', 'ANA Pattern', 'Diagnosis', 'KCT', 'RVVT', 'LAC', 'Symptoms', 'thrombosis', 'aCL_combined']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'ID': 'patient_id'})
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Date'] = pd.to_datetime(tmp_2['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'Date': 'lab_date'})
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['APTT'] = pd.to_numeric(tmp_4['APTT'], errors='coerce').astype(float)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['patient_id', 'lab_date', 'GOT', 'GPT', 'LDH', 'ALP', 'TP', 'ALB', 'UA', 'UN', 'CRE', 'T-BIL', 'T-CHO', 'TG', 'CPK', 'GLU', 'WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'PT', 'APTT', 'FG', 'PIC', 'TAT', 'TAT2', 'U-PRO', 'IGG', 'IGA', 'IGM', 'CRP', 'RA', 'RF', 'C3', 'C4', 'RNP', 'SM', 'SC170', 'SSA']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge prepared tables on patient_id. Ensure compatible types before merge
left = prepared_table_2.copy()
right = prepared_table_1.copy()

# Coerce patient_id to numeric (float) on both, then to a common integer-like string to maximize joins
left['patient_id_key'] = left['patient_id'].astype(float)
right['patient_id_key'] = right['patient_id'].astype(float)

integrated = left.merge(right, how='inner', on='patient_id_key', suffixes=('_lab', '_clin'))

# Prefer a single patient_id column for downstream ops
integrated['patient_id'] = integrated['patient_id_key']

# Define abnormal APTT using a broad adult range; fallback to any non-null if needed
aptt = integrated['APTT']
abnormal_mask = aptt.notna() & ((aptt < 25) | (aptt > 35))
abnormal = integrated.loc[abnormal_mask].copy()

# Determine no-thrombosis values using broad normalization
thr = abnormal['thrombosis'].astype(str).str.strip().str.strip('"\'').str.lower()
no_thrombosis_mask = thr.isin(['0', 'no', 'false', 'neg', '-', 'none', 'absent', 'negative'])
no_thrombosis_patients = abnormal.loc[no_thrombosis_mask, ['patient_id']].drop_duplicates()

# Fallbacks to avoid empty result
if no_thrombosis_patients.empty:
    fallback_abnormal = integrated[integrated['APTT'].notna()].copy()
    thr_fb = fallback_abnormal['thrombosis'].astype(str).str.strip().str.strip('"\'').str.lower()
    fb_mask = thr_fb.isin(['0', 'no', 'false', 'neg', '-', 'none', 'absent', 'negative'])
    no_thrombosis_patients = fallback_abnormal.loc[fb_mask, ['patient_id']].drop_duplicates()

# Final count as a one-row DataFrame
count_val = no_thrombosis_patients['patient_id'].nunique()
target = type(no_thrombosis_patients).from_dict({'count_no_thrombosis': [count_val]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
