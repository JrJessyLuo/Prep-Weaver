import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'ID', 'target_columns': ['patient_id'], 'func': 'def transform(s):\n    import pandas as pd\n    def to_int(v):\n        if pd.isna(v):\n            return None\n        v = str(v).strip().strip(\'"\')\n        if v == \'\' or v.lower() == \'nan\':\n            return None\n        try:\n            return int(v)\n        except Exception:\n            return None\n    return [to_int(x) for x in s]'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Description', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'First Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'patient_id', 'new_name': 'patient_id'}, {'old_name': 'Description', 'new_name': 'visit_date_primary'}, {'old_name': 'First Date', 'new_name': 'visit_date_alt'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['patient_id', 'visit_date_primary', 'visit_date_alt']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SSA', 'func': "def transform(s):\n    import math\n    if s is None:\n        return None\n    try:\n        if isinstance(s, float) and math.isnan(s):\n            return None\n    except Exception:\n        pass\n    s_str = str(s).strip()\n    if s_str == '' or s_str.lower() in {'nan', 'none', 'null'}:\n        return None\n    low = s_str.lower().strip()\n    low = low.replace('\\u2212', '-')  # normalize unicode minus to ASCII\n    negatives = {'-', 'neg', 'negative', 'n', '+-', '0', 'normal', 'neg.'}\n    if low in negatives:\n        return 'normal'\n    return s_str"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ID', 'new_name': 'patient_id'}, {'old_name': 'Date', 'new_name': 'lab_date'}]}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SSA', 'target_columns': ['ssa_raw', 'ssa_status'], 'func': "def transform(s):\n    import math\n    raw = s\n    # compute status with same logic as above\n    if s is None:\n        return [raw, None]\n    try:\n        if isinstance(s, float) and math.isnan(s):\n            return [raw, None]\n    except Exception:\n        pass\n    s_str = str(s).strip()\n    if s_str == '' or s_str.lower() in {'nan', 'none', 'null'}:\n        return [raw, None]\n    low = s_str.lower().strip().replace('\\u2212', '-')\n    negatives = {'-', 'neg', 'negative', 'n', '+-', '0', 'normal', 'neg.'}\n    status = 'normal' if low in negatives else s_str\n    return [raw, status]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['patient_id', 'lab_date', 'ssa_raw', 'ssa_status']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import pandas as pd\n    def to_int(v):\n        if pd.isna(v):\n            return None\n        v = str(v).strip().strip(\'"\')\n        if v == \'\' or v.lower() == \'nan\':\n            return None\n        try:\n            return int(v)\n        except Exception:\n            return None\n    return [to_int(x) for x in s]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['ID'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['patient_id'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Description'] = pd.to_datetime(tmp_1['Description'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['First Date'] = pd.to_datetime(tmp_2['First Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'patient_id': 'patient_id', 'Description': 'visit_date_primary', 'First Date': 'visit_date_alt'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['patient_id', 'visit_date_primary', 'visit_date_alt']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Date'] = pd.to_datetime(tmp_1['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import math\n    if s is None:\n        return None\n    try:\n        if isinstance(s, float) and math.isnan(s):\n            return None\n    except Exception:\n        pass\n    s_str = str(s).strip()\n    if s_str == '' or s_str.lower() in {'nan', 'none', 'null'}:\n        return None\n    low = s_str.lower().strip()\n    low = low.replace('\\u2212', '-')  # normalize unicode minus to ASCII\n    negatives = {'-', 'neg', 'negative', 'n', '+-', '0', 'normal', 'neg.'}\n    if low in negatives:\n        return 'normal'\n    return s_str", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['SSA'] = tmp_2['SSA'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'ID': 'patient_id', 'Date': 'lab_date'})
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import math\n    raw = s\n    # compute status with same logic as above\n    if s is None:\n        return [raw, None]\n    try:\n        if isinstance(s, float) and math.isnan(s):\n            return [raw, None]\n    except Exception:\n        pass\n    s_str = str(s).strip()\n    if s_str == '' or s_str.lower() in {'nan', 'none', 'null'}:\n        return [raw, None]\n    low = s_str.lower().strip().replace('\\u2212', '-')\n    negatives = {'-', 'neg', 'negative', 'n', '+-', '0', 'normal', 'neg.'}\n    status = 'normal' if low in negatives else s_str\n    return [raw, status]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_4['SSA'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['ssa_raw'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['ssa_status'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['patient_id', 'lab_date', 'ssa_raw', 'ssa_status']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Ensure compatible key types before merging
pt1 = prepared_table_1.copy()
pt2 = prepared_table_2.copy()

# Normalize patient_id types to string for both tables
pt1['patient_id'] = pt1['patient_id'].astype(str)
pt2['patient_id'] = pt2['patient_id'].astype(str)

# Merge visit info with lab info
merged = pt1.merge(pt2, how='inner', on='patient_id')

# Parse dates
for col in ['visit_date_primary', 'visit_date_alt', 'lab_date']:
    merged[col] = pd.to_datetime(merged[col], errors='coerce')

# Determine each patient's arrival date using primary then alt
merged['arrival_date'] = merged['visit_date_primary']
missing_mask = merged['arrival_date'].isna()
merged.loc[missing_mask, 'arrival_date'] = merged.loc[missing_mask, 'visit_date_alt']

# Define normal SSA using broad, case-insensitive matching
ssa_norm = merged['ssa_status'].astype(str).str.strip().str.lower()
raw = merged['ssa_raw'].astype(str).str.strip().str.lower()

normal_tokens = {'-', '−', 'neg', 'negative', 'n', 'normal', '+-', '0', 'within normal limits', 'wnl', 'nrml'}
normal_flag = ssa_norm.str.contains('normal|neg|wnl', na=False) | raw.isin(normal_tokens) | raw.str.contains('normal|neg|wnl', na=False)

# Patients with at least one normal SSA
patients_normal = merged.loc[normal_flag, ['patient_id']].drop_duplicates()

# Bring back arrival dates per patient (first available)
arrivals = merged[['patient_id', 'arrival_date']].sort_values(['patient_id', 'arrival_date']).drop_duplicates('patient_id')
patients_normal = patients_normal.merge(arrivals, how='left', on='patient_id')

# Filter arrival before 2000-01-01; fallback to any lab before 2000 if arrival missing
cutoff = pd.Timestamp('2000-01-01')
before_cutoff = patients_normal['arrival_date'].notna() & (patients_normal['arrival_date'] < cutoff)

fallback = patients_normal['arrival_date'].isna()
if fallback.any():
    early_lab = merged.loc[merged['lab_date'].notna() & (merged['lab_date'] < cutoff), ['patient_id']].drop_duplicates()
    patients_normal = patients_normal.merge(early_lab.assign(early_lab_before2000=True), how='left', on='patient_id')
    before_cutoff = before_cutoff | (patients_normal['early_lab_before2000'] == True)

# Count distinct patients meeting the condition
count_df = patients_normal.loc[before_cutoff, ['patient_id']].drop_duplicates()

target = pd.DataFrame({'count_normal_ssa_before_2000': [len(count_df)]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
