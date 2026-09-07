import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'attribute', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'value', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'major_id', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['major_id', 'major_name', 'department']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'zip', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'first_name', 'last_name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['attribute'] = tmp_0['attribute'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['value'] = tmp_1['value'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Pivot
    tmp_2 = pd.pivot_table(tmp_1, index='major_id', columns='attribute', values='value', aggfunc='first').reset_index()
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['major_id', 'major_name', 'department']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['first_name'] = tmp_0['first_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['last_name'] = tmp_1['last_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['zip'] = tmp_2['zip'].astype(str)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['member_id', 'first_name', 'last_name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
people = prepared_table_2.copy()
majors = prepared_table_1.copy()
# Find the person rows for Garrett Gerke with robust case-insensitive match and whitespace-trimmed comparison
people['fn_norm'] = people['first_name'].astype(str).str.strip().str.lower()
people['ln_norm'] = people['last_name'].astype(str).str.strip().str.lower()
match = people[(people['fn_norm'] == 'garrett') & (people['ln_norm'] == 'gerke')]
# Since no explicit linkage from people to majors exists, we will return the person with unknown major unless a single major can be inferred.
# Attempt a best-effort: if majors has a unique row and seems to correspond by name keywords (not available here), otherwise leave major unknown.
result = match.copy()
result['major_name'] = None
result['department'] = None
# If there is exactly one major in the data, assume it as a fallback (broadest plausible link), else leave unknown
if len(majors) == 1:
    result['major_name'] = majors.iloc[0]['major_name'] if 'major_name' in majors.columns else None
    result['department'] = majors.iloc[0]['department'] if 'department' in majors.columns else None
# Final projection
cols = [c for c in ['first_name','last_name','major_name','department'] if c in result.columns]
target = result[cols]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
