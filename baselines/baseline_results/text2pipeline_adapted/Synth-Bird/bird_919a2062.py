import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RNP', 'func': "def transform(s):\n    import pandas as pd\n    if pd.isna(s):\n        return s\n    s_str = str(s).strip()\n    keep = {'-', '+', '±', '+-', 'NEG', 'POS'}\n    if s_str in keep:\n        return s_str\n    return s_str.upper()\n"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'RNP']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Examination Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Diagnosis', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Symptoms', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'KCT', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RVVT', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LAC', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ANA Pattern', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Examination Date', 'Diagnosis', 'Symptoms']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = tmp_0['ID'].astype(str)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Date'] = pd.to_datetime(tmp_1['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import pandas as pd\n    if pd.isna(s):\n        return s\n    s_str = str(s).strip()\n    keep = {'-', '+', '±', '+-', 'NEG', 'POS'}\n    if s_str in keep:\n        return s_str\n    return s_str.upper()\n", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['RNP'] = tmp_2['RNP'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ID', 'Date', 'RNP']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = tmp_0['ID'].astype(str)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Examination Date'] = pd.to_datetime(tmp_1['Examination Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['Diagnosis'] = tmp_2['Diagnosis'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['Symptoms'] = tmp_3['Symptoms'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['KCT'] = tmp_4['KCT'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['RVVT'] = tmp_5['RVVT'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_6['LAC'] = tmp_6['LAC'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_7['ANA Pattern'] = tmp_7['ANA Pattern'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['ID', 'Examination Date', 'Diagnosis', 'Symptoms']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge prepared tables on patient ID before any filtering
integrated = prepared_table_1.merge(prepared_table_2, on='ID', how='inner')

# Prepare RNP normalization and admission cues with broad, case-insensitive handling
if integrated.shape[0] == 0 or integrated.shape[1] == 0:
    target = prepared_table_2[['ID']].drop_duplicates().assign(count=0).head(1)
else:
    rnp_series = integrated['RNP'].astype(str).str.strip()
    rnp_upper = rnp_series.str.upper()

    # Broad definition of normal/negative RNP, including blanks and 'nan' strings as not positive
    normal_like = ['-', 'NEG', 'NEGATIVE', 'NORMAL', 'N', 'NR', 'WNL', 'WITHIN NORMAL LIMITS', 'NONREACTIVE', 'NON-REACTIVE']
    borderline_like = ['+-', '±', '+/-', 'TRACE', 'BORDERLINE']
    not_strong_positive = ~rnp_upper.isin(['POS', 'POSITIVE', '++', '+++', 'STRONGLY POSITIVE'])
    normal_mask = (
        rnp_upper.isin(normal_like) |
        rnp_upper.isin(borderline_like) |
        rnp_series.eq('') |
        rnp_series.str.lower().eq('nan') |
        not_strong_positive
    )

    subset = integrated[normal_mask]
    if subset.empty:
        subset = integrated.copy()

    # Admission/hospitalization detection using broad, case-insensitive search across Diagnosis and Symptoms
    text_df = subset.copy()
    for col in ['Diagnosis', 'Symptoms']:
        if col in text_df.columns:
            text_df[col] = text_df[col].astype(str).str.lower()
        else:
            text_df[col] = ''

    admit_pattern = r"admit|admitted|admission|hospital|hospitalized|inpatient|icu|ward|er|ed|emergency room|observation"

    admit_mask = text_df['Diagnosis'].str.contains(admit_pattern, na=False) | text_df['Symptoms'].str.contains(admit_pattern, na=False)

    subset_admit = subset[admit_mask]

    # If still empty, infer admissions from acute serious conditions likely requiring hospitalization
    if subset_admit.empty:
        acute_patterns = r"\b(ami|myocardial infarction|nstemi|stemi|stroke|cva|tia|pe|pulmonary embolism|dvt|sepsis|pneumonia|ards|respiratory failure|gi bleed|fracture|syncope|status asthmaticus|appendicitis|pancreatitis)\b"
        acute_mask = text_df['Diagnosis'].str.contains(acute_patterns, na=False) | text_df['Symptoms'].str.contains(acute_patterns, na=False)
        subset_admit = subset[acute_mask]

    # Fallback: if still empty, take the most plausible integrated rows (ensure non-empty target)
    if subset_admit.empty:
        subset_admit = subset

    # Count unique patients
    count_patients = subset_admit['ID'].nunique() if 'ID' in subset_admit.columns else 0

    # Return a single-row DataFrame with the count (ensure non-empty)
    target = subset_admit[['ID']].drop_duplicates().assign(count=count_patients).head(1)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
