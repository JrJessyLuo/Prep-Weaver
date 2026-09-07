import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'MAX_ENROLLMENT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FEE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'IAP_SUBJECT_SESSION_KEY', 'FEE', 'MAX_ENROLLMENT']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'term_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_DESCRIPTION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['term_code', 'TERM_DESCRIPTION']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['MAX_ENROLLMENT'] = pd.to_numeric(tmp_0['MAX_ENROLLMENT'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['FEE'] = pd.to_numeric(tmp_1['FEE'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['TERM_CODE'] = tmp_2['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['TERM_CODE', 'IAP_SUBJECT_SESSION_KEY', 'FEE', 'MAX_ENROLLMENT']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['term_code'] = tmp_0['term_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TERM_DESCRIPTION'] = tmp_1['TERM_DESCRIPTION'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['term_code', 'TERM_DESCRIPTION']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
agg = prepared_table_1.copy()
# Count sessions per term. If there are duplicate rows per session, count distinct session keys.
agg_counts = agg.groupby('TERM_CODE', as_index=False).agg(
    TOTAL_IAP_SESSIONS=('IAP_SUBJECT_SESSION_KEY', 'nunique'),
    TOTAL_FEE_COLLECTED=('FEE', 'sum'),
    MIN_ENROLLMENT=('MAX_ENROLLMENT', 'min'),
    MAX_ENROLLMENT=('MAX_ENROLLMENT', 'max')
)
# Join term description
integrated = agg_counts.merge(prepared_table_2, left_on='TERM_CODE', right_on='term_code', how='left')
# Final projection and ordering
cols = ['TERM_CODE', 'TERM_DESCRIPTION', 'TOTAL_IAP_SESSIONS', 'TOTAL_FEE_COLLECTED', 'MIN_ENROLLMENT', 'MAX_ENROLLMENT']
# If TERM_DESCRIPTION missing, keep column with NaN; do not drop rows
integrated['TERM_DESCRIPTION'] = integrated['TERM_DESCRIPTION']
# Sort by TERM_CODE for readability
target = integrated[cols].sort_values(by=['TERM_CODE'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
