import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Concatenate', 'params': {'concatenate_columns': ['prefix', 'id_core', 'suffix'], 'target_column': 'patient_id_raw', 'func': "def transform(row):\n    a = '' if row['prefix'] is None else str(row['prefix'])\n    b = '' if row['id_core'] is None else str(row['id_core'])\n    c = '' if row['suffix'] is None else str(row['suffix'])\n    return a + b + c"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'patient_id_raw', 'func': 'def transform(s):\n    s = \'\' if s is None else str(s)\n    return s.replace(\'"\',\'\').strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'patient_id_raw', 'new_name': 'patient_id'}, {'old_name': 'attr', 'new_name': 'attribute'}, {'old_name': 'val', 'new_name': 'value'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute', 'func': "def transform(s):\n    return '' if s is None else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'value', 'func': "def transform(s):\n    return '' if s is None else str(s).strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['patient_id', 'attribute', 'value']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ID', 'new_name': 'patient_id'}]}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['patient_id', 'Date', 'UA']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Concatenate
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(row):\n    a = '' if row['prefix'] is None else str(row['prefix'])\n    b = '' if row['id_core'] is None else str(row['id_core'])\n    c = '' if row['suffix'] is None else str(row['suffix'])\n    return a + b + c", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_0['patient_id_raw'] = tmp_0[['prefix', 'id_core', 'suffix']].apply(_concat_func_1, axis=1)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = \'\' if s is None else str(s)\n    return s.replace(\'"\',\'\').strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['patient_id_raw'] = tmp_1['patient_id_raw'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'patient_id_raw': 'patient_id', 'attr': 'attribute', 'val': 'value'})
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return '' if s is None else str(s).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['attribute'] = tmp_3['attribute'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec("def transform(s):\n    return '' if s is None else str(s).strip()", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['value'] = tmp_4['value'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['patient_id', 'attribute', 'value']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = tmp_0['ID'].astype(str)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'ID': 'patient_id'})
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Date'] = pd.to_datetime(tmp_2['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['patient_id', 'Date', 'UA']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='patient_id', how='left')
# Identify gender from attribute-value pairs; robust case-insensitive match
mask_gender_attr = integrated['attribute'].str.contains('sex|gender', case=True, regex=True, na=False)
sex_map_series = integrated.loc[mask_gender_attr, ['patient_id', 'value']].copy()
# Normalize gender value strings broadly
sex_map_series['sex_norm'] = sex_map_series['value'].astype(str).str.strip().str.lower()
# Map common encodings to Male/Female
male_terms = ['m', 'male', 'man', 'boy']
female_terms = ['f', 'female', 'woman', 'girl']
sex_map_series['sex'] = sex_map_series['sex_norm'].apply(lambda x: 'Male' if any(t==x or x.startswith(t) for t in male_terms) else ('Female' if any(t==x or x.startswith(t) for t in female_terms) else None))
# Deduplicate to one sex per patient by first non-null
sex_map = sex_map_series.dropna(subset=['sex']).drop_duplicates(subset=['patient_id'], keep='first')[['patient_id','sex']]
# Attach sex back to lab rows (many rows per patient by date)
integrated2 = prepared_table_2.merge(sex_map, on='patient_id', how='left')
# Determine abnormal UA. Use common adult reference ranges: Male 3.4-7.0 mg/dL, Female 2.4-6.0 mg/dL. If sex unknown, use a broad 2.4-7.0 to avoid over-filtering.
ua = integrated2['UA']
sex = integrated2['sex']
# Build boolean for abnormal per row
lower_m = 3.4
upper_m = 7.0
lower_f = 2.4
upper_f = 6.0
lower_u = 2.4
upper_u = 7.0
is_m = sex == 'Male'
is_f = sex == 'Female'
is_u = sex.isna()
abn_m = is_m & ((ua < lower_m) | (ua > upper_m))
abn_f = is_f & ((ua < lower_f) | (ua > upper_f))
abn_u = is_u & ((ua < lower_u) | (ua > upper_u))
integrated2['abnormal_ua'] = abn_m | abn_f | abn_u
# Among abnormal UA rows, count distinct patients by sex
abn = integrated2[integrated2['abnormal_ua']].copy()
# Keep one record per patient to avoid multiple counts
abn_unique = abn.drop_duplicates(subset=['patient_id'])
# Count by sex; unknown sex will not contribute to male/female ratio
counts = abn_unique.groupby('sex', dropna=False).size().rename('count').reset_index()
male_count = int(counts.loc[counts['sex']=='Male', 'count'].sum())
female_count = int(counts.loc[counts['sex']=='Female', 'count'].sum())
# Build a one-row result with the ratio as M:F string and numeric components
ratio_str = f"{male_count}:{female_count}" if female_count != 0 else f"{male_count}:0"
target = counts.copy()
# Create a tidy output with total abnormal patients and ratio
total_abn_patients = len(abn_unique['patient_id'].unique())
summary = []
summary.append({'metric':'male_count','value':male_count})
summary.append({'metric':'female_count','value':female_count})
summary.append({'metric':'total_abnormal_patients','value':total_abn_patients})
summary.append({'metric':'male_to_female_ratio','value':ratio_str})
target = pd.DataFrame(summary)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
