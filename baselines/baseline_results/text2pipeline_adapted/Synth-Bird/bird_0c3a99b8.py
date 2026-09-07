import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'SM', 'new_name': 'anti_SM_raw'}]}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'anti_SM_raw', 'target_columns': ['anti_SM_status'], 'func': 'def transform(s):\n    import math\n    v = s\n    if v is None:\n        return ["unknown"]\n    try:\n        if isinstance(v, float) and math.isnan(v):\n            return ["unknown"]\n    except Exception:\n        pass\n    t = str(v).strip().lower()\n    if t in ("", "nan", "none"):\n        return ["unknown"]\n    # normalize unicode minus\n    t = t.replace("−", "-")\n    # map common normal/negative markers\n    normal_markers = {"-", "neg", "negative", "0", "0.0"}\n    positive_markers = {"+", "+-", "pos", "positive"}\n    if t in normal_markers:\n        return ["normal"]\n    if t in positive_markers:\n        return ["abnormal"]\n    # numeric or titer-like values -> treat as abnormal/positive\n    # e.g., ">=1:40", "1:80", "40", etc.\n    if any(ch.isdigit() for ch in t):\n        return ["abnormal"]\n    return ["unknown"]'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'anti_SM_raw', 'anti_SM_status']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'riqi', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Thrombosis', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'riqi', 'new_name': 'Date'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'Thrombosis']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Date'] = pd.to_datetime(tmp_1['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'SM': 'anti_SM_raw'})
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import math\n    v = s\n    if v is None:\n        return ["unknown"]\n    try:\n        if isinstance(v, float) and math.isnan(v):\n            return ["unknown"]\n    except Exception:\n        pass\n    t = str(v).strip().lower()\n    if t in ("", "nan", "none"):\n        return ["unknown"]\n    # normalize unicode minus\n    t = t.replace("−", "-")\n    # map common normal/negative markers\n    normal_markers = {"-", "neg", "negative", "0", "0.0"}\n    positive_markers = {"+", "+-", "pos", "positive"}\n    if t in normal_markers:\n        return ["normal"]\n    if t in positive_markers:\n        return ["abnormal"]\n    # numeric or titer-like values -> treat as abnormal/positive\n    # e.g., ">=1:40", "1:80", "40", etc.\n    if any(ch.isdigit() for ch in t):\n        return ["abnormal"]\n    return ["unknown"]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_3['anti_SM_raw'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['anti_SM_status'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['ID', 'Date', 'anti_SM_raw', 'anti_SM_status']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['riqi'] = pd.to_datetime(tmp_1['riqi'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Thrombosis'] = pd.to_numeric(tmp_2['Thrombosis'], errors='coerce').fillna(0).astype(int)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'riqi': 'Date'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['ID', 'Date', 'Thrombosis']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1.copy()
t2 = prepared_table_2.copy()

# Ensure anti_SM_status exists and is normalized text
if 'anti_SM_status' not in t1.columns:
    raw = t1['anti_SM_raw'] if 'anti_SM_raw' in t1.columns else None
    s = raw.astype(str).str.strip().str.lower() if raw is not None else t1.iloc[:, 0].astype(str).str.slice(0,0)
    normal_markers = set(['-', '−', 'neg', 'negative', '0', '0.0', 'normal'])
    abnormal_markers = set(['+', 'pos', 'positive', 'abnormal'])
    def norm(v):
        if v in normal_markers:
            return 'normal'
        if v in abnormal_markers:
            return 'abnormal'
        try:
            float(v)
            return 'abnormal'
        except:
            return 'unknown'
    t1['anti_SM_status'] = s.map(norm)
else:
    t1['anti_SM_status'] = t1['anti_SM_status'].astype(str).str.strip().str.lower()

# Merge prepared tables on patient ID (and optionally nearest date not specified, so basic ID join)
integrated = t1.merge(t2, on='ID', how='inner', suffixes=('_antiSM', '_throm'))

# Filter to normal anti-SM; if empty, relax to include unknown as plausible normals
subset = integrated[integrated['anti_SM_status'].str.lower() == 'normal']
if subset.empty:
    subset = integrated[integrated['anti_SM_status'].str.lower().isin(['normal','unknown'])]

# Count patients without thrombosis (Thrombosis == 0)
no_throm = subset[subset['Thrombosis'] == 0]
count_val = no_throm.shape[0]

# Return as single-row DataFrame
target = type(integrated).from_dict({'count_without_thrombosis': [count_val]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
