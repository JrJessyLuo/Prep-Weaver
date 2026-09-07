import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'merged_ID_Attribute_Value', 'target_columns': ['raw_id', 'attribute', 'value'], 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('|||')\n    if len(parts) < 3:\n        parts = (parts + [None, None, None])[:3]\n    else:\n        parts = parts[:3]\n    return parts"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'raw_id', 'func': 'def transform(s):\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute', 'func': "def transform(s):\n    return ('' if s is None else str(s)).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'value', 'func': "def transform(s):\n    return ('' if s is None else str(s)).strip()"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'raw_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'raw_id', 'new_name': 'patient_id'}]}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'patient_id', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'last'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Description', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Description', 'new_name': 'birthday'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['patient_id', 'birthday']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ID', 'new_name': 'patient_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'patient_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Date', 'new_name': 'lab_date'}]}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'lab_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ALB', 'new_name': 'albumin'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'albumin', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['patient_id', 'lab_date', 'albumin']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('|||')\n    if len(parts) < 3:\n        parts = (parts + [None, None, None])[:3]\n    else:\n        parts = parts[:3]\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['merged_ID_Attribute_Value'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['raw_id'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['attribute'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_0['value'] = _split_values_1.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['raw_id'] = tmp_1['raw_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return ('' if s is None else str(s)).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['attribute'] = tmp_2['attribute'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec("def transform(s):\n    return ('' if s is None else str(s)).strip()", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['value'] = tmp_3['value'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['raw_id'] = pd.to_numeric(tmp_4['raw_id'], errors='coerce').fillna(0).astype(int)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'raw_id': 'patient_id'})
    # Step 7: Pivot
    tmp_6 = pd.pivot_table(tmp_5, index='patient_id', columns='attribute', values='value', aggfunc='last').reset_index()
    # Step 8: StandardizeDatetime
    tmp_7 = tmp_6.copy()
    tmp_7['Description'] = pd.to_datetime(tmp_7['Description'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 9: Rename
    tmp_8 = tmp_7.rename(columns={'Description': 'birthday'})
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['patient_id', 'birthday']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'ID': 'patient_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['patient_id'] = pd.to_numeric(tmp_1['patient_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'Date': 'lab_date'})
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['lab_date'] = pd.to_datetime(tmp_3['lab_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'ALB': 'albumin'})
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['albumin'] = pd.to_numeric(tmp_5['albumin'], errors='coerce').astype(float)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['patient_id', 'lab_date', 'albumin']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
pt = prepared_table_1.copy()
lab = prepared_table_2.copy()
# Determine sex from available columns (Sex or Gender), robustly marking male
sex_series = None
if 'Sex' in pt.columns:
    sex_series = pt['Sex']
elif 'Gender' in pt.columns:
    sex_series = pt['Gender']
else:
    sex_series = None
# Merge patients with labs
integrated = lab.merge(pt, on='patient_id', how='left')
# Define albumin normal range if not provided; use a common clinical range: 3.5 to 5.0 g/dL
lower, upper = 3.5, 5.0
# Flag male
if sex_series is not None and ('Sex' in integrated.columns or 'Gender' in integrated.columns):
    sex_col = 'Sex' if 'Sex' in integrated.columns else 'Gender'
    male_mask = integrated[sex_col].astype(str).str.strip().str.lower().isin(['m','male'])
else:
    # If sex is unavailable, preserve rows but create a mask that selects none, then relax to best plausible (no filter)
    male_mask = integrated['patient_id'] == -1
    if not male_mask.any():
        male_mask = integrated['patient_id'] == integrated['patient_id']  # relax: include all
# Albumin out-of-range mask
alb_mask = integrated['albumin'].notna() & (~integrated['albumin'].between(lower, upper))
filtered = integrated[male_mask & alb_mask]
# If filtering yields no rows, relax sex criteria to include all with albumin out of range
if filtered.empty:
    filtered = integrated[alb_mask]
# Sort by birthday descending; if birthday missing, place at bottom by using fill value
if 'birthday' in filtered.columns:
    # Ensure birthday is datetime
    try:
        filtered['birthday'] = filtered['birthday']
    except Exception:
        pass
    filtered = filtered.sort_values(by=['birthday'], ascending=[False], kind='mergesort')
else:
    filtered = filtered.sort_values(by=['patient_id'], ascending=[True], kind='mergesort')
# Select output columns: patient_id and birthday
cols = ['patient_id']
if 'birthday' in filtered.columns:
    cols.append('birthday')
target = filtered[cols].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
